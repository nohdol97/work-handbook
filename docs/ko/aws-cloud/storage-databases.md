---
id: aws-cloud-storage-databases
status: studied
last_updated: 2026-10-04
last_reviewed: 2026-10-04
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

최신 compact 원문의 번호·순서·통합 비교를 보존했다. 4.3–4.4의 EFS 공유·DB 동시 쓰기와 4.5–4.7의 DB 배치·읽기·복제 조건은 뒤의 별도 보완에서 확인한다. 실제 AWS 운영·복구 시험 기록이 아니다.

<!-- SOURCE CORE START -->

## 4.1 EBS

Block Storage.

대표 용도:
- EC2 OS Disk
- Application Disk
- DB Disk
- EKS Persistent Volume

특징:
- AZ 단위
- Snapshot 지원
- IOPS / Throughput 고려

```text
IOPS = 초당 I/O 작업 횟수
Throughput = 초당 전송 데이터 양
```

---

## 4.2 S3

S3 = Simple Storage Service.

> AWS Object Storage

```text
Bucket
└─ Object
```

Object는 Key로 식별한다.

대표 용도:
- Dataset
- Model Artifact
- CSV / Parquet
- Logs
- Backup
- Image / Video
- Data Lake

### Versioning
같은 Key의 이전 버전을 보존할 수 있다.

### Lifecycle
오래된 Object를 다른 Storage Class로 이동하거나 삭제.

### Bucket Policy
Bucket 자체에 적용하는 Resource-based Policy.

```text
IAM Policy = User / Role 쪽 권한
Bucket Policy = Bucket 쪽 권한
```

### Bucket 분리 이유
Bucket은 큰 관리/보안 경계다.

- Access Policy
- Lifecycle
- Versioning / Replication
- Encryption
- 환경 분리
- 비용/운영 관리

Prefix는 Bucket 내부의 논리적 분류다.

```text
Bucket = 큰 관리 / 보안 경계
Prefix = Bucket 내부 논리적 분류
```

### S3는 파일시스템이 아니다
기본적으로 API(GetObject / PutObject)로 접근한다.

### VPC Endpoint
Private Subnet에서 NAT 없이 S3 접근에 사용할 수 있다.

---

## 4.3 EFS

EFS = Elastic File System.

> 여러 EC2/EKS Workload가 동시에 Mount할 수 있는 공유 파일시스템

특징:
- File Storage
- NFS 기반
- 여러 AZ Client 접근
- Mount Target
- NFS 기본 TCP 2049

비교:
```text
EBS = Block / 서버 디스크
EFS = Shared File
S3 = Object / API
```

Kubernetes:
```text
Pod 전용 Persistent Disk → EBS
여러 Pod 공유 File System → EFS
Dataset / Model / Object → S3
```

---

## 4.4 PostgreSQL 여러 Pod와 EFS

여러 PostgreSQL Pod가 하나의 EFS `PGDATA`를 공유하면 안 된다.

잘못된 구조:
```text
        EFS
       /   \
Postgres A  Postgres B
```

일반적 구조:
```text
Primary → PVC A → EBS A
Replica → PVC B → EBS B
```

데이터는 PostgreSQL Replication으로 복제한다.

```text
Primary
 ↓ WAL Replication
Replica
```

EFS는 DB 실시간 데이터 디렉터리보다 Shared File / Dump / Export에 더 적합하고, 백업은 S3를 많이 고려한다.

---

## 4.5 RDS

RDS = Relational Database Service.

> AWS Managed 관계형 DB 서비스

지원 예:
- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server
- Aurora

RDS는 하나의 DB 엔진이 아니라 여러 엔진을 Managed 형태로 제공하는 서비스다.

### 직접 PostgreSQL vs RDS
RDS는 OS, DB 설치, Backup, Patch, Failover, Replication, Storage 운영 부담을 상당 부분 줄인다.

### DB Subnet Group
RDS가 배치될 수 있는 Private Subnet 집합.

### Security Group
예:
```text
5432 ← APP-SG
```

### Endpoint
Application은 DB IP가 아니라 Endpoint를 사용한다.

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
Pod 수가 늘면 DB Connection도 증가하므로 Connection Pool 관리가 중요하다.
필요 시 RDS Proxy를 고려할 수 있다.

---

## 4.6 Aurora

Aurora는 AWS가 만든 PostgreSQL/MySQL-compatible DB Engine이다.

핵심:
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
Writer 장애 시 Reader를 새 Writer로 승격할 수 있다.

### Aurora Serverless
수요에 따라 DB Compute Capacity를 탄력적으로 조절하는 방식.

Aurora가 항상 더 좋은 것은 아니다.
비용, AWS Lock-in, PostgreSQL Extension/Version 호환성 등을 고려한다.

---

## 4.7 ElastiCache

> AWS Managed In-Memory Cache

대표 용도:
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

### RDS와 역할
```text
RDS = Source of Truth
ElastiCache = 빠른 임시 / 캐시 데이터
```

### Replica / Shard
```text
Replica = 같은 데이터 복제
Shard = 데이터 분할
```

### TTL / Invalidation
Cache는 stale data 문제가 있으므로 TTL, Delete, Update 정책이 필요하다.

Redis는 무조건 도입하는 것이 아니라 실제 DB 부하나 Latency 문제가 있을 때 도입하는 것이 좋다.

---

## Chapter 4 통합 비교

| 종류 | AWS 서비스 | 대표 용도 |
|---|---|---|
| Block Storage | EBS | OS / DB Disk |
| File Storage | EFS | Shared File System |
| Object Storage | S3 | Dataset / Model / Backup |
| Relational DB | RDS / Aurora | Transactional Data |
| In-Memory Cache | ElastiCache | Cache / Session |

---

<!-- SOURCE CORE END -->

## 별도 보완: 공유·배치·읽기의 조건

공식 문서 확인일: 2026-10-04.

- **4.2:** S3 endpoint가 존재하는 것만으로 접근 권한이 생기지는 않는다. Gateway endpoint의 route table 연결과 endpoint·IAM·bucket policy를 함께 확인한다. [S3 Gateway Endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- **4.3:** 여러 AZ client의 접근과 데이터의 Multi-AZ 저장은 다르다. EFS Regional은 여러 AZ에 저장하고 One Zone은 하나의 AZ에 저장하므로 그 AZ 손실에 대한 내성이 없다. 공유 mount 자체가 동시 쓰기 조정을 제공하지 않으며 file lock은 advisory다. [EFS 유형·일관성](https://docs.aws.amazon.com/efs/latest/ug/features.html)
- **4.4:** 경고의 대상은 독립 PostgreSQL 서버들이 동일 `PGDATA`를 동시에 수정하는 구성이다. 모든 NFS 사용을 금지하는 뜻은 아니다. PostgreSQL은 NFS 사용 조건을 별도로 설명한다. 전용 PVC를 나눈 뒤에도 DB replication·failover를 따로 구성해야 한다. [PostgreSQL 파일시스템 조건](https://www.postgresql.org/docs/current/creating-cluster.html), [PostgreSQL 학습](../platform-infrastructure/postgresql.md)
- **4.5:** DB subnet group은 subnet 집합이며 반드시 private만 가능한 것은 아니다. 원문은 private 배치 예시로 읽는다. 실제 공개 여부는 public accessibility·경로·보안 설정도 확인한다. [RDS VPC 배치](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)
- **4.5:** Multi-AZ DB instance의 standby는 읽기를 제공하지 않지만 Multi-AZ DB cluster의 두 standby는 읽기도 제공한다. HA와 read scaling의 구분은 배포 유형별로 적용한다. [RDS Multi-AZ 유형](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- **4.6:** Aurora reader endpoint는 query가 아니라 연결을 분산한다. Reader가 없으면 writer로 연결되며 writer도 읽기를 처리할 수 있다. [Aurora reader endpoint](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Endpoints.Reader.html)
- **4.7:** 원문의 역할 구분은 일반적인 cache 사용 모델이다. Valkey/Redis OSS의 비동기 복제는 최근 쓰기를 잃을 수 있고 일부 Valkey 구성은 별도 durability를 제공한다. 엔진·버전·설정별 복구 조건을 확인하며 TTL만으로 즉시 정합성을 가정하지 않는다. [ElastiCache 복제 조건](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Replication.html)

읽기 순서: 4.1–4.3의 접근 방식을 비교하고 4.4에서 동시 writer의 제약을 확인한다. 4.5–4.7은 저장 장치가 아니라 관리형 데이터 서비스의 역할로 읽는다. [Compute](compute.md)와 배치 관계를 연결한다.

## LLM in Practice

### 상황

DB와 모델 파일에 같은 공유 방식을 제안한 가상 설계다. [4.3–4.4](#43-efs)를 바탕으로 동시 접근 요구부터 검토한다.

### LLM에 제공할 맥락

비식별 Pod/PVC 배치, DB 복제, EFS 유형, 파일 읽기·갱신 방식과 복구 목표를 제공한다.

### 예시 프롬프트

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 설계가 PostgreSQL Pod 2개의 PGDATA와 모델 파일을 같은 EFS로 공유하려 한다.
    자료: [writer·reader 수·PVC·DB 복제·EFS 유형·복구 요구]. 미수집 설정은 미확인이다.
    [요청]
    기존 설계를 먼저 평가하고 DB 데이터와 읽기 중심 모델 파일의 요구를 구분하라.
    [출력]
    데이터 / 동시 접근 / 위험 / 누락 증거 / 다음 확인 표를 작성하라.
    전용 volume과 DB replication, EFS Regional/One Zone을 구분하라.
    [검증]
    관측과 가정을 나누고 AWS·PostgreSQL 공식 문서 및 실제 설정에 대조하라.
    데이터 이동·삭제를 실행하지 말고 격리된 일관성·복구 시험안을 제시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A hypothetical design shares PGDATA for 2 PostgreSQL Pods and model files on the same EFS.
    Material: [writer/reader counts, PVCs, DB replication, EFS type, recovery needs]. Uncollected settings are unknown.
    [Task]
    Assess the existing design first; separate DB data needs from model files mainly used for reads.
    [Output]
    Create a table: data / concurrent access / risk / missing evidence / next check.
    Distinguish dedicated volumes, DB replication, and EFS Regional/One Zone.
    [Checks]
    Separate observations from assumptions; compare official AWS/PostgreSQL docs with actual settings.
    Do not move or delete data; propose isolated consistency and recovery tests.
    ```

### 기대 출력

동일 PGDATA의 동시 수정 위험과 모델 파일 공유 조건을 구분한 검토표.

### LLM이 틀릴 수 있는 점

공유 mount가 DB 복제도 제공한다고 생각하거나 여러 AZ에서 접근하면 One Zone도 AZ 장애에 안전하다고 단정할 수 있다.

### 검증 방법

실제 writer·volume·복제 구성을 대조하고 격리 환경의 복원·정합성 시험으로 검증한다. LLM 출력은 가설이며 이 페이지에서는 DB나 AWS 리소스를 실행하지 않았다.
