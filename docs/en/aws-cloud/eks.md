---
id: aws-cloud-eks
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
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

This page preserves Chapter 5 of the latest compact source in its original structure. Read the **Supplement and conditions** for Karpenter behavior in 5.2, IP capacity in 5.3, controllers and Services in 5.4, CSI in 5.5, and permission associations in 5.7. This is Basic conceptual study, not a record of building EKS, changing AWS permissions, or running commands.

<!-- SOURCE CORE START -->

## 5.1 EKS structure

EKS = Elastic Kubernetes Service.

> AWS operates the Kubernetes control plane as a managed service.

```text
EKS
├─ Control Plane
│  └─ AWS Managed
└─ Data Plane
   ├─ Node
   ├─ Node
   └─ Node
```

AWS manages control plane components such as the API server, scheduler, controller manager, and etcd.

The actual Pods run on worker nodes.

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
> A group of worker nodes with similar characteristics

```text
EKS
├─ General Node Group
└─ GPU Node Group
```

Settings for each node group:
- Instance Type
- AMI
- Subnet
- Scaling range
- On-Demand / Spot

### Managed Node Group
AWS helps manage much of the node lifecycle.

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
You can set `Min / Desired / Max`.

However, an autoscaler is needed to decide when to add or remove nodes based on pending Pods.

```text
Pod Pending
 ↓
Cluster Autoscaler / Karpenter
 ↓
Node Group Scale Out
```

```text
Node Group = Which node pool to operate
Autoscaler = When to add and remove nodes
```

---

## 5.3 VPC CNI / Pod IP

CNI = Container Network Interface.

The Amazon VPC CNI in EKS lets Pods receive VPC IP addresses directly.

Example:
```text
Subnet 10.0.1.0/24
├─ Node 10.0.1.10
├─ Pod A 10.0.1.21
└─ Pod B 10.0.1.22
```

Pods also consume addresses from the subnet IP pool.

Therefore:
```text
More Pods
 ↓
More subnet IP consumption
 ↓
Possible IP exhaustion
```

### Subnet size
`/24 = 256 addresses`, but only 251 are usable, shared by nodes, Pods, ENIs, and other resources.

If you expect growth:
- Larger private subnets
- Additional private subnets
- Distribute nodes across multiple AZs/subnets

These are options to consider.

Example:
```text
/24 = 256 addresses
/20 = 4096 addresses
```

An existing subnet cannot simply be expanded from `/24 → /20`, so initial CIDR planning matters.

---

## 5.4 AWS Load Balancer Controller

> Connects Kubernetes resources with AWS load balancers.

Common mappings:
```text
Ingress → ALB
Service type=LoadBalancer → NLB
```

The controller watches Kubernetes resources and calls AWS APIs to create or update ALBs/NLBs, listeners, target groups, and other resources.

Targets depend on configuration:
```text
instance target → EC2 Node
ip target → Pod IP
```

### Final distinction between roles
```text
Kubernetes Service
= A stable endpoint for Pod replicas + L4 load distribution

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

EBS is scoped to an AZ, so Pod scheduling must also account for the volume's AZ.

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

Used when multiple Pods share the same file system.

Summary:
```text
Disk dedicated to a Pod → EBS
File system shared by multiple Pods → EFS
Object / Dataset / Model → S3
```

---

## 5.6 ECR

ECR = Elastic Container Registry.

> AWS Managed Container Image Registry

Basic flow:
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
Run the Pod
```

### Repository / Tag
Images are managed by repository, and tags distinguish versions.

### IAM authentication
The EKS node or relevant AWS identity needs permission to pull ECR images.

### AI Platform
```text
ECR = Executable code / Container image
S3 = Model Weight / Dataset / Artifact
```

---

## 5.7 Pod Identity / IAM

Pods use IAM roles to access AWS resources instead of storing access keys directly.

```text
Pod
 ↓
IAM Role
 ↓
S3 / SQS / Secrets Manager
```

Using only the node role can give excessive permissions because multiple Pods on the same node share those permissions.

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

Example:
```text
model-loader → S3 Read Role
api → Secrets Manager Read Role
worker → SQS Consume Role
```

### IRSA
IAM Roles for Service Accounts.

For a basic understanding:
```text
IRSA / Pod Identity
= Associate an IAM role with Pods
```

This is the basic idea.

### Distinguish from RBAC
```text
Pod → Kubernetes API = RBAC
Pod → AWS Resource = IAM
```

---

# Overall Chapter 5 structure

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
Internal access to Pod replicas → Kubernetes Service
```

---

<!-- SOURCE CORE END -->

## Key points

Diagnose EKS failures by separating control plane, node, Pod, image, storage, and permission concerns.

## LLM in Practice: review EKS Pod startup failures by layer


**Prompt:**

=== "한국어"

    ```text {.prompt}
    EKS Pod 시작 실패를 조사할 때 IP·image pull·volume·애플리케이션 IAM 계층을 구분한다.
    Pod 시작 단계를 event 순서로 추적하고 각 실패를 IP·image·volume·IAM 가설로 분류하라. Pending을 node 부족으로 단정하지 말고 EC2 node role/Fargate execution role과 앱 role을 구분하라.
    실패 단계 / 오류·시각 / 책임 identity 또는 구성 / 누락 증거 / 다음 확인 표를 작성하라. CNI 주소·ENI/maxPods, CSI 권한·AZ, agent/SDK·OIDC·trust 조건을 관련 오류에 연결하고 최소 수정 후보와 재검증 기준을 적어라.
    비밀값은 요구하거나 출력하지 말고, 검토안만 작성해 줘. 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Separate IP, image-pull, volume, and application-IAM failures when investigating EKS Pod startup.
    Trace startup stages in event order and classify failures into IP, image, volume, and IAM hypotheses. Do not infer node shortage from Pending. Distinguish the EC2 node/Fargate execution role from the application role.
    Produce a table: failed stage / error and time / responsible identity or setting / missing evidence / next check. Link CNI addresses and ENI/maxPods, CSI permissions and zones, and agent/SDK, OIDC and trust conditions to the relevant error. Give minimal proposals and recheck criteria.
    Do not request or reveal secrets. Draft a review only; do not apply changes.
    ```

**Key point:** IP, image, volume, and IAM failure layers in startup-event order, responsible identities/settings, and minimal fixes with recheck criteria. It may assume one Pod-role change fixes image pulls and volumes, or confuse IAM with Kubernetes RBAC. Align event and CNI/CSI/controller-log timestamps with IAM associations. Separate image-pull identity from application roles and link IP/ENI, zone, agent/SDK, and trust conditions to the relevant errors. This is an authored work example, not a verified model result or measured improvement.

## Supplement and conditions

Official documentation checked: 2026-10-04. These conditions are separate from the source and were not tested on a real cluster.

### 5.1–5.2: Managed scope and autoscalers

The source focuses on EC2 worker nodes. A managed control plane does not replace application, node-capacity, or availability design. Cluster Autoscaler adjusts Auto Scaling Groups, while Karpenter provisions nodes directly for workload requirements. Do not read the source's `Karpenter → Node Group Scale Out` as increasing an existing Managed Node Group. EKS Auto Mode compute automation is another operating model. [AWS EKS autoscaling](https://docs.aws.amazon.com/eks/latest/userguide/autoscaling.html).

### 5.3: IP counts and actual Pod capacity

`251` is the address count after subtracting 5 AWS-reserved addresses from an ordinary IPv4 `/24` subnet. It does not guarantee room for 251 Pods. Account for nodes, ENIs, other resources, CNI address reservations, and instance ENI/IP and maxPods limits. Prefix delegation also requires checking free subnet space and configuration. Do not apply the source's IPv4 arithmetic directly to IPv6. [VPC CNI](https://docs.aws.amazon.com/eks/latest/userguide/managing-vpc-cni.html), [Prefixes and Pod IP capacity](https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html).

### 5.4: Controller and Service responsibilities

Creating an Ingress or LoadBalancer Service does not always create an ALB or NLB. A controller that handles it, the right class, IAM permissions, and subnet settings are required. Distinguish Auto Mode management from an AWS Load Balancer Controller you install. [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html).

The source describes a typical Service. A headless Service has no cluster IP or platform proxy/load balancing. Controller calls to AWS APIs are control flow; each application request does not pass through the controller. [Kubernetes Service](https://kubernetes.io/docs/concepts/services-networking/service/).

### 5.5: CSI permissions and storage constraints

Declaring a PVC does not automatically connect every storage system. Provide a compatible CSI driver and IAM permissions, and check StorageClass/PV settings and static or dynamic provisioning. Check EBS AZ topology with scheduling; EBS volumes cannot be mounted by Fargate Pods. EFS works with Fargate, but dynamic provisioning is unsupported there, so use static provisioning. The source's dedicated-disk/shared-file distinction describes roles, not guarantees of concurrent filesystem-write consistency or backups. [EBS CSI](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html), [EFS CSI](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html).

### 5.6–5.7: Separate image pulls from application IAM

For ECR image pulls on EC2 nodes, check the node IAM role. Fargate uses the pod execution role. Do not confuse the application's Pod Identity/IRSA role with image-pull permissions. [ECR on EKS](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html).

Pod Identity associates a cluster, namespace, and ServiceAccount with an IAM role. A standard EC2-node setup needs the Pod Identity Agent, a supported SDK credential chain, and correct role trust and permissions. Auto Mode includes agent functionality. IRSA uses a cluster OIDC provider and ServiceAccount tokens instead. A matching ServiceAccount name alone does not grant permissions. [Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html), [Agent setup](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-agent-setup.html), [IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html).

Even with a separate Pod role, node credentials may remain accessible unless node IMDS access is restricted. Pod Identity does not make containers an independent security boundary. The shared `IAM Role` box in the final diagram shows role association; it is not a recommendation to share one broad role across every workload. [Pod Identity isolation conditions](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).

[Existing Kubernetes operations](../platform-infrastructure/kubernetes-operations.md) · [Platform security](../platform-infrastructure/platform-security.md)
