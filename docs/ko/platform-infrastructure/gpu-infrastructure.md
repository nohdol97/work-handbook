---
id: platform-infrastructure-gpu-infrastructure
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
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

제공된 학습 원문의 번호·순서·예시를 보존했다. 아래 수치·환경 설명은 원문 기록이며 이 문서가 실제 운영 환경이나 실측 성능을 검증했다는 뜻은 아니다. 모델·GPU 사양, 메모리 계산의 조건과 운영상 정정은 뒤의 보완 절에서 해당 절 번호와 함께 확인한다. 코드·명령은 실행하지 않았다.

특히 GPU Util 100%만으로 compute 병목을 확정할 수 없고 spare GPU 합계만으로 Node 장애 복구를 보장할 수 없다는 정정을 보완에서 확인한다.

<!-- SOURCE CORE START -->

## 9.1 GPU Fundamentals

GPU는 대규모 병렬 연산을 빠르게 처리하는 가속기다.

핵심:

```text
CPU vs GPU
CUDA
VRAM
GPU Compute
```

### CPU vs GPU

CPU:
- 범용 로직
- OS
- Application
- DB

GPU:
- Matrix multiplication
- Tensor 연산
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

GPU 전용 Memory.

LLM Serving에서:

```text
Model Weights
KV Cache
Activation
Runtime
```

사용.

### VRAM vs Compute

```text
VRAM
= 얼마나 담을 수 있는가

GPU Compute
= 얼마나 빠르게 계산하는가
```

예:

```text
VRAM 95%
GPU Util 20%
→ Memory 많이 차지, Compute 여유

VRAM 60%
GPU Util 100%
→ Compute 병목
```

---

## 9.2 NVIDIA Container Stack

핵심 구조:

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

Host OS가 GPU를 제어.

대표 확인 명령:

```bash
nvidia-smi
```

### CUDA Runtime

Container 안에서 vLLM/PyTorch가 GPU 연산을 사용하는 실행 환경.

### NVIDIA Container Toolkit

Host GPU를 Container에서 사용할 수 있게 연결.

### Driver는 Host에

```text
Host
└─ NVIDIA Driver

Container
└─ CUDA Runtime
```

### Version Compatibility

Container CUDA Runtime과 Host NVIDIA Driver의 호환성이 중요하다.

---

## 9.3 Kubernetes GPU

핵심:

```text
Device Plugin
GPU Resource Request
GPU Scheduling
```

### NVIDIA Device Plugin

Kubernetes에 Node의 GPU Resource를 등록.

예:

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

GPU 여유가 있는 Node를 Scheduler가 선택.

### 기본 GPU 할당

보통 정수 단위:

```text
1 GPU
2 GPU
4 GPU
```

0.5 GPU 같은 공유는 별도 기술 필요.

### GPU 부족

```text
GPU Capacity 없음
↓
Pod Pending
```

### Device Plugin vs Container Toolkit

```text
Device Plugin
→ Kubernetes가 GPU를 스케줄링 가능하게 함

Container Toolkit
→ Container가 실제 GPU를 사용하게 함
```

---

## 9.4 GPU Node Pool

> GPU Node를 일반 Node와 별도 그룹으로 관리

### 구조

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

일반 Pod가 GPU Node에 못 들어오게 제한.

### Toleration

GPU workload가 해당 Node에 들어갈 수 있게 허용.

### Affinity + Toleration

```text
Affinity
→ 어디로 갈지 선택

Toleration
→ 그 Node에 들어갈 수 있게 허용
```

---

## 9.5 GPU Sharing

핵심:

```text
Dedicated GPU
Time Slicing
MIG
MPS
```

### Dedicated GPU

GPU 한 장을 한 workload가 전용 사용.

장점:
- 성능 예측 쉬움
- 간섭 적음

### Time Slicing

시간을 나눠 여러 workload가 같은 GPU를 사용.

장점:
- utilization 향상

단점:
- 성능 간섭
- latency 변동

### MIG

Multi-Instance GPU.

GPU를 여러 격리된 작은 GPU Instance로 분할.

```text
GPU
├─ MIG A
├─ MIG B
└─ MIG C
```

### MPS

Multi-Process Service.

여러 CUDA Process가 하나의 GPU를 효율적으로 공유.

### 선택 감각

```text
대형 Production LLM
→ Dedicated

작은 실험 여러 개
→ Time Slicing

강한 분할/격리
→ MIG

여러 CUDA Process
→ MPS
```

---

## 9.6 Multi-GPU

핵심:

```text
PCIe
NVLink
NCCL
Inter-GPU Communication
```

### 왜 통신하나

Tensor Parallel에서는 GPU끼리 같은 Layer 계산 결과를 계속 교환.

### PCIe

범용 시스템 연결.

### NVLink

GPU ↔ GPU 고속 연결.

TP 같은 workload에서 중요.

### NCCL

NVIDIA Collective Communications Library.

GPU 간 통신 Library.

### TP와 통신

```text
GPU 계산
↓
다른 GPU와 결과 교환
↓
다음 Layer
```

통신이 느리면 GPU가 서로를 기다려 전체 inference가 느려진다.

가능하면 TP GPU들을 같은 Node에 배치하는 것이 좋다.

---

## 9.7 Multi-Node Inference

> 하나의 모델을 여러 GPU 서버에 걸쳐 실행

### 구조

```text
Server A GPUs
↕
Network
↕
Server B GPUs
```

### Single-Node와 차이

같은 Node:
- NVLink 등 고속 interconnect

다른 Node:
- Network를 거침

### RDMA

Remote Direct Memory Access.

CPU 개입을 줄여 서버 간 Memory 데이터 전송을 빠르게 하는 기술.

### InfiniBand

AI/HPC용 고속 저지연 Network.

### NCCL Multi-Node

NCCL은 여러 서버 GPU 간 통신에도 사용.

### 원칙

```text
가능하면 Single-Node
↓
한 Node에 안 들어갈 때 Multi-Node
```

---

## 9.8 GPU Capacity Planning

질문:

> 어떤 모델을, 어느 Context와 동시 사용자로 서비스하려면 GPU가 몇 장 필요한가?

핵심:

```text
Model Weight
KV Cache
Concurrency
Compute Capacity
Replica 수
```

### 1. Model Weight 계산

```text
Weight Memory
≈ Parameter 수 × Precision
```

### 2. 남는 VRAM 계산

```text
GPU VRAM
- Model Weight
- Runtime/Activation
=
KV Cache 여유
```

### 3. KV Cache

```text
KV Cache
≈ token당 KV
× active context tokens
× concurrent sequences
```

### 4. Compute

Memory에 들어간다고 충분한 건 아니다.

```text
Concurrency ↑
↓
GPU utilization ↑
↓
Queue ↑
↓
TTFT / TPOT 악화
```

### 5. Benchmark

예:

```text
Concurrency 1
5
10
20
```

각 구간에서:

```text
TTFT
TPOT
Throughput
GPU Utilization
GPU Memory
KV Cache Utilization
Queue
```

을 측정.

### 6. Replica 수

예:

```text
Replica 1개
→ concurrent 8까지 SLA 만족

Peak concurrency = 24
→ 최소 3 replicas 정도부터 검토
```

여기에 장애 여유를 추가.

### 기본 순서

```text
1. Model Size
2. Precision
3. 최소 GPU 수
4. 남는 VRAM
5. KV Cache Capacity
6. Context / Concurrency
7. Benchmark
8. Replica 수
9. HA Spare Capacity
```

### 현재 B300 / GLM 환경에서 확인할 값

```text
Replica당 GPU 수
실제 Weight 크기
KV Cache dtype
평균 / P95 Context
Peak concurrency
Replica별 KV Cache utilization
TTFT / TPOT
```

---

## 9.9 GPU Failure / Operations

핵심:

```text
GPU OOM
GPU Unhealthy
Driver / CUDA 문제
GPU Node 장애
복구 / 교체
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

대표 원인:

```text
Context 너무 김
동시 요청 많음
Model 큼
gpu_memory_utilization 공격적
```

해결 방향:

```text
Concurrency 감소
Context 제한
KV dtype 조정
Quantization
GPU 추가
TP 증가
```

### Kubernetes OOMKilled와 구분

```text
Container RAM 부족
→ OOMKilled

GPU VRAM 부족
→ CUDA OOM
```

### GPU Unhealthy

TP=4에서 GPU 하나 장애:

```text
GPU0 ✅
GPU1 ✅
GPU2 ❌
GPU3 ✅

→ Replica 전체 장애 가능
```

### Driver / CUDA Stack

문제 계층:

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

### GPU Node 장애

다른 Node에 충분한 GPU가 있어야 재배치 가능.

예:

```text
Replica가 GPU 4개 필요
다른 Node 여유 2개
→ Pod Pending
```

### Spare Capacity

GPU를 100% 모두 쓰면 장애 복구가 어려울 수 있다.

```text
총 16 GPUs
현재 16 사용
→ Node 장애 시 재배치 불가
```

여유가 있으면:

```text
총 16
12 사용
4 spare

→ 4-GPU Replica 재생성 가능
```

즉 여유 GPU는 낭비가 아니라 HA Capacity일 수 있다.

### Node 교체

```text
Cordon
↓
Drain
↓
점검 / 교체
↓
정상 확인
↓
Cluster 재참여
```

### 운영 Metric

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

### Memory vs Compute 병목

```text
GPU Util 낮음
VRAM 거의 꽉 참
CUDA OOM
→ Memory Capacity 문제

VRAM 여유
GPU Util 100%
Queue 증가
→ Compute Capacity 문제
```

---

<!-- SOURCE CORE END -->

## 보완 — 원문 해석과 운영 조건

검토일: 2026-10-01. 원문 예시는 운영 환경을 확인한 결과가 아니다.

### 9.1 / 9.8 / 9.9 사용률과 용량

**`GPU Util 100% → Compute 병목`은 단정할 수 없다.** [NVIDIA nvidia-smi 문서](https://docs.nvidia.com/deploy/nvidia-smi/index.html)의 GPU utilization은 표본 구간에 kernel이 실행된 시간 비율이다. 연산기의 최대 처리량을 얼마나 썼는지를 직접 뜻하지 않는다. Memory bandwidth, 통신, kernel 효율, clock 제한, CPU 공급 지연을 함께 확인한다. 낮은 사용률도 무조건 여유 compute를 뜻하지 않는다.

9.8의 8 concurrent/replica와 peak 24로 3개를 구하는 것은 선형 확장 가정이다. 실제 request 길이 분포, 큐, 라우팅 편향, 장애 중 SLO를 부하 시험으로 확인한다. GLM/B300 수치와 단위별 계산 조건은 [vLLM 보완](vllm.md)의 7.2 및 무번호 계산 절에 있다.

### 9.3–9.5 GPU 요청·배치·공유

[Kubernetes GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)에서 GPU `limits`만 지정하면 request도 그 값이 되고, 둘 다 있으면 동일해야 한다. Node 전체 여유 합계가 아니라 해당 Pod가 배치될 한 Node의 자원과 제약을 본다. 9.4의 toleration은 taint를 허용할 뿐 특정 Node로 배치를 보장하지 않으며, taint 효과와 required/preferred affinity도 구분한다.

[NVIDIA GPU sharing 문서](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/gpu-sharing.html)에 따르면 time slicing은 replica 사이 memory/fault isolation을 제공하지 않고 request 수에 비례한 compute도 보장하지 않는다. MIG는 지원되는 GPU와 profile에 한해 분할한다. Dedicated/time slicing/MIG/MPS는 원문의 선택 감각만으로 서로 대체할 수 없다.

### 9.9 장애 여유와 복구

16장 중 4장이 spare라는 합계만으로 Node 장애 후 복구를 보장하지 않는다. 원문의 8장짜리 Node 두 개에서 12장을 사용한다면 Node 하나가 사라진 뒤 남는 전체 GPU는 8장이다. 12장의 기존 serving 용량을 모두 복구할 수 없다. 살아 있는 적합한 Node 하나에 4-GPU 배치가 가능해야 단일 4-GPU replica를 재생성한다. CPU/RAM·affinity·taint·장치 health·모델 준비 시간까지 확인한다.

Cordon/drain 순서는 계획된 정비의 개요다. 실제 drain은 중단 허용 범위·PodDisruptionBudget·대체 capacity를 검토한 뒤 실행한다. 이 페이지에서는 GPU 명령, drain, 부하 시험을 실행하지 않았다. 읽기 순서: 9.1–9.3의 계층을 구분한 뒤 9.4–9.7에서 배치·공유·통신을 확인하고 9.8–9.9에서 용량·장애 가정을 검증한다.

## LLM in Practice

### 상황

가상 8-GPU Node 두 개에서 4-GPU replica 세 개를 운영한다. spare 4장이 Node 장애를 견디는지 [Kubernetes 운영](kubernetes-operations.md)과 함께 검토한다. 실제 장애 기록이 아니다.

### LLM에 제공할 맥락

Node별 replica 배치, allocatable·allocated GPU, affinity·taint, device health, CPU/RAM, startup 시간, 장애 시 필요한 최소 serving 용량을 익명화해 제공한다.

### 예시 프롬프트

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 GPU 장애 복구안을 검토하라.
    관측: Node A/B 각각 8 GPU, replica 세 개가 각각 4 GPU를 요청한다.
    가정: 12 GPU 사용과 spare 4 GPU만 알려져 있고 실제 배치는 미확인이다.
    제약: 운영 drain·재시작·장애 주입은 실행하지 않는다.
    [요청]
    관측 사실 / 가정 / 누락 증거를 먼저 구분하라.
    A 장애와 B 장애 각각에서 남는 총 GPU와 기존 replica 사용량을 나눠 계산하라.
    전체 12 GPU serving 복구와 4 GPU replica 하나 복구를 구분하라.
    필요한 affinity·taint·device health·CPU/RAM·readiness 증거를 열거하라.
    [출력]
    출력: 장애 경우 / 가용 capacity / 불가능 조건 / 다음 읽기 전용 확인 표.
    [검증]
    실제 배치와 scheduler 이벤트로 반증할 가설 및 격리 시험 계획을 제안하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Review a hypothetical GPU recovery plan.
    Observations: nodes A/B each have 8 GPUs; three replicas request 4 GPUs each.
    Assumptions: only 12 used GPUs and 4 spare GPUs are known; actual placement is unknown.
    Constraint: do not run production drain, restarts, or fault injection.
    [Task]
    Separate observations, assumptions, and missing evidence first.
    For failure of A and failure of B, separate total surviving GPUs from GPUs used by existing replicas.
    Distinguish restoring all 12 serving GPUs from restoring one 4-GPU replica.
    List required affinity, taint, device-health, CPU/RAM, and readiness evidence.
    [Output]
    Output a table: failure case / available capacity / impossible conditions / next read-only check.
    [Checks]
    Propose falsifiable hypotheses using placement and scheduler events, plus an isolated test plan.
    ```

### 기대 출력

Node별 장애 경우와 살아남은 capacity, 복구 가능한 replica, 부족 증거, 확인 순서를 담은 표.

### LLM이 틀릴 수 있는 점

전체 spare 합계를 단일 Node의 여유로 오해하거나 살아남은 replica가 쓰는 GPU를 이중 계산하고, GPU Util만으로 compute 병목을 확정할 수 있다.

### 검증 방법

스케줄러 이벤트·Node 상태·실제 자원 배치를 대조하고 계획된 격리 환경에서 장애 시나리오와 readiness 시간을 시험한다. LLM 결과는 검증 전 가설이며 운영 drain이나 장애 주입은 실행하지 않았다.

## 관련 문서

- [플랫폼 인프라 학습 지도](index.md)
