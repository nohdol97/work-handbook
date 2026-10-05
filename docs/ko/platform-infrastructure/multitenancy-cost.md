---
id: platform-multitenancy-cost
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - PIS4-13-01
  - PIS4-13-02
  - PIS4-13-03
  - PIS4-13-04
  - PIS4-13-05
  - PIS4-13-06
  - PIS4-13-07
  - PIS4-13-08
  - PIS4-13-09
  - PIS4-13-10
---

# Chapter 13. Multi-tenancy, Quotas & Cost Control

제공된 학습 원문의 번호·순서·예시를 그대로 보존했다. 13.1–13.4의 격리 계층·Quota·LimitRange와 13.6–13.9의 LLM 제한·비용 수치는 뒤의 별도 보완 조건과 함께 읽는다. 예시는 실제 정책 적용이나 부하 실험 결과가 아니다.

<!-- SOURCE CORE START -->

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

<!-- SOURCE CORE END -->

## 보완 — 격리와 사용량 제한의 실제 범위

2026-10-05 공식 문서를 확인했다. Cluster 정책 배포·부하 시험·비용 측정은 수행하지 않았다.

### 13.1 / 13.2 격리는 단일 강도 순서가 아니다

원문의 화살표는 학습용 개념도다. Namespace, RBAC, NetworkPolicy, Quota는 서로 다른 문제를 다루며 하나가 다른 것을 대체하지 않는다. NetworkPolicy는 지원하는 CNI가 있어야 적용된다. Dedicated node도 공유 control plane의 격리 문제를 모두 해결하지는 않는다. [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)

Toleration은 해당 taint를 허용할 뿐 특정 node로 배치를 강제하지 않는다. 전용 배치에는 node affinity 등도 필요하며, tenant가 임의의 toleration이나 배치 설정으로 경계를 넘지 못하도록 정책을 확인한다. [Taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)

### 13.3 / 13.7 Quota는 실시간 사용률 제한이나 예약이 아니다

ResourceQuota는 주로 선언한 requests/limits의 합계와 object 수를 admission 시 제한한다. GPU device-plugin 자원 이름이 `nvidia.com/gpu`이면 quota 항목은 `requests.nvidia.com/gpu`다. Quota 초과로 생성이 거절된 경우와, 생성은 됐지만 배치 가능한 GPU가 없어 Pending인 경우를 구분한다. [Kubernetes ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/)

### 13.4 LimitRange의 적용 시점

LimitRange의 기본값 주입은 Container의 requests/limits에 적용되며 Pod·Container 최소/최대와 PVC 저장 요청 범위도 제약할 수 있다. 새 정책이 기존 실행 Pod를 다시 설정하지는 않는다. 기본값을 넣은 최종 requests/limits가 서로 일관되고 Quota 내에 있는지 확인한다. [Kubernetes LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/)

### 13.6–13.9 예시 수치와 비용 모델

`2M TPM`, 동시 요청 `10`, `128K` context는 원문의 정책 예시이며 LiteLLM의 기본값이나 검증된 권장값이 아니다. 실제 [LiteLLM](litellm.md) 설정과 [vLLM](vllm.md) 용량을 확인해야 한다. 요청 수나 token 비율로 나눈 비용은 배분 규칙이며 실제 GPU 실행 시간을 그대로 측정한 값은 아니다. 공유비·유휴비·장애 여유비의 처리 방식을 명시하고 합계가 실제 청구액과 맞는지 확인하는 것은 이 학습 예시를 적용할 때의 검토 기준이다.

## 관련 문서

- [Platform 학습 지도](index.md)
- [Kubernetes 운영](kubernetes-operations.md)
- [GPU 인프라](gpu-infrastructure.md)
- [Platform 보안](platform-security.md)
- [Terraform과 IaC](terraform-iac.md)
