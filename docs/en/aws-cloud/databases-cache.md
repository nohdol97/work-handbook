---
id: aws-cloud-databases-cache
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-05-01
  - AWS-05-02
  - AWS-05-03
---

# Chapter 5. Database / Cache

This page preserves Chapter 5 in the same order, with all paragraphs, tables, and examples. Read the **Supplement and conditions** after the source for Multi-AZ deployment types in 5.1, Aurora endpoints and Serverless in 5.2, and engine-specific replication and session conditions in 5.3. This is Basic conceptual study, not a record of creating AWS resources, testing failover, or measuring performance.

<!-- SOURCE CORE START -->

## 5.1 RDS

RDS = **Relational Database Service**

> A managed relational database service where AWS handles many operational tasks

Example:

```text
Application
   ↓
RDS PostgreSQL
```

### Common DB engines

- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server

RDS is not itself a DB engine. It is a service that provides several DB engines in managed form.

### EC2 PostgreSQL vs RDS

Self-managed:

```text
EC2
 ↓
PostgreSQL
```

You manage:

- OS
- PostgreSQL installation
- Disk
- Backup
- Patch
- Monitoring
- Failover
- Replication

RDS:

```text
Application
 ↓
RDS PostgreSQL
```

AWS handles many infrastructure operations.

Users mainly focus on:

- Schema
- Query
- Index
- Application Connection
- DB Parameter

These are the main areas of responsibility.

### RDS usually runs in private subnets

```text
VPC
│
├─ Public Subnet
│   └─ ALB
│
└─ Private Subnet
    ├─ Application
    └─ RDS
```

### DB Subnet Group

A list of subnets that defines the subnets and AZs where RDS can be placed.

```text
DB Subnet Group
├─ Private Subnet A
├─ Private Subnet B
└─ Private Subnet C
```

### Security Group

PostgreSQL:

```text
TCP 5432
Source: APP-SG
```

### RDS Endpoint

The application uses an endpoint instead of a database IP address.

```text
mydb.xxxxxx.ap-northeast-2.rds.amazonaws.com
```

The endpoint provides access even when failover or infrastructure changes replace the actual DB instance.

### Multi-AZ

```text
AZ A
└─ Primary RDS

AZ B
└─ Standby RDS
```

If the primary fails, the standby takes over.

Purpose:

```text
Multi-AZ
= High Availability
```

### Read Replica

```text
             Primary
             /     \
      Replica A   Replica B
```

- Write → Primary
- Read → Replica

Purpose:

```text
Read Replica
= Read Scaling
```

### Multi-AZ vs Read Replica

```text
Multi-AZ
→ Failure recovery

Read Replica
→ Distribute read load
```

### Backup / Snapshot

- Automated Backup
- Point-in-Time Recovery
- Manual Snapshot

### Storage

Users configure storage size, type, IOPS, and other settings. They do not attach or detach EBS volumes directly.

### Scaling

Vertical scaling by changing the instance class.

Read scaling through read replicas.

### Connection problems

As the number of Pods grows, the number of database connections also grows.

Example:

```text
Pod 100
×
Connection 20
=
2,000 DB Connections
```

Connection pool management is important.

Consider RDS Proxy when needed.

### EKS + RDS

```text
Internet
 ↓
ALB
 ↓
EKS
├─ Pod
├─ Pod
└─ Pod
   ↓
RDS PostgreSQL
```

Keep the application stateless and store persistent transactional data in RDS.

### Running PostgreSQL yourself on EKS vs RDS

When you run it yourself:

- StatefulSet
- PVC
- EBS
- Replication
- Backup
- Failover
- Upgrade
- Operator

You must operate these components yourself.

RDS can greatly reduce the operational burden.

However, even with RDS, you still need to manage the following.

- Slow Query
- Index
- Schema
- Connection Pool
- Transaction
- Lock
- Vacuum
- Capacity Planning

---

## 5.2 Aurora

Aurora is a **relational database engine built by AWS for the cloud**.

Relationship to RDS:

```text
Amazon RDS
├─ PostgreSQL
├─ MySQL
├─ MariaDB
├─ Oracle
├─ SQL Server
└─ Aurora
```

In other words:

> RDS = Managed database service  
> Aurora = One of the DB engines available through RDS

### PostgreSQL / MySQL Compatible

- Aurora PostgreSQL-Compatible
- Aurora MySQL-Compatible

AWS built the engine, but it provides PostgreSQL/MySQL-compatible interfaces.

### Separating compute and storage

Standard RDS PostgreSQL:

```text
DB Instance
   ↓
Storage
```

Aurora:

```text
         Shared Aurora Storage
          ↑       ↑       ↑
        DB 1    DB 2    DB 3
```

Core design:

> Multiple DB instances use a shared distributed storage layer

### Writer / Reader

```text
              Aurora Cluster
                   │
          ┌────────┴────────┐
          │                 │
       Writer            Readers
          │              /     \
          │          Reader1  Reader2
          │
          └──── Shared Storage ────
```

- Writer = INSERT / UPDATE / DELETE
- Reader = SELECT / Read Scaling

### Endpoint

Cluster Endpoint:

```text
Application Write
      ↓
Cluster Endpoint
      ↓
Writer
```

Reader Endpoint:

```text
Application Read
      ↓
Reader Endpoint
     /      \
Reader1    Reader2
```

### Failover

If the writer fails, one of the readers can be promoted to become the new writer.

The application continues to use the cluster endpoint.

### Multi-AZ

Aurora storage uses a distributed design built with Multi-AZ high availability in mind.

### Automatic storage growth

Storage capacity grows automatically as data increases.

### Aurora Serverless

It reduces the burden of managing a fixed DB instance size and adjusts compute capacity to demand.

```text
Provisioned
= Choose the server size yourself

Serverless
= Operate compute elastically
```

### Aurora is not always the better choice

Factors to consider:

- Cost
- Feature differences
- PostgreSQL version / Extension compatibility
- AWS dependence
- Operational complexity

RDS PostgreSQL may be enough for a small, simple service.

Consider Aurora PostgreSQL as scale grows and HA or read scaling becomes important.

### Connection pool problems

Aurora still requires database connection management.

```text
Application
 ↓
Connection Pool
 ↓
RDS Proxy (if needed)
 ↓
Aurora
```

### RDS PostgreSQL vs Aurora PostgreSQL

| Item | RDS PostgreSQL | Aurora PostgreSQL |
|---|---|---|
| DB engine | PostgreSQL | AWS-built PostgreSQL-compatible engine |
| Storage structure | Instance-centered managed storage | Shared distributed storage |
| HA | Multi-AZ | Designed around Multi-AZ |
| Read Scaling | Read Replica | Aurora Reader |
| Failover | Supported | Based on the cluster structure |
| Storage growth | Requires some management | More automated |
| Cost/structure | Relatively simple | Can be more complex or expensive |

---

## 5.3 ElastiCache

ElastiCache:

> A managed in-memory cache service operated by AWS

You can run a Redis-family cache as an AWS-managed service.

### Why use a cache?

Sending every request to RDS increases database load.

```text
Application
   ↓
ElastiCache
   ↓ Cache Miss
RDS
```

### Cache Aside

Read flow:

```text
Application
    ↓
ElastiCache
    ↓
Key exists?
```

Cache Hit:
- Return directly from Redis

Cache Miss:
1. Read from RDS
2. Store in Redis
3. Return to the user

### It does not replace RDS

```text
RDS
= Source of Truth

ElastiCache
= Fast temporary data / Cache
```

### Common uses

- Cache
- Session
- Rate Limit
- Counter
- Leaderboard
- Temporary State

### Running Redis yourself vs ElastiCache

Self-managed Redis:

```text
EKS
└─ Redis StatefulSet
   ├─ PVC
   ├─ Replication
   ├─ Failover
   ├─ Backup
   └─ Upgrade
```

ElastiCache:

```text
Application
   ↓
Managed Cache
```

Similar approach:

```text
Self-managed PostgreSQL → RDS
Self-managed Redis      → ElastiCache
```

### Private Network

It usually runs on a private VPC network.

```text
VPC
│
├─ Public Subnet
│   └─ ALB
└─ Private Subnet
    ├─ EKS
    ├─ RDS
    └─ ElastiCache
```

### Security Group

Redis-compatible services generally use port `6379`.

```text
CACHE-SG
Inbound
6379 ← APP-SG
```

### Primary / Replica

```text
Primary
   ↓ Replication
Replica
```

Used for high availability and read scaling.

### Multi-AZ

```text
AZ A
└─ Primary

AZ B
└─ Replica
```

If the primary fails, a replica can be promoted.

### Sharding

Split data across multiple shards when it cannot all fit in one node's memory.

```text
Cluster
├─ Shard 1
│  ├─ Primary
│  └─ Replica
└─ Shard 2
   ├─ Primary
   └─ Replica
```

### Replica vs Shard

```text
Replica
= Replicate the same data
= HA / Read Scaling

Shard
= Partition data
= Capacity / Write Scaling
```

### TTL

```text
user:123
TTL = 600 seconds
```

Useful for sessions, caches, tokens, and rate limits.

### Cache Invalidation

The database value may change while the cache keeps the old value, resulting in stale data.

Therefore:

```text
DB Update
 ↓
Cache Delete / Update
```

Or use a TTL.

### Session storage

Storing sessions in Pod-local memory can cause problems when there are multiple Pods.

```text
        ElastiCache
        /    |    \
     Pod A Pod B Pod C
```

Moving sessions to an external store lets the application remain stateless.

### Connection to auto scaling

```text
Application
= Stateless

Session / Cache
= ElastiCache

Persistent Data
= RDS

Object
= S3
```

### RDS vs ElastiCache

| Item | RDS | ElastiCache |
|---|---|---|
| Storage location | Mainly disk | Mainly memory |
| Data | Persistent data | Temporary/cached data |
| Speed | Relatively slow | Very fast |
| Common uses | Users/orders/settings | Cache/session |
| Source of truth | Usually yes | Usually no |

### Must you always add Redis?

No.

You can leave Redis out if RDS alone is enough for an early-stage service.

Adding Redis introduces the following complexity.

- Cache Policy
- TTL
- Invalidation
- Memory management
- Failover

It is therefore better to consider it when there is actual database load or a latency problem.

---

<!-- SOURCE CORE END -->

## Supplement and conditions

Official documentation checked: 2026-10-03. These corrections and conditions are separate from the source. They are not results from running deployment or failover commands.

### 5.1 RDS engines and Multi-AZ deployment types

The source engine list gives examples. Current RDS documentation also includes Db2. Check feature support by engine, version, and Region. [RDS DB instances](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.html).

The source Primary/Standby diagram describes a **Multi-AZ DB instance deployment**. Its standby does not serve reads. A **Multi-AZ DB cluster deployment** has a writer and two standbys that can serve reads. Do not apply the source distinction between Multi-AZ for HA and read replicas for scaling to every deployment type. [RDS Multi-AZ types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html).

Keeping an endpoint does not guarantee uninterrupted connections or transactions. After failover, clients must resolve the changed DNS record and reconnect. Design retries with transaction-result checks and duplicate prevention. [RDS Multi-AZ failover](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.Failover.html).

`100 × 20 = 2,000` assumes that each Pod holds 20 connections. Check actual concurrent connections, pool limits, idle connections, and database limits. Adding RDS Proxy does not create unlimited database processing capacity.

### 5.2 Aurora endpoints, failover, and Serverless

The reader endpoint balances **connections**. It does not spread the individual queries of one connection across readers. With no readers, it connects to the writer. The source Writer/Reader split describes roles; the writer can also serve reads. [Aurora reader endpoints](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Endpoints.Reader.html).

If the writer fails, Aurora can promote an existing replica or create a new primary. Clients must reconnect through the cluster endpoint; existing connections are not preserved automatically. During failover, the reader endpoint can briefly connect to the new writer. [Aurora endpoints and HA](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.Endpoints.html).

Serverless still requires checking capacity ranges and supported engines, Regions, and features. It does not mean unlimited capacity or guaranteed lower cost. [Aurora Serverless](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html). Automatic pause at 0 ACUs requires supported engine versions and settings. A connection can face a delay while the instance resumes. [Automatic pause and resume](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html).

### 5.3 ElastiCache engines, replication, and sharding

ElastiCache supports Valkey, Redis OSS, and Memcached through node-based and Serverless options. The source primary/replica/shard explanation mainly describes node-based Valkey and Redis OSS configurations. [ElastiCache overview](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html).

Node-based Memcached does not have the same replica-based HA or automatic failover. Valkey and Redis OSS use one shard with cluster mode disabled and can partition across several shards with cluster mode enabled. Do not assume Serverless has the same internal layout as the node-based diagram. [Engine comparison](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/SelectEngine.html).

Standard asynchronous replication can lose recent writes during failover. Check Multi-AZ, replica placement, and automatic failover conditions. Some Valkey configurations offer a separate durability feature. Do not generalize that every ElastiCache deployment stores only temporary data without durability. Check recovery guarantees against the engine, version, durability setting, and write mode. [Replication and durability](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.html), [Multi-AZ failover](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/AutoFailover.html).

### 5.3 TTL, sessions, and cache adoption

The source TTL of `600 seconds` is an example, not a guarantee of immediate consistency. Cache-aside can return stale values before expiry. Database updates and cache invalidation are separate operations, so also review failures and races. [AWS caching strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html).

External sessions can be shared independently of Pod replacement, but they are not necessarily permanent. Define behavior for expiry, eviction under memory policies, replication loss, login again, and revocation. These are operational conditions to check for the source session design. Distinguish rebuilding ordinary cached data from the user impact of losing sessions. The source claim that caching is much faster than RDS does not replace workload-specific measurements. Compare cache hits and misses, database load, and added network latency with actual requirements.

[PostgreSQL operations](../platform-infrastructure/postgresql.md) · [Redis operations](../platform-infrastructure/redis.md)

## LLM in Practice: review growing DB connections and a cache proposal

- **Situation:** Database connections grew after Pod scaling, and someone proposed adding Redis.
- **Context to give:** Sanitized Pod and pool counts, database engine and deployment type, connection and query metrics, session needs, and acceptable stale-data duration.
- **Example prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Pod 수와 Pod별 pool 상한: [비식별 설정]
    RDS/Aurora 엔진·버전·배포 유형과 연결·query 지표: [자료]
    Cache 엔진·모드, session 손실 허용, stale 허용 시간: [확인값 또는 모름]
    [요청]
    연결 증가의 관측과 가정을 나누고 pool 조정·DB 검토·캐시 도입안을 평가하세요.
    [출력]
    100×20 예시와 실제 수치를 구분한 연결 예산, 가설별 근거와 다음 읽기 전용 확인을 작성하세요.
    [검증]
    Multi-AZ 유형별 읽기 기능, reader endpoint의 연결 분산, 캐시 손실 조건을 확인하세요.
    지연 지표 하나로 원인을 단정하거나 리소스 변경·장애조치를 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Pod count and pool limit per Pod: [sanitized settings]
    RDS/Aurora engine, version, deployment type, and connection/query metrics: [material]
    Cache engine and mode, acceptable session loss, and stale-data duration: [known values or unknown]
    [Task]
    Separate observations from assumptions about connection growth and assess pool changes, database review, and cache adoption.
    [Output]
    Provide a connection budget separating the 100×20 example from actual numbers, evidence for each hypothesis, and next read-only checks.
    [Checks]
    Check read support by Multi-AZ type, connection balancing at reader endpoints, and cache data-loss conditions.
    Do not infer a cause from one latency metric alone or execute resource changes or failover.
    ```

- **Expected output:** A connection budget, evidence and missing information for each hypothesis, and a comparison of cache benefits, consistency, and session-loss conditions.
- **What can go wrong:** The LLM may assume every Multi-AZ standby serves reads or that Redis automatically solves a connection surge.
- **How to validate:** Compare AWS documentation, actual pool and deployment settings, and metrics from the same time window. Run any needed experiment separately in an isolated environment within authorized scope. No experiment was run for this page.
