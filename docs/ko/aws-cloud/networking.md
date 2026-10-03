---
id: aws-cloud-networking
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-02-01
  - AWS-02-02
  - AWS-02-03
  - AWS-02-04
  - AWS-02-05
  - AWS-02-06
  - AWS-02-07
  - AWS-02-08
  - AWS-02-09
---

# Chapter 2. Networking

제공된 AWS Cloud Basic의 학습 원문이다. 번호·순서·예시와 중간 보충 절을 보존했다. 실제 AWS 리소스를 생성하거나 정책·라우팅을 적용한 기록이 아니다. **본문 안내:** 뒤의 **원문 절별 보완과 정정**에서 IPv4 연결 조건, CIDR 예약 주소, public/zonal NAT 전제와 regional NAT, SG 참조, ALB health check 예외를 확인한다.

**절 바로가기:** [2.1 VPC](#21-vpc) · [2.2 Public / Private Subnet](#22-public-private-subnet) · [2.3 Route Table](#23-route-table) · [2.4 Internet Gateway](#24-internet-gateway) · [2.5 NAT Gateway](#25-nat-gateway) · [2.6 Security Group](#26-security-group)

<!-- SOURCE CORE START -->

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

<!-- SOURCE CORE END -->

## 원문 절별 보완과 정정

공식 문서 확인일: 2026-10-03. 원문 IP·도메인·라우트는 설명용이며 실제 대상에 연결하거나 설정을 적용하지 않았다.

### 2.1~2.4 및 Public IP 보충: 라우팅과 연결 조건

원문의 Public IP·NAT 흐름은 주로 IPv4 예다. Public subnet의 기준은 IGW로 가는 route이며 반드시 전체 인터넷 대상 default route여야 하는 것은 아니다. Public IPv4/Elastic IP, route뿐 아니라 SG·NACL·실제 listener도 확인한다. IGW는 IPv4에서 인스턴스의 private 주소와 public 주소를 매핑한다. IPv6는 별도 주소·route 조건으로 검토하며 public IPv4가 필수라고 일반화하지 않는다. [AWS Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)

2.1의 VPC peering은 CIDR 비중복만으로 완성되지 않는다. 양쪽 route와 보안 설정을 확인하고, A–B와 B–C peering이 A–C 전이 연결을 제공한다고 가정하지 않는다. [AWS VPC peering 제한](https://docs.aws.amazon.com/vpc/latest/peering/invalid-peering-configurations.html)

### CIDR 보충: 전체 주소 수와 사용 가능 수

일반 IPv4 subnet의 첫 4개와 마지막 1개 주소는 AWS가 예약하므로 `/24`는 256개 중 251개를 자원에 할당할 수 있다. 표의 `/32`·`/0`은 CIDR 표현·route/규칙 예이며 일반 VPC IPv4 subnet 크기 허용 범위 `/16`~`/28`과 구분한다. BYOIP에는 별도 예약 예외가 있으므로 모든 주소 체계에 5개 예약을 적용하지 않는다. [AWS subnet CIDR](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)

### 2.5: Public·Private와 Zonal·Regional NAT를 구분한다

원문의 public subnet·Elastic IP·AZ별 배치는 **public zonal NAT Gateway** 예다. IPv4 패킷은 먼저 NAT Gateway의 private IP로 변환되고, 인터넷으로 나갈 때 IGW가 그 주소를 Elastic IP로 변환한다. Private NAT는 Elastic IP를 사용하지 않으며 IGW를 통한 인터넷 출구가 아니다. [AWS NAT Gateway 유형](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)

현재는 **regional NAT Gateway**도 지원한다. 호스팅용 public subnet 없이 VPC에 만들며, 자동 모드에서는 workload가 있는 AZ로 확장한다. 수동 모드는 AZ 확장을 직접 관리한다. 현재 private NAT는 지원하지 않으며, 신규 AZ 자동 확장은 즉시 완료된다고 가정하지 않는다. 원문의 AZ별 public zonal 설계와 적용 방식이 다르다. [AWS regional NAT](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html)

Zonal NAT를 여러 AZ가 하나만 공유하면 그 NAT의 AZ 장애가 다른 AZ의 egress에도 영향을 줄 수 있다. 같은 AZ의 NAT를 사용하도록 route까지 확인한다. NAT Gateway 자체에는 SG를 연결할 수 없다. [AWS NAT Gateway 조건](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html)

2.5의 endpoint 우회는 해당 서비스·기능에 필요한 endpoint, route/DNS, 정책이 갖춰진 경우다. 예를 들어 ECR 이미지 pull에는 ECR API/DKR endpoint와 이미지 계층을 위한 S3 경로가 필요할 수 있다. “AWS 서비스이므로 NAT가 전혀 필요 없다”고 일반화하지 않는다. [Amazon ECR VPC endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)

### 2.6: SG 참조와 실제 허용 규칙

여러 SG를 붙이면 허용 규칙이 합쳐진다. 다른 SG를 source로 지정하는 것은 그 SG의 규칙을 복사하는 것이 아니라 연결된 자원의 private IP에서 오는 해당 protocol/port를 허용하는 것이다. 실제 ENI·Pod/Node 대상과 outbound도 확인한다. 원문의 HTTPS 규칙은 TCP 443 허용이며 애플리케이션이 HTTPS를 제공한다는 보장은 아니다. [AWS SG 규칙](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)

### ALB 보충: Health check 예외와 실제 EKS 경로

“200 OK면 정상”은 예시다. 실제 성공 code matcher·연속 성공/실패 횟수·timeout을 확인한다. **Target group의 등록 대상이 모두 unhealthy이면 ALB가 fail open하여 unhealthy 대상에도 요청을 보낼 수 있다.** 따라서 “Unhealthy Target에는 트래픽을 보내지 않는다”를 무조건 보장으로 읽지 않는다. [ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

Ingress→Controller는 설정을 반영하는 제어 흐름이다. ALB 실제 데이터 경로는 instance target이면 NodePort를 거쳐 Pod로, IP target이면 Pod IP로 직접 갈 수 있다. Service가 항상 별도 네트워크 홉이라고 해석하지 않는다. [EKS ALB routing](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

## LLM 실무 활용

### Private subnet의 통신 실패를 경로별로 분리하기

**상황:** 가상 private EKS 서비스에서 이미지 pull과 외부 API 호출이 실패한다. [AWS 기본 구조](foundations.md)의 IAM과 네트워크 원인을 분리해 기존 구성을 검토한다.

**LLM에 줄 맥락:** 비식별 IPv4 CIDR, subnet route 연결, NAT 유형·availability mode·AZ, endpoint/DNS, SG·NACL, 대상 포트·실패 시각·오류. 실제 공인 IP·계정 식별자·토큰은 제외한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 private EKS에서 이미지 pull과 외부 API 호출이 실패한다.
    CIDR·route 연결·NAT type/mode/AZ·endpoint/DNS: [비식별 구성]
    SG·NACL·목적지 포트·실패 시각·오류: [비식별 관측]
    [요청]
    현재 경로를 먼저 검토하고 관측·가정·원인 가설·누락 증거를 구분하라.
    ECR/S3와 외부 API 경로, 네트워크와 IAM 실패를 따로 검토하라.
    [출력]
    경로 / 가설 / 필요한 증거 / 다음 읽기 전용 확인 표를 작성하라.
    Public/private와 zonal/regional NAT 조건, 응답 경로를 표시하라.
    [검증]
    Route 존재나 SG 허용만으로 연결 성공을 단정하지 말라.
    공식 문서와 실제 비식별 설정으로 확인하고 비밀값은 출력하지 말라.
    NAT 생성·route 변경·방화벽 완화는 실행하지 말라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Image pulls and external API calls fail in a hypothetical private EKS environment.
    CIDRs, route associations, NAT type/mode/AZ, endpoints/DNS: [sanitized configuration]
    SGs, NACLs, destination ports, failure times, and errors: [sanitized observations]
    [Task]
    Review the current paths first; separate observations, assumptions, hypotheses, and missing evidence.
    Review ECR/S3 and external API paths separately, and distinguish network from IAM failures.
    [Output]
    Create a table: path / hypothesis / required evidence / next read-only check.
    Mark public/private and zonal/regional NAT conditions and return paths.
    [Checks]
    Do not infer successful connectivity from a route or SG allow rule alone.
    Check official docs and actual sanitized settings; do not output secrets.
    Do not create NAT gateways, change routes, or relax firewall rules.
    ```

**기대 출력:** 이미지 pull과 외부 API의 왕복 경로, NAT·endpoint·DNS·SG·IAM의 구분된 가설, 부족한 근거와 확인 순서.

**LLM이 틀릴 수 있는 부분:** 모든 NAT가 public subnet에 있어야 한다고 가정하거나, SG가 route를 만든다고 보거나, endpoint 하나면 모든 AWS API와 이미지 계층을 처리한다고 단정할 수 있다.

**검증 방법:** 사람이 route association, NAT mode, endpoint 정책·DNS, SG/NACL과 시간대가 맞는 로그를 대조한다. 연결 시험이나 변경은 승인된 시험 환경에서 별도로 수행한다. 이 예시는 실제 장애 해결·모델 응답 기록이 아니다.
