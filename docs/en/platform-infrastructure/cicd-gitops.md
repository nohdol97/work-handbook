---
id: platform-infrastructure-cicd-gitops
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
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

The supplied study notes retain their numbering, order, examples, and GPU supplement. Example versions, placements, and commands are not execution results. See the separate supplement for Helm release and Argo CD rollback conditions in 11.3/11.6, the meaning of Healthy, and traffic migration and GPU headroom conditions in 11.7–11.8.

<!-- SOURCE CORE START -->

## 11.1 CI/CD Fundamentals

CI/CD:

> Automate testing, building, and deploying code changes to actual environments

Key points:

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
CI succeeds
↓
Container Image
↓
Registry
↓
CD
↓
Kubernetes
```

### Overall pipeline

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

Traditional CD:

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
Change deployment settings in Git

Argo CD
↓
Check Git
↓
Kubernetes
```

Key points:

```text
CI
= Build and validate the application

GitOps
= Manage which version is deployed to the cluster
```

---

## 11.2 Container Build Pipeline

> Build source code into a container image and store it in a registry

Key points:

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

Example:

```text
my-api:1.0
my-api:1.1
my-api:20261003
```

Use explicit versions in production instead of relying only on `latest`.

### Connect Git commits to images

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

Use the same image in:

```text
dev
staging
prod
```

The same image is used in all three environments.

Separate environment differences through:

```text
ConfigMap
Secret
Helm Values
```

These hold the differences.

### Core flow

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

> A package manager that templates Kubernetes YAML for reuse across environments and services

Key points:

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

Relationship:

```text
Template
= Deployment structure

Values
= Actual configuration values
```

### Values by environment

```text
values-dev.yaml
values-staging.yaml
values-prod.yaml
```

### Release

An instance of a chart deployed to an actual cluster.

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
↓ Problem
Rollback
↓
v1
```

### How to understand Helm

```text
Kubernetes components
Deployment / Service / Ingress / ConfigMap ...
↓
Share common structure through Helm templates

Differences by environment
replica / image tag / CPU / domain ...
↓
Values
```

In other words:

> Reuse deployment structure through templates and inject environment differences through values

### Where Helm release information is stored

In Helm 3, release information is stored by default in Secrets in the Kubernetes namespace where the release is installed.

Example:

```text
Namespace: my-api-prod

├─ Deployment
├─ Service
├─ ConfigMap
└─ Helm Release Secret
```

Revision examples:

```text
sh.helm.release.v1.my-api.v1
sh.helm.release.v1.my-api.v2
sh.helm.release.v1.my-api.v3
```

Inspect:

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
= Blueprint / template package

Release
= Record and state of a chart installed in an actual cluster
```

### Image versions can also be managed in Helm values

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
→ Version of the deployment structure

Image Tag
→ Application code version
```

---

## 11.4 Environment Management

> Deploy the same application to dev / staging / prod while safely managing different settings for each environment

Key points:

```text
Same image
+
Same Helm template
+
Values by environment
```

### Keep the image the same

```text
Dev     → my-api:1.5.0
Staging → my-api:1.5.0
Prod    → my-api:1.5.0
```

### Configuration by environment

Example:

```text
Replica count
CPU / Memory
Domain
DB address
Log level
Autoscaling
```

### Separate namespaces

```text
my-api-dev
my-api-staging
my-api-prod
```

For each environment:

```text
Secret
ConfigMap
ResourceQuota
NetworkPolicy
RBAC
```

These can be separated.

### Do not store plaintext secrets in values

A good structure:

```text
Helm Values
→ Reference only the Secret name

Actual secret
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

Promote the same artifact instead of building a new image for each environment.

### Example Git layout

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

Key points:

> Build once, deploy many

---

## 11.5 GitOps

GitOps:

> Store Kubernetes desired state in Git and continuously reconcile the actual cluster with Git

### Source of Truth

Git:

```text
image.tag = 1.5.0
replicas = 3
```

Production should match this state too.

### Traditional deployment

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

### GitOps deployment

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

Then, in the deployment Git repository:

```yaml
image:
  tag: "1.5.0"
```

Change this setting.

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
→ Check Git
→ Apply to Kubernetes
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

This is drift.

### Connection to Helm

```text
Helm
= Generate manifests

Git
= Store desired state

Argo CD
= Synchronize Git and the cluster
```

### When to use kubectl

In a GitOps environment, kubectl is mainly used for:

```text
Observation
Troubleshooting
Emergency incident response
```

These are its main uses.

For normal configuration and deployment changes:

```text
Git + Argo CD
```

This is the default approach.

Common diagnostic commands:

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

Break-glass examples:

```bash
kubectl cordon node-a
kubectl drain node-a
```

Reconcile the state with Git after emergency actions.

### Distinguish Argo CD / Grafana / kubectl responsibilities

```text
Argo CD
= Deployment state / resource structure / sync / health

Grafana
= Metrics / Logs / Alert

kubectl
= Detailed Kubernetes diagnosis / immediate inspection
```

### Argo CD can also show Pod state

```text
Application
↓
Deployment
↓
ReplicaSet
↓
Pod
```

Health can be inspected in a resource tree.

For detailed causes, however:

```text
kubectl describe
kubectl logs
events
```

These may be more direct.

---

## 11.6 Argo CD

Argo CD:

> A GitOps controller that compares and synchronizes Kubernetes desired state in Git with actual cluster state

Key points:

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

A unit of deployment management.

Broadly:

```text
Which Git repository?
Which path?
Which revision?
Which cluster?
Which namespace?
```

These are defined.

### Sync

```text
Git Desired State
↓
Helm / Manifest Rendering
↓
Apply to Kubernetes
↓
Actual state matches
```

### Manual Sync

After detecting Git changes, show OutOfSync and let an operator sync.

### Auto Sync

```text
Git change
↓
Argo CD detects the change
↓
Automatic sync
↓
Kubernetes Update
```

### Self Heal

Restore direct cluster changes to the state in Git.

### Prune

Remove resources from the cluster when they disappear from Git.

### Health

The state of the actual resources.

### Difference between sync and health

```text
Synced
= Configuration matches Git

Healthy
= The application is working normally
```

Therefore:

```text
Synced
but
Degraded
```

This is possible.

### Rollback

You can return to a previously synced revision, but under GitOps principles it is important to align Git state with the rollback state too.

### Helm and Argo CD responsibilities

```text
Helm
= Generate Kubernetes manifests

Argo CD
= Synchronize desired state with the cluster
```

### Must Argo CD be given the Helm path?

When using a Helm chart in Git, provide the Argo CD Application with:

```text
1. Git Repository
2. Branch / Commit
3. Helm chart path
4. Values
5. Target cluster / namespace
```

Provide these details.

Example:

```yaml
spec:
  source:
    repoURL: ...
    targetRevision: main
    path: apps/my-api
```

Example repository:

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

### Argo CD rollback and Helm releases

When Argo CD uses Helm, Helm mainly renders manifests.

Therefore:

```text
Argo CD rollback
→ Previous Application revision
→ Render the chart and values from that revision
→ Apply to Kubernetes
```

This is the accurate way to understand it.

It is not simply reactivating a Helm release Secret.

### Image versions can also be specified in Helm values

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

Returning to a previous commit can render and apply the previous image tag again.

---

## 11.7 Deployment Strategies

Key points:

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
Blue = Current production
Green = New version
```

Switch all traffic after preparing and validating Green.

Return quickly to Blue if a problem occurs.

### Canary

```text
95% → v1
5%  → v2
```

Gradually:

```text
80 / 20
50 / 50
0 / 100
```

### Canary in AI serving

A new model may differ in:

```text
Response quality
TTFT
TPOT
VRAM
OOM
Tool Calling
Output format
```

Validate these differences with a small share of traffic first.

---

## 11.8 AI Serving Deployment

AI serving deployments must manage:

```text
Model Version
vLLM Version
Serving Configuration
GPU Capacity
```

Manage these together.

### Model Version

Example:

```text
vLLM Image
→ vllm:0.x

Model
→ glm-5.3-fp4-v1
```

Serving settings:

```text
model
max_model_len
tensor_parallel_size
kv_cache_dtype
gpu_memory_utilization
```

These should also be recorded in Git.

### Replacing a model immediately is risky

Things that may change:

```text
Weight size
VRAM usage
KV cache requirements
TTFT
TPOT
Throughput
Response quality
Tool Calling
```

### vLLM Rollout

```text
New vLLM / model Pod
↓
Model Load
↓
Allocate GPU memory
↓
Startup Probe
↓
Readiness
```

Send traffic after it becomes Ready.

### LiteLLM Routing Migration

```text
100% → v1
0%   → v2

↓ Canary

95% → v1
5%  → v2

↓ Expand

80 / 20
50 / 50
0 / 100
```

### Separate responsibilities

```text
Argo CD
→ Deploy vLLM / model resources

LiteLLM
→ Switch user traffic
```

### Validation metrics

```text
Error Rate
TTFT
TPOT
Queue Time
GPU Utilization
VRAM / KV Cache
OOM
Response quality
```

### Safe Rollback

A problem occurs:

```text
20% → v1
80% → v2

↓ Problem

100% → v1
0%   → v2
```

Then remove or modify v2 resources through Git / Argo CD.

---

## Supplement on AI model replacement and GPU / VRAM capacity

### Validation needs capacity for both the old and new models

Example:

```text
Existing GLM-v1
→ 4 GPUs

New GLM-v2
→ 4 GPUs

Validation period
→ At least about 8 GPUs of capacity are needed
```

Blue-green / canary needs temporary additional capacity.

### Example with 3 existing replicas

```text
Replica A → GPU ×4
Replica B → GPU ×4
Replica C → GPU ×4

12 GPUs in total
```

New canary:

```text
Existing 12 GPUs
+
New Replica D → GPU ×4
=
16 GPUs in total
```

### Uses of spare capacity

```text
Node/GPU failure response
Rolling Update
Canary
Model Upgrade
Traffic Spike
```

### Spare GPUs differ from unused VRAM on serving GPUs

Example:

```text
B300 Node

GPU 0~3 → GLM Replica A
GPU 4~7 → Spare
```

GPU 0~3 used by Replica A:

```text
GPU 0~3 VRAM

├─ Model Weight
├─ KV Cache
├─ Activation
├─ Runtime Buffer
└─ Free capacity
```

The remaining VRAM here is used for **Replica A's KV cache / runtime capacity**.

If GPU 4~7 are free instead:

```text
GPU 4~7
= Spare GPUs that can host a new replica
```

### A new model needs both weights and KV cache

```text
Spare GPU
↓
New model weights
+
New model KV cache
+
Activation
+
Runtime
```

All of these must fit.

Therefore:

```text
New model weights use almost 100% of spare GPU VRAM
→ Not enough KV cache space
→ Not enough serving capacity
```

This is possible.

Key points:

> A model fitting on GPUs is different from having enough capacity to serve it in practice.

### VRAM is fundamentally local memory on each GPU

A new model cannot freely borrow unused VRAM from GPUs used by an existing replica as if it were a shared pool.

```text
GPU 0~3
→ Old GLM Weight + KV Cache

GPU 4~7
→ New GLM Weight + KV Cache
```

### Assessing actual spare serving capacity

```text
Spare GPU count
↓
Do the new model weights fit?
↓
Is there enough space left for the KV cache?
↓
Can it support the target context / concurrency?
↓
Can it meet the TTFT / TPOT SLA?
```

For 1M-context LLMs in particular, KV cache capacity matters greatly alongside weights.

---

<!-- SOURCE CORE END -->

## Supplement — version tracking and rollback conditions

Official documentation checked on 2026-10-03. The source's Helm 3 statements were checked against Helm 3 documentation. Argo CD and LiteLLM links refer to stable documentation at review time. No installation, deployment, rollback, or load test was run.

### 11.2 / 11.4 version names and artifact identity

Even an explicit tag can be moved to different content. Record the image digest and check the deployed target to promote the same artifact and reproduce an earlier build. Using a Git commit as a tag does not itself make the registry tag immutable. [Kubernetes Images](https://kubernetes.io/docs/concepts/containers/images/)

### 11.3 / 11.6 the boundary between Helm releases and Argo CD

Secrets are the default Helm 3 storage backend; `HELM_DRIVER` can select another backend. Release records include chart and values data. Keeping secrets out of values therefore matters for release access as well as Git access. [Helm 3 storage backends](https://helm.sh/docs/v3/topics/advanced/)

In `helm rollback my-api 2`, `2` is a release revision, not an image tag. Check the actual context, namespace, and release history first. This command changes the cluster; it does not restore a database or external state to the past. [Helm 3 rollback](https://helm.sh/docs/v3/helm/helm_rollback/)

Normal Argo CD Helm integration uses `helm template` to generate manifests, while Argo CD manages the lifecycle. The Helm release Secret/history in 11.3 is therefore different from Application deployment history in 11.6. The source's `path` example selects a chart; it does not automatically select `env/prod/values.yaml`. Check the required `helm.valueFiles` and actual values precedence. [Argo CD Helm](https://argo-cd.readthedocs.io/en/stable/user-guide/helm/)

### 11.5 / 11.6 sync, Healthy, and rollback

Enabling automated sync does not automatically enable both live-drift repair and deletion. Check `selfHeal` and `prune` separately. **Direct rollback cannot be performed on an Application with automated sync enabled.** Commit the desired earlier state to Git and sync it, or adjust automated sync and Git desired state together under an approved recovery procedure. [Argo CD automated sync](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/)

`Healthy` is the result of resource-specific health checks. It does not guarantee successful user requests, model response quality, or TTFT/TPOT targets. Separate request validation and metrics are needed. [Argo CD resource health](https://argo-cd.readthedocs.io/en/stable/operator-manual/health/)

In the command list in 11.5, `exec` can execute arbitrary commands inside a container, and `port-forward` opens an access path. `cordon` and `drain` change placement and availability. Do not treat the entire diagnostic list as read-only. No such commands were run for this page.

### 11.7 / 11.8 and GPU supplement migration conditions

Ratios such as 95/5 are example traffic targets. The LiteLLM router selects backends using the configured strategy and weights. Measure actual short-window distribution, retries, and fallbacks separately. Before returning 100% of traffic to the old version, check its replicas' health, capacity, and compatibility, and consider requests already in progress. [LiteLLM routing](https://docs.litellm.ai/docs/routing)

The 4+4=8 and 12+4=16 GPU calculations assume adding a new replica while keeping existing replicas. If a canary consumes all spare GPUs, those same GPUs cannot also be counted as failure reserve. Check suitable node placement and failure domains as well as weights, KV cache, and runtime memory per GPU. [GPU capacity planning](gpu-infrastructure.md)

Extra Pod count and allowed disruption during rolling updates depend on settings such as `maxSurge` and `maxUnavailable`. The source's temporary extra capacity assumes validation while retaining existing capacity. It does not mean every strategy always needs the same number of extra GPUs. [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

`vllm:0.x` and `glm-5.3-fp4-v1` are illustrative names. Pin and check actual image/model revisions and serving settings. VRAM on another replica's GPUs does not automatically form a shared pool; separate sharing/offload mechanisms are outside this example's assumptions. [vLLM study](vllm.md)

Reading guide: separate artifacts from environment settings in 11.1–11.4, then identify desired state and controller responsibilities in 11.5–11.6. In 11.7–11.8 and the GPU supplement, calculate new-version validation, traffic rollback, and failure reserve separately.

## LLM in Practice

### Situation

Errors increased in a hypothetical v2 canary. Use [GPU capacity planning](gpu-infrastructure.md) and [LiteLLM](litellm.md) to review conditions for returning to the old model. This is not an actual incident or model execution result.

### Context to Give the LLM

Provide sanitized Git/image/model revisions, sync policy, placement and GPU headroom, routing settings, and time-aligned request/error/latency/KV metrics. Leave missing values unknown.

### Example Prompt

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 모델 v2 canary에서 오류가 늘었지만 원인은 미확인이다.
    관측: Argo CD Synced/Healthy, GPU 16장 중 기존 replica 12장과 canary 4장 사용.
    자료: [Git revision·image digest·model revision·routing 설정·TTFT/TPOT·오류·KV 지표].
    Automated sync/selfHeal/prune와 실제 Node 배치는 미확인이다.
    [요청]
    관측·가정·누락 증거를 분리하고 v1 복귀 계획의 실행 가능성을 검토하라.
    Helm release rollback과 Argo CD rollback, Git revert, routing 전환을 구분하라.
    [출력]
    가설 / 필요한 증거 / 읽기 전용 다음 확인 / 복귀 조건 표를 작성하라.
    Canary와 장애 여유를 이중 계산하지 말고 v1의 100% 부하 수용 조건을 적어라.
    [검증]
    Healthy만으로 품질·SLA 충족을 단정하지 말고 실제 요청 지표와 대조하라.
    자동 sync 조건과 image/model 불변성을 공식 문서·설정으로 확인하라.
    Rollback·drain·routing 변경은 실행하지 말고 격리 시험 계획만 제안하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Errors increased during a hypothetical v2 model canary; the cause is unknown.
    Observations: Argo CD is Synced/Healthy; existing replicas use 12 GPUs and the canary uses 4 of 16 GPUs.
    Material: [Git revision, image digest, model revision, routing settings, TTFT/TPOT, errors, and KV metrics].
    Automated sync/selfHeal/prune settings and actual node placement are unknown.
    [Task]
    Separate observations, assumptions, and missing evidence; review whether a v1 recovery plan is feasible.
    Distinguish Helm release rollback, Argo CD rollback, Git revert, and routing changes.
    [Output]
    Create a table: hypothesis / required evidence / next read-only check / recovery conditions.
    Do not count canary capacity twice as failure reserve; state when v1 can accept 100% of traffic.
    [Checks]
    Do not infer quality or SLA compliance from Healthy alone; check actual request metrics.
    Verify automated sync conditions and image/model immutability against official docs and configuration.
    Do not run rollback, drain, or routing changes; propose an isolated test plan only.
    ```

### Expected Output

A table separating causal hypotheses, disproof conditions, further read-only checks, v1 recovery prerequisites, and capacity shortages.

### What the LLM Can Get Wrong

It may treat Healthy as a guarantee of response quality or suggest direct rollback while automated sync is enabled. It may double-count canary GPUs as failure reserve or assume a moved tag still identifies the original image.

### How to Validate

Compare Application settings and history, Git diffs, image digests, actual model revisions, node placement, router metrics, and request metrics. After human review, test recovery and load in an isolated environment. LLM output is a hypothesis; no deployment, rollback, or model execution was performed for this page.

## Related topics

- [Platform infrastructure study map](index.md)
- [Kubernetes operations](kubernetes-operations.md)
