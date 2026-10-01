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

This conceptual study record preserves the source order and form. Example numbers, commands, and identifiers are teaching material, not results of execution or operational testing. Read the section-specific supplement after the source core for clarifications and conditions on simplified statements.

<!-- SOURCE CORE START -->

## 5.1 PostgreSQL Architecture

PostgreSQL is a relational database.

Core architecture from a platform perspective:

```text
Client
↓
PostgreSQL
↓
Memory + WAL + Disk
```

### Process Model

Each client connection uses a separate PostgreSQL process.

```text
Client A → Process A
Client B → Process B
Client C → Process C
```

As connections increase:

```text
More processes
↓
More memory
↓
More context switching
↓
Lower performance
```

### Shared Memory / Shared Buffers

Caches frequently used data in memory.

### WAL

WAL = Write-Ahead Log.

Records changes in WAL before writing them to the actual table.

```text
UPDATE
↓
Write WAL
↓
Process change
↓
Write to disk later
```

Uses:
- Crash recovery
- Replication
- PITR

---

## 5.2 Connection Management

Key points:

```text
max_connections
Connection Pool
PgBouncer
```

### Why connections can be a problem

Example:

```text
100 Pods
×
20 Connections
=
2,000 DB Connections
```

PostgreSQL connections use processes and memory, so too many add overhead.

### max_connections

The maximum number of simultaneous connections.

Simply raising it by a large amount is not always a good solution.

### Connection Pool

Reuses connections instead of creating one for every request.

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

### Why one Pod has multiple database connections

One Pod handles multiple user requests at the same time.

```text
Request 1 → DB query
Request 2 → DB query
Request 3 → DB query
```

With only one connection, database work may be serialized.

A pool of 10 connections can handle multiple database operations in parallel.

Important:

```text
50 Pods
×
Pool 20
=
Up to 1,000 connections
```

Calculate the Pod replica count and pool size together.

### PgBouncer

A lightweight connection pooler in front of PostgreSQL.

```text
Application Pods
↓
PgBouncer
↓
PostgreSQL
```

Example:

```text
Application connections 1000
↓
PgBouncer
↓
PostgreSQL connections 100
```

It is especially useful in Kubernetes and autoscaling environments.

---

## 5.3 Transactions / MVCC

Key points:

```text
Transaction
Isolation
MVCC
Vacuum
```

### Transaction

Groups multiple database operations into one logical unit.

```text
BEGIN
↓
Subtract from A
↓
Add to B
↓
COMMIT
```

ROLLBACK on failure.

### Isolation

Defines how much concurrent transactions can see of each other's work.

### MVCC

Multi-Version Concurrency Control.

> Keeps multiple data versions so reads and writes block each other less

```text
Reader
→ Reads an existing version

Writer
→ Creates a new version
```

### Vacuum

Cleans up old row versions.

```text
UPDATE / DELETE
↓
More old versions
↓
Vacuum
```

### Autovacuum

Runs vacuum automatically.

If it does not work properly, tables and indexes may grow and performance may fall.

### Lock

Concurrent transactions updating the same row may compete for locks.

```text
Read + Write
→ Relatively parallel processing

Write + Write
→ Lock contention is possible
```

---

## 5.4 Index / Query Performance

Key points:

```text
Index
B-tree
Query Planner
EXPLAIN
Slow Query
Lock
```

### Index

A structure for finding data quickly without searching the entire table.

### B-tree

The most basic index type.

```sql
CREATE INDEX idx_users_email
ON users(email);
```

Commonly used for `=`, `<`, `>`, range queries, sorting, and similar operations.

### Index Trade-off

```text
May improve read performance
Higher write cost
More disk space
```

### Query Planner

Chooses sequential scans, index scans, join methods, and other steps before executing SQL.

### EXPLAIN

```sql
EXPLAIN SELECT ...;
EXPLAIN ANALYZE SELECT ...;
```

### Causes of slow queries

```text
Missing index
Too many rows scanned
Inefficient joins
Too much data returned
Lock waits
```

### Basic tuning order

```text
1. Identify slow queries
2. EXPLAIN
3. Check for sequential scans
4. Check required indexes
5. Check the number of rows read
6. Check lock waits
```

Important principle:

> When the database is slow, check queries and indexes before adding Redis.

---

## 5.5 PostgreSQL HA

Key points:

```text
Primary
Standby
Streaming Replication
Synchronous / Asynchronous
Failover
```

### Streaming Replication

Sends WAL to the standby.

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
Apply on primary
↓
Respond to client
↓
Standby catches up
```

Fast, but recent data may be lost.

### Synchronous

```text
Client Write
↓
Primary
↓
Confirm the change on standby
↓
Respond to client
```

Improves data durability, but may increase write latency.

### Failover

```text
Primary ❌
↓
Standby
↓
New primary
```

### Read Replica

Can be used to distribute read load.

Asynchronous replication may return slightly stale data.

---

## 5.6 Backup / Recovery

Backups are still needed separately even with HA.

Example:

```text
Incorrect DELETE on primary
↓
Replication
↓
Deleted on standby too
```

Key points:

```text
Logical Backup
Physical Backup
WAL Archiving
PITR
```

### Logical Backup

Common tool: `pg_dump`

Backs up logical schemas, tables, and rows.

### Physical Backup

Backs up the actual PostgreSQL data files.

### WAL Archiving

```text
Primary
↓
Generate WAL
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
Replay to the desired point in time
```

Example:

```text
10:00 Backup
10:45 Table accidentally deleted
→ Recover to 10:44
```

### HA vs Backup

```text
Replication / HA
→ Prepare for server failures

Backup / PITR
→ Prepare for operational mistakes / data corruption
```

---

## 5.7 Operational Tuning

Key points:

```text
Connection
Memory
Autovacuum
Checkpoint
Disk I/O
```

### Memory

Common settings at the basic level:

```text
shared_buffers
work_mem
```

- shared_buffers: data cache
- work_mem: memory for query operations such as sorts and joins

A high work_mem setting may cause high total memory use when many queries run concurrently.

### Autovacuum

```text
UPDATE / DELETE
↓
More dead tuples
↓
Autovacuum
```

### Checkpoint

A recovery reference point for writing changed data from memory to disk.

```text
Checkpoint
→ Affects disk I/O and recovery
```

### Operational tuning order

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

PostgreSQL is a stateful workload.

Key points:

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

### Separate Kubernetes and PostgreSQL HA responsibilities

```text
Kubernetes
= Restore the Pod lifecycle

PostgreSQL HA
= Primary / Standby / Replication / Failover
```

### Operator

Automates PostgreSQL operations through a Kubernetes controller.

Example:

```text
Create primary
Create standby
Replication
Failover
Backup
Restore
Upgrade
```

### Must an Operator be installed before PostgreSQL on Kubernetes?

Not necessarily.

#### Set it up directly

```text
Kubernetes
↓
StatefulSet
↓
PostgreSQL
↓
PVC / PV
```

It is possible without an Operator.

However, you must manage the primary and standbys, replication, failover, backups, upgrades, and recovery yourself.

#### When using an Operator

```text
1. Prepare a Kubernetes cluster
2. Install the PostgreSQL Operator
3. Register the CRDs
4. Create a PostgreSQL Cluster custom resource
5. The Operator creates the actual PostgreSQL setup
```

When using an Operator, install the Operator first.

Think of an Operator as teaching Kubernetes how to operate PostgreSQL.

### Persistent Volume ≠ Backup

A PVC or PV also persists operational mistakes.

```text
DROP TABLE users;
```

Backups, WAL archives, and PITR are therefore separate concerns.

### Managed DB

In real platforms:

```text
Kubernetes Application
↓
Managed PostgreSQL
```

Example:

```text
EKS
↓
RDS PostgreSQL
```

This architecture is also very common.

---

<!-- SOURCE CORE END -->

## Supplement and conditions

Official documentation checked: 2026-10-01. The PostgreSQL references were read against version 18, which was current when checked. This does not claim runtime validation of an installed version, the SQL examples, or recovery procedures.

### 5.1 The precise WAL ordering

The key WAL guarantee is that the relevant WAL records must reach durable storage before changed pages are persisted in data files. The source flow is conceptual. It does not mean that a WAL disk write happens before every in-memory change. [PostgreSQL WAL](https://www.postgresql.org/docs/18/wal-intro.html).

### 5.2 What connection pooling covers

`1,000 → 100` is an example configuration. A pooler does not automatically multiply processing capacity by ten. PgBouncer transaction pooling assigns a server connection only for a transaction, then returns it to the pool. Compatibility with session-dependent features differs from session pooling. Check the driver and the features actually used. [PgBouncer features](https://www.pgbouncer.org/features.html).

### 5.3 Vacuum and 5.4 execution plans

Regular `VACUUM` makes space reusable, but usually does not shrink files and return space to the OS. It also cannot arbitrarily remove row versions that another transaction can still see. Check long transactions and autovacuum state together. [PostgreSQL routine vacuuming](https://www.postgresql.org/docs/18/routine-vacuuming.html).

`EXPLAIN ANALYZE` actually runs the target statement. Even SELECT can create load or function side effects, so review the statement and execution environment first. Distinguish an estimated `EXPLAIN` plan from runtime statistics. [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/18/sql-explain.html).

### 5.5 What synchronous commits wait for

Standby acknowledgment depends on configuration. Check `synchronous_standby_names` together with `synchronous_commit`. `on` waits for durable WAL flush on the selected synchronous standbys. `remote_apply` also waits for replay that makes the transaction visible to queries. `remote_write` does not provide the same durability guarantee. Commit waits may grow when a synchronous standby does not respond. [PostgreSQL synchronous_commit](https://www.postgresql.org/docs/18/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT).

### 5.6 Requirements for PITR

PITR needs a valid base backup and an unbroken WAL sequence through the recovery target. Adding WAL to a `pg_dump` result is not physical PITR. The source's 10:44 recovery is an example target that assumes the required backup, WAL, and timeline are available. Check the restored result in a separate environment. [PostgreSQL continuous archiving](https://www.postgresql.org/docs/18/continuous-archiving.html).

### 5.7 Total memory and work_mem

`work_mem` is a baseline for individual operations such as sorts and hashes, not a fixed limit for a whole connection or query. One query can contain multiple operations, and many sessions can run concurrently. Hash operations also use `hash_mem_multiplier`. Therefore, `connection count × work_mem` alone does not give the total memory ceiling. [PostgreSQL resource consumption](https://www.postgresql.org/docs/18/runtime-config-resource.html).

### 5.8 StatefulSet and Operators

`postgres-0 → Primary` is an example. The ordinal itself does not guarantee the PostgreSQL primary role, and roles can change after failover. StatefulSet provides stable identities and storage associations. Database roles and recovery logic need separate configuration. [Kubernetes StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

The Operator pattern implements operational logic through custom resources and a controller. The source installation sequence is conceptual. Follow the selected Operator's installation documentation for the actual CRD and controller installation order, supported PostgreSQL versions, and backup features. [Kubernetes Operator pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

## LLM in Practice: review connection growth and DB latency

- **Situation:** DB latency increased after scaling Pods, but the cause is not confirmed.
- **Context to give:** Pod and pool counts, active and idle connections, query plans, locks, memory, and autovacuum observations.
- **Example prompt:**

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

- **Expected output:** A table of hypotheses and further checks that separates connection limits from actual load.
- **What can go wrong:** The LLM may infer the cause from connection count alone or mistake EXPLAIN ANALYZE for a read-only plan lookup.
- **How to validate:** A person compares the original observations and configuration. Review checks requiring execution before running them in a separate isolated environment. No SQL was executed for this page.

[Redis](redis.md) · [PostgreSQL](postgresql.md) · [Kubernetes operations](kubernetes-operations.md)
