---
items:
- id: PIS3-00-01
  knowledge: Chapter10~11 Basic 핵심 개념과 중간 실무 질문, 이전1~9장 및 다음12장 Terraform/IaC 학습 경계
  kind: scope
  source_lines: 1–10
  destination: platform-infrastructure/index.md
- id: PIS3-00-02
  knowledge: Identity→RBAC→Secrets→NetworkPolicy→TLS/mTLS→컨테이너·공급망·tenant 보안, Git→CI test/build/scan/registry→배포
    Git Helm/environment values→Argo CD→Kubernetes와 모델/vLLM/readiness/LiteLLM canary/metric·quality/확대·rollback
    연결
  kind: architecture
  source_lines: 2538–2603
  destination: platform-infrastructure/index.md
- id: PIS3-00-03
  knowledge: 1~11장 Basic 개념 학습 완료, 12장 Terraform/IaC 다음, 13~15장 tenant/quota/cost·IDP·최종AI구조 미학습 상태
  kind: study-status
  source_lines: 2604–2624
  destination: platform-infrastructure/index.md
- id: PIS3-10-01
  knowledge: Authentication은 신원 확인, Authorization은 허용행위 결정; login/APIkey/SA/SSO 예; UserA model조회·deployment수정불가
    대 admin수정·secret관리; IAM user/team/service/role/permission; Backend→PostgreSQL·LiteLLM→vLLM·App→Kafka
    서비스identity; 사람개발자K8s조회 대 backendDB연결; 최소권한 bad 모든서비스admin 대 backend특정DB/LiteLLM특정secret/monitoring조회
  kind: concept,comparison,examples,security-principle
  source_lines: 13-199
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-02
  knowledge: Role namespace권한·pods get/list와 deployments get/update 예, RoleBinding 사용자/SA연결, ClusterRole
    모든namespacepod/node/clusterresource 조회 예; Pod→SA→binding→role, backupPVC조회; 모든podclusteradmin 위험과
    monitoring/controller/backup별 최소권한. ClusterRole effective scope binding별 조건은 보완 필요
  kind: rbac,scope,identity,examples,conditions
  source_lines: 200-338
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-03
  knowledge: Kubernetes Secret env/file 소비, DB_PASSWORD/API_KEY/JWT_SECRET 이름, gitplaintext노출 경고; External
    store→controller→K8sSecret→pod; AWSSecretsManager/Vault/CloudManager, access/audit/rotation/dynamiccredential;
    v1→v2→app교체→v1폐기; password123 hardcode 나쁜예; code/image와secret분리; LiteLLM/backend/Kafka개별credential
    최소범위
  kind: secret-lifecycle,architecture,example,security-boundary
  source_lines: 339-523
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-04
  knowledge: frontend→backend→PostgreSQL/Redis 필요한통신, NetworkPolicy Pod 접근; ingress/egress 정의, LiteLLM→vLLM허용·인터넷제한;
    firewall/securitygroup과podpolicy 계층; vLLM→Redis불필요차단; defaultdeny 후 app·metrics예외; CNI Calico/Cilium
    enforcement; LiteLLMegress/vLLMingress 양방향규칙과 허용연결응답패킷왕복
  kind: network,flow,conditions,examples
  source_lines: 524-754
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-05
  knowledge: TLS 암호화와 서버certificate확인; prompt/내부데이터/sourcecode/API정보 보호; 일반TLS와APIkey/JWT/SSO 사용자인증; mTLS
    양certificate 서비스identity, NetworkPolicy접속권한 대TLS암호화 대mTLS상호identity; certv1만료→v2발급→교체→v1폐기
  kind: tls,identity,comparison,lifecycle
  source_lines: 755-908
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-06
  knowledge: 침해container가host/다른container피해 확대 제한; nonroot runAsNonRoot true YAML, capabilities최소·필요추가,
    privileged hostdevice/kernel권한 예외; seccomp syscall허용/차단, readonly /app/bin/etc 대 /tmp/data별도volume;
    securityContext runAsNonRoot+readOnlyRootFilesystem YAML. container-level field 위치 보완 필요
  kind: container-hardening,configuration,security-boundary
  source_lines: 909-1038
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-07
  knowledge: 'image/library 공급망: scanner OpenSSL취약점 예, CI code/build/scan/push; SBOMUbuntu/Python/FastAPI/OpenSSL/requests/기타목록;
    build/sign/registry·배포검증; tag가변 대digestcontent고정; registry push/pull/delete/scan권한; 개발자prod이미지직접수정불가·검증CIpush·승인registrypull;
    전체CI/CDtest-scan-SBOM-sign-deploy흐름'
  kind: supply-chain,provenance,comparison,flow
  source_lines: 1039-1166
  destination: platform-infrastructure/platform-security.md
- id: PIS3-10-08
  knowledge: team-a/b/c namespace 논리격리 한계, team별RBAC·networkdefaultdeny·secret개별접근·CPUmemGPU quota/limitrange;
    namespace service/team/env/security/lifecycle기준; service-env(payment/agent)·myservicedev/prod리소스목록·teamenv패턴;
    shopping-prod와database-prod분리 또는managedDB; dev/staging/prodnamespace와strongdev/prodcluster분리; chapteridentity→rbac→secret→network→tls→hardening→supplychain→tenant최종흐름
  kind: multitenancy,examples,design-tradeoffs,resource-isolation
  source_lines: 1167-1355
  destination: platform-infrastructure/platform-security.md
- id: PIS3-11-01
  knowledge: ': CI/CD:; : > 코드 변경을 테스트하고, 빌드하고, 실제 환경에 배포하는 과정을 자동화; : 핵심:; : ```text

    CI

    = Build + Test


    CD

    = Deploy

    ```; CI: ```text

    Developer

    ↓

    Git Push

    ↓

    CI Pipeline

    ├─ Unit Test

    ├─ Lint

    ├─ Security Scan

    └─ Docker Image Build

    ```; CD: ```text

    CI 성공

    ↓

    Container Image

    ↓

    Registry

    ↓

    CD

    ↓

    Kubernetes

    ```; 전체 Pipeline: ```text

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

    ```; CI vs GitOps: 전통적 CD:; CI vs GitOps: ```text

    CI Pipeline

    ↓

    kubectl / Helm

    ↓

    Kubernetes

    ```; CI vs GitOps: GitOps:; CI vs GitOps: ```text

    CI

    ↓

    Git의 Deployment 설정 변경


    Argo CD

    ↓

    Git 확인

    ↓

    Kubernetes

    ```; CI vs GitOps: 핵심:; CI vs GitOps: ```text

    CI

    = Application을 만들고 검증


    GitOps

    = 어떤 버전을 Cluster에 배포할지 관리

    ```'
  kind: 개념·조건·주의
  source_lines: 1360–1457
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-02
  knowledge: 'CI vs GitOps: > 소스 코드를 Container Image로 만들고 Registry에 저장하는 과정; CI vs GitOps: 핵심:; CI vs
    GitOps: ```text

    Build

    Tag

    Push

    Versioning

    ```; Build: ```text

    Source Code

    ↓

    Dockerfile

    ↓

    docker build

    ↓

    Container Image

    ```; Tag: 예:; Tag: ```text

    my-api:1.0

    my-api:1.1

    my-api:20261003

    ```; Tag: Production에서는 `latest`만 쓰는 것보다 명확한 버전을 사용.; Git Commit과 Image 연결: ```text

    Git commit

    a1b2c3d

    ↓

    Build

    ↓

    my-api:a1b2c3d

    ```; Registry Push: ```text

    CI

    ↓

    my-api:1.3

    ↓

    Container Registry

    ```; Build once, deploy many: 같은 Image를:; Build once, deploy many: ```text

    dev

    staging

    prod

    ```; Build once, deploy many: 에 사용.; Build once, deploy many: 환경 차이는:; Build once, deploy many: ```text

    ConfigMap

    Secret

    Helm Values

    ```; Build once, deploy many: 로 분리.; 핵심 흐름: ```text

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

    ```'
  kind: 개념·조건·주의
  source_lines: 1463–1555
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-03
  knowledge: "핵심 흐름: Helm:; 핵심 흐름: > Kubernetes YAML을 템플릿화해서 여러 환경과 서비스에 재사용하기 위한 패키지 관리자; 핵심 흐름: 핵심:;\
    \ 핵심 흐름: ```text\nChart\nTemplate\nValues\nRelease\nUpgrade / Rollback\n```; Chart: ```text\nmy-api-chart/\n\
    ├─ Chart.yaml\n├─ values.yaml\n└─ templates/\n   ├─ deployment.yaml\n   ├─ service.yaml\n   └─ ingress.yaml\n\
    ```; Template: ```yaml\nreplicas: {{ .Values.replicaCount }}\n\nimage:\n  repository: {{ .Values.image.repository\
    \ }}\n  tag: {{ .Values.image.tag }}\n```; Values: ```yaml\nreplicaCount: 3\n\nimage:\n  repository:\
    \ my-api\n  tag: \"1.3\"\n```; Values: 관계:; Values: ```text\nTemplate\n= 배포 구조\n\nValues\n= 실제 설정값\n\
    ```; 환경별 Values: ```text\nvalues-dev.yaml\nvalues-staging.yaml\nvalues-prod.yaml\n```; Release: Chart를\
    \ 실제 Cluster에 배포한 인스턴스.; Release: ```text\nChart\n= my-api\n\nRelease\n= my-api-prod\n```; Upgrade\
    \ / Rollback: ```text\nmy-api:v1\n↓\nmy-api:v2\n↓ 문제\nRollback\n↓\nv1\n```; Helm을 이렇게 이해하면 된다: ```text\n\
    Kubernetes 구성요소\nDeployment / Service / Ingress / ConfigMap ...\n↓\nHelm Template로 공통화\n\n환경별 차이\n\
    replica / image tag / CPU / domain ...\n↓\nValues\n```; Helm을 이렇게 이해하면 된다: 즉:; Helm을 이렇게 이해하면 된다:\
    \ > 배포 구조는 Template으로 재사용하고, 환경별 차이는 Values로 주입; Helm Release 정보는 어디 저장되는가: Helm 3 기준 기본적으로 해당 Release가\
    \ 설치된 Kubernetes Namespace의 Secret에 저장.; Helm Release 정보는 어디 저장되는가: 예:; Helm Release 정보는 어디 저장되는가:\
    \ ```text\nNamespace: my-api-prod\n\n├─ Deployment\n├─ Service\n├─ ConfigMap\n└─ Helm Release Secret\n\
    ```; Helm Release 정보는 어디 저장되는가: Revision 예:; Helm Release 정보는 어디 저장되는가: ```text\nsh.helm.release.v1.my-api.v1\n\
    sh.helm.release.v1.my-api.v2\nsh.helm.release.v1.my-api.v3\n```; Helm Release 정보는 어디 저장되는가: 확인:; Helm\
    \ Release 정보는 어디 저장되는가: ```bash\nhelm history my-api\n```; Helm Release 정보는 어디 저장되는가: Rollback:; Helm\
    \ Release 정보는 어디 저장되는가: ```bash\nhelm rollback my-api 2\n```; Chart vs Release: ```text\nChart\n=\
    \ 설계도 / Template 패키지\n\nRelease\n= Chart를 실제 Cluster에 설치한 기록 + 상태\n```; Image 버전도 Helm Values에 관리\
    \ 가능: ```yaml\nimage:\n  repository: registry.example.com/my-api\n  tag: \"1.3.0\"\n```; Image 버전도\
    \ Helm Values에 관리 가능: Template:; Image 버전도 Helm Values에 관리 가능: ```yaml\ncontainers:\n  - name: my-api\n\
    \    image: \"{{ .Values.image.repository }}:{{ .Values.image.tag }}\"\n```; Chart Version vs Image\
    \ Tag: ```text\nChart Version\n→ 배포 구조의 버전\n\nImage Tag\n→ Application 코드 버전\n```"
  kind: 개념·조건·주의
  source_lines: 1561–1736
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-04
  knowledge: "Chart Version vs Image Tag: > 같은 애플리케이션을 dev / staging / prod에 배포하되 환경별 설정만 안전하게 다르게 관리;\
    \ Chart Version vs Image Tag: 핵심:; Chart Version vs Image Tag: ```text\n같은 Image\n+\n같은 Helm Template\n\
    +\n환경별 Values\n```; Image는 동일하게: ```text\nDev     → my-api:1.5.0\nStaging → my-api:1.5.0\nProd   \
    \ → my-api:1.5.0\n```; 환경별 Configuration: 예:; 환경별 Configuration: ```text\nReplica 수\nCPU / Memory\n\
    Domain\nDB 주소\nLog level\nAutoscaling\n```; Namespace 분리: ```text\nmy-api-dev\nmy-api-staging\nmy-api-prod\n\
    ```; Namespace 분리: 환경별:; Namespace 분리: ```text\nSecret\nConfigMap\nResourceQuota\nNetworkPolicy\n\
    RBAC\n```; Namespace 분리: 분리 가능.; Secret은 Values에 평문 저장하지 않기: 좋은 구조:; Secret은 Values에 평문 저장하지 않기: ```text\n\
    Helm Values\n→ Secret 이름만 참조\n\n실제 Secret\n→ Vault / Secrets Manager / External Secrets\n```; Promotion:\
    \ ```text\nImage Build\n↓\nDev\n↓\nStaging\n↓\nProd\n```; Promotion: 환경마다 새 Image를 Build하지 않고 같은 artifact를\
    \ 승격.; Git 구조 예: ```text\ndeploy/\n├─ chart/\n├─ dev/\n│  └─ values.yaml\n├─ staging/\n│  └─ values.yaml\n\
    └─ prod/\n   └─ values.yaml\n```; Git 구조 예: 핵심:; Git 구조 예: > Build once, deploy many"
  kind: 개념·조건·주의
  source_lines: 1742–1836
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-05
  knowledge: "Git 구조 예: GitOps:; Git 구조 예: > Kubernetes Desired State를 Git에 저장하고 실제 Cluster를 Git 상태와 계속\
    \ 맞추는 운영 방식; Source of Truth: Git:; Source of Truth: ```text\nimage.tag = 1.5.0\nreplicas = 3\n```;\
    \ Source of Truth: Production도 이 상태여야 한다.; 기존 배포 방식: ```text\nDeveloper\n↓\nGit Push\n↓\nCI\n↓\nhelm\
    \ upgrade / kubectl apply\n↓\nKubernetes\n```; GitOps 방식: ```text\nDeveloper\n↓\nGit Push\n↓\nCI\n\
    ├─ Test\n├─ Build\n└─ Registry Push\n```; GitOps 방식: 그 다음 배포 Git:; GitOps 방식: ```yaml\nimage:\n  tag:\
    \ \"1.5.0\"\n```; GitOps 방식: 변경.; GitOps 방식: ```text\nGit\n↓\nArgo CD\n↓\nKubernetes\n```; Pull-based\
    \ Deployment: ```text\nArgo CD\n→ Git 확인\n→ Kubernetes 반영\n```; Drift: Git:; Drift: ```text\nreplicas\
    \ = 3\n```; Drift: Cluster:; Drift: ```text\nreplicas = 10\n```; Drift: 이면 Drift.; Helm과 연결: ```text\n\
    Helm\n= Manifest 생성\n\nGit\n= Desired State 저장\n\nArgo CD\n= Git과 Cluster 동기화\n```; kubectl은 언제 쓰는가:\
    \ GitOps 환경에서 kubectl은 주로:; kubectl은 언제 쓰는가: ```text\n관찰\nTroubleshooting\n긴급 장애 대응\n```; kubectl은\
    \ 언제 쓰는가: 에 사용.; kubectl은 언제 쓰는가: 정상적인 설정/배포 변경은:; kubectl은 언제 쓰는가: ```text\nGit + Argo CD\n```; kubectl은\
    \ 언제 쓰는가: 가 기본.; kubectl은 언제 쓰는가: 자주 쓰는 진단 명령:; kubectl은 언제 쓰는가: ```text\nkubectl get pods\nkubectl\
    \ describe pod\nkubectl get events\nkubectl logs\nkubectl logs --previous\nkubectl exec\nkubectl top\n\
    kubectl get pvc\nkubectl get nodes\nkubectl port-forward\n```; kubectl은 언제 쓰는가: Break-glass 예:; kubectl은\
    \ 언제 쓰는가: ```bash\nkubectl cordon node-a\nkubectl drain node-a\n```; kubectl은 언제 쓰는가: 긴급 조치 후 Git과\
    \ 상태를 다시 맞춘다.; Argo CD / Grafana / kubectl 역할 구분: ```text\nArgo CD\n= 배포 상태 / Resource 구조 / Sync /\
    \ Health\n\nGrafana\n= Metrics / Logs / Alert\n\nkubectl\n= Kubernetes 상세 진단 / 즉시 확인\n```; Argo CD에서도\
    \ Pod 상태 조회 가능: ```text\nApplication\n↓\nDeployment\n↓\nReplicaSet\n↓\nPod\n```; Argo CD에서도 Pod 상태\
    \ 조회 가능: 트리 구조로 Health 확인 가능.; Argo CD에서도 Pod 상태 조회 가능: 그러나 상세 원인에는:; Argo CD에서도 Pod 상태 조회 가능: ```text\n\
    kubectl describe\nkubectl logs\nevents\n```; Argo CD에서도 Pod 상태 조회 가능: 가 더 직접적일 수 있다."
  kind: 개념·조건·주의
  source_lines: 1842–2017
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-06
  knowledge: "Argo CD에서도 Pod 상태 조회 가능: Argo CD:; Argo CD에서도 Pod 상태 조회 가능: > Git에 정의된 Kubernetes Desired\
    \ State와 실제 Cluster 상태를 비교하고 동기화하는 GitOps Controller; Argo CD에서도 Pod 상태 조회 가능: 핵심:; Argo CD에서도 Pod\
    \ 상태 조회 가능: ```text\nApplication\nSync\nHealth\nAuto Sync\nSelf Heal\nPrune\nRollback\n```; Application:\
    \ 배포 관리 단위.; Application: 대략:; Application: ```text\n어느 Git Repository?\n어느 경로?\n어느 Revision?\n어느\
    \ Cluster?\n어느 Namespace?\n```; Application: 를 정의.; Sync: ```text\nGit Desired State\n↓\nHelm / Manifest\
    \ Rendering\n↓\nKubernetes 적용\n↓\nActual State 일치\n```; Manual Sync: Git 변경 감지 후 OutOfSync까지만 표시하고\
    \ 운영자가 Sync.; Auto Sync: ```text\nGit 변경\n↓\nArgo CD 감지\n↓\n자동 Sync\n↓\nKubernetes Update\n```; Self\
    \ Heal: Cluster 직접 변경을 Git 상태로 복구.; Prune: Git에서 사라진 Resource를 Cluster에서도 제거.; Health: 실제 Resource의\
    \ 상태.; Sync와 Health 차이: ```text\nSynced\n= Git과 설정이 같다\n\nHealthy\n= Application이 정상 동작한다\n```; Sync와\
    \ Health 차이: 따라서:; Sync와 Health 차이: ```text\nSynced\nbut\nDegraded\n```; Sync와 Health 차이: 가능.; Rollback:\
    \ 과거 synced revision으로 되돌릴 수 있으나 GitOps 원칙상 Git 상태도 rollback 상태와 맞추는 것이 중요.; Helm과 Argo CD 역할: ```text\n\
    Helm\n= Kubernetes Manifest 생성\n\nArgo CD\n= Desired State를 Cluster와 동기화\n```; Argo CD에 Helm 경로를 알려줘야\
    \ 하는가: Git 안의 Helm Chart를 쓰는 경우 Argo CD Application에:; Argo CD에 Helm 경로를 알려줘야 하는가: ```text\n1. Git\
    \ Repository\n2. Branch / Commit\n3. Helm Chart 경로\n4. Values\n5. 대상 Cluster / Namespace\n```; Argo\
    \ CD에 Helm 경로를 알려줘야 하는가: 를 알려준다.; Argo CD에 Helm 경로를 알려줘야 하는가: 예:; Argo CD에 Helm 경로를 알려줘야 하는가: ```yaml\n\
    spec:\n  source:\n    repoURL: ...\n    targetRevision: main\n    path: apps/my-api\n```; Argo CD에\
    \ Helm 경로를 알려줘야 하는가: Repository 예:; Argo CD에 Helm 경로를 알려줘야 하는가: ```text\nplatform-deploy/\n├─ apps/\n\
    │  └─ my-api/\n│     ├─ Chart.yaml\n│     ├─ values.yaml\n│     └─ templates/\n└─ env/\n   └─ prod/\n\
    \      └─ values.yaml\n```; Argo CD Rollback과 Helm Release: Argo CD가 Helm을 사용하는 경우 Helm은 주로 Manifest\
    \ Rendering 역할.; Argo CD Rollback과 Helm Release: 따라서:; Argo CD Rollback과 Helm Release: ```text\nArgo\
    \ CD rollback\n→ 과거 Application revision\n→ 당시 Chart + Values 렌더링\n→ Kubernetes에 적용\n```; Argo CD\
    \ Rollback과 Helm Release: 이라고 이해하는 것이 정확.; Argo CD Rollback과 Helm Release: 단순히 Helm Release Secret\
    \ 하나를 다시 활성화하는 개념과는 다름.; Image 버전도 Helm Values에 작성 가능: ```yaml\nimage:\n  repository: registry.example.com/my-api\n\
    \  tag: \"1.3.0\"\n```; Image 버전도 Helm Values에 작성 가능: Git History:; Image 버전도 Helm Values에 작성 가능:\
    \ ```text\nCommit A → 1.2.0\nCommit B → 1.3.0\nCommit C → 1.4.0\n```; Image 버전도 Helm Values에 작성 가능:\
    \ 이전 Commit 상태로 돌아가면 이전 Image Tag가 다시 렌더링되어 적용될 수 있음."
  kind: 개념·조건·주의
  source_lines: 2023–2200
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-07
  knowledge: 'Image 버전도 Helm Values에 작성 가능: 핵심:; Image 버전도 Helm Values에 작성 가능: ```text

    Rolling

    Blue-Green

    Canary

    ```; Rolling Update: ```text

    v1 v1 v1

    ↓

    v2 v1 v1

    ↓

    v2 v2 v1

    ↓

    v2 v2 v2

    ```; Blue-Green: ```text

    Blue = 기존 Production

    Green = 새 버전

    ```; Blue-Green: Green 준비/검증 후 트래픽 전체 전환.; Blue-Green: 문제 시 Blue로 빠르게 원복.; Canary: ```text

    95% → v1

    5%  → v2

    ```; Canary: 점진적으로:; Canary: ```text

    80 / 20

    50 / 50

    0 / 100

    ```; AI Serving에서 Canary: 새 Model은:; AI Serving에서 Canary: ```text

    응답 품질

    TTFT

    TPOT

    VRAM

    OOM

    Tool Calling

    출력 형식

    ```; AI Serving에서 Canary: 등이 달라질 수 있으므로 일부 트래픽으로 먼저 검증.'
  kind: 개념·조건·주의
  source_lines: 2206–2266
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-08
  knowledge: 'AI Serving에서 Canary: AI Serving 배포는:; AI Serving에서 Canary: ```text

    Model Version

    vLLM Version

    Serving Configuration

    GPU Capacity

    ```; AI Serving에서 Canary: 를 함께 관리해야 한다.; Model Version: 예:; Model Version: ```text

    vLLM Image

    → vllm:0.x


    Model

    → glm-5.3-fp4-v1

    ```; Model Version: Serving 설정:; Model Version: ```text

    model

    max_model_len

    tensor_parallel_size

    kv_cache_dtype

    gpu_memory_utilization

    ```; Model Version: 도 Git에 기록하면 좋다.; 새 모델을 바로 교체하면 위험: 변할 수 있는 것:; 새 모델을 바로 교체하면 위험: ```text

    Weight 크기

    VRAM 사용량

    KV Cache 요구량

    TTFT

    TPOT

    Throughput

    응답 품질

    Tool Calling

    ```; vLLM Rollout: ```text

    새 vLLM / Model Pod

    ↓

    Model Load

    ↓

    GPU Memory 할당

    ↓

    Startup Probe

    ↓

    Readiness

    ```; vLLM Rollout: Ready 된 뒤 트래픽 전달.; LiteLLM Routing Migration: ```text

    100% → v1

    0%   → v2


    ↓ Canary


    95% → v1

    5%  → v2


    ↓ 확대


    80 / 20

    50 / 50

    0 / 100

    ```; 역할 분리: ```text

    Argo CD

    → vLLM / Model Resource 배포


    LiteLLM

    → 사용자 트래픽 전환

    ```; 검증 지표: ```text

    Error Rate

    TTFT

    TPOT

    Queue Time

    GPU Utilization

    VRAM / KV Cache

    OOM

    응답 품질

    ```; Safe Rollback: 문제 발생:; Safe Rollback: ```text

    20% → v1

    80% → v2


    ↓ 문제


    100% → v1

    0%   → v2

    ```; Safe Rollback: 그 후 Git / Argo CD에서 v2 Resource 제거 또는 수정.'
  kind: 개념·조건·주의
  source_lines: 2272–2393
  destination: platform-infrastructure/cicd-gitops.md
- id: PIS3-11-09
  knowledge: '검증 기간에는 구 모델 + 신 모델 동시 Capacity 필요: 예:; 검증 기간에는 구 모델 + 신 모델 동시 Capacity 필요: ```text

    기존 GLM-v1

    → GPU 4장


    새 GLM-v2

    → GPU 4장


    검증 기간

    → 최소 GPU 8장 수준 자원 필요

    ```; 검증 기간에는 구 모델 + 신 모델 동시 Capacity 필요: Blue-Green / Canary는 일시적인 추가 Capacity가 필요.; 기존 3 Replica
    예: ```text

    Replica A → GPU ×4

    Replica B → GPU ×4

    Replica C → GPU ×4


    총 12 GPU

    ```; 기존 3 Replica 예: 새 Canary:; 기존 3 Replica 예: ```text

    기존 12 GPU

    +

    신규 Replica D → GPU ×4

    =

    총 16 GPU

    ```; Spare Capacity 용도: ```text

    Node/GPU 장애 대응

    Rolling Update

    Canary

    Model Upgrade

    Traffic Spike

    ```; Spare GPU와 기존 Serving GPU의 남는 VRAM은 다름: 예:; Spare GPU와 기존 Serving GPU의 남는 VRAM은 다름: ```text

    B300 Node


    GPU 0~3 → GLM Replica A

    GPU 4~7 → Spare

    ```; Spare GPU와 기존 Serving GPU의 남는 VRAM은 다름: Replica A가 사용하는 GPU 0~3:; Spare GPU와 기존 Serving GPU의
    남는 VRAM은 다름: ```text

    GPU 0~3 VRAM


    ├─ Model Weight

    ├─ KV Cache

    ├─ Activation

    ├─ Runtime Buffer

    └─ 여유

    ```; Spare GPU와 기존 Serving GPU의 남는 VRAM은 다름: 여기서 남는 VRAM은 **Replica A의 KV Cache / Runtime Capacity**에
    사용된다.; Spare GPU와 기존 Serving GPU의 남는 VRAM은 다름: 반면 GPU 4~7이 비어 있다면:; Spare GPU와 기존 Serving GPU의 남는
    VRAM은 다름: ```text

    GPU 4~7

    = 새 Replica를 올릴 수 있는 Spare GPU

    ```; 새 모델도 Weight + KV Cache가 모두 필요: ```text

    Spare GPU

    ↓

    새 Model Weight

    +

    새 Model KV Cache

    +

    Activation

    +

    Runtime

    ```; 새 모델도 Weight + KV Cache가 모두 필요: 이 모두 들어가야 한다.; 새 모델도 Weight + KV Cache가 모두 필요: 따라서:; 새 모델도 Weight
    + KV Cache가 모두 필요: ```text

    새 Model Weight가 Spare GPU VRAM을 거의 100% 사용

    → KV Cache 공간 부족

    → Serving Capacity 부족

    ```; 새 모델도 Weight + KV Cache가 모두 필요: 가능.; 새 모델도 Weight + KV Cache가 모두 필요: 핵심:; 새 모델도 Weight + KV Cache가
    모두 필요: > "모델이 GPU에 들어간다"와 "실제로 서비스 가능한 Capacity가 있다"는 다르다.; VRAM은 기본적으로 GPU별 Local Memory: 새 모델이 기존
    Replica가 쓰는 GPU의 남는 VRAM을 자유롭게 공용 Pool처럼 빌려 쓰는 구조가 아니다.; VRAM은 기본적으로 GPU별 Local Memory: ```text

    GPU 0~3

    → Old GLM Weight + KV Cache


    GPU 4~7

    → New GLM Weight + KV Cache

    ```; 진짜 Serving Spare Capacity 판단: ```text

    Spare GPU 수

    ↓

    새 Model Weight가 들어가는가?

    ↓

    KV Cache 공간도 충분히 남는가?

    ↓

    목표 Context / Concurrency 가능한가?

    ↓

    TTFT / TPOT SLA 가능한가?

    ```; 진짜 Serving Spare Capacity 판단: 특히 1M Context LLM에서는 Weight 외 KV Cache Capacity가 매우 중요하다.'
  kind: 개념·조건·주의
  source_lines: 2401–2534
  destination: platform-infrastructure/cicd-gitops.md
---

# 10~11장 지식 추출

번호별 개념·예시·조건과 별도 GPU 용량 보충, 소개·연결·진도를 20개 ID로 추적한다. 페이지 작성 전에 담당별 상세 추출을 수행했다.
