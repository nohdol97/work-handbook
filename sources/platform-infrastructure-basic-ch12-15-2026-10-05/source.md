<!-- 반입 기록
범위: Platform / Infrastructure / AI Serving Basic 12~15장과 최종 구조·학습 완료 기록
한계: 개념 학습 원문이며 실제 배포·운영·부하·복구 실험 결과가 아니다.
원본 bytes: 48741; SHA-256: 72cf7231f3c4cf8477775ed27921e9e034ad4c282ab436778362f27d2d4f995d
정규화: 없음. 원문 공백과 모든 byte를 경계 뒤에 보존한다.
whitespace_restoration: []
-->
<!-- ORIGINAL SOURCE START -->
# Platform / Infrastructure / AI Serving Basic
## Source Markdown — Chapter 12~15

> 이 문서는 이 학습 세션에서 **Chapter 11 이후** 진행한 내용을 정리한 source markdown이다.  
> 범위: **Chapter 12 Terraform & Infrastructure as Code ~ Chapter 15 End-to-End AI Platform Architecture**

---

# Chapter 12. Terraform & Infrastructure as Code

## 12.1 IaC Fundamentals

Infrastructure as Code(IaC)는 인프라를 콘솔에서 수동으로 만드는 대신 코드로 선언하고 관리하는 방식이다.

핵심 목적:

- 인프라 변경 이력 관리
- 반복 가능한 환경 구성
- 환경 간 일관성 확보
- 리뷰 가능한 변경
- 자동화된 생성/수정/삭제

대표적인 역할 분리는 다음과 같다.

```text
Terraform
= Cloud / Infrastructure 생성

Argo CD + Helm
= Kubernetes Application 배포
```

예:

```text
Terraform
↓
VPC
Subnet
Security Group
Load Balancer
EKS
Node Pool
GPU Node Pool
RDS
Storage
IAM
```

그 위에:

```text
Argo CD
↓
Backend
LiteLLM
vLLM
Worker
```

를 배포한다.

---

## 12.2 Terraform 기본 구성 요소

### Provider

Terraform이 어떤 플랫폼의 API와 통신할지 정의한다.

예:

```text
AWS Provider
Kubernetes Provider
GitHub Provider
```

### Resource

Terraform이 직접 생성하고 관리하는 대상이다.

예:

```text
aws_vpc
aws_subnet
aws_eks_cluster
aws_db_instance
```

### Data Source

Terraform이 직접 만들지는 않고 기존 리소스 정보를 조회한다.

예:

```text
기존 VPC 조회
기존 AMI 조회
기존 IAM Role 조회
```

### Variable

외부에서 값을 받아 같은 코드를 여러 환경에서 재사용할 수 있게 한다.

예:

```text
environment = dev
environment = prod
```

### Output

생성된 인프라 정보를 외부로 전달한다.

예:

```text
VPC ID
Cluster Endpoint
Database Endpoint
```

---

## 12.3 Terraform State

Terraform에서 중요한 개념은 **State**이다.

Terraform State는:

```text
Terraform Resource Address
↔
실제 Cloud Resource ID
```

의 매핑을 보관한다.

예:

```text
aws_vpc.main
↔
vpc-123456
```

State에는 마지막으로 확인된 리소스 속성들도 저장된다.

Terraform의 일반적인 흐름:

```text
Terraform Code
↓
State 확인
↓
Provider를 통해 실제 Resource 조회
↓
Desired State와 Actual State 비교
↓
Plan 생성
↓
Apply
↓
State 업데이트
```

### Git과 State의 차이

```text
Git
= 원하는 인프라 구조를 코드로 저장

State
= Terraform Resource와 실제 Resource의 연결 정보 저장
```

Git만 있다고 Terraform이 기존 리소스를 자동으로 자신이 관리하는 대상으로 인식하는 것은 아니다.

State가 사라지면 Terraform은 기존 리소스와의 연결을 잃을 수 있다.

기존 Resource를 Terraform 관리 대상으로 연결할 때는 `import`를 사용할 수 있다.

---

## 12.4 Remote State

개인 로컬 State만 사용하면 팀 작업에 적합하지 않다.

팀에서는 Remote State를 사용하는 것이 일반적이다.

AWS 환경 예:

```text
S3
→ Terraform State 저장

State Locking
→ 동시에 여러 사람이 Apply하는 문제 방지
```

현재 Terraform S3 Backend에서는 S3 기반 lockfile 방식(`use_lockfile=true`)을 사용할 수 있으며, 과거 DynamoDB 기반 locking 방식은 deprecated 방향으로 이해하면 된다.

State 저장소에는 다음이 중요하다.

- 접근 권한
- 버전 관리
- 백업
- 암호화
- Locking

특히 S3 Versioning을 켜두면 State 복구에 도움이 된다.

---

## 12.5 Terraform Plan / Apply Workflow

일반적인 Team Workflow:

```text
Developer
↓
Pull Request
↓
CI
↓
terraform plan
↓
Review
↓
Merge / Approval
↓
terraform apply
↓
Remote State Update
```

`plan`은:

> 어떤 변경이 발생할지 확인

`apply`는:

> 실제 인프라에 변경 적용

이다.

둘은 하나의 Pipeline에서 단계로 나눌 수도 있고 서로 다른 Workflow로 구성할 수도 있다.

중요한 것은:

```text
Plan
↓
Review / Approval
↓
Apply
```

의 Gate가 존재하는 것이다.

---

## 12.6 Terraform Module

Module은 재사용 가능한 인프라 패키지다.

예:

```text
modules/
└─ vpc/
   ├─ main.tf
   ├─ variables.tf
   └─ outputs.tf
```

환경별:

```text
dev
↓
VPC Module

prod
↓
동일 VPC Module
```

을 재사용할 수 있다.

예시 Module:

```text
VPC Module
EKS Module
GPU Node Module
Database Module
```

Module을 통해 회사 표준을 코드에 넣을 수 있다.

예:

```text
Logging 기본 활성화
Encryption 필수
Tagging 규칙
Security 설정
```

비교:

```text
Helm Chart
= Kubernetes Application 구조 재사용

Terraform Module
= Infrastructure 구조 재사용
```

---

## 12.7 Cloud Infrastructure 구성

Terraform은 다음과 같은 Cloud Resource를 만들 수 있다.

```text
Network
├─ VPC
├─ Subnet
├─ Route Table
├─ Security Group
└─ Load Balancer

Compute
├─ EKS
├─ General Node Pool
└─ GPU Node Pool

Data
├─ RDS
└─ Storage
```

Resource 간 Dependency는 Terraform Reference를 통해 표현할 수 있다.

예:

```text
Subnet
↓
VPC ID 참조
```

Terraform이 Dependency Graph를 계산해 생성 순서를 결정한다.

---

## 12.8 Terraform과 Kubernetes Resource 경계

일반적인 권장 역할:

```text
Terraform
→ Cluster / Node / Cloud Infrastructure

Argo CD
→ Kubernetes Application
```

Terraform:

```text
EKS
GPU Node Pool
IAM
Cloud Storage
RDS
```

Argo CD:

```text
Deployment
Service
Ingress
ConfigMap
Application workload
```

Namespace / RBAC처럼 양쪽 모두 관리 가능한 리소스도 있다.

중요한 원칙:

> 하나의 리소스를 Terraform과 Argo CD가 동시에 관리하지 않는다.

Terraform이 Argo CD 자체를 Bootstrap하는 패턴은 가능하다.

---

## 12.9 Environment Strategy

Module은 재사용하고 State는 환경별로 분리하는 것이 좋다.

예:

```text
infra/
├─ modules/
│  ├─ vpc/
│  ├─ eks/
│  └─ database/
└─ env/
   ├─ dev/
   ├─ staging/
   └─ prod/
```

State:

```text
dev state
staging state
prod state
```

Prod 규모가 커지면 더 나눌 수도 있다.

예:

```text
network state
eks state
database state
gpu state
```

Terraform Workspace도 사용할 수 있지만, Production에서는 directory/root module + separate state 구조가 더 명확한 경우가 많다.

Long-lived branch로 환경을 나누기보다는:

```text
main
+
environment directory
+
separate state
```

방식이 일반적으로 관리하기 쉽다.

---

## 12.10 Terraform Operations

### Drift

Terraform 코드와 실제 Cloud 상태가 달라지는 것.

예:

```text
Terraform에서는 SG Rule 없음
Cloud Console에서 수동으로 Rule 추가
```

다음 Plan에서 Drift를 감지할 수 있다.

가능하면 Console 직접 변경보다 Terraform을 통한 변경을 우선한다.

### Replace

일부 속성 변경은 Update가 아니라 Resource 재생성이 필요할 수 있다.

Plan에서:

```text
update
replace
destroy
create
```

를 확인해야 한다.

### Import

기존 Cloud Resource를 Terraform State에 연결한다.

### State Recovery

Remote State versioning / backup을 이용해 복구 가능성을 확보한다.

State 직접 수정은 위험하므로 가능한 최소화한다.

---

# Chapter 13. Multi-tenancy, Quotas & Cost Control

## 13.1 Multi-tenancy 모델

여러 팀이 하나의 Platform을 함께 쓰는 방식에는 여러 수준이 있다.

```text
Shared Cluster
↓
Namespace 기반 Isolation
↓
Dedicated Node Pool
↓
Dedicated Cluster
```

일반적인 내부 AI Platform에서는:

```text
Shared Cluster
+
Namespace
+
RBAC
+
NetworkPolicy
+
Quota
```

를 기본으로 하고, 더 강한 격리가 필요할 때 Node Pool 또는 Cluster까지 분리한다.

---

## 13.2 Isolation Layer

강도를 높이면:

```text
Namespace
↓
RBAC
↓
NetworkPolicy
↓
ResourceQuota
↓
Dedicated Node Pool
↓
Dedicated Cluster
```

로 생각할 수 있다.

### Namespace

논리적 리소스 경계.

### RBAC

누가 어떤 리소스를 조작할 수 있는지 제한.

### NetworkPolicy

서비스 간 통신을 제한.

### Node Isolation

Label / Taint 등을 이용해 특정 Workload만 특정 Node에 배치.

---

## 13.3 ResourceQuota

ResourceQuota는 Namespace 전체 자원 사용량을 제한한다.

예:

```text
Team A Namespace

CPU <= 100
Memory <= 500Gi
GPU <= 8
```

또한 일부 Kubernetes object 개수도 제한할 수 있다.

중요:

> Quota가 있다고 실제 Resource가 예약되는 것은 아니다.

예:

```text
GPU quota = 8
```

이어도 Cluster에 GPU가 없으면 Pod는 Pending이다.

---

## 13.4 LimitRange

LimitRange는 개별 Pod / Container 수준의 기본값과 최소/최대값을 정의한다.

예:

```text
Default CPU Request
Default Memory Request
Maximum Memory
Minimum CPU
```

구분:

```text
ResourceQuota
= Namespace 전체 Aggregate Limit

LimitRange
= Pod / Container 수준의 기본/최소/최대 설정
```

둘은 함께 사용하는 경우가 많다.

---

## 13.5 Fairness와 Noisy Neighbor

하나의 팀이 자원을 과도하게 사용하면 다른 팀에 영향을 줄 수 있다.

이를 Noisy Neighbor라고 한다.

해결 수단:

```text
Quota
PriorityClass
Preemption
Dedicated Resource
```

Fairness는 무조건 동일한 자원을 나누는 것이 아니다.

예:

```text
Production Service
> Development Experiment
```

처럼 중요도와 SLA에 따라 차등 관리할 수 있다.

---

## 13.6 AI / LLM Quota

AI Platform에서는 Kubernetes 자원만 제한해서는 부족하다.

LLM 사용량도 제한해야 한다.

예:

```text
RPM
TPM
Concurrent Requests
Max Context Length
GPU Quota
```

특히 공유 vLLM Pool에서는:

```text
1M Context Request
+
높은 Concurrency
```

가 KV Cache를 많이 점유해 다른 팀까지 느리게 만들 수 있다.

따라서:

```text
TPM
Concurrency
Context Length
```

등을 Tenant별로 제한해야 한다.

---

## 13.7 Kubernetes Quota와 LLM Quota 차이

```text
Kubernetes ResourceQuota
→ CPU / Memory / GPU 등 물리 자원

LLM Quota
→ Token / Request / Context / Concurrency 등 서비스 사용량
```

둘 다 필요하다.

예:

```text
Team A

Kubernetes:
GPU <= 4

LiteLLM:
TPM <= 2M
Concurrency <= 10
Context <= 128K
```

---

## 13.8 Cost Attribution

비용을 줄이려면 먼저 누가 얼마나 사용하는지 알아야 한다.

예:

```text
Team
Service
Model
GPU Usage
Token Usage
```

를 연결한다.

Dedicated GPU:

```text
GPU-hours
```

로 계산하기 쉽다.

Shared vLLM:

```text
Input Tokens
Output Tokens
Model
Context
Request Metadata
```

등으로 비용을 나눌 수 있다.

Shared Infrastructure와 Spare Capacity도 비용이다.

따라서:

```text
Tag
Label
Namespace
Owner
```

가 중요하다.

---

## 13.9 GPU Cost Optimization

GPU 비용 최적화는 GPU Utilization 숫자 하나만 보는 것이 아니다.

봐야 할 것:

```text
GPU Compute Utilization
VRAM
KV Cache
Queue
Throughput
Latency
```

방법:

- Continuous Batching
- 적절한 Model Replica 수
- 작은 Workload는 Sharing
- Autoscaling
- Right-sizing
- Quantization
- 적절한 Context Limit

하지만 Cost를 줄이기 위해 Spare Capacity를 완전히 없애면 HA / Canary / Rolling Update / Traffic Spike 대응이 어려워질 수 있다.

따라서:

```text
Cost
vs
Reliability / SLA
```

를 같이 본다.

---

## 13.10 Showback / Chargeback

### Showback

팀에 비용 정보를 보여주지만 실제 비용을 청구하지는 않는다.

### Chargeback

각 팀 Budget에 실제 비용을 반영한다.

내부 Platform에서는 일반적으로:

```text
Cost Attribution
↓
Showback
↓
Quota
↓
필요하면 Chargeback
```

순서로 발전시키는 것이 현실적이다.

Shared Resource 비용은:

- 사용량 비례
- 균등 배분
- Platform 공통 예산 처리

등 다양한 방식으로 나눌 수 있다.

---

# Chapter 14. Internal Developer Platform / Self-Service

## 14.1 Platform as a Product

Platform Team은 단순히 Cluster를 운영하는 팀이 아니라 내부 개발자를 고객으로 보는 Product Team처럼 동작할 수 있다.

목표:

```text
Developer가 빠르게
안전하게
표준화된 방식으로
서비스를 만들고 운영
```

할 수 있도록 한다.

중요한 관점:

```text
Cluster Uptime만 관리
→ 부족

Developer Experience
Delivery Speed
Safety
Standardization
→ 중요
```

---

## 14.2 Golden Path

Golden Path는:

> 회사가 권장하는 가장 쉽고 안전한 표준 개발/배포 경로

이다.

예:

```text
Backend Service 생성
↓
Repository
Dockerfile
CI
Helm
Argo CD
Namespace
Monitoring
```

을 표준 Template으로 제공한다.

특징:

- Opinionated
- Standardized
- Guardrail 포함
- 필요하면 Escape Hatch 제공

즉 모든 자유도를 제거하는 것이 아니라 기본적으로 안전한 경로를 제공한다.

---

## 14.3 Self-Service

개발자가 Ticket을 만들어 Platform Team이 수동으로 처리하는 대신:

```text
Portal / API
↓
요청
↓
Automation
```

형태로 직접 Resource를 만들 수 있게 한다.

예:

```text
Create Backend
Create Database
Create Model Endpoint
Request GPU
```

하지만 Self-Service는:

```text
Raw Cloud Admin Access
Raw Kubernetes Admin Access
```

를 주는 것이 아니다.

사용자가 입력할 수 있는 값을 제한하고 뒤에서 표준 Module / Template을 실행한다.

---

## 14.4 Developer Portal

Developer Portal은 내부 Platform의 Front Door다.

대표적인 OSS 예시는 Backstage다.

Portal에서 제공할 수 있는 것:

```text
Service Catalog
Ownership
Templates
Self-Service UI
Docs
Deployment Link
Monitoring Link
```

예:

```text
agent-api

Owner: Team A
Repo: Git
Deployment: Argo CD
Dashboard: Grafana
Docs: Internal Docs
```

Portal은 Terraform이나 Kubernetes를 대체하는 것이 아니라 그 앞에서 Platform 기능을 통합해서 보여준다.

---

## 14.5 Platform API

Platform API는:

> 개발자가 Kubernetes / Terraform / Cloud API를 직접 사용하지 않고 Platform이 제공하는 단순화된 Interface를 사용하는 방식

이다.

예:

```http
POST /platform/databases
```

```json
{
  "type": "postgres",
  "size": "medium",
  "environment": "dev"
}
```

개발자는:

```text
PostgreSQL 필요
```

만 표현한다.

Platform은 내부적으로:

```text
Validation
Policy
Terraform
Git
Argo CD
Kubernetes
```

등을 실행한다.

---

## 14.6 Platform API의 추상화

개발자에게:

```text
EKS Node Group 생성
Helm Values 수정
Argo CD Application 생성
```

을 요구하지 않고:

```text
Backend Service 생성
```

같은 Intent만 받는다.

뒤에서:

```text
Namespace
Deployment
Service
Ingress
CI/CD
Monitoring
```

을 구성할 수 있다.

Portal / CLI / CI Pipeline이 모두 같은 Platform API를 사용할 수도 있다.

```text
Portal
CLI
CI
 ↓
Platform API
```

이렇게 하면 정책이 일관된다.

---

## 14.7 Kubernetes CRD를 Platform API로 사용

Kubernetes CRD(Custom Resource Definition)를 이용해 회사만의 Resource를 만들 수 있다.

예:

```yaml
kind: ModelEndpoint

spec:
  model: qwen-32b
  gpu: b300
  replicas: 2
```

Platform Controller가 이를 읽고:

```text
ModelEndpoint
↓
vLLM Deployment
↓
GPU Scheduling
↓
Service
↓
LiteLLM 등록
```

을 자동화할 수 있다.

Basic 수준에서:

> CRD = 우리 Platform만의 Kubernetes Resource 종류를 만드는 기능

으로 이해하면 된다.

---

## 14.8 왜 직접 Terraform을 모두 열어주지 않는가

모든 개발자가 자유롭게 Terraform을 사용하면 다음 문제가 생길 수 있다.

```text
잘못된 GPU Instance
Public DB
과도한 Resource
Security Group 오설정
회사 표준 위반
```

Platform API에서 선택지를 제한할 수 있다.

예:

```text
GPU Type
→ H100 / B300만 허용

Production
→ Replica >= 2

Database
→ Public Access 금지
```

즉 Platform API는:

```text
Abstraction
+
Guardrail
```

역할을 한다.

---

## 14.9 Platform Automation

Self-Service의 핵심은 UI가 아니라 요청 뒤에서 실제 작업을 자동 수행하는 것이다.

전체 흐름:

```text
Request
↓
Validation / Policy
↓
Automation
↓
Terraform / Git / Argo CD
↓
Infrastructure / Application
```

### Infrastructure 생성 예

```text
"PostgreSQL 생성"
↓
Platform API
↓
Validation
↓
Terraform Module
↓
Plan
↓
Approval
↓
Apply
↓
RDS 생성
```

### Application 생성 예

```text
"Backend Service 생성"
↓
Repository 생성
↓
Dockerfile
↓
CI Pipeline
↓
Helm Values
↓
Argo CD Application
↓
Kubernetes 배포
```

---

## 14.10 Policy Automation

Platform Automation에 운영/보안 정책을 넣을 수 있다.

예:

```text
Production Replica >= 2
Container = non-root
Database Public Access = 금지
GPU = 허용된 Type만
```

요청이 정책을 위반하면:

```text
Request
↓
Policy Validation
↓
Reject
```

할 수 있다.

즉:

> Automation = 편의성 + Guardrail

이다.

---

## 14.11 Approval Workflow

모든 요청을 자동 승인할 필요는 없다.

예:

```text
Dev Namespace
→ 자동 승인

Production DB
→ 관리자 승인

B300 GPU 8개
→ 비용 승인
```

비용 / 위험도에 따라 Workflow를 다르게 설계한다.

---

## 14.12 AI Platform Self-Service

AI Platform Self-Service에서는 개발자가 Model Serving 인프라를 직접 구성하지 않는다.

Portal 입력 예:

```text
Model: Qwen 32B
Environment: prod
Context: 128K
Replicas: 2
```

뒤에서는:

```text
GPU
Tensor Parallel
vLLM Deployment
Service
LiteLLM Routing
Auth
Quota
Monitoring
```

등을 자동 구성한다.

---

## 14.13 AI Capacity Validation

Platform은 Model Endpoint를 만들기 전에 Capacity를 검증할 수 있다.

예:

```text
Model
Precision
Context
Concurrency
↓
Weight Memory
KV Cache
Compute
↓
필요 GPU 수 계산
```

즉 앞에서 학습한 GPU Capacity Planning이 Self-Service Logic에 들어갈 수 있다.

---

## 14.14 AI Endpoint 자동화 흐름

```text
Developer
↓
"Qwen Endpoint 생성"
↓
Platform API
↓
Policy / Capacity Validation
↓
GPU Resource 결정
↓
Git 변경
↓
Argo CD
↓
vLLM Deployment
↓
Service
↓
LiteLLM 등록
↓
Auth / Quota
↓
Monitoring
↓
Endpoint 반환
```

개발자는 최종적으로:

```text
https://llm.company.com/qwen-32b
```

같은 Endpoint를 받는다.

---

## 14.15 GPU Capacity 부족

예:

```text
요청
→ B300 x4

현재 Spare
→ B300 x2
```

이면:

```text
Reject
Approval Pending
GPU Node Expansion Workflow
```

등으로 처리할 수 있다.

Self-Service는 무조건 생성해주는 시스템이 아니다.

---

## 14.16 비용 Guardrail

비싼 Model / Large Context / Large GPU Request는 Approval을 넣을 수 있다.

예:

```text
Qwen 7B
→ 자동 승인

Qwen 72B
→ 팀장 승인

1M Context Large Model
→ Platform / Cost 승인
```

즉:

```text
Self-Service
≠
Unlimited Resource
```

이다.

---

## 14.17 Resource Lifecycle 자동화

생성뿐 아니라 삭제까지 자동화해야 한다.

```text
Endpoint 삭제
↓
LiteLLM Routing 제거
↓
vLLM Deployment 제거
↓
GPU 반환
↓
DNS / Secret 정리
```

Lifecycle 전체를 관리하지 않으면 Resource가 계속 쌓인다.

---

## 14.18 Platform Governance

Platform Governance는:

> 개발자가 Self-Service를 자유롭게 사용하되 회사의 보안/비용/운영 기준을 벗어나지 못하도록 정책을 적용하는 것

이다.

핵심:

```text
Allowed Configuration
Resource Constraints
Security Guardrail
Policy as Code
```

---

## 14.19 Allowed Configuration

예:

```text
GPU
→ B300 / H100만

Production Replica
→ 최소 2

Database
→ Public 금지

Container Image
→ 승인 Registry만
```

Portal/API 수준에서부터 선택지를 제한할 수 있다.

---

## 14.20 Resource Constraints

예:

```text
Team A
GPU <= 4

Dev
CPU <= 4
Memory <= 16Gi
```

ResourceQuota, LimitRange, LLM Quota 등으로 구현할 수 있다.

---

## 14.21 Security Guardrail

예:

```text
Container
→ non-root

Secret
→ Git 평문 금지

Network
→ Default Deny

Production
→ TLS 필수

Image
→ Scan 통과
```

개발자가 보안 규칙을 매번 외우지 않아도 Platform이 강제한다.

---

## 14.22 Policy as Code

운영/보안 규칙을 문서에만 적지 않고 코드로 검사한다.

```text
Developer Request
↓
Policy Engine
↓
Allowed?
├─ Yes → Deploy
└─ No  → Reject
```

예:

```text
Production
replicas=1
↓
Policy violation
↓
Deployment blocked
```

---

## 14.23 Self-Service와 Governance 관계

Self-Service와 Governance는 반대가 아니다.

```text
Self-Service
= 빠른 개발

Governance
= 안전한 범위 제한
```

좋은 Platform은:

> 빠르게 만들 수 있지만 위험한 구성을 만들기는 어렵게 한다.

를 목표로 한다.

---

## 14.24 Platform Governance vs Data Governance

Platform Governance:

```text
누가
어떤 Infra / Model / GPU를
어떤 설정으로 사용할 수 있는가
```

Data Governance:

```text
Data Access
Data Quality
Catalog
Lineage
PII
Retention
```

서로 다른 영역이다.

---

# Chapter 15. End-to-End AI Platform Architecture

## 15.1 Request Path

LLM Request의 기본 경로:

```text
User / Application
↓
Load Balancer / Gateway
↓
LiteLLM
↓
vLLM
↓
GPU
```

### User → Gateway

외부 요청은 HTTPS를 통해 들어온다.

```text
User
↓
Load Balancer / Ingress / Gateway
↓
LiteLLM Service
```

여기서:

- TLS termination
- Host / Path Routing
- Network entry

등을 처리할 수 있다.

---

## 15.2 LiteLLM Request Processing

LiteLLM은 실제 inference를 하지 않고 정책/라우팅을 담당한다.

예:

```text
Request
↓
Authentication
↓
Authorization
↓
Rate Limit
↓
Quota / Budget
↓
Cache
↓
Model Routing
```

LiteLLM은:

> 누가 어떤 모델을 얼마나 사용할 수 있고, 어느 Backend로 보낼지를 결정

한다.

---

## 15.3 LiteLLM → vLLM

Model Pool 예:

```text
GLM Pool
├─ vLLM Replica A
├─ vLLM Replica B
└─ vLLM Replica C
```

LiteLLM은 Health / Routing / Load 등의 기준으로 Replica를 선택한다.

---

## 15.4 vLLM → GPU

vLLM은 실제 추론을 수행한다.

```text
Prompt
↓
Prefill
↓
KV Cache
↓
Decode
↓
Token Generation
```

실제 계산:

```text
vLLM
↓
CUDA
↓
GPU
```

vLLM이 사용하는 핵심 개념:

```text
PagedAttention
Continuous Batching
KV Cache Management
```

---

## 15.5 Streaming Response

LLM 응답은 Token 단위로 Streaming할 수 있다.

```text
GPU
↓
vLLM
↓
LiteLLM
↓
User
```

이 과정에서 중요 지표:

```text
TTFT
TPOT
```

---

## 15.6 Cache Hit

Cache가 있다면 GPU까지 가지 않을 수도 있다.

```text
User
↓
LiteLLM
↓
Redis Cache
↓
Response
```

즉:

```text
Cache Hit
→ GPU 사용 없음

Cache Miss
→ vLLM / GPU Inference
```

---

## 15.7 Retry / Fallback

Replica 장애:

```text
LiteLLM
↓
vLLM A 실패
↓
Retry
↓
vLLM B
```

Model Pool 전체 장애:

```text
GLM 실패
↓
Qwen
또는
External Provider
```

로 Fallback할 수도 있다.

---

## 15.8 Application Infrastructure

AI Platform도 일반 Backend 시스템이 필요하다.

```text
Kubernetes
├─ Backend
├─ LiteLLM
├─ vLLM
├─ Worker
└─ Platform Components
```

PostgreSQL / Redis / Kafka는 Kubernetes 내부 또는 Managed Service로 운영할 수 있다.

---

## 15.9 Backend API

Backend는 Business Logic을 처리한다.

예:

```text
User
↓
Backend
├─ 사용자 정보 조회
├─ 권한 확인
├─ Agent 실행
├─ Data 조회
└─ LLM 요청
```

LLM 호출:

```text
Backend
↓
LiteLLM
↓
vLLM
```

---

## 15.10 PostgreSQL 역할

PostgreSQL은 영구 데이터를 저장한다.

예:

```text
User
Team
Agent 설정
Prompt 정보
Model 설정
Permission
Service Metadata
```

개념적으로:

> PostgreSQL = 시스템의 영구적인 Source of Truth

에 가깝다.

---

## 15.11 Redis 역할

Redis는 빠른 임시/공유 상태에 적합하다.

예:

```text
Session
Cache
Rate Limit
Temporary Token
Request Deduplication
```

구분:

```text
PostgreSQL
= 영구 데이터

Redis
= 빠른 임시 상태 / Cache
```

---

## 15.12 Kafka 역할

Kafka는 서비스 간 비동기 Event 전달에 사용한다.

예:

```text
User Agent 실행
↓
Backend
↓
Kafka Event
↓
Worker
↓
후속 처리
```

또는:

```text
Click Event
Model Call Event
Audit Event
Usage Event
```

를 전달할 수 있다.

---

## 15.13 Sync vs Async

즉시 응답이 필요한 요청:

```text
User
↓
Backend
↓
LiteLLM
↓
vLLM
↓
Response
```

후처리:

```text
Backend
↓
Kafka
↓
Worker
```

예:

- 사용 로그 저장
- 통계
- 데이터 처리
- 알림

---

## 15.14 Managed Service 활용

모든 Component를 Kubernetes 안에 넣을 필요는 없다.

예:

```text
Kubernetes
├─ Backend
├─ LiteLLM
├─ vLLM
└─ Worker

Managed
├─ RDS
├─ Redis
└─ Kafka / MSK
```

Kubernetes 사용 = 모든 상태 시스템을 K8s 안에서 운영한다는 의미는 아니다.

---

## 15.15 AI Serving Infrastructure

AI Serving Layer:

```text
LiteLLM
↓
vLLM
↓
GPU
```

역할:

```text
LiteLLM
= Gateway / Policy / Routing

vLLM
= Model Serving

GPU
= 실제 Compute
```

---

## 15.16 Model Replica

같은 Model Serving Instance를 여러 개 띄울 수 있다.

```text
GLM Pool
├─ Replica A
├─ Replica B
└─ Replica C
```

장점:

- Throughput 증가
- HA
- Rolling Update
- Canary

LiteLLM이 Replica 간 요청을 분산한다.

---

## 15.17 Tensor Parallel vs Replica

```text
Tensor Parallel
= 모델 하나를 여러 GPU에 분산

Replica
= 같은 Model Server를 여러 개 운영
```

예:

```text
Replica A
→ TP=4
→ GPU 4개

Replica B
→ TP=4
→ GPU 4개
```

---

## 15.18 GPU Scheduling

vLLM Pod가 GPU를 요청한다.

```text
vLLM Pod
GPU request = 4
```

Kubernetes Scheduler가 적절한 Node를 찾는다.

예:

```text
Node A
2 GPU available
→ 불가

Node B
4 GPU available
→ 가능
```

GPU가 없으면 Pod는 Pending이다.

---

## 15.19 Readiness

대형 모델은 Pod가 Running이어도 바로 Serving 가능한 것이 아니다.

```text
Pod Created
↓
Model Weight Load
↓
VRAM Allocation
↓
KV Cache 준비
↓
Readiness Success
```

중요:

```text
Pod Running
≠
Model Serving Ready
```

새 Replica가 Ready된 뒤에만 Traffic을 보내야 한다.

---

## 15.20 AI Serving Capacity Bottleneck

예:

```text
Queue 증가
TTFT 증가
GPU Utilization 100%
```

→ Compute Capacity 부족 가능성.

반면:

```text
GPU Utilization 낮음
VRAM 거의 가득
KV Cache 높음
```

→ Memory / Context / Concurrency 병목 가능성.

따라서:

```text
Compute Bottleneck
vs
Memory Bottleneck
```

을 구분해야 한다.

---

## 15.21 Kubernetes Node Pool 구조

```text
General Node Pool
├─ Backend
├─ LiteLLM
├─ Worker
└─ Platform Components

GPU Node Pool
├─ vLLM GLM
├─ vLLM GLM
└─ vLLM Qwen
```

GPU Scheduling에서:

```text
Node Label
Taint / Toleration
Affinity
GPU Request
Topology Spread
```

등을 사용한다.

---

# 15.4 Reliability

## 15.22 Reliability 기본

Reliability는:

> 일부 Pod / Node / GPU / DB가 장애 나도 전체 서비스가 계속 동작하도록 설계하는 것

이다.

핵심:

```text
HA
Failure Domain
Retry / Fallback
Autoscaling
Graceful Shutdown
```

---

## 15.23 Multiple Replicas

단일 Replica:

```text
LiteLLM x1
→ 장애 시 전체 Gateway 중단
```

따라서:

```text
LiteLLM A
LiteLLM B
LiteLLM C
```

처럼 여러 Replica를 둔다.

vLLM도 같은 개념이다.

---

## 15.24 Node 분산

나쁜 예:

```text
Node A
├─ LiteLLM A
├─ LiteLLM B
└─ LiteLLM C
```

Node 장애 시 모두 장애.

좋은 구조:

```text
Node A → Replica A
Node B → Replica B
Node C → Replica C
```

사용:

```text
Anti-Affinity
Topology Spread
```

---

## 15.25 AZ 분산

Failure Domain을 더 크게 보면:

```text
Pod
↓
Node
↓
AZ
```

이다.

Cloud에서는 가능하면 Replica를 여러 AZ에 나눈다.

---

## 15.26 Retry / Fallback

Replica 실패:

```text
LiteLLM
↓
Replica A 실패
↓
Retry
↓
Replica B
```

Pool 실패:

```text
GLM
↓
Qwen / External Provider
```

Retry는 과도하게 사용하면 Retry Storm을 만들 수 있으므로:

```text
Timeout
Retry Limit
Backoff
```

가 필요하다.

---

## 15.27 Autoscaling

Traffic 증가:

```text
Traffic ↑
↓
Queue ↑
↓
TTFT ↑
```

대응:

```text
LiteLLM Replica 증가
vLLM Replica 증가
GPU Node 증가
```

하지만 LLM은 Model Load가 느리다.

따라서:

```text
Autoscaling
+
Spare Capacity
```

를 함께 생각한다.

---

## 15.28 Graceful Shutdown

이상적인 종료:

```text
Pod 종료 예정
↓
Readiness 실패
↓
새 요청 차단
↓
기존 요청 처리 완료
↓
SIGTERM
↓
정상 종료
```

Streaming LLM 요청에서는 특히 중요하다.

---

## 15.29 Stateful Component HA

Kubernetes가 Pod를 다시 띄운다고 DB HA가 해결되는 것은 아니다.

```text
PostgreSQL
→ Primary / Standby / Failover

Redis
→ Replica / Sentinel / Cluster

Kafka
→ Replication / ISR / Leader Election
```

즉:

```text
Kubernetes HA
+
Application / Database 자체 HA
```

가 필요하다.

---

# 15.5 Security

## 15.30 User Access

외부 사용자의 신원을 확인한다.

```text
User
↓
SSO / IAM / API Key
↓
Authentication
↓
Authorization
```

예:

```text
Team A → GLM 사용 가능
Team B → Qwen만 가능
```

---

## 15.31 Kubernetes RBAC

Cluster 내부 권한:

```text
Developer
↓
Role / RoleBinding
↓
자기 Namespace만
```

Pod:

```text
Pod
↓
ServiceAccount
↓
필요한 권한만
```

원칙:

> Least Privilege

---

## 15.32 Secrets

Secret은 코드/Git에 평문 저장하지 않는다.

```text
Vault / Secrets Manager
↓
External Secrets
↓
Kubernetes Secret
↓
Pod
```

각 서비스는 자기에게 필요한 Secret만 접근한다.

---

## 15.33 Network Security

NetworkPolicy로 서비스 간 통신을 제한한다.

예:

```text
LiteLLM → vLLM 허용

일반 Pod → vLLM 직접 접근 차단
```

기본 패턴:

```text
Default Deny
↓
필요한 Ingress / Egress만 Allow
```

---

## 15.34 TLS / mTLS

```text
NetworkPolicy
= 연결 가능 여부

TLS
= 통신 암호화

mTLS
= 암호화 + 양쪽 Service Identity
```

외부:

```text
User
↓ HTTPS
Gateway
```

내부에서도 필요하면 mTLS를 적용한다.

---

## 15.35 Container Security

예:

```text
Non-root
Read-only filesystem
Linux Capabilities 최소화
Seccomp
Privileged 최소화
```

목표:

> Pod가 침해되어도 Host / 다른 Pod로 피해가 확산되기 어렵게 한다.

---

## 15.36 Supply Chain Security

배포 전 Image도 검증한다.

```text
Code
↓
Build
↓
Image Scan
↓
SBOM
↓
Signing
↓
Registry
↓
Kubernetes
```

Production은 승인 Registry / Image만 허용하는 것이 좋다.

---

# 15.6 Deployment

## 15.37 전체 배포 흐름

```text
Code
↓
CI
↓
Image Registry
↓
Git Desired State
↓
Argo CD
↓
Helm
↓
Kubernetes
```

---

## 15.38 CI

PR / Merge 과정:

```text
Code
↓
Test
↓
Lint
↓
Security Scan
↓
Container Build
```

예:

```text
agent-api:a1b2c3d
```

같은 Immutable Image Version을 만든다.

---

## 15.39 Registry

CI가 만든 Image를 Registry에 저장한다.

```text
CI
↓
Image
↓
ECR / Harbor / Registry
```

이 단계에서는 아직 Production Pod가 바뀐 것이 아니다.

---

## 15.40 Deployment Git

실제 어떤 Image Version을 배포할지 GitOps Repository에서 관리한다.

예:

```yaml
image:
  repository: agent-api
  tag: a1b2c3d
```

구분:

```text
Application Repository
→ Code / Image 생성

Deployment Repository
→ 어떤 Image를 어디에 배포할지 정의
```

---

## 15.41 Argo CD

Git 변경을 감지한다.

```text
Git
↓
Argo CD
↓
OutOfSync
↓
Sync
```

Manual / Auto Sync 모두 가능하다.

---

## 15.42 Helm

Helm은:

```text
Chart
+
values-prod.yaml
```

로 Kubernetes Manifest를 만든다.

역할:

```text
Git
= Desired State

Helm
= Manifest Rendering

Argo CD
= Git과 Cluster 동기화
```

---

## 15.43 Rolling Update

Deployment 변경:

```text
Old
Old
Old

↓
New
Old
Old

↓
New
New
Old

↓
New
New
New
```

Readiness가 성공한 Pod부터 Traffic을 받는다.

---

## 15.44 AI Serving Deployment

vLLM은 일반 Backend보다 시작이 느릴 수 있다.

```text
New vLLM Pod
↓
Image Pull
↓
Model Load
↓
VRAM Allocation
↓
KV Cache 준비
↓
Readiness
```

그래서:

```text
Pod Running
≠
Serving Ready
```

이다.

---

## 15.45 Model Canary

새 Model:

```text
Git
↓
Argo CD
↓
새 vLLM Replica
↓
Readiness
↓
LiteLLM Routing
↓
5%
↓
20%
↓
50%
↓
100%
```

문제가 있으면 LiteLLM Routing을 기존 Model로 되돌릴 수 있다.

Canary / Blue-Green은 Old + New를 동시에 유지해야 하므로 추가 GPU / VRAM Capacity가 필요하다.

---

## 15.46 Terraform 위치

```text
Terraform
↓
Infrastructure
↓
Kubernetes
↓
Argo CD + Helm
↓
Application
```

으로 이해하면 된다.

---

# 15.7 Multi-tenancy

## 15.47 기본 Isolation

Multi-tenancy는:

> 여러 팀이 같은 Platform을 쓰되 서로의 자원/권한/성능/비용에 영향을 최소화하는 것

이다.

세 가지 큰 관점:

```text
Access Isolation
Resource Isolation
Usage Isolation
```

---

## 15.48 Namespace

예:

```text
team-a-prod
team-b-prod
team-c-dev
```

Namespace는 기본 논리적 경계다.

---

## 15.49 RBAC

```text
Team A
↓
RoleBinding
↓
team-a Namespace만 접근
```

구분:

```text
Namespace
= 어디를 나눌지

RBAC
= 누가 무엇을 할지
```

---

## 15.50 NetworkPolicy

Namespace가 다르다고 Network가 자동 차단되는 것은 아니다.

```text
Default Deny
↓
필요한 Communication만 Allow
```

예:

```text
team-a Backend
→ team-a Redis 허용

team-a Backend
→ team-b Redis 차단
```

---

## 15.51 ResourceQuota

한 팀이 Cluster 자원을 독점하지 못하게 한다.

예:

```text
Team A

CPU <= 100
Memory <= 500Gi
GPU <= 8
```

---

## 15.52 GPU Isolation

AI Platform에서는 GPU가 비싸고 희소하다.

방법:

```text
Shared GPU Pool
Dedicated GPU Pool
```

중요한 Production은 Dedicated Node에, 작은 개발 Workload는 Shared Resource에 배치할 수 있다.

---

## 15.53 LiteLLM Tenant Policy

Kubernetes Resource만 나누면 충분하지 않다.

LiteLLM에서:

```text
API Key
Team
Model Access
RPM
TPM
Concurrency
Budget
```

을 제한할 수 있다.

예:

```text
Team A
→ GLM
→ TPM 5M
→ Concurrency 20

Team B
→ Qwen
→ TPM 1M
→ Concurrency 5
```

---

## 15.54 Shared vLLM Noisy Neighbor

하나의 vLLM Pool을 여러 팀이 공유할 때:

```text
Team A
→ 1M Context Requests 다량 발생
↓
KV Cache 대량 점유
↓
Queue 증가
↓
Team B / C Latency 증가
```

대응:

```text
TPM
Concurrency
Max Context
Rate Limit
```

---

## 15.55 Cost Attribution

Tenant별:

```text
GPU-hours
Input Tokens
Output Tokens
Model
Context
```

를 추적해 Showback / Chargeback의 기반으로 사용할 수 있다.

---

# 15.8 Self-Service Platform

## 15.56 전체 Self-Service 구조

```text
Developer
↓
Developer Portal
↓
Platform API
↓
Policy / Validation
↓
Automation
↓
Terraform / GitOps
↓
실제 Resource
```

---

## 15.57 Developer Input

예:

```text
Service: agent-api
Environment: prod
Model: qwen-32b
Replicas: 2
```

개발자가 직접:

```text
Terraform
Helm
Argo CD
GPU Scheduling
RBAC
NetworkPolicy
```

을 설정하지 않도록 한다.

---

## 15.58 Developer Portal 기능

예:

```text
Create Service
Create Database
Create Model Endpoint
Request GPU
View Deployment
View Cost
```

---

## 15.59 Platform API

Portal / CLI / CI가 하나의 Platform API를 사용할 수 있다.

```text
Portal
CLI
CI Pipeline
     ↓
Platform API
```

---

## 15.60 Policy / Validation

예:

```text
Production인가?
GPU Quota 충분?
허용 Model인가?
Replica 최소 조건 만족?
Security Policy 만족?
```

결과:

```text
Valid → Automation
Invalid → Reject
High Cost → Approval
```

---

## 15.61 Automation

Infrastructure:

```text
Platform API
↓
Terraform
↓
VPC / EKS / GPU Node / RDS
```

Application:

```text
Platform API
↓
Git
↓
Argo CD
↓
Helm
↓
Kubernetes
```

AI Serving:

```text
vLLM Deployment
↓
GPU Scheduling
↓
Service
↓
LiteLLM Registration
```

---

## 15.62 Monitoring 자동 연결

좋은 Self-Service는 생성만 하지 않는다.

```text
Service 생성
↓
Metrics
↓
Logs
↓
Dashboard
↓
Alerts
```

까지 연결할 수 있다.

---

## 15.63 Ownership 자동 등록

Service Catalog 예:

```text
agent-api

Owner: Team A
Repository: Git
Deployment: Argo CD
Dashboard: Grafana
```

운영 시 담당자를 바로 찾을 수 있어야 한다.

---

# 15.9 Production Failure Scenarios

## 15.64 기본 장애 대응 원칙

Production 장애는 무작정 로그부터 보는 것이 아니라:

> 어느 Layer의 문제인지 빠르게 범위를 좁히는 것이 핵심

이다.

전체 흐름:

```text
User
↓
Gateway / LiteLLM
↓
Backend
↓
vLLM
↓
GPU

Side Dependencies:
PostgreSQL / Redis / Kafka
```

---

## 15.65 요청 전체 실패

증상:

```text
5xx
Timeout
Connection refused
```

확인 순서:

```text
Load Balancer
↓
Ingress / Gateway
↓
Service
↓
Pod
```

체크:

```text
Pod Running?
Readiness?
Service Endpoint?
Ingress Routing?
NetworkPolicy?
```

처음부터 GPU를 볼 필요는 없다.

---

## 15.66 LLM 응답이 느림

증상:

```text
TTFT ↑
Queue ↑
```

확인:

```text
LiteLLM 병목?
↓
vLLM Queue?
↓
GPU Utilization?
↓
KV Cache?
```

예:

```text
GPU 100%
Queue 증가
→ Compute 부족 가능성
```

```text
GPU 낮음
KV Cache 거의 가득
→ Memory / Context / Concurrency 문제 가능성
```

---

## 15.67 vLLM Pod Pending

Scheduling 문제 가능성이 크다.

확인:

```text
GPU 요청 수
Node GPU 여유
Node Selector
Affinity
Taint / Toleration
ResourceQuota
```

예:

```text
Pod needs GPU x4

Node A: 2 free
Node B: 2 free
```

총 4개가 남아 있어도 한 Node에 4개가 필요하다면 Scheduling 불가할 수 있다.

---

## 15.68 vLLM Pod Crash

구분:

```text
OOMKilled
= Container Memory 문제

CUDA OOM
= GPU VRAM 문제
```

CUDA OOM이면:

```text
Model Weight
KV Cache
Context
Concurrency
```

를 본다.

---

## 15.69 DB Slow

증상:

```text
API Latency ↑
DB Connection Timeout
```

확인 순서:

```text
Connection Pool
↓
max_connections
↓
Slow Query
↓
Index
↓
Lock Wait
↓
Disk I/O
```

바로 Redis부터 붙이는 것이 아니라 Query / Index / Connection 문제를 먼저 확인한다.

---

## 15.70 Redis 장애

증상:

```text
Cache Timeout
Session 문제
Rate Limit 오동작
```

Cache 용도라면:

```text
Redis 장애
↓
DB Fallback
```

이 가능할 수 있다.

설계 시:

> Redis가 없어도 서비스가 동작 가능한가?

를 판단해야 한다.

---

## 15.71 Kafka Consumer Lag

원인:

```text
Consumer 처리 부족
Consumer 장애
Partition 수 부족
Downstream DB 느림
Network 문제
```

단순히 Consumer 수만 늘리는 것으로 해결되지 않을 수 있다.

같이 봐야 할 것:

```text
Partition
Consumer
Processing Time
Downstream Bottleneck
```

---

## 15.72 Node 장애

예:

```text
GPU Node A 장애
↓
vLLM Replica A 장애
```

다른 Replica가 있으면:

```text
LiteLLM
↓
Replica B / C
```

로 우회 가능하다.

하지만 Spare GPU가 없으면 Replica A가 다른 Node에서 다시 뜨지 못할 수 있다.

따라서:

```text
HA
+
Spare Capacity
```

가 필요하다.

---

## 15.73 배포 직후 장애

증상:

```text
Deploy 직후
5xx ↑
Latency ↑
```

먼저 최근 변경을 본다.

```text
Image?
Config?
Model Version?
Helm Values?
```

복구:

```text
Git / Argo Rollback
```

AI Serving에서는:

```text
LiteLLM Routing
↓
기존 Model로 우회
```

도 가능하다.

---

## 15.74 장애 대응 기본 사고 순서

```text
1. 영향 범위는 어디인가?
2. 최근 변경이 있었나?
3. Pod가 정상인가?
4. Resource 부족인가?
5. Network / DNS 문제인가?
6. Dependency 장애인가?
7. Infra / Node 문제인가?
```

핵심:

```text
Symptom
↓
Layer 구분
↓
범위 축소
↓
원인 확인
↓
복구
```

---

# 15.10 Final Architecture Design

## 15.75 전체 구조

최종 AI Platform은 크게 다음 영역으로 볼 수 있다.

```text
1. User / Application
2. Application Platform
3. AI Serving Platform
4. Infrastructure
5. Platform Management
```

전체:

```text
                         User / Developer
                                │
                         HTTPS / API
                                ↓
                    Load Balancer / Gateway
                                ↓
                ┌───────────────┴───────────────┐
                ↓                               ↓
           Backend API                      LiteLLM
                │                               │
      ┌─────────┼─────────┐            Auth / Quota / Routing
      ↓         ↓         ↓                    ↓
 PostgreSQL   Redis      Kafka             vLLM Pool
                          ↓                    ↓
                        Worker          GPU Node Pool
```

---

## 15.76 Platform Management Layer

전체를 관리하는 기술:

```text
Terraform
Argo CD
Helm
Kubernetes
Monitoring
Security
Governance
Developer Portal
```

---

## 15.77 User Request Path

```text
User
↓
Load Balancer / Ingress
↓
LiteLLM
↓
vLLM
↓
GPU
↓
Streaming Response
```

LiteLLM:

```text
Authentication
Authorization
Rate Limit
Quota
Cache
Routing
Retry / Fallback
```

vLLM:

```text
Prefill
KV Cache
Continuous Batching
PagedAttention
Decode
```

---

## 15.78 Application Platform

```text
Backend
├─ PostgreSQL
├─ Redis
├─ Kafka
└─ LiteLLM
```

역할:

```text
PostgreSQL
= 영구 데이터

Redis
= Cache / Session / 빠른 공유 상태

Kafka
= 비동기 Event

Backend
= Business Logic
```

---

## 15.79 AI Serving Platform

```text
                    LiteLLM
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       GLM Pool     Qwen Pool    External API
          │            │
      ┌───┴───┐    ┌───┴───┐
      ↓       ↓    ↓       ↓
    vLLM    vLLM vLLM    vLLM
      ↓       ↓    ↓       ↓
     GPU     GPU   GPU     GPU
```

역할:

```text
LiteLLM
= Gateway / Policy / Routing

vLLM
= Inference Engine

GPU
= Compute
```

---

## 15.80 Kubernetes Structure

```text
Kubernetes Cluster

General Node Pool
├─ Backend
├─ LiteLLM
├─ Worker
├─ Argo CD
└─ Platform Components

GPU Node Pool
├─ vLLM GLM
├─ vLLM GLM
└─ vLLM Qwen
```

---

## 15.81 Infrastructure Layer

```text
Terraform
↓
VPC
Subnet
Load Balancer
EKS
General Node Pool
GPU Node Pool
RDS
Storage
IAM
```

역할 분리:

```text
Terraform
= Infrastructure Desired State

Argo CD
= Kubernetes Application Desired State
```

---

## 15.82 Deployment Flow

```text
Developer
↓
Git Push / PR
↓
CI
├─ Test
├─ Build
├─ Security Scan
└─ Image Push
↓
Registry
↓
Deployment Git
↓
Argo CD
↓
Helm
↓
Kubernetes
```

AI Model:

```text
New vLLM Replica
↓
Model Load
↓
Readiness
↓
LiteLLM Canary
↓
5% → 20% → 100%
```

---

## 15.83 Reliability

```text
LiteLLM
→ Multiple Replicas

Backend
→ Multiple Replicas

vLLM
→ Multiple Replicas

PostgreSQL
→ Primary / Standby

Redis
→ Replication / Sentinel / Cluster

Kafka
→ Replication / ISR
```

Failure Domain:

```text
Pod
↓
Node
↓
AZ
```

핵심:

```text
Replica
+
Anti-Affinity
+
Multi-AZ
+
Retry
+
Fallback
+
Spare Capacity
```

---

## 15.84 Security

전체:

```text
User
↓
Authentication
↓
Authorization
↓
TLS
↓
Gateway
↓
NetworkPolicy
↓
Service
```

Cluster 내부:

```text
RBAC
ServiceAccount
Secrets
NetworkPolicy
Container Security
Image Scan
```

보안 Layer:

```text
Identity
→ Permission
→ Network
→ Secret
→ Container
→ Image
```

---

## 15.85 Multi-tenancy

여러 팀이 하나의 Platform을 사용하면:

```text
Namespace
RBAC
NetworkPolicy
ResourceQuota
GPU Quota
LiteLLM TPM / RPM / Concurrency
Cost Attribution
```

까지 함께 관리한다.

AI Platform에서는 특히:

```text
GPU
Context
Concurrency
Token Usage
```

를 관리해야 Noisy Neighbor를 줄일 수 있다.

---

## 15.86 Self-Service

```text
Developer
↓
Developer Portal
↓
Platform API
↓
Policy / Governance
↓
Automation
↓
Terraform / GitOps
```

요청별:

```text
Infrastructure Request
→ Terraform

Application Request
→ Git + Argo CD

Model Endpoint Request
→ vLLM + GPU + LiteLLM
```

목표:

> 개발자가 Kubernetes / GPU / Terraform 내부 구현을 몰라도 표준화된 Platform 기능을 사용할 수 있게 한다.

---

## 15.87 Observability

전체 Layer를 관찰할 수 있어야 한다.

```text
Application
→ Request Latency / Error

LiteLLM
→ RPM / TPM / Routing / Quota

vLLM
→ TTFT / TPOT / Queue

GPU
→ Utilization / VRAM

Kubernetes
→ Pod / Node / Scheduling

PostgreSQL
→ Connection / Query / Lock

Kafka
→ Consumer Lag
```

장애 시:

```text
User
↓
Gateway
↓
Backend / LiteLLM
↓
vLLM
↓
GPU
```

순으로 Layer를 좁힌다.

---

# Final Architecture

```text
                         Developer
                             │
                      Developer Portal
                             │
                       Platform API
                             │
                  Policy / Governance
                             │
             ┌───────────────┴───────────────┐
             ↓                               ↓
         Terraform                        GitOps
             ↓                               ↓
     Cloud Infrastructure                 Argo CD
             │                               ↓
             └──────────────┬───────────────┘
                            ↓
                     Kubernetes Cluster
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
       Backend           LiteLLM            Worker
     /    |    \             │
    ↓     ↓     ↓            ↓
Postgres Redis Kafka      vLLM Pool
                            ↓
                         GPU Pool
```

전체 공통 Layer:

```text
Security
Reliability
Observability
Quota
Cost
Governance
```

---

# Final Mental Model

## Linux → Kubernetes

```text
Linux Process
↓
Container
↓
Pod
↓
Deployment / Service
↓
Kubernetes Cluster
↓
Cloud Infrastructure
```

## AI Serving

```text
Application
↓
LiteLLM
↓
vLLM
↓
GPU
```

## Deployment

```text
Git
↓
CI
↓
Image
↓
Helm
↓
Argo CD
↓
Kubernetes
```

## Platform

```text
Developer Portal
↓
Platform API
↓
Policy
↓
Automation
↓
Terraform / GitOps
```

---

# Basic 과정의 최종 목표

이 과정의 목적은 각 기술의 내부 구현을 모두 외우는 것이 아니다.

최종적으로 다음을 판단할 수 있어야 한다.

- 각 기술이 시스템에서 어디에 위치하는가
- 왜 필요한가
- 어떤 역할과 책임을 가지는가
- 다른 기술과 어떻게 연결되는가
- 장애 발생 시 어느 Layer부터 확인해야 하는가
- Resource / Security / Cost / Reliability를 어떻게 함께 고려하는가

즉:

> **전체 시스템을 보고 구조를 설계하고, AI 또는 자동화가 만든 구현 결과를 검증하고, 장애와 성능 문제의 범위를 판단할 수 있는 Platform Engineering 기본기**를 갖추는 것이 목표다.

---

# Curriculum Completion

```text
Chapter 12 Terraform & Infrastructure as Code ✅
Chapter 13 Multi-tenancy, Quotas & Cost Control ✅
Chapter 14 Internal Developer Platform / Self-Service ✅
Chapter 15 End-to-End AI Platform Architecture ✅
```

**Platform / Infrastructure / AI Serving Basic 완료**
