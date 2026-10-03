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

# AWS 클라우드 기초와 학습 현황

AWS Cloud Basic의 1~5장과 중간 보충 질문을 담았다. **완료는 Basic 개념 학습**을 뜻한다. AWS 계정이나 리소스를 조회·생성하거나 배포·비용·성능·장애를 시험했다는 의미가 아니다. 다음은 6장 Kubernetes on AWS이며 6~12장은 아직 학습 본문이 없는 후속 목차다.

**읽기 안내:** 원문의 순서·번호·표·도식·예시를 그대로 보존한다. 각 장의 보완 구역에서 적용 조건을 확인한다. 아래 통합 구조에서 S3 위치·ALB 표시·NAT와 RDS 배치는 단순화된 원문 도식이므로 뒤의 **통합 구조 보완**을 함께 읽는다.

## 학습 문서

| 완료한 장 | 정규 문서 | 핵심 범위 |
|---|---|---|
| 1 | [AWS 기본 구조](foundations.md) | Region/AZ·Account·Organizations·IAM·Role·권한 경계 |
| 2 | [네트워킹](networking.md) | VPC·subnet·route·CIDR/IP·IGW·NAT·SG·ALB 보충 |
| 3 | [컴퓨트](compute.md) | EC2·AMI·ASG·health check·load balancer·EKS 연결 |
| 4 | [스토리지](storage.md) | EBS·S3·EFS·snapshot·공유와 격리·DB Pod 저장소 |
| 5 | [데이터베이스·캐시](databases-cache.md) | RDS·Aurora·ElastiCache·HA·replica/shard·connection·TTL |

[플랫폼·인프라 과정](../platform-infrastructure/index.md)은 Linux·Kubernetes와 서비스 운영의 공통 기반을 다룬다. 이 AWS 과정은 관리 서비스의 구성과 책임을 연결하며, 두 과정의 학습 진도는 별도다. [데이터 플랫폼](../data-platform/curriculum.md)의 저장·처리 관점도 함께 참고한다.

## 원문 소개와 전체 커리큘럼

<!-- SOURCE INTRO START -->

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

<!-- SOURCE INTRO END -->

## 원문 통합 구조

<!-- SOURCE ARCHITECTURE START -->

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

<!-- SOURCE ARCHITECTURE END -->

## 통합 구조 보완

2026-10-03에 AWS 공식 문서를 확인했다. 아래는 원문 도식의 적용 범위이며 실제 환경 검증 결과가 아니다.

- **S3 위치:** S3를 VPC 아래 그린 것은 서비스 연결을 나타내는 단순화다. 일반 S3 bucket을 EC2처럼 subnet 안에 배치하지 않는다. S3 gateway endpoint를 통해 VPC에서 접근할 수 있으며 이 경로는 IGW/NAT를 필요로 하지 않는다. 따라서 모든 S3 요청이 아래 NAT outbound 도식을 따르는 것은 아니다. [AWS S3 gateway endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
- **ALB 표시:** AZ A/B의 ALB 표시는 각 AZ에서 동작하는 load balancer node로 읽는다. 일반적인 다중 AZ 구성에서 AZ마다 별도 ALB를 반드시 생성한다는 뜻은 아니다. [Elastic Load Balancing 동작](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html)
- **NAT 구성:** NAT Gateway A/B를 public subnet에 두는 그림은 public **zonal** NAT 예시다. 현재 regional NAT도 지원되므로 모든 배포의 필수 구조로 일반화하지 않는다. 실제 mode와 경로·가용성 조건은 [네트워킹 보완](networking.md)과 [Regional NAT 공식 문서](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html)를 확인한다.
- **데이터 계층:** RDS Primary/Standby 그림과 ElastiCache Primary/Replica는 가능한 구성의 예시다. 읽기 제공·failover·shard 동작을 모든 RDS/Aurora/ElastiCache 유형에 그대로 적용하지 않는다. [데이터베이스·캐시 보완](databases-cache.md)에서 구성별 조건을 구분한다.

## 원문 학습 상태

<!-- SOURCE STATUS START -->

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

<!-- SOURCE STATUS END -->
