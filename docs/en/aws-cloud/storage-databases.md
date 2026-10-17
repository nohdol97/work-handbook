---
id: aws-cloud-storage-databases
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AWSC-04-01
  - AWSC-04-02
  - AWSC-04-03
  - AWSC-04-04
  - AWSC-04-05
  - AWSC-04-06
  - AWSC-04-07
  - AWSC-04-08
---

# Chapter 4. Storage & Database

The configurations are study examples, not results from a running AWS environment.

<!-- SOURCE CORE START -->

## 4.1 EBS

Choosing storage is like choosing a private locker, shared shelf, or transaction ledger. Writers, sharing needs, and recovery requirements determine the right service.

Block Storage.

Common uses:
- EC2 OS Disk
- Application Disk
- DB Disk
- EKS Persistent Volume

Features:
- Scoped to an AZ
- Snapshot support
- Consider IOPS / Throughput

```text
IOPS = Number of I/O operations per second
Throughput = Amount of data transferred per second
```

---

## 4.2 S3

S3 = Simple Storage Service.

> AWS Object Storage

```text
Bucket
└─ Object
```

An object is identified by its key.

Common uses:
- Dataset
- Model Artifact
- CSV / Parquet
- Logs
- Backup
- Image / Video
- Data Lake

### Versioning
Can preserve earlier versions of the same key.

### Lifecycle
Move older objects to another storage class or delete them.

### Bucket Policy
A resource-based policy applied to the bucket itself.

```text
IAM Policy = Permissions on the user / role side
Bucket Policy = Permissions on the bucket side
```

### Reasons to separate buckets
A bucket is a major management/security boundary.

- Access Policy
- Lifecycle
- Versioning / Replication
- Encryption
- Environment separation
- Cost/operations management

A prefix is a logical grouping within a bucket.

```text
Bucket = Major management / security boundary
Prefix = Logical grouping within a bucket
```

### S3 is not a file system
It is mainly accessed through APIs (GetObject / PutObject).

### VPC Endpoint
Can provide S3 access from a private subnet without NAT.


An S3 endpoint's existence does not grant access. Check gateway-endpoint route table associations alongside endpoint, IAM, and bucket policies. [S3 Gateway Endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)

---

## 4.3 EFS

EFS = Elastic File System.

> A shared file system that multiple EC2/EKS workloads can mount at the same time

Features:
- File Storage
- NFS-based
- Access by clients in multiple AZs
- Mount Target
- NFS default TCP 2049

Comparison:
```text
EBS = Block / server disk
EFS = Shared File
S3 = Object / API
```

Kubernetes:
```text
Dedicated persistent disk for a Pod → EBS
File system shared by multiple Pods → EFS
Dataset / Model / Object → S3
```


Access by clients in multiple AZs differs from Multi-AZ data storage. EFS Regional stores data across AZs. One Zone stores it in one AZ and is not resilient to that AZ's loss. A shared mount does not coordinate concurrent writes by itself; file locks are advisory. [EFS types and consistency](https://docs.aws.amazon.com/efs/latest/ug/features.html)

---

## 4.4 Multiple PostgreSQL Pods and EFS

Multiple PostgreSQL Pods must not share one EFS `PGDATA`.

Incorrect structure:
```text
        EFS
       /   \
Postgres A  Postgres B
```

Typical structure:
```text
Primary → PVC A → EBS A
Replica → PVC B → EBS B
```

Data is replicated through PostgreSQL replication.

```text
Primary
 ↓ WAL Replication
Replica
```

EFS is more suitable for shared files / dumps / exports than a live DB data directory. S3 is often considered for backups.


The warning concerns independent PostgreSQL servers modifying the same `PGDATA` concurrently. It does not ban all NFS use. PostgreSQL documents NFS requirements separately. Dedicated PVCs still need separate DB replication and failover configuration. [PostgreSQL file system requirements](https://www.postgresql.org/docs/current/creating-cluster.html), [PostgreSQL study](../platform-infrastructure/postgresql.md)

---

## 4.5 RDS

RDS = Relational Database Service.

> An AWS-managed relational database service

Supported examples:
- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server
- Aurora

RDS is not a single DB engine. It is a service providing several engines in managed form.

### Self-managed PostgreSQL vs RDS
RDS greatly reduces the burden of operating the OS, DB installation, backups, patches, failover, replication, and storage.

### DB Subnet Group
A set of private subnets where RDS can be placed.

### Security Group
Example:
```text
5432 ← APP-SG
```

### Endpoint
The application uses an endpoint instead of a DB IP address.

### Multi-AZ
```text
Multi-AZ = High Availability
```

### Read Replica
```text
Read Replica = Read Scaling
```

### Backup
- Automated Backup
- Point-in-Time Recovery
- Snapshot

### Connection Pool
As the Pod count grows, DB connections also increase, so connection pool management matters.
Consider RDS Proxy if needed.


A DB subnet group is a collection of subnets; it is not restricted to private ones. Read the source as a private-placement example. Also check public accessibility, routes, and security settings. [RDS VPC placement](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)

A Multi-AZ DB instance standby does not serve reads, while the two standbys in a Multi-AZ DB cluster do. Apply the HA/read-scaling distinction by deployment type. [RDS Multi-AZ types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)

---

## 4.6 Aurora

Aurora is a PostgreSQL/MySQL-compatible DB engine built by AWS.

Core idea:
```text
Writer ─┐
Reader ─┼→ Shared Distributed Storage
Reader ─┘
```

### Writer / Reader
```text
Writer = Write
Reader = Read Scaling
```

### Endpoint
```text
Cluster Endpoint → Writer
Reader Endpoint → Readers
```

### Failover
If the writer fails, a reader can be promoted to become the new writer.

### Aurora Serverless
A way to adjust DB compute capacity elastically with demand.

Aurora is not always the better choice.
Consider cost, AWS lock-in, PostgreSQL extension/version compatibility, and other factors.


The Aurora reader endpoint balances connections, not individual queries. Without readers it connects to the writer, which can also serve reads. [Aurora reader endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Endpoints.Reader.html)

---

## 4.7 ElastiCache

> AWS Managed In-Memory Cache

Common uses:
- Cache
- Session
- Rate Limit
- Counter
- Temporary State

### Cache Aside
```text
Application
 ↓
ElastiCache
 ↓ Cache Miss
RDS
```

### Roles alongside RDS
```text
RDS = Source of Truth
ElastiCache = Fast temporary / cached data
```

### Replica / Shard
```text
Replica = Replicate the same data
Shard = Partition data
```

### TTL / Invalidation
Caches can hold stale data, so TTL, delete, and update policies are needed.

Redis is not required in every system. Consider it when there is an actual DB load or latency problem.


The source roles describe a common cache model. Asynchronous Valkey/Redis OSS replication can lose recent writes, and some Valkey configurations offer separate durability. Check recovery conditions by engine, version, and settings. Do not infer immediate consistency from TTL alone. [ElastiCache replication conditions](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.html)

---

## Chapter 4 combined comparison

| Type | AWS service | Common uses |
|---|---|---|
| Block Storage | EBS | OS / DB Disk |
| File Storage | EFS | Shared File System |
| Object Storage | S3 | Dataset / Model / Backup |
| Relational DB | RDS / Aurora | Transactional Data |
| In-Memory Cache | ElastiCache | Cache / Session |

---

<!-- SOURCE CORE END -->

## Key points

Choose S3, block or file storage, databases, and caches according to data shape, sharing needs, and read patterns.

Read this with [Compute](compute.md) to connect storage choices with service placement.

## LLM in Practice

**Prompt:**

=== "한국어"

    ```text {.prompt}
    DB와 모델 파일 저장소를 바꾸는 설계안을 검토해 줘. PostgreSQL의 같은 PGDATA를 독립 서버가 동시에 쓰는 경우와 읽기 중심 모델 파일 공유를 구분하고, 저장 방식별 복구 조건을 설명해 줘. 실제 스토리지나 DB는 변경하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review a proposal to change database and model-file storage. Separate independent PostgreSQL servers writing one PGDATA from sharing mostly read-only model files, and explain recovery requirements for each option. Do not change storage or databases.
    ```

**Key point:** Writer/volume relationships for DB and model files, failure-domain and consistency risks, proposals, and a restore-check matrix for RPO/RTO. It may equate shared mounts with DB replication or assume One Zone survives an AZ failure because clients in multiple zones can read it. Check for independent writers to the same PGDATA and actual replication/backups. Require separate checks for EFS/DB deployment failure and read behavior and for consistent model-file updates. Related: [4.3–4.4](#43-efs)
