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

This page preserves the supplied study source’s numbering, order, and examples. Read the isolation layers, quotas, and LimitRange in 13.1–13.4, and the LLM limits and cost examples in 13.6–13.9, with the separate supplement. The examples are not results of policy deployment or load tests.

<!-- SOURCE CORE START -->

## 13.1 Multi-tenancy Models

Several teams can share one platform at different levels.

```text
Shared Cluster
↓
Namespace-based isolation
↓
Dedicated Node Pool
↓
Dedicated Cluster
```

In a typical internal AI platform:

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

Use this as the baseline, and separate node pools or clusters when stronger isolation is needed.

---

## 13.2 Isolation Layer

Think of increasing isolation strength as:

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

This is one way to view the layers.

### Namespace

A logical resource boundary.

### RBAC

Restrict who can act on which resources.

### NetworkPolicy

Restrict communication between services.

### Node Isolation

Use labels, taints, and similar controls to place only specific workloads on specific nodes.

---

## 13.3 ResourceQuota

ResourceQuota limits aggregate resource usage across a namespace.

Example:

```text
Team A Namespace

CPU <= 100
Memory <= 500Gi
GPU <= 8
```

It can also limit the number of some Kubernetes objects.

Important:

> A quota does not reserve actual resources.

Example:

```text
GPU quota = 8
```

Even with this quota, a Pod stays Pending if the cluster has no available GPUs.

---

## 13.4 LimitRange

LimitRange defines defaults and minimum/maximum values for individual Pods and containers.

Example:

```text
Default CPU Request
Default Memory Request
Maximum Memory
Minimum CPU
```

Distinction:

```text
ResourceQuota
= Aggregate limit across a namespace

LimitRange
= Defaults and minimum/maximum settings for Pods and containers
```

They are often used together.

---

## 13.5 Fairness and Noisy Neighbors

One team's excessive resource usage can affect other teams.

This is called a noisy neighbor.

Possible controls:

```text
Quota
PriorityClass
Preemption
Dedicated Resource
```

Fairness does not always mean allocating equal resources.

Example:

```text
Production Service
> Development Experiment
```

Resources can be managed differently based on importance and SLA, as shown here.

---

## 13.6 AI / LLM Quota

Limiting only Kubernetes resources is not enough for an AI platform.

LLM usage also needs limits.

Example:

```text
RPM
TPM
Concurrent Requests
Max Context Length
GPU Quota
```

In a shared vLLM pool in particular:

```text
1M Context Request
+
High concurrency
```

This can consume much of the KV cache and slow down other teams too.

Therefore:

```text
TPM
Concurrency
Context Length
```

Limit these per tenant.

---

## 13.7 Difference between Kubernetes Quotas and LLM Quotas

```text
Kubernetes ResourceQuota
→ Physical resources such as CPU / Memory / GPU

LLM Quota
→ Service usage such as tokens / requests / context / concurrency
```

Both are needed.

Example:

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

To reduce cost, first know who uses how much.

Example:

```text
Team
Service
Model
GPU Usage
Token Usage
```

Connect these dimensions.

Dedicated GPU:

```text
GPU-hours
```

This makes cost easier to calculate.

Shared vLLM:

```text
Input Tokens
Output Tokens
Model
Context
Request Metadata
```

These can be used to allocate cost.

Shared infrastructure and spare capacity also cost money.

Therefore:

```text
Tag
Label
Namespace
Owner
```

These are important.

---

## 13.9 GPU Cost Optimization

Optimizing GPU cost requires more than looking at one GPU utilization number.

What to examine:

```text
GPU Compute Utilization
VRAM
KV Cache
Queue
Throughput
Latency
```

Methods:

- Continuous Batching
- An appropriate number of model replicas
- Sharing for small workloads
- Autoscaling
- Right-sizing
- Quantization
- Appropriate context limits

Removing all spare capacity to cut cost can make HA, canaries, rolling updates, and traffic spikes harder to handle.

Therefore:

```text
Cost
vs
Reliability / SLA
```

Consider both together.

---

## 13.10 Showback / Chargeback

### Showback

Show cost information to teams without actually charging them.

### Chargeback

Apply actual costs to each team's budget.

For internal platforms, in general:

```text
Cost Attribution
↓
Showback
↓
Quota
↓
Chargeback if needed
```

This is a practical order of development.

Costs of shared resources:

- Proportional to usage
- Equal allocation
- Covered by a shared platform budget

These are some ways to allocate them.

---

<!-- SOURCE CORE END -->

## Supplement — What isolation and usage limits actually cover

Official documentation checked on 2026-10-05. No cluster policies were deployed, and no load tests or cost measurements were performed.

### 13.1 / 13.2 Isolation is not one ranking of strength

The source's arrows are a learning model. Namespaces, RBAC, NetworkPolicy, and quotas address different problems; one does not replace another. NetworkPolicy needs a supporting CNI. Dedicated nodes do not solve every isolation issue in a shared control plane. [Kubernetes multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/)

A toleration permits a taint; it does not force placement on a particular node. Dedicated placement also needs controls such as node affinity. Check policies that prevent tenants from crossing boundaries with arbitrary tolerations or placement settings. [Taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)

### 13.3 / 13.7 Quotas do not cap live utilization or reserve capacity

ResourceQuota mainly limits declared request/limit totals and object counts at admission. For the GPU device-plugin resource `nvidia.com/gpu`, the quota key is `requests.nvidia.com/gpu`. Distinguish creation rejected for exceeding quota from a created Pod that stays Pending because no suitable GPU is available. [Kubernetes ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/)

### 13.4 When LimitRange applies

LimitRange supplies default Container requests/limits. It can also constrain Pod/Container minimums and maximums, and PVC storage requests. A new policy does not reconfigure existing running Pods. Check that the final requests/limits after defaults are consistent and fit the quota. [Kubernetes LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/)

### 13.6–13.9 Example numbers and cost models

`2M TPM`, `10` concurrent requests, and `128K` context are source policy examples, not LiteLLM defaults or validated recommendations. Check actual [LiteLLM](litellm.md) settings and [vLLM](vllm.md) capacity. Dividing cost by requests or tokens is an allocation rule, not a direct measurement of GPU execution time. When applying this study example, define how shared, idle, and failure-reserve costs are handled and reconcile allocated totals with actual bills.

## Related topics

- [Platform study map](index.md)
- [Kubernetes operations](kubernetes-operations.md)
- [GPU infrastructure](gpu-infrastructure.md)
- [Platform security](platform-security.md)
- [Terraform and IaC](terraform-iac.md)
