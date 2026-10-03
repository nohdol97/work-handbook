<!-- 반입 기록
범위: 플랫폼·인프라·AI 서빙 Basic 10~11장 전체 업로드
한계: 개념 학습 자료이며 명령 실행·운영 구축·성능 측정 결과가 아니다.
원본 bytes: 30821; SHA-256: 30aeff977286785ab2564310da337a67fc4fe1ae66f3094cbd023b8291b2f1bc
정규화: 없음. 원문의 hard break와 모든 byte를 경계 뒤에 그대로 보존한다.
whitespace_restoration: []
-->
<!-- ORIGINAL SOURCE START -->
# Platform / Infrastructure / AI Serving — Basic Study Notes

> 범위: Chapter 10 ~ Chapter 11  
> 이전 범위: Chapter 1~3, Chapter 4~9  
> 수준: Basic — 플랫폼 엔지니어가 반드시 알아야 할 핵심 개념 중심  
> 포함: 본 학습 내용 + 중간 실무 질문/보충 설명  
> 다음 학습 시작점: Chapter 12. Terraform & Infrastructure as Code

---

# Chapter 10. Platform Security

## 10.1 Authentication / Authorization

보안에서 가장 먼저 구분해야 하는 것은:

```text
Authentication
Authorization
```

이다.

### Authentication

Authentication은:

> 누구인지 확인하는 것

이다.

예:

```text
사용자 로그인
API Key
Service Account
SSO
```

흐름:

```text
Request
↓
Identity 확인
↓
"누구인지" 판별
```

### Authorization

Authorization은:

> 그 사용자가 무엇을 할 수 있는지 결정하는 것

이다.

예:

```text
User A
→ Model 조회 가능
→ Deployment 수정 불가

Admin
→ Deployment 수정 가능
→ Secret 관리 가능
```

즉:

```text
Authentication
= 누구인가?

Authorization
= 무엇을 할 수 있는가?
```

### IAM

IAM = Identity and Access Management.

쉽게 말하면:

> 사용자, 서비스, 권한을 중앙에서 관리하는 체계

이다.

예:

```text
User
Team
Service
Role
Permission
```

Cloud에서는 AWS IAM 같은 형태로 많이 본다.

### Service Identity

사람뿐 아니라 서비스도 신원을 가진다.

예:

```text
Backend API
↓
PostgreSQL

LiteLLM
↓
vLLM

Application
↓
Kafka
```

이때:

```text
"이 요청이 어느 서비스에서 왔는가?"
```

를 확인할 수 있어야 한다.

이를 Service Identity라고 생각하면 된다.

### User Identity vs Service Identity

```text
User Identity
→ 사람

Service Identity
→ Application / Pod / Service
```

예:

```text
개발자 A
→ Kubernetes 조회 권한

Backend Service
→ PostgreSQL 연결 권한
```

### Least Privilege

보안의 중요한 원칙:

> 필요한 권한만 최소한으로 준다.

나쁜 예:

```text
모든 서비스
→ Admin 권한
```

좋은 예:

```text
Backend
→ 특정 DB만 접근

LiteLLM
→ 특정 Secret만 읽기

Monitoring
→ 조회 권한만
```

### 핵심 정리

```text
Authentication
= 누구인가?

Authorization
= 무엇을 할 수 있는가?

IAM
= 사용자 / 서비스 / 권한을 관리하는 체계

Service Identity
= 서비스 자체의 신원

Least Privilege
= 필요한 권한만 최소한으로 부여
```

---

## 10.2 Kubernetes RBAC

RBAC = Role-Based Access Control.

> 누가 Kubernetes에서 어떤 작업을 할 수 있는지 권한을 제어하는 방식

핵심:

```text
Role
ClusterRole
RoleBinding
ServiceAccount
```

### Role

특정 Namespace 안에서의 권한을 정의한다.

예:

```text
developer-role

pods
→ get
→ list

deployments
→ get
→ update
```

즉:

> Role = Namespace 단위 권한 정의

### RoleBinding

Role을 실제 사용자나 ServiceAccount에 연결한다.

```text
developer-role
↓
RoleBinding
↓
User A
```

### ClusterRole

Namespace 하나에 한정되지 않는 Cluster 범위 권한.

예:

```text
모든 Namespace의 Pod 조회
Node 조회
Cluster 전체 Resource 조회
```

구분:

```text
Role
→ Namespace 범위

ClusterRole
→ Cluster 범위
```

### ServiceAccount

Pod가 Kubernetes API를 호출할 때 사용하는 Identity.

예:

```text
Backup Pod
↓
Kubernetes API
↓
특정 PVC 정보 조회
```

구조:

```text
Pod
↓
ServiceAccount
↓
RoleBinding
↓
Role
```

### 왜 ServiceAccount가 중요한가

나쁜 예:

```text
모든 Pod
→ Cluster Admin
```

Pod 하나가 침해되면 Cluster 전체가 위험해질 수 있다.

좋은 예:

```text
Monitoring Pod
→ 조회만

Deployment Controller
→ 필요한 Deployment 수정만

Backup Pod
→ 필요한 Storage Resource만 접근
```

### 핵심 정리

```text
Role
= Namespace 안의 권한 정의

ClusterRole
= Cluster 범위 권한 정의

RoleBinding
= 권한을 User / ServiceAccount에 연결

ServiceAccount
= Pod / Application의 Kubernetes Identity
```

---

## 10.3 Secrets

Secret은:

> Password, API Key, Token, Certificate 같은 민감한 값을 안전하게 관리하는 것

핵심:

```text
Kubernetes Secret
External Secrets
Vault / Secret Manager
Secret Rotation
```

### Kubernetes Secret

예:

```text
DB_PASSWORD
API_KEY
JWT_SECRET
```

Pod에서는:

```text
Environment Variable
또는
File Mount
```

형태로 사용 가능.

```text
Pod
↓
Kubernetes Secret
↓
DB_PASSWORD
```

### Kubernetes Secret이라고 자동으로 완벽히 안전한 것은 아님

특히 Manifest에 Secret 값을 직접 적고 Git에 올리면:

```text
Git Repository
↓
Secret 노출
```

이 될 수 있다.

기본 원칙:

> Secret 값을 Git에 평문으로 넣지 않는다.

### External Secret Store

Production에서는 실제 Secret 원본을 Kubernetes 밖에 두는 경우가 많다.

예:

```text
AWS Secrets Manager
HashiCorp Vault
Cloud Secret Manager
```

구조:

```text
External Secret Store
↓
External Secrets Controller
↓
Kubernetes Secret
↓
Pod
```

### Vault

Vault 같은 시스템은 Secret 관리 전용 시스템이다.

예:

```text
Database Password
API Token
Certificate
```

장점:

```text
접근 제어
Audit
Secret Rotation
동적 Credential
```

Basic에서는:

> Vault = 중앙 Secret 금고

정도로 이해하면 된다.

### Secret Rotation

Secret 값을 주기적으로 변경하는 것.

예:

```text
DB Password v1
↓
새 Password v2 생성
↓
Application 설정 변경
↓
v1 폐기
```

### Application에 Secret을 직접 박지 않기

나쁜 예:

```python
DB_PASSWORD = "password123"
```

좋은 구조:

```text
Application
↓
Environment Variable / Mounted Secret
↓
Secret Store
```

즉:

```text
Code / Image
≠
Secret
```

### Least Privilege와 연결

```text
LiteLLM Pod
→ LiteLLM 관련 API Key만

Backend Pod
→ 해당 DB Password만

Kafka Client
→ Kafka Credential만
```

### 핵심 정리

```text
Kubernetes Secret
= Pod에 민감한 설정 전달

Secret 값을 Git에 평문 저장하면 안 됨

External Secret Store
= 실제 Secret을 외부에서 중앙 관리

Vault / Secrets Manager
= Secret 전용 관리 시스템

Secret Rotation
= Secret 값을 주기적으로 교체
```

---

## 10.4 Network Security

Network Security는:

> 어떤 서비스가 어떤 서비스와 통신할 수 있는지 제한하는 것

핵심:

```text
NetworkPolicy
Firewall
Security Group
Service-to-Service Isolation
```

### 기본적으로 다 열어두면 위험

예:

```text
Frontend
Backend
PostgreSQL
Redis
Kafka
```

좋은 구조:

```text
Frontend
→ Backend만 접근

Backend
→ PostgreSQL / Redis 접근

Frontend
→ PostgreSQL 직접 접근 불가
```

### NetworkPolicy

Kubernetes에서 Pod 간 통신을 제한하는 Resource.

예:

```text
Backend Pod
↓
PostgreSQL Pod
```

만 허용하고 다른 Pod는 차단.

즉:

> NetworkPolicy = Pod 수준 네트워크 접근 제어

### Ingress / Egress

Ingress:

```text
Client
→ Pod
```

Pod로 들어오는 트래픽.

Egress:

```text
Pod
→ PostgreSQL
```

Pod에서 나가는 트래픽.

예:

```text
LiteLLM
→ vLLM 허용
→ 인터넷 직접 접근 제한
```

### Firewall / Security Group

보통 Node나 Cloud Network 수준.

```text
Internet
↓
Firewall / Security Group
↓
Load Balancer
↓
Kubernetes
```

구분:

```text
Security Group / Firewall
→ Network / Server 수준

NetworkPolicy
→ Kubernetes Pod 수준
```

### Service-to-Service Isolation

AI Platform 예:

```text
User
↓
LiteLLM
↓
vLLM
```

만 허용.

또:

```text
LiteLLM
→ Redis 허용
→ PostgreSQL 허용

vLLM
→ Redis 접근 불필요
→ 차단
```

### Default Deny

```text
기본 차단
→ 필요한 통신만 허용
```

예:

```text
모든 Pod 통신 차단
↓
Backend → PostgreSQL 허용
LiteLLM → vLLM 허용
Monitoring → Metrics Port 허용
```

### CNI와 연결

```text
NetworkPolicy
↓
Calico / Cilium
↓
실제 Packet 허용 / 차단
```

즉:

```text
Kubernetes
→ 정책 정의

CNI
→ 정책 실행
```

### 보충: LiteLLM ↔ vLLM에서 Ingress/Egress

LiteLLM이 vLLM에 연결을 시작한다면:

```text
LiteLLM Pod
   ↓
 egress
   ↓
vLLM Pod
 ingress
```

즉:

```text
LiteLLM 쪽
→ vLLM으로 나가는 Egress 허용

vLLM 쪽
→ LiteLLM에서 들어오는 Ingress 허용
```

연결이 허용된 후에는 해당 연결에 대한 응답 패킷은 왕복할 수 있다.

중요한 기억법:

```text
A → B

A 입장
= Egress

B 입장
= Ingress
```

### 핵심 정리

```text
NetworkPolicy
= Pod 간 통신 제어

Ingress
= 들어오는 트래픽

Egress
= 나가는 트래픽

Firewall / Security Group
= Network / Node 수준 제어

Default Deny
= 기본 차단 후 필요한 통신만 허용
```

---

## 10.5 TLS / mTLS

TLS:

> 네트워크로 오가는 데이터를 암호화하는 기술

핵심:

```text
TLS
Certificate
mTLS
Certificate Rotation
```

### 왜 TLS가 필요한가

예:

```text
LiteLLM
↓ HTTP
vLLM
```

LLM 요청에는:

```text
Prompt
회사 내부 데이터
Source Code
API 정보
```

가 포함될 수 있다.

TLS 사용:

```text
LiteLLM
↓ HTTPS / 암호화
vLLM
```

### Certificate

TLS에서 서버의 신원을 확인하는 데 사용.

```text
Client
↓
"정말 내가 접속하려던 서버인가?"
↓
Server Certificate 확인
```

### 일반 TLS

보통:

```text
Client
→ Server Certificate 확인
```

사용자 인증은 별도로:

```text
API Key
JWT
SSO
```

등으로 수행.

### mTLS

mTLS = Mutual TLS.

서버와 클라이언트가 서로 Certificate를 확인.

```text
LiteLLM
Certificate
   ↕
Certificate
vLLM
```

즉:

```text
LiteLLM
→ "너 진짜 vLLM 맞아?"

vLLM
→ "너 진짜 허용된 LiteLLM 맞아?"
```

### mTLS와 Service Identity

서비스마다 Certificate를 부여해 Service Identity를 증명할 수 있다.

```text
LiteLLM Certificate
vLLM Certificate
Backend Certificate
```

### NetworkPolicy와 TLS 차이

```text
NetworkPolicy
= 누가 연결할 수 있는가

TLS
= 연결된 통신 내용을 암호화

mTLS
= 암호화 + 서로의 Service Identity 확인
```

### Certificate Rotation

```text
Certificate v1
↓
만료 가까워짐
↓
Certificate v2 발급
↓
서비스 교체
↓
v1 폐기
```

### 핵심 정리

```text
TLS
= 통신 암호화 + 서버 신원 확인

Certificate
= 서비스의 신원을 증명

mTLS
= Client와 Server가 서로 Certificate 확인

Certificate Rotation
= Certificate를 주기적으로 갱신
```

---

## 10.6 Container Security

핵심 목표:

> Container가 침해되더라도 Host나 다른 Container까지 피해가 커지지 않게 제한

핵심:

```text
Non-root
Linux Capabilities
Seccomp
Read-only Filesystem
```

### Non-root

나쁜 예:

```text
Container Process
→ root
```

가능하면:

```text
Container Process
→ 일반 User
```

Kubernetes 예:

```yaml
securityContext:
  runAsNonRoot: true
```

### Linux Capabilities

root 권한을 세부 권한으로 나눈 개념.

원칙:

```text
기본 Capability 최소화
↓
정말 필요한 것만 추가
```

### Privileged Container

매우 강한 Host 권한을 가진 Container.

```text
Container
↓
Host Device / Kernel 기능 접근
```

일반 App에서는 피하고, 특수 Agent 등에 예외적으로 사용.

### Seccomp

Process가 사용할 수 있는 Linux syscall을 제한.

```text
Container Process
↓
System Call
↓
Seccomp Policy
├─ 허용
└─ 차단
```

### Read-only Filesystem

Container root filesystem을 읽기 전용으로 설정.

```text
/app
/bin
/etc
→ 수정 불가
```

필요한 쓰기 공간만:

```text
/tmp
/data
```

Volume으로 별도 허용.

### Kubernetes securityContext

Pod/Container Linux 보안 권한을 설정하는 곳.

예:

```yaml
securityContext:
  runAsNonRoot: true
  readOnlyRootFilesystem: true
```

### 핵심 정리

```text
Non-root
= root로 실행하지 않기

Linux Capabilities
= 필요한 Linux 권한만 허용

Privileged Container
= 매우 강한 권한
= 일반 App에서는 피하기

Seccomp
= 사용할 수 있는 syscall 제한

Read-only Filesystem
= Container 내부 변조 제한
```

---

## 10.7 Supply Chain Security

Supply Chain Security:

> 배포하는 Container Image와 Library가 안전한지 확인하는 것

핵심:

```text
Image Scanning
SBOM
Image Signing
Registry Security
```

### Image Scanning

```text
my-app:v1
↓
Image Scanner
↓
OpenSSL 취약점 발견
```

CI에 넣을 수 있다.

```text
Code
↓
Image Build
↓
Security Scan
↓
Registry Push
```

### SBOM

SBOM = Software Bill of Materials.

> Software 안에 무엇이 들어 있는지 적어놓은 부품 목록

예:

```text
Application Image
├─ Ubuntu
├─ Python
├─ FastAPI
├─ OpenSSL
├─ requests
└─ 기타 Library
```

### Image Signing

```text
Image Build
↓
Signing
↓
Signed Image
↓
Registry
```

배포 시 서명 검증 가능.

### Tag vs Digest

```text
Tag
→ 사람이 보기 좋은 버전
→ 바뀔 수 있음

Digest
→ 특정 Image content 고정 식별
```

### Registry Security

관리할 것:

```text
누가 Push?
누가 Pull?
누가 삭제?
취약점 Scan?
```

좋은 구조:

```text
Developer
→ 직접 Production Image 수정 불가

CI Pipeline
→ 검증 후 Push

Production
→ 승인된 Registry에서만 Pull
```

### 전체 CI/CD와 연결

```text
Code
↓
Build
↓
Test
↓
Container Image
↓
Image Scan
↓
SBOM
↓
Image Signing
↓
Registry
↓
Kubernetes Deploy
```

---

## 10.8 Multi-tenant Security

Multi-tenancy:

> 여러 팀이나 서비스가 하나의 Platform / Kubernetes Cluster를 같이 사용하는 구조

핵심:

```text
Namespace Isolation
RBAC
Network Isolation
Secret Isolation
Resource Isolation
```

### Namespace Isolation

예:

```text
namespace: team-a
namespace: team-b
namespace: team-c
```

Namespace는 기본적인 논리적 격리 단위.

하지만 Namespace만으로 완전한 보안 격리는 아니다.

### RBAC Isolation

```text
Developer A
→ team-a만 접근

Developer B
→ team-b만 접근
```

### Network Isolation

```text
team-a Pod
→ team-b DB 접근 금지
```

Default Deny 후 필요한 통신만 허용.

### Secret Isolation

각 ServiceAccount가 자기 Secret만 접근하도록 제한.

### Resource Isolation

한 팀이 CPU/Memory/GPU를 독점하지 않도록:

```text
ResourceQuota
LimitRange
GPU Quota
```

사용.

### Namespace는 팀 단위만이 아니다

Namespace 설계 기준:

```text
Service
Team
Environment
Security Boundary
Lifecycle
```

실무에서 흔한 패턴:

```text
<service>-<environment>
```

예:

```text
payment-dev
payment-staging
payment-prod

agent-platform-dev
agent-platform-prod
```

각 Namespace 안에:

```text
frontend
backend
worker
ConfigMap
Secret
Service
```

등을 같이 둘 수 있다.

### 서비스 단위 예

```text
my-service-dev
├─ frontend
├─ backend
├─ worker
└─ postgres

my-service-prod
├─ frontend
├─ backend
├─ worker
└─ postgres
```

### 팀 + 환경 패턴

```text
team-a-dev
team-a-prod
team-b-dev
team-b-prod
```

내부에 여러 서비스 배치 가능.

### DB는 꼭 같은 Namespace일 필요 없음

예:

```text
shopping-prod
├─ frontend
├─ backend
└─ worker

database-prod
└─ PostgreSQL
```

또는 Managed DB 사용 가능.

### Dev / Prod 분리

```text
myapp-dev
myapp-staging
myapp-prod
```

더 강한 격리가 필요하면:

```text
Dev Cluster
Prod Cluster
```

자체를 나누기도 한다.

### Chapter 10 최종 정리

```text
Identity
↓
RBAC
↓
Secret
↓
NetworkPolicy
↓
TLS / mTLS
↓
Container Hardening
↓
Supply Chain Security
↓
Multi-tenant Isolation
```

---

# Chapter 11. CI/CD, Helm, Argo CD & GitOps

## 11.1 CI/CD Fundamentals

CI/CD:

> 코드 변경을 테스트하고, 빌드하고, 실제 환경에 배포하는 과정을 자동화

핵심:

```text
CI
= Build + Test

CD
= Deploy
```

### CI

```text
Developer
↓
Git Push
↓
CI Pipeline
├─ Unit Test
├─ Lint
├─ Security Scan
└─ Docker Image Build
```

### CD

```text
CI 성공
↓
Container Image
↓
Registry
↓
CD
↓
Kubernetes
```

### 전체 Pipeline

```text
Developer
↓
Git Push
↓
CI
├─ Test
├─ Build
└─ Image Scan
↓
Container Image
↓
Registry
↓
CD
↓
Kubernetes
```

### CI vs GitOps

전통적 CD:

```text
CI Pipeline
↓
kubectl / Helm
↓
Kubernetes
```

GitOps:

```text
CI
↓
Git의 Deployment 설정 변경

Argo CD
↓
Git 확인
↓
Kubernetes
```

핵심:

```text
CI
= Application을 만들고 검증

GitOps
= 어떤 버전을 Cluster에 배포할지 관리
```

---

## 11.2 Container Build Pipeline

> 소스 코드를 Container Image로 만들고 Registry에 저장하는 과정

핵심:

```text
Build
Tag
Push
Versioning
```

### Build

```text
Source Code
↓
Dockerfile
↓
docker build
↓
Container Image
```

### Tag

예:

```text
my-api:1.0
my-api:1.1
my-api:20261003
```

Production에서는 `latest`만 쓰는 것보다 명확한 버전을 사용.

### Git Commit과 Image 연결

```text
Git commit
a1b2c3d
↓
Build
↓
my-api:a1b2c3d
```

### Registry Push

```text
CI
↓
my-api:1.3
↓
Container Registry
```

### Build once, deploy many

같은 Image를:

```text
dev
staging
prod
```

에 사용.

환경 차이는:

```text
ConfigMap
Secret
Helm Values
```

로 분리.

### 핵심 흐름

```text
Git Commit
↓
Test
↓
Build
↓
Tag
↓
Security Scan
↓
Registry Push
```

---

## 11.3 Helm

Helm:

> Kubernetes YAML을 템플릿화해서 여러 환경과 서비스에 재사용하기 위한 패키지 관리자

핵심:

```text
Chart
Template
Values
Release
Upgrade / Rollback
```

### Chart

```text
my-api-chart/
├─ Chart.yaml
├─ values.yaml
└─ templates/
   ├─ deployment.yaml
   ├─ service.yaml
   └─ ingress.yaml
```

### Template

```yaml
replicas: {{ .Values.replicaCount }}

image:
  repository: {{ .Values.image.repository }}
  tag: {{ .Values.image.tag }}
```

### Values

```yaml
replicaCount: 3

image:
  repository: my-api
  tag: "1.3"
```

관계:

```text
Template
= 배포 구조

Values
= 실제 설정값
```

### 환경별 Values

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

### Release

Chart를 실제 Cluster에 배포한 인스턴스.

```text
Chart
= my-api

Release
= my-api-prod
```

### Upgrade / Rollback

```text
my-api:v1
↓
my-api:v2
↓ 문제
Rollback
↓
v1
```

### Helm을 이렇게 이해하면 된다

```text
Kubernetes 구성요소
Deployment / Service / Ingress / ConfigMap ...
↓
Helm Template로 공통화

환경별 차이
replica / image tag / CPU / domain ...
↓
Values
```

즉:

> 배포 구조는 Template으로 재사용하고, 환경별 차이는 Values로 주입

### Helm Release 정보는 어디 저장되는가

Helm 3 기준 기본적으로 해당 Release가 설치된 Kubernetes Namespace의 Secret에 저장.

예:

```text
Namespace: my-api-prod

├─ Deployment
├─ Service
├─ ConfigMap
└─ Helm Release Secret
```

Revision 예:

```text
sh.helm.release.v1.my-api.v1
sh.helm.release.v1.my-api.v2
sh.helm.release.v1.my-api.v3
```

확인:

```bash
helm history my-api
```

Rollback:

```bash
helm rollback my-api 2
```

### Chart vs Release

```text
Chart
= 설계도 / Template 패키지

Release
= Chart를 실제 Cluster에 설치한 기록 + 상태
```

### Image 버전도 Helm Values에 관리 가능

```yaml
image:
  repository: registry.example.com/my-api
  tag: "1.3.0"
```

Template:

```yaml
containers:
  - name: my-api
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
```

### Chart Version vs Image Tag

```text
Chart Version
→ 배포 구조의 버전

Image Tag
→ Application 코드 버전
```

---

## 11.4 Environment Management

> 같은 애플리케이션을 dev / staging / prod에 배포하되 환경별 설정만 안전하게 다르게 관리

핵심:

```text
같은 Image
+
같은 Helm Template
+
환경별 Values
```

### Image는 동일하게

```text
Dev     → my-api:1.5.0
Staging → my-api:1.5.0
Prod    → my-api:1.5.0
```

### 환경별 Configuration

예:

```text
Replica 수
CPU / Memory
Domain
DB 주소
Log level
Autoscaling
```

### Namespace 분리

```text
my-api-dev
my-api-staging
my-api-prod
```

환경별:

```text
Secret
ConfigMap
ResourceQuota
NetworkPolicy
RBAC
```

분리 가능.

### Secret은 Values에 평문 저장하지 않기

좋은 구조:

```text
Helm Values
→ Secret 이름만 참조

실제 Secret
→ Vault / Secrets Manager / External Secrets
```

### Promotion

```text
Image Build
↓
Dev
↓
Staging
↓
Prod
```

환경마다 새 Image를 Build하지 않고 같은 artifact를 승격.

### Git 구조 예

```text
deploy/
├─ chart/
├─ dev/
│  └─ values.yaml
├─ staging/
│  └─ values.yaml
└─ prod/
   └─ values.yaml
```

핵심:

> Build once, deploy many

---

## 11.5 GitOps

GitOps:

> Kubernetes Desired State를 Git에 저장하고 실제 Cluster를 Git 상태와 계속 맞추는 운영 방식

### Source of Truth

Git:

```text
image.tag = 1.5.0
replicas = 3
```

Production도 이 상태여야 한다.

### 기존 배포 방식

```text
Developer
↓
Git Push
↓
CI
↓
helm upgrade / kubectl apply
↓
Kubernetes
```

### GitOps 방식

```text
Developer
↓
Git Push
↓
CI
├─ Test
├─ Build
└─ Registry Push
```

그 다음 배포 Git:

```yaml
image:
  tag: "1.5.0"
```

변경.

```text
Git
↓
Argo CD
↓
Kubernetes
```

### Pull-based Deployment

```text
Argo CD
→ Git 확인
→ Kubernetes 반영
```

### Drift

Git:

```text
replicas = 3
```

Cluster:

```text
replicas = 10
```

이면 Drift.

### Helm과 연결

```text
Helm
= Manifest 생성

Git
= Desired State 저장

Argo CD
= Git과 Cluster 동기화
```

### kubectl은 언제 쓰는가

GitOps 환경에서 kubectl은 주로:

```text
관찰
Troubleshooting
긴급 장애 대응
```

에 사용.

정상적인 설정/배포 변경은:

```text
Git + Argo CD
```

가 기본.

자주 쓰는 진단 명령:

```text
kubectl get pods
kubectl describe pod
kubectl get events
kubectl logs
kubectl logs --previous
kubectl exec
kubectl top
kubectl get pvc
kubectl get nodes
kubectl port-forward
```

Break-glass 예:

```bash
kubectl cordon node-a
kubectl drain node-a
```

긴급 조치 후 Git과 상태를 다시 맞춘다.

### Argo CD / Grafana / kubectl 역할 구분

```text
Argo CD
= 배포 상태 / Resource 구조 / Sync / Health

Grafana
= Metrics / Logs / Alert

kubectl
= Kubernetes 상세 진단 / 즉시 확인
```

### Argo CD에서도 Pod 상태 조회 가능

```text
Application
↓
Deployment
↓
ReplicaSet
↓
Pod
```

트리 구조로 Health 확인 가능.

그러나 상세 원인에는:

```text
kubectl describe
kubectl logs
events
```

가 더 직접적일 수 있다.

---

## 11.6 Argo CD

Argo CD:

> Git에 정의된 Kubernetes Desired State와 실제 Cluster 상태를 비교하고 동기화하는 GitOps Controller

핵심:

```text
Application
Sync
Health
Auto Sync
Self Heal
Prune
Rollback
```

### Application

배포 관리 단위.

대략:

```text
어느 Git Repository?
어느 경로?
어느 Revision?
어느 Cluster?
어느 Namespace?
```

를 정의.

### Sync

```text
Git Desired State
↓
Helm / Manifest Rendering
↓
Kubernetes 적용
↓
Actual State 일치
```

### Manual Sync

Git 변경 감지 후 OutOfSync까지만 표시하고 운영자가 Sync.

### Auto Sync

```text
Git 변경
↓
Argo CD 감지
↓
자동 Sync
↓
Kubernetes Update
```

### Self Heal

Cluster 직접 변경을 Git 상태로 복구.

### Prune

Git에서 사라진 Resource를 Cluster에서도 제거.

### Health

실제 Resource의 상태.

### Sync와 Health 차이

```text
Synced
= Git과 설정이 같다

Healthy
= Application이 정상 동작한다
```

따라서:

```text
Synced
but
Degraded
```

가능.

### Rollback

과거 synced revision으로 되돌릴 수 있으나 GitOps 원칙상 Git 상태도 rollback 상태와 맞추는 것이 중요.

### Helm과 Argo CD 역할

```text
Helm
= Kubernetes Manifest 생성

Argo CD
= Desired State를 Cluster와 동기화
```

### Argo CD에 Helm 경로를 알려줘야 하는가

Git 안의 Helm Chart를 쓰는 경우 Argo CD Application에:

```text
1. Git Repository
2. Branch / Commit
3. Helm Chart 경로
4. Values
5. 대상 Cluster / Namespace
```

를 알려준다.

예:

```yaml
spec:
  source:
    repoURL: ...
    targetRevision: main
    path: apps/my-api
```

Repository 예:

```text
platform-deploy/
├─ apps/
│  └─ my-api/
│     ├─ Chart.yaml
│     ├─ values.yaml
│     └─ templates/
└─ env/
   └─ prod/
      └─ values.yaml
```

### Argo CD Rollback과 Helm Release

Argo CD가 Helm을 사용하는 경우 Helm은 주로 Manifest Rendering 역할.

따라서:

```text
Argo CD rollback
→ 과거 Application revision
→ 당시 Chart + Values 렌더링
→ Kubernetes에 적용
```

이라고 이해하는 것이 정확.

단순히 Helm Release Secret 하나를 다시 활성화하는 개념과는 다름.

### Image 버전도 Helm Values에 작성 가능

```yaml
image:
  repository: registry.example.com/my-api
  tag: "1.3.0"
```

Git History:

```text
Commit A → 1.2.0
Commit B → 1.3.0
Commit C → 1.4.0
```

이전 Commit 상태로 돌아가면 이전 Image Tag가 다시 렌더링되어 적용될 수 있음.

---

## 11.7 Deployment Strategies

핵심:

```text
Rolling
Blue-Green
Canary
```

### Rolling Update

```text
v1 v1 v1
↓
v2 v1 v1
↓
v2 v2 v1
↓
v2 v2 v2
```

### Blue-Green

```text
Blue = 기존 Production
Green = 새 버전
```

Green 준비/검증 후 트래픽 전체 전환.

문제 시 Blue로 빠르게 원복.

### Canary

```text
95% → v1
5%  → v2
```

점진적으로:

```text
80 / 20
50 / 50
0 / 100
```

### AI Serving에서 Canary

새 Model은:

```text
응답 품질
TTFT
TPOT
VRAM
OOM
Tool Calling
출력 형식
```

등이 달라질 수 있으므로 일부 트래픽으로 먼저 검증.

---

## 11.8 AI Serving Deployment

AI Serving 배포는:

```text
Model Version
vLLM Version
Serving Configuration
GPU Capacity
```

를 함께 관리해야 한다.

### Model Version

예:

```text
vLLM Image
→ vllm:0.x

Model
→ glm-5.3-fp4-v1
```

Serving 설정:

```text
model
max_model_len
tensor_parallel_size
kv_cache_dtype
gpu_memory_utilization
```

도 Git에 기록하면 좋다.

### 새 모델을 바로 교체하면 위험

변할 수 있는 것:

```text
Weight 크기
VRAM 사용량
KV Cache 요구량
TTFT
TPOT
Throughput
응답 품질
Tool Calling
```

### vLLM Rollout

```text
새 vLLM / Model Pod
↓
Model Load
↓
GPU Memory 할당
↓
Startup Probe
↓
Readiness
```

Ready 된 뒤 트래픽 전달.

### LiteLLM Routing Migration

```text
100% → v1
0%   → v2

↓ Canary

95% → v1
5%  → v2

↓ 확대

80 / 20
50 / 50
0 / 100
```

### 역할 분리

```text
Argo CD
→ vLLM / Model Resource 배포

LiteLLM
→ 사용자 트래픽 전환
```

### 검증 지표

```text
Error Rate
TTFT
TPOT
Queue Time
GPU Utilization
VRAM / KV Cache
OOM
응답 품질
```

### Safe Rollback

문제 발생:

```text
20% → v1
80% → v2

↓ 문제

100% → v1
0%   → v2
```

그 후 Git / Argo CD에서 v2 Resource 제거 또는 수정.

---

## AI 모델 교체와 GPU / VRAM Capacity 보충

### 검증 기간에는 구 모델 + 신 모델 동시 Capacity 필요

예:

```text
기존 GLM-v1
→ GPU 4장

새 GLM-v2
→ GPU 4장

검증 기간
→ 최소 GPU 8장 수준 자원 필요
```

Blue-Green / Canary는 일시적인 추가 Capacity가 필요.

### 기존 3 Replica 예

```text
Replica A → GPU ×4
Replica B → GPU ×4
Replica C → GPU ×4

총 12 GPU
```

새 Canary:

```text
기존 12 GPU
+
신규 Replica D → GPU ×4
=
총 16 GPU
```

### Spare Capacity 용도

```text
Node/GPU 장애 대응
Rolling Update
Canary
Model Upgrade
Traffic Spike
```

### Spare GPU와 기존 Serving GPU의 남는 VRAM은 다름

예:

```text
B300 Node

GPU 0~3 → GLM Replica A
GPU 4~7 → Spare
```

Replica A가 사용하는 GPU 0~3:

```text
GPU 0~3 VRAM

├─ Model Weight
├─ KV Cache
├─ Activation
├─ Runtime Buffer
└─ 여유
```

여기서 남는 VRAM은 **Replica A의 KV Cache / Runtime Capacity**에 사용된다.

반면 GPU 4~7이 비어 있다면:

```text
GPU 4~7
= 새 Replica를 올릴 수 있는 Spare GPU
```

### 새 모델도 Weight + KV Cache가 모두 필요

```text
Spare GPU
↓
새 Model Weight
+
새 Model KV Cache
+
Activation
+
Runtime
```

이 모두 들어가야 한다.

따라서:

```text
새 Model Weight가 Spare GPU VRAM을 거의 100% 사용
→ KV Cache 공간 부족
→ Serving Capacity 부족
```

가능.

핵심:

> "모델이 GPU에 들어간다"와 "실제로 서비스 가능한 Capacity가 있다"는 다르다.

### VRAM은 기본적으로 GPU별 Local Memory

새 모델이 기존 Replica가 쓰는 GPU의 남는 VRAM을 자유롭게 공용 Pool처럼 빌려 쓰는 구조가 아니다.

```text
GPU 0~3
→ Old GLM Weight + KV Cache

GPU 4~7
→ New GLM Weight + KV Cache
```

### 진짜 Serving Spare Capacity 판단

```text
Spare GPU 수
↓
새 Model Weight가 들어가는가?
↓
KV Cache 공간도 충분히 남는가?
↓
목표 Context / Concurrency 가능한가?
↓
TTFT / TPOT SLA 가능한가?
```

특히 1M Context LLM에서는 Weight 외 KV Cache Capacity가 매우 중요하다.

---

# Chapter 10 ~ 11 전체 연결

```text
Platform Security

Identity
↓
RBAC
↓
Secrets
↓
NetworkPolicy
↓
TLS / mTLS
↓
Container Hardening
↓
Supply Chain Security
↓
Tenant Isolation
```

```text
CI/CD & GitOps

Developer
↓
Git
↓
CI
├─ Test
├─ Build
├─ Scan
└─ Registry Push
↓
Deployment Git
├─ Helm Chart
└─ Environment Values
↓
Argo CD
↓
Kubernetes
```

AI Serving까지 연결:

```text
Git
↓
Model / vLLM / Helm Values
↓
Argo CD
↓
vLLM Replica 배포
↓
Readiness
↓
LiteLLM Canary Routing
↓
Metrics / Quality 검증
↓
Traffic 확대 또는 Rollback
```

---

# 현재 전체 커리큘럼 상태

```text
1. Linux, Networking, Containers ✅
2. Kubernetes Core ✅
3. Kubernetes Production Operations ✅
4. Redis for Platform Systems ✅
5. PostgreSQL for Platform Systems ✅
6. Kafka for Platform Systems ✅
7. vLLM ✅
8. LiteLLM ✅
9. GPU Infrastructure & Scheduling ✅
10. Platform Security ✅
11. CI/CD, Helm, Argo CD & GitOps ✅
12. Terraform & Infrastructure as Code ← 현재/다음
13. Multi-tenancy, Quotas & Cost Control
14. Internal Developer Platform / Self-Service
15. End-to-End AI Platform Architecture
```

> 다음 학습은 **Chapter 12. Terraform & Infrastructure as Code**부터 이어진다.
