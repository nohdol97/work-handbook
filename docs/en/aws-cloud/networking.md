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

These are supplied AWS Cloud Basic study notes. The numbering, order, examples, and intervening supplements are preserved in translation. They are not a record of creating AWS resources or applying policies or routes. **Reading guide:** The **Supplements and corrections by source section** explain IPv4 connectivity conditions, reserved CIDR addresses, the public/zonal NAT assumptions and regional NAT, SG references, and ALB health-check exceptions.

**Section shortcuts:** [2.1 VPC](#21-vpc) · [2.2 Public / Private Subnet](#22-public-private-subnet) · [2.3 Route Table](#23-route-table) · [2.4 Internet Gateway](#24-internet-gateway) · [2.5 NAT Gateway](#25-nat-gateway) · [2.6 Security Group](#26-security-group)

<!-- SOURCE CORE START -->

## 2.1 VPC

VPC = **Virtual Private Cloud**

> A virtual private network space used within AWS

Structure:

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

### Why is a VPC needed?

It logically separates our service's network within the large shared AWS cloud.

```text
AWS
├─ Company A VPC
├─ Company B VPC
└─ Company C VPC
```

### VPC CIDR

Example:

```text
10.0.0.0/16
```

Approximately:

```text
10.0.0.0
~
10.0.255.255
```

### VPC and subnets

```text
VPC 10.0.0.0/16
│
├─ Subnet A 10.0.1.0/24
├─ Subnet B 10.0.2.0/24
└─ Subnet C 10.0.3.0/24
```

- VPC = A large network
- Subnet = A smaller network carved out of a VPC

### Difference in scope

- VPC = Region scope
- Subnet = Belongs to one AZ

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

A single subnet cannot span multiple AZs.

### Creating a VPC does not create internet connectivity

Separate configuration is required to connect to the internet:

- Internet Gateway
- Route Table
- Public IP and other settings

### Private IP communication within a VPC

```text
App 10.0.1.10
   ↓
Private Network
   ↓
DB 10.0.2.20
```

### Databases are usually not exposed directly to the outside

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

One way to connect different VPCs.

```text
VPC A
   │
   └──── Peering ──── VPC B
```

### Watch for CIDR conflicts

Example:

```text
Dev VPC 10.10.0.0/16
Stage VPC 10.20.0.0/16
Prod VPC 10.30.0.0/16
```

If the VPCs will be connected, plan non-overlapping address ranges.

### Connection to EKS

```text
VPC
 ↓
Subnet
 ↓
EKS Node
 ↓
Pod
```

### Supplementary Q&A: Does a subnet serve the same role as an EKS node?

No.

- Subnet = Network space
- EKS Node = An actual compute server

```text
VPC
└─ Subnet
   └─ EKS Node
      └─ Pod
```

A subnet can contain multiple nodes.

```text
Subnet A
├─ Node 1
├─ Node 2
├─ Node 3
└─ Node 4
```

A node is placed in a specific subnet in a specific AZ.

Analogy:

> A subnet is the land, and an EKS node is a server built on that land.

---

## 2.2 Public / Private Subnet

Key points:

> Public Subnet = A subnet routed for direct internet communication  
> Private Subnet = A subnet configured to prevent direct access from the internet

Public/private is determined by **route table configuration**, not a special subnet type.

### Public Subnet

Typical route:

```text
0.0.0.0/0 → Internet Gateway
```

A public subnet does not automatically expose every resource inside it to the internet.

Direct internet access usually requires:

- IGW Route
- Public IP / Elastic IP
- Security Group permission

These are among the required conditions.

### Private Subnet

There is no direct route to an Internet Gateway.

Example:

```text
10.0.0.0/16 → local
```

Or, if outbound internet access is needed:

```text
0.0.0.0/0 → NAT Gateway
```

### Servers in private subnets can also use the internet

```text
Private Subnet
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
Internet
```

In other words:

- Going from inside to outside: Possible
- Direct internet access into a private resource: Not possible

### Typical placement

Public Subnet:

- ALB
- NAT Gateway
- Bastion Host (if needed)

Private Subnet:

- EKS Node
- EC2 Application
- RDS
- ElastiCache
- MSK

### Multi-AZ structure

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

> A rule table that determines where to send traffic headed to a destination

Example:

```text
Destination        Target
--------------------------------
10.0.0.0/16        local
0.0.0.0/0          igw-xxxx
```

- Destination = Where the traffic is going
- Target = Where to send it

### `10.0.0.0/16 → local`

Traffic to a destination within the same VPC is sent through the VPC's internal network.

### `0.0.0.0/0`

This means all IPv4 addresses.

```text
0.0.0.0/0 → IGW
```

= Send traffic out through the IGW when there is no more specific route.

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

Example:

```text
10.0.0.0/16  → local
10.10.0.0/16 → peering
0.0.0.0/0    → IGW
```

Choose the CIDR route that most specifically matches the destination.

### Route Table vs Security Group

```text
Route Table
= Where to go

Security Group
= Whether it is allowed
```

---

# Detailed CIDR supplement

CIDR = **Classless Inter-Domain Routing**

> A way to express IP address ranges

Example:

```text
10.0.0.0/24
```

= `10.0.0.0 ~ 10.0.0.255`

### Meaning of `/24`

IPv4 = 32bit.

`/24` means that the first 24 bits are fixed as the network address.

The remaining 8 bits:

```text
2^8 = 256
```

A `/24` therefore covers a total of 256 IPv4 addresses.

### `/16`

```text
10.0.0.0/16
```

The remaining 16 bits:

```text
2^16 = 65,536
```

Range:

```text
10.0.0.0
~
10.0.255.255
```

### A shorter prefix means a larger range

```text
/16 → Large
/20
/24
/28
/32 → Very small
```

### Common CIDRs

| CIDR | Total addresses |
|---|---:|
| `/16` | 65,536 |
| `/20` | 4,096 |
| `/24` | 256 |
| `/28` | 16 |
| `/32` | 1 |
| `/0` | All IPv4 addresses |

### `0.0.0.0/0`

With 0 fixed bits, it matches every IPv4 address.

### `/32`

This means exactly one IP address.

Example:

```text
203.0.113.10/32
```

It can be used to allow one specific administrator IP address.

### VPC / Subnet CIDR

```text
VPC 10.0.0.0/16
│
├─ Public A  10.0.1.0/24
├─ Public B  10.0.2.0/24
├─ Private A 10.0.11.0/24
└─ Private B 10.0.12.0/24
```

The subnet CIDR must be contained within the VPC CIDR.

### CIDR overlap

Subnet CIDRs in the same VPC cannot overlap.

Example:

```text
10.0.1.0/24
10.0.1.128/25
```

These overlap.

### Subnet masks and CIDR

```text
255.255.0.0     = /16
255.255.255.0   = /24
255.255.255.255 = /32
```

### AWS subnet reserved IPs

AWS reserves some IP addresses in each subnet.

For example, a `/24` theoretically contains 256 addresses, but AWS reserves 5, leaving fewer usable addresses.

In EKS in particular, Pods can also use VPC IP addresses, so subnet IP exhaustion must be considered.

### EKS and CIDR

With the AWS VPC CNI, Pods can receive VPC IP addresses directly.

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

An undersized subnet can run out of IP addresses as the number of Pods grows.

---

# Public IP / Private IP supplement

## Public IP

An address routable across the internet.

Example:

```text
3.34.100.20
8.8.8.8
```

## Private IP

An address used only within private networks. It is not routed directly over the internet.

Common private IPv4 ranges:

| Private IP range | CIDR |
|---|---|
| `10.0.0.0 ~ 10.255.255.255` | `10.0.0.0/8` |
| `172.16.0.0 ~ 172.31.255.255` | `172.16.0.0/12` |
| `192.168.0.0 ~ 192.168.255.255` | `192.168.0.0/16` |

`10.0.0.0/16`, commonly used in AWS VPCs, is also a private range.

```text
EC2
Private IP: 10.0.1.10
      ↓
IGW or NAT
      ↓
Public IP
      ↓
Internet
```

Key points:

- Private IP = Internal communication
- Public IP = Internet communication

---

## 2.4 Internet Gateway

IGW = **Internet Gateway**

> A gateway connecting a VPC to the internet

```text
Internet
   │
  IGW
   │
  VPC
```

Attaching an IGW does not automatically complete internet connectivity.

### An IGW belongs to a VPC

It attaches to a VPC, not to a specific subnet.

### Public Subnet

```text
0.0.0.0/0 → IGW
```

A route is required to use the IGW.

### External access

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

A public EC2 instance usually needs the following for internet communication:

1. Attach an IGW to the VPC
2. Subnet Route: `0.0.0.0/0 → IGW`
3. Assign a public IP to EC2
4. Allow the traffic in the Security Group

### Public and private IP mapping

EC2 uses a private IP by default and can communicate with the internet through a public IP.

For a basic understanding:

> A resource with a public IP communicates with the internet through an IGW

This is a useful starting point.

### Private subnets do not use an IGW directly

A private subnet usually uses:

```text
0.0.0.0/0 → NAT Gateway
```

This is its default route.

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

### IGWs are not created separately for every AZ

Typically, one IGW attaches to a VPC and multiple public subnets share it.

---

## 2.5 NAT Gateway

NAT Gateway:

> An exit that lets resources in private subnets access the internet

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

It translates a private IP into a public IP to send outbound requests.

Example:

```text
10.0.11.20
   ↓
NAT
   ↓
Public IP
```

### Outbound only

```text
Private EC2 → Internet
✅

Internet → Initiate directly to private EC2
❌
```

### NAT Gateway placement

It is usually placed in a **public subnet**.

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

A NAT Gateway usually uses an Elastic IP.

```text
Private EC2 10.0.11.20
   ↓
NAT Gateway Public IP
   ↓
Internet
```

External systems see the NAT Gateway's public IP.

### Multi-AZ

Consider NAT Gateways in each AZ for production.

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

### EKS and NAT

Private EKS nodes can use a NAT Gateway to access external APIs and download packages and images.

For AWS services, however, VPC endpoints can bypass NAT.

Example:

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

> A virtual firewall attached to AWS resources

Main checks:

- Protocol
- Port
- Source / Destination

Example:

```text
TCP 443
Source: 0.0.0.0/0
```

= Allow HTTPS from all IPv4 addresses

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
Internet / other AWS resources
```

### Route Table vs SG

```text
Route Table
= Where to send traffic

Security Group
= Whether to allow communication
```

### Stateful

Security Groups are stateful.

Response traffic for an allowed connection is automatically permitted.

### Web server example

```text
Inbound
HTTP  80  0.0.0.0/0
HTTPS 443 0.0.0.0/0
```

SSH is usually restricted to a specific administrator IP instead of being open to everyone.

```text
SSH 22 203.0.113.10/32
```

### DB SG

PostgreSQL:

```text
5432 ← APP-SG
```

Allow only the application's Security Group in this way.

### Allowing SG-to-SG traffic

```text
ALB-SG
Inbound 443 ← 0.0.0.0/0

APP-SG
Inbound 8080 ← ALB-SG

DB-SG
Inbound 5432 ← APP-SG
```

This makes operations easier even when server IPs increase in number or change.

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

Security Groups are based on Allow rules.

- Traffic matching an allow rule passes
- Traffic with no matching rule is blocked

There are no explicit Deny rules.

### SG vs NACL

| | Security Group | NACL |
|---|---|---|
| Scope | Resource/ENI | Subnet |
| State | Stateful | Stateless |
| Allow | Supported | Supported |
| Deny | No explicit Deny | Supported |

---

# ALB supplement

ALB = **Application Load Balancer**

> An L7 load balancer that distributes user requests across multiple servers or Pods

```text
Internet
   ↓
  ALB
 ↙   ↘
App1 App2
```

### Main responsibilities

- Load balancing
- Excluding failed servers
- Using multiple AZs
- Handling HTTPS
- URL/host-based routing

### L7 Load Balancer

It understands HTTP/HTTPS content.

Example:

```text
/api/* → API Server
/web/* → Web Server
```

Host-based routing:

```text
api.example.com → API
www.example.com → Web
```

### Listener

Defines which protocol/port receives requests.

```text
Listener 80
Listener 443
```

### Target Group

A group of backends that receive actual requests.

```text
ALB
 ↓
Target Group
 ├─ EC2 A
 ├─ EC2 B
 └─ EC2 C
```

### Health Check

Example:

```text
GET /health
```

200 OK means healthy.

Traffic is not sent to unhealthy targets.

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

An ALB can handle HTTPS termination.

```text
User
 ↓ HTTPS
ALB
 ↓ HTTP or HTTPS
Application
```

Certificates are usually integrated with ACM.

### EKS and ALB

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

| Item | ALB | NLB |
|---|---|---|
| Layer | L7 | L4 |
| Understands HTTP/HTTPS | O | X |
| Path Routing | O | X |
| Host Routing | O | X |
| TCP/UDP | Limited | Strength |
| Typical use | Web/API | TCP/UDP, high-performance networking |

---

<!-- SOURCE CORE END -->

## Supplements and corrections by source section

Official documentation checked on 2026-10-03. The source IPs, domains, and routes are illustrative; no connections were made to those targets and no settings were applied.

### 2.1–2.4 and the public IP supplement: Routing and connectivity conditions

The source's public IP and NAT flows mainly illustrate IPv4. A public subnet has a route to an IGW; this need not be a default route covering the entire internet. Check public IPv4/Elastic IP and routes, as well as SGs, NACLs, and actual listeners. For IPv4, an IGW maps the instance's private address to its public address. Review IPv6 addresses and routes separately; do not generalize that a public IPv4 address is mandatory. [AWS Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)

Non-overlapping CIDRs alone do not complete VPC peering in 2.1. Check routes and security settings on both sides. Do not assume that A–B and B–C peering provide transitive A–C connectivity. [AWS VPC peering limitations](https://docs.aws.amazon.com/vpc/latest/peering/invalid-peering-configurations.html)

### CIDR supplement: Total and usable addresses

AWS reserves the first 4 and last 1 addresses in an ordinary IPv4 subnet, leaving 251 of a `/24`'s 256 addresses assignable to resources. The table's `/32` and `/0` illustrate CIDR notation and routes/rules; distinguish these from the `/16`–`/28` size range allowed for ordinary VPC IPv4 subnets. BYOIP has separate reservation exceptions, so do not apply the 5-address rule to every addressing scheme. [AWS subnet CIDRs](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)

### 2.5: Distinguish public/private from zonal/regional NAT

The source's public-subnet, Elastic-IP, and per-AZ placement illustrates a **public zonal NAT Gateway**. IPv4 packets are first translated to the NAT Gateway's private IP; the IGW then translates this to the Elastic IP for internet access. Private NAT does not use an Elastic IP and is not an internet exit through an IGW. [AWS NAT Gateway types](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)

**Regional NAT Gateways** are now supported too. They are created in a VPC without a hosting public subnet; automatic mode expands to AZs with workloads. In manual mode, you manage AZ expansion yourself. Private NAT is currently unsupported, and automatic expansion to a new AZ should not be assumed instantaneous. This differs from the source's per-AZ public zonal design. [AWS regional NAT](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html)

If several AZs share one zonal NAT Gateway, failure of its AZ can affect egress from the other AZs. Check routes so workloads use the NAT in their own AZ. A Security Group cannot be attached to the NAT Gateway itself. [AWS NAT Gateway conditions](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html)

The endpoint bypass in 2.5 requires the endpoints, routes/DNS, and policies needed by the service and feature. For example, ECR image pulls may require ECR API/DKR endpoints and an S3 path for image layers. Do not generalize that using an AWS service removes every need for NAT. [Amazon ECR VPC endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)

### 2.6: SG references and actual allow rules

Allow rules are combined when multiple SGs are attached. Referencing another SG as a source does not copy its rules; it allows the specified protocol/port from associated resources' private IPs. Check actual ENI and Pod/node targets, and outbound rules too. The source's HTTPS rule allows TCP 443; it does not guarantee that the application serves HTTPS. [AWS SG rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)

### ALB supplement: Health-check exceptions and actual EKS paths

“200 OK means healthy” is an example. Check the configured success-code matcher, consecutive success/failure thresholds, and timeout. **If every registered target in a target group is unhealthy, ALB can fail open and send requests to unhealthy targets too.** Do not read “Traffic is not sent to unhealthy targets” as an unconditional guarantee. [ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

Ingress-to-controller describes the control flow that applies configuration. The ALB data path may go through NodePort to Pods with instance targets, or directly to Pod IPs with IP targets. Do not interpret the Service as always being a separate network hop. [EKS ALB routing](https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html)

## LLM in Practice

### Separate communication failures by path in a private subnet

**Situation:** Image pulls and external API calls fail in a hypothetical private EKS service. Review the existing configuration and separate IAM causes from network causes using [AWS foundations](foundations.md).

**Context to Give the LLM:** Sanitized IPv4 CIDRs, subnet route associations, NAT type/availability mode/AZ, endpoints/DNS, SGs/NACLs, destination ports, failure times, and errors. Exclude actual public IPs, account identifiers, and tokens.

**Example Prompt:**

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

**Expected Output:** Round-trip paths for image pulls and external APIs; separate hypotheses for NAT, endpoints, DNS, SGs, and IAM; missing evidence and an ordered set of checks.

**What the LLM Can Get Wrong:** It may assume every NAT must reside in a public subnet, treat an SG as creating a route, or assume one endpoint handles every AWS API and image layer.

**How to Validate:** A person compares route associations, NAT mode, endpoint policies/DNS, SGs/NACLs, and time-aligned logs. Run connectivity tests or changes separately in an approved test environment. This is not a record of actual incident resolution or model responses.
