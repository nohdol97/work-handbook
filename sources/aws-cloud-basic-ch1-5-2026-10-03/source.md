<!-- 반입 기록
범위: AWS Cloud Basic 1~5장·전체 커리큘럼·보충 질문·통합 구조·학습 현황
한계: 개념 학습 자료이며 실제 AWS 리소스 생성·요금 확인·장애 시험 결과가 아니다.
원본 bytes: 48720; SHA-256: 0df46aa97572c214c47f72b7881cf921da5a5a16111218680ae1a3296b44c25f
정규화: 없음. 원문의 hard break와 모든 byte를 경계 뒤에 그대로 보존한다.
whitespace_restoration: []
-->
<!-- ORIGINAL SOURCE START -->
# AWS Cloud Basic — Source Markdown

> 이 문서는 현재 세션에서 학습한 내용을 기준으로 정리한 source markdown이다.  
> 범위: Chapter 1 ~ Chapter 5 완료분 + 중간 보충 질문/답변  
> 목적: 이후 문서화, 핸드북 작성, 복습 자료의 원본으로 사용

---

# 전체 커리큘럼

1. AWS 기본 구조
   - Region / Availability Zone
   - AWS Account
   - IAM 기본
2. Networking
   - VPC
   - Public / Private Subnet
   - Route Table
   - Internet Gateway
   - NAT Gateway
   - Security Group
   - 보충: CIDR
   - 보충: Public IP / Private IP
   - 보충: ALB
3. Compute
   - EC2
   - Auto Scaling
   - Load Balancer
4. Storage
   - EBS
   - S3
   - EFS
5. Database / Cache
   - RDS
   - Aurora
   - ElastiCache
6. Kubernetes on AWS
   - EKS
   - Node Group
   - Managed Node Group
   - AWS Load Balancer Controller
   - EBS CSI
7. Messaging
   - MSK
   - SQS / SNS 기본
8. Security
   - IAM Role
   - IRSA / Pod Identity
   - KMS
   - Secrets Manager
9. Observability
   - CloudWatch
   - CloudTrail
10. IaC
   - Terraform on AWS
11. AI / GPU Infrastructure
   - GPU EC2
   - EKS GPU Node
   - ECR
   - S3 Model Storage
12. End-to-End Architecture
   - VPC
   - EKS
   - ALB
   - RDS
   - ElastiCache
   - MSK
   - S3
   - GPU Node
   - Terraform

---

# Chapter 1. AWS 기본 구조

## 1.1 Region / Availability Zone

AWS를 이해할 때 가장 먼저 잡아야 하는 개념은 Region과 Availability Zone(AZ)이다.

- **Region**: AWS가 운영하는 큰 지리적 영역
- **AZ**: Region 안에 있는 서로 분리된 장애 영역

서울 Region 예:

```text
Region
ap-northeast-2
```

그 안에는 여러 AZ가 있다.

```text
ap-northeast-2a
ap-northeast-2b
ap-northeast-2c
ap-northeast-2d
```

구조:

```text
AWS
│
├─ Seoul Region (ap-northeast-2)
│   ├─ AZ A
│   ├─ AZ B
│   ├─ AZ C
│   └─ AZ D
│
├─ Tokyo Region
└─ Virginia Region
```

### Region은 왜 필요한가?

사용자와 서버 사이의 거리, 데이터 규제, 서비스 지원 여부, 비용 등을 고려해 Region을 선택한다.

예를 들어 한국 사용자를 대상으로 서비스한다면 일반적으로 서울 Region을 고려한다.

```text
Seoul Region
ap-northeast-2
```

Region 선택 시 주요 기준:

- 사용자와의 거리
- 데이터 저장 위치 / 규제
- 서비스 지원 여부
- 비용

### AZ는 왜 필요한가?

한 데이터센터에 모든 서비스를 몰아넣으면 해당 데이터센터 장애 시 전체 서비스가 중단될 수 있다.

그래서 AWS는 Region 내부를 여러 AZ로 나눠 장애 영역을 분리한다.

```text
Seoul Region
│
├─ AZ A
│   └─ Server A
├─ AZ B
│   └─ Server B
└─ AZ C
    └─ Server C
```

하나의 AZ에 장애가 나더라도 다른 AZ에서 계속 서비스를 제공할 수 있다.

이를 **Multi-AZ Architecture**라고 한다.

### Region과 AZ 차이

| 개념 | 의미 |
|---|---|
| Region | 큰 지리적 AWS 운영 영역 |
| AZ | Region 내부의 독립된 장애 영역 |
| 예시 Region | `ap-northeast-2` |
| 예시 AZ | `ap-northeast-2a` |
| 주 목적 | 지역 선택 |
| AZ 주 목적 | 고가용성 |

중요:

```text
Region 장애 대응
≠
AZ 장애 대응
```

Multi-AZ는 Region 내부의 AZ 장애 대응이다.

### 실무 배치

좋지 않은 구조:

```text
AZ A

EC2
 ↓
EC2
 ↓
Database
```

AZ A 장애 시 전체 서비스 장애.

일반적인 구조:

```text
              Internet
                 │
                ALB
              /     \
           AZ A      AZ B
            │          │
          EC2        EC2
             \        /
              \      /
               RDS
            Multi-AZ
```

### Kubernetes와 연결

```text
EKS Cluster

AZ A
 └ Node

AZ B
 └ Node

AZ C
 └ Node
```

즉 Kubernetes의 고가용성을 AWS의 Multi-AZ 기반 위에서 구현할 수 있다.

### AZ = 데이터센터 하나인가?

정확히는 아니다.

AZ는 하나 이상의 물리적 데이터센터로 구성될 수 있는 **독립된 장애 영역**으로 이해하면 된다.

핵심:

```text
Region
= 큰 지리적 영역

AZ
= Region 내부의 독립된 장애 영역

실무 기본
= Single Region + Multi-AZ
```

---

## 1.2 AWS Account

AWS Account는 단순 로그인 계정이 아니라 **리소스, 비용, 권한을 나누는 큰 관리 경계**다.

```text
AWS Account
│
├─ EC2
├─ S3
├─ RDS
├─ EKS
└─ IAM
```

### 환경을 Account로 분리

하나의 Account에 Dev/Prod를 모두 넣을 수도 있지만 운영 실수 위험이 커질 수 있다.

```text
AWS Organization
│
├─ Dev Account
├─ Staging Account
└─ Production Account
```

즉:

> Account separation = 큰 단위의 격리

### Account와 Region의 차이

하나의 AWS Account에서 여러 Region을 사용할 수 있다.

```text
AWS Account
│
├─ Seoul Region
├─ Tokyo Region
└─ Virginia Region
```

정리:

```text
Account
= 관리 / 권한 / 비용 경계

Region
= 지리적 배치 영역
```

### Account ID

AWS Account에는 12자리 고유 Account ID가 있다.

예:

```text
123456789012
```

ARN 예:

```text
arn:aws:iam::123456789012:role/MyRole
```

### Root User

Root User는 Account의 최상위 사용자다.

```text
AWS Account
   │
 Root User
```

실무에서는 평소 운영에 Root User를 쓰지 않는 것이 기본이다.

```text
Root User
→ 초기 설정 / 매우 제한된 작업

IAM / SSO
→ 평소 운영
```

### IAM User와 Account

```text
AWS Account
│
├─ IAM User A
├─ IAM User B
└─ IAM Role
```

비유:

```text
회사 = AWS Account
직원 계정 = IAM User
직책 / 임시 권한 = IAM Role
```

### AWS Organizations

여러 Account를 중앙에서 관리할 수 있다.

```text
AWS Organizations
│
├─ Management Account
├─ Dev Account
├─ Prod Account
├─ Security Account
└─ Data Account
```

### OU

Organizational Unit.

Account들의 그룹/폴더.

```text
AWS Organization
│
├─ Production OU
│   ├─ AI Platform Prod
│   └─ Data Platform Prod
│
└─ Non-Production OU
    ├─ Dev
    └─ Test
```

### SCP

Service Control Policy.

조직 차원에서 Account/OU가 가질 수 있는 권한의 **최대 범위**를 제한한다.

```text
IAM Policy
= 실제 권한 부여

SCP
= 조직 차원의 최대 허용 범위 제한
```

SCP 자체가 권한을 부여하는 것은 아니다.

### 비용 분리

Account별로 비용을 보기 쉬워진다.

```text
Dev Account       $1,000
Prod Account      $10,000
Data Account      $5,000
AI Account        $20,000
```

### 정리

```text
AWS Organization
        │
      Account
        │
      Region
        │
        AZ
        │
     Resources
```

정확히는 Account 하나가 여러 Region을 사용할 수 있다.

핵심:

- AWS Account = 리소스 / 비용 / 권한의 큰 관리 경계
- Root User = Account의 최상위 사용자
- AWS Organizations = 여러 Account 중앙 관리
- 실무에서는 Dev / Prod 등을 Account 단위로 분리하는 경우가 많다

---

## 1.3 IAM 기본

IAM = **Identity and Access Management**

> 누가, 어떤 AWS 리소스에, 무엇을 할 수 있는가를 관리하는 시스템

핵심 요소:

```text
IAM User
IAM Role
IAM Policy
```

의미:

```text
User
= 사람 또는 고정 사용자

Role
= 필요할 때 맡는 권한

Policy
= 어떤 행동을 허용/거부할지 정의
```

### IAM User

AWS Account 내부의 사용자.

기업 환경에서는 사람에게 장기 Access Key를 주는 방식보다 SSO / IAM Identity Center + Role을 더 많이 고려한다.

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

의미:

- Effect = Allow
- Action = S3 객체 읽기
- Resource = 특정 Bucket 내부 객체

핵심 필드:

```text
Effect
Action
Resource
Condition
```

### IAM Role

Role은 특정 사용자에 고정된 계정이 아니라 **권한 묶음**이다.

```text
User
  ↓
Assume Role
  ↓
AdminRole
  ↓
관리자 권한
```

### 왜 Role이 필요한가?

나쁜 구조:

```text
EC2
└─ Access Key 저장
```

좋은 구조:

```text
EC2
 ↓
IAM Role
 ↓
S3
```

고정 Access Key를 애플리케이션에 저장하지 않아도 된다.

### Temporary Credential

Role을 사용하면 임시 자격 증명을 받을 수 있다.

```text
Application
    ↓
IAM Role
    ↓
Temporary Credential
    ↓
AWS API
```

일반적으로 포함:

- Access Key
- Secret Key
- Session Token
- Expiration

### EC2 + IAM Role

```text
EC2
 │
 └─ IAM Role
      │
      └─ Policy
           └─ s3:GetObject
```

애플리케이션은 AWS SDK를 통해 Role 기반 임시 Credential을 사용할 수 있다.

### EKS에서는?

Pod가 S3에 접근한다면:

```text
Pod
 ↓
IAM Role
 ↓
S3
```

이를 위해 IRSA 또는 EKS Pod Identity를 사용할 수 있다.

### Trust Policy

Role에는 두 종류의 관점이 있다.

```text
Role
│
├─ Permission Policy
│    └─ 이 Role이 무엇을 할 수 있는가
│
└─ Trust Policy
     └─ 누가 이 Role을 맡을 수 있는가
```

### Least Privilege

필요한 최소 권한만 부여한다.

나쁜 예:

```text
s3:*
Resource: *
```

좋은 예:

```text
s3:GetObject
Resource: my-bucket/*
```

### Allow와 Deny

기본적으로 권한이 없으면 Deny.

명시적인 Deny가 있으면 Allow보다 우선한다.

```text
Explicit Deny
> Allow
```

### 사람 / 서비스 권한 구조

사람:

```text
Developer
    ↓
SSO / Identity Center
    ↓
IAM Role
    ↓
AWS Resource
```

EC2:

```text
EC2
 ↓
IAM Role
 ↓
S3 / DynamoDB / etc
```

EKS Pod:

```text
Pod
 ↓
Pod Identity / IRSA
 ↓
IAM Role
 ↓
AWS Resource
```

### IAM과 Kubernetes RBAC

```text
Pod → Kubernetes API 접근
= Kubernetes RBAC

Pod → S3 접근
= AWS IAM
```

즉:

```text
Kubernetes 내부 권한
= RBAC

AWS 리소스 권한
= IAM
```

---

# Chapter 2. Networking

## 2.1 VPC

VPC = **Virtual Private Cloud**

> AWS 안에서 사용하는 가상의 사설 네트워크 공간

구조:

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

### 왜 VPC가 필요한가?

AWS라는 거대한 공유 Cloud 안에서 우리 서비스의 네트워크를 논리적으로 분리하기 위해 사용한다.

```text
AWS
├─ Company A VPC
├─ Company B VPC
└─ Company C VPC
```

### VPC CIDR

예:

```text
10.0.0.0/16
```

대략:

```text
10.0.0.0
~
10.0.255.255
```

### VPC와 Subnet

```text
VPC 10.0.0.0/16
│
├─ Subnet A 10.0.1.0/24
├─ Subnet B 10.0.2.0/24
└─ Subnet C 10.0.3.0/24
```

- VPC = 큰 네트워크
- Subnet = VPC를 나눈 작은 네트워크

### 범위 차이

- VPC = Region 범위
- Subnet = 하나의 AZ에 속함

```text
VPC
│
├─ AZ A
│   └─ Subnet A
├─ AZ B
│   └─ Subnet B
└─ AZ C
    └─ Subnet C
```

Subnet 하나가 여러 AZ에 걸칠 수는 없다.

### VPC 생성 = 인터넷 연결이 아니다

인터넷에 연결하려면 별도의 구성 필요:

- Internet Gateway
- Route Table
- Public IP 등

### VPC 내부 Private IP 통신

```text
App 10.0.1.10
   ↓
Private Network
   ↓
DB 10.0.2.20
```

### DB는 보통 외부에 직접 노출하지 않는다

```text
Internet
   ↓
ALB
   ↓
Application
   ↓
RDS
```

### VPC Peering

서로 다른 VPC끼리 연결하는 방법 중 하나.

```text
VPC A
   │
   └──── Peering ──── VPC B
```

### CIDR 충돌 주의

예:

```text
Dev VPC 10.10.0.0/16
Stage VPC 10.20.0.0/16
Prod VPC 10.30.0.0/16
```

서로 연결할 계획이 있다면 대역을 겹치지 않게 설계한다.

### EKS와 연결

```text
VPC
 ↓
Subnet
 ↓
EKS Node
 ↓
Pod
```

### 보충 Q&A: Subnet이 EKS Node 같은 역할인가?

아니다.

- Subnet = 네트워크 공간
- EKS Node = 실제 컴퓨팅 서버

```text
VPC
└─ Subnet
   └─ EKS Node
      └─ Pod
```

하나의 Subnet 안에 여러 Node가 존재할 수 있다.

```text
Subnet A
├─ Node 1
├─ Node 2
├─ Node 3
└─ Node 4
```

하나의 Node는 특정 AZ의 특정 Subnet에 배치된다.

비유:

> Subnet은 땅이고, EKS Node는 그 땅 위에 세우는 서버다.

---

## 2.2 Public / Private Subnet

핵심:

> Public Subnet = 인터넷과 직접 통신할 수 있도록 라우팅된 Subnet  
> Private Subnet = 인터넷에서 직접 들어올 수 없도록 구성한 Subnet

Public/Private는 특별한 Subnet 타입이 아니라 **Route Table 구성**으로 결정된다.

### Public Subnet

대표 Route:

```text
0.0.0.0/0 → Internet Gateway
```

Public Subnet이라고 해서 안의 모든 리소스가 자동으로 인터넷에 노출되는 것은 아니다.

직접 인터넷 접근을 위해서는 보통:

- IGW Route
- Public IP / Elastic IP
- Security Group 허용

등이 필요하다.

### Private Subnet

Internet Gateway로 직접 가는 Route가 없다.

예:

```text
10.0.0.0/16 → local
```

또는 Outbound Internet이 필요하다면:

```text
0.0.0.0/0 → NAT Gateway
```

### Private Subnet 서버도 인터넷 사용 가능

```text
Private Subnet
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
Internet
```

즉:

- 내부에서 외부로 나감: 가능
- 인터넷에서 Private Resource로 직접 들어옴: 불가

### 대표 배치

Public Subnet:

- ALB
- NAT Gateway
- Bastion Host(필요 시)

Private Subnet:

- EKS Node
- EC2 Application
- RDS
- ElastiCache
- MSK

### Multi-AZ 구조

```text
VPC
│
├─ AZ A
│   ├─ Public Subnet A
│   └─ Private Subnet A
├─ AZ B
│   ├─ Public Subnet B
│   └─ Private Subnet B
└─ AZ C
    ├─ Public Subnet C
    └─ Private Subnet C
```

---

## 2.3 Route Table

Route Table:

> 목적지로 갈 때 어디로 보내야 하는지 정하는 규칙표

예:

```text
Destination        Target
--------------------------------
10.0.0.0/16        local
0.0.0.0/0          igw-xxxx
```

- Destination = 어디로 가려는가
- Target = 어디로 보낼 것인가

### `10.0.0.0/16 → local`

같은 VPC 내부 목적지라면 VPC 내부 네트워크로 보낸다.

### `0.0.0.0/0`

모든 IPv4 주소를 의미한다.

```text
0.0.0.0/0 → IGW
```

= 더 구체적인 Route가 없으면 외부로 IGW를 통해 보낸다.

### Public Route Table

```text
10.0.0.0/16 → local
0.0.0.0/0   → IGW
```

### Private Route Table

```text
10.0.0.0/16 → local
0.0.0.0/0   → NAT Gateway
```

### Longest Prefix Match

예:

```text
10.0.0.0/16  → local
10.10.0.0/16 → peering
0.0.0.0/0    → IGW
```

목적지와 가장 구체적으로 맞는 CIDR Route를 선택한다.

### Route Table vs Security Group

```text
Route Table
= 어디로 갈지

Security Group
= 갈 수 있는지
```

---

# CIDR 상세 보충

CIDR = **Classless Inter-Domain Routing**

> IP 주소 범위를 표현하는 방식

예:

```text
10.0.0.0/24
```

= `10.0.0.0 ~ 10.0.0.255`

### `/24` 의미

IPv4 = 32bit.

`/24`는 앞의 24bit를 네트워크 주소로 고정한다는 뜻.

남은 8bit:

```text
2^8 = 256
```

따라서 `/24`는 총 256개 IPv4 주소 범위를 가진다.

### `/16`

```text
10.0.0.0/16
```

남은 16bit:

```text
2^16 = 65,536
```

범위:

```text
10.0.0.0
~
10.0.255.255
```

### Prefix가 작을수록 범위는 크다

```text
/16 → 큼
/20
/24
/28
/32 → 매우 작음
```

### 자주 보는 CIDR

| CIDR | 전체 주소 수 |
|---|---:|
| `/16` | 65,536 |
| `/20` | 4,096 |
| `/24` | 256 |
| `/28` | 16 |
| `/32` | 1 |
| `/0` | 모든 IPv4 |

### `0.0.0.0/0`

고정되는 bit가 0개이므로 모든 IPv4 주소와 매칭된다.

### `/32`

정확히 IP 하나를 의미.

예:

```text
203.0.113.10/32
```

특정 관리자 IP 하나만 허용할 때 사용 가능.

### VPC / Subnet CIDR

```text
VPC 10.0.0.0/16
│
├─ Public A  10.0.1.0/24
├─ Public B  10.0.2.0/24
├─ Private A 10.0.11.0/24
└─ Private B 10.0.12.0/24
```

Subnet CIDR은 VPC CIDR 안에 포함되어야 한다.

### CIDR overlap

같은 VPC 안의 Subnet CIDR은 겹칠 수 없다.

예:

```text
10.0.1.0/24
10.0.1.128/25
```

는 서로 겹친다.

### Subnet Mask와 CIDR

```text
255.255.0.0     = /16
255.255.255.0   = /24
255.255.255.255 = /32
```

### AWS Subnet 예약 IP

AWS는 각 Subnet에서 일부 IP를 예약한다.

예를 들어 `/24`는 이론적으로 256개지만 AWS가 5개 주소를 예약하므로 실제 사용 가능 수는 더 적다.

특히 EKS에서는 Pod도 VPC IP를 사용할 수 있으므로 Subnet IP 고갈을 고려해야 한다.

### EKS와 CIDR

AWS VPC CNI를 사용하면 Pod가 VPC IP를 직접 받을 수 있다.

```text
Private Subnet 10.0.1.0/24
│
├─ Node 1
│   ├─ Pod A → 10.0.1.21
│   └─ Pod B → 10.0.1.22
└─ Node 2
    ├─ Pod C → 10.0.1.23
    └─ Pod D → 10.0.1.24
```

Subnet을 너무 작게 잡으면 Pod 증가 시 IP 부족 문제가 생길 수 있다.

---

# Public IP / Private IP 보충

## Public IP

인터넷 전체에서 라우팅 가능한 주소.

예:

```text
3.34.100.20
8.8.8.8
```

## Private IP

내부 네트워크에서만 쓰는 주소. 인터넷에서 직접 라우팅되지 않는다.

대표적인 IPv4 Private 범위:

| Private IP 범위 | CIDR |
|---|---|
| `10.0.0.0 ~ 10.255.255.255` | `10.0.0.0/8` |
| `172.16.0.0 ~ 172.31.255.255` | `172.16.0.0/12` |
| `192.168.0.0 ~ 192.168.255.255` | `192.168.0.0/16` |

AWS VPC에서 자주 쓰는 `10.0.0.0/16`도 Private 범위다.

```text
EC2
Private IP: 10.0.1.10
      ↓
IGW 또는 NAT
      ↓
Public IP
      ↓
Internet
```

핵심:

- Private IP = 내부 통신용
- Public IP = 인터넷 통신용

---

## 2.4 Internet Gateway

IGW = **Internet Gateway**

> VPC와 인터넷 사이를 연결하는 게이트웨이

```text
Internet
   │
  IGW
   │
  VPC
```

IGW를 붙였다고 인터넷 연결이 자동으로 완성되는 것은 아니다.

### IGW는 VPC 단위

특정 Subnet이 아니라 VPC에 연결된다.

### Public Subnet

```text
0.0.0.0/0 → IGW
```

Route가 있어야 IGW를 사용한다.

### 외부 접근

```text
User
 ↓
Internet
 ↓
IGW
 ↓
VPC
 ↓
Public Subnet
 ↓
EC2
```

Public EC2가 인터넷 통신하려면 보통:

1. VPC에 IGW 연결
2. Subnet Route: `0.0.0.0/0 → IGW`
3. EC2에 Public IP
4. Security Group 허용

### Public IP와 Private IP 매핑

EC2는 Private IP를 기본으로 사용하며 Public IP를 통해 인터넷과 통신할 수 있다.

Basic에서는:

> Public IP를 가진 리소스가 IGW를 통해 인터넷과 통신한다

정도로 이해.

### Private Subnet은 IGW를 직접 쓰지 않는다

Private Subnet은 보통:

```text
0.0.0.0/0 → NAT Gateway
```

를 사용한다.

### ALB + IGW

```text
User
 ↓
Internet
 ↓
IGW
 ↓
Public Subnet
 ↓
ALB
 ↓
Private Subnet
 ↓
EKS Pod
```

### IGW는 AZ별로 여러 개 만들지 않는다

일반적으로 하나의 VPC에 IGW 하나를 연결하고 여러 Public Subnet이 같은 IGW를 사용한다.

---

## 2.5 NAT Gateway

NAT Gateway:

> Private Subnet 안의 리소스가 인터넷으로 나갈 수 있게 해주는 출구

```text
Private Subnet
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
Internet
```

### NAT

Network Address Translation.

Private IP를 Public IP로 변환해 외부로 요청을 보낸다.

예:

```text
10.0.11.20
   ↓
NAT
   ↓
Public IP
```

### Outbound만

```text
Private EC2 → Internet
✅

Internet → Private EC2 직접 시작
❌
```

### NAT Gateway 위치

일반적으로 **Public Subnet**에 둔다.

```text
VPC
│
├─ Public Subnet
│   └─ NAT Gateway
└─ Private Subnet
    └─ EKS Node
```

### Private Route Table

```text
10.0.0.0/16 → local
0.0.0.0/0   → NAT Gateway
```

### NAT Gateway Public IP

NAT Gateway는 보통 Elastic IP를 사용한다.

```text
Private EC2 10.0.11.20
   ↓
NAT Gateway Public IP
   ↓
Internet
```

외부에서는 NAT Gateway의 Public IP가 보인다.

### Multi-AZ

Production에서는 AZ별 NAT Gateway 구성을 고려한다.

```text
AZ A
├─ Public Subnet A
│   └─ NAT Gateway A
└─ Private Subnet A

AZ B
├─ Public Subnet B
│   └─ NAT Gateway B
└─ Private Subnet B
```

### EKS와 NAT

Private EKS Node가 외부 API, 패키지, 이미지를 가져올 때 NAT Gateway를 사용할 수 있다.

다만 AWS 내부 서비스는 VPC Endpoint로 NAT를 우회할 수 있다.

예:

```text
Private EKS
 ↓
VPC Endpoint
 ↓
S3 / ECR
```

---

## 2.6 Security Group

Security Group:

> AWS 리소스 앞에 붙는 가상 방화벽

주로 검사:

- Protocol
- Port
- Source / Destination

예:

```text
TCP 443
Source: 0.0.0.0/0
```

= 모든 IPv4에서 HTTPS 허용

### Inbound / Outbound

Inbound:

```text
Client
  ↓
EC2
```

Outbound:

```text
EC2
 ↓
Internet / 다른 AWS 리소스
```

### Route Table vs SG

```text
Route Table
= 어디로 보낼지

Security Group
= 통신을 허용할지
```

### Stateful

Security Group은 Stateful이다.

허용된 연결의 응답 트래픽은 자동으로 허용된다.

### 웹 서버 예

```text
Inbound
HTTP  80  0.0.0.0/0
HTTPS 443 0.0.0.0/0
```

SSH는 보통 전체 공개 대신 특정 관리자 IP에 제한.

```text
SSH 22 203.0.113.10/32
```

### DB SG

PostgreSQL:

```text
5432 ← APP-SG
```

처럼 Application SG만 허용.

### SG → SG 허용

```text
ALB-SG
Inbound 443 ← 0.0.0.0/0

APP-SG
Inbound 8080 ← ALB-SG

DB-SG
Inbound 5432 ← APP-SG
```

이 방식은 서버 IP가 늘어나거나 바뀌어도 운영이 편하다.

### EKS

```text
Internet
 ↓ 443
ALB-SG
 ↓
ALB
 ↓
APP-SG
 ↓
EKS
 ↓ 5432
DB-SG
 ↓
RDS
```

### Deny Rule

Security Group은 기본적으로 Allow rule 기반이다.

- 허용 규칙에 있으면 통과
- 없으면 차단

명시적 Deny rule은 없다.

### SG vs NACL

| | Security Group | NACL |
|---|---|---|
| 적용 단위 | Resource/ENI | Subnet |
| 상태 | Stateful | Stateless |
| Allow | 가능 | 가능 |
| Deny | 명시적 Deny 없음 | 가능 |

---

# ALB 보충 설명

ALB = **Application Load Balancer**

> 사용자 요청을 여러 서버나 Pod로 나눠 보내는 L7 Load Balancer

```text
Internet
   ↓
  ALB
 ↙   ↘
App1 App2
```

### 핵심 역할

- 부하 분산
- 장애 서버 제외
- 여러 AZ 활용
- HTTPS 처리
- URL/Host 기반 라우팅

### L7 Load Balancer

HTTP/HTTPS 내용을 이해한다.

예:

```text
/api/* → API Server
/web/* → Web Server
```

Host 기반:

```text
api.example.com → API
www.example.com → Web
```

### Listener

어떤 Protocol/Port로 요청을 받을지 정의.

```text
Listener 80
Listener 443
```

### Target Group

실제 요청을 받을 Backend 그룹.

```text
ALB
 ↓
Target Group
 ├─ EC2 A
 ├─ EC2 B
 └─ EC2 C
```

### Health Check

예:

```text
GET /health
```

200 OK면 정상.

Unhealthy Target에는 트래픽을 보내지 않는다.

### Public / Internal ALB

Public ALB:

```text
Internet
 ↓
IGW
 ↓
ALB
 ↓
Private App
```

Internal ALB:

```text
Internal Service
 ↓
Internal ALB
 ↓
Backend
```

### TLS Termination

ALB가 HTTPS 종료를 담당할 수 있다.

```text
User
 ↓ HTTPS
ALB
 ↓ HTTP 또는 HTTPS
Application
```

인증서는 보통 ACM과 연계.

### EKS와 ALB

```text
Ingress
 ↓
AWS Load Balancer Controller
 ↓
ALB
 ↓
Kubernetes Service
 ↓
Pod
```

### ALB vs NLB

| 항목 | ALB | NLB |
|---|---|---|
| Layer | L7 | L4 |
| HTTP/HTTPS 이해 | O | X |
| Path Routing | O | X |
| Host Routing | O | X |
| TCP/UDP | 제한적 | 강점 |
| 대표 용도 | Web/API | TCP/UDP, 고성능 네트워크 |

---

# Chapter 3. Compute

## 3.1 EC2

EC2 = **Elastic Compute Cloud**

> AWS에서 빌려 쓰는 가상 서버

### EC2 구성 시 선택

- AMI
- Instance Type
- VPC
- Subnet
- Security Group
- Storage
- IAM Role

### AMI

Amazon Machine Image.

EC2 생성을 위한 서버 이미지.

```text
AMI
 ↓
EC2 생성
 ↓
운영체제가 설치된 서버
```

AMI와 Docker Image의 차이:

```text
AMI
= VM 전체 이미지

Docker Image
= Container 실행 이미지
```

### Instance Type

CPU, Memory, GPU 등의 서버 사양.

대표 계열:

```text
t = 범용/저비용
m = General Purpose
c = Compute Optimized
r = Memory Optimized
g / p = GPU
```

### EC2는 특정 Subnet에 배치

```text
VPC
└─ Subnet
   └─ EC2
```

Subnet 선택으로 AZ도 결정된다.

### Public EC2 / Private EC2

Public:

```text
Internet
 ↓
IGW
 ↓
Public Subnet
 ↓
EC2
```

Private:

```text
Private Subnet
└─ EC2
```

Private EC2의 외부 접속:

```text
EC2
 ↓
NAT Gateway
 ↓
IGW
 ↓
Internet
```

### Security Group

EC2 앞의 접근 제어.

### EBS

EC2 저장공간으로 보통 EBS를 사용.

```text
EC2
 ↓
EBS Volume
```

### IAM Role

```text
EC2
 ↓
IAM Role
 ↓
S3
```

고정 Access Key 저장을 피할 수 있다.

### User Data

EC2 최초 부팅 시 실행할 초기화 Script.

### Stop / Start / Terminate

- Stop = 전원 끄기
- Start = 다시 켜기
- Terminate = 인스턴스 제거

### Public IP / Elastic IP

Public IP는 변할 수 있다.

고정 Public IPv4가 필요하면 Elastic IP 사용 가능.

현대적인 웹 서비스에서는 EC2 Public IP에 직접 의존하기보다:

```text
DNS
 ↓
ALB
 ↓
EC2 여러 대
```

구조를 많이 사용한다.

### 단일 EC2 문제

Single Point of Failure.

Production에서는 여러 AZ에 여러 EC2를 두는 구성이 일반적.

### EKS Node와 EC2

Managed Node Group을 쓰면 EKS Worker Node의 실체가 EC2인 경우가 많다.

```text
EKS Cluster
   ↓
Node Group
   ↓
EC2
   ↓
Pod
```

### AI/GPU

GPU EC2 위에 vLLM 등을 실행할 수 있다.

---

## 3.2 Auto Scaling

Auto Scaling:

> 트래픽이나 상태에 따라 EC2 개수를 자동으로 늘리거나 줄이는 기능

### Scale Out / Scale In

```text
Scale Out
= 서버 추가

Scale In
= 서버 제거
```

Horizontal Scaling.

Vertical Scaling은 서버 한 대의 사양을 키우는 것.

### Auto Scaling Group(ASG)

```text
Min     = 2
Desired = 3
Max     = 10
```

- Min = 최소 인스턴스 수
- Desired = 유지하려는 인스턴스 수
- Max = 최대 수

### Self Healing

Desired 3인데 한 대가 죽으면 새 EC2를 만들어 3대를 유지한다.

### Launch Template

EC2 생성 설계도.

```text
Launch Template
├─ AMI
├─ Instance Type
├─ Security Group
├─ IAM Role
├─ Storage
└─ User Data
```

### ALB와 결합

```text
ALB
 ↓
Target Group
 ↓
ASG
├─ EC2 A
├─ EC2 B
└─ EC2 C
```

Scale Out된 인스턴스도 Target Group에 등록된다.

### Health Check

불량 인스턴스를 트래픽 대상에서 제외하거나 교체할 수 있다.

### Dynamic Scaling

CloudWatch Metric 기반.

예:

```text
CPU > 70%
→ EC2 증가
```

### Target Tracking

예:

```text
평균 CPU 50% 유지
```

목표에 맞게 자동 증감.

### Scheduled Scaling

정해진 시간에 증감.

### Multi-AZ

ASG를 여러 AZ에 걸쳐 구성해 장애 대응.

### EKS와 연결

EKS에서는 Node 수를 조절하기 위해:

- Managed Node Group
- Auto Scaling Group
- Cluster Autoscaler
- Karpenter

등이 연결될 수 있다.

### Stateless Application

Auto Scaling에서는 EC2가 언제든 생성/삭제되므로 애플리케이션은 Stateless가 유리하다.

```text
Application
= Stateless

State
= RDS / ElastiCache / S3
```

---

## 3.3 Load Balancer

Load Balancer:

> 들어오는 요청을 여러 Backend 서버로 분산

### 핵심 역할

1. 요청 분산
2. Health Check
3. 단일 진입점 제공

### ALB vs NLB

ALB:
- L7
- HTTP/HTTPS
- Path/Host 기반 Routing

NLB:
- L4
- TCP/UDP/TLS
- 고성능 네트워크

### Listener

어떤 Protocol/Port로 요청을 받을지 정의.

### Listener Rule

```text
/api/*   → API Target Group
/admin/* → Admin Target Group
그 외    → Web Target Group
```

### Target Group

Backend 서버 그룹.

### Auto Scaling 연동

새 EC2가 생기면 Target Group에 등록되어 ALB가 트래픽을 분산한다.

### HTTPS / ACM

ALB Listener에서 TLS Termination 가능.

### Public / Internal ALB

둘 다 존재 가능.

### 전체 Compute 구조

```text
Internet
   ↓
  IGW
   ↓
  ALB
   ↓
Target Group
   ↓
Auto Scaling Group
├─ EC2 - AZ A
├─ EC2 - AZ A
├─ EC2 - AZ B
└─ EC2 - AZ B
```

정리:

```text
EC2
= 실제 서버

ASG
= 서버 개수 관리

ALB
= 요청 분산

Target Group
= Backend 묶음

Listener
= 요청 받을 Port/Protocol
```

---

# Chapter 4. Storage

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

# Chapter 5. Database / Cache

## 5.1 RDS

RDS = **Relational Database Service**

> AWS가 많은 운영 작업을 대신해주는 Managed 관계형 DB 서비스

예:

```text
Application
   ↓
RDS PostgreSQL
```

### 대표 DB Engine

- PostgreSQL
- MySQL
- MariaDB
- Oracle
- SQL Server

RDS 자체가 DB Engine이 아니라 여러 DB Engine을 Managed 형태로 제공하는 서비스다.

### EC2 PostgreSQL vs RDS

직접 운영:

```text
EC2
 ↓
PostgreSQL
```

직접 관리:

- OS
- PostgreSQL 설치
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

AWS가 많은 인프라 운영을 담당.

사용자는 주로:

- Schema
- Query
- Index
- Application Connection
- DB Parameter

등에 집중.

### RDS는 보통 Private Subnet

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

RDS가 어느 Subnet/AZ들에 배치될 수 있는지 정의하는 Subnet 목록.

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

Application은 DB IP가 아니라 Endpoint를 사용.

```text
mydb.xxxxxx.ap-northeast-2.rds.amazonaws.com
```

장애조치/인프라 변경 시 실제 DB 인스턴스가 바뀌어도 Endpoint를 통해 접근 가능.

### Multi-AZ

```text
AZ A
└─ Primary RDS

AZ B
└─ Standby RDS
```

Primary 장애 시 Standby로 Failover.

목적:

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

목적:

```text
Read Replica
= Read Scaling
```

### Multi-AZ vs Read Replica

```text
Multi-AZ
→ 장애 대응

Read Replica
→ 읽기 부하 분산
```

### Backup / Snapshot

- Automated Backup
- Point-in-Time Recovery
- Manual Snapshot

### Storage

사용자는 Storage Size, Type, IOPS 등을 설정하지만 EBS를 직접 attach/detach하는 방식은 아니다.

### Scaling

Instance Class 변경을 통한 Vertical Scaling.

Read Replica를 통한 Read Scaling.

### Connection 문제

Pod 수 증가 시 DB Connection도 같이 증가한다.

예:

```text
Pod 100
×
Connection 20
=
2,000 DB Connections
```

Connection Pool 관리가 중요.

필요 시 RDS Proxy도 고려.

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

애플리케이션은 Stateless하게, 영속적 Transactional Data는 RDS에 저장.

### EKS에서 PostgreSQL 직접 운영 vs RDS

직접 운영 시:

- StatefulSet
- PVC
- EBS
- Replication
- Backup
- Failover
- Upgrade
- Operator

등을 직접 운영해야 한다.

RDS 사용 시 운영 부담을 크게 줄일 수 있다.

단, RDS라도 다음은 여전히 신경 써야 한다.

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

Aurora는 AWS가 만든 **클라우드용 관계형 DB 엔진**이다.

RDS 관계:

```text
Amazon RDS
├─ PostgreSQL
├─ MySQL
├─ MariaDB
├─ Oracle
├─ SQL Server
└─ Aurora
```

즉:

> RDS = Managed DB 서비스  
> Aurora = RDS에서 사용할 수 있는 DB Engine 중 하나

### PostgreSQL / MySQL Compatible

- Aurora PostgreSQL-Compatible
- Aurora MySQL-Compatible

AWS가 만든 엔진이지만 PostgreSQL/MySQL 호환 인터페이스를 제공.

### Compute와 Storage 분리

일반 RDS PostgreSQL:

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

핵심 설계:

> 여러 DB Instance가 Shared Distributed Storage Layer를 사용

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

Writer 장애 시 Reader 중 하나를 새로운 Writer로 승격 가능.

애플리케이션은 Cluster Endpoint를 계속 바라본다.

### Multi-AZ

Aurora Storage는 Multi-AZ 고가용성을 강하게 고려한 분산 스토리지 구조를 사용한다.

### Storage 자동 확장

데이터 증가에 따라 Storage Capacity가 자동으로 확장되는 구조를 제공한다.

### Aurora Serverless

사용자가 고정 DB Instance Size를 직접 관리하는 부담을 줄이고 수요에 따라 Compute Capacity를 조절한다.

```text
Provisioned
= 서버 크기 직접 선택

Serverless
= Compute를 탄력적으로 운영
```

### Aurora가 항상 더 좋은 것은 아니다

고려 요소:

- 비용
- 기능 차이
- PostgreSQL 버전 / Extension 호환성
- AWS 종속성
- 운영 복잡도

작고 단순한 서비스는 RDS PostgreSQL로 충분할 수 있다.

규모가 커지고 HA/Read Scaling이 중요하면 Aurora PostgreSQL을 고려할 수 있다.

### Connection Pool 문제

Aurora에서도 DB Connection 관리는 필요하다.

```text
Application
 ↓
Connection Pool
 ↓
RDS Proxy (필요 시)
 ↓
Aurora
```

### RDS PostgreSQL vs Aurora PostgreSQL

| 항목 | RDS PostgreSQL | Aurora PostgreSQL |
|---|---|---|
| DB 엔진 | PostgreSQL | AWS 자체 PostgreSQL-compatible |
| Storage 구조 | Instance 중심 Managed Storage | Shared Distributed Storage |
| HA | Multi-AZ | Multi-AZ 중심 설계 |
| Read Scaling | Read Replica | Aurora Reader |
| Failover | 지원 | Cluster 구조 기반 |
| Storage 확장 | 관리 요소 있음 | 더 자동화됨 |
| 비용/구조 | 상대적으로 단순 | 상대적으로 복잡/비쌀 수 있음 |

---

## 5.3 ElastiCache

ElastiCache:

> AWS가 운영해주는 Managed In-Memory Cache 서비스

Redis 계열 캐시를 AWS Managed 형태로 운영할 수 있다.

### 왜 Cache가 필요한가?

모든 요청이 RDS로 가면 DB 부하가 커진다.

```text
Application
   ↓
ElastiCache
   ↓ Cache Miss
RDS
```

### Cache Aside

조회 흐름:

```text
Application
    ↓
ElastiCache
    ↓
Key 존재?
```

Cache Hit:
- Redis에서 바로 반환

Cache Miss:
1. RDS 조회
2. Redis 저장
3. 사용자 반환

### RDS를 대체하지 않는다

```text
RDS
= Source of Truth

ElastiCache
= 빠른 임시 데이터 / Cache
```

### 대표 용도

- Cache
- Session
- Rate Limit
- Counter
- Leaderboard
- Temporary State

### 직접 Redis 운영 vs ElastiCache

직접 Redis 운영:

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

유사 철학:

```text
PostgreSQL 직접 운영 → RDS
Redis 직접 운영      → ElastiCache
```

### Private Network

보통 VPC Private Network에 둔다.

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

Redis-compatible 서비스는 일반적으로 `6379` 포트를 사용.

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

고가용성과 Read Scaling에 활용.

### Multi-AZ

```text
AZ A
└─ Primary

AZ B
└─ Replica
```

Primary 장애 시 Replica를 승격 가능.

### Sharding

데이터가 한 노드 메모리에 모두 들어가지 않을 때 여러 Shard로 분할.

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
= 같은 데이터 복제
= HA / Read Scaling

Shard
= 데이터 분할
= Capacity / Write Scaling
```

### TTL

```text
user:123
TTL = 600초
```

세션, 캐시, Token, Rate Limit 등에 유용.

### Cache Invalidation

DB 값은 바뀌었지만 Cache에 옛 값이 남아 stale data가 될 수 있다.

따라서:

```text
DB Update
 ↓
Cache Delete / Update
```

또는 TTL을 사용한다.

### Session 저장

여러 Pod가 있는 경우 세션을 Pod Local Memory에 저장하면 문제가 생길 수 있다.

```text
        ElastiCache
        /    |    \
     Pod A Pod B Pod C
```

세션을 외부 저장소로 분리하면 Application을 Stateless하게 유지할 수 있다.

### Auto Scaling과 연결

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

| 항목 | RDS | ElastiCache |
|---|---|---|
| 저장 위치 | Disk 중심 | Memory 중심 |
| 데이터 | 영구 데이터 | 임시/캐시 데이터 |
| 속도 | 상대적으로 느림 | 매우 빠름 |
| 대표 용도 | 사용자/주문/설정 | Cache/Session |
| 원본 데이터 | 주로 O | 보통 X |

### Redis를 무조건 넣어야 하는가?

아니다.

초기 서비스가 RDS만으로 충분하면 Redis를 넣지 않아도 된다.

Redis를 추가하면 다음 복잡성이 생긴다.

- Cache Policy
- TTL
- Invalidation
- Memory 관리
- Failover

따라서 실제 DB 부하나 Latency 문제가 있을 때 도입하는 접근이 좋다.

---

# Chapter 1~5 통합 아키텍처

지금까지 학습한 내용을 하나의 구조로 연결하면 다음과 같다.

```text
AWS Region
│
└─ VPC
   │
   ├─ Internet Gateway
   │
   ├─ AZ A
   │   ├─ Public Subnet A
   │   │   ├─ ALB
   │   │   └─ NAT Gateway A
   │   │
   │   └─ Private Subnet A
   │       ├─ EKS / EC2
   │       ├─ RDS Primary
   │       └─ ElastiCache Primary
   │
   ├─ AZ B
   │   ├─ Public Subnet B
   │   │   ├─ ALB
   │   │   └─ NAT Gateway B
   │   │
   │   └─ Private Subnet B
   │       ├─ EKS / EC2
   │       ├─ RDS Standby
   │       └─ ElastiCache Replica
   │
   └─ S3
       ├─ Dataset
       ├─ Model
       ├─ Backup
       └─ Parquet / Iceberg
```

애플리케이션 요청 흐름:

```text
User
 ↓
Internet
 ↓
IGW
 ↓
ALB
 ↓
EKS / EC2
 ↓
├─ RDS
├─ ElastiCache
└─ S3
```

Private Resource의 외부 Outbound:

```text
EKS / EC2
 ↓
NAT Gateway
 ↓
IGW
 ↓
Internet
```

스토리지 역할:

```text
EBS
= 서버 디스크

EFS
= 공유 파일시스템

S3
= Object Storage

RDS
= 관계형 영구 데이터

ElastiCache
= 빠른 임시 / 캐시 데이터
```

권한/보안:

```text
IAM
= AWS Resource 접근 권한

Security Group
= 네트워크 접근 허용

Route Table
= 트래픽 경로

VPC / Subnet
= 네트워크 배치
```

---

# 현재 학습 진행 상태

완료:

- Chapter 1. AWS 기본 구조 ✅
- Chapter 2. Networking ✅
- Chapter 3. Compute ✅
- Chapter 4. Storage ✅
- Chapter 5. Database / Cache ✅

다음 학습:

## Chapter 6. Kubernetes on AWS

예정 항목:

- EKS
- Node Group
- Managed Node Group
- AWS Load Balancer Controller
- EBS CSI Driver

이후:

- Chapter 7. Messaging
- Chapter 8. Security
- Chapter 9. Observability
- Chapter 10. IaC
- Chapter 11. AI / GPU Infrastructure
- Chapter 12. End-to-End Architecture
