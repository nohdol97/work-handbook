---
id: platform-developer-platform
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - PIS4-14-01
  - PIS4-14-02
  - PIS4-14-03
  - PIS4-14-04
  - PIS4-14-05
  - PIS4-14-06
  - PIS4-14-07
  - PIS4-14-08
  - PIS4-14-09
  - PIS4-14-10
  - PIS4-14-11
  - PIS4-14-12
  - PIS4-14-13
  - PIS4-14-14
  - PIS4-14-15
  - PIS4-14-16
  - PIS4-14-17
  - PIS4-14-18
  - PIS4-14-19
  - PIS4-14-20
  - PIS4-14-21
  - PIS4-14-22
  - PIS4-14-23
  - PIS4-14-24
---

# Chapter 14. Internal Developer Platform / Self-Service

예시 구성과 명령은 학습용이며 실제 배포·장애 실험 결과가 아니다.

<!-- SOURCE CORE START -->

## 14.1 Platform as a Product

개발자 플랫폼은 필요한 환경을 신청하는 셀프서비스 창구와 비슷하다. 요청이 승인되어도 실제 GPU나 저장소가 준비되고 서비스가 Ready가 되어야 사용할 수 있다.

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

**CRD와 Controller의 역할**

CRD는 Resource 종류를 등록한다. Custom Resource만으로는 구조화된 데이터를 저장·조회하며, 원하는 상태를 실제 배포로 만드는 동작은 Controller가 구현한다. 원문의 YAML은 `apiVersion`·`metadata` 등을 생략한 개념 예시이며 바로 적용할 완성된 manifest가 아니다. LiteLLM 등록 역시 Kubernetes가 자동 제공하는 기능이 아니라 Platform Controller의 구현 범위다. [Kubernetes Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)

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

**승인·용량·삭제의 확인 지점**

설계 권고: 승인할 때 요청 내용·정책 버전·비용 근거를 함께 기록하고, 실제 실행 직전에 용량을 다시 확인한다. 승인 대기 중 다른 요청이 GPU를 사용할 수 있으므로 “승인됨”과 “배치 가능”을 같은 상태로 취급하지 않는다. 재시도로 중복 Resource가 생기지 않도록 요청 식별자와 생성 결과를 연결하고, 중간 실패의 남은 Resource도 표시한다.

14.14의 Endpoint 반환 전에는 model readiness뿐 아니라 인증·quota·라우팅이 의도대로 동작하는지 요청으로 확인하는 편이 좋다. 14.17의 삭제 순서는 개념 흐름이다. 실제 절차에는 진행 중 요청 처리, 다른 서비스와 공유한 DNS·Secret의 소유권 확인, 반환된 GPU와 남은 과금 Resource 확인을 넣는다. Endpoint 삭제 요청 접수만으로 정리 완료를 보고하지 않는다.

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

**Quota와 실제 용량**

ResourceQuota는 Namespace 단위의 총 Resource 사용 제약이다. 예를 들어 `nvidia.com/gpu` 확장 Resource에는 `requests.nvidia.com/gpu: 4`로 요청 총량을 제한할 수 있다. 이 제한은 GPU 예약이나 특정 모델의 성능 보장이 아니다. Team A가 여러 Namespace를 쓰면 팀 전체 상한을 별도로 설계해야 한다. [Kubernetes Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)

LLM token·비용 quota와 GPU 개수는 서로 다른 단위다. 14.13의 Model·Precision·Context·Concurrency 입력으로 GPU당 메모리·배치 가능성·목표 응답 지연을 확인하는 과정은 별도로 남겨 둔다. 관련: [GPU 용량 계획](gpu-infrastructure.md), [멀티테넌시와 비용](multitenancy-cost.md).

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

**Governance의 연결 지점**

Platform Governance와 Data Governance는 구분되는 영역이지만 모델 Endpoint의 데이터 접근·로그 보존·소유자 정책에서는 함께 검토할 수 있다. 설계 시 Resource 생성 권한만으로 학습 데이터·프롬프트·응답 로그 접근 권한까지 허용했다고 해석하지 않는다.

---

<!-- SOURCE CORE END -->

## 관련 문서

- [플랫폼 인프라 학습 지도](index.md)
- [Terraform과 IaC](terraform-iac.md)
- [멀티테넌시와 비용](multitenancy-cost.md)
- [전체 AI 플랫폼 아키텍처](architecture.md)

## 핵심 정리

셀프서비스는 요청을 빠르게 하지만 승인과 실제 리소스 준비 상태는 따로 확인해야 한다.

## LLM in Practice

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    GPU가 부족한 상태에서 모델 endpoint 요청이 승인 대기 중이야. 요청 상태, quota, 실제 배치 가능 용량과 부분 실패 후 남은 리소스를 검토해 진행 가능 조건을 알려 줘. 승인을 대신하거나 리소스를 생성하지 마.
    ```

=== "English"

    ```text {.prompt}
    A model endpoint request is awaiting approval while GPU capacity is short. Review request state, quota, schedulable capacity, and resources left after partial failures. State what is needed to proceed without granting approval or creating resources.
    ```

**핵심 사항:** 승인·quota·배치 가능성을 구분한 진행/중단 표와 중복 생성·부분 실패 정리의 확인 목록. Quota가 남으면 GPU도 비어 있다고 가정하거나 승인 기록만으로 모델 성능을 보장할 수 있다. 실제 Resource를 확인하지 않고 요청 재시도나 삭제를 안전하다고 단정할 수 있다. 정책 버전과 승인 범위, 같은 시각의 실제 GPU 배치·quota 사용량, 요청 식별자별 생성 결과를 대조한다. 목표 context·concurrency에서 측정한 응답 지연과 오류를 확인한다. 이 시나리오는 검토용 예시이며 실제 모델 실행·성능 검증 기록이 아니다.
