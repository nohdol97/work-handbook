<!-- 반입 기록
범위: 최신 압축형 AWS Cloud Basic 1~5장·7장 커리큘럼·최종 요약·진도
한계: 개념 학습 자료이며 실제 AWS 리소스 운영·성능·복구 검증 결과가 아니다.
원본 bytes: 24577; SHA-256: 7df52de48d6b77561746b371e3b96a5fd66f196a26144c6599304316340d2c79
정규화: 없음. 원문의 hard break와 모든 byte를 경계 뒤에 그대로 보존한다.
whitespace_restoration: []
-->
<!-- ORIGINAL SOURCE START -->
# AWS Cloud Basic — Source Markdown (Chapter 1~5)

> 기준: 현재 세션의 압축형 AWS Cloud Basic 커리큘럼  
> 원칙: 중복 제거, 핵심 중심, 세션 중 나온 보충 질문과 오개념 교정 반영  
> Terraform / IaC는 다른 Platform / Infrastructure 세션에서 이미 학습했으므로 별도 Chapter에서 제외

---

# 전체 압축 커리큘럼

1. AWS Foundation
2. Networking
3. Compute & Load Balancing
4. Storage & Database
5. EKS on AWS
6. AWS Managed Services
7. AI/GPU + End-to-End

이 문서는 Chapter 1~5까지의 학습 내용을 정리한다.

---

# Chapter 1. AWS Foundation

## 1.1 Region / Availability Zone

### Region
AWS의 큰 지리적 운영 영역이다.

예:
```text
Seoul Region
ap-northeast-2
```

Region 선택 시 주요 고려 요소:
- 사용자와의 거리 / Latency
- 데이터 저장 위치와 규제
- 해당 Region의 AWS 서비스 지원 여부
- 비용

### Availability Zone
AZ는 하나의 Region 안에 존재하는 독립된 장애 영역이다.

```text
Seoul Region
├─ AZ A
├─ AZ B
├─ AZ C
└─ AZ D
```

AZ는 데이터센터 하나라고 단정하기보다 하나 이상의 데이터센터로 구성될 수 있는 독립 장애 영역으로 이해한다.

### Multi-AZ
한 AZ에만 서비스를 배치하면 해당 AZ 장애가 전체 서비스 장애로 이어질 수 있다.

```text
ALB
├─ AZ A → Application
└─ AZ B → Application
```

따라서 Production에서는 하나의 Region 안에서 여러 AZ에 리소스를 분산하는 구성이 기본이다.

핵심:
```text
Region = 큰 지리적 영역
AZ = Region 내부의 독립 장애 영역
기본 운영 패턴 = Single Region + Multi-AZ
```

---

## 1.2 AWS Account / Organizations

AWS Account는 단순 로그인 계정이 아니라 리소스, 비용, 권한의 큰 관리 경계다.

```text
AWS Account
├─ EC2
├─ S3
├─ RDS
├─ EKS
└─ IAM
```

하나의 Account 안에서 여러 Region을 사용할 수 있다.

```text
Account = 관리 / 권한 / 비용 경계
Region = 지리적 배치 영역
```

실무에서는 환경이나 조직에 따라 Account를 분리하기도 한다.

```text
AWS Organization
├─ Dev Account
├─ Staging Account
├─ Prod Account
├─ Security Account
└─ Data Account
```

장점:
- 운영 실수 격리
- 권한 분리
- 비용 분리
- 보안 경계 강화

### Root User
Account의 최상위 사용자다. 평소 운영에는 사용하지 않고 초기 설정이나 매우 제한된 작업에만 사용하는 것이 기본이다.

### AWS Organizations
여러 AWS Account를 중앙에서 관리한다.

### OU
Organizational Unit. Account들을 묶는 논리적 그룹이다.

### SCP
Service Control Policy. 조직/OU/Account 수준에서 최대 허용 권한 범위를 제한한다.

```text
IAM Policy = 실제 권한 부여
SCP = 조직 수준의 최대 허용 범위 제한
```

SCP 자체가 권한을 주는 것은 아니다.

---

## 1.3 IAM User / Role / Policy

IAM = Identity and Access Management.

> 누가 어떤 AWS Resource에 무엇을 할 수 있는가를 관리한다.

핵심:
```text
IAM User
IAM Role
IAM Policy
```

### IAM User
AWS Account 내부의 고정 사용자 Identity.

기업 환경에서는 사람에게 장기 Access Key를 직접 주기보다 SSO / IAM Identity Center + Role 방식을 많이 고려한다.

### IAM Policy
권한 규칙.

예:
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

핵심 요소:
```text
Effect
Action
Resource
Condition
```

### IAM Role
필요할 때 맡는 권한 묶음.

```text
Identity
 ↓
AssumeRole
 ↓
IAM Role
 ↓
AWS Resource
```

Role 기반 인증에서는 만료 시간이 있는 Temporary Credential을 사용할 수 있다.

일반적으로:
- Access Key
- Secret Key
- Session Token
- Expiration

### Trust Policy vs Permission Policy
```text
Trust Policy = 누가 이 Role을 맡을 수 있는가
Permission Policy = Role을 맡았을 때 무엇을 할 수 있는가
```

### Least Privilege
필요한 최소 권한만 부여한다.

```text
나쁜 예
s3:* / Resource: *

좋은 예
s3:GetObject / 특정 bucket/*
```

### IAM과 Kubernetes RBAC
```text
Pod → Kubernetes API = Kubernetes RBAC
Pod → S3 / SQS / Secrets Manager = AWS IAM
```

---

## 1.4 AWS Resource / ARN

AWS Resource 예:
- EC2 Instance
- S3 Bucket
- IAM Role
- RDS Instance
- EKS Cluster

많은 AWS Resource는 ARN(Amazon Resource Name)으로 식별한다.

예:
```text
arn:aws:iam::123456789012:role/MyRole
```

---

# Chapter 2. Networking

## 2.1 VPC

VPC = Virtual Private Cloud.

> AWS 안에 만드는 사설 네트워크 공간

```text
AWS Account
 ↓
Region
 ↓
VPC
 ↓
Subnet
 ↓
EC2 / EKS / RDS
```

VPC는 Region 범위 Resource다.

예:
```text
VPC CIDR
10.0.0.0/16
```

### VPC와 Subnet
```text
VPC 10.0.0.0/16
├─ Subnet A 10.0.1.0/24
├─ Subnet B 10.0.2.0/24
└─ Subnet C 10.0.3.0/24
```

```text
VPC = Region 범위
Subnet = 하나의 AZ에 속함
```

### Subnet과 EKS Node
Subnet은 Node가 아니다.

```text
VPC
└─ Subnet
   └─ EKS Node
      └─ Pod
```

- Subnet = 네트워크 공간
- EKS Node = 실제 컴퓨팅 서버, 보통 EC2

하나의 Subnet 안에 여러 Node가 들어갈 수 있다.

비유:
> Subnet은 땅이고, Node는 그 땅 위의 서버다.

---

## 2.2 CIDR

CIDR = Classless Inter-Domain Routing.

> IP 주소 범위를 표현하는 방식

예:
```text
10.0.0.0/24
```

IPv4는 32bit이고 `/24`는 앞 24bit가 네트워크 영역으로 고정된다는 의미다.

```text
/16 = 65,536 주소
/20 = 4,096
/24 = 256
/28 = 16
/32 = 1
/0  = 모든 IPv4
```

핵심:
```text
Prefix 숫자가 작을수록 범위 큼
Prefix 숫자가 클수록 범위 작음
```

### 0.0.0.0/0
모든 IPv4 주소와 매칭된다.

### /32
정확히 IP 하나를 의미한다.

### AWS 예약 IP
AWS는 각 Subnet에서 일부 IP를 예약한다.

따라서 `/24 = 256개`지만 실제 사용 가능한 주소는 251개다.

그리고 EKS에서는:
- Node IP
- Pod IP
- ENI 관련 주소
- 기타 AWS Resource IP

등도 사용하므로 `/24 = Node+Pod 256개`라고 계산하면 안 된다.

---

## 2.3 Public IP / Private IP

대표 Private IPv4 범위:

| 범위 | CIDR |
|---|---|
| 10.0.0.0 ~ 10.255.255.255 | 10.0.0.0/8 |
| 172.16.0.0 ~ 172.31.255.255 | 172.16.0.0/12 |
| 192.168.0.0 ~ 192.168.255.255 | 192.168.0.0/16 |

```text
Private IP = 내부 네트워크 통신
Public IP = 인터넷 통신
```

Private IP는 인터넷에서 직접 라우팅되지 않는다.

---

## 2.4 Public / Private Subnet

Public/Private Subnet은 별도 타입이 아니라 Route Table 구성으로 구분된다.

### Public Subnet
대표 Route:
```text
0.0.0.0/0 → Internet Gateway
```

Public Resource의 직접 인터넷 통신에는 보통:
- IGW Route
- Public IP / Elastic IP
- Security Group 허용

등이 필요하다.

### Private Subnet
IGW로 직접 가는 Route가 없다.

외부로 나가야 할 경우:
```text
0.0.0.0/0 → NAT Gateway
```

대표 배치:
```text
Public Subnet
→ ALB / NAT Gateway

Private Subnet
→ EKS Node / EC2 App / RDS / ElastiCache / MSK
```

---

## 2.5 Route Table

> 목적지에 따라 트래픽을 어디로 보낼지 결정한다.

예:
```text
Destination        Target
10.0.0.0/16        local
0.0.0.0/0          igw-xxxx
```

### 대표 Route
```text
10.0.0.0/16 → local
= 같은 VPC 내부 통신

0.0.0.0/0 → IGW
= Public Internet

0.0.0.0/0 → NAT Gateway
= Private Subnet Outbound
```

### Longest Prefix Match
여러 Route가 매칭되면 더 구체적인 CIDR이 우선한다.

### Route Table vs Security Group
```text
Route Table = 어디로 갈지
Security Group = 통신을 허용할지
```

---

## 2.6 Internet Gateway

IGW = Internet Gateway.

> VPC와 인터넷을 연결하는 Gateway

```text
Internet
 ↓
IGW
 ↓
VPC
```

IGW는 특정 Subnet이 아니라 VPC에 연결한다.

Public Subnet:
```text
0.0.0.0/0 → IGW
```

Public EC2가 직접 인터넷 통신하려면 일반적으로:
1. VPC에 IGW
2. Route Table
3. Public IP
4. Security Group 허용

IGW는 AZ마다 만드는 것이 아니라 VPC 단위로 여러 Public Subnet이 공유한다.

---

## 2.7 NAT Gateway

> Private Subnet Resource의 인터넷 Outbound 출구

```text
Private Subnet
 ↓
NAT Gateway
 ↓
IGW
 ↓
Internet
```

```text
Private → Internet = 가능
Internet → Private 직접 시작 = 불가
```

NAT Gateway는 일반적으로 Public Subnet에 둔다.

Production Multi-AZ에서는 AZ별 NAT Gateway를 고려한다.

AWS 내부 서비스(S3/ECR 등)는 VPC Endpoint를 통해 NAT를 우회할 수 있는 경우도 있다.

---

## 2.8 Security Group

> AWS Resource / ENI에 적용되는 Stateful 가상 방화벽

기준:
- Protocol
- Port
- Source / Destination

예:
```text
TCP 443
Source: 0.0.0.0/0
```

### Stateful
허용된 요청의 응답 트래픽은 자동으로 허용한다.

### SG Reference
IP 대신 다른 Security Group을 Source로 지정할 수 있다.

```text
ALB-SG
443 ← Internet

APP-SG
8080 ← ALB-SG

DB-SG
5432 ← APP-SG
```

### Security Group vs NACL
| 항목 | Security Group | NACL |
|---|---|---|
| 적용 | Resource/ENI | Subnet |
| Stateful | O | X |
| Allow | O | O |
| Explicit Deny | X | O |

---

## 2.9 Multi-AZ VPC 기본 구조

```text
VPC
├─ AZ A
│  ├─ Public Subnet A
│  │  ├─ ALB
│  │  └─ NAT Gateway A
│  └─ Private Subnet A
│     └─ Application / EKS Node
└─ AZ B
   ├─ Public Subnet B
   │  ├─ ALB
   │  └─ NAT Gateway B
   └─ Private Subnet B
      └─ Application / EKS Node
```

---

# Chapter 3. Compute & Load Balancing

## 3.1 EC2

EC2 = Elastic Compute Cloud.

> AWS의 가상 서버

대표 설정:
- AMI
- Instance Type
- VPC
- Subnet
- Security Group
- Storage
- IAM Role

### AMI
EC2 생성용 VM 이미지.

```text
AMI = VM 전체 이미지
Docker Image = Container 실행 이미지
```

### Instance Type
CPU / Memory / GPU 등의 하드웨어 사양.

```text
t = 범용 / 저비용
m = General Purpose
c = Compute Optimized
r = Memory Optimized
g / p = GPU
```

### EC2와 Subnet
EC2는 특정 Subnet에 생성되며 Subnet 선택으로 AZ가 결정된다.

### User Data
최초 부팅 시 실행할 초기화 Script.

### Public / Private EC2
Public EC2는 IGW/Public IP와 연결될 수 있고, Private EC2는 NAT를 통해 외부로 나갈 수 있다.

### Elastic IP
고정 Public IPv4가 필요한 경우 사용 가능.

### IAM Role
Access Key를 코드에 직접 저장하기보다 IAM Role을 통해 AWS Resource에 접근한다.

### EKS Node
EKS Worker Node의 실체는 보통 EC2다.

---

## 3.2 EBS와 EC2

EBS = Elastic Block Store.

> EC2에 붙이는 Block Storage

```text
EC2
 ↓
EBS
```

EC2는 Compute, EBS는 Storage다.

EBS는 특정 AZ에 속하므로 EC2와 같은 AZ에서 Attach한다.

---

## 3.3 Launch Template / Auto Scaling Group

### Launch Template
EC2 생성 설계도.

포함 예:
- AMI
- Instance Type
- Security Group
- IAM Role
- Storage
- User Data

### ASG
Auto Scaling Group.

```text
Min 2
Desired 3
Max 10
```

```text
Scale Out = 서버 추가
Scale In = 서버 제거
```

Desired보다 인스턴스가 줄면 새 EC2를 만들어 수를 맞출 수 있다.

Scaling 방식:
- Metric 기반
- Target Tracking
- Scheduled Scaling

Auto Scaling 환경에서는 Application을 Stateless하게 두는 것이 유리하다.

```text
Persistent Data → RDS
Cache / Session → ElastiCache
Object → S3
```

---

## 3.4 ALB

ALB = Application Load Balancer.

> HTTP/HTTPS를 이해하는 L7 Load Balancer

역할:
- 요청 분산
- Health Check
- TLS Termination
- Host Routing
- Path Routing

예:
```text
/api/* → api-service
/admin/* → admin-service
```

### Listener
어떤 Protocol/Port로 요청을 받을지 정의.

### Target Group
실제 Backend Target 묶음.

### Health Check
Unhealthy Target에는 트래픽을 보내지 않는다.

ALB는 Internet-facing 또는 Internal로 사용할 수 있다.

---

## 3.5 NLB

NLB = Network Load Balancer.

> TCP / UDP / TLS 중심의 L4 Load Balancer

```text
ALB = L7 / HTTP / HTTPS / Path / Host
NLB = L4 / TCP / UDP / TLS
```

중요:
> ALB = 외부용, NLB = 내부용으로 구분하는 것이 아니다.

둘 다 외부/내부 구성 가능하다.

---

## 3.6 Kubernetes Service와 ALB/NLB

Kubernetes Service도 Protocol과 Port를 가진다.

예:
```yaml
ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

Service의 핵심 역할:
> 여러 Pod Replica를 하나의 안정적인 Endpoint로 묶고 L4 수준에서 분산한다.

### 내부 Pod 통신
```text
Pod
 ↓
ClusterIP Service
 ↓
Pod Replicas
```

### 외부 HTTP/HTTPS
```text
Internet
 ↓
ALB
 ↓
Service
 ↓
Pod Replicas
```

### TCP/UDP
```text
Client
 ↓
NLB
 ↓
Service
 ↓
Pod Replicas
```

최종 정리:
```text
Service = Pod Replica를 안정적인 Endpoint로 묶음
ALB = L7 HTTP/HTTPS 진입점
NLB = L4 TCP/UDP/TLS 진입점
```

### ALB/NLB Target
구성에 따라:
```text
instance target → EC2 Node
ip target → Pod IP
```

즉 ALB/NLB가 항상 Node만 선택하는 것은 아니다.

---

# Chapter 4. Storage & Database

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

# Chapter 5. EKS on AWS

## 5.1 EKS 구조

EKS = Elastic Kubernetes Service.

> AWS가 Kubernetes Control Plane을 Managed 형태로 운영한다.

```text
EKS
├─ Control Plane
│  └─ AWS Managed
└─ Data Plane
   ├─ Node
   ├─ Node
   └─ Node
```

Control Plane의 API Server, Scheduler, Controller Manager, etcd 등을 AWS가 관리한다.

Worker Node에서 실제 Pod가 실행된다.

```text
VPC
 ↓
Private Subnet
 ↓
EC2 Node
 ↓
Pod
```

---

## 5.2 Node Group / Managed Node Group

Node Group:
> 같은 특성의 Worker Node 묶음

```text
EKS
├─ General Node Group
└─ GPU Node Group
```

Node Group별 설정:
- Instance Type
- AMI
- Subnet
- Scaling 범위
- On-Demand / Spot

### Managed Node Group
AWS가 Node Lifecycle 관리의 상당 부분을 도와준다.

```text
EKS
 ↓
Managed Node Group
 ↓
EC2 Auto Scaling Group
 ↓
EC2 Nodes
```

### Scaling
`Min / Desired / Max`를 설정할 수 있다.

하지만 Pod Pending을 보고 실제 Node 증감을 판단하려면 Autoscaler가 필요하다.

```text
Pod Pending
 ↓
Cluster Autoscaler / Karpenter
 ↓
Node Group Scale Out
```

```text
Node Group = 어떤 Node Pool을 운영할지
Autoscaler = 언제 Node를 늘리고 줄일지
```

---

## 5.3 VPC CNI / Pod IP

CNI = Container Network Interface.

EKS의 Amazon VPC CNI는 Pod가 VPC IP를 직접 받을 수 있게 한다.

예:
```text
Subnet 10.0.1.0/24
├─ Node 10.0.1.10
├─ Pod A 10.0.1.21
└─ Pod B 10.0.1.22
```

Pod도 Subnet IP Pool을 소비한다.

따라서:
```text
Pod 증가
 ↓
Subnet IP 소비 증가
 ↓
IP 고갈 가능
```

### Subnet 크기
`/24 = 256개`지만 실제 사용 가능은 251개이고 Node/Pod/ENI 등이 함께 사용한다.

규모가 커질 것 같다면:
- 더 큰 Private Subnet
- 추가 Private Subnet
- 여러 AZ/Subnet으로 Node 분산

을 고려한다.

예:
```text
/24 = 256 주소
/20 = 4096 주소
```

이미 만든 Subnet을 단순히 `/24 → /20`으로 확장하는 방식은 사용할 수 없으므로 초기 CIDR 설계가 중요하다.

---

## 5.4 AWS Load Balancer Controller

> Kubernetes Resource와 AWS Load Balancer를 연결한다.

대표:
```text
Ingress → ALB
Service type=LoadBalancer → NLB
```

Controller가 Kubernetes 리소스를 감시하고 AWS API를 호출해 ALB/NLB, Listener, Target Group 등을 생성/수정한다.

Target은 구성에 따라:
```text
instance target → EC2 Node
ip target → Pod IP
```

### 최종 역할 구분
```text
Kubernetes Service
= Pod Replica의 안정적 Endpoint + L4 분산

ALB
= HTTP/HTTPS L7 Routing

NLB
= TCP/UDP/TLS L4 Routing
```

---

## 5.5 EBS / EFS CSI Driver

CSI = Container Storage Interface.

```text
EBS CSI Driver → EBS
EFS CSI Driver → EFS
```

### EBS CSI
```text
Pod
 ↓
PVC
 ↓
EBS CSI Driver
 ↓
EBS
```

EBS는 AZ 단위이므로 Pod Scheduling에서도 Volume AZ를 고려해야 한다.

### EFS CSI
```text
Pods
 ↓
PVC
 ↓
EFS CSI Driver
 ↓
EFS
```

여러 Pod가 같은 파일시스템을 공유할 때 사용.

정리:
```text
Pod 전용 Disk → EBS
여러 Pod 공유 File System → EFS
Object / Dataset / Model → S3
```

---

## 5.6 ECR

ECR = Elastic Container Registry.

> AWS Managed Container Image Registry

기본 흐름:
```text
Source Code
 ↓
docker build
 ↓
Container Image
 ↓
ECR
 ↓
EKS Node Pull
 ↓
Pod 실행
```

### Repository / Tag
Repository별로 Image를 관리하고 Tag로 버전을 구분한다.

### IAM 인증
EKS Node 또는 관련 AWS Identity에 ECR Image Pull 권한이 필요하다.

### AI Platform
```text
ECR = 실행 코드 / Container Image
S3 = Model Weight / Dataset / Artifact
```

---

## 5.7 Pod Identity / IAM

Pod가 AWS Resource에 접근할 때 Access Key를 직접 저장하지 않고 IAM Role을 사용한다.

```text
Pod
 ↓
IAM Role
 ↓
S3 / SQS / Secrets Manager
```

Node Role만 사용하면 같은 Node의 여러 Pod가 권한을 공유하게 되어 과도한 권한이 생길 수 있다.

### EKS Pod Identity
```text
Pod
 ↓
ServiceAccount
 ↓
EKS Pod Identity
 ↓
IAM Role
 ↓
AWS Resource
```

예:
```text
model-loader → S3 Read Role
api → Secrets Manager Read Role
worker → SQS Consume Role
```

### IRSA
IAM Roles for Service Accounts.

Basic에서는:
```text
IRSA / Pod Identity
= Pod 단위 IAM Role 연결
```

로 이해하면 된다.

### RBAC과 구분
```text
Pod → Kubernetes API = RBAC
Pod → AWS Resource = IAM
```

---

# Chapter 5 전체 구조

```text
                    Internet
                       ↓
                      ALB
                       ↓
                      EKS
          ┌────────────┴────────────┐
          │                         │
   General Node Group         GPU Node Group
          │                         │
         Pods                    vLLM Pods
          │                         │
          └──── Pod Identity ───────┘
                       ↓
                    IAM Role
                 /      |       \
               S3      SQS   Secrets Manager
```

Storage:
```text
PVC
├─ EBS CSI → EBS
└─ EFS CSI → EFS
```

Container Image:
```text
ECR → EKS Node → Pod
```

Network:
```text
VPC
 ↓
Private Subnet
 ↓
EC2 Node
 ↓
VPC CNI
 ↓
Pod IP
```

Traffic:
```text
HTTP/HTTPS → ALB
TCP/UDP → NLB
Pod Replica 내부 접근 → Kubernetes Service
```

---

# Chapter 1~5 최종 요약

## AWS Foundation
```text
Region / AZ
Account / Organizations
IAM / Role / Policy
ARN
```

## Networking
```text
VPC
 ↓
Subnet
 ↓
Route Table
 ↓
IGW / NAT
 ↓
Security Group
```

## Compute
```text
AMI
 ↓
Launch Template
 ↓
ASG
 ↓
EC2
```

외부 트래픽:
```text
ALB / NLB
 ↓
Target Group
 ↓
Application
```

## Storage & Database
```text
EBS = Block
EFS = Shared File
S3 = Object
RDS / Aurora = Relational DB
ElastiCache = Cache
```

## EKS
```text
EKS
├─ Managed Control Plane
├─ Managed Node Group
├─ VPC CNI
├─ AWS Load Balancer Controller
├─ EBS / EFS CSI
├─ ECR
└─ Pod Identity / IAM
```

---

# 현재 진도

완료:
- Chapter 1. AWS Foundation ✅
- Chapter 2. Networking ✅
- Chapter 3. Compute & Load Balancing ✅
- Chapter 4. Storage & Database ✅
- Chapter 5. EKS on AWS ✅

다음:

## Chapter 6. AWS Managed Services
1. SQS
2. SNS
3. MSK
4. KMS
5. Secrets Manager
6. CloudWatch
7. CloudTrail

그 다음:

## Chapter 7. AI/GPU + End-to-End
