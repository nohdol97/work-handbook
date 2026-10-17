---
id: platform-infrastructure-gpu-infrastructure
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - PIS2-09-01
  - PIS2-09-02
  - PIS2-09-03
  - PIS2-09-04
  - PIS2-09-05
  - PIS2-09-06
  - PIS2-09-07
  - PIS2-09-08
  - PIS2-09-09
---

# Chapter 9. GPU Infrastructure & Scheduling

The configurations and commands are study examples, not results of a deployment or failure test.

<!-- SOURCE CORE START -->

## 9.1 GPU Fundamentals

GPU capacity is more than a count of empty seats. A model that needs several GPUs on one node also depends on placement and capacity after a node failure.

A GPU is an accelerator that processes large parallel workloads quickly.

Key points:

```text
CPU vs GPU
CUDA
VRAM
GPU Compute
```

### CPU vs GPU

CPU:
- General-purpose logic
- OS
- Application
- DB

GPU:
- Matrix multiplication
- Tensor operations
- AI training / inference

### CUDA

```text
Application / PyTorch / vLLM
↓
CUDA
↓
NVIDIA GPU
```

### VRAM

Memory dedicated to the GPU.

In LLM serving, it holds:

```text
Model Weights
KV Cache
Activation
Runtime
```

These use VRAM.

### VRAM vs Compute

```text
VRAM
= How much it can hold

GPU Compute
= How fast it can compute
```

Example:

```text
VRAM 95%
GPU Util 20%
→ High memory use, spare compute capacity

VRAM 60%
GPU Util 100%
→ Compute bottleneck
```

**Interpreting utilization and capacity**

**`GPU Util 100% → Compute bottleneck` is not a conclusive diagnosis.** In the [NVIDIA nvidia-smi documentation](https://docs.nvidia.com/deploy/nvidia-smi/index.html), GPU utilization measures the fraction of a sample period with a running kernel. It does not directly measure use of peak compute throughput. Check memory bandwidth, communication, kernel efficiency, clock limits, and CPU input delays together. Low utilization does not necessarily mean spare compute capacity either.

The 9.8 example of 8 concurrent requests per replica and a peak of 24 assumes linear scaling to 3 replicas. Test actual request-length distributions, queues, routing imbalance, and failure-time SLOs under load. See section 7.2 and the capacity calculation in [vLLM](vllm.md) for GLM/B300 numbers and unit assumptions.

---

## 9.2 NVIDIA Container Stack

Core stack:

```text
vLLM
↓
CUDA Runtime
↓
NVIDIA Container Toolkit
↓
NVIDIA Driver
↓
GPU
```

### NVIDIA Driver

The host OS controls the GPU.

A common inspection command:

```bash
nvidia-smi
```

### CUDA Runtime

The runtime that lets vLLM/PyTorch use GPU computation inside the container.

### NVIDIA Container Toolkit

Makes the host GPU available to containers.

### The driver runs on the host

```text
Host
└─ NVIDIA Driver

Container
└─ CUDA Runtime
```

### Version Compatibility

The container CUDA runtime must be compatible with the host NVIDIA driver.

---

## 9.3 Kubernetes GPU

Key points:

```text
Device Plugin
GPU Resource Request
GPU Scheduling
```

### NVIDIA Device Plugin

Registers the node's GPU resources with Kubernetes.

Example:

```text
nvidia.com/gpu = 8
```

### Pod GPU Request

```yaml
resources:
  limits:
    nvidia.com/gpu: 4
```

### Scheduling

The scheduler selects a node with available GPUs.

### Basic GPU allocation

Usually in whole numbers:

```text
1 GPU
2 GPU
4 GPU
```

Sharing such as 0.5 GPU requires a separate mechanism.

### GPU shortage

```text
No GPU capacity available
↓
Pod Pending
```

### Device Plugin vs Container Toolkit

```text
Device Plugin
→ Lets Kubernetes schedule GPUs

Container Toolkit
→ Lets containers actually use GPUs
```

**GPU requests, placement, and sharing**

Under [Kubernetes GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/), a GPU `limits` value also becomes the request when no request is given. If both are present, they must match. Check resources and constraints on one node that can host the pod, rather than total cluster headroom. In 9.4, a toleration permits a taint but does not ensure placement on a particular node. Distinguish taint effects and required/preferred affinity.

The [NVIDIA GPU sharing documentation](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html) states that time slicing provides no memory/fault isolation between replicas and does not guarantee compute proportional to request count. MIG partitions only supported GPUs and profiles. Dedicated GPUs, time slicing, MIG, and MPS cannot be exchanged based only on the source's selection guide.

---

## 9.4 GPU Node Pool

> Manage GPU nodes as a separate group from general nodes

### Layout

```text
Kubernetes Cluster

General Node Pool
├─ Node A
├─ Node B

GPU Node Pool
├─ B300 Node 1
└─ B300 Node 2
```

### Label / Affinity

```text
gpu=true
gpu-type=b300
```

### Taint

Restricts ordinary pods from entering GPU nodes.

### Toleration

Allows GPU workloads to enter those nodes.

### Affinity + Toleration

```text
Affinity
→ Select where to go

Toleration
→ Allow entry to that node
```

---

## 9.5 GPU Sharing

Key points:

```text
Dedicated GPU
Time Slicing
MIG
MPS
```

### Dedicated GPU

One workload has exclusive use of one GPU.

Advantages:
- Easier to predict performance
- Less interference

### Time Slicing

Multiple workloads share one GPU over time.

Advantages:
- Better utilization

Disadvantages:
- Performance interference
- Variable latency

### MIG

Multi-Instance GPU.

Partitions a GPU into several smaller, isolated GPU instances.

```text
GPU
├─ MIG A
├─ MIG B
└─ MIG C
```

### MPS

Multi-Process Service.

Multiple CUDA processes share one GPU efficiently.

### A guide to choosing

```text
Large production LLM
→ Dedicated

Several small experiments
→ Time Slicing

Strong partitioning / isolation
→ MIG

Multiple CUDA processes
→ MPS
```

---

## 9.6 Multi-GPU

Key points:

```text
PCIe
NVLink
NCCL
Inter-GPU Communication
```

### Why communication is needed

In tensor parallelism, GPUs repeatedly exchange computation results for the same layer.

### PCIe

A general-purpose system interconnect.

### NVLink

A high-speed GPU ↔ GPU interconnect.

This matters for workloads such as TP.

### NCCL

NVIDIA Collective Communications Library.

A library for communication between GPUs.

### TP and communication

```text
GPU computation
↓
Exchange results with other GPUs
↓
Next layer
```

Slow communication makes GPUs wait for each other and slows down inference overall.

Place TP GPUs on the same node where possible.

---

## 9.7 Multi-Node Inference

> Run one model across multiple GPU servers

### Layout

```text
Server A GPUs
↕
Network
↕
Server B GPUs
```

### Differences from single-node inference

Same node:
- High-speed interconnects such as NVLink

Different nodes:
- Traffic crosses the network

### RDMA

Remote Direct Memory Access.

A technology that speeds up memory data transfers between servers by reducing CPU involvement.

### InfiniBand

A high-speed, low-latency network for AI/HPC.

### NCCL Multi-Node

NCCL is also used for GPU communication across servers.

### Principle

```text
Single-node where possible
↓
Multi-node when the model does not fit on one node
```

---

## 9.8 GPU Capacity Planning

Question:

> How many GPUs are needed to serve a given model at a given context length and number of concurrent users?

Key points:

```text
Model Weight
KV Cache
Concurrency
Compute Capacity
Replica count
```

### 1. Calculate model weights

```text
Weight Memory
≈ Parameter count × Precision
```

### 2. Calculate remaining VRAM

```text
GPU VRAM
- Model Weight
- Runtime/Activation
=
Available KV cache capacity
```

### 3. KV Cache

```text
KV Cache
≈ KV per token
× active context tokens
× concurrent sequences
```

### 4. Compute

Fitting in memory is not enough.

```text
Concurrency ↑
↓
GPU utilization ↑
↓
Queue ↑
↓
TTFT / TPOT worsen
```

### 5. Benchmark

Example:

```text
Concurrency 1
5
10
20
```

At each level, measure:

```text
TTFT
TPOT
Throughput
GPU Utilization
GPU Memory
KV Cache Utilization
Queue
```

Measure these metrics.

### 6. Replica count

Example:

```text
1 replica
→ Meets the SLA up to concurrency 8

Peak concurrency = 24
→ Start by considering at least about 3 replicas
```

Add spare capacity for failures.

### Basic sequence

```text
1. Model Size
2. Precision
3. Minimum GPU count
4. Remaining VRAM
5. KV Cache Capacity
6. Context / Concurrency
7. Benchmark
8. Replica count
9. HA Spare Capacity
```

### Values to check in the current B300 / GLM environment

```text
GPUs per replica
Actual weight size
KV Cache dtype
Average / P95 context
Peak concurrency
KV cache utilization per replica
TTFT / TPOT
```

---

## 9.9 GPU Failure / Operations

Key points:

```text
GPU OOM
GPU Unhealthy
Driver / CUDA issues
GPU node failure
Recovery / replacement
```

### GPU OOM

```text
Model Weight
+ KV Cache
+ Activation
+ Runtime
>
VRAM
```

→ CUDA Out of Memory.

Common causes:

```text
Context too long
Too many concurrent requests
Large model
Aggressive gpu_memory_utilization
```

Possible remedies:

```text
Reduce concurrency
Limit context
Adjust KV dtype
Quantization
Add GPUs
Increase TP
```

### Distinguish this from Kubernetes OOMKilled

```text
Insufficient container RAM
→ OOMKilled

Insufficient GPU VRAM
→ CUDA OOM
```

### GPU Unhealthy

One GPU fails with TP=4:

```text
GPU0 ✅
GPU1 ✅
GPU2 ❌
GPU3 ✅

→ The entire replica may fail
```

### Driver / CUDA Stack

Layers to investigate:

```text
vLLM
↓
CUDA Runtime
↓
Container Toolkit
↓
NVIDIA Driver
↓
GPU
```

### GPU node failure

Rescheduling requires enough GPUs on another node.

Example:

```text
The replica needs 4 GPUs
Another node has 2 GPUs free
→ Pod Pending
```

### Spare Capacity

Using 100% of the GPUs can make recovery difficult.

```text
16 GPUs in total
16 currently in use
→ Cannot reschedule after a node failure
```

With spare capacity:

```text
16 in total
12 in use
4 spare

→ A 4-GPU replica can be recreated
```

Spare GPUs can therefore provide HA capacity instead of being wasted.

### Node replacement

```text
Cordon
↓
Drain
↓
Inspect / replace
↓
Verify health
↓
Rejoin the cluster
```

### Operational metrics

```text
GPU Utilization
VRAM Usage
Temperature
GPU Error
Pod Restart
CUDA Error
vLLM Queue
TTFT / TPOT
```

### Memory vs compute bottlenecks

```text
Low GPU utilization
VRAM almost full
CUDA OOM
→ Memory capacity problem

Spare VRAM
GPU Util 100%
Queue grows
→ Compute capacity problem
```

**spare capacity and recovery**

A total of 4 spare GPUs out of 16 does not guarantee recovery after a node failure. If 12 GPUs are in use across the source's two 8-GPU nodes, losing one node leaves only 8 GPUs in total. The original 12-GPU serving capacity cannot be fully restored. Recreating a single 4-GPU replica requires a feasible 4-GPU placement on one suitable surviving node. Also check CPU/RAM, affinity, taints, device health, and model readiness time.

The cordon/drain sequence outlines planned maintenance. Actual drain requires review of allowed disruption, PodDisruptionBudgets, and replacement capacity. No GPU commands, drain, or load tests were run for this page. 

---

<!-- SOURCE CORE END -->

## Related topics

- [Platform infrastructure study map](index.md)

## Key points

GPU operations require attention to memory, model loading, node health, and recovery capacity as well as allocated devices.

## LLM in Practice

**Prompt:**

=== "한국어"

    ```text {.prompt}
    GPU Node 정비 전에 replica를 다른 Node로 옮길 수 있는지 계산해 줘. Node별 실제 배치와 모델의 GPU 묶음 요구를 사용하고, canary·정비·장애 예비 용량을 중복 계산하지 마. Node 작업은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Before GPU node maintenance, calculate whether replicas can move to other nodes. Use actual placement and each model’s grouped GPU requirement; do not double-count canary, maintenance, or failure reserve. Do not operate nodes.
    ```

**Key point:** Surviving replicas, replacement capacity, and minimum-serving-capacity status for each node failure, plus expansion or placement proposals. It may treat total spare GPUs as capacity on one node or infer a compute bottleneck from 100% GPU utilization. Recalculate GPUs, CPU/RAM, affinity, taints, and surviving-replica use on each eligible node, not just total GPUs. Recovery time must include model preparation and readiness. Related: [Kubernetes operations](kubernetes-operations.md)
