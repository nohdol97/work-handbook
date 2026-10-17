---
id: platform-infrastructure-cicd-gitops
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - PIS3-11-01
  - PIS3-11-02
  - PIS3-11-03
  - PIS3-11-04
  - PIS3-11-05
  - PIS3-11-06
  - PIS3-11-07
  - PIS3-11-08
  - PIS3-11-09
---

# Chapter 11. CI/CD, Helm, Argo CD & GitOps

예시 구성과 명령은 학습용이며 실제 배포·장애 실험 결과가 아니다.

<!-- SOURCE CORE START -->

## 11.1 CI/CD Fundamentals

CI/CD는 변경을 검사하고 전달하는 조립 라인, GitOps는 원하는 배포 상태를 적어 둔 작업 지시서와 비슷하다. 검사 통과, 배포 상태, 실제 서비스 준비를 각각 확인한다.

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

**버전 이름과 artifact 동일성**

명확한 tag도 다시 가리키는 대상이 바뀔 수 있다. 같은 artifact를 승격하고 이전 실행물을 재현하려면 image digest를 기록하고 배포 대상을 확인한다. Git commit을 tag로 썼다는 사실만으로 registry에서 불변성이 보장되지는 않는다. [Kubernetes Images](https://kubernetes.io/docs/concepts/containers/images/)

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

**Helm release와 Argo CD의 경계**

Helm 3의 Secret 저장은 기본 backend이며 `HELM_DRIVER`로 다른 backend를 선택할 수 있다. Release 정보에는 chart·values가 들어가므로 values에 비밀값을 넣지 않는 원칙은 Git뿐 아니라 release 접근 권한에도 연결된다. [Helm 3 storage backends](https://helm.sh/docs/v3/topics/advanced/)

`helm rollback my-api 2`의 `2`는 image tag가 아니라 release revision이다. 실제 context·namespace·release history를 먼저 확인한다. 이 명령은 cluster를 변경하며, DB나 외부 상태를 과거로 복구하는 명령이 아니다. [Helm 3 rollback](https://helm.sh/docs/v3/helm/helm_rollback/)

Argo CD의 일반적인 Helm 통합은 `helm template`로 manifest를 만들고 Argo CD가 lifecycle을 관리한다. 그러므로 11.3의 Helm release Secret/history와 11.6의 Application 배포 history는 같은 기록이 아니다. 원문의 `path` 예시는 chart 선택을 보여줄 뿐 `env/prod/values.yaml`을 자동 선택하지 않는다. 필요한 `helm.valueFiles`와 실제 values 우선순위를 확인한다. [Argo CD Helm](https://argo-cd.readthedocs.io/en/stable/user-guide/helm/)

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

**Sync·Healthy·rollback**

자동 sync를 켜도 live drift 복구와 삭제가 모두 자동 활성화되는 것은 아니다. `selfHeal`과 `prune`을 따로 확인한다. **Automated sync가 활성화된 Application에는 직접 rollback을 수행할 수 없다.** Git에 원하는 이전 상태를 새 commit으로 반영해 sync하거나, 승인된 복구 절차에 따라 automated sync 설정과 Git desired state를 함께 조정한다. [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)

`Healthy`는 resource별 health 평가 결과다. 사용자 요청 성공, 모델의 응답 품질, TTFT/TPOT 목표 충족까지 보장하지 않는다. 별도 요청 검증과 지표가 필요하다. [Argo CD resource health](https://argo-cd.readthedocs.io/en/stable/operator-manual/health/)

11.5의 명령 목록 중 `exec`는 container 안에서 임의 명령을 실행할 수 있고 `port-forward`는 접근 경로를 연다. `cordon`·`drain`은 실제 배치·가용성을 변경한다. 진단 명령 전체를 읽기 전용으로 취급하지 않는다. 이 문서는 해당 명령을 실행하지 않았다.

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

**AI Serving 전환과 GPU 용량 조건**

95/5 등은 목표 트래픽 비율의 예시다. LiteLLM router는 구성된 전략과 weight로 backend를 선택하며, 짧은 구간의 실제 분포·retry·fallback은 별도로 관측해야 한다. 구 버전으로 100%를 돌리기 전에 구 replica의 health·capacity·호환성을 확인하고 진행 중인 요청도 고려한다. [LiteLLM routing](https://docs.litellm.ai/docs/routing)

4+4=8, 12+4=16 GPU 계산은 기존 replica를 유지하며 새 replica를 추가하는 예시다. 이 여유를 canary가 모두 쓰면 같은 GPU를 장애 복구 여유로 다시 계산할 수 없다. GPU별 Weight·KV·runtime뿐 아니라 적합한 Node 배치와 장애 영역을 확인한다. [GPU 용량 계획](gpu-infrastructure.md)

Rolling update의 실제 추가 Pod 수와 허용 중단은 `maxSurge`·`maxUnavailable` 등에 달려 있다. 원문의 “일시적 추가 capacity”는 기존 용량을 유지한 채 검증하는 조건이며, 모든 전략이 항상 같은 추가 GPU 수를 요구한다는 뜻은 아니다. [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

`vllm:0.x`, `glm-5.3-fp4-v1`은 설명용 이름이다. 실제 image/model revision·serving 설정을 고정해 확인한다. 다른 replica GPU의 VRAM이 자동 공용 pool이 되지는 않으며, 별도 공유/offload 기술은 이 예시의 가정 밖이다. [vLLM 학습](vllm.md)

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

<!-- SOURCE CORE END -->

## 관련 문서

- [플랫폼 인프라 학습 지도](index.md)
- [Kubernetes 운영](kubernetes-operations.md)

## 핵심 정리

배포 버전과 실제 실행 상태를 연결해 확인하고, 롤백 가능성은 모델·데이터·용량까지 포함해 판단한다.

## LLM in Practice

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    모델 canary에서 오류가 늘었어. 배포 diff, Argo CD 상태, traffic routing과 GPU 여유를 보고 이전 버전으로 돌아갈 수 있는지 검토해 줘. Git revert, Helm rollback, routing 전환의 역할을 구분하고 실제 rollback은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Errors increased during a model canary. Review the deployment diff, Argo CD state, traffic routing, and spare GPU capacity to assess a return to the previous version. Separate Git revert, Helm rollback, and routing changes; do not perform a rollback.
    ```

**핵심 사항:** canary 실패 가설, v1 트래픽 복귀 단계별 부하·호환성·GPU 여유와 진행/중단 판정표. Synced/Healthy를 응답 품질 보장으로 보거나 변경 가능한 tag로 이전 실행물이 재현된다고 판단할 수 있다. Git·digest·model revision과 Argo CD 정책, 실제 라우팅/요청 지표를 대조한다. canary GPU를 장애 예비로 세거나 구 버전 100% 부하 근거가 없는 복귀안은 보류한다. 관련: [GPU 용량 계획](gpu-infrastructure.md) · [LiteLLM](litellm.md)
