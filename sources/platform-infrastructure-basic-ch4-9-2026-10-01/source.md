<!-- 반입 기록
범위: 업로드 Markdown 전체 1~3865행, Chapters 4~9 및 연결 구조·진도.
한계: Basic 개념 학습과 실무 질문의 기록이며 명령 실행·구축·성능 측정 증거가 아님.
원본 bytes: 49215; SHA-256: 22b642075e0101c311887240629a8833dce8b95ce476700e48b09882ebdccac7
정규화: 없음. 원문의 hard break와 모든 byte를 경계 뒤에 그대로 보존한다.
whitespace_restoration: []
-->
<!-- ORIGINAL SOURCE START -->
# Platform / Infrastructure / AI Serving — Basic Study Notes

> 범위: Chapter 4 ~ Chapter 9  
> 이전 파일: Chapter 1 ~ Chapter 3  
> 수준: Basic — 플랫폼 엔지니어가 반드시 알아야 할 핵심 개념 중심  
> 포함: 본 학습 내용 + 중간 실무 질문/보충 설명  
> 현재까지 완료: Redis / PostgreSQL / Kafka 운영 / vLLM / LiteLLM / GPU Infrastructure

---

# Chapter 4. Redis for Platform Systems

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

# Chapter 5. PostgreSQL for Platform Systems

## 5.1 PostgreSQL Architecture

PostgreSQL은 관계형 DB다.

플랫폼 관점 핵심 구조:

```text
Client
↓
PostgreSQL
↓
Memory + WAL + Disk
```

### Process Model

Client Connection마다 별도 PostgreSQL Process를 사용한다.

```text
Client A → Process A
Client B → Process B
Client C → Process C
```

Connection이 많아지면:

```text
Process 증가
↓
Memory 증가
↓
Context switching 증가
↓
성능 저하
```

### Shared Memory / Shared Buffers

자주 쓰는 데이터를 Memory에 캐시.

### WAL

WAL = Write-Ahead Log.

변경 내용을 실제 Table에 쓰기 전에 먼저 WAL에 기록한다.

```text
UPDATE
↓
WAL 기록
↓
변경 처리
↓
나중에 Disk 반영
```

용도:
- 장애 복구
- Replication
- PITR

---

## 5.2 Connection Management

핵심:

```text
max_connections
Connection Pool
PgBouncer
```

### Connection이 문제인 이유

예:

```text
100 Pods
×
20 Connections
=
2,000 DB Connections
```

PostgreSQL Connection은 Process/Memory를 사용하므로 너무 많으면 부담이 된다.

### max_connections

동시에 받을 수 있는 Connection 상한.

단순히 크게 늘리는 것이 항상 좋은 해결책은 아니다.

### Connection Pool

Connection을 매 요청마다 만들지 않고 재사용.

```text
Application
↓
Connection Pool
├─ Connection 1
├─ Connection 2
├─ Connection 3
└─ ...
↓
PostgreSQL
```

### Pod 하나가 DB Connection을 여러 개 가지는 이유

Pod 하나가 여러 사용자 요청을 동시에 처리하기 때문이다.

```text
Request 1 → DB query
Request 2 → DB query
Request 3 → DB query
```

Connection 하나만 있으면 DB 작업이 직렬화될 수 있다.

Connection Pool 10개라면 여러 DB 작업을 병렬로 처리할 수 있다.

중요:

```text
Pod 50개
×
Pool 20
=
최대 1,000 Connections
```

따라서 Pod replica 수와 pool size를 함께 계산해야 한다.

### PgBouncer

PostgreSQL 앞의 가벼운 Connection Pooler.

```text
Application Pods
↓
PgBouncer
↓
PostgreSQL
```

예:

```text
Application connections 1000
↓
PgBouncer
↓
PostgreSQL connections 100
```

특히 Kubernetes/Autoscaling 환경에 유용하다.

---

## 5.3 Transactions / MVCC

핵심:

```text
Transaction
Isolation
MVCC
Vacuum
```

### Transaction

여러 DB 작업을 하나의 논리적 단위로 묶음.

```text
BEGIN
↓
A 차감
↓
B 추가
↓
COMMIT
```

실패 시 ROLLBACK.

### Isolation

동시에 실행되는 Transaction이 서로의 작업을 어디까지 볼지 정함.

### MVCC

Multi-Version Concurrency Control.

> 여러 데이터 버전을 유지해서 Read와 Write가 서로 덜 막히게 함

```text
Reader
→ 기존 버전 읽음

Writer
→ 새 버전 생성
```

### Vacuum

오래된 Row Version 정리.

```text
UPDATE / DELETE
↓
Old Version 증가
↓
Vacuum
```

### Autovacuum

Vacuum 자동 수행.

제대로 동작하지 않으면 Table/Index가 커지고 성능 저하 가능.

### Lock

같은 Row를 여러 Transaction이 동시에 수정하면 Lock 경쟁 가능.

```text
Read + Write
→ 비교적 병렬 처리

Write + Write
→ Lock 경쟁 가능
```

---

## 5.4 Index / Query Performance

핵심:

```text
Index
B-tree
Query Planner
EXPLAIN
Slow Query
Lock
```

### Index

Table 전체를 다 뒤지지 않고 데이터를 빠르게 찾기 위한 구조.

### B-tree

가장 기본적인 Index.

```sql
CREATE INDEX idx_users_email
ON users(email);
```

주로 `=`, `<`, `>`, 범위 조회, 정렬 등에 사용.

### Index Trade-off

```text
Read 성능 향상 가능
Write 비용 증가
Disk 사용 증가
```

### Query Planner

SQL 실행 전에 Seq Scan / Index Scan / Join 방식 등을 선택.

### EXPLAIN

```sql
EXPLAIN SELECT ...;
EXPLAIN ANALYZE SELECT ...;
```

### Slow Query 원인

```text
Index 없음
너무 많은 Row Scan
비효율적 Join
너무 많은 데이터 반환
Lock 대기
```

### 기본 튜닝 순서

```text
1. 느린 Query 확인
2. EXPLAIN
3. Seq Scan 여부
4. 필요한 Index 확인
5. 읽는 Row 수 확인
6. Lock 대기 확인
```

중요한 원칙:

> DB가 느리다고 바로 Redis부터 넣지 말고 Query와 Index를 먼저 확인한다.

---

## 5.5 PostgreSQL HA

핵심:

```text
Primary
Standby
Streaming Replication
Synchronous / Asynchronous
Failover
```

### Streaming Replication

WAL을 Standby에 전달.

```text
Primary
↓
WAL
↓
Standby
```

### Asynchronous

```text
Client Write
↓
Primary 반영
↓
Client 응답
↓
Standby 따라옴
```

빠르지만 최근 데이터 유실 가능.

### Synchronous

```text
Client Write
↓
Primary
↓
Standby 반영 확인
↓
Client 응답
```

데이터 안정성은 높지만 Write latency가 증가할 수 있다.

### Failover

```text
Primary ❌
↓
Standby
↓
새 Primary
```

### Read Replica

Read 부하 분산에 사용 가능.

비동기 복제라면 약간 오래된 데이터가 보일 수 있다.

---

## 5.6 Backup / Recovery

HA가 있어도 Backup은 별도로 필요하다.

예:

```text
Primary에서 잘못된 DELETE
↓
Replication
↓
Standby에서도 삭제
```

핵심:

```text
Logical Backup
Physical Backup
WAL Archiving
PITR
```

### Logical Backup

대표: `pg_dump`

논리적인 Schema/Table/Row를 백업.

### Physical Backup

실제 PostgreSQL 데이터 파일 단위 백업.

### WAL Archiving

```text
Primary
↓
WAL 생성
↓
Archive Storage
```

### PITR

Point-In-Time Recovery.

```text
Base Backup
+
WAL Archive
↓
원하는 시점까지 Replay
```

예:

```text
10:00 Backup
10:45 Table 실수 삭제
→ 10:44로 복구
```

### HA vs Backup

```text
Replication / HA
→ 서버 장애 대비

Backup / PITR
→ 운영 실수 / 데이터 손상 대비
```

---

## 5.7 Operational Tuning

핵심:

```text
Connection
Memory
Autovacuum
Checkpoint
Disk I/O
```

### Memory

Basic에서 대표적으로:

```text
shared_buffers
work_mem
```

- shared_buffers: 데이터 캐시
- work_mem: 정렬/Join 등 Query 작업용 Memory

work_mem을 너무 크게 잡으면 동시 Query가 많을 때 총 Memory 사용량이 커질 수 있다.

### Autovacuum

```text
UPDATE / DELETE
↓
Dead Tuple 증가
↓
Autovacuum
```

### Checkpoint

메모리의 변경 데이터를 Disk에 반영하는 기준점.

```text
Checkpoint
→ Disk I/O와 Recovery에 영향
```

### 운영 튜닝 순서

```text
1. Slow Query
2. Index / Query Plan
3. Connection
4. Memory
5. Autovacuum
6. Disk I/O
```

---

## 5.8 PostgreSQL on Kubernetes

PostgreSQL은 Stateful workload.

핵심:

```text
StatefulSet
Persistent Storage
Operator
Failover
Backup
```

### StatefulSet

```text
postgres-0 → Primary
postgres-1 → Standby
postgres-2 → Standby
```

### Persistent Storage

```text
PostgreSQL Pod
↓
PVC
↓
PV
↓
Persistent Disk
```

### Kubernetes와 PostgreSQL HA 역할 분리

```text
Kubernetes
= Pod lifecycle 복구

PostgreSQL HA
= Primary / Standby / Replication / Failover
```

### Operator

PostgreSQL 운영 로직을 Kubernetes Controller로 자동화.

예:

```text
Primary 생성
Standby 생성
Replication
Failover
Backup
Restore
Upgrade
```

### PostgreSQL을 K8s에 구축할 때 Operator가 선행되어야 하는가?

반드시 아니다.

#### 직접 구축

```text
Kubernetes
↓
StatefulSet
↓
PostgreSQL
↓
PVC / PV
```

Operator 없이 가능.

하지만 Primary/Standby, Replication, Failover, Backup, Upgrade, Recovery를 직접 관리해야 한다.

#### Operator를 사용한다면

```text
1. Kubernetes Cluster 준비
2. PostgreSQL Operator 설치
3. CRD 등록
4. PostgreSQL Cluster Custom Resource 생성
5. Operator가 실제 PostgreSQL 구성 생성
```

즉 Operator를 이용한다면 Operator 설치가 먼저다.

Operator는 Kubernetes에게 PostgreSQL 운영 방법을 추가해주는 것이라고 이해하면 된다.

### Persistent Volume ≠ Backup

PVC/PV가 있어도 운영 실수는 그대로 저장된다.

```text
DROP TABLE users;
```

따라서 Backup / WAL Archive / PITR는 별도다.

### Managed DB

실제 Platform에서는:

```text
Kubernetes Application
↓
Managed PostgreSQL
```

예:

```text
EKS
↓
RDS PostgreSQL
```

구조도 매우 흔하다.

---

# Chapter 6. Kafka for Platform Systems

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

# Chapter 7. vLLM

## 7.1 LLM Serving Fundamentals

vLLM은 LLM Inference Server다.

### Model Serving

```text
LLM Model
↓
GPU Memory Load
↓
Inference Server
↓
사용자 요청
```

### Training vs Inference

```text
Training
→ 모델 학습

Inference
→ 학습된 모델로 답변 생성
```

### Token

LLM이 처리하는 기본 단위.

```text
Input Tokens
Output Tokens
```

### Prefill

입력 Prompt 전체를 처리하는 단계.

### Decode

출력 Token을 반복적으로 하나씩 생성하는 단계.

전체 흐름:

```text
Request
↓
Prompt Tokens
↓
Prefill
↓
Decode
↓
Output Tokens
↓
Response
```

---

## 7.2 GPU Memory

핵심:

```text
Model Weights
KV Cache
Activation
Runtime Memory
```

### Model Weights

학습된 모델의 parameter.

### Precision

```text
FP32 → 4 bytes
FP16/BF16 → 2 bytes
INT8/FP8 → 약 1 byte
```

### KV Cache

이전 Token 계산 결과를 저장해 Decode 시 재사용.

```text
Prompt / 생성 Token
↓
KV Cache
↓
다음 Token 생성에 재사용
```

### KV Cache 증가 요인

```text
동시 Request ↑
Context Length ↑
→ KV Cache ↑
```

### Activation

현재 연산 중 필요한 임시 데이터.

### VRAM 구조

```text
GPU VRAM
├─ Model Weights
├─ KV Cache
├─ Activation
└─ Runtime
```

---

## GLM-5.3 / B200 / B300 실무 계산

### B200에서 GLM-5.3 FP32를 가정했을 때

GLM-5.3 계열은 약 744B total parameters / 40B active parameters인 MoE 모델로 봤다.

FP32 Weight 단순 계산:

```text
744B × 4 bytes
≈ 2.98TB
```

B200 1장 180GB라면 Weight만 넣어도 최소 17장 이상 필요.

실제 Serving에는:

```text
Weight
KV Cache
Activation
Runtime
Communication buffer
```

가 추가로 필요하므로 더 많은 GPU가 필요하다.

### MoE 특징

```text
Total parameters ≈ 744B
Active parameters ≈ 40B
```

Compute는 일부 Expert만 활성화되지만 Memory에는 전체 Expert Weight가 필요하다.

### Precision별 단순 Weight Memory

```text
FP32 ≈ 2.98TB
BF16 ≈ 1.49TB
FP8  ≈ 744GB
FP4  ≈ 372GB
```

실제는 scale / metadata / quantization overhead로 차이가 생길 수 있다.

### 동시 사용자 수는 GPU Memory만으로 결정되지 않음

```text
Concurrency
=
GPU Memory
+
GPU Compute
+
Context Length
+
Output Length
+
목표 tokens/sec
```

Memory에 많은 Sequence가 들어가도 빠르게 처리할 수 있는지는 별도다.

---

## KV Cache와 Context Length

KV Cache는 Context 길이에 거의 선형적으로 증가한다.

```text
KV Cache
≈ 토큰당 KV 크기
× 현재 Context Token 수
× 동시 Sequence 수
```

예:

```text
Input = 8K
Output generated = 2K

Current context ≈ 10K
```

10K에 대한 KV Cache를 유지한다.

### 일반 Transformer 토큰당 KV Cache 공식

```text
KV Cache / token
≈ 2 × Layers × KV Heads × Head Dimension × Bytes
```

`2`는 K + V.

예:

```text
Layers = 80
KV Heads = 8
Head Dim = 128
BF16 = 2 bytes

2 × 80 × 8 × 128 × 2
= 327,680 bytes
≈ 320 KiB / token
```

대략:

```text
1K context   ≈ 320 MiB
8K context   ≈ 2.5 GiB
32K context  ≈ 10 GiB
128K context ≈ 40 GiB
```

### 모델마다 KV Cache 크기 다름

```text
KV Cache
∝
Token 수
× Layer 수
× KV Head 수
× Head Dimension
× KV precision
```

GQA/MQA는 KV Head 수를 줄여 KV Cache를 줄일 수 있다.

### Weight precision과 KV precision은 별개

```text
Model Weight precision
≠
KV Cache precision
```

예:

```text
Weight = BF16
KV Cache = FP8
```

가능.

---

## GLM-5.3의 1M Context와 KV Cache

GLM-5.3은 일반 MHA/GQA보다 MLA 계열의 압축 KV 표현을 사용한다고 보고 계산했다.

이 세션에서 사용한 단순 근사:

```text
(kv_lora_rank 512 + rope dim 64)
× 78 layers
× BF16 2 bytes
≈ 87.8 KiB / token
```

따라서 core MLA cache 단순 근사:

```text
1M context
≈ 약 87.8 GiB / request
```

FP8 KV라면 대략 절반 수준:

```text
1M context
≈ 약 44 GiB / request
```

실제 vLLM에서는 block allocation / padding / indexer cache / runtime overhead 등이 추가될 수 있으므로 실측이 필요하다.

### 30명 개발자 + 1M Context

30명이 동시에 1M Context를 꽉 채운다고 단순 가정:

BF16 KV:

```text
87.8 GiB × 30
≈ 2.57 TiB
```

FP8 KV:

```text
약 44 GiB × 30
≈ 1.3 TiB
```

따라서:

```text
30 Developers
+
Coding Agent
+
1M Context
```

환경이라면 매우 큰 KV Cache HBM이 합리적일 수 있다.

중요:

```text
1M Context 지원
≠
항상 1M 사용
```

실제 봐야 할 값:

```text
평균 active context
P95 context
Peak concurrent sequences
kv_cache_dtype
KV cache utilization
```

---

## B300 2대 / GLM-5.3 FP4 3개 관련 실무 연결

사용자 설명:
- 서버 1대당 GPU 8장
- B300 서버 2대
- 총 GPU 16장
- GLM-5.3 FP4 모델 3개 Serving
- 일부 공간은 KV Cache / 학습 용도 여유

가능한 예시 구조:

```text
B300 Server #1
GPU 0~3 → GLM Replica A
GPU 4~7 → GLM Replica B

B300 Server #2
GPU 0~3 → GLM Replica C
GPU 4~7 → Training / Spare Capacity
```

이는 실제 `tensor_parallel_size`를 확인해야 확정 가능.

### B300 Memory

B300 1장 약 288GB HBM이라고 보면:

```text
1 server = 8 GPUs
≈ 2.3TB HBM

2 servers
≈ 4.6TB HBM
```

### GLM-5.3 FP4 단순 Weight

```text
744B × 0.5 byte
≈ 372GB
```

실제 quantization overhead 포함 시 더 커질 수 있다.

### Replica 하나가 B300 4장이라면

```text
4 × 288GB
≈ 1.15TB HBM
```

대략:

```text
Weight ≈ 400GB 전후+
KV Cache = 상당한 나머지
Activation
Runtime
Communication buffers
```

### 남은 VRAM과 Training

같은 GPU에서 vLLM Serving과 Training을 동시에 하는 것은:

```text
VRAM
GPU Compute
Memory Bandwidth
```

를 경쟁하므로 운영이 까다롭다.

더 깔끔한 구조:

```text
Serving 전용 GPU
+
Training / Experiment 전용 GPU
```

### 30명만 보면 과해 보일 수 있지만

일반 Chat + 짧은 Context라면 과할 수 있다.

하지만:

```text
30 Developers
+
1M Context
+
Coding Agent workload
```

면 완전히 다른 Capacity 요구가 된다.

---

## 7.3 PagedAttention

PagedAttention:

> KV Cache를 큰 연속 공간으로 잡지 않고 작은 Block/Page 단위로 관리

### 기존 문제

요청마다 앞으로 얼마나 길어질지 모르므로 큰 연속 공간을 미리 잡으면 낭비 발생.

### Block 기반

```text
GPU KV Cache
[Block][Block][Block][Block]...
```

Request마다 필요한 Block만 할당.

### 효과

```text
Memory waste ↓
Fragmentation ↓
Concurrent sequences ↑
Throughput ↑
```

### 주의

PagedAttention은:
- Weight를 줄이지 않음
- Token 수를 줄이지 않음
- KV Cache 배치를 효율화함

---

## 7.4 Continuous Batching

> 여러 요청을 묶어 처리하되, 끝난 요청 자리에 새 요청을 계속 넣는 방식

### Static Batching 문제

```text
A 20 tokens
B 500 tokens
C 100 tokens
```

A/C가 빨리 끝나도 B 때문에 자리가 비효율적으로 남을 수 있다.

### Continuous Batching

```text
A 종료 → D 투입
C 종료 → E 투입
```

### 효과

```text
GPU utilization ↑
Throughput ↑
```

PagedAttention과 결합:

```text
새 Request
↓
KV Block 할당
↓
Batch 참여
↓
완료
↓
KV Block 반환
↓
새 Request 투입
```

Concurrency를 너무 높이면 Queue/TTFT/TPOT이 악화될 수 있다.

---

## 7.5 Performance Metrics

핵심:

```text
TTFT
TPOT
Tokens/sec
Throughput
Queue Time
```

### TTFT

Time To First Token.

```text
Request
↓
Queue
↓
Prefill
↓
첫 Token
```

### TPOT

Time Per Output Token.

예:

```text
TPOT = 50ms
→ 약 20 tok/s
```

### Throughput

서버 전체 처리량.

```text
output tokens/sec
requests/sec
```

### Queue Time

GPU 처리 전에 기다리는 시간.

### 관계

```text
Request
↓
Queue Time
↓
Prefill
↓
첫 Token ← TTFT
↓
Decode
↓
Token ... ← TPOT / tok/s
```

Concurrency 증가 시 Throughput은 올라갈 수 있지만 어느 시점부터 Queue와 Latency가 급격히 악화된다.

---

## 7.6 Parallelism

핵심:

```text
Tensor Parallelism
Pipeline Parallelism
Data Parallelism
```

### Tensor Parallelism

하나의 Layer 연산을 여러 GPU가 나눠 처리.

```text
GPU 0 ─┐
GPU 1 ─┼→ 같은 Layer
GPU 2 ─┤
GPU 3 ─┘
```

모델이 GPU 한 장에 안 들어갈 때 중요.

### Pipeline Parallelism

Layer 구간을 GPU별로 분할.

```text
GPU0 → Layer 1~20
GPU1 → Layer 21~40
GPU2 → Layer 41~60
GPU3 → Layer 61~80
```

### Data Parallelism

모델 전체 Replica를 여러 개 운영해 요청 분산.

### 조합

```text
GPU 0~3 → Replica A, TP=4
GPU 4~7 → Replica B, TP=4
```

핵심:

```text
모델이 너무 크다
→ TP / PP

사용자가 너무 많다
→ DP / Replica 증가
```

---

## 7.7 Quantization

> 모델 Weight precision을 낮춰 VRAM 사용량과 연산 비용을 줄이는 기술

### Precision

```text
FP32 ≈ 4 bytes
FP16/BF16 ≈ 2 bytes
INT8/FP8 ≈ 1 byte
4-bit/FP4 ≈ 0.5 byte
```

### 효과

```text
Weight VRAM ↓
필요 GPU 수 ↓
비용 ↓
남는 VRAM ↑
KV Cache Capacity ↑
```

### Trade-off

```text
Precision ↓
→ 모델 품질 저하 가능
```

### AWQ / GPTQ

대표적인 low-bit Weight Quantization 방식.

### Weight Quantization과 KV Cache는 별개

```text
Weight = FP8
KV Cache = BF16
```

가능.

---

## 7.8 vLLM API Server

vLLM은 OpenAI-compatible API Server 형태로 Serving 가능.

```text
Client
↓
POST /v1/chat/completions
↓
vLLM
↓
Model
↓
GPU
```

주요 서버 설정:

```text
Model
GPU 수
Tensor Parallel
Max Context
GPU Memory Utilization
Quantization
```

주요 요청 설정:

```text
max_tokens
temperature
top_p
```

---

## 7.9 vLLM on Kubernetes

핵심:

```text
GPU Request
GPU Node Scheduling
Replica
Readiness
Autoscaling
```

### GPU Resource Request

```yaml
resources:
  limits:
    nvidia.com/gpu: 1
```

### GPU Node 배치

```text
Node Label
Node Affinity
Taint
Toleration
```

### Multi-GPU Pod

```text
Tensor Parallel = 4
GPU Request = 4
```

보통 같은 Node의 GPU 4장을 쓰는 게 유리하다.

### Startup / Readiness

```text
Pod Running
≠
Model Ready
```

```text
Container
↓
Model Load
↓
VRAM 할당
↓
KV Cache 준비
↓
Ready
```

### Autoscaling

일반 API보다 Scale-out 시간이 길 수 있다.

```text
Pod 생성
↓
Image Pull
↓
Model Load
↓
GPU Memory Load
↓
Readiness
```

Queue / TTFT / GPU Utilization 등의 지표를 함께 봐야 한다.

GPU가 없으면 Pod Pending.

---

## 7.10 Production Serving

핵심:

```text
Model Startup
Failure Recovery
Scaling
Rolling Update
```

### Failure Recovery

```text
vLLM Pod 장애
↓
Kubernetes 재시작
↓
Model Reload
↓
Readiness
```

Replica 하나뿐이면 Reload 동안 서비스 영향 가능.

### Scaling

```text
Request 증가
↓
Queue / TTFT 악화
↓
vLLM Replica 증가
↓
GPU Capacity 필요
```

### Rolling Update

```text
새 Replica 준비
↓
Readiness 성공
↓
기존 Replica 제거
```

### Production Metrics

```text
GPU Utilization
GPU Memory
Queue Length
TTFT
TPOT
Throughput
Error Rate
Pod Restart Count
```

### Graceful Shutdown

```text
새 요청 차단
↓
기존 요청 마무리
↓
Pod 종료
```

---

# Chapter 8. LiteLLM

## 8.1 LiteLLM 역할

LiteLLM은 여러 LLM Provider와 vLLM 앞에 두는 LLM Gateway다.

### 기본 구조

```text
Applications
↓
LiteLLM
↓
├─ vLLM
├─ OpenAI
├─ Anthropic
└─ 기타 Provider
```

### 주요 역할

```text
Unified API
Routing
Load Balancing
Retry / Fallback
Authentication
Rate Limit
Quota / Budget
Cost Tracking
Caching
Observability 연동
```

### vLLM과 차이

```text
vLLM
= 실제 모델 Inference

LiteLLM
= Gateway / Control Layer
```

---

## 8.2 Provider Routing

> 요청을 어떤 실제 모델 / Provider / Deployment로 보낼지 결정

### 같은 모델 여러 Deployment

```text
qwen-32b
├─ vLLM A
├─ vLLM B
└─ vLLM C
```

### 서로 다른 Provider

```text
internal-chat
↓
Primary → 사내 vLLM
Fallback → External Provider
```

### Routing 기준

```text
Weight
Latency
Load
Rate Limit
Cost
Custom
```

### Session Affinity

같은 Conversation을 가능하면 같은 Backend에 계속 보낼 수 있다.

---

## 8.3 Load Balancing

같은 모델 Backend 여러 개에 요청 분산.

```text
LiteLLM
├─ vLLM A
├─ vLLM B
└─ vLLM C
```

LLM에서는 요청 수만 같다고 부하가 같은 게 아니다.

```text
Request A → 1K input
Request B → 100K input
```

따라서:

```text
현재 처리 요청 수
Queue
RPM / TPM
Latency
Backend Health
```

같은 상태도 중요하다.

### Kubernetes Service와 차이

```text
Kubernetes Service
→ Network Endpoint 분산

LiteLLM
→ Model / Provider / Replica 수준 분산
→ Rate Limit / Latency / Health / Fallback 고려
```

---

## 8.4 Retry / Fallback

핵심:

```text
Retry
Timeout
Fallback
Health-aware routing
```

### Retry

일시적 실패 시 다시 시도.

### Retry Storm

```text
Backend 과부하
↓
실패
↓
Retry 증가
↓
더 과부하
```

따라서 Retry 횟수 제한 / Timeout / Backoff가 필요.

### Fallback

다른 모델/Provider로 우회.

```text
GLM
↓ 실패
Qwen
↓ 실패
External Provider
```

### Retry vs Fallback

```text
Retry
= 같은 요청 재시도

Fallback
= 다른 Backend / Model / Provider
```

---

## 8.5 Rate Limiting

> 사용자/팀의 과도한 LLM 사용 제한

목적: Noisy Neighbor 방지.

### RPM

Requests Per Minute.

### TPM

Tokens Per Minute.

LLM에서는 요청 수보다 Token 사용량이 실제 GPU 부하를 더 잘 반영할 수 있다.

### Concurrency Limit

동시에 처리 가능한 요청 수 제한.

### 적용 단위

```text
User
Team
API Key
Application
Tenant
```

### Rate Limit vs Autoscaling

```text
Autoscaling
= Capacity 늘림

Rate Limiting
= 들어오는 부하 제한
```

---

## 8.6 Budget / Quota

```text
Rate Limit
→ 1분 100 requests

Quota
→ 하루 100만 tokens

Budget
→ 월 $100
```

### Token Quota

팀별 일간/월간 Token 한도.

### Spend Budget

외부 Provider 비용 제한.

### 내부 vLLM도 Quota 필요

API 비용이 없어도:

```text
GPU 구매 비용
전력
운영 비용
Capacity
```

가 있기 때문에 팀별 공정성 관리가 필요하다.

---

## 8.7 Authentication

Authentication:

> 누가 요청했는가?

대표: API Key.

```text
Authorization: Bearer <API_KEY>
```

### 팀별 Key

```text
Team A → Key A
Team B → Key B
Service C → Key C
```

이를 기준으로 Rate Limit / Quota / Budget / Model Access를 적용할 수 있다.

### Authentication vs Authorization

```text
Authentication
= 누구인가?

Authorization
= 무엇을 할 수 있는가?
```

기업 환경에서는 SSO/IAM과 연동할 수 있다.

---

## 8.8 Caching

> 같은 LLM 요청의 이전 응답 재사용

기본 흐름:

```text
Request
↓
LiteLLM
↓
Cache
├─ HIT  → 바로 응답
└─ MISS → vLLM / Provider
           ↓
         Cache 저장
```

### Redis

여러 LiteLLM Replica가 Cache 공유.

```text
LiteLLM A ─┐
LiteLLM B ─┼→ Redis
LiteLLM C ─┘
```

### Exact Cache

완전히 같은 요청.

### Semantic Cache

의미가 비슷한 요청.

Agent / 대화형 traffic에서는 잘못된 Cache Hit에 주의.

### 효과

```text
Latency ↓
GPU 사용량 ↓
외부 API 비용 ↓
Throughput 여유 ↑
```

---

## 8.9 LiteLLM on Kubernetes

LiteLLM은 Stateless Gateway로 운영하기 좋다.

### Deployment

```text
Deployment
replicas: 3
↓
LiteLLM Pod A
LiteLLM Pod B
LiteLLM Pod C
```

### 상태 외부화

```text
Cache → Redis
Usage / Key / 설정 → DB / 외부 저장소
Secret → Kubernetes Secret / Secret Manager
```

### Scaling

```text
LiteLLM 부하 증가
→ Gateway Pod 증가

GPU Queue 증가
→ vLLM Replica / GPU Node 증가
```

중요:

```text
LiteLLM Replica 증가
≠
GPU Capacity 증가
```

---

## 8.10 LiteLLM + vLLM Architecture

전체 구조:

```text
Applications
↓
Load Balancer
↓
LiteLLM Replicas
↓
├─ Qwen Pool
├─ GLM Pool
└─ External LLM
↓
vLLM
↓
GPU
```

### LiteLLM 역할

```text
Authentication
Authorization
Routing
Load Balancing
Retry
Fallback
Rate Limit
Quota / Budget
Caching
```

### vLLM 역할

```text
Model Weight Loading
GPU Inference
KV Cache
PagedAttention
Continuous Batching
Token Generation
```

### Request Flow

```text
1. Request
2. Authentication
3. Authorization
4. Rate Limit / Quota
5. Cache
6. Model Pool 선택
7. vLLM Replica 선택
8. GPU Inference
9. Response
```

### Scaling 계층

```text
LiteLLM Scaling
→ Gateway Capacity

vLLM Scaling
→ Serving Capacity

GPU Node Scaling
→ Compute Capacity
```

### 병목 구분

```text
LiteLLM CPU 100%
→ Gateway 병목

vLLM Queue 증가
→ Serving 부족

GPU Memory 부족
→ KV Cache / Model 문제

GPU Utilization 100%
→ Compute 부족
```

---

# Chapter 9. GPU Infrastructure & Scheduling

## 9.1 GPU Fundamentals

GPU는 대규모 병렬 연산을 빠르게 처리하는 가속기다.

핵심:

```text
CPU vs GPU
CUDA
VRAM
GPU Compute
```

### CPU vs GPU

CPU:
- 범용 로직
- OS
- Application
- DB

GPU:
- Matrix multiplication
- Tensor 연산
- AI training / inference

### CUDA

```text
Application / PyTorch / vLLM
↓
CUDA
↓
NVIDIA GPU
```

### VRAM

GPU 전용 Memory.

LLM Serving에서:

```text
Model Weights
KV Cache
Activation
Runtime
```

사용.

### VRAM vs Compute

```text
VRAM
= 얼마나 담을 수 있는가

GPU Compute
= 얼마나 빠르게 계산하는가
```

예:

```text
VRAM 95%
GPU Util 20%
→ Memory 많이 차지, Compute 여유

VRAM 60%
GPU Util 100%
→ Compute 병목
```

---

## 9.2 NVIDIA Container Stack

핵심 구조:

```text
vLLM
↓
CUDA Runtime
↓
NVIDIA Container Toolkit
↓
NVIDIA Driver
↓
GPU
```

### NVIDIA Driver

Host OS가 GPU를 제어.

대표 확인 명령:

```bash
nvidia-smi
```

### CUDA Runtime

Container 안에서 vLLM/PyTorch가 GPU 연산을 사용하는 실행 환경.

### NVIDIA Container Toolkit

Host GPU를 Container에서 사용할 수 있게 연결.

### Driver는 Host에

```text
Host
└─ NVIDIA Driver

Container
└─ CUDA Runtime
```

### Version Compatibility

Container CUDA Runtime과 Host NVIDIA Driver의 호환성이 중요하다.

---

## 9.3 Kubernetes GPU

핵심:

```text
Device Plugin
GPU Resource Request
GPU Scheduling
```

### NVIDIA Device Plugin

Kubernetes에 Node의 GPU Resource를 등록.

예:

```text
nvidia.com/gpu = 8
```

### Pod GPU Request

```yaml
resources:
  limits:
    nvidia.com/gpu: 4
```

### Scheduling

GPU 여유가 있는 Node를 Scheduler가 선택.

### 기본 GPU 할당

보통 정수 단위:

```text
1 GPU
2 GPU
4 GPU
```

0.5 GPU 같은 공유는 별도 기술 필요.

### GPU 부족

```text
GPU Capacity 없음
↓
Pod Pending
```

### Device Plugin vs Container Toolkit

```text
Device Plugin
→ Kubernetes가 GPU를 스케줄링 가능하게 함

Container Toolkit
→ Container가 실제 GPU를 사용하게 함
```

---

## 9.4 GPU Node Pool

> GPU Node를 일반 Node와 별도 그룹으로 관리

### 구조

```text
Kubernetes Cluster

General Node Pool
├─ Node A
├─ Node B

GPU Node Pool
├─ B300 Node 1
└─ B300 Node 2
```

### Label / Affinity

```text
gpu=true
gpu-type=b300
```

### Taint

일반 Pod가 GPU Node에 못 들어오게 제한.

### Toleration

GPU workload가 해당 Node에 들어갈 수 있게 허용.

### Affinity + Toleration

```text
Affinity
→ 어디로 갈지 선택

Toleration
→ 그 Node에 들어갈 수 있게 허용
```

---

## 9.5 GPU Sharing

핵심:

```text
Dedicated GPU
Time Slicing
MIG
MPS
```

### Dedicated GPU

GPU 한 장을 한 workload가 전용 사용.

장점:
- 성능 예측 쉬움
- 간섭 적음

### Time Slicing

시간을 나눠 여러 workload가 같은 GPU를 사용.

장점:
- utilization 향상

단점:
- 성능 간섭
- latency 변동

### MIG

Multi-Instance GPU.

GPU를 여러 격리된 작은 GPU Instance로 분할.

```text
GPU
├─ MIG A
├─ MIG B
└─ MIG C
```

### MPS

Multi-Process Service.

여러 CUDA Process가 하나의 GPU를 효율적으로 공유.

### 선택 감각

```text
대형 Production LLM
→ Dedicated

작은 실험 여러 개
→ Time Slicing

강한 분할/격리
→ MIG

여러 CUDA Process
→ MPS
```

---

## 9.6 Multi-GPU

핵심:

```text
PCIe
NVLink
NCCL
Inter-GPU Communication
```

### 왜 통신하나

Tensor Parallel에서는 GPU끼리 같은 Layer 계산 결과를 계속 교환.

### PCIe

범용 시스템 연결.

### NVLink

GPU ↔ GPU 고속 연결.

TP 같은 workload에서 중요.

### NCCL

NVIDIA Collective Communications Library.

GPU 간 통신 Library.

### TP와 통신

```text
GPU 계산
↓
다른 GPU와 결과 교환
↓
다음 Layer
```

통신이 느리면 GPU가 서로를 기다려 전체 inference가 느려진다.

가능하면 TP GPU들을 같은 Node에 배치하는 것이 좋다.

---

## 9.7 Multi-Node Inference

> 하나의 모델을 여러 GPU 서버에 걸쳐 실행

### 구조

```text
Server A GPUs
↕
Network
↕
Server B GPUs
```

### Single-Node와 차이

같은 Node:
- NVLink 등 고속 interconnect

다른 Node:
- Network를 거침

### RDMA

Remote Direct Memory Access.

CPU 개입을 줄여 서버 간 Memory 데이터 전송을 빠르게 하는 기술.

### InfiniBand

AI/HPC용 고속 저지연 Network.

### NCCL Multi-Node

NCCL은 여러 서버 GPU 간 통신에도 사용.

### 원칙

```text
가능하면 Single-Node
↓
한 Node에 안 들어갈 때 Multi-Node
```

---

## 9.8 GPU Capacity Planning

질문:

> 어떤 모델을, 어느 Context와 동시 사용자로 서비스하려면 GPU가 몇 장 필요한가?

핵심:

```text
Model Weight
KV Cache
Concurrency
Compute Capacity
Replica 수
```

### 1. Model Weight 계산

```text
Weight Memory
≈ Parameter 수 × Precision
```

### 2. 남는 VRAM 계산

```text
GPU VRAM
- Model Weight
- Runtime/Activation
=
KV Cache 여유
```

### 3. KV Cache

```text
KV Cache
≈ token당 KV
× active context tokens
× concurrent sequences
```

### 4. Compute

Memory에 들어간다고 충분한 건 아니다.

```text
Concurrency ↑
↓
GPU utilization ↑
↓
Queue ↑
↓
TTFT / TPOT 악화
```

### 5. Benchmark

예:

```text
Concurrency 1
5
10
20
```

각 구간에서:

```text
TTFT
TPOT
Throughput
GPU Utilization
GPU Memory
KV Cache Utilization
Queue
```

을 측정.

### 6. Replica 수

예:

```text
Replica 1개
→ concurrent 8까지 SLA 만족

Peak concurrency = 24
→ 최소 3 replicas 정도부터 검토
```

여기에 장애 여유를 추가.

### 기본 순서

```text
1. Model Size
2. Precision
3. 최소 GPU 수
4. 남는 VRAM
5. KV Cache Capacity
6. Context / Concurrency
7. Benchmark
8. Replica 수
9. HA Spare Capacity
```

### 현재 B300 / GLM 환경에서 확인할 값

```text
Replica당 GPU 수
실제 Weight 크기
KV Cache dtype
평균 / P95 Context
Peak concurrency
Replica별 KV Cache utilization
TTFT / TPOT
```

---

## 9.9 GPU Failure / Operations

핵심:

```text
GPU OOM
GPU Unhealthy
Driver / CUDA 문제
GPU Node 장애
복구 / 교체
```

### GPU OOM

```text
Model Weight
+ KV Cache
+ Activation
+ Runtime
>
VRAM
```

→ CUDA Out of Memory.

대표 원인:

```text
Context 너무 김
동시 요청 많음
Model 큼
gpu_memory_utilization 공격적
```

해결 방향:

```text
Concurrency 감소
Context 제한
KV dtype 조정
Quantization
GPU 추가
TP 증가
```

### Kubernetes OOMKilled와 구분

```text
Container RAM 부족
→ OOMKilled

GPU VRAM 부족
→ CUDA OOM
```

### GPU Unhealthy

TP=4에서 GPU 하나 장애:

```text
GPU0 ✅
GPU1 ✅
GPU2 ❌
GPU3 ✅

→ Replica 전체 장애 가능
```

### Driver / CUDA Stack

문제 계층:

```text
vLLM
↓
CUDA Runtime
↓
Container Toolkit
↓
NVIDIA Driver
↓
GPU
```

### GPU Node 장애

다른 Node에 충분한 GPU가 있어야 재배치 가능.

예:

```text
Replica가 GPU 4개 필요
다른 Node 여유 2개
→ Pod Pending
```

### Spare Capacity

GPU를 100% 모두 쓰면 장애 복구가 어려울 수 있다.

```text
총 16 GPUs
현재 16 사용
→ Node 장애 시 재배치 불가
```

여유가 있으면:

```text
총 16
12 사용
4 spare

→ 4-GPU Replica 재생성 가능
```

즉 여유 GPU는 낭비가 아니라 HA Capacity일 수 있다.

### Node 교체

```text
Cordon
↓
Drain
↓
점검 / 교체
↓
정상 확인
↓
Cluster 재참여
```

### 운영 Metric

```text
GPU Utilization
VRAM Usage
Temperature
GPU Error
Pod Restart
CUDA Error
vLLM Queue
TTFT / TPOT
```

### Memory vs Compute 병목

```text
GPU Util 낮음
VRAM 거의 꽉 참
CUDA OOM
→ Memory Capacity 문제

VRAM 여유
GPU Util 100%
Queue 증가
→ Compute Capacity 문제
```

---

# Chapter 4 ~ 9 전체 연결

```text
Redis
→ 빠른 공유 상태 / Cache / Rate Limit

PostgreSQL
→ 영구 데이터 / Transaction / HA / Backup

Kafka
→ Event Streaming Cluster 운영

vLLM
→ GPU 기반 LLM Inference

LiteLLM
→ LLM Gateway / Routing / Quota / Retry

GPU Infrastructure
→ 실제 Compute / Memory / Scheduling / HA
```

전체 Platform 구조:

```text
Application / User
        ↓
     LiteLLM
        ↓
      vLLM
        ↓
       GPU

Backend Services
├─ Redis
├─ PostgreSQL
└─ Kafka

Kubernetes
├─ Pod / Deployment / StatefulSet
├─ Scheduling
├─ Storage
├─ Networking
└─ GPU Scheduling
```

---

# 현재 전체 커리큘럼 상태

```text
1. Linux, Networking, Containers ✅
2. Kubernetes Core ✅
3. Kubernetes Production Operations ✅
4. Redis for Platform Systems ✅
5. PostgreSQL for Platform Systems ✅
6. Kafka for Platform Systems ✅
7. vLLM ✅
8. LiteLLM ✅
9. GPU Infrastructure & Scheduling ✅
10. Platform Security ← 다음
11. CI/CD, Helm, Argo CD & GitOps
12. Terraform & Infrastructure as Code
13. Multi-tenancy, Quotas & Cost Control
14. Internal Developer Platform / Self-Service
15. End-to-End AI Platform Architecture
```

> 다음 학습은 **Chapter 10. Platform Security**부터 이어진다.
