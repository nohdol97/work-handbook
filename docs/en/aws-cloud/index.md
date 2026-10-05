---
id: aws-cloud-overview
status: overview
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AWSC-00-01
  - AWSC-00-02
  - AWSC-00-03
  - AWSC-00-04
---

# AWS cloud basics and study progress

This section follows the newly supplied **compact seven-chapter curriculum**. Chapters 1–5 cover accounts, networking, compute, storage/databases, and EKS. **Chapter 6, AWS Managed Services**, is next. Completed means Basic conceptual study, not actual AWS implementation, operations, load tests, or recovery tests.

The source numbering, order, tables, diagrams, and examples are preserved in translation. Read the short supplement after each chapter for product-specific conditions.

| Completed chapter | Canonical topic | Main scope |
|---|---|---|
| 1 | [AWS Foundation](foundations.md) | Regions/AZs, accounts/Organizations, IAM, ARNs |
| 2 | [Networking](networking.md) | VPCs, CIDR, IPs, subnets, routes, IGW, NAT, security groups, Multi-AZ |
| 3 | [Compute & Load Balancing](compute.md) | EC2/EBS, launch templates/ASGs, ALB/NLB, Kubernetes Services |
| 4 | [Storage & Database](storage-databases.md) | EBS, S3, EFS, PostgreSQL Pods, RDS, Aurora, ElastiCache |
| 5 | [EKS on AWS](eks.md) | Control plane, node groups, CNI, load balancer controller, CSI, ECR, Pod Identity/IRSA |

The source states that Terraform/IaC was already covered in another Platform/Infrastructure session and excludes it from the AWS curriculum. The later [platform course](../platform-infrastructure/index.md) source supplies Chapters 12–15. See [Terraform and IaC](../platform-infrastructure/terraform-iac.md) for the source and its conditions. AWS progress follows the source below.

## Source introduction and compact curriculum

<!-- SOURCE INTRO START -->

# AWS Cloud Basic — Source Markdown (Chapter 1~5)

> Basis: the compact AWS Cloud Basic curriculum from the current session  
> Principles: remove duplication, focus on core concepts, and include supplementary questions and misconception corrections from the session  
> Terraform / IaC was already studied in another Platform / Infrastructure session, so it is excluded as a separate chapter

---

# Full compact curriculum

1. AWS Foundation
2. Networking
3. Compute & Load Balancing
4. Storage & Database
5. EKS on AWS
6. AWS Managed Services
7. AI/GPU + End-to-End

This document records the material studied in Chapters 1~5.

---

<!-- SOURCE INTRO END -->

## Source final summary

<!-- SOURCE SUMMARY START -->

# Final summary of Chapters 1~5

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

External traffic:
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

<!-- SOURCE SUMMARY END -->

## Source progress and next study

<!-- SOURCE STATUS START -->

# Current progress

Completed:
- Chapter 1. AWS Foundation ✅
- Chapter 2. Networking ✅
- Chapter 3. Compute & Load Balancing ✅
- Chapter 4. Storage & Database ✅
- Chapter 5. EKS on AWS ✅

Next:

## Chapter 6. AWS Managed Services
1. SQS
2. SNS
3. MSK
4. KMS
5. Secrets Manager
6. CloudWatch
7. CloudTrail

After that:

## Chapter 7. AI/GPU + End-to-End

<!-- SOURCE STATUS END -->
