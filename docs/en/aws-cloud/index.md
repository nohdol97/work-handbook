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
  - AWSC2-00-01
  - AWSC2-00-02
  - AWSC2-00-03
---

# AWS cloud basics and study progress

This section covers the **full compact seven-chapter curriculum**. **Basic conceptual study of Chapters 1–7 is complete**, from accounts, networking, compute, storage/databases, and EKS to managed services, security, observability, GPU serving, and the final AWS architecture. Completed means Basic conceptual study, not actual AWS implementation, operations, load tests, or recovery tests.

The source numbering, order, tables, diagrams, and examples are preserved in translation. Read the short supplement after each chapter for product-specific conditions.

| Completed chapter | Canonical topic | Main scope |
|---|---|---|
| 1 | [AWS Foundation](foundations.md) | Regions/AZs, accounts/Organizations, IAM, ARNs |
| 2 | [Networking](networking.md) | VPCs, CIDR, IPs, subnets, routes, IGW, NAT, security groups, Multi-AZ |
| 3 | [Compute & Load Balancing](compute.md) | EC2/EBS, launch templates/ASGs, ALB/NLB, Kubernetes Services |
| 4 | [Storage & Database](storage-databases.md) | EBS, S3, EFS, PostgreSQL Pods, RDS, Aurora, ElastiCache |
| 5 | [EKS on AWS](eks.md) | Control plane, node groups, CNI, load balancer controller, CSI, ECR, Pod Identity/IRSA |
| 6 | [AWS Managed Services](managed-services.md) | SQS, SNS, MSK, KMS, Secrets Manager, CloudWatch, CloudTrail |
| 7 | [AI/GPU and end-to-end AWS architecture](ai-gpu-architecture.md) | GPU EC2, EKS GPU nodes, ECR/S3, vLLM, final AI/data platform |

The source states that Terraform/IaC was already covered in another Platform/Infrastructure session and excludes it from the AWS curriculum. The later [platform course](../platform-infrastructure/index.md) source supplies Chapters 12–15. See [Terraform and IaC](../platform-infrastructure/terraform-iac.md) for the source and its conditions. Current AWS progress follows the latest Chapters 6–7 completion record below. Further advanced study and lab material have not been supplied.

## Latest Source: Chapters 6–7 Scope, Summary, and Completion

<!-- SOURCE MANAGED INTRO START -->

# AWS Cloud Basic — Source Markdown (Chapter 6~7)

> Scope: material studied after Chapter 5  
> Included: Chapter 6. AWS Managed Services + Chapter 7. AI/GPU + End-to-End  
> Principles:
> - Based on material actually studied in the session
> - Includes questions and supplementary explanations from the session
> - Removes duplication
> - Focuses on core concepts at the Basic level
> - Does not repeat Terraform / IaC, which was already studied in another session

---

<!-- SOURCE MANAGED INTRO END -->

<!-- SOURCE MANAGED SUMMARY START -->

# Final Summary of Chapters 6~7

## Messaging / Event

```text
SQS = Task Queue
SNS = Pub/Sub / Fan-out
MSK = Kafka / Event Streaming
```

## Security

```text
IAM = Permissions
KMS = Encryption Key
Secrets Manager = Secret storage / Rotation
```

## Observability

```text
CloudWatch = Monitoring
CloudTrail = Audit
```

## AI / GPU

```text
GPU EC2 = GPU Compute
EKS GPU Node = GPU Worker Node
ECR = Container Image
S3 = Model / Dataset
vLLM = GPU-based LLM Serving
```

---

<!-- SOURCE MANAGED SUMMARY END -->

<!-- SOURCE MANAGED STATUS START -->

# AWS Cloud Basic Final Study Completion Status

Completed:
- Chapter 1. AWS Foundation ✅
- Chapter 2. Networking ✅
- Chapter 3. Compute & Load Balancing ✅
- Chapter 4. Storage & Database ✅
- Chapter 5. EKS on AWS ✅
- Chapter 6. AWS Managed Services ✅
- Chapter 7. AI/GPU + End-to-End ✅

Final core structure:

```text
Network
→ VPC / Subnet / Route / IGW / NAT / SG

Compute
→ EC2 / ASG / EKS

Traffic
→ ALB / NLB / Service

Storage
→ EBS / EFS / S3

Data
→ RDS / Aurora / ElastiCache

Messaging
→ SQS / SNS / MSK

Security
→ IAM / KMS / Secrets Manager

Observability
→ CloudWatch / CloudTrail

AI
→ GPU EC2 / EKS GPU Node / ECR / S3 / vLLM
```

You have met the AWS Cloud Basic goal if you can explain why each AWS service exists, where it fits, and what it connects to.

<!-- SOURCE MANAGED STATUS END -->

## Earlier Source: Chapters 1–5 Introduction and Compact Curriculum

The following introduction, summary, and progress describe the earlier Chapters 1–5 source. “Next” inside that source refers to that point in time, separate from the current completion of Chapters 1–7.

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

## Earlier Source: Chapters 1–5 Final Summary

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

## Earlier Source: Progress and Next Study After Chapters 1–5

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
