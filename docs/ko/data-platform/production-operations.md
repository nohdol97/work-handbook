---
id: data-platform-production-operations
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE2-20-01
  - DPE2-20-02
  - DPE2-20-03
  - DPE2-20-04
  - DPE2-20-05
  - DPE2-20-06
  - DPE2-20-07
  - DPE2-20-08
  - DPE2-20-09
  - DPE2-20-10
  - DPE2-20-11
  - DPE2-20-12
  - DPE2-20-13
  - DPE2-20-14
  - DPE2-20-15
  - DPE2-20-16
  - DPE2-20-17
  - DPE2-20-18
  - DPE2-20-19
  - DPE2-20-20
  - DPE2-20-21
  - DPE2-20-22
---

# Chapter 20 — Production Data Platform Engineering

제공된 완성본의 20장 목차와 기술 내용을 따라 입문자용 문장으로 다듬었다. 예시와 도식은 개념 학습 자료이며 실제 구현·운영·복구 검증 기록이 아니다. 영어 기술 용어·코드는 유지하고 text 도식의 일반 설명은 같은 형식으로 번역했다.

<!-- SOURCE CORE START -->

이 단계는 앞에서 배운 개념을 **프로덕션 운영**으로 연결한다.

핵심 변화는 다음과 같다.

> 앞 장에서는 “이 기술은 어떻게 작동하는가?”를 물었다.  
> 프로덕션 엔지니어링에서는 “새벽 3시에 고장 나면 무슨 일이 일어나는가?”를 묻는다.

---

## 20.1 Backfills

누락된 3일의 주문 집계나 버그 수정 후의 결과를 복구할 때, 날짜·파티션처럼 재처리 범위를 먼저 정한다.

> **정해진 범위의 과거 데이터를 다시 계산한다.**

사용 사례:

- 파이프라인 장애,
- 버그 수정,
- 새로운 업무 로직,
- 누락 데이터,
- 스키마 수정.

범위를 한정한 backfill을 우선한다.

```text
나쁜 예:
5년 전체를 다시 계산

더 나은 예:
영향받은 partition만 다시 계산
```

예시:

```text
2026-09-01 ~ 2026-09-03
```

또는:

```text
event_date partition
```

필수 조건:

- 멱등성을 가진 task,
- 매개변수로 지정하는 날짜 범위,
- 예측 가능한 출력 교체,
- 자원 제어.

---

## 20.2 Reprocessing

**재처리(Reprocessing)**는 과거 입력을 다시 읽어 결과를 만드는 더 넓은 작업이며 backfill도 여기에 속한다. 원본 이벤트·Bronze·스냅샷 중 어디서 다시 시작할지 먼저 정한다.

### Kafka Replay

```text
Kafka offset
 ↓
event를 다시 소비
```

Event Log가 여전히 기준 원본(source of truth)일 때 유용하다.

### Bronze Replay

```text
Bronze Raw History
 ↓
새로운 변환
 ↓
Silver / Gold 재구축
```

원시 이력이 가치 있는 이유 중 하나다.

### Iceberg Snapshot Recovery

데이터 손상이 최근에 발생했다면:

```text
문제가 있는 현재 snapshot
 ↓
정상인 이전 snapshot
```

Time travel/rollback이 복구에 도움이 될 수 있다.

중요한 질문:

> **무엇이 권위 있는 기준 원본인가?**

가능한 답:

```text
Operational DB
Kafka
Bronze
Iceberg Snapshot
external source
```

장애가 난 뒤에 처음 원본을 고르면 보존 기간이 끝났거나 재생 순서를 모를 수 있다. 평소에 데이터셋별 재처리 출발점을 기록한다.

---

## 20.3 Incident Drill — Schema Break

**스키마 변경 장애**는 생산자가 필드 이름이나 타입을 바꾸어 소비자가 더는 데이터를 읽지 못하는 상황이다. 계약을 깨는 변경인지 확인하고 영향받은 구간을 찾는다.

```text
원본:
amount BIGINT

변경 후:
amount STRING
```

가능한 연결 경로:

```text
Producer
 ↓
CDC / Event
 ↓
Flink/Spark
 ↓
Silver
 ↓
dbt
 ↓
Dashboard
```

대응:

```text
schema 변경 감지
 ↓
호환되지 않는 데이터 중지/격리
 ↓
Lineage로 영향 분석
 ↓
producer/consumer 수정
 ↓
영향 데이터 backfill
 ↓
검증
```

예방:

- Data Contracts
- Schema Registry
- 호환성 검사
- CI/CD 검증

---

## 20.4 Incident Drill — Bad Data

**잘못된 데이터 장애**는 파이프라인이 돌아가도 값이 틀린 상황이다. 예를 들어 결제 금액이 두 번 더해졌다면 실행 성공 여부만으로는 문제를 찾지 못한다.

```text
latency_ms = -100
```

또는:

```text
user_id의 90%가 NULL
```

대응:

```text
품질 경보
 ↓
확산 차단
 ↓
격리 / 게시 중지
 ↓
근본 원인
 ↓
수정
 ↓
재처리
 ↓
검증
```

작업 상태가 성공이어도 값이 틀리면 게시를 멈추거나 격리한다. 복구 뒤에는 업무 지표까지 다시 확인한다.

---

## 20.5 Incident Drill — Data Skew

**데이터 쏠림(Data Skew)**은 일부 키나 파티션에 작업량이 몰리는 현상이다. 한 계산 노드만 늦게 끝난다면 키 분포와 분할 방법을 확인한다.

```text
대부분의 Spark task는 빠르게 완료
하나의 task가 끝없이 실행
```

또는:

```text
특정 Flink key에 부하 집중
```

조사할 항목:

- key 분포,
- null/기본값,
- join cardinality,
- 부하가 집중된 고객/팀.

가능한 대응:

```text
salting
pre-aggregation
heavy key 별도 처리
partition 전략 변경
AQE
```

스트리밍에서 키를 바꾸거나 salting으로 부하를 나누면 같은 키의 순서가 달라질 수 있다. 순서 보장이 필요한 이벤트인지 먼저 확인한다.

---

## 20.6 Incident Drill — Small File Explosion

**작은 파일 폭증**은 잦은 쓰기로 파일 수가 지나치게 늘어난 상황이다. 저장량이 같아도 파일 목록을 읽고 여는 일이 많아져 쿼리가 느려질 수 있다.

```text
수백만 개의 작은 Parquet 파일
```

결과:

- metadata 부담,
- 느린 query planning,
- 많은 object storage 요청,
- 낮은 task 효율.

원인:

- 지나치게 잦은 streaming commit,
- 지나친 partition 분할,
- 너무 많은 작은 쓰기.

대응:

```text
Compaction
 ↓
목표 파일 크기 조정
 ↓
쓰기 빈도 조정
 ↓
partition 전략 재검토
```

---

## 20.7 Incident Drill — Stale Table

**오래된 테이블(Stale Table)**은 작업은 끝났어도 기대한 새 데이터가 보이지 않는 상태다. 마지막 성공 시각과 원본 도착 시각을 비교한다.

```text
현재 시각: 10:00
Gold의 최신 데이터: 08:40
```

계층별로 조사한다.

```text
Source Freshness?
Kafka?
Bronze?
Silver?
Gold?
Dashboard?
```

최신성(Freshness)은 원본 도착, Bronze·Silver·Gold 갱신, 대시보드 반영 시각을 각각 재야 지연이 시작된 곳을 찾을 수 있다.

---

## 20.8 Incident Drill — Corrupt Transformation

**손상된 변환(Corrupt Transformation)**은 코드나 비즈니스 규칙 오류가 잘못된 결과를 만드는 상황이다. 배포 시점과 영향을 받은 결과 범위를 먼저 확인한다.

```text
WHERE event_type = 'clik'
```

Job은 성공한다.

결과:

```text
0행
```

Pipeline 건강 상태:

```text
GREEN
```

데이터 건강 상태:

```text
RED
```

대응:

```text
Volume / Quality 이상
 ↓
변경된 변환 찾기
 ↓
코드 수정
 ↓
영향 구간 backfill
```

중요한 교훈:

> **정상 Pipeline ≠ 정상 Data**

---

## 20.9 Incident Drill — CDC Failure

**CDC 장애**는 데이터베이스 변경을 가져오는 흐름이 멈추거나 누락되는 상황이다. 원본 로그 보존 기간과 마지막 처리 위치가 복구 가능 범위를 정한다.

```text
Connector 중지
Offset 손실
필요한 WAL 만료
중복 replay
Schema 변경
```

일반적인 복구:

```text
재시작
 ↓
저장된 Offset
 ↓
Replay
 ↓
멱등한 downstream 처리
```

심각한 경우의 복구:

```text
Offset 사용 불가
또는 WAL 사용 불가
 ↓
Snapshot / Re-bootstrap
```

---

## 20.10 Capacity Planning

**용량 계획(Capacity Planning)**은 예상 데이터량과 동시 작업을 플랫폼이 감당할 수 있는지 미리 따지는 일이다. 현재 평균뿐 아니라 급증 시간대와 복구 작업도 포함한다.

주요 입력:

```text
events / second
GB / TB per day
retention days
peak multiplier
number of partitions
file count
Spark concurrency
query concurrency
streaming state size
```

예:

```text
10k events/sec
× average event size
× 86,400 sec/day
→ daily ingestion volume
```

평균만을 기준으로 계획하지 않는다.

함께 고려할 항목:

```text
peak traffic
backfill traffic
incident replay
month-end reports
concurrent dashboards
```

---

## 20.11 Kafka Capacity Questions

Kafka 용량을 볼 때는 초당 입력량뿐 아니라 보존 기간, 복제 수, 소비자 지연을 함께 묻는다. 버퍼가 꽉 차기 전에 어느 지표가 먼저 악화되는지 정한다.

```text
초당 event는 몇 개인가?
partition은 몇 개인가?
보존 기간은 얼마인가?
consumer는 몇 개인가?
replay traffic은 얼마나 되는가?
```

Partition이 너무 적으면:

```text
consumer 병렬성 제한
```

Partition이 너무 많으면:

```text
운영 부담 증가
```

---

## 20.12 Lakehouse Capacity Questions

Lakehouse 용량에는 저장 바이트뿐 아니라 파일 수, 메타데이터, 동시 쓰기와 유지보수 작업이 포함된다. 작은 파일이 쌓이면 같은 데이터량에서도 비용이 달라진다.

```text
TB/day
file count/day
average file size
partition count
snapshot count
delete file growth
```

데이터 크기만으로는 충분하지 않다.

```text
파일 8개에 담긴 1 TB
≠
파일 1,000,000개에 담긴 1 TB
```

운영상의 특성이 크게 다르다.

---

## 20.13 Spark Capacity Questions

Spark 용량은 입력량, 셔플, 메모리, 병렬 작업 수에 좌우된다. 평균 실행 시간만 보지 말고 가장 느린 파티션을 확인한다.

```text
concurrent jobs
shuffle volume
executor memory
task count
CPU
backfill overlap
```

매일 정상 작동하는 파이프라인도 90일 backfill이 동시에 시작되면 실패할 수 있다.

Backfill에는 별도의 용량 정책이 필요하다.

---

## 20.14 Query Capacity Questions

조회 용량은 동시 사용자와 쿼리 복잡도에 따라 달라진다. Trino·SQL Warehouse·Snowflake에서는 응답 지연과 대기열을 함께 본다.

```text
concurrent users
dashboard refresh rate
query scan size
join complexity
memory
peak BI windows
```

대화형 workload와 batch workload가 반드시 같은 compute pool을 공유해야 하는 것은 아니다.

Workload isolation이 유용하다.

---

## 20.15 Cost Engineering

**비용 엔지니어링(Cost Engineering)**은 필요한 성능과 신뢰성을 유지하면서 계산·저장·조회 비용을 관리하는 일이다. 사용량과 실제 청구 단위를 연결해 본다.

```text
Compute
Storage
Network
Object Storage Requests
Serving Stores
Compaction
Streaming always-on compute
AI inference
```

### Compute optimization

줄일 항목:

```text
unnecessary scan
shuffle
recomputation
idle compute
oversized clusters
```

### Storage optimization

관리할 항목:

```text
Retention
Snapshot expiration
Orphan files
Duplicate datasets
Raw data lifespan
```

### Serving cost

모든 workload를 비용이 큰 분석 엔진으로 보내지 않는다.

예:

```text
Heavy analytics
→ Lakehouse

Low-latency operational read
→ Serving Store / Cache
```

### FinOps dimensions

다음 항목으로 태그를 지정한다.

```text
team
project
environment
pipeline
product
```

비용 책임을 명확히 하기 위해서다.

---

## 20.16 DR / Recovery

**DR(Disaster Recovery, 재해 복구)**은 장애로 서비스나 데이터가 사라졌을 때 다시 운영 가능한 상태로 되돌리는 계획이다. 백업 파일뿐 아니라 메타데이터와 접근 경로도 확인한다.

주요 복구 시나리오:

```text
Catalog loss
Object storage problem
Checkpoint loss
CDC state loss
Region outage
Bad deployment
Credential/policy corruption
```

---

## 20.17 Catalog Recovery

**카탈로그 복구**는 테이블 이름과 현재 메타데이터 위치를 되찾는 일이다. 객체 파일이 남아 있어도 이 연결이 끊기면 테이블을 바로 조회하지 못할 수 있다.

Table metadata/catalog를 잃으면:

```text
Parquet 파일은 여전히 존재할 수 있음
하지만
table을 즉시 사용하지 못할 수 있음
```

따라서 catalog metadata는 프로덕션 인프라다.

다음을 이용해 보호한다.

- managed service의 내구성,
- 지원되는 backup/export,
- 설정을 위한 infrastructure-as-code,
- 복구 절차.

---

## 20.18 Table Recovery

**테이블 복구**는 잘못된 쓰기나 삭제 이후 올바른 상태를 되찾는 일이다. 스냅샷과 백업을 쓸 수 있는 기간을 먼저 확인한다.

```text
Iceberg snapshot
time travel
rollback
Bronze replay
source replay
```

가장 빠른 복구 방법은 장애 유형에 따라 다르다.

---

## 20.19 Checkpoint Loss

**체크포인트(Checkpoint)**는 스트리밍 작업이 어디까지 처리했는지와 필요한 상태를 저장한 복구 지점이다. 책갈피와 그때까지 적어 둔 계산 장부를 함께 보관해야 이어서 계산할 수 있는 것과 같다. 이를 잃으면 원본 보존 범위부터 확인해야 한다.

Spark/Flink checkpoint를 잃으면:

```text
어디에서 처리를 재개해야 하는가?
```

가능한 선택:

- Kafka에서 replay,
- Savepoint에서 복구,
- state 재구축,
- 알고 있는 timestamp에서 재시작.

다음이 발생할 수 있다.

- 중복 처리,
- 긴 복구 시간,
- downstream 부하 급증.

장애 전에 계획한다.

---

## 20.20 Source-of-Truth Decisions

각 중요 데이터셋의 **기준 원본(Source of Truth)**을 문서화한다. 재처리할 때 어느 입력을 믿고 어느 결과를 다시 만들지 미리 정해야 중복과 누락을 줄인다.

```text
Source of Truth
Recovery Source
Maximum Replay Window
Retention
Owner
SLO
```

예:

```text
fact_llm_call

기준 원본:
7일 동안의 Kafka raw event
+
수집 후 Iceberg Bronze

복구:
7일 미만이면 Kafka replay
그 밖에는 Bronze에서 재구축
```

이렇게 하면 복구가 즉흥 대응에서 절차로 바뀐다.

---

## 20.21 Data Platform SLOs

**SLO(Service Level Objective)**는 데이터 서비스가 목표로 삼는 수준이다. 새로움, 정확성, 가용성, 복구 시간, 조회 지연을 측정 가능한 값으로 정한다.

### Freshness

```text
Gold table의 원본 대비 지연 < 15 min
```

### Correctness

```text
duplicate rate < 0.01%
required field completeness > 99.9%
```

### Availability

```text
Query 계층 가용성 99.9%
```

### Recovery Time

RTO:

> 플랫폼은 얼마나 빨리 복구되어야 하는가?

예:

```text
중요 dataset RTO < 1 hour
```

### Recovery Point

RPO:

> 어느 정도의 데이터 손실을 허용할 수 있는가?

예:

```text
RPO < 5 minutes
```

### Query Latency

```text
dashboard query p95 < 5 seconds
```

Dataset마다 필요한 SLO가 다르다.

등급을 나눈다.

```text
Tier 1
→ 경영/업무 핵심
→ 엄격한 SLO

Tier 2
→ 일반 분석

Tier 3
→ 실험
```

---

## 20.22 Production Runbook Mental Model

**운영 절차서(Runbook)**는 장애 때 누가 무엇을 확인하고 어떻게 복구할지 적은 안내서다. 새벽에도 따라 할 수 있도록 입력·판단·종료 기준을 구체적으로 쓴다.

```text
Owner
Source
Destination
SLO
Alert
Failure Modes
Replay Procedure
Backfill Procedure
Rollback Procedure
Cost Owner
Downstream Impact
```

성숙한 플랫폼은 아키텍처 그림만으로 정의되지 않는다.

다음도 기준이 된다.

> **아키텍처가 고장 났을 때 운영자가 해야 할 일을 정확히 알고 있는가.**

---

<!-- SOURCE CORE END -->

## 처음 읽는 사람을 위한 연결

이 장은 소방 훈련처럼 읽으면 좋다. 불이 난 뒤 소화기를 찾기보다, 평소에 대피 경로와 담당자를 정한다. 데이터 플랫폼에서도 장애 전에 기준 원본, 보존 기간, 복구 목표, 영향받은 소비자와 책임자를 정해야 한다. RTO는 복구에 허용되는 시간, RPO는 잃을 수 있는 데이터의 시간 범위다. 이 비유는 준비 순서를 설명할 뿐 실제 복구 절차를 대신하지 않는다.

예를 들어 Gold 테이블이 비었는데 작업은 성공했다면 [20.8](#208-incident-drill-corrupt-transformation)의 변환 오류를 의심할 수 있다. 먼저 게시를 제한하고 Bronze 원본과 lineage를 확인한다. 그다음 [20.1](#201-backfills)의 영향 범위 재계산과 [20.2](#202-reprocessing)의 재처리 경로 및 [20.16](#2016-dr-recovery)의 복구 원본을 비교한다. 재실행 전에 중복·누락·업무 합계의 인수 기준을 정해야 빠른 복구가 잘못된 데이터를 퍼뜨리지 않는다.

## 핵심 정리

- 작업 성공과 데이터 정상은 별개다. 건수·키·신선도·업무 결과를 확인한다.
- Backfill·replay·snapshot 복구는 남아 있는 원본과 영향 범위에 따라 선택한다.
- 장애 전에 기준 원본, 보존, 담당자, 중단·재개 기준과 RTO/RPO를 정한다.

## LLM in Practice

### 제한된 재처리 계획 검토

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    변환 배포 후 Gold 결과가 0행이 되었다. 정상 pipeline 실행 기록만으로 복구 완료를 판단할 수 없다.
    현재 구조와 관찰·가정·누락 근거를 확인한 뒤 Kafka replay, Bronze 재처리, snapshot 복구의 적합 조건을 비교하세요.
    승인된 영향 범위에 한정한 복구 계획만 제안하세요. 삭제나 실행은 하지 마세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A transformation deployment leaves Gold with zero rows. Normal pipeline success records cannot establish recovery.
    Assess the current design first. Separate observations, assumptions, hypotheses, and missing evidence.
    Compare prerequisites for Kafka replay, Bronze reprocessing, and snapshot recovery.
    Propose a recovery plan limited to the approved affected range. Do not delete or execute anything.
    Review the material; do not apply changes.
    ```

**핵심 사항:** 관찰·가정·가설·누락 근거가 분리된 조사 표와 제한된 복구 계획. 범위, 원본 선택, 사전조건, 자원 한도, 중단·검증·에스컬레이션 기준을 포함한다. Job 성공을 데이터 정상으로 해석하거나, 만료된 Kafka 이력이 있다고 가정하거나, snapshot rollback이 모든 downstream 결과를 복원한다고 오해할 수 있다. RTO/RPO를 뒤바꾸거나 중복·state·동시 쓰기 영향을 빠뜨릴 수 있다. 사람이 실제 source retention, offset, snapshot, 변환 diff, lineage와 공식 문서를 확인한다. 승인된 격리 환경에서 작은 범위로 재처리해 건수·키·필수 값·freshness와 업무 결과를 대조한다. 운영 실행은 별도 승인과 사전조건을 충족한 뒤에만 진행한다. LLM 출력은 실행 명령이나 확인된 원인이 아닌 작업 가설이다.

## 부록: 기존 학습 보충과 적용 조건

이 문서는 개념 학습과 가상 장애 훈련을 정리한다. 실제 장애 대응·복구 훈련·성능 측정을 수행했다는 기록이 아니다. 기술의 작동 원리에서 한 걸음 더 나아가 **새벽 3시에 장애가 나면 무엇을 확인하고 어떻게 복구할지**를 다룬다. 제품별 복구 동작은 2026-09-26에 공식 문서를 확인했으며 실제 버전·설정에 맞게 다시 검증해야 한다.

### 먼저 정할 것

중요 데이터마다 책임자, 기준 원본(source of truth), 복구 원본, 보존 기간, 최대 replay 가능 구간, SLO를 정한다. 작업 성공 여부와 데이터 건강 상태를 따로 관찰한다. 복구 속도만 높이다가 중복·누락·잘못된 결과를 확산시키지 않는다.

```mermaid
flowchart TD
  A[Quality or freshness alert] --> B[Contain affected publication]
  B --> C[Inspect source and lineage]
  C --> D{Valid recovery source?}
  D -->|Retained event log| E[Scoped Kafka replay]
  D -->|Raw history| F[Bronze reprocessing]
  D -->|Valid table snapshot| G[Evaluate snapshot recovery]
  E --> H[Validate counts keys quality and freshness]
  F --> H
  G --> H
  H --> I{Acceptance checks pass?}
  I -->|Yes| J[Resume publication and monitor]
  I -->|No| K[Keep containment and escalate]
```

이 흐름은 복구 계획의 구조다. 실제 publish 중지, offset 변경, snapshot rollback, 재게시에는 해당 시스템의 승인·동시 쓰기 제어·복구 사전조건이 필요하다.

### Backfill과 재처리

**Backfill**은 정해진 과거 범위의 데이터를 다시 계산하는 일이다. 파이프라인 장애, 버그 수정, 새 업무 로직, 누락 데이터, 스키마 수정에 사용한다. 영향 범위를 먼저 정한다. 5년 전체를 재계산하기보다 `2026-09-01 ~ 2026-09-03` 또는 영향받은 `event_date` partition만 대상으로 삼는다.

필수 조건은 멱등 작업, 날짜 범위 매개변수, 예측 가능한 출력 교체, 자원 제어다. 재시도해도 결과가 중복되지 않아야 하고 어느 범위를 교체하는지 알 수 있어야 한다. 원본의 날짜 표기는 업무 범위 예시다. 실행 시에는 시간대와 시작·끝 경계의 포함 여부도 명시한다.

Backfill은 **reprocessing**의 한 형태다. 복구 경로는 남아 있는 원본과 장애 종류에 따라 고른다.

| 경로 | 흐름 | 적합한 조건과 확인할 점 |
| --- | --- | --- |
| Kafka replay | Offset → 이벤트 다시 소비 | Event Log가 기준 원본이며 필요한 이벤트가 실제 보존되어 있음 |
| Bronze replay | Raw history → 수정한 변환 → Silver/Gold 재구축 | 원시 이력의 범위·완전성과 적용할 변환 버전을 확인 |
| Iceberg snapshot recovery | 잘못된 현재 snapshot → 유효한 이전 snapshot 검토 | 최근 손상에서 time travel로 비교하고 rollback의 영향 범위를 확인 |
| Source replay | Operational DB 또는 외부 원본 → 재수집 | 원본이 필요한 과거 상태까지 재현할 수 있는지 확인 |

기준 원본은 Operational DB, Kafka, Bronze, Iceberg snapshot, 외부 원본 중 무엇인지 장애 전에 결정한다. 이전 snapshot으로 되돌리는 것과 그 시점 이후의 정상 변경을 재생하는 것은 별도 문제다. [Iceberg](lakehouse-iceberg.md)와 [오케스트레이션](orchestration.md)을 함께 본다.

### 20.3~20.9 장애 훈련의 적용 조건

원문의 증상·대응 순서를 사용하되 다음 조건을 확인한다.

| 원문 사례 | 적용 시 추가 확인 |
|---|---|
| [20.3 Schema break](#203-incident-drill-schema-break) | 자동 타입 변환이 업무 의미까지 보존하는지 확인한다. 복구 검사는 타입·값·건수·downstream 결과를 포함한다. [CDC](cdc-debezium.md), [Lineage](lineage-metadata.md). |
| [20.4 Bad data](#204-incident-drill-bad-data) | [품질 규칙](data-quality.md)이 형식뿐 아니라 업무상 유효성을 검사하는지 확인한다. |
| [20.5 Skew](#205-incident-drill-data-skew) | 측정한 병목과 대응 후보를 대조한다. Streaming의 re-keying/salting은 키별 순서 요구를 보존해야 한다. [Spark](spark.md), [Flink](flink.md). |
| [20.6 Small files](#206-incident-drill-small-file-explosion) | Compaction도 compute·I/O를 소비하므로 쓰기·쿼리 부하와 함께 계획한다. [Iceberg 유지보수](https://iceberg.apache.org/docs/latest/maintenance/). |
| [20.7 Stale table](#207-incident-drill-stale-table) | 원본 지연, 전송·변환·게시 지연, dashboard 갱신 지연을 분리한다. [관측성](data-observability.md). |
| [20.8 Corrupt transformation](#208-incident-drill-corrupt-transformation) | `clik` 대신 의도한 `click`과 실제 배포 diff를 대조하고 영향 구간을 정한다. |
| [20.9 CDC failure](#209-incident-drill-cdc-failure) | Connector 버전·snapshot mode·replication slot을 대조한다. 재시작은 사라진 로그를 복원하지 않는다. Re-bootstrap 전 downstream 정합·중복 제거·누락 검증을 정한다. [Debezium 공식 문서](https://debezium.io/documentation/reference/stable/connectors/postgresql.html). |

### 용량 계획

용량 계획은 예상 데이터량과 동시 작업을 감당할 수 있는지 추정하는 일이다. 입력은 events/s, GB 또는 TB/day, retention days, peak multiplier, partition 수, 파일 수, Spark 동시성, query 동시성, streaming state 크기다.

```text
10,000 events/second
× average bytes/event
× 86,400 seconds/day
= estimated ingestion bytes/day
```

이것은 수집량 산식이지 최종 저장·네트워크 용량 보장은 아니다. 실제 평균 크기를 넣고 압축·복제·보존·재처리 비용을 별도로 확인한다. 평균뿐 아니라 peak traffic, backfill, 장애 replay, 월말 보고서, 동시 dashboard도 고려한다.

| 계층 | 확인할 입력·질문 | 운영상 경계 |
| --- | --- | --- |
| Kafka | events/s, partition 수, retention, consumer 수, replay traffic | Partition이 너무 적으면 consumer 병렬성이 제한되고 너무 많으면 운영 부담 증가 |
| Lakehouse | TB/day, file count/day, 평균 파일 크기, partition 수, snapshot 수, delete file 증가량 | 같은 1 TB라도 파일 8개와 1,000,000개는 다른 운영 특성을 가짐 |
| Spark | 동시 job, shuffle량, executor memory, task 수, CPU, backfill 겹침 | 평소 일별 작업이 성공해도 90일 backfill과 겹치면 실패할 수 있음 |
| Trino/SQL Warehouse/Snowflake | 동시 사용자, dashboard 갱신 빈도, scan 크기, join 복잡도, memory, BI 피크 | Interactive와 batch workload의 compute pool 분리를 검토 |

Backfill에는 별도 용량 정책이 필요하다. 동시 실행 수와 자원 한도, 정상 작업 우선순위를 정한다. Workload isolation은 대화형 쿼리를 batch의 자원 경쟁으로부터 보호하는 선택지다.

### 비용 엔지니어링

주요 비용은 compute, storage, network, object storage requests, serving stores, compaction, 상시 streaming compute, AI inference다. 한 가지 비용만 줄이다가 다른 계층의 비용을 늘리지 않도록 전체를 본다.

- **Compute:** 불필요한 scan, shuffle, 재계산, idle compute, 과도하게 큰 cluster를 줄인다.
- **Storage:** retention, snapshot expiration, orphan files, 중복 dataset, raw data 수명을 관리한다.
- **Serving:** 무거운 분석은 lakehouse, 저지연 운영 조회는 serving store/cache가 적합할 수 있다. 모든 조회를 비싼 분석 엔진으로 보내지 않는다.
- **FinOps:** team, project, environment, pipeline, product로 비용을 분류해 책임자를 드러낸다.

삭제는 비용 절감과 복구 능력을 함께 바꾼다. Snapshot을 만료하면 해당 time travel 경로를 잃는다. Orphan cleanup의 보존 구간이 진행 중인 쓰기보다 짧으면 아직 commit하지 않은 파일을 삭제할 수 있다. 경로 표기 불일치도 잘못된 삭제를 일으킬 수 있다. 삭제 전에는 필요한 복구 구간·참조 snapshot·쓰기 기간·실제 파일 경로·후보 목록을 확인하고 승인된 절차를 사용한다. 이것은 정리 계획의 제약이며 삭제 실행 지시가 아니다. [Iceberg 유지보수 안전 조건](https://iceberg.apache.org/docs/latest/maintenance/)

### DR: 무엇을 복구해야 하는가

DR(Disaster Recovery)의 시나리오는 catalog 손실, object storage 문제, checkpoint 손실, CDC state 손실, region 장애, 잘못된 배포, credential/policy 손상이다. 자격 증명 자체를 공개 runbook이나 LLM 입력에 넣지 않는다. 이 문서는 실제 자격 증명 변경 절차를 제시하지 않는다.

#### Catalog 복구

Lakehouse table은 파일만으로 이루어지지 않는다. Parquet 파일이 남아 있어도 metadata/catalog를 잃으면 table을 즉시 사용할 수 없을 수 있다. Catalog metadata를 프로덕션 인프라로 보호한다. Managed service의 내구성, 지원되는 backup/export, 설정용 infrastructure-as-code, 복구 절차를 함께 준비한다. 제공자·catalog별 지원 범위를 확인한다.

#### Table 복구

Iceberg snapshot, time travel, rollback, Bronze replay, source replay가 후보이다. 장애 유형에 따라 가장 빠르고 올바른 경로가 다르다. Snapshot이 남아 있는지, 필요한 파일에 접근 가능한지, 복구 후의 정상 변경을 어떻게 다시 적용할지 확인한다.

#### Checkpoint 손실

Spark/Flink의 checkpoint/state를 잃으면 **어디에서 처리를 재개할지**를 먼저 정해야 한다. Kafka replay, 호환되는 Flink savepoint 복원, state 재구축, 알려진 timestamp에서 재시작이 후보다. Timestamp에서 입력을 재개하는 것만으로 과거 집계·join state까지 복원되는 것은 아니다.

중복 처리, 긴 복구 시간, downstream 부하 급증을 계획에 반영한다. Flink checkpoint는 주로 장애 복구용이며 savepoint는 운영자가 관리하는 계획된 중단·변경·복원에 쓰인다. 둘의 수명과 복원 조건을 혼동하거나 Flink savepoint를 Spark에 그대로 적용하지 않는다. 실제 상태·코드 호환성을 확인한다. [Flink checkpoint와 savepoint](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints_vs_savepoints/)

### Dataset별 기준 원본과 복구 계약

각 중요 dataset의 문서에는 다음 항목을 둔다.

| 항목 | 가상 `fact_llm_call` 예시 |
| --- | --- |
| Source of Truth | 7일 동안의 Kafka raw events + 수집 후 Iceberg Bronze |
| Recovery Source | 7일 미만 범위는 Kafka replay, 7일 이상 된 범위는 Bronze 재구축 |
| Maximum Replay Window | Kafka에 실제 남은 event 구간; 오래된 구간은 Bronze 가용 이력으로 별도 제한 |
| Retention | Kafka 7일이라는 예시 정책과 별도로 Bronze 보존 기간을 명시 |
| Owner | 책임 팀/담당 역할을 실제 운영 문서에 지정 |
| SLO | Dataset의 freshness, correctness, availability, RTO/RPO 목표 |

7일은 제품 기본값이 아닌 가상 정책이다. 실제 log retention/compaction, 누락, 수집 완료 여부를 확인한다. Kafka에서 사라졌다고 Bronze에 반드시 존재하는 것은 아니다. 이 계약은 복구를 즉흥 판단에서 확인 가능한 절차로 바꾼다.

### SLO, RTO, RPO

아래 숫자는 요구사항을 논의하기 위한 예시이며 달성한 측정값이나 보편적인 권장값이 아니다.

| 범주 | 의미 | 예시 목표 |
| --- | --- | --- |
| Freshness | 원본 대비 데이터 지연 | Gold가 원본보다 15분 미만 지연 |
| Correctness | 중복과 필수 필드 완전성 등 | Duplicate rate < 0.01%; required field completeness > 99.9% |
| Availability | 쿼리 계층을 사용할 수 있는 비율 | 99.9% |
| RTO: Recovery Time Objective | 복구까지 허용하는 시간 | 중요 dataset < 1시간 |
| RPO: Recovery Point Objective | 허용 가능한 데이터 손실 구간 | < 5분 |
| Query latency | 사용자 쿼리의 응답 지연 | Dashboard query p95 < 5초 |

RTO는 **얼마나 빨리 복구해야 하는가**, RPO는 **얼마나 많은 과거 데이터 손실을 허용하는가**다. 복구 완료 시간과 복구 가능한 데이터 시점을 구분한다. 측정 구간·분모·관측 지점도 실제 SLO에 명시한다.

Dataset별로 목표를 나눈다. Tier 1은 경영·업무 핵심 데이터로 엄격한 SLO를 적용한다. Tier 2는 일반 분석, Tier 3는 실험 데이터다. 중요도에 맞는 복구 투자와 비용을 선택한다.

### Runbook 필수 항목과 완료 판단

중요 파이프라인마다 Owner, Source, Destination, SLO, Alert, Failure Modes, Replay Procedure, Backfill Procedure, Rollback Procedure, Cost Owner, Downstream Impact를 기록한다.

운영 문서에는 최초 점검, 가설을 구분할 근거, 영향 범위, 승인된 복구 절차, 중단 조건, 검증 방법, 에스컬레이션 역할을 구체화한다. 사전조건을 충족하지 못하거나 복구 원본의 완전성을 입증하지 못하면 추측으로 offset·파일·권한을 변경하지 않고 담당자에게 에스컬레이션한다. 복구 후에는 freshness·건수·키 중복·품질·downstream 결과를 확인하고 재발 방지 조치를 기록한다.

성숙한 플랫폼은 아키텍처 그림뿐 아니라 그 구조가 고장 났을 때 작업자가 무엇을 해야 하는지 아는 것으로도 평가된다.
