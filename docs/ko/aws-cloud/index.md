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

# AWS 클라우드 기초와 학습 현황

제공된 **압축형 7장 커리큘럼 전체**를 반영했다. 계정·네트워크·컴퓨트·스토리지/DB·EKS에서 관리형 서비스·보안·관측·GPU 서빙·최종 AWS 구조까지 **1~7장 Basic 개념 학습 완료** 상태다. 완료는 Basic 개념 학습을 뜻하며 실제 AWS 구축·운영·부하·복구 시험을 뜻하지 않는다.

원문의 번호·순서·표·도식·예시를 보존했다. 제품별 적용 조건은 각 장 본문 뒤의 짧은 보완 설명에서 확인한다.

| 완료한 장 | 정규 문서 | 핵심 범위 |
|---|---|---|
| 1 | [AWS Foundation](foundations.md) | Region/AZ·Account/Organizations·IAM·ARN |
| 2 | [Networking](networking.md) | VPC·CIDR·IP·subnet·route·IGW·NAT·SG·Multi-AZ |
| 3 | [Compute & Load Balancing](compute.md) | EC2/EBS·Launch Template/ASG·ALB/NLB·Kubernetes Service |
| 4 | [Storage & Database](storage-databases.md) | EBS·S3·EFS·PostgreSQL Pod·RDS·Aurora·ElastiCache |
| 5 | [EKS on AWS](eks.md) | Control plane·Node Group·CNI·LB Controller·CSI·ECR·Pod Identity/IRSA |
| 6 | [AWS Managed Services](managed-services.md) | SQS·SNS·MSK·KMS·Secrets Manager·CloudWatch·CloudTrail |
| 7 | [AI/GPU·전체 AWS 구조](ai-gpu-architecture.md) | GPU EC2·EKS GPU Node·ECR/S3·vLLM·최종 AI/Data Platform |

원문은 Terraform/IaC를 다른 Platform/Infrastructure 세션에서 이미 다뤘다고 밝혀 AWS 목차에서 제외한다. 이후 제공된 [플랫폼 과정](../platform-infrastructure/index.md) 12~15장에 해당 학습 본문이 반영되었다. [Terraform·IaC](../platform-infrastructure/terraform-iac.md)에서 원문과 적용 조건을 확인한다. 현재 AWS 진도는 아래 최신 6~7장 완료 기록을 따른다. 후속 심화·실습 자료는 아직 제공되지 않았다.

## 최신 원문: 6~7장 범위·요약·완료

<!-- SOURCE MANAGED INTRO START -->

# AWS Cloud Basic — Source Markdown (Chapter 6~7)

> 범위: Chapter 5 이후 학습 내용  
> 포함 범위: Chapter 6. AWS Managed Services + Chapter 7. AI/GPU + End-to-End  
> 원칙:
> - 세션에서 실제 학습한 내용 기준
> - 중간 질문/보충 설명 포함
> - 중복 제거
> - Basic 수준 핵심 중심
> - Terraform / IaC는 다른 세션에서 이미 학습했으므로 반복하지 않음

---

<!-- SOURCE MANAGED INTRO END -->

<!-- SOURCE MANAGED SUMMARY START -->

# Chapter 6~7 최종 요약

## Messaging / Event

```text
SQS = Task Queue
SNS = Pub/Sub / Fan-out
MSK = Kafka / Event Streaming
```

## Security

```text
IAM = 권한
KMS = Encryption Key
Secrets Manager = Secret 저장 / Rotation
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
vLLM = GPU 기반 LLM Serving
```

---

<!-- SOURCE MANAGED SUMMARY END -->

<!-- SOURCE MANAGED STATUS START -->

# AWS Cloud Basic 최종 학습 완료 상태

완료:
- Chapter 1. AWS Foundation ✅
- Chapter 2. Networking ✅
- Chapter 3. Compute & Load Balancing ✅
- Chapter 4. Storage & Database ✅
- Chapter 5. EKS on AWS ✅
- Chapter 6. AWS Managed Services ✅
- Chapter 7. AI/GPU + End-to-End ✅

최종 핵심 구조:

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

각 AWS 서비스가 왜 존재하고, 어디에 배치되며, 무엇과 연결되는지 설명할 수 있으면 AWS Cloud Basic 목표를 달성한 것이다.

<!-- SOURCE MANAGED STATUS END -->

## 이전 원문: 1~5장 소개와 압축 커리큘럼

아래 소개·요약·진도는 1~5장 자료를 받았을 당시 기록이다. 원문 속 “다음”은 당시 시점을 뜻하며 현재 1~7장 완료 상태와 구분한다.

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

## 이전 원문: 1~5장 최종 요약

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

## 이전 원문: 1~5장 당시 진도와 다음 학습

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
