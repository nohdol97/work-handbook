---
id: aws-cloud-networking
status: studied
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids:
  - AWSC-02-01
  - AWSC-02-02
  - AWSC-02-03
  - AWSC-02-04
  - AWSC-02-05
  - AWSC-02-06
  - AWSC-02-07
  - AWSC-02-08
  - AWSC-02-09
---

# Chapter 2. Networking

제공된 compact 원문의 순서와 예시를 보존한 학습 기록이다. 실제 AWS 운영 결과가 아니다. **본문 안내:** 뒤의 보완에서 IPv4·예약 IP·NAT 유형·SG 참조의 적용 조건을 확인한다.

<!-- SOURCE CORE START -->

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

<!-- SOURCE CORE END -->

## 보완: 2.2~2.9의 적용 조건

공식 문서 확인일: 2026-10-04.

**2.2 CIDR:** `/24`의 251개는 AWS가 5개 주소를 예약하는 일반 IPv4 subnet 기준이다. BYOIP에는 예외가 있다. CIDR 표의 `/32`, `/0`은 주소 범위 설명이며, VPC IPv4 subnet의 허용 크기는 `/16`~`/28`이다. [AWS subnet 크기](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html).

**2.4~2.6 인터넷 경로:** 원문의 Public IP와 `0.0.0.0/0` 설명은 IPv4 기준이다. Public subnet이어도 리소스의 public IPv4, 라우팅, SG·NACL, 실제 수신 서비스 조건이 충족되어야 통신한다. IPv6는 주소와 `::/0` 경로를 별도로 확인한다. [AWS Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html).

**2.7·2.9 NAT:** Public subnet의 AZ별 NAT는 **public zonal NAT Gateway** 구성이다. 이 경우 각 private subnet에서 같은 AZ의 NAT로 라우팅해야 AZ 간 의존을 줄인다. 현재 regional NAT Gateway도 지원하며 public subnet 없이 구성하고 자동 또는 수동 AZ 모드를 선택한다. Regional 방식은 private NAT를 지원하지 않는다. Private NAT는 IGW를 통한 인터넷 출구가 아니다. Endpoint로 우회하려면 대상 서비스와 필요한 endpoint·DNS·정책을 따로 확인한다. [Regional NAT](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html), [NAT 유형](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html).

**2.8 SG 참조:** 참조는 상대 SG의 규칙을 복사하지 않고 연결된 네트워크 인터페이스의 private IP에 적용된다. 여러 SG를 연결하면 허용 규칙을 합친다. SG의 허용만으로 경로가 만들어지지는 않는다. [AWS SG 규칙](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html).

## LLM 실습: 두 AZ의 private 앱 인터넷 경로 검토

- **상황:** AZ B 앱이 AZ A NAT에 의존하는 구성을 찾는다.
- **LLM에 제공할 맥락:** 가상 VPC의 AZ A/B에 public·private subnet이 있고, 각 AZ의 public zonal NAT가 있다. 두 private subnet의 기본 경로는 모두 NAT A이다.
- **기대 출력:** 정상·AZ A 장애 때의 경로 표와 같은 AZ NAT로 분리하는 변경안.
- **검증 방법:** SG 허용과 라우팅을 구분하고, AZ B를 NAT B로 연결하며 인터넷에서 새 연결을 시작할 수 있다고 주장하지 않는다.
- **주의점:** 라우트·NAT 상태·DNS·SG·NACL을 실제 환경에서 별도로 검증한다. 이 예시는 실행 결과가 아니다.
- **LLM이 틀릴 수 있는 점:** AZ B의 NAT 경로를 확인하지 않고 정상이라고 단정하거나 SG 허용을 라우팅과 혼동할 수 있다.
- **예시 프롬프트:** 아래 두 언어 탭을 사용한다.
- **출처 연결:** 2.4~2.9, AWSC-02-04~09.

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 VPC의 AZ A/B에 public·private subnet과 각 AZ의 public zonal NAT가 있다. 두 private subnet의 0.0.0.0/0 경로는 NAT A이다.
    [요청]
    AZ A 장애가 AZ B 앱의 인터넷 접근에 미치는 영향을 분석하고 같은 AZ NAT를 쓰는 변경안을 제시하라.
    [출력]
    정상/장애 경로 표, 변경할 라우트, 추가 검증 항목을 작성하라.
    [검증]
    라우팅과 SG 허용을 구분하고 NAT B·IGW·DNS·NACL 상태를 가정하지 마라. NAT를 통해 인터넷에서 새 연결을 시작할 수 있다고 쓰지 마라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A fictional VPC has public and private subnets in AZs A and B, with a public zonal NAT in each AZ. Both private subnets route 0.0.0.0/0 to NAT A.
    [Task]
    Analyze how an AZ A outage affects the AZ B app's internet access and propose using each AZ's own NAT.
    [Output]
    Provide a normal/outage path table, routes to change, and additional checks.
    [Checks]
    Distinguish routing from SG permissions; do not assume NAT B, IGW, DNS, or NACL status. Do not claim the internet can initiate new connections through NAT.
    ```
