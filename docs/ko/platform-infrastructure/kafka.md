---
id: platform-infrastructure-kafka
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
knowledge_ids:
  - PIS2-06-01
  - PIS2-06-02
  - PIS2-06-03
  - PIS2-06-04
  - PIS2-06-05
  - PIS2-06-06
---

# Chapter 6. Kafka for Platform Systems

제공된 Basic Chapter 6의 학습 기록이다. 실제 Kafka 클러스터 구축·재할당·재시작을 수행한 운영 실적이 아니다. 선행 개념은 [이벤트 아키텍처](../data-platform/event-architecture.md), Kubernetes 배치와 유지보수는 [Kubernetes 운영](kubernetes-operations.md)에서 연결해 읽는다.

**본문 안내:** 원문 구역은 제공 자료의 문장·번호·도식·순서를 그대로 보존했다. 6.1·6.3의 ISR와 쓰기 승인 조건, 6.6의 StatefulSet·Strimzi 조건은 뒤의 **원문 절별 보완과 정정**을 함께 읽는다. 수치와 구성은 학습 예이며 이 환경에서 실행하거나 성능·복구를 시험하지 않았다.

<!-- SOURCE CORE START -->

> Kafka의 Broker / Topic / Partition / Producer / Consumer / Consumer Group / Offset / Ordering / 기본 semantics 등 개념은 Data Platform Basic에서 이미 학습한 것으로 간주한다. 이 Chapter에서는 Platform / Infrastructure 운영 관점만 다룬다.

## 6.1 Replication / ISR / Leader Election

핵심:

```text
Replication Factor
ISR
Leader
Leader Election
Under-Replicated Partition
```

### Replication Factor

```text
RF = 3

Broker A → Leader
Broker B → Follower
Broker C → Follower
```

### ISR

ISR = In-Sync Replicas.

> Leader 데이터를 충분히 잘 따라가고 있는 Replica 집합

예:

```text
ISR = A, B, C
```

Follower가 복제를 못 따라가면 ISR에서 빠질 수 있다.

### ISR이 중요한 이유

Follower가 존재한다고 무조건 안전한 Replica는 아니다.

```text
Leader offset = 1000
Follower B    = 999
Follower C    = 500
```

C처럼 크게 뒤처진 Replica는 최신 Leader 후보로 부적절할 수 있다.

### Leader Election

```text
Leader 장애
↓
Leader Election
↓
새 Leader
```

### Under-Replicated Partition

```text
RF = 3
ISR = 2
```

서비스가 살아 있어도 장애 내성이 줄어든 상태.

ISR에서 빠지는 대표 원인:

```text
Broker 장애
Network 문제
Disk 느림
CPU / Broker overload
```

---

## 6.2 Cluster Sizing / Capacity

핵심:

```text
Broker 수
Partition 수
Disk Capacity / Throughput
Network Throughput
```

### Disk Capacity

예:

```text
100GB/day
× 7 days
= 700GB raw
```

RF=3:

```text
700GB × 3
= 2.1TB
```

기본 감각:

```text
필요 Storage
≈ 일일 데이터량
× Retention 일수
× Replication Factor
+ 여유
```

### Disk Throughput

Kafka는 동시에:

```text
Producer Write
Replication Write
Consumer Read
```

를 수행한다.

Disk가 느리면 Follower lag → ISR 이탈로 이어질 수 있다.

### Network Throughput

```text
Producer Traffic
+
Replication Traffic
+
Consumer Traffic
```

을 고려.

### Partition 수

Partition이 많으면 Consumer 병렬성이 늘어난다.

너무 많으면:

```text
metadata 증가
file/resource 증가
leader election 부담 증가
운영 복잡도 증가
```

### Capacity Planning 입력

```text
초당 데이터량
초당 읽기량
평균 이벤트 크기
Retention
Replication Factor
Partition 수
Peak Traffic
Disk 사용률
Network 사용률
```

---

## 6.3 Reliability 설정

핵심:

```text
acks
min.insync.replicas
Replication Factor
```

### acks=0

Producer가 응답을 기다리지 않음. 빠르지만 데이터 유실 위험 큼.

### acks=1

Leader만 받으면 성공.

Follower 복제 전 Leader 장애 시 데이터 유실 가능.

### acks=all

필요한 ISR Replica까지 반영된 뒤 성공.

### min.insync.replicas

예:

```text
RF = 3
min ISR = 2
```

ISR이 2개 이상일 때만 Write 허용.

ISR 1개만 남으면 데이터 안전성을 위해 Write를 거부할 수 있다.

대표 Production 조합:

```text
RF = 3
acks = all
min.insync.replicas = 2
```

### Trade-off

```text
안전성 ↑
→ 장애 상황 Write 실패 가능성 ↑

Availability ↑
→ 데이터 유실 가능성 ↑
```

---

## 6.4 Security

핵심:

```text
TLS
SASL
ACL
```

### TLS

통신 암호화.

### SASL

Authentication.

```text
누구인가?
```

### ACL

Authorization.

```text
무엇을 할 수 있는가?
```

전체 흐름:

```text
Client
↓ TLS
통신 암호화
↓ SASL
인증
↓ ACL
권한 확인
```

---

## 6.5 Operations

핵심:

```text
Rebalancing
Partition Reassignment
Broker Expansion
Rolling Restart
```

### Rebalancing

Consumer Group의 Partition 담당 재분배.

### Partition Reassignment

Partition을 다른 Broker로 이동.

용도:

```text
Broker 증설
특정 Broker 부하 집중
Disk 사용량 불균형
```

### Broker Expansion

Broker 추가 후 기존 Partition을 새 Broker로 옮겨야 실제 부하 분산 가능.

### Rolling Restart

Broker를 하나씩 재시작.

```text
Broker A restart
↓
정상 확인
↓
Broker B restart
```

작업 전:

```text
ISR 정상?
Under-Replicated Partition 없음?
Broker 상태 정상?
```

확인.

---

## 6.6 Kafka on Kubernetes

Kafka는 Stateful workload.

핵심:

```text
StatefulSet
Persistent Storage
Anti-Affinity
Operator
Failure Handling
```

### StatefulSet

```text
kafka-0
kafka-1
kafka-2
```

### Persistent Storage

```text
Kafka Pod
↓
PVC
↓
PV
↓
Persistent Disk
```

### Broker 분산

나쁜 예:

```text
Node A
├─ kafka-0
├─ kafka-1
└─ kafka-2
```

좋은 예:

```text
Node A → kafka-0
Node B → kafka-1
Node C → kafka-2
```

사용:

```text
Pod Anti-Affinity
Topology Spread
```

### Kubernetes와 Kafka 역할 분리

```text
Kubernetes
= Broker Process / Pod lifecycle

Kafka
= Partition / Replication / Leader
```

### Operator

대표적으로 Strimzi 같은 Kafka Operator를 사용할 수 있다.

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 정정

2026-10-01 공식 문서를 확인했다. 아래는 원문을 대체하지 않는 적용 조건이다. Kafka 자료는 4.3 문서 기준이며 대상 클러스터의 버전·기능 플래그는 별도로 확인해야 한다.

### 6.1 보완: offset 예와 선출 자격

원문의 `1000 / 999 / 500`은 뒤처짐을 설명하는 예이며 고정된 offset 차이만으로 ISR 여부를 판정하지 않는다. ISR 이탈 조건과 실제 replica 상태를 확인한다. 또한 ISR 밖의 모든 replica가 항상 안전하지 않은 것은 아니다. Kafka의 Eligible Leader Replicas(ELR)는 별도 추적한 replica를 안전한 선출 후보로 사용할 수 있다. 현재 ISR, ELR 설정·상태, unclean election 정책을 함께 확인한다. [Kafka ELR](https://kafka.apache.org/43/operations/eligible-leader-replicas/)

### 6.2 보완: 용량 산식의 범위

`2.1TB`는 원문 입력을 곱한 전체 replica 데이터량의 학습 추정값이다. 단일 broker 요구량이나 실제 구매 용량을 확정하지 않는다. 운영 검토에서는 압축 후 저장량, retention 정책, broker별 편중, index·segment 여유, 장애 복구·재할당 중 추가 공간과 읽기·복제 트래픽을 측정한다. Partition 증가는 병렬성의 상한을 높이지만 hot key나 느린 consumer를 자동으로 해결하지 않는다. 이는 원문 산식과 partition trade-off에서 도출한 점검 항목이다.

### 6.3 정정: acks=all과 min ISR

`acks=all`은 `min.insync.replicas` 수만큼만 기다린다는 뜻이 아니다. 성공 응답에는 현재 ISR 전체의 확인이 필요하다. ISR이 3개이고 min ISR이 2여도 ISR 3개 모두가 대상이다. min ISR에는 leader가 포함되며, `acks=all`에서 ISR이 기준보다 적으면 쓰기가 실패한다. `acks=1`에도 같은 producer 승인 보장이 적용된다고 해석하지 않는다. Consumer에게 데이터가 보이는 high watermark 조건과 producer 응답 조건도 구분한다. [Producer acks](https://kafka.apache.org/43/configuration/producer-configs/), [Topic min.insync.replicas](https://kafka.apache.org/43/configuration/topic-configs/)

이 조합만으로 중복 제거·end-to-end exactly-once가 보장되지는 않는다. Producer idempotence, retry와 consumer 처리·offset commit은 별도 검토 대상이다. 위의 `RF=3` 예는 배치 장애 영역과 허용 가능한 쓰기 중단도 함께 평가해야 한다.

### 6.4 보완: 보안 기능은 명시적으로 구성

TLS는 암호화뿐 아니라 인증서 기반 인증에도 사용할 수 있다. SASL은 인증 수단이며 자체를 전송 암호화와 동일시하지 않는다. 원문 흐름은 한 가지 개념 조합이다. 실제 listener의 보안 프로토콜, 인증 방식, authorizer·ACL을 확인해야 하며 Kafka를 설치했다고 모두 활성화되지는 않는다. [Kafka security overview](https://kafka.apache.org/43/security/security-overview/)

### 6.5 보완: 재할당과 유지보수

일반적인 broker 추가는 기존 partition을 자동 재분배하지 않는다. 자동화 도구가 있더라도 재할당 계획·대상 broker·복제 진행률·throttle을 확인한다. 작업 전 상태가 정상이었다는 사실만으로 다음 broker 재시작을 진행하지 않는다. 각 단계 후 ISR 회복과 실제 가용성을 확인한다. 이것은 원문 점검 절차를 운영 계획에 적용하기 위한 조건이며 작업 실행 승인이 아니다. [Kafka operations](https://kafka.apache.org/43/operations/basic-kafka-operations/)

### 6.6 보완: StatefulSet과 Operator의 경계

StatefulSet은 stateful workload를 이해하는 기본 개념이다. 모든 Kafka Operator가 StatefulSet을 생성한다고 단정하면 안 된다. 현재 Strimzi는 `StrimziPodSet` 등 자체 리소스를 관리한다. 선택한 Operator 버전의 리소스와 storage·rack 배치 구성을 확인한다. [Strimzi deployment guide](https://strimzi.io/docs/operators/latest/full/deploying.html)

Pod를 서로 다른 Node에 놓는 것과 서로 다른 Zone·장애 영역에 replica를 배치하는 것도 다르다. PVC가 있다는 사실은 백업·복구 시험 완료를 의미하지 않는다. 관련 배치·중단 조건은 [Kubernetes 운영](kubernetes-operations.md)과 함께 검토한다.

## LLM in Practice

### ISR 감소 상태에서 유지보수 계획 검토

**상황:** 가상의 Kafka topic에서 ISR이 줄어든 상태로 broker 유지보수 가능 여부를 검토한다. 이 페이지의 6.1·6.3·6.5 보완과 [Kubernetes 운영](kubernetes-operations.md)의 중단 조건을 연결한다.

**LLM에 줄 맥락:** 비식별 topic·producer 설정, Kafka 버전과 ELR 상태, ISR 변화, broker별 disk/network 지표, 오류 코드와 유지보수 허용 범위. 인증 정보와 실제 내부 주소는 제외한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 Kafka topic은 RF=3, acks=all, min.insync.replicas=2다.
    현재 ISR은 2개이고 follower 하나의 disk latency가 증가했다.
    버전과 ELR 설정: [확인한 값 또는 미확인]
    ISR 변화, broker별 disk/network, producer 오류: [비식별 관측값]
    아직 재시작이나 재할당은 하지 않았다.
    [요청]
    현재 상태와 유지보수 계획을 먼저 검토하라.
    관측 사실, 가정, 원인 가설, 누락 근거를 구분하라.
    ISR이 1개로 줄 때 producer 응답과 쓰기 가용성을 설명하라.
    min ISR=2가 항상 2개 응답만 기다린다는 뜻인지 검토하라.
    [출력]
    읽기 전용 확인 순서, 진행 조건, 중단 조건을 표로 제시하라.
    원인 확인 없이 acks나 min ISR을 낮추는 변경을 권하지 말라.
    [검증]
    실제 topic/producer 설정과 해당 버전 공식 문서로 대조하라.
    변경 실행은 별도 승인 절차가 필요하다고 명시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A hypothetical Kafka topic uses RF=3, acks=all, and min.insync.replicas=2.
    The ISR has 2 members, and one follower has rising disk latency.
    Version and ELR settings: [verified values or unknown]
    ISR changes, broker disk/network metrics, producer errors: [sanitized observations]
    No restart or reassignment has been performed.
    [Task]
    Review the current state and maintenance plan first.
    Separate observations, assumptions, hypotheses, and missing evidence.
    Explain producer responses and write availability if the ISR falls to 1.
    Check whether minimum ISR=2 means waiting for only 2 acknowledgments every time.
    [Output]
    Give a table of read-only checks, go conditions, and stop conditions.
    Do not recommend lowering acks or minimum ISR without finding the cause.
    [Checks]
    Compare actual topic/producer settings with the version-specific official docs.
    State that executing a change needs a separate approval process.
    ```

**예상 결과:** 쓰기 승인 조건, 가능한 lag 원인, 근거를 가르는 조회, 작업을 멈출 조건을 분리한 표.

**LLM이 틀릴 수 있는 부분:** ISR 2개를 정상 여유가 충분한 상태로 단정하거나, min ISR을 대기 replica 수로 오해하거나, 버전·ELR 차이 없이 선출 규칙을 일반화할 수 있다.

**검증 방법:** 실제 설정·오류·지표와 해당 버전 공식 문서를 사람이 대조한다. 테스트와 변경은 승인된 환경에서 별도로 수행한다. 이 프롬프트는 작성한 활용 예이며 LLM 응답이나 실제 복구 결과를 검증했다는 뜻이 아니다.
