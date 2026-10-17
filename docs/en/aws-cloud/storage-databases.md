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

The latest compact source keeps its numbering, order, and combined comparison. See the separate supplement for EFS sharing and concurrent DB writes in 4.3–4.4, and DB placement, reads, and replication in 4.5–4.7. This is not a record of AWS operations or recovery tests.

<!-- SOURCE CORE START -->

## 4.1 EBS

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

## LLM in Practice

**Prompt:**

=== "한국어"

    ```text {.prompt}
    DB 또는 모델 파일 저장소를 바꾸는 설계·PVC PR에서 공유 방식과 복구 조건을 검토한다.
    현재 설계를 먼저 평가하라. 독립 PostgreSQL 서버의 같은 PGDATA 동시 쓰기와 읽기 중심 모델 파일 공유를 구분하고 전용 volume·DB replication·공유 mount의 책임을 나눠라.
    데이터 / 접근·동시 writer / 장애 영역 / 위험·근거 / 변경 후보 / 복구 검증 표를 작성하라. 모든 NFS를 금지하지 말고 EFS Regional/One Zone, RDS Multi-AZ 유형, Aurora 연결 분산을 실제 구성에 맞춰 구분하라.
    비밀값은 요구하거나 출력하지 말고, 검토안만 작성해 줘. 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review sharing and recovery requirements in a design or PVC PR that changes DB or model-file storage.
    Assess the existing design first. Distinguish independent PostgreSQL servers writing the same PGDATA from sharing mostly read-only model files. Separate dedicated volumes, DB replication, and shared-mount responsibilities.
    Produce a table: data / access and concurrent writers / failure domain / risk and evidence / proposal / recovery check. Do not ban all NFS use. Distinguish EFS Regional/One Zone, RDS Multi-AZ types, and Aurora connection distribution for the actual setup.
    Do not request or reveal secrets. Draft a review only; do not apply changes.
    ```

**Key point:** Writer/volume relationships for DB and model files, failure-domain and consistency risks, proposals, and a restore-check matrix for RPO/RTO. It may equate shared mounts with DB replication or assume One Zone survives an AZ failure because clients in multiple zones can read it. Check for independent writers to the same PGDATA and actual replication/backups. Require separate checks for EFS/DB deployment failure and read behavior and for consistent model-file updates. This is an authored work example, not a verified model result or measured improvement. Related: [4.3–4.4](#43-efs)

## Separate supplement: sharing, placement, and reads

Official documentation checked: 2026-10-04.

- **4.2:** An S3 endpoint's existence does not grant access. Check gateway-endpoint route table associations alongside endpoint, IAM, and bucket policies. [S3 Gateway Endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- **4.3:** Access by clients in multiple AZs differs from Multi-AZ data storage. EFS Regional stores data across AZs. One Zone stores it in one AZ and is not resilient to that AZ's loss. A shared mount does not coordinate concurrent writes by itself; file locks are advisory. [EFS types and consistency](https://docs.aws.amazon.com/efs/latest/ug/features.html)
- **4.4:** The warning concerns independent PostgreSQL servers modifying the same `PGDATA` concurrently. It does not ban all NFS use. PostgreSQL documents NFS requirements separately. Dedicated PVCs still need separate DB replication and failover configuration. [PostgreSQL file system requirements](https://www.postgresql.org/docs/current/creating-cluster.html), [PostgreSQL study](../platform-infrastructure/postgresql.md)
- **4.5:** A DB subnet group is a collection of subnets; it is not restricted to private ones. Read the source as a private-placement example. Also check public accessibility, routes, and security settings. [RDS VPC placement](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)
- **4.5:** A Multi-AZ DB instance standby does not serve reads, while the two standbys in a Multi-AZ DB cluster do. Apply the HA/read-scaling distinction by deployment type. [RDS Multi-AZ types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- **4.6:** The Aurora reader endpoint balances connections, not individual queries. Without readers it connects to the writer, which can also serve reads. [Aurora reader endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Endpoints.Reader.html)
- **4.7:** The source roles describe a common cache model. Asynchronous Valkey/Redis OSS replication can lose recent writes, and some Valkey configurations offer separate durability. Check recovery conditions by engine, version, and settings. Do not infer immediate consistency from TTL alone. [ElastiCache replication conditions](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.html)

Reading guide: compare access methods in 4.1–4.3, then concurrent-writer limits in 4.4. Read 4.5–4.7 as managed data-service roles rather than storage devices. Connect their placement to [Compute](compute.md).
