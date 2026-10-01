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

This conceptual study record preserves the source order and form. Example numbers, commands, and identifiers are teaching material, not results of execution or operational testing. Read the section-specific supplement after the source core for clarifications and conditions on simplified statements.

<!-- SOURCE CORE START -->

## 4.1 Redis Fundamentals

Redis is a key-value store that keeps data in memory for very fast reads and writes.

### Key-value structure

```text
key → value
```

Example:

```text
"user:1001:name" → "Alice"
"session:abc123" → user session information
```

Redis finds data quickly by key.

### In-Memory Database

Redis stores data mainly in RAM.

```text
Application
↓
Redis
↓
RAM
```

RAM is fast, but expensive and limited in capacity. Redis is therefore often used as a secondary store for data that needs fast access, rather than fully replacing a primary store such as PostgreSQL.

### Common data structures

```text
String
Hash
List
Set
Sorted Set
```

- String: the simplest value
- Hash: stores multiple fields like one object
- List: an ordered collection of values
- Set: a collection of unique values
- Sorted Set: supports ordering by score

### TTL

TTL = Time To Live.

```text
session:abc123
TTL = 30 minutes
```

The data is automatically deleted when its TTL expires.

Main uses:

```text
Session
Cache
Temporary token
Rate limit
```

### Why Redis is fast

```text
1. Storage in RAM
2. Simple access by key
```

### Redis vs PostgreSQL

```text
PostgreSQL
→ Primary store for durable data

Redis
→ Temporary or secondary data that needs fast access
```

Example:

```text
User accounts → PostgreSQL
User sessions → Redis
Original product information → PostgreSQL
Product information cache → Redis
```

---

## 4.2 Platform Use Cases

Main platform uses for Redis:

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
Check Redis
├─ HIT → Return immediately
└─ MISS → Query DB → Store in Redis
```

Keep frequently read data in Redis for a short time to reduce database load and response time.

### Session

```text
session:abc123
→ user_id=1001
```

Multiple API Pods can share session state by using the same Redis store.

```text
API Pod A ─┐
API Pod B ─┼→ Redis Session
API Pod C ─┘
```

### What "multiple servers" means here

In this study session, multiple servers usually means running the same service as multiple application instances, Pods, or processes.

```text
Deployment
 replicas: 3

Pod A ─┐
Pod B ─┼→ Redis
Pod C ─┘
```

Each user request may go to a different Pod.

```text
Request 1 → Pod A
Request 2 → Pod C
Request 3 → Pod B
```

If each Pod stores sessions only in its own memory, the next request may not find the state when it reaches another Pod. Redis serves as a shared state store.

### Rate Limiting

Example:

```text
user:1001:requests = 37
```

For a limit of 100 requests per minute:

```text
Request
↓
Increment Redis counter
↓
100 or fewer → Allow
More than 100 → Reject
```

### Distributed Counter

```text
API Pod A ─┐
API Pod B ─┼→ request_count = 10025
API Pod C ─┘
```

Example:

```text
Today's API call count
Concurrent user count
usage count
```

### Distributed Lock

Prevents multiple servers from doing the same job at the same time.

```text
Pod A
↓
Acquire lock
↓
Perform work

Pod B
↓
Lock already exists
↓
Wait or fail
```

### Request Deduplication

Process a request only once even if it arrives multiple times.

```text
payment-123 does not exist
→ Process
→ Record in Redis

Same request arrives again
→ Already exists
→ Do not process again
```

### When to introduce Redis

The most common reasons:

```text
1. PostgreSQL load grows because it repeatedly reads the same data
2. Some data needs faster responses without reaching the database
```

Traffic patterns and bottleneck locations matter more than user count.

Signals to consider Redis:

```text
Repeated reads of the same data
Higher PostgreSQL CPU / I/O
More DB connections
Higher read query latency
Low latency requirements
Need for TTL / sessions / rate limits
```

These ranges give a rough sense of scale, but are not absolute rules.

```text
Tens to hundreds of req/s
→ PostgreSQL alone is often enough

Hundreds to thousands of req/s
→ Redis may help more when many reads repeat

Thousands to tens of thousands or more req/s
→ A cache layer is common, but still not mandatory
```

Example:

```text
5,000 req/s
Cache Hit = 95%

→ About 250 req/s reach PostgreSQL
```

### Redis adds costs as well as performance

Added complexity:

```text
Cache invalidation
TTL configuration
Redis failures
Memory management
Hot Key
Data inconsistency between Redis and PostgreSQL
```

If PostgreSQL can handle the load, first optimize:

```text
Index
Query
Connection Pool
```

Then consider Redis.

---

## 4.3 Persistence

Redis is RAM-based, so data may be lost on restart.

Key points:

```text
RDB
AOF
```

### RDB

Saves a snapshot of Redis state at a specific point in time.

```text
Save state at 10:00
↓
dump.rdb
```

Advantages:
- Relatively small file
- Fast recovery
- Useful for backups

Disadvantages:
- Data written after the last snapshot may be lost

### AOF

Append Only File.

Continuously records write commands.

```text
SET user:1 Alice
INCR request_count
DEL session:123
```

Replays commands on restart to restore state.

### RDB vs AOF

```text
RDB
→ Snapshot at a specific point in time
→ Fast and simple
→ Some recent data may be lost

AOF
→ Continuously records write commands
→ Useful for reducing data loss
→ Greater file size / disk I/O burden
```

### Persistence may matter less for a cache

```text
Redis cache is lost
↓
Read again from PostgreSQL
↓
Rebuild cache
```

Key question:

> Can the Redis data be rebuilt if it is lost?

---

## 4.4 Replication

Redis replication copies data from a primary to replicas.

```text
        Primary
       /       \
  Replica A   Replica B
```

Usually:

```text
Write → Primary
Read  → Primary or Replica
```

Main purposes:

```text
1. Prepare for primary failure
2. Distribute read load
```

Redis replication is generally asynchronous.

```text
Client Write
↓
Apply on primary
↓
Respond to client
↓
Replicate to replica
```

### Replication Lag

```text
Primary     = 101
Replica     = 100
```

A replica may lag behind the primary.

Important:

```text
Replication
≠
Automatic Failover
```

---

## 4.5 Redis Sentinel

Sentinel provides Redis HA and automatic failover.

Main roles:

```text
Monitoring
Failover
Provide primary information
```

### Failover

```text
Primary ❌
 ├─ Replica A
 └─ Replica B

↓

Replica A → New primary
```

Multiple Sentinel instances can assess failures together.

```text
Sentinel 1
Sentinel 2
Sentinel 3
     ↓
Redis Primary / Replica
```

An application can discover the current primary through Sentinel.

```text
Application
↓
Sentinel
↓
Discover current primary
↓
Connect to new primary
```

### Sentinel vs Redis Cluster

```text
Sentinel
→ Focus on HA / failover

Redis Cluster
→ Sharding + HA
```

---

## 4.6 Redis Cluster

Redis Cluster distributes data across multiple Redis nodes and handles failures.

Key points:

```text
Sharding + Replication + Failover
```

### Sharding

```text
Redis A → Part of the data
Redis B → Part of the data
Redis C → Part of the data
```

### Hash Slot

```text
Key
↓
hash
↓
Hash Slot
↓
Responsible Redis node
```

### Resharding

Moves data by slot when nodes are added or removed.

### Cluster HA

```text
Primary A → Replica A
Primary B → Replica B
Primary C → Replica C
```

### Sentinel vs Cluster

```text
Sentinel
= Focus on HA

Redis Cluster
= Scale-out + HA
```

Common reasons to need a cluster:

```text
Data exceeds one node's memory
Traffic exceeds one node's throughput
Horizontal scaling is needed
```

---

## 4.7 Performance

Key points:

```text
Hot Key
Big Key
Memory / Eviction
Memory Fragmentation
Pipelining
```

### Hot Key

Requests concentrate on one key.

```text
Many clients
↓
One key
↓
Load concentrates on one Redis node
```

Even in Redis Cluster, one specific node owns that key.

### Big Key

One key contains too much data.

Problems:

```text
Higher CPU usage
More network transfer
Slower responses
```

### Eviction

Decides which keys to remove when memory is full.

### Memory Fragmentation

Memory allocated by the OS may exceed the actual data size.

### Pipelining

Sends commands in batches to reduce network round trips.

```text
SET A
SET B
SET C
↓
Send together
```

Operational checks:

```text
Redis is slow
→ Hot Key?
→ Big Key?
→ Not enough memory?
→ Too many network round trips?
```

---

## 4.8 Redis on Kubernetes

Redis is treated as a stateful workload.

Key points:

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

Provides stable identity.

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

### Separate Kubernetes and Redis HA responsibilities

```text
Kubernetes
= Pod dies → Create a new Pod

Redis Sentinel / Cluster
= Detect primary failure / Failover / Restore data roles
```

### Backup

Persistence and backup are separate concerns.

```text
RDB / AOF
↓
Separate backup
↓
External storage
```

### Operator

A Kubernetes controller can automate Redis Cluster creation, failover, scaling, and other tasks.

---

<!-- SOURCE CORE END -->

## Supplement and conditions

Official documentation checked: 2026-10-01. These notes are separate from the unchanged source. They do not record a Redis installation, load test, failover, or restore test.

### 4.1 What TTL means

Expired keys are removed on access and by periodic expiry checks. TTL marks when the application should no longer treat the data as valid. It does not mean all memory is reclaimed at that exact instant. [Redis EXPIRE](https://redis.io/docs/latest/commands/expire/).

### 4.2 Atomicity for rate limits, locks, and deduplication

A per-minute counter needs a time window and an expiry policy. An interruption between separate `INCR` and `EXPIRE` requests can leave a key without expiry. Check the atomicity conditions in the official pattern. [Redis INCR](https://redis.io/docs/latest/commands/incr/).

The source's `absent → process → record` flow alone cannot guarantee one execution. Two requests may both observe absence, or processing may finish before a crash prevents recording. This is a design limitation inferred from the source flow. For external effects such as payments, design durable idempotency records in the destination store together with the processing result. A Redis marker alone is not a complete exactly-once guarantee.

Review atomic acquisition, expiry, owner identifiers, and release that checks ownership together. If work exceeds the TTL, another client may acquire the lock. Failover with asynchronous replication can also break mutual exclusion. The official lock documentation explains these conditions and why a plain `DEL` may remove another owner's lock. [Redis distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/).

`5,000 × (1 − 0.95) = 250 req/s` is a teaching calculation. It assumes one DB request per miss and no other DB traffic. It is not an adoption threshold or measured performance. Also assess the DB load from concurrent misses while rebuilding the cache.

### 4.3 Persistence and possible data loss

Enabling AOF does not eliminate all data loss. Check the `appendfsync` policy and storage conditions. With `everysec`, a failure can lose about one second of writes. Since Redis 7.0, AOF uses base and incremental files plus a manifest, so backups must preserve a consistent file set. RDB and AOF still need separate backup storage and restore checks. [Redis persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/).

### 4.4–4.6 Conditions for HA and Cluster

Sentinel's failure-detection quorum differs from the Sentinel majority needed to authorize failover. Place Sentinels in independent failure domains and check client discovery and reconnection to the new primary. Sentinel cannot fully prevent the loss of acknowledged writes with asynchronous replication. [Redis Sentinel](https://redis.io/docs/latest/operate/oss_and_stack/management/sentinel/).

Redis Cluster uses 16,384 hash slots. Multi-key operations have same-slot requirements, so check key design and Cluster support in the client. Adding nodes does not automatically split one hot key. Cluster can also lose writes depending on failure timing and replication state. [Redis Cluster specification](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/).

### 4.7–4.8 Memory and Kubernetes responsibilities

Do not infer a memory leak from fragmentation metrics alone. Compare data size, memory retained by the allocator, and usage reported by the OS. [Redis memory optimization](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/).

StatefulSet provides stable Pod identities and storage associations. It does not automatically configure Redis role election, replication, or backups. A PVC alone does not guarantee backup or full disaster recovery. [Kubernetes StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).

## LLM in Practice: review Redis latency causes

- **Situation:** Redis has become slow, but the cause is unknown.
- **Context to give:** Sanitized latency, hit/miss, key distribution, memory, DB load, and observation windows.
- **Example prompt:**

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

- **Expected output:** Evidence and missing information for each hypothesis, plus further read-only checks.
- **What can go wrong:** The LLM may assume that adding Cluster nodes fixes a hot key or that every cache miss means a DB bottleneck.
- **How to validate:** Compare the original metrics, traces, and configuration. Run any needed reproduction separately in an isolated environment. No reproduction test was run for this page.

[Redis](redis.md) · [PostgreSQL](postgresql.md) · [Kubernetes operations](kubernetes-operations.md)
