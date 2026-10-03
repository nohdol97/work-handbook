---
id: aws-cloud-storage
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-04-01
  - AWS-04-02
  - AWS-04-03
---

# Chapter 4. Storage

The supplied section numbers, order, diagrams, and supplementary Q&A are preserved. See the separate supplement for EBS Multi-Attach, deletion, and snapshots in 4.1; S3 bucket types and access conditions in 4.2; and EFS Regional/One Zone and shared-write limits in 4.3. Bucket names and layouts are study examples, not results from running AWS resources.

<!-- SOURCE CORE START -->

## 4.1 EBS

EBS = **Elastic Block Store**

> A virtual disk attached to EC2

```text
EC2
 ↓
EBS Volume
```

Analogy:

```text
EC2 = The computer itself
EBS = SSD/HDD
```

### EBS and EC2 are separate resources

EBS is storage that can be detached from EC2.

### Block Storage

The operating system sees it as a normal disk device.

Examples:

```text
/dev/xvda
/dev/nvme0n1
```

Create a file system such as ext4/xfs on top of it.

### EBS vs S3

```text
EBS
= Server disk

S3
= Object Storage
```

### EBS is scoped to an AZ

An EC2 instance and an EBS volume generally need to be in the same AZ to be attached.

```text
EC2: AZ A
EBS: AZ A
→ Can attach

EC2: AZ A
EBS: AZ B
→ Cannot attach directly
```

### Root Volume

The primary disk where the EC2 operating system is installed.

You can also attach additional EBS data volumes.

### Volume Type

Common types:

- gp3 = General-purpose SSD
- io2 = For high IOPS needs
- st/sc = HDD families

### IOPS vs Throughput

```text
IOPS
= Number of I/O operations per second

Throughput
= Amount of data transferred per second
```

### Snapshot

A point-in-time backup of an EBS volume.

```text
EBS
 ↓
Snapshot
 ↓
New EBS
```

It can also be restored in another AZ.

### EC2 termination and EBS

The root volume may be deleted along with EC2 depending on its `Delete on Termination` setting.

### Instance Store

Temporary storage local to the host.

```text
Important persistent data
→ EBS

Temporary data that can be lost
→ Instance Store
```

### EBS in EKS

```text
Pod
 ↓
PVC
 ↓
PV
 ↓
EBS
```

The AWS EBS CSI Driver manages EBS in between.

### AZ constraints

EBS is in a specific AZ, so constraints can arise when a Pod moves to a node in another AZ.

### RDS

RDS provides managed internal storage, so users do not directly attach/detach EBS volumes.

---

## 4.2 S3

S3 = **Simple Storage Service**

> AWS object storage

```text
Application
   ↓
S3 API
   ↓
Bucket
   ↓
Objects
```

### Bucket / Object

- Bucket = A container for objects
- Object = The actual data

Example:

```text
my-data-bucket
├─ images/logo.png
├─ models/model-v1.bin
└─ logs/2026/10/03/app.log
```

### A structure that looks like folders

These are object keys, not actual folders.

```text
logs/2026/10/03/app.log
```

The whole string is the key.

### Difference from EBS

EBS:

```text
EC2
 ↓
File System
 ↓
EBS
```

S3:

```text
Application
 ↓
HTTP/API
 ↓
S3
```

### Shared use by multiple services

```text
        S3
      /  |  \
    EC2 EKS Lambda
```

### Common data to store

- Images / videos
- Logs
- Backups
- CSV / Parquet
- AI Model
- Dataset
- Static web files
- Data Lake

### Data Platform

```text
Raw Data
   ↓
S3
   ↓
Parquet / Iceberg
   ↓
Analytics / AI
```

### S3 is a Region-based service

Choose a Region when creating a bucket.

It is not used by attaching it to a specific AZ like EBS.

### Versioning

You can preserve previous versions of the same key.

### Lifecycle

Older objects can be moved to a cheaper storage class or deleted.

### Storage Class

- Standard
- Infrequent Access families
- Glacier families

### Access Control

Usually kept private.

```text
Application
 ↓
IAM Role
 ↓
S3
```

### Bucket Policy

A resource-based policy applied to the bucket itself.

```text
IAM Policy
= Permissions on the user/role side

Bucket Policy
= Permissions on the bucket side
```

### VPC Endpoint

A private subnet can use a VPC Endpoint instead of NAT to access S3.

```text
Private Subnet
 ↓
VPC Endpoint
 ↓
S3
```

### AI / LLM

```text
S3
└─ Model Files
     ↓
GPU Node
     ↓
vLLM
```

### S3 is not a NAS

S3 is not a regular file system.

Its basic access methods are APIs such as:

- GetObject
- PutObject

These are API operations.

### Supplementary Q&A: Why divide object storage into buckets?

Separating policies and permissions is one major reason.

A bucket can be seen as a **major management boundary**.

```text
Bucket
├─ Access Policy
├─ Lifecycle
├─ Versioning
├─ Encryption
├─ Logging
└─ Objects
```

Examples:

```text
company-raw-data
company-model-artifacts
company-public-assets
```

Permission separation example:

```text
raw-data bucket
→ Only Data Engineers can write

model bucket
→ The AI Serving Role can only read

public-assets bucket
→ Public access is allowed
```

Other reasons to separate buckets:

- Security boundaries
- Separate lifecycle policies
- Separate versioning/replication settings
- Cost and operations management
- Environment separation (dev/stage/prod)

However, you do not need a separate bucket for every data type.

Prefixes within one bucket can also provide logical separation.

```text
data-platform-prod/
├─ raw/
├─ processed/
└─ curated/
```

Summary:

> Bucket = A major management/security boundary  
> Prefix = Logical grouping within a bucket

---

## 4.3 EFS

EFS = **Elastic File System**

> A shared file system that multiple EC2/EKS instances can mount at the same time

```text
        EFS
      /  |  \
    EC2 EC2 EKS
```

### Difference from EBS

```text
EBS
= Server disk

EFS
= Shared network file system
```

### Difference from S3

S3 is API-based object storage.

EFS can be mounted and used like a POSIX-style file system.

```text
/mnt/shared/file.txt
```

### NFS-based

EFS is a network file system and generally uses the NFS protocol.

### Why share files?

When multiple EC2 instances need to see the same files.

```text
        EFS
         │
    ┌────┼────┐
    ↓    ↓    ↓
  EC2A EC2B EC2C
```

### Multi-AZ

It can be designed for access from instances in multiple AZs.

### Mount Target

A network access point for EFS in a VPC.

### Security Group

NFS generally uses TCP 2049.

Example:

```text
EFS-SG
Inbound
2049 ← APP-SG
```

### EKS + EFS

```text
Pod
 ↓
PVC
 ↓
EFS CSI Driver
 ↓
EFS
```

Suitable when multiple Pods use the same shared file system.

### EBS vs EFS in Kubernetes

```text
EBS
→ Block storage for a single workload

EFS
→ File storage shared by multiple workloads
```

### S3 vs EFS

```text
Store/transfer data as objects
→ S3

Share a POSIX file system
→ EFS
```

### AI platform example

Using S3:

```text
S3
 ↓
GPU Node A downloads
GPU Node B downloads
GPU Node C downloads
```

Using EFS:

```text
        EFS
      /  |  \
   GPUA GPUB GPUC
```

### Data Platform

S3 is usually a more natural fit for a Data Lake than EFS.

```text
Raw Data
 ↓
S3
 ↓
Parquet / Iceberg
```

EFS fits cases that need a shared file system, such as shared config, workspaces, and legacy app files.

### Comparison of the 3 storage services

| Item | EBS | EFS | S3 |
|---|---|---|---|
| Storage Type | Block | File | Object |
| Access | Attach | Mount | API |
| Sharing | Limited | Shared by multiple servers | Shared by multiple services |
| Scope | AZ | Access across multiple AZs is possible | Region-based |
| Common uses | OS, DB Disk | Shared File System | Dataset, Backup, Model |
| EKS | PVC + EBS CSI | PVC + EFS CSI | SDK/API |

Selection criteria:

```text
Need a server disk
→ EBS

Multiple servers need to see the same file system
→ EFS

Store large amounts of files/data as objects
→ S3
```

### Supplementary Q&A: Do multiple PostgreSQL Pods share EFS?

No.

In general, multiple PostgreSQL Pods must not write to the same `PGDATA` on one EFS file system at the same time.

```text
        EFS
       /   \
Postgres A  Postgres B
   ↓            ↓
Modify the same DB files concurrently ❌
```

This risks data corruption.

Usually, each PostgreSQL Pod has its own dedicated volume.

```text
Postgres Primary
      ↓
    PVC A
      ↓
    EBS A

Postgres Replica
      ↓
    PVC B
      ↓
    EBS B
```

Data is copied through PostgreSQL replication, not file system sharing.

```text
Primary
  │
  │ WAL Replication
  ▼
Replica
```

In Kubernetes, a StatefulSet can be used to create this structure:

```text
postgres-0 → PVC-0 → EBS-0
postgres-1 → PVC-1 → EBS-1
postgres-2 → PVC-2 → EBS-2
```

This is one possible setup.

EFS is more suitable for backups or shared dumps than for the DB data directory.

```text
PostgreSQL
 ↓
pg_dump
 ↓
EFS or S3
```

S3 is especially common for backups.

On AWS, strongly consider RDS PostgreSQL / Aurora PostgreSQL rather than running PostgreSQL directly inside EKS, unless there is a specific reason to do so.

---

<!-- SOURCE CORE END -->

## Separate supplement: AZ, sharing, and persistence boundaries

Official documentation checked: 2026-10-03. The source is preserved above; apply the following conditions alongside it.

### 4.1 EBS AZ placement and Multi-Attach

EC2 must be in the same AZ as the EBS volume it directly attaches. Restoring in another AZ creates a **new volume** from a snapshot; it does not directly attach the existing volume there. [AWS EBS features](https://docs.aws.amazon.com/ebs/latest/userguide/EBSFeatures.html)

“Single workload” in the 4.3 comparison describes a common usage model. Supported `io1`/`io2` Multi-Attach volumes can attach to multiple Nitro instances in one AZ. However, concurrent access from multiple servers to a normal ext4/XFS file system is unsafe. Check supported Regions, operating systems, and instance types, and use a cluster-aware file system and coordinated writes. Multi-Attach does not replace cross-AZ or PostgreSQL replication. [AWS EBS Multi-Attach](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes-multi.html)

The volume type identifiers for the source's `st/sc` HDD families are `st1` and `sc1`. [AWS EBS volume types](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html)

### 4.1 Deletion settings and recoverability

Check `DeleteOnTermination` for each EBS volume's block device mapping, not just the root volume. Defaults can vary with root/data use, attachment time and method, and AMI settings. Preserved volumes still incur charges. Instance termination is not a backup policy. [AWS EBS persistence on termination](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/preserving-volumes-on-termination.html)

A snapshot does not include application or OS cache that has not reached the volume. DB backups need paused writes, flushing, or an application-specific consistency procedure. Creating a snapshot does not replace a restore test. [AWS EBS snapshots](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-creating-snapshot.html)

### 4.2 S3 scope and access conditions

“Region-based” describes common S3 use. S3 Express One Zone stores data in a directory bucket in a specific AZ. Do not assume all S3 data is stored across multiple AZs. [AWS S3 directory buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-create.html)

A name such as `public-assets` or a separate bucket does not grant public access. Check effective bucket policies and S3 Block Public Access settings. A prefix is a grouping, not an access boundary by itself. [AWS S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

Versioning must be enabled to preserve earlier versions. An ordinary delete request usually creates a delete marker, but deleting a specific version can permanently remove it. Earlier versions also incur storage charges, so review Lifecycle settings with Versioning. [AWS S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

For an S3 Gateway Endpoint, check route table associations and endpoint, IAM, and bucket policies. An endpoint's existence does not grant every subnet access to all S3 requests or remove every NAT path. [AWS S3 Gateway Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)

### 4.3 EFS Regional / One Zone and concurrent writes

Access from clients in multiple AZs differs from data replication across AZs. EFS Regional stores data across multiple AZs. One Zone stores data in one AZ and is not resilient to the loss of that AZ. [AWS EFS file system types](https://docs.aws.amazon.com/efs/latest/ug/features.html)

Regional supports a mount target in each AZ. One Zone supports only one mount target, in the file system's AZ. Access from a client in another AZ does not make the storage Multi-AZ. Also consider the path and cost of cross-AZ access. [AWS EFS mount targets](https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html), [AWS EFS One Zone mounting](https://docs.aws.amazon.com/efs/latest/ug/mounting-one-zone.html)

A shared mount does not coordinate concurrent writes by itself. EFS file locks are advisory. Applications must handle NFS consistency and locking semantics. [AWS EFS consistency](https://docs.aws.amazon.com/efs/latest/ug/features.html)

The PostgreSQL Q&A in 4.3 rules out independent DB servers modifying the same `PGDATA` concurrently. Do not expand this into “PostgreSQL cannot use any NFS storage.” PostgreSQL documents conditions for NFS use. The StatefulSet/PVC diagram also does not configure DB replication or failover by itself. [PostgreSQL file system requirements](https://www.postgresql.org/docs/current/creating-cluster.html), [PostgreSQL study](../platform-infrastructure/postgresql.md)

Reading guide: use 4.1 to separate attachment, AZ placement, and data lifetime; 4.2 for object APIs, permissions, and versions; and 4.3 for mounts, concurrent writes, and failure domains. Before choosing storage, record the access method, concurrent writers, and recovery needs, then connect them to AZ placement in [Compute](compute.md).

## LLM in Practice

### Situation

A hypothetical EKS design proposes EFS for both a shared `PGDATA` used by 2 PostgreSQL Pods and model files shared by multiple GPU nodes. Use [the Q&A in 4.3](#43-efs) to assess each data type's requirements first.

### Context to Give the LLM

Provide sanitized Pod/PVC and AZ placement, DB replication settings, model-file read and update behavior, EFS type, recovery goals, and performance requirements. Do not provide actual data or access keys.

### Example Prompt

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 EKS: PostgreSQL Pod 2개가 같은 EFS PGDATA에 쓰도록 제안되었다.
    여러 GPU Node도 EFS의 모델 파일을 읽으려 한다. EFS 유형과 복구 목표는 미확인이다.
    자료: [Pod/PVC·AZ 배치·DB 복제 구성·모델 갱신 방식·성능 요구].
    [요청]
    현재 제안부터 평가하고 DB 데이터와 모델 artifact의 동시 접근 요구를 구분하라.
    관측·가정·위험·누락 증거를 분리하고 EBS/EFS/S3 선택 조건을 설명하라.
    [출력]
    데이터 / writer·reader / 저장소 조건 / 장애 영역 / 추가 확인 표를 작성하라.
    동일 PGDATA의 동시 writer, Multi-Attach, EFS Regional/One Zone, S3 API 차이를 포함하라.
    [검증]
    AWS·PostgreSQL 공식 문서와 실제 설정으로 가설을 검증하라.
    StatefulSet이나 공유 mount만으로 DB 복제·failover가 생긴다고 가정하지 마라.
    데이터 이동·삭제·mount 변경은 실행하지 말고 격리된 복구 시험 계획을 제시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Hypothetical EKS: 2 PostgreSQL Pods are proposed to write to the same EFS PGDATA.
    Several GPU nodes also plan to read model files from EFS. The EFS type and recovery goals are unknown.
    Material: [Pod/PVC and AZ placement, DB replication setup, model update process, performance needs].
    [Task]
    Assess the current proposal first; separate concurrent-access needs for DB data and model artifacts.
    Separate observations, assumptions, risks, and missing evidence; explain EBS/EFS/S3 selection conditions.
    [Output]
    Create a table: data / writers and readers / storage conditions / failure domain / further checks.
    Include concurrent writers to one PGDATA, Multi-Attach, EFS Regional/One Zone, and S3 API differences.
    [Checks]
    Validate hypotheses against official AWS and PostgreSQL docs and actual settings.
    Do not assume a StatefulSet or shared mount creates DB replication or failover.
    Do not move or delete data or change mounts; propose an isolated recovery test plan.
    ```

### Expected Output

A conditional review table that first identifies the risk of concurrent writes to the same DB files, then separates DB replication from model distribution that mainly involves reads.

### What the LLM Can Get Wrong

It may claim that Multi-Attach or EFS makes DB replication unnecessary. It may treat One Zone as safe from AZ loss because it can be mounted from another AZ, or treat S3 as a regular POSIX file system.

### How to Validate

Compare storage types, mount targets, PVCs, and actual replication settings. Use isolated tests to check data consistency, recovery time, and recovery points. The LLM's choice is a hypothesis. This page did not operate AWS resources or databases or run recovery experiments.
