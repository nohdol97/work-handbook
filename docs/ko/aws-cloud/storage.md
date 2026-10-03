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

제공된 원문의 번호·순서·도식·보충 Q&A를 보존했다. 4.1의 EBS Multi-Attach·삭제·snapshot, 4.2의 S3 bucket 유형·접근 조건, 4.3의 EFS Regional/One Zone·공유 쓰기 제약은 뒤의 별도 보완에서 확인한다. Bucket 이름과 배치는 학습 예시이며 실제 AWS 실행 결과가 아니다.

<!-- SOURCE CORE START -->

## 4.1 EBS

EBS = **Elastic Block Store**

> EC2에 붙여 사용하는 가상 디스크

```text
EC2
 ↓
EBS Volume
```

비유:

```text
EC2 = 컴퓨터 본체
EBS = SSD/HDD
```

### EBS와 EC2는 별도 리소스

EBS는 EC2와 분리 가능한 저장장치다.

### Block Storage

운영체제에서는 일반 디스크 장치처럼 보인다.

예:

```text
/dev/xvda
/dev/nvme0n1
```

위에 ext4/xfs 같은 파일시스템을 구성.

### EBS vs S3

```text
EBS
= 서버 디스크

S3
= Object Storage
```

### EBS는 AZ 단위

EC2와 EBS를 연결하려면 기본적으로 같은 AZ여야 한다.

```text
EC2: AZ A
EBS: AZ A
→ Attach 가능

EC2: AZ A
EBS: AZ B
→ 직접 Attach 불가
```

### Root Volume

EC2 운영체제가 설치된 기본 디스크.

추가 데이터 EBS도 연결 가능.

### Volume Type

대표:

- gp3 = 일반적인 SSD
- io2 = 높은 IOPS 요구
- st/sc = HDD 계열

### IOPS vs Throughput

```text
IOPS
= 초당 I/O 작업 횟수

Throughput
= 초당 전송 데이터 양
```

### Snapshot

EBS Volume의 시점 기반 백업.

```text
EBS
 ↓
Snapshot
 ↓
New EBS
```

다른 AZ에 복원도 가능.

### EC2 Terminate와 EBS

Root Volume은 `Delete on Termination` 설정에 따라 EC2와 같이 삭제될 수 있다.

### Instance Store

호스트 로컬 임시 스토리지.

```text
중요한 지속 데이터
→ EBS

잃어도 되는 임시 데이터
→ Instance Store
```

### EKS에서 EBS

```text
Pod
 ↓
PVC
 ↓
PV
 ↓
EBS
```

AWS EBS CSI Driver가 중간에서 EBS를 관리.

### AZ 제약

EBS는 특정 AZ에 있으므로 Pod가 다른 AZ Node로 이동할 때 제약이 생길 수 있다.

### RDS

RDS는 내부 스토리지를 Managed 형태로 제공하므로 사용자가 EBS를 직접 attach/detach하지 않는다.

---

## 4.2 S3

S3 = **Simple Storage Service**

> AWS의 Object Storage

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

- Bucket = Object를 담는 컨테이너
- Object = 실제 데이터

예:

```text
my-data-bucket
├─ images/logo.png
├─ models/model-v1.bin
└─ logs/2026/10/03/app.log
```

### 폴더처럼 보이는 구조

실제로는 폴더가 아니라 Object Key.

```text
logs/2026/10/03/app.log
```

이 전체가 Key다.

### EBS와 차이

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

### 여러 서비스가 공동 사용

```text
        S3
      /  |  \
    EC2 EKS Lambda
```

### 대표 저장 데이터

- 이미지 / 영상
- 로그
- 백업
- CSV / Parquet
- AI Model
- Dataset
- 정적 웹 파일
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

### S3는 Region 기반 서비스

Bucket 생성 시 Region을 선택한다.

EBS처럼 특정 AZ에 붙이는 개념으로 쓰지 않는다.

### Versioning

같은 Key의 이전 버전을 보존할 수 있다.

### Lifecycle

오래된 Object를 저렴한 Storage Class로 이동하거나 삭제할 수 있다.

### Storage Class

- Standard
- Infrequent Access 계열
- Glacier 계열

### Access Control

보통 Private으로 사용.

```text
Application
 ↓
IAM Role
 ↓
S3
```

### Bucket Policy

Bucket 자체에 적용하는 Resource-based Policy.

```text
IAM Policy
= User/Role 쪽 권한

Bucket Policy
= Bucket 쪽 권한
```

### VPC Endpoint

Private Subnet에서 S3 접근 시 NAT 대신 VPC Endpoint를 사용할 수 있다.

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

### S3는 NAS가 아니다

S3는 일반 파일시스템이 아니다.

기본 접근은:

- GetObject
- PutObject

같은 API 방식.

### 보충 Q&A: Object Storage를 Bucket으로 나누는 이유

정책/권한 분리가 큰 이유 중 하나다.

Bucket은 **큰 관리 경계**로 볼 수 있다.

```text
Bucket
├─ Access Policy
├─ Lifecycle
├─ Versioning
├─ Encryption
├─ Logging
└─ Objects
```

예:

```text
company-raw-data
company-model-artifacts
company-public-assets
```

권한 분리 예:

```text
raw-data bucket
→ Data Engineer만 write 가능

model bucket
→ AI Serving Role은 read만 가능

public-assets bucket
→ 외부 공개 허용
```

그 외 Bucket 분리 이유:

- 보안 경계
- Lifecycle 정책 분리
- Versioning/Replication 설정 분리
- 비용/운영 관리
- 환경 분리(dev/stage/prod)

다만 데이터 종류마다 무조건 Bucket을 나눌 필요는 없다.

하나의 Bucket 내부 Prefix로 논리적 구분도 가능.

```text
data-platform-prod/
├─ raw/
├─ processed/
└─ curated/
```

정리:

> Bucket = 큰 관리/보안 경계  
> Prefix = Bucket 내부 논리적 분류

---

## 4.3 EFS

EFS = **Elastic File System**

> 여러 EC2/EKS 인스턴스가 동시에 마운트해서 쓸 수 있는 공유 파일시스템

```text
        EFS
      /  |  \
    EC2 EC2 EKS
```

### EBS와 차이

```text
EBS
= 서버 디스크

EFS
= 공유 네트워크 파일시스템
```

### S3와 차이

S3는 API 기반 Object Storage.

EFS는 POSIX 스타일 파일시스템처럼 Mount해서 사용할 수 있다.

```text
/mnt/shared/file.txt
```

### NFS 기반

EFS는 네트워크 파일시스템이며 일반적으로 NFS 프로토콜을 사용한다.

### 공유가 필요한 이유

여러 EC2가 같은 파일을 봐야 할 때.

```text
        EFS
         │
    ┌────┼────┐
    ↓    ↓    ↓
  EC2A EC2B EC2C
```

### Multi-AZ

여러 AZ의 인스턴스에서 접근 가능하도록 설계할 수 있다.

### Mount Target

VPC에서 EFS에 접근하기 위한 네트워크 접점.

### Security Group

NFS는 일반적으로 TCP 2049를 사용.

예:

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

여러 Pod가 하나의 공유 파일시스템을 함께 사용할 때 적합.

### EBS vs EFS in Kubernetes

```text
EBS
→ 단일 Workload용 Block Storage

EFS
→ 여러 Workload가 공유하는 File Storage
```

### S3 vs EFS

```text
Object 형태로 저장/전송
→ S3

POSIX 파일시스템 공유
→ EFS
```

### AI Platform 예

S3 방식:

```text
S3
 ↓
GPU Node A 다운로드
GPU Node B 다운로드
GPU Node C 다운로드
```

EFS 방식:

```text
        EFS
      /  |  \
   GPUA GPUB GPUC
```

### Data Platform

Data Lake는 보통 EFS보다 S3가 자연스럽다.

```text
Raw Data
 ↓
S3
 ↓
Parquet / Iceberg
```

EFS는 Shared Config, Workspace, Legacy App Files 등 파일시스템 공유가 필요할 때 적합.

### Storage 3종 비교

| 항목 | EBS | EFS | S3 |
|---|---|---|---|
| Storage Type | Block | File | Object |
| 접근 | Attach | Mount | API |
| 공유 | 제한적 | 여러 서버 공유 | 여러 서비스 공유 |
| 범위 | AZ | Multi-AZ 접근 가능 | Region 기반 |
| 대표 용도 | OS, DB Disk | Shared File System | Dataset, Backup, Model |
| EKS | PVC + EBS CSI | PVC + EFS CSI | SDK/API |

선택 기준:

```text
서버 디스크가 필요
→ EBS

여러 서버가 같은 파일시스템을 봐야 함
→ EFS

대규모 파일/데이터를 객체 형태로 저장
→ S3
```

### 보충 Q&A: PostgreSQL 여러 Pod면 EFS를 공유하는가?

아니다.

여러 PostgreSQL Pod가 하나의 EFS에 동일한 `PGDATA`를 동시에 쓰는 구조는 일반적으로 사용하면 안 된다.

```text
        EFS
       /   \
Postgres A  Postgres B
   ↓            ↓
동일 DB 파일 동시 수정 ❌
```

데이터 손상 위험이 있다.

일반적으로 각 PostgreSQL Pod가 자기 전용 Volume을 가진다.

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

데이터 복제는 파일시스템 공유가 아니라 PostgreSQL Replication으로 한다.

```text
Primary
  │
  │ WAL Replication
  ▼
Replica
```

Kubernetes에서는 StatefulSet을 사용해:

```text
postgres-0 → PVC-0 → EBS-0
postgres-1 → PVC-1 → EBS-1
postgres-2 → PVC-2 → EBS-2
```

형태로 구성할 수 있다.

EFS는 DB 데이터 디렉터리보다는 백업/공유 Dump 같은 용도에 더 적합하다.

```text
PostgreSQL
 ↓
pg_dump
 ↓
EFS 또는 S3
```

특히 백업은 S3가 더 흔하다.

AWS에서는 특별한 이유가 없다면 EKS 내부 직접 PostgreSQL 운영보다 RDS PostgreSQL / Aurora PostgreSQL도 강하게 고려한다.

---

<!-- SOURCE CORE END -->

## 별도 보완: AZ·공유·보존의 실제 경계

공식 문서 확인일: 2026-10-03. 원문은 위에 보존했으며 다음 조건을 함께 적용한다.

### 4.1 EBS의 AZ와 Multi-Attach

EBS를 직접 연결할 EC2는 같은 AZ에 있어야 한다. 다른 AZ 복원은 snapshot에서 **새 volume**을 만드는 방식이며 기존 volume의 직접 연결이 아니다. [AWS EBS features](https://docs.aws.amazon.com/ebs/latest/userguide/EBSFeatures.html)

4.3 비교의 “단일 Workload”는 일반적인 사용 모델이다. 지원되는 `io1`/`io2` Multi-Attach는 같은 AZ의 Nitro 인스턴스 여러 대에 연결할 수 있지만, 일반 ext4/XFS를 여러 서버에서 동시에 쓰는 방식은 안전하지 않다. 지원 리전·OS·인스턴스 조건과 cluster-aware 파일시스템·쓰기 조정이 필요하다. Multi-Attach는 AZ 간 복제나 PostgreSQL 복제를 대신하지 않는다. [AWS EBS Multi-Attach](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes-multi.html)

원문의 HDD 계열 `st/sc`에 해당하는 volume type 식별자는 `st1`과 `sc1`이다. [AWS EBS volume types](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html)

### 4.1 삭제 설정과 복구 가능성

`DeleteOnTermination`은 root뿐 아니라 각 EBS volume의 block device mapping별로 확인한다. Root/data 구분, 연결 시점과 방법, AMI 설정에 따라 기본값이 다를 수 있다. 보존된 volume은 계속 비용이 발생하며, 인스턴스 종료를 백업 정책으로 취급하지 않는다. [AWS EBS persistence on termination](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/preserving-volumes-on-termination.html)

Snapshot은 아직 volume에 기록되지 않은 애플리케이션·OS cache를 포함하지 않는다. DB 백업에는 쓰기 정지·flush 또는 애플리케이션에 맞는 일관성 절차가 필요하다. Snapshot 생성만으로 복원 검증을 대신할 수 없다. [AWS EBS snapshots](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-creating-snapshot.html)

### 4.2 S3의 범위와 접근 조건

“Region 기반” 설명은 일반적인 S3 사용의 기준이다. S3 Express One Zone은 특정 AZ의 directory bucket에 데이터를 저장하므로 모든 S3 데이터가 여러 AZ에 저장된다고 일반화하지 않는다. [AWS S3 directory buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-bucket-create.html)

`public-assets`라는 이름이나 bucket 분리만으로 공개 접근이 허용되지는 않는다. Bucket policy와 S3 Block Public Access 등 실제 유효 설정을 확인한다. Prefix도 분류일 뿐 그 자체가 권한 경계는 아니다. [AWS S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)

Versioning은 설정을 활성화해야 이전 버전을 보존한다. 보통의 삭제 요청은 delete marker를 만들지만 특정 version을 지정한 삭제는 그 버전을 영구 삭제할 수 있다. 이전 version도 저장 비용이 발생하므로 Lifecycle 설정과 함께 검토한다. [AWS S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

S3 Gateway Endpoint는 대상 route table 연결과 endpoint·IAM·bucket policy 조건을 확인해야 한다. Endpoint가 있다는 사실만으로 모든 subnet의 모든 S3 요청에 접근 권한이 생기거나 NAT 경유가 사라지는 것은 아니다. [AWS S3 Gateway Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)

### 4.3 EFS Regional / One Zone과 동시 쓰기

여러 AZ의 client가 접근할 수 있다는 것과 데이터가 여러 AZ에 복제되어 있다는 것은 다르다. EFS Regional은 여러 AZ에 데이터를 저장하고, One Zone은 하나의 AZ에 저장하므로 그 AZ 손실에 대한 내성이 없다. [AWS EFS file system types](https://docs.aws.amazon.com/efs/latest/ug/features.html)

Regional은 AZ별 mount target을 만들 수 있다. One Zone은 파일시스템과 같은 AZ의 mount target 하나만 지원하며 다른 AZ client가 접근해도 저장소가 Multi-AZ로 바뀌지 않는다. 교차 AZ 접근 비용·경로도 고려한다. [AWS EFS mount targets](https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html), [AWS EFS One Zone mounting](https://docs.aws.amazon.com/efs/latest/ug/mounting-one-zone.html)

공유 mount 자체가 동시 쓰기 조정을 해결하지는 않는다. EFS의 file lock은 advisory이며 애플리케이션이 NFS의 일관성·잠금 의미를 다뤄야 한다. [AWS EFS consistency](https://docs.aws.amazon.com/efs/latest/ug/features.html)

4.3의 PostgreSQL Q&A가 금지하는 것은 독립적인 DB 서버들이 동일 `PGDATA`를 동시에 수정하는 구조다. 이를 “PostgreSQL은 모든 NFS 저장소를 사용할 수 없다”로 확대하지 않는다. PostgreSQL은 NFS 사용 조건을 별도로 설명한다. StatefulSet별 PVC 도식도 그 자체로 DB replication·failover 구성을 완료하지 않는다. [PostgreSQL file system requirements](https://www.postgresql.org/docs/current/creating-cluster.html), [PostgreSQL 학습](../platform-infrastructure/postgresql.md)

읽기 순서: 4.1에서 attach·AZ·데이터 수명을, 4.2에서 object API·권한·version을, 4.3에서 mount·공유 쓰기·장애 영역을 구분한다. Storage 선택 전에 접근 방식, 동시 writer, 복구 요구를 적고 [Compute](compute.md)의 AZ 배치와 연결한다.

## LLM in Practice

### 상황

가상의 EKS 설계가 PostgreSQL Pod 2개의 동일 `PGDATA` 공유와 여러 GPU Node의 모델 파일 공유를 모두 EFS로 해결하려 한다. [4.3의 Q&A](#43-efs)를 바탕으로 데이터별 요구를 먼저 검토한다.

### LLM에 제공할 맥락

비식별 Pod/PVC·AZ 배치, DB replication 구성, 모델 파일의 읽기·갱신 방식, EFS 유형, 복구 목표와 성능 요구를 제공한다. 실제 데이터·접근 키는 제공하지 않는다.

### 예시 프롬프트

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

### 기대 출력

동일 DB 파일 동시 쓰기 위험을 먼저 짚고, DB replication과 읽기 중심 모델 배포를 구분한 조건부 검토표.

### LLM이 틀릴 수 있는 점

Multi-Attach나 EFS를 쓰면 DB replication이 불필요하다고 판단할 수 있다. 다른 AZ에서 mount된다는 이유로 One Zone을 AZ 장애에 안전하다고 설명하거나 S3를 일반 POSIX 파일시스템으로 취급할 수도 있다.

### 검증 방법

Storage type·mount target·PVC와 실제 replication 설정을 대조하고, 데이터 일관성과 복구 시간·시점을 격리 시험으로 확인한다. LLM의 선택은 가설이며 이 페이지에서는 AWS 리소스·DB를 운영하거나 복구 실험을 실행하지 않았다.
