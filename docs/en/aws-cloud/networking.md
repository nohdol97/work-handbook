---
id: aws-cloud-networking
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
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

The configurations are study examples, not results from a running AWS environment.

<!-- SOURCE CORE START -->

## 2.1 VPC

A VPC path works like a road network: check the source, next hop, and destination. An address and an allow rule do not create a route or gateway.

VPC = Virtual Private Cloud.

> A private network space created within AWS

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

A VPC is a Region-scoped resource.

Example:
```text
VPC CIDR
10.0.0.0/16
```

### VPC and subnets
```text
VPC 10.0.0.0/16
├─ Subnet A 10.0.1.0/24
├─ Subnet B 10.0.2.0/24
└─ Subnet C 10.0.3.0/24
```

```text
VPC = Region scope
Subnet = Belongs to one AZ
```

### Subnets and EKS nodes
A subnet is not a node.

```text
VPC
└─ Subnet
   └─ EKS Node
      └─ Pod
```

- Subnet = Network space
- EKS Node = An actual compute server, usually EC2

A subnet can contain multiple nodes.

Analogy:
> A subnet is the land, and a node is a server on that land.

---

## 2.2 CIDR

CIDR = Classless Inter-Domain Routing.

> A way to express IP address ranges

Example:
```text
10.0.0.0/24
```

IPv4 has 32 bits, and `/24` means the first 24 bits are fixed as the network portion.

```text
/16 = 65,536 addresses
/20 = 4,096
/24 = 256
/28 = 16
/32 = 1
/0  = All IPv4 addresses
```

Key points:
```text
A smaller prefix number means a larger range
A larger prefix number means a smaller range
```

### 0.0.0.0/0
Matches all IPv4 addresses.

### /32
Means exactly one IP address.

### AWS reserved IP addresses
AWS reserves some IP addresses in each subnet.

Therefore, `/24 = 256 addresses`, but only 251 addresses are usable.

EKS also uses:
- Node IP
- Pod IP
- Addresses associated with ENIs
- Other AWS resource IPs

These also consume addresses, so do not calculate `/24 = 256 combined nodes and Pods`.


The 251 usable addresses in a `/24` assume an ordinary IPv4 subnet where AWS reserves five addresses; BYOIP has an exception. The CIDR table's `/32` and `/0` describe address ranges, while VPC IPv4 subnets permit `/16` through `/28`. [AWS subnet sizing](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html).

---

## 2.3 Public IP / Private IP

Common private IPv4 ranges:

| Range | CIDR |
|---|---|
| 10.0.0.0 ~ 10.255.255.255 | 10.0.0.0/8 |
| 172.16.0.0 ~ 172.31.255.255 | 172.16.0.0/12 |
| 192.168.0.0 ~ 192.168.255.255 | 192.168.0.0/16 |

```text
Private IP = Internal network communication
Public IP = Internet communication
```

Private IP addresses are not routed directly over the internet.

---

## 2.4 Public / Private Subnet

Public/private subnets are distinguished by route table configuration, not separate types.

### Public Subnet
Typical route:
```text
0.0.0.0/0 → Internet Gateway
```

Direct internet communication for a public resource usually requires:
- IGW Route
- Public IP / Elastic IP
- Security Group permission

These are among the required conditions.

### Private Subnet
There is no direct route to an IGW.

When outbound access is needed:
```text
0.0.0.0/0 → NAT Gateway
```

Typical placement:
```text
Public Subnet
→ ALB / NAT Gateway

Private Subnet
→ EKS Node / EC2 App / RDS / ElastiCache / MSK
```


The source's public IP and `0.0.0.0/0` explanation assumes IPv4. A public subnet still requires a resource's public IPv4 address, routing, SG and NACL rules, and a listening service for communication. Check IPv6 addresses and `::/0` routing separately. [AWS Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html).

---

## 2.5 Route Table

> Determines where to send traffic based on its destination.

Example:
```text
Destination        Target
10.0.0.0/16        local
0.0.0.0/0          igw-xxxx
```

### Typical routes
```text
10.0.0.0/16 → local
= Communication within the same VPC

0.0.0.0/0 → IGW
= Public Internet

0.0.0.0/0 → NAT Gateway
= Private Subnet Outbound
```

### Longest Prefix Match
When multiple routes match, the more specific CIDR takes precedence.

### Route Table vs Security Group
```text
Route Table = Where to go
Security Group = Whether to allow communication
```

---

## 2.6 Internet Gateway

IGW = Internet Gateway.

> A gateway connecting a VPC to the internet

```text
Internet
 ↓
IGW
 ↓
VPC
```

An IGW attaches to a VPC, not to a specific subnet.

Public Subnet:
```text
0.0.0.0/0 → IGW
```

Direct internet communication from public EC2 usually requires:
1. An IGW on the VPC
2. Route Table
3. Public IP
4. Security Group permission

An IGW is shared by multiple public subnets at VPC level, rather than created for every AZ.

---

## 2.7 NAT Gateway

> An outbound internet exit for resources in private subnets

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
Private → Internet = Possible
Internet → Initiate directly to private resources = Not possible
```

A NAT Gateway is usually placed in a public subnet.

Consider a NAT Gateway in each AZ for production Multi-AZ deployments.

Some AWS services, such as S3/ECR, can bypass NAT through VPC endpoints.


Per-AZ NAT in public subnets describes **public zonal NAT Gateways**. Route each private subnet through its own AZ's NAT to reduce cross-AZ dependencies. Regional NAT Gateways are also supported, require no public subnet, and offer automatic or manual AZ modes. Regional NAT does not support private NAT. Private NAT is not an internet exit through an IGW. To bypass NAT with endpoints, verify the target service and required endpoints, DNS, and policies separately. [Regional NAT](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html), [NAT types](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html).

---

## 2.8 Security Group

> A stateful virtual firewall applied to AWS resources / ENIs

Criteria:
- Protocol
- Port
- Source / Destination

Example:
```text
TCP 443
Source: 0.0.0.0/0
```

### Stateful
Response traffic for an allowed request is automatically permitted.

### SG Reference
Another Security Group can be specified as the source instead of an IP address.

```text
ALB-SG
443 ← Internet

APP-SG
8080 ← ALB-SG

DB-SG
5432 ← APP-SG
```

### Security Group vs NACL
| Item | Security Group | NACL |
|---|---|---|
| Scope | Resource/ENI | Subnet |
| Stateful | O | X |
| Allow | O | O |
| Explicit Deny | X | O |


A reference does not copy the other SG's rules; it applies to private IPs of associated network interfaces. Rules from multiple attached SGs are combined. An SG allow rule does not create a route. [AWS SG rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html).

---

## 2.9 Basic Multi-AZ VPC structure

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

## Key points

VPCs and subnets divide placement; routes, gateways, and security groups determine actual communication paths.

## LLM practice: review internet paths for private apps in two AZs


**Prompt:**

=== "한국어"

    ```text {.prompt}
    두 AZ의 private 앱이 NAT A에 의존하는지 route 변경안을 검토해 줘. 각 subnet의 실제 route와 NAT 유형을 보고 정상 경로와 AZ A 장애 경로를 설명해 줘. 확인하지 않은 DNS·SG 상태를 가정하거나 route를 변경하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review whether private apps in two AZs depend on NAT A. Use each subnet’s actual routes and NAT type to explain normal traffic and an AZ A failure. Do not assume unverified DNS or security-group state, and do not change routes.
    ```

**Key point:** Per-subnet next hops during normal operation and an AZ outage, failure boundaries, route-change/recovery proposals, and validation checks. It may equate SG permission with an existing route or claim that the internet can initiate connections through NAT. Compare NAT type, zone, and actual routes with flow/DNS evidence. Distinguish SG permission from route existence and make remaining cross-zone dependencies testable after the change.
