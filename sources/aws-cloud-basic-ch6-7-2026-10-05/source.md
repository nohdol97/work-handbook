<!-- 반입 기록
범위: AWS Cloud Basic 6~7장과 최종 요약·완료 기록
한계: Basic 개념 학습 자료이며 실제 AWS 배포·비용·부하·장애 실험 결과가 아니다.
원본 bytes: 20117; SHA-256: e81466af2bf97a9b2bdd14e34b34e7118ea07f95c62e4485cf69be1e6b3b0cc3
정규화: 없음. 원문 공백과 모든 byte를 경계 뒤에 그대로 보존한다.
whitespace_restoration: []
-->
<!-- ORIGINAL SOURCE START -->
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

# Chapter 6. AWS Managed Services

## 6.1 SQS

SQS = **Simple Queue Service**

> 서비스 사이의 메시지를 Queue에 저장해두고 비동기로 처리하는 AWS Managed Message Queue

기본 구조:

```text
Producer
   ↓
  SQS
   ↓
Consumer
```

예:

```text
API Pod
 ↓
SQS
 ↓
Worker Pod
```

API가 오래 걸리는 작업을 직접 처리하지 않고 Queue에 넣은 뒤 바로 응답할 수 있다.

### 왜 SQS를 쓰는가?

```text
User
 ↓
API
 ↓
SQS에 Job 저장
 ↓
즉시 응답

Worker
 ↓
SQS에서 Job 가져옴
 ↓
실제 처리
```

핵심 효과:
- Producer와 Consumer 분리
- 트래픽 급증 흡수
- 비동기 처리
- 장애 시 재시도 가능

### Consumer Polling

SQS는 Consumer가 Queue에서 메시지를 가져간다.

```text
Worker
 ↓ poll
SQS
 ↓
Message
```

Kafka처럼 Event Stream을 지속적으로 읽는 감각보다는 Queue에 쌓인 Task를 Worker가 가져가 처리하는 모델에 가깝다.

### Visibility Timeout

Consumer가 메시지를 가져가도 즉시 삭제되지 않는다.

```text
Worker A가 Message 수신
 ↓
Visibility Timeout
 ↓
다른 Worker에게 잠시 숨김
```

Worker가 처리 완료 후 Delete하면 메시지가 제거된다.

실패해서 Delete하지 못하면:

```text
처리 실패
 ↓
Visibility Timeout 만료
 ↓
Message 재노출
 ↓
다른 Worker가 다시 처리 가능
```

### Dead Letter Queue

계속 실패하는 메시지를 별도 Queue로 격리할 수 있다.

```text
Main Queue
 ↓ 반복 실패
DLQ
```

용도:
- 실패 메시지 분석
- 오류 원인 확인
- 수동 재처리

### Standard vs FIFO

#### Standard Queue
- 높은 처리량
- 순서가 완전히 보장되지는 않음
- 중복 전달 가능성을 고려해야 함
- Consumer는 Idempotent하게 만드는 것이 좋음

#### FIFO Queue
FIFO = First-In-First-Out.

```text
A
B
C
→ A → B → C
```

기본 선택 기준:

```text
일반 비동기 작업
→ Standard

순서가 중요
→ FIFO
```

### EKS와 SQS

```text
API Pods
   ↓
  SQS
   ↓
Worker Pods
```

Queue Depth가 늘면 Worker Pod 수를 늘리는 Auto Scaling 구조도 만들 수 있다.

AI Platform 예:

```text
사용자 요청
 ↓
API
 ↓
SQS
 ↓
Evaluation Worker
 ↓
LLM Evaluation 실행
```

---

## 6.1.1 SQS vs Kafka

중요한 차이는 **병렬 처리 여부가 아니다.** SQS도 Consumer를 여러 개 두면 병렬 처리가 가능하다.

핵심 차이:

```text
SQS
= Task Queue

Kafka
= Event Log / Event Streaming Platform
```

### SQS

```text
Producer
 ↓
Queue
 ↓
Worker A / B / C
```

느낌:

> "이 작업을 누군가 한 번 처리해줘."

예:
- 이미지 변환 Job
- 이메일 발송
- LLM Evaluation Job
- 주문 후처리

처리 완료 후 메시지는 보통 삭제된다.

### Kafka

```text
Event
 ↓
Kafka Topic
 ↓
Consumer Groups
```

느낌:

> "이 이벤트가 발생했으니 기록해둘게. 필요한 시스템이 각자 읽어."

예:

```text
click event
 ↓
Kafka
├─ Analytics Group
├─ Recommendation Group
└─ Monitoring Group
```

한 Consumer가 읽었다고 Event가 없어지는 것이 아니다.

### Replay

Kafka는 Offset을 되돌려 과거 Event를 다시 읽을 수 있다.

```text
지난 3일 이벤트
 ↓ Replay
새 알고리즘으로 재처리
```

SQS는 이런 장기 Event Log / Replay 용도로 설계된 서비스가 아니다.

### 병렬 처리 방식

SQS:

```text
Queue
 ↓
Worker A
Worker B
Worker C
```

Kafka:

```text
Topic
├─ Partition 0 → Consumer A
├─ Partition 1 → Consumer B
└─ Partition 2 → Consumer C
```

Partition이 Kafka의 병렬 처리 단위가 된다.

| 항목 | SQS | Kafka |
|---|---|---|
| 모델 | Queue | Distributed Log |
| 목적 | Task 전달 | Event 보존/Streaming |
| 처리 후 | Delete | 일정 기간 보존 |
| Replay | 제한적 | Offset 기반 가능 |
| 여러 독립 Consumer | 별도 구성 | Consumer Group |
| 병렬 처리 | Consumer 수 | Partition + Consumer |
| 대표 용도 | 비동기 Job | Event Pipeline |

---

## 6.2 SNS

SNS = **Simple Notification Service**

> 하나의 메시지를 여러 Subscriber에게 동시에 전달하는 Managed Pub/Sub 서비스

```text
Publisher
   ↓
 SNS Topic
 ├─ Subscriber A
 ├─ Subscriber B
 └─ Subscriber C
```

### Topic

메시지는 Topic에 Publish한다.

```text
Order Service
   ↓
SNS Topic
├─ Email Service
├─ Analytics
└─ Notification Service
```

### SNS vs SQS

```text
SQS
= 1개의 작업을 Worker에게 분배

SNS
= 1개의 이벤트를 여러 곳에 Broadcast
```

### SNS + SQS

실무에서 흔한 Fan-out 패턴:

```text
            SNS Topic
          /     |      \
         ↓      ↓       ↓
      SQS A   SQS B   SQS C
        ↓       ↓       ↓
     Worker   Worker   Worker
```

장점:
- 시스템 간 결합도 감소
- 각 Consumer 속도 차이 흡수
- 실패/재시도 독립
- 한 시스템 장애가 다른 시스템에 덜 영향

### Subscriber 종류

대표적으로:
- SQS
- HTTP/HTTPS Endpoint
- Lambda
- Email
- SMS

Basic에서는 AWS 서비스 간 이벤트 분배에 SNS → SQS / Lambda 조합이 흔하다고 이해하면 충분하다.

---

## 6.3 Amazon MSK

MSK = **Managed Streaming for Apache Kafka**

> AWS가 Kafka Broker 인프라 운영을 상당 부분 대신해주는 Managed Kafka 서비스

Kafka 자체 개념은 이미 학습한 것으로 보고 AWS 관점만 다룬다.

### 직접 Kafka 운영 vs MSK

직접 운영:

```text
EC2 / EKS
 ↓
Kafka Cluster
├─ Broker
├─ Storage
├─ Replication
├─ Patch
└─ Failure Handling
```

MSK:

```text
Producer / Consumer
        ↓
       MSK
```

### VPC 내부 배치

보통 Private Subnet에 Broker를 배치한다.

```text
VPC
├─ Private Subnet A
│  └─ MSK Broker
├─ Private Subnet B
│  └─ MSK Broker
└─ Private Subnet C
   └─ MSK Broker
```

EKS Application은 VPC 내부에서 접근한다.

### Multi-AZ

```text
AZ A → Broker
AZ B → Broker
AZ C → Broker
```

Kafka Replication과 AWS Multi-AZ를 함께 활용한다.

### Security

```text
Network
→ VPC / Security Group

Authentication
→ Kafka Client 인증

Encryption
→ 전송 / 저장 암호화
```

### EKS + MSK

```text
Users / Services
      ↓
     EKS
      ↓
     MSK
      ↓
 ┌────┼─────┐
 ↓    ↓     ↓
Analytics
Data Pipeline
Monitoring
```

### SQS vs MSK

```text
SQS
= Task Queue

MSK
= Event Streaming / Event Log
```

예:

```text
이미지 변환 Job
→ SQS

사용자 Click Event
→ MSK
```

---

## 6.4 KMS

KMS = **Key Management Service**

> AWS Resource를 암호화할 때 사용하는 암호화 Key를 생성하고 관리하는 서비스

### 연결되는 대표 서비스

```text
S3 → Object 암호화
EBS → Disk 암호화
RDS → DB Storage 암호화
Secrets Manager → Secret 암호화
```

KMS 자체에 일반 데이터를 저장하는 것이 아니라 다른 AWS 서비스가 데이터를 암호화할 때 사용할 Key를 관리한다.

### Encryption at Rest vs In Transit

```text
At Rest
= 저장 데이터 암호화

In Transit
= 전송 데이터 암호화
```

### AWS Managed Key vs Customer Managed Key

AWS Managed Key:
- AWS가 서비스용으로 관리

Customer Managed Key:
- 사용자가 직접 생성
- Key Policy 관리
- Rotation 설정
- 환경/서비스별 Key 분리

```text
단순 사용
→ AWS Managed Key

세밀한 통제 필요
→ Customer Managed Key
```

### IAM과 KMS

```text
IAM
= 누가 AWS Resource를 사용할 수 있는가

KMS
= 누가 Encryption Key를 사용할 수 있는가
```

KMS로 암호화된 S3 Object를 읽을 때는 상황에 따라:

```text
s3:GetObject
+
kms:Decrypt
```

권한이 함께 필요할 수 있다.

### Key Rotation

KMS는 Key Lifecycle과 Rotation 관리 기능을 제공한다.

---

## 6.5 Secrets Manager

Secrets Manager:

> DB Password, API Key, Token 같은 민감한 값을 안전하게 저장·조회·교체하는 AWS Managed 서비스

### 저장 대상

- Database Username / Password
- API Key
- OAuth Client Secret
- External Service Token

### IAM과 연결

```text
API Pod
 ↓
Pod Identity
 ↓
IAM Role
 ↓
secretsmanager:GetSecretValue
 ↓
Secrets Manager
```

### KMS와 Secrets Manager 관계

정확한 흐름:

```text
Plain Secret
   ↓
Secrets Manager
   ↓
KMS Key 사용
   ↓
Encrypted Secret 저장
```

사용자가 먼저 KMS로 직접 암호화해서 Secrets Manager에 넣는다는 의미가 아니라, Secrets Manager가 저장 시 KMS Key를 사용해 암호화한다고 이해한다.

조회 시:

```text
EKS Pod
 ↓
IAM Role
 ↓
Secrets Manager
 ↓
KMS를 이용해 복호화
 ↓
Secret 반환
```

역할 정리:

```text
Secrets Manager
= Secret 저장 / 조회 / Rotation

KMS
= Secret 암호화 Key 관리

IAM
= 누가 Secret과 Key를 사용할 수 있는지 제어
```

### Secret Rotation

```text
Old Password
 ↓
Rotation
 ↓
New Password
```

RDS Credential 등과 연동해 Secret Lifecycle을 자동화할 수 있다.

### Kubernetes Secret과 차이

```text
Kubernetes Secret
= Kubernetes 내부 Secret Resource

AWS Secrets Manager
= AWS Managed Secret Store
```

둘은 별개지만 연동할 수 있다.

---

## 6.6 CloudWatch

CloudWatch:

> AWS Resource와 Application의 상태를 관찰하는 Monitoring 서비스

Basic에서는 세 가지가 핵심이다.

```text
Metrics
Logs
Alarm
```

### Metrics

예:

```text
EC2 → CPUUtilization
ALB → RequestCount / TargetResponseTime
RDS → CPU / Connection / Storage
SQS → Queue Message 수
```

### Logs

```text
EKS Pod
 ↓
Application Log
 ↓
CloudWatch Logs
```

Metric은 상태 수치, Log는 상세 사건 기록이다.

### Alarm

```text
CPU > 80%
5분 지속
 ↓
CloudWatch Alarm
```

또는:

```text
SQS Queue Depth > 1000
 ↓
Alarm
```

### Auto Scaling과 연결

```text
CloudWatch Metric
   ↓
CPU 80%
   ↓
Scaling Policy
   ↓
ASG Scale Out
```

### EKS에서

```text
Infrastructure
→ Node CPU / Memory

Application
→ Pod Log / App Metric
```

### CloudWatch vs Prometheus/Grafana

```text
CloudWatch
= AWS Resource 중심 Managed Monitoring

Prometheus
= Metric 수집 / Time Series Monitoring

Grafana
= Dashboard / Visualization
```

---

## 6.7 CloudTrail

CloudTrail:

> AWS에서 누가, 언제, 어떤 API를 호출해서 무엇을 했는지 기록하는 Audit 서비스

### 기록 정보

```text
Who → 어떤 User / Role
When → 언제
What → 어떤 AWS API
Where → 어떤 Region / Resource
```

### CloudWatch와 차이

```text
CloudWatch
= 시스템 상태 / 성능

CloudTrail
= AWS API 활동 기록
```

예:

```text
EC2 CPU 95%
→ CloudWatch

누가 EC2를 삭제했는가?
→ CloudTrail
```

### Console 작업도 API

```text
AWS Console
 ↓
AWS API
 ↓
CloudTrail
```

### 보안 사고 조사

Security Group, IAM Policy, S3 설정 등의 변경 주체와 시점을 추적하는 데 중요하다.

### CloudTrail + CloudWatch

```text
CloudTrail
→ 누가 무엇을 했는지

CloudWatch
→ 그 결과 시스템 상태가 어떻게 변했는지
```

---

# Chapter 6 전체 요약

```text
SQS = Task Queue
SNS = Pub/Sub / Fan-out
MSK = Managed Kafka / Event Streaming
KMS = Encryption Key 관리
Secrets Manager = Secret 저장 / 조회 / Rotation
CloudWatch = Monitoring
CloudTrail = Audit
```

---

# Chapter 7. AI/GPU + End-to-End

## 7.1 GPU EC2

GPU EC2:

> GPU가 장착된 EC2 Instance

```text
일반 EC2
→ CPU + Memory

GPU EC2
→ CPU + Memory + GPU
```

대표 용도:
- LLM Inference
- Model Training
- Image / Video AI
- CUDA Workload

### GPU VRAM

LLM Serving에서는 GPU VRAM이 핵심 자원이다.

```text
GPU
├─ Compute
└─ VRAM
```

모델이 한 GPU에 들어가지 않으면 여러 GPU에 분산할 수 있다.

### GPU EC2도 일반 AWS 구조를 따른다

```text
VPC
 ↓
Private Subnet
 ↓
GPU EC2
├─ Security Group
├─ IAM Role
├─ EBS
└─ GPU
```

### Container와 GPU

```text
ECR
 ↓
GPU EC2
 ↓
Container
 ↓
vLLM
 ↓
GPU
```

### Model Storage

```text
ECR
→ vLLM 실행 Image

S3
→ Model Weight
```

실행 흐름:

```text
GPU EC2
 ↓
ECR에서 Image Pull
 ↓
S3에서 Model 다운로드
 ↓
GPU VRAM에 Model Load
 ↓
Serving Ready
```

---

## 7.2 EKS GPU Node

EKS GPU Node:

> GPU EC2를 EKS Worker Node로 사용하는 것

```text
EKS
├─ General Node Group
│  ├─ CPU EC2
│  └─ CPU EC2
└─ GPU Node Group
   ├─ GPU EC2
   └─ GPU EC2
```

### 왜 분리하는가?

```text
General Node Group
→ API / Backend / Agent

GPU Node Group
→ vLLM / AI Inference
```

### 특정 Pod만 GPU Node에 배치

Kubernetes Scheduling 기능 활용:
- Label
- NodeSelector
- Taint
- Toleration
- Affinity

### GPU Resource Request

```text
Pod
resources:
  GPU: 1
```

Scheduler는 GPU Capacity가 남아 있는 Node를 찾는다.

### NVIDIA Device Plugin

```text
GPU EC2
 ↓
NVIDIA Driver
 ↓
NVIDIA Device Plugin
 ↓
Kubernetes에서 GPU Resource 인식
 ↓
GPU Pod Scheduling
```

### GPU Node Scaling

```text
vLLM Pod 증가
 ↓
GPU Capacity 부족
 ↓
GPU Node Group Scale Out
 ↓
GPU EC2 추가
```

GPU는 비싸므로 최소 Node 수, Scale Out 조건, Idle 시간, Spot 여부 등을 신중하게 본다.

---

## 7.3 ECR + S3 Model Storage

AI Serving에서는 실행 코드와 모델을 분리한다.

```text
ECR
→ 실행 환경 / Container Image

S3
→ Model Weight / Tokenizer / Artifact
```

### 왜 Model을 ECR Image 안에 넣지 않는가?

모델은 매우 클 수 있다.

```text
Image 크기 증가
↓
Build 느림
↓
Push/Pull 느림
↓
Model 변경 때 Image 재Build
```

그래서 Code와 Model Lifecycle을 분리한다.

### Pod 시작 흐름

```text
EKS GPU Node
 ↓
ECR에서 vLLM Image Pull
 ↓
S3에서 Model 다운로드
 ↓
Local Disk / Cache 저장
 ↓
GPU VRAM에 Load
 ↓
Serving Ready
```

정리:

```text
ECR
= 무엇을 실행할 것인가

S3
= 어떤 모델을 실행할 것인가
```

### IAM 권한

```text
vLLM Pod
 ↓
Pod Identity
 ↓
IAM Role
 ↓
s3:GetObject
 ↓
model-prod/*
```

### Model Versioning

```text
s3://model-bucket/
├─ llama-v1/
├─ llama-v2/
└─ llama-v3/
```

Container Image는 그대로 두고 Model Version만 바꿀 수 있다.

### Model Cache

```text
S3
 ↓ 최초 다운로드
Node Local Disk / EBS / Cache
 ↓
GPU Pod
```

S3는 원본 Model Storage, 실제 Serving에서는 Node 근처에 캐시할 수 있다.

---

## 7.4 vLLM Serving 구조

기본 요청 흐름:

```text
User
 ↓ HTTPS
ALB
 ↓
Kubernetes Service
 ↓
vLLM Pod
 ↓
GPU
 ↓
Model
```

### GPU Node 배치

```text
EKS
├─ General Node Group
│  └─ API / Backend Pods
└─ GPU Node Group
   └─ vLLM Pods
```

### API Layer 분리

실무에서는 vLLM을 외부에 직접 노출하지 않고 API Layer를 둘 수 있다.

```text
User
 ↓
ALB
 ↓
API Pod
 ↓
vLLM Service
 ↓
vLLM Pod
 ↓
GPU
```

API Layer 역할 예:
- 인증
- Rate Limit
- 요청 검증
- Model Routing
- Usage Logging

### 여러 vLLM Replica

```text
Service
├─ vLLM Pod A → GPU A
├─ vLLM Pod B → GPU B
└─ vLLM Pod C → GPU C
```

GPU Memory와 Model Loading 비용이 크므로 일반 Web Pod처럼 무작정 Replica를 늘리면 비용이 크다.

### Scaling과 Cold Start

```text
새 GPU EC2 생성
 ↓
ECR Image Pull
 ↓
S3 Model Download
 ↓
GPU VRAM Load
 ↓
Ready
```

실무 고려:
- 최소 GPU Node 유지
- Model Cache
- Autoscaling
- 트래픽 예측

---

## 7.5 End-to-End AWS Architecture

전체 구조:

```text
AWS Account
└─ Seoul Region
   └─ VPC
      │
      ├─ Public Subnets
      │   ├─ ALB
      │   └─ NAT Gateway
      │
      └─ Private Subnets
          ├─ EKS
          │   ├─ General Node Group
          │   └─ GPU Node Group
          ├─ RDS / Aurora
          ├─ ElastiCache
          └─ MSK
```

VPC 주변 Managed Services:

```text
S3
ECR
SQS / SNS
KMS
Secrets Manager
CloudWatch
CloudTrail
```

### 사용자 요청 흐름

일반 API:

```text
User
 ↓
Internet
 ↓
ALB
 ↓
EKS Service
 ↓
API Pod
 ↓
RDS / ElastiCache
```

LLM 요청:

```text
User
 ↓
ALB
 ↓
API Pod
 ↓
vLLM Service
 ↓
GPU Pod
 ↓
GPU
```

### 데이터 저장 역할

```text
RDS / Aurora
→ 사용자 / 설정 / Transactional Data

ElastiCache
→ Cache / Session

S3
→ Dataset / Model / Backup / Object

EBS
→ Pod 또는 EC2의 Block Disk

EFS
→ 여러 Pod가 공유하는 File System
```

### 비동기 / 이벤트

```text
SQS
→ 하나의 작업을 Worker에게 전달

SNS
→ 하나의 이벤트를 여러 Subscriber에게 전달

MSK
→ 이벤트를 보존하고 여러 Consumer Group이 독립 소비
```

예:

```text
API
 ↓
SQS
 ↓
Evaluation Worker
```

또는:

```text
User Click
 ↓
MSK
├─ Analytics
├─ Recommendation
└─ Monitoring
```

### Security

```text
IAM
→ 누가 AWS Resource에 접근 가능한가

Pod Identity
→ Pod별 IAM Role

Security Group
→ Network 접근 제어

KMS
→ Encryption Key 관리

Secrets Manager
→ Password / API Key 저장
```

### Observability / Audit

```text
CloudWatch
→ Metric / Log / Alarm

CloudTrail
→ AWS API Audit
```

### 최종 AI/Data Platform 구조

```text
                         Internet
                            ↓
                           ALB
                            ↓
                           EKS
                 ┌──────────┴──────────┐
                 │                     │
        General Node Group       GPU Node Group
                 │                     │
         API / Agent Pods          vLLM Pods
          /      |      \               │
         ↓       ↓       ↓              ↓
       RDS   ElastiCache  SQS          GPU
                          │              ↑
                          ↓              │
                       Workers           │
                                         │
ECR ─────────────→ Container Images      │
S3 ──────────────→ Model / Dataset ─────┘

MSK
→ Event Streaming

SNS
→ Event Fan-out

KMS
→ Encryption

Secrets Manager
→ Secrets

CloudWatch
→ Monitoring

CloudTrail
→ Audit
```

---

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
