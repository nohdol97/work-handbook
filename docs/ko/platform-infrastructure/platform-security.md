---
id: platform-infrastructure-platform-security
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - PIS3-10-01
  - PIS3-10-02
  - PIS3-10-03
  - PIS3-10-04
  - PIS3-10-05
  - PIS3-10-06
  - PIS3-10-07
  - PIS3-10-08
---

# Chapter 10. Platform Security

제공된 Basic Chapter 10의 학습 기록이다. 실제 보안 정책·인증서·Secret을 설정하거나 침투·복구 시험을 수행한 운영 경험을 뜻하지 않는다. [Kubernetes 핵심](kubernetes-core.md)과 [LiteLLM](litellm.md)의 배치·서비스 경계와 연결해 읽는다.

**본문 안내:** 원문은 문장·번호·도식·예제를 그대로 보존했다. 10.2의 ClusterRole 범위, 10.3·10.8의 Secret 접근, 10.4의 NetworkPolicy 적용 조건, 10.5의 인증과 인가, 10.6의 securityContext 위치는 뒤의 **원문 절별 보완과 정정**을 함께 읽는다. `password123`은 하드코딩을 설명하는 원문의 의도적 나쁜 예이며 실제 credential이 아니다. 코드·명령은 실행하지 않았다.

<!-- SOURCE CORE START -->

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

<!-- SOURCE CORE END -->

## 원문 절별 보완과 정정

아래는 2026-10-03에 공식 문서와 대조한 보완이며, 원문의 코드·정책을 적용하거나 보안 시험을 수행한 결과가 아니다.

### 10.1·10.2: Kubernetes 권한의 적용 범위

ClusterRole은 클러스터 범위의 **객체**이지만 항상 모든 namespace에 권한을 주는 것은 아니다. RoleBinding으로 연결하면 그 namespace의 권한을 부여하고, ClusterRoleBinding으로 연결하면 클러스터 범위에서 부여한다. Kubernetes RBAC은 Kubernetes API 권한을 제어한다. ServiceAccount가 있다는 사실만으로 PostgreSQL·LiteLLM·vLLM의 애플리케이션 인증·인가가 구성되지는 않는다. [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

### 10.3·10.8: Secret 저장·접근·회전의 조건

Secret의 base64 표현은 암호화가 아니며, 기본적으로 etcd의 Secret은 별도 설정 없이 암호화되어 저장되지 않는다. 저장 암호화와 최소 권한을 함께 설정해야 한다. Secret API 읽기를 막아도 같은 namespace에서 그 Secret을 사용하는 Pod를 만들 수 있다면 값을 노출할 수 있다. 따라서 ServiceAccount별 API 권한만으로 Secret 격리가 완성되지 않는다. [Secret 보안 권장 사항](https://kubernetes.io/docs/concepts/security/secrets-good-practices/)

환경변수로 주입한 Secret은 실행 중인 컨테이너에 자동 갱신되지 않는다. 일반 Secret volume 갱신은 지연될 수 있고 `subPath` 마운트는 자동 갱신되지 않는다. 애플리케이션의 재읽기·재시작과 구 자격 증명 폐기를 포함해 회전을 검증해야 한다. 외부 저장소에서 Kubernetes Secret으로 동기화한 경우에도 이 조건을 확인한다. 원문의 `password123`은 의도적으로 잘못된 하드코딩 예이다. [Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)

### 10.4: NetworkPolicy는 적용 조건을 확인한다

NetworkPolicy를 집행하는 네트워크 플러그인이 필요하다. 정책이 선택하지 않은 방향은 기본적으로 격리되지 않는다. 허용 규칙은 순서대로 차단하는 방화벽 규칙이 아니라 합집합으로 적용된다. 통신하려면 격리된 출발지의 egress와 목적지의 ingress 모두 허용해야 하며, 허용된 연결의 응답 트래픽은 암묵적으로 허용된다. Default deny를 도입할 때 DNS 등 필요한 의존 경로도 검토한다. 이 정책만으로 TLS 암호화나 애플리케이션 인가가 생기지는 않는다. [Kubernetes NetworkPolicy](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

### 10.5: mTLS 인증과 서비스 인가를 구분한다

mTLS는 인증서와 신뢰 설정에 따라 통신 상대의 신원을 확인한다. 그 신원이 특정 서비스의 작업을 수행해도 되는지는 별도 인가 정책으로 결정한다. 원문의 “너 진짜 허용된 LiteLLM 맞아?”는 인증서만 설치하면 모든 접근 권한까지 해결된다는 뜻으로 읽지 않는다. 인증서 갱신과 실제 적용도 확인해야 한다. [Istio 인증·인가](https://istio.io/latest/docs/concepts/security/)

### 10.6: securityContext의 위치와 파일시스템 범위

원문의 두 필드 예는 완전한 Pod manifest가 아니다. `readOnlyRootFilesystem`은 `.spec.containers[*].securityContext`에 설정하는 컨테이너 필드이며 Pod 수준 `.spec.securityContext`에는 넣지 않는다. 루트 파일시스템을 읽기 전용으로 만들어도 별도 마운트의 쓰기 권한까지 제거하지는 않는다. `runAsNonRoot`는 임의의 비-root UID를 자동으로 선택해 주는 설정이 아니므로 이미지와 실행 UID도 확인한다. [Kubernetes security context](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)

### 10.7: 서명과 안전성은 같은 판정이 아니다

이미지 서명 검증은 신뢰하는 키 또는 서명자 신원·issuer와 실제 배포할 digest를 대조해야 한다. 서명이 있다는 사실이나 digest 고정만으로 취약점이 없다고 결론 내릴 수 없다. SBOM은 구성 목록이고 스캔은 탐지 범위 안의 결과이므로, 이 구분은 원문의 공급망 단계들을 함께 읽기 위한 판단 기준이다. [Sigstore 서명 검증](https://docs.sigstore.dev/cosign/verifying/verify/)

### 10.8: namespace 분리의 한계

Namespace는 논리적 경계이며 독립적인 보안 샌드박스를 보장하지 않는다. 상호 신뢰 수준에 따라 RBAC·네트워크·Pod 보안과 노드 또는 클러스터 분리를 함께 검토한다. Quota는 자원 사용량 제한이지 성능이나 GPU 장애 격리의 보장이 아니다. [Kubernetes 멀티테넌시](https://kubernetes.io/docs/concepts/security/multi-tenancy/), [GPU 인프라](gpu-infrastructure.md)

## LLM 실무 활용

### Secret을 노출하지 않고 서비스 보안 경계 검토하기

**상황:** 가상의 LiteLLM 서비스가 모델 서버와 DB에 접근한다. 10.2~10.6·10.8과 보완 내용을 사용해 배포 전 권한·통신 경계를 검토한다.

**LLM에 줄 맥락:** 비식별 namespace·ServiceAccount·RoleBinding 관계, Secret 참조 이름과 주입 방식, NetworkPolicy·CNI 버전, mTLS·인가 설정의 요약. 비밀값·토큰·실제 내부 주소는 제외한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 LiteLLM 서비스의 비식별 구성 요약: [구성]
    ServiceAccount·RoleBinding·Pod 생성 권한: [관계]
    Secret 참조와 주입 방식·회전 방식: [비밀값 없는 설명]
    CNI·NetworkPolicy·mTLS·서비스 인가 설정: [설정 요약]
    [요청]
    10.2~10.6과 10.8의 보완 조건으로 보안 경계를 검토하라.
    관측 사실, 가정, 위험 가설, 누락 근거를 구분하라.
    Secret API 읽기와 Pod를 통한 간접 접근을 따로 검토하라.
    mTLS 인증을 서비스 인가로, namespace를 완전 격리로 간주하지 말라.
    [출력]
    경계, 현재 근거, 실패 가능성, 필요한 추가 확인 표를 작성하라.
    최소 권한 후보와 정상 통신이 막힐 수 있는 의존성을 설명하라.
    [검증]
    배포 버전의 공식 문서와 실제 정책 범위를 사람이 대조하게 하라.
    비밀값을 요구·출력하거나 정책을 적용하지 말라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Sanitized configuration summary for a hypothetical LiteLLM service: [configuration]
    ServiceAccount, RoleBinding, and Pod creation permissions: [relationships]
    Secret references, injection, and rotation: [description without secret values]
    CNI, NetworkPolicy, mTLS, and service authorization: [settings summary]
    [Task]
    Review security boundaries using the supplements to 10.2–10.6 and 10.8.
    Separate observations, assumptions, risk hypotheses, and missing evidence.
    Review Secret API reads separately from indirect access through Pods.
    Do not equate mTLS authentication with service authorization or namespaces with full isolation.
    [Output]
    Give a table of boundaries, current evidence, possible failures, and required checks.
    Explain least-privilege candidates and dependencies whose legitimate traffic could be blocked.
    [Checks]
    Have a person compare version-specific official docs with actual policy scope.
    Do not request or output secret values or apply policies.
    ```

**기대 출력:** API 권한·Secret 간접 접근·통신·서비스 인가를 구분한 검토표와 미확인 조건. DNS 등 정상 의존 경로와 Secret 갱신 전파도 확인 항목으로 포함한다.

**LLM이 틀릴 수 있는 부분:** ClusterRole을 무조건 전역 권한으로 보거나, Secret 읽기 금지만으로 마운트를 막았다고 판단하거나, 정책 파일 존재를 집행 성공으로 오인할 수 있다.

**검증 방법:** 사람이 비식별 설정과 배포 버전의 공식 문서를 대조한다. 실제 허용·거부 및 회전 시험은 별도 승인된 시험 환경에서 수행한다. 이 예시는 작성한 검토 시나리오이며 실제 모델 응답·보안 시험의 성공 기록이 아니다.
