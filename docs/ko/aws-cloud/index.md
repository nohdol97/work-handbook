---
id: aws-cloud-overview
status: overview
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids:
  - AWSC-00-01
  - AWSC-00-02
  - AWSC-00-03
  - AWSC-00-04
---

# AWS 클라우드 기초와 학습 현황

새로 제공된 **압축형 7장 커리큘럼**을 따른다. 1~5장의 계정·네트워크·컴퓨트·스토리지/DB·EKS를 담았으며 다음은 **6장 AWS Managed Services**다. 완료는 Basic 개념 학습을 뜻하며 실제 AWS 구축·운영·부하·복구 시험을 뜻하지 않는다.

원문의 번호·순서·표·도식·예시를 보존했다. 제품별 적용 조건은 각 장 본문 뒤의 짧은 보완 설명에서 확인한다.

| 완료한 장 | 정규 문서 | 핵심 범위 |
|---|---|---|
| 1 | [AWS Foundation](foundations.md) | Region/AZ·Account/Organizations·IAM·ARN |
| 2 | [Networking](networking.md) | VPC·CIDR·IP·subnet·route·IGW·NAT·SG·Multi-AZ |
| 3 | [Compute & Load Balancing](compute.md) | EC2/EBS·Launch Template/ASG·ALB/NLB·Kubernetes Service |
| 4 | [Storage & Database](storage-databases.md) | EBS·S3·EFS·PostgreSQL Pod·RDS·Aurora·ElastiCache |
| 5 | [EKS on AWS](eks.md) | Control plane·Node Group·CNI·LB Controller·CSI·ECR·Pod Identity/IRSA |

원문은 Terraform/IaC를 다른 Platform/Infrastructure 세션에서 이미 다뤘다고 밝혀 AWS 목차에서 제외한다. 이 파일에 해당 학습 본문은 없으므로 [기존 플랫폼 과정](../platform-infrastructure/index.md)의 공개 본문 범위는 1~11장 그대로 유지한다. AWS 과정의 진도는 아래 원문 기준이다.

## 원문 소개와 압축 커리큘럼

<!-- SOURCE INTRO START -->

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

<!-- SOURCE INTRO END -->

## 원문 최종 요약

<!-- SOURCE SUMMARY START -->

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

<!-- SOURCE SUMMARY END -->

## 원문 진도와 다음 학습

<!-- SOURCE STATUS START -->

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

<!-- SOURCE STATUS END -->
