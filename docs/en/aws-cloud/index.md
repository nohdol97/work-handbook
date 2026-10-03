---
id: aws-cloud-overview
status: overview
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-00-01
  - AWS-00-02
  - AWS-00-03
  - AWS-00-04
---

# AWS cloud basics and study progress

This section contains AWS Cloud Basic Chapters 1–5 and supplementary questions. **Completed means Basic conceptual study.** It does not mean AWS accounts or resources were inspected or created, or that deployments, costs, performance, or failures were tested. Chapter 6, Kubernetes on AWS, is next. Chapters 6–12 remain future topics without supplied study content.

**Reading guide:** The source order, numbering, tables, diagrams, and examples are preserved in translation. Check each chapter's supplement for applicable conditions. The S3 position, ALB labels, and NAT and RDS placement in the integrated architecture are simplified source diagrams. Read **Integrated architecture supplement** below as well.

## Study pages

| Completed chapter | Canonical topic | Main scope |
|---|---|---|
| 1 | [AWS foundations](foundations.md) | Regions/AZs, accounts, Organizations, IAM, roles, permission boundaries |
| 2 | [Networking](networking.md) | VPCs, subnets, routes, CIDR/IP, IGW, NAT, security groups, ALB supplement |
| 3 | [Compute](compute.md) | EC2, AMIs, ASGs, health checks, load balancers, EKS connections |
| 4 | [Storage](storage.md) | EBS, S3, EFS, snapshots, sharing and isolation, database Pod storage |
| 5 | [Databases and cache](databases-cache.md) | RDS, Aurora, ElastiCache, HA, replicas/shards, connections, TTL |

The [platform and infrastructure course](../platform-infrastructure/index.md) covers the common foundations of Linux, Kubernetes, and service operations. This AWS course connects managed-service configurations and responsibilities. The courses track progress separately. Also refer to storage and processing in the [data platform course](../data-platform/curriculum.md).

## Source introduction and full curriculum

<!-- SOURCE INTRO START -->

# AWS Cloud Basic — Source Markdown

> This source Markdown records the material studied in the current session.  
> Scope: completed Chapters 1 ~ 5 + supplementary questions and answers  
> Purpose: a source for later documentation, handbook writing, and review material

---

# Full curriculum

1. AWS foundations
   - Region / Availability Zone
   - AWS Account
   - IAM basics
2. Networking
   - VPC
   - Public / Private Subnet
   - Route Table
   - Internet Gateway
   - NAT Gateway
   - Security Group
   - Supplement: CIDR
   - Supplement: Public IP / Private IP
   - Supplement: ALB
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
   - SQS / SNS basics
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

<!-- SOURCE INTRO END -->

## Source integrated architecture

<!-- SOURCE ARCHITECTURE START -->

# Integrated architecture for Chapters 1~5

The material studied so far connects in the following structure.

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

Application request flow:

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

Outbound access from private resources:

```text
EKS / EC2
 ↓
NAT Gateway
 ↓
IGW
 ↓
Internet
```

Storage roles:

```text
EBS
= Server disk

EFS
= Shared filesystem

S3
= Object Storage

RDS
= Persistent relational data

ElastiCache
= Fast temporary / cached data
```

Permissions/security:

```text
IAM
= AWS resource access permissions

Security Group
= Network access allowances

Route Table
= Traffic paths

VPC / Subnet
= Network placement
```

---

<!-- SOURCE ARCHITECTURE END -->

## Integrated architecture supplement

AWS official documentation was checked on 2026-10-03. These notes explain the source diagram's scope; they are not results of testing an actual environment.

- **S3 placement:** Drawing S3 under the VPC is a simplified view of service connections. A general-purpose S3 bucket is not placed in a subnet like an EC2 instance. A gateway endpoint provides VPC access to S3 without an IGW or NAT. Not every S3 request therefore follows the NAT outbound diagram. [AWS S3 gateway endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- **ALB labels:** Read the ALB labels in AZs A/B as load balancer nodes operating in those zones. A typical multi-AZ setup does not require a separate ALB for every AZ. [How Elastic Load Balancing works](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html)
- **NAT configuration:** The diagram with NAT Gateways A/B in public subnets is a public **zonal** NAT example. Regional NAT is also supported, so this is not the required design for every deployment. Check actual modes, paths, and availability conditions in the [networking supplement](networking.md) and [regional NAT documentation](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html).
- **Data layer:** RDS Primary/Standby and ElastiCache Primary/Replica illustrate possible configurations. Do not apply their read-serving, failover, or sharding behavior to every RDS/Aurora/ElastiCache type. The [databases and cache supplement](databases-cache.md) separates these conditions.

## Source study status

<!-- SOURCE STATUS START -->

# Current study progress

Completed:

- Chapter 1. AWS foundations ✅
- Chapter 2. Networking ✅
- Chapter 3. Compute ✅
- Chapter 4. Storage ✅
- Chapter 5. Database / Cache ✅

Next study:

## Chapter 6. Kubernetes on AWS

Planned topics:

- EKS
- Node Group
- Managed Node Group
- AWS Load Balancer Controller
- EBS CSI Driver

After that:

- Chapter 7. Messaging
- Chapter 8. Security
- Chapter 9. Observability
- Chapter 10. IaC
- Chapter 11. AI / GPU Infrastructure
- Chapter 12. End-to-End Architecture

<!-- SOURCE STATUS END -->
