---
id: platform-terraform-iac
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - PIS4-12-01
  - PIS4-12-02
  - PIS4-12-03
  - PIS4-12-04
  - PIS4-12-05
  - PIS4-12-06
  - PIS4-12-07
  - PIS4-12-08
  - PIS4-12-09
  - PIS4-12-10
---

# Chapter 12. Terraform & Infrastructure as Code

제공된 학습 원문의 번호·순서·예시를 그대로 보존했다. 12.3–12.5의 State 보안·S3 locking·승인된 Plan 적용 조건과 12.9의 Workspace 격리 한계는 뒤의 별도 보완에서 확인한다. 예시는 실제 인프라 실행 결과가 아니다.

<!-- SOURCE CORE START -->

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

<!-- SOURCE CORE END -->

## 보완 — State 보호와 실행 경계

2026-10-05 공식 문서를 확인했다. Terraform 실행·Cloud 변경·State 복구는 수행하지 않았다.

### 12.3 / 12.4 State와 Plan의 민감정보

State와 저장된 Plan에는 비밀번호 같은 민감정보가 포함될 수 있다. `sensitive = true`는 표시를 숨기는 설정이며 파일에서 값을 제거하지 않는다. State·Plan을 Git이나 공개 CI 로그에 올리지 않고 저장소 접근·암호화·보존 정책을 함께 관리한다. [Terraform sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)

### 12.4 S3 locking은 명시적으로 활성화

S3 backend의 `use_lockfile` 기본값은 `false`다. Remote State를 설정했다는 사실만으로 동시 쓰기가 보호되지는 않는다. 활성화 시 `.tflock` 객체에 필요한 읽기·쓰기·삭제 권한을 확인한다. DynamoDB locking은 공식적으로 deprecated이며, 이행 중에는 두 방식을 함께 설정할 수 있다. State 복구를 위해 bucket versioning도 확인한다. [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)

### 12.5 / 12.10 검토한 Plan과 실제 적용

Plan 파일 없이 `terraform apply`를 실행하면 새 Plan을 만든다. 검토한 변경을 적용하려면 저장한 Plan과 승인 대상을 연결해야 한다. 저장된 Plan을 전달하면 추가 대화형 확인 없이 실행되므로 승인 Gate는 그 앞에 있어야 한다. Apply가 일부 성공한 뒤 실패해도 자동 rollback되지는 않는다. State 복구와 실제 Cloud 변경 복구를 별도로 검토한다. [Terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply)

### 12.9 CLI Workspace와 접근 경계

여기서 말하는 Workspace는 Terraform CLI의 State workspace다. 별도 자격증명·접근제어가 필요한 배포나 시스템 분해에는 적합하지 않다. 디렉터리만 나누어도 권한이 분리되는 것은 아니므로 backend State 위치와 실행 자격증명을 함께 확인한다. [Terraform workspaces](https://developer.hashicorp.com/terraform/language/state/workspaces)

## 관련 문서

- [Platform 학습 지도](index.md)
- [CI/CD와 GitOps](cicd-gitops.md)
- [Platform 보안](platform-security.md)
- [멀티테넌시와 비용](multitenancy-cost.md)
