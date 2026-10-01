---
id: platform-infrastructure-redis
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
knowledge_ids:
  - PIS2-04-01
  - PIS2-04-02
  - PIS2-04-03
  - PIS2-04-04
  - PIS2-04-05
  - PIS2-04-06
  - PIS2-04-07
  - PIS2-04-08
---

# Chapter 4. Redis for Platform Systems

원문의 순서와 형태를 보존한 개념 학습 기록이다. 예시 수치·명령·식별자는 설명용이며 실행·운영 검증 결과가 아니다. 원문의 단순화와 주의할 적용 조건은 본문 뒤 보완 설명에서 해당 절 번호로 확인한다.

<!-- SOURCE CORE START -->

## 4.1 Redis Fundamentals

Redis는 메모리에 데이터를 저장해서 매우 빠르게 읽고 쓰는 Key-Value 저장소다.

### Key-Value 구조

```text
key → value
```

예:

```text
"user:1001:name" → "Alice"
"session:abc123" → 사용자 세션 정보
```

Redis는 Key를 기준으로 빠르게 데이터를 찾는다.

### In-Memory Database

Redis는 데이터를 주로 RAM에 저장한다.

```text
Application
↓
Redis
↓
RAM
```

RAM은 빠르지만 비싸고 용량이 제한적이다. 그래서 Redis는 PostgreSQL 같은 주 저장소를 완전히 대체하기보다 빠른 접근이 필요한 데이터를 저장하는 보조 저장소로 많이 쓴다.

### 대표 Data Structure

```text
String
Hash
List
Set
Sorted Set
```

- String: 가장 단순한 값
- Hash: 하나의 객체처럼 여러 field 저장
- List: 순서가 있는 값 집합
- Set: 중복 없는 값 집합
- Sorted Set: score 기반 정렬 가능

### TTL

TTL = Time To Live.

```text
session:abc123
TTL = 30분
```

TTL이 끝나면 자동 삭제된다.

주요 용도:

```text
Session
Cache
Temporary token
Rate limit
```

### Redis가 빠른 이유

```text
1. RAM에 저장
2. Key 기반 단순 접근
```

### Redis vs PostgreSQL

```text
PostgreSQL
→ 영구 데이터의 주 저장소

Redis
→ 빠른 접근이 필요한 임시/보조 데이터
```

예:

```text
사용자 계정 → PostgreSQL
사용자 Session → Redis
상품 정보 원본 → PostgreSQL
상품 정보 Cache → Redis
```

---

## 4.2 Platform Use Cases

Redis의 주요 플랫폼 용도:

```text
Cache
Session
Rate Limiting
Counter
Distributed Lock
Request Deduplication
```

### Cache

```text
Application
↓
Redis 확인
├─ HIT → 바로 반환
└─ MISS → DB 조회 → Redis 저장
```

자주 읽는 데이터를 Redis에 잠깐 저장해 DB 부하와 응답 시간을 줄인다.

### Session

```text
session:abc123
→ user_id=1001
```

여러 API Pod가 공통 Redis를 사용하면 같은 Session 상태를 공유할 수 있다.

```text
API Pod A ─┐
API Pod B ─┼→ Redis Session
API Pod C ─┘
```

### 여기서 "여러 서버"의 의미

이 세션에서 말한 여러 서버는 보통 같은 서비스를 여러 Application Instance / Pod / Process로 띄운 것을 의미한다.

```text
Deployment
 replicas: 3

Pod A ─┐
Pod B ─┼→ Redis
Pod C ─┘
```

사용자 요청은 매번 다른 Pod로 갈 수 있다.

```text
Request 1 → Pod A
Request 2 → Pod C
Request 3 → Pod B
```

각 Pod가 자기 메모리에만 Session을 저장하면 다음 요청이 다른 Pod로 갈 때 상태를 찾지 못할 수 있다. 그래서 Redis를 공통 상태 저장소로 쓴다.

### Rate Limiting

예:

```text
user:1001:requests = 37
```

1분 100회 제한이라면:

```text
요청
↓
Redis counter 증가
↓
100 이하 → 허용
100 초과 → 거부
```

### Distributed Counter

```text
API Pod A ─┐
API Pod B ─┼→ request_count = 10025
API Pod C ─┘
```

예:

```text
오늘 API 호출 수
동시 사용자 수
usage count
```

### Distributed Lock

여러 서버가 같은 작업을 동시에 하지 않게 한다.

```text
Pod A
↓
lock 획득
↓
작업 수행

Pod B
↓
lock 이미 존재
↓
대기 또는 실패
```

### Request Deduplication

같은 요청을 여러 번 받아도 한 번만 처리.

```text
payment-123 없음
→ 처리
→ Redis 기록

같은 요청 재수신
→ 이미 존재
→ 중복 처리 안 함
```

### Redis를 도입하는 계기

가장 흔한 계기:

```text
1. PostgreSQL이 같은 데이터를 반복해서 읽느라 부하가 커짐
2. DB까지 가지 않고 더 빠르게 응답하고 싶은 데이터가 생김
```

다만 사용자 수보다 트래픽 패턴과 병목 위치가 더 중요하다.

Redis를 고려할 신호:

```text
동일 데이터 조회 반복
PostgreSQL CPU / I/O 증가
DB Connection 증가
Read query latency 증가
낮은 latency 요구
TTL / Session / Rate limit 필요
```

대략적인 규모 감각은 있지만 절대 기준은 아니다.

```text
수십~수백 req/s
→ PostgreSQL만으로 충분한 경우 많음

수백~수천 req/s
→ 반복 Read가 많다면 Redis 효과 커질 수 있음

수천~수만+ req/s
→ Cache Layer가 흔하지만 여전히 필수는 아님
```

예:

```text
5,000 req/s
Cache Hit = 95%

→ PostgreSQL까지 가는 요청 약 250 req/s
```

### Redis는 공짜 성능 향상이 아님

추가되는 복잡성:

```text
Cache invalidation
TTL 설정
Redis 장애
Memory 관리
Hot Key
Redis/PostgreSQL 데이터 불일치
```

따라서 PostgreSQL이 충분히 감당한다면 먼저:

```text
Index
Query
Connection Pool
```

을 최적화한 뒤 Redis를 고려한다.

---

## 4.3 Persistence

Redis는 RAM 기반이므로 재시작 시 데이터가 사라질 수 있다.

핵심:

```text
RDB
AOF
```

### RDB

특정 시점의 Redis 상태를 Snapshot으로 저장.

```text
10:00 상태 저장
↓
dump.rdb
```

장점:
- 파일 비교적 작음
- 복구 빠름
- Backup 용도로 좋음

단점:
- 마지막 Snapshot 이후 데이터 손실 가능

### AOF

Append Only File.

Write 명령을 계속 기록.

```text
SET user:1 Alice
INCR request_count
DEL session:123
```

재시작 시 명령을 다시 적용해 상태 복구.

### RDB vs AOF

```text
RDB
→ 일정 시점 Snapshot
→ 빠르고 단순
→ 최근 데이터 일부 손실 가능

AOF
→ Write 명령 계속 기록
→ 데이터 손실 줄이기 좋음
→ 파일 / Disk I/O 부담 증가
```

### Cache라면 Persistence 중요도가 낮을 수 있음

```text
Redis Cache 유실
↓
PostgreSQL에서 다시 읽음
↓
Cache 재생성
```

핵심 판단:

> Redis 데이터가 사라져도 다시 만들 수 있는가?

---

## 4.4 Replication

Redis Replication은 Primary 데이터를 Replica로 복제하는 구조다.

```text
        Primary
       /       \
  Replica A   Replica B
```

보통:

```text
Write → Primary
Read  → Primary 또는 Replica
```

주요 목적:

```text
1. Primary 장애 대비
2. Read 부하 분산
```

Redis Replication은 일반적으로 비동기다.

```text
Client Write
↓
Primary 반영
↓
Client 응답
↓
Replica 복제
```

### Replication Lag

```text
Primary     = 101
Replica     = 100
```

Replica가 Primary를 따라오는 데 지연이 생길 수 있다.

중요:

```text
Replication
≠
Automatic Failover
```

---

## 4.5 Redis Sentinel

Sentinel은 Redis HA / 자동 Failover 기능이다.

핵심 역할:

```text
Monitoring
Failover
Primary 정보 제공
```

### Failover

```text
Primary ❌
 ├─ Replica A
 └─ Replica B

↓

Replica A → 새로운 Primary
```

Sentinel 자체도 여러 개 두어 함께 장애를 판단할 수 있다.

```text
Sentinel 1
Sentinel 2
Sentinel 3
     ↓
Redis Primary / Replica
```

Application은 Sentinel을 통해 현재 Primary를 확인할 수 있다.

```text
Application
↓
Sentinel
↓
현재 Primary 확인
↓
새 Primary 연결
```

### Sentinel vs Redis Cluster

```text
Sentinel
→ HA / Failover 중심

Redis Cluster
→ Sharding + HA
```

---

## 4.6 Redis Cluster

Redis Cluster는 데이터를 여러 Redis Node에 분산 저장하고 장애에도 대응하는 구조다.

핵심:

```text
Sharding + Replication + Failover
```

### Sharding

```text
Redis A → 일부 데이터
Redis B → 일부 데이터
Redis C → 일부 데이터
```

### Hash Slot

```text
Key
↓
hash
↓
Hash Slot
↓
담당 Redis Node
```

### Resharding

Node 추가/제거 시 Slot 단위로 이동.

### Cluster HA

```text
Primary A → Replica A
Primary B → Replica B
Primary C → Replica C
```

### Sentinel vs Cluster

```text
Sentinel
= HA 중심

Redis Cluster
= Scale-out + HA
```

Cluster가 필요한 대표 상황:

```text
데이터가 한 Node 메모리를 초과
트래픽이 한 Node 처리량을 초과
수평 확장 필요
```

---

## 4.7 Performance

핵심:

```text
Hot Key
Big Key
Memory / Eviction
Memory Fragmentation
Pipelining
```

### Hot Key

특정 Key 하나에 요청 집중.

```text
많은 Client
↓
하나의 Key
↓
특정 Redis Node 부하 집중
```

Redis Cluster에서도 해당 Key는 특정 Node 하나가 담당한다.

### Big Key

하나의 Key가 너무 큰 데이터를 가짐.

문제:

```text
CPU 사용 증가
Network 전송 증가
응답 지연
```

### Eviction

Memory가 가득 찼을 때 어떤 Key를 제거할지 결정.

### Memory Fragmentation

실제 데이터보다 OS에서 할당한 Memory가 더 커질 수 있음.

### Pipelining

여러 명령을 묶어서 전송해 Network round trip을 줄임.

```text
SET A
SET B
SET C
↓
한 번에 전송
```

운영 점검:

```text
Redis 느림
→ Hot Key?
→ Big Key?
→ Memory 부족?
→ Network round trip 과다?
```

---

## 4.8 Redis on Kubernetes

Redis는 Stateful workload로 본다.

핵심:

```text
StatefulSet
Persistent Storage
HA
Backup / Restore
Failure Handling
```

### StatefulSet

```text
redis-0
redis-1
redis-2
```

stable identity 제공.

### Persistent Storage

```text
Redis Pod
↓
PVC
↓
PV
↓
Persistent Disk
```

### Kubernetes와 Redis HA의 역할 분리

```text
Kubernetes
= Pod 죽음 → 새 Pod 생성

Redis Sentinel / Cluster
= Primary 장애 판단 / Failover / 데이터 역할 복구
```

### Backup

Persistence와 Backup은 별도다.

```text
RDB / AOF
↓
별도 Backup
↓
외부 Storage
```

### Operator

Redis Cluster 생성, Failover, Scaling 등을 자동화하는 Kubernetes Controller를 사용할 수 있다.

---

<!-- SOURCE CORE END -->

## 보완 설명과 적용 조건

공식 문서 확인일: 2026-10-01. 아래는 원문을 고치지 않고 구분한 보완이다. Redis 설치, 부하 시험, 장애 전환 또는 복구를 실행한 기록은 아니다.

### 4.1 TTL의 의미

만료된 key는 접근할 때와 주기적인 만료 검사에서 제거된다. TTL은 애플리케이션에서 더 이상 유효하지 않은 시점을 나타내며, 그 순간 모든 메모리를 즉시 회수한다는 뜻은 아니다. [Redis EXPIRE](https://redis.io/docs/latest/commands/expire/).

### 4.2 Rate limit, lock, 중복 방지의 원자성

분당 counter는 시간 구간과 만료 정책이 있어야 한다. `INCR`와 `EXPIRE`를 별도 요청으로 처리하다 중단되면 만료가 빠지는 경쟁 조건이 생길 수 있으므로 공식 패턴의 원자적 처리 조건을 확인한다. [Redis INCR](https://redis.io/docs/latest/commands/incr/).

원문의 `없음 → 처리 → 기록` 흐름만으로 한 번의 처리를 보장할 수는 없다. 두 요청이 동시에 없음을 확인하거나 처리 직후 기록 전에 중단될 수 있다. 이는 원문 흐름에서 도출한 설계상 한계다. 결제 같은 외부 부작용에는 대상 저장소의 내구성 있는 idempotency 기록과 처리 결과를 함께 설계해야 한다. Redis marker 하나를 완전한 exactly-once 보장으로 해석하지 않는다.

Lock은 획득의 원자성, 만료, 소유자 식별자, 소유자 확인 후 해제를 함께 검토한다. 작업이 TTL보다 오래 걸리면 다른 client가 lock을 얻을 수 있다. 비동기 복제의 장애 전환도 상호 배제를 깨뜨릴 수 있다. 공식 lock 문서는 이런 보장 조건을 다루며 단순 `DEL`로 다른 소유자의 lock을 지우지 말라고 설명한다. [Redis distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/).

`5,000 × (1 − 0.95) = 250 req/s`는 각 miss가 DB 요청 하나이고 다른 DB traffic이 없다는 설명용 계산이다. Cache 도입 기준이나 실측 성능이 아니다. Cache 재구축 시 동시 miss가 DB에 미칠 부하도 따로 검토한다.

### 4.3 Persistence와 데이터 손실 범위

AOF를 켰다는 사실만으로 데이터 손실이 없어지지 않는다. `appendfsync` 정책과 저장장치 조건을 확인한다. `everysec` 정책에서는 장애 시 약 1초의 write를 잃을 수 있다. Redis 7.0부터 AOF는 base·incremental 파일과 manifest를 쓰므로 백업은 파일 집합의 일관성까지 고려해야 한다. RDB/AOF가 있어도 별도 보관과 복구 확인이 필요하다. [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).

### 4.4–4.6 HA와 Cluster의 조건

Sentinel의 장애 판단 quorum과 failover 승인에 필요한 Sentinel 과반수는 다르다. 독립적인 장애 영역에 Sentinel을 배치하고 client가 새 primary를 발견하고 재연결하는지 검토한다. Sentinel도 비동기 복제에서 이미 응답한 write의 손실을 완전히 막지는 못한다. [Redis Sentinel](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/).

Redis Cluster는 16,384 hash slot을 사용한다. 여러 key를 함께 쓰는 연산에는 같은 slot 조건이 있으므로 key 설계와 client의 Cluster 지원도 확인한다. Node 추가는 단일 hot key를 자동 분할하지 않는다. Cluster 역시 장애 시점과 복제 상태에 따른 write 손실 가능성이 있다. [Redis Cluster specification](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/).

### 4.7–4.8 메모리와 Kubernetes 역할

Fragmentation 지표만으로 누수를 단정하지 않는다. 데이터 크기와 allocator가 보유한 메모리, OS에 보이는 사용량을 함께 본다. [Redis memory optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/).

StatefulSet은 Pod 식별자와 저장소 연결을 유지하는 기반이다. Redis 역할 선출·복제·백업을 자동으로 구성하지 않는다. PVC만으로 백업이나 전체 장애 복구가 보장되지 않는다. [Kubernetes StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

## LLM in Practice: Redis 지연 원인 검토

- **상황:** Redis가 느려졌지만 원인이 확인되지 않았다.
- **제공 맥락:** 비식별 latency·hit/miss·key 분포·메모리·DB 부하와 관측 구간.
- **예시 prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Redis 지연과 cache miss 관측: [비식별 지표]
    key 크기·호출 분포·TTL·DB 부하·복제 상태: [자료]
    [요청]
    관측과 가정을 나누고 hot key·big key·동시 miss 가설을 검토하세요.
    [출력]
    각 가설의 근거, 누락 정보, 다음 읽기 전용 확인을 표로 작성하세요.
    [검증]
    낮은 hit rate 하나로 근본 원인을 단정하지 마세요.
    설정 변경·key 삭제·장애 전환 없이 검토안만 작성하세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Observed Redis latency and cache misses: [sanitized metrics]
    Key sizes, call distribution, TTL, DB load, and replication state: [material]
    [Task]
    Separate observations from assumptions and review hot-key, big-key, and concurrent-miss hypotheses.
    [Output]
    Make a table of evidence, missing information, and next read-only checks for each hypothesis.
    [Checks]
    Do not infer a root cause from a low hit rate alone.
    Draft a review without changing configuration, deleting keys, or triggering failover.
    ```

- **기대 결과:** 가설별 근거와 누락 정보, 추가 읽기 전용 확인 목록.
- **오류 가능성:** Cluster 추가만으로 hot key가 해결되거나 cache miss가 항상 DB 병목이라는 결론을 낼 수 있다.
- **검증:** 원본 지표·trace·설정과 대조하고 필요한 재현은 격리 환경에서 별도 수행한다. 이 문서에서 재현 시험은 실행하지 않았다.

[Redis](redis.md) · [PostgreSQL](postgresql.md) · [Kubernetes 운영](kubernetes-operations.md)
