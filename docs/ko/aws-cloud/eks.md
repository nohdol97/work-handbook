---
id: aws-cloud-eks
status: studied
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids:
  - AWSC-05-01
  - AWSC-05-02
  - AWSC-05-03
  - AWSC-05-04
  - AWSC-05-05
  - AWSC-05-06
  - AWSC-05-07
  - AWSC-05-08
---

# Chapter 5. EKS on AWS

최신 compact 자료의 Chapter 5를 원문 형태로 보존했다. 5.2의 Karpenter 동작, 5.3의 IP 용량, 5.4의 Controller·Service, 5.5의 CSI와 5.7의 권한 연결 조건은 뒤의 **보완 및 적용 조건**을 함께 읽는다. Basic 개념 학습이며 실제 EKS 구축·AWS 권한 변경·명령 실행의 기록이 아니다.

<!-- SOURCE CORE START -->

## 5.1 EKS 구조

EKS = Elastic Kubernetes Service.

> AWS가 Kubernetes Control Plane을 Managed 형태로 운영한다.

```text
EKS
├─ Control Plane
│  └─ AWS Managed
└─ Data Plane
   ├─ Node
   ├─ Node
   └─ Node
```

Control Plane의 API Server, Scheduler, Controller Manager, etcd 등을 AWS가 관리한다.

Worker Node에서 실제 Pod가 실행된다.

```text
VPC
 ↓
Private Subnet
 ↓
EC2 Node
 ↓
Pod
```

---

## 5.2 Node Group / Managed Node Group

Node Group:
> 같은 특성의 Worker Node 묶음

```text
EKS
├─ General Node Group
└─ GPU Node Group
```

Node Group별 설정:
- Instance Type
- AMI
- Subnet
- Scaling 범위
- On-Demand / Spot

### Managed Node Group
AWS가 Node Lifecycle 관리의 상당 부분을 도와준다.

```text
EKS
 ↓
Managed Node Group
 ↓
EC2 Auto Scaling Group
 ↓
EC2 Nodes
```

### Scaling
`Min / Desired / Max`를 설정할 수 있다.

하지만 Pod Pending을 보고 실제 Node 증감을 판단하려면 Autoscaler가 필요하다.

```text
Pod Pending
 ↓
Cluster Autoscaler / Karpenter
 ↓
Node Group Scale Out
```

```text
Node Group = 어떤 Node Pool을 운영할지
Autoscaler = 언제 Node를 늘리고 줄일지
```

---

## 5.3 VPC CNI / Pod IP

CNI = Container Network Interface.

EKS의 Amazon VPC CNI는 Pod가 VPC IP를 직접 받을 수 있게 한다.

예:
```text
Subnet 10.0.1.0/24
├─ Node 10.0.1.10
├─ Pod A 10.0.1.21
└─ Pod B 10.0.1.22
```

Pod도 Subnet IP Pool을 소비한다.

따라서:
```text
Pod 증가
 ↓
Subnet IP 소비 증가
 ↓
IP 고갈 가능
```

### Subnet 크기
`/24 = 256개`지만 실제 사용 가능은 251개이고 Node/Pod/ENI 등이 함께 사용한다.

규모가 커질 것 같다면:
- 더 큰 Private Subnet
- 추가 Private Subnet
- 여러 AZ/Subnet으로 Node 분산

을 고려한다.

예:
```text
/24 = 256 주소
/20 = 4096 주소
```

이미 만든 Subnet을 단순히 `/24 → /20`으로 확장하는 방식은 사용할 수 없으므로 초기 CIDR 설계가 중요하다.

---

## 5.4 AWS Load Balancer Controller

> Kubernetes Resource와 AWS Load Balancer를 연결한다.

대표:
```text
Ingress → ALB
Service type=LoadBalancer → NLB
```

Controller가 Kubernetes 리소스를 감시하고 AWS API를 호출해 ALB/NLB, Listener, Target Group 등을 생성/수정한다.

Target은 구성에 따라:
```text
instance target → EC2 Node
ip target → Pod IP
```

### 최종 역할 구분
```text
Kubernetes Service
= Pod Replica의 안정적 Endpoint + L4 분산

ALB
= HTTP/HTTPS L7 Routing

NLB
= TCP/UDP/TLS L4 Routing
```

---

## 5.5 EBS / EFS CSI Driver

CSI = Container Storage Interface.

```text
EBS CSI Driver → EBS
EFS CSI Driver → EFS
```

### EBS CSI
```text
Pod
 ↓
PVC
 ↓
EBS CSI Driver
 ↓
EBS
```

EBS는 AZ 단위이므로 Pod Scheduling에서도 Volume AZ를 고려해야 한다.

### EFS CSI
```text
Pods
 ↓
PVC
 ↓
EFS CSI Driver
 ↓
EFS
```

여러 Pod가 같은 파일시스템을 공유할 때 사용.

정리:
```text
Pod 전용 Disk → EBS
여러 Pod 공유 File System → EFS
Object / Dataset / Model → S3
```

---

## 5.6 ECR

ECR = Elastic Container Registry.

> AWS Managed Container Image Registry

기본 흐름:
```text
Source Code
 ↓
docker build
 ↓
Container Image
 ↓
ECR
 ↓
EKS Node Pull
 ↓
Pod 실행
```

### Repository / Tag
Repository별로 Image를 관리하고 Tag로 버전을 구분한다.

### IAM 인증
EKS Node 또는 관련 AWS Identity에 ECR Image Pull 권한이 필요하다.

### AI Platform
```text
ECR = 실행 코드 / Container Image
S3 = Model Weight / Dataset / Artifact
```

---

## 5.7 Pod Identity / IAM

Pod가 AWS Resource에 접근할 때 Access Key를 직접 저장하지 않고 IAM Role을 사용한다.

```text
Pod
 ↓
IAM Role
 ↓
S3 / SQS / Secrets Manager
```

Node Role만 사용하면 같은 Node의 여러 Pod가 권한을 공유하게 되어 과도한 권한이 생길 수 있다.

### EKS Pod Identity
```text
Pod
 ↓
ServiceAccount
 ↓
EKS Pod Identity
 ↓
IAM Role
 ↓
AWS Resource
```

예:
```text
model-loader → S3 Read Role
api → Secrets Manager Read Role
worker → SQS Consume Role
```

### IRSA
IAM Roles for Service Accounts.

Basic에서는:
```text
IRSA / Pod Identity
= Pod 단위 IAM Role 연결
```

로 이해하면 된다.

### RBAC과 구분
```text
Pod → Kubernetes API = RBAC
Pod → AWS Resource = IAM
```

---

# Chapter 5 전체 구조

```text
                    Internet
                       ↓
                      ALB
                       ↓
                      EKS
          ┌────────────┴────────────┐
          │                         │
   General Node Group         GPU Node Group
          │                         │
         Pods                    vLLM Pods
          │                         │
          └──── Pod Identity ───────┘
                       ↓
                    IAM Role
                 /      |       \
               S3      SQS   Secrets Manager
```

Storage:
```text
PVC
├─ EBS CSI → EBS
└─ EFS CSI → EFS
```

Container Image:
```text
ECR → EKS Node → Pod
```

Network:
```text
VPC
 ↓
Private Subnet
 ↓
EC2 Node
 ↓
VPC CNI
 ↓
Pod IP
```

Traffic:
```text
HTTP/HTTPS → ALB
TCP/UDP → NLB
Pod Replica 내부 접근 → Kubernetes Service
```

---

<!-- SOURCE CORE END -->

## 보완 및 적용 조건

공식 문서 확인일: 2026-10-04. 아래 조건은 원문 밖 보완이며 실제 클러스터에서 시험한 결과가 아니다.

### 5.1~5.2: Managed 범위와 Autoscaler

원문은 EC2 worker node 중심 구조다. Managed control plane이 애플리케이션·node 용량·가용성 설계를 대신하지 않는다. Cluster Autoscaler는 Auto Scaling Group을 조절하지만, Karpenter는 workload 요구에 맞춰 node를 직접 provision한다. 따라서 원문의 `Karpenter → Node Group Scale Out`을 기존 Managed Node Group 증설로 해석하지 않는다. EKS Auto Mode의 compute 자동화도 별도 운영 방식이다. [AWS EKS autoscaling](https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html).

### 5.3: IP 주소 수와 실제 Pod 용량

`251`은 일반 IPv4 `/24` subnet에서 AWS 예약 5개를 뺀 주소 수이지 Pod 251개 실행 보장이 아니다. Node·ENI·다른 리소스·CNI의 미리 확보한 주소와 instance별 ENI/IP·maxPods 한도를 함께 본다. Prefix delegation도 남은 subnet 공간과 설정 조건을 확인해야 한다. 원문의 IPv4 계산을 IPv6에 그대로 적용하지 않는다. [VPC CNI](https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html), [Prefix와 Pod IP 용량](https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html).

### 5.4: Controller와 Service가 담당하는 범위

Ingress·LoadBalancer Service를 만들기만 하면 항상 ALB·NLB가 생기는 것은 아니다. 해당 리소스를 처리할 controller·class·IAM 권한·subnet 설정이 필요하다. Auto Mode와 직접 설치한 AWS Load Balancer Controller의 관리 방식을 구분한다. [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html).

원문의 Service 역할은 일반적인 Service 설명이다. Headless Service는 cluster IP와 플랫폼의 proxy/load balancing을 제공하지 않는다. Controller의 AWS API 호출은 제어 흐름이며 매 요청이 controller를 통과한다는 뜻이 아니다. [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/).

### 5.5: CSI 권한과 저장소 제약

PVC 선언만으로 모든 저장소가 자동 연결되지는 않는다. 호환되는 CSI driver와 IAM 권한을 갖추고, StorageClass/PV 설정과 static·dynamic provisioning 방식을 확인한다. EBS의 AZ topology와 scheduling을 함께 확인하며 EBS 볼륨은 Fargate Pod에 mount할 수 없다. EFS는 Fargate에서 사용할 수 있지만 dynamic provisioning은 지원하지 않아 static provisioning을 사용한다. 원문의 전용 disk·공유 file 구분은 역할 설명이며 filesystem 동시 쓰기 정합성이나 backup 보장이 아니다. [EBS CSI](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html), [EFS CSI](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html).

### 5.6~5.7: Image pull과 애플리케이션 IAM 분리

EC2 node 기반 ECR image pull 권한은 node IAM role에서 확인한다. Fargate는 pod execution role을 사용한다. 애플리케이션에 연결한 Pod Identity/IRSA role을 image pull 권한과 혼동하지 않는다. [ECR on EKS](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html).

Pod Identity는 cluster·namespace·ServiceAccount와 IAM role의 association이다. 일반 EC2 node 구성에서는 Pod Identity Agent, 지원 SDK credential chain, 올바른 role trust·permission이 필요하다. Auto Mode에는 agent 기능이 포함된다. IRSA는 cluster OIDC provider와 ServiceAccount token을 사용하는 다른 연결 방식이다. ServiceAccount 이름만 같다고 권한이 자동 부여되지는 않는다. [Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html), [Agent 설정](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html), [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).

Pod에 별도 role을 연결해도 node IMDS 접근을 제한하지 않으면 node 자격 증명 접근이 남을 수 있다. Pod Identity는 container를 독립 보안 경계로 바꾸지 않는다. 최종 구조도의 공통 `IAM Role`은 역할 연결을 나타내며 모든 workload에 하나의 광범위한 role을 공유하라는 뜻이 아니다. [Pod Identity 격리 조건](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).

[기존 Kubernetes 운영](../platform-infrastructure/kubernetes-operations.md) · [플랫폼 보안](../platform-infrastructure/platform-security.md)

## LLM 실무: EKS Pod 시작 실패를 계층별로 검토

- **상황:** 가상 model-loader Pod가 시작되지 않아 IP·image·volume·IAM 원인을 구분해야 한다.
- **LLM에 줄 맥락:** 비식별 event·상태·subnet 여유 IP·node 한도·image pull identity·PVC/CSI·ServiceAccount/role association. 키와 토큰은 제외한다.
- **예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 model-loader Pod의 상태·events·실패 시각: [비식별 관측]
    Node/CNI/IP 여유, image pull identity, PVC/CSI, SA/role association: [설정 또는 모름]
    [요청]
    현재 구성을 먼저 읽고 관측·가정·IP/image/volume/IAM 가설을 구분하세요.
    [출력]
    계층별 근거, 누락 정보, 다음 읽기 전용 확인을 표로 제시하세요.
    [검증]
    Pod Pending만으로 node 부족을 단정하지 마세요.
    Image pull role과 애플리케이션 role을 구분하고 공식 조건과 대조하세요.
    AWS 변경·권한 확대·Pod 재시작을 실행하지 말고 비밀값을 요구하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    State, events, and failure time for a hypothetical model-loader Pod: [sanitized observations]
    Node/CNI/IP capacity, image-pull identity, PVC/CSI, SA/role association: [settings or unknown]
    [Task]
    Read the current setup first and separate observations, assumptions, and IP/image/volume/IAM hypotheses.
    [Output]
    Provide a table of evidence, missing information, and next read-only checks by layer.
    [Checks]
    Do not infer a node shortage from Pod Pending alone.
    Distinguish the image-pull role from the application role and compare with official conditions.
    Do not change AWS resources, broaden permissions, restart Pods, or request secrets.
    ```

- **기대 출력:** 실패 계층별 증거표, 원인을 확정하기 전에 필요한 추가 관측과 확인 순서.
- **LLM이 틀릴 수 있는 점:** 모든 Pending을 node 부족으로 보거나, Pod role만 바꾸면 image pull과 volume 문제가 모두 해결된다고 단정할 수 있다.
- **검증 방법:** 같은 시간대의 event·controller log·CNI/IP 상태·CSI·IAM 설정을 공식 문서와 비교한다. 필요한 시험은 별도 격리 환경에서 승인 범위로 수행한다. 이 페이지에서는 실제 시험이나 모델 실행을 하지 않았다.
