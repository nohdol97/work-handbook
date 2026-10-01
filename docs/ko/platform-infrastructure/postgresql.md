---
id: platform-infrastructure-postgresql
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
knowledge_ids:
  - PIS2-05-01
  - PIS2-05-02
  - PIS2-05-03
  - PIS2-05-04
  - PIS2-05-05
  - PIS2-05-06
  - PIS2-05-07
  - PIS2-05-08
---

# Chapter 5. PostgreSQL for Platform Systems

원문의 순서와 형태를 보존한 개념 학습 기록이다. 예시 수치·명령·식별자는 설명용이며 실행·운영 검증 결과가 아니다. 원문의 단순화와 주의할 적용 조건은 본문 뒤 보완 설명에서 해당 절 번호로 확인한다.

<!-- SOURCE CORE START -->

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

<!-- SOURCE CORE END -->

## 보완 설명과 적용 조건

공식 문서 확인일: 2026-10-01. PostgreSQL 링크는 확인 당시 current인 18 문서를 기준으로 읽었다. 설치된 버전의 동작이나 아래 SQL·복구 절차를 실행 검증했다는 뜻은 아니다.

### 5.1 WAL의 정확한 순서

WAL의 핵심 보장은 데이터 파일의 변경 페이지를 영구 저장하기 전에 해당 WAL 기록이 영구 저장되어야 한다는 것이다. 원문의 흐름은 개념도이며 메모리의 모든 변경보다 WAL 디스크 쓰기가 먼저라는 뜻은 아니다. [PostgreSQL WAL](https://www.postgresql.org/docs/18/wal-intro.html).

### 5.2 Connection pool의 범위

`1,000 → 100`은 설명용 구성이다. Pooler가 처리 용량을 자동으로 열 배 늘리지는 않는다. PgBouncer의 transaction pooling은 transaction 동안만 서버 connection을 할당하고 이후 반환한다. Session에 의존하는 기능과의 호환성이 session pooling과 다르므로 드라이버·실제 사용 기능을 확인한다. [PgBouncer features](https://www.pgbouncer.org/features.html).

### 5.3 Vacuum과 5.4 실행 계획

일반 `VACUUM`은 다시 쓸 수 있는 공간을 확보하지만 보통 파일을 줄여 OS에 반환하지는 않는다. 아직 다른 transaction에서 볼 수 있는 row version을 임의로 지울 수도 없다. 긴 transaction과 autovacuum 상태를 함께 확인한다. [PostgreSQL routine vacuuming](https://www.postgresql.org/docs/18/routine-vacuuming.html).

`EXPLAIN ANALYZE`는 대상 문장을 실제 실행한다. SELECT도 부하나 함수 부작용을 일으킬 수 있으므로 실행 환경과 문장을 먼저 확인한다. `EXPLAIN`의 추정 계획과 실행 통계를 구분한다. [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html).

### 5.5 Synchronous의 대기 지점

Standby 확인은 설정에 따라 다르다. `synchronous_standby_names`와 `synchronous_commit`을 함께 확인한다. `on`은 지정된 synchronous standby의 WAL durable flush를 기다리고, `remote_apply`는 replay되어 query에서 보이는 시점까지 기다린다. `remote_write`는 같은 내구성 보장이 아니다. 동기 standby가 응답하지 않으면 commit 대기가 길어질 수 있다. [PostgreSQL synchronous_commit](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT).

### 5.6 PITR의 전제

PITR에는 올바른 base backup과 복구 시점까지 이어지는 WAL이 필요하다. `pg_dump` 결과에 WAL을 붙이는 방식은 physical PITR이 아니다. 원문의 10:44 복구는 필요한 backup·WAL·timeline을 보유한 경우의 설명용 목표다. 복구 결과는 별도 환경에서 실제 확인해야 한다. [PostgreSQL continuous archiving](https://www.postgresql.org/docs/18/continuous-archiving.html).

### 5.7 work_mem의 총량

`work_mem`은 connection이나 query 전체의 고정 상한이 아니라 sort·hash 같은 개별 연산의 기준이다. 한 query에 여러 연산이 있고 동시에 여러 session이 실행될 수 있다. Hash 연산에는 `hash_mem_multiplier`도 관여한다. 따라서 `connection 수 × work_mem`만으로 전체 메모리 상한을 계산하지 않는다. [PostgreSQL resource consumption](https://www.postgresql.org/docs/18/runtime-config-resource.html).

### 5.8 StatefulSet과 Operator

`postgres-0 → Primary`는 예시이며 ordinal 자체가 PostgreSQL primary 역할을 보장하지 않는다. Failover 후 역할은 바뀔 수 있다. StatefulSet은 안정적인 식별자·저장소 연결을 제공하고, DB 역할·복구 로직은 별도로 구성한다. [Kubernetes StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

Operator는 custom resource와 controller를 통해 운영 로직을 구현하는 패턴이다. 원문의 설치 순서는 개념도다. CRD 등록과 controller 설치의 실제 순서·지원 PostgreSQL 버전·backup 기능은 선택한 Operator의 설치 문서를 따른다. [Kubernetes Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## LLM in Practice: Connection 증가와 DB 지연 검토

- **상황:** Pod 확장 뒤 DB 지연이 늘었고 원인이 확정되지 않았다.
- **제공 맥락:** Pod·pool 수, active/idle connection, query plan, lock·메모리·autovacuum 관측.
- **예시 prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Pod 수·pool 크기·활성 connection·대기 시간: [비식별 관측]
    추정 query plan·lock 대기·메모리·autovacuum 상태: [자료]
    [요청]
    Connection 상한과 실제 동시성을 구분하고 병목 가설을 검토하세요.
    [출력]
    관측, 가정, 누락 근거와 다음 읽기 전용 확인을 표로 작성하세요.
    [검증]
    max_connections 증가나 Redis 도입을 근거 없이 결론 내리지 마세요.
    EXPLAIN ANALYZE·설정 변경·SQL 실행 없이 검토안만 작성하세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Pod count, pool sizes, active connections, and wait times: [sanitized observations]
    Estimated query plans, lock waits, memory, and autovacuum state: [material]
    [Task]
    Distinguish connection limits from actual concurrency and review bottleneck hypotheses.
    [Output]
    Make a table of observations, assumptions, missing evidence, and next read-only checks.
    [Checks]
    Do not recommend raising max_connections or adding Redis without evidence.
    Draft a review without EXPLAIN ANALYZE, configuration changes, or SQL execution.
    ```

- **기대 결과:** Connection 한도와 실제 부하를 구분한 가설 및 추가 확인 표.
- **오류 가능성:** Connection 수만으로 원인을 확정하거나 EXPLAIN ANALYZE를 읽기 전용 계획 조회로 오해할 수 있다.
- **검증:** 원본 관측·설정을 사람이 대조하고 실행이 필요한 검증은 별도 격리 환경에서 검토 후 수행한다. 이 문서에서 SQL을 실행하지 않았다.

[Redis](redis.md) · [PostgreSQL](postgresql.md) · [Kubernetes 운영](kubernetes-operations.md)
