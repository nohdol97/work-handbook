---
id: platform-infrastructure-vllm
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
knowledge_ids:
  - PIS2-07-01
  - PIS2-07-02
  - PIS2-07-03
  - PIS2-07-04
  - PIS2-07-05
  - PIS2-07-06
  - PIS2-07-07
  - PIS2-07-08
  - PIS2-07-09
  - PIS2-07-10
  - PIS2-07-A1
  - PIS2-07-A2
  - PIS2-07-A3
  - PIS2-07-A4
---

# Chapter 7. vLLM

제공된 학습 원문의 번호·순서·예시를 보존했다. 아래 수치·환경 설명은 원문 기록이며 이 문서가 실제 운영 환경이나 실측 성능을 검증했다는 뜻은 아니다. 모델·GPU 사양, 메모리 계산의 조건과 운영상 정정은 뒤의 보완 절에서 해당 절 번호와 함께 확인한다. 코드·명령은 실행하지 않았다.

특히 744B/40B·FP4 Weight 크기의 모델별 차이와 1M token의 단위 조건을 보완에서 확인한다.

<!-- SOURCE CORE START -->

## 7.1 LLM Serving Fundamentals

vLLM은 LLM Inference Server다.

### Model Serving

```text
LLM Model
↓
GPU Memory Load
↓
Inference Server
↓
사용자 요청
```

### Training vs Inference

```text
Training
→ 모델 학습

Inference
→ 학습된 모델로 답변 생성
```

### Token

LLM이 처리하는 기본 단위.

```text
Input Tokens
Output Tokens
```

### Prefill

입력 Prompt 전체를 처리하는 단계.

### Decode

출력 Token을 반복적으로 하나씩 생성하는 단계.

전체 흐름:

```text
Request
↓
Prompt Tokens
↓
Prefill
↓
Decode
↓
Output Tokens
↓
Response
```

---

## 7.2 GPU Memory

핵심:

```text
Model Weights
KV Cache
Activation
Runtime Memory
```

### Model Weights

학습된 모델의 parameter.

### Precision

```text
FP32 → 4 bytes
FP16/BF16 → 2 bytes
INT8/FP8 → 약 1 byte
```

### KV Cache

이전 Token 계산 결과를 저장해 Decode 시 재사용.

```text
Prompt / 생성 Token
↓
KV Cache
↓
다음 Token 생성에 재사용
```

### KV Cache 증가 요인

```text
동시 Request ↑
Context Length ↑
→ KV Cache ↑
```

### Activation

현재 연산 중 필요한 임시 데이터.

### VRAM 구조

```text
GPU VRAM
├─ Model Weights
├─ KV Cache
├─ Activation
└─ Runtime
```

---

## GLM-5.3 / B200 / B300 실무 계산

### B200에서 GLM-5.3 FP32를 가정했을 때

GLM-5.3 계열은 약 744B total parameters / 40B active parameters인 MoE 모델로 봤다.

FP32 Weight 단순 계산:

```text
744B × 4 bytes
≈ 2.98TB
```

B200 1장 180GB라면 Weight만 넣어도 최소 17장 이상 필요.

실제 Serving에는:

```text
Weight
KV Cache
Activation
Runtime
Communication buffer
```

가 추가로 필요하므로 더 많은 GPU가 필요하다.

### MoE 특징

```text
Total parameters ≈ 744B
Active parameters ≈ 40B
```

Compute는 일부 Expert만 활성화되지만 Memory에는 전체 Expert Weight가 필요하다.

### Precision별 단순 Weight Memory

```text
FP32 ≈ 2.98TB
BF16 ≈ 1.49TB
FP8  ≈ 744GB
FP4  ≈ 372GB
```

실제는 scale / metadata / quantization overhead로 차이가 생길 수 있다.

### 동시 사용자 수는 GPU Memory만으로 결정되지 않음

```text
Concurrency
=
GPU Memory
+
GPU Compute
+
Context Length
+
Output Length
+
목표 tokens/sec
```

Memory에 많은 Sequence가 들어가도 빠르게 처리할 수 있는지는 별도다.

---

## KV Cache와 Context Length

KV Cache는 Context 길이에 거의 선형적으로 증가한다.

```text
KV Cache
≈ 토큰당 KV 크기
× 현재 Context Token 수
× 동시 Sequence 수
```

예:

```text
Input = 8K
Output generated = 2K

Current context ≈ 10K
```

10K에 대한 KV Cache를 유지한다.

### 일반 Transformer 토큰당 KV Cache 공식

```text
KV Cache / token
≈ 2 × Layers × KV Heads × Head Dimension × Bytes
```

`2`는 K + V.

예:

```text
Layers = 80
KV Heads = 8
Head Dim = 128
BF16 = 2 bytes

2 × 80 × 8 × 128 × 2
= 327,680 bytes
≈ 320 KiB / token
```

대략:

```text
1K context   ≈ 320 MiB
8K context   ≈ 2.5 GiB
32K context  ≈ 10 GiB
128K context ≈ 40 GiB
```

### 모델마다 KV Cache 크기 다름

```text
KV Cache
∝
Token 수
× Layer 수
× KV Head 수
× Head Dimension
× KV precision
```

GQA/MQA는 KV Head 수를 줄여 KV Cache를 줄일 수 있다.

### Weight precision과 KV precision은 별개

```text
Model Weight precision
≠
KV Cache precision
```

예:

```text
Weight = BF16
KV Cache = FP8
```

가능.

---

## GLM-5.3의 1M Context와 KV Cache

GLM-5.3은 일반 MHA/GQA보다 MLA 계열의 압축 KV 표현을 사용한다고 보고 계산했다.

이 세션에서 사용한 단순 근사:

```text
(kv_lora_rank 512 + rope dim 64)
× 78 layers
× BF16 2 bytes
≈ 87.8 KiB / token
```

따라서 core MLA cache 단순 근사:

```text
1M context
≈ 약 87.8 GiB / request
```

FP8 KV라면 대략 절반 수준:

```text
1M context
≈ 약 44 GiB / request
```

실제 vLLM에서는 block allocation / padding / indexer cache / runtime overhead 등이 추가될 수 있으므로 실측이 필요하다.

### 30명 개발자 + 1M Context

30명이 동시에 1M Context를 꽉 채운다고 단순 가정:

BF16 KV:

```text
87.8 GiB × 30
≈ 2.57 TiB
```

FP8 KV:

```text
약 44 GiB × 30
≈ 1.3 TiB
```

따라서:

```text
30 Developers
+
Coding Agent
+
1M Context
```

환경이라면 매우 큰 KV Cache HBM이 합리적일 수 있다.

중요:

```text
1M Context 지원
≠
항상 1M 사용
```

실제 봐야 할 값:

```text
평균 active context
P95 context
Peak concurrent sequences
kv_cache_dtype
KV cache utilization
```

---

## B300 2대 / GLM-5.3 FP4 3개 관련 실무 연결

사용자 설명:
- 서버 1대당 GPU 8장
- B300 서버 2대
- 총 GPU 16장
- GLM-5.3 FP4 모델 3개 Serving
- 일부 공간은 KV Cache / 학습 용도 여유

가능한 예시 구조:

```text
B300 Server #1
GPU 0~3 → GLM Replica A
GPU 4~7 → GLM Replica B

B300 Server #2
GPU 0~3 → GLM Replica C
GPU 4~7 → Training / Spare Capacity
```

이는 실제 `tensor_parallel_size`를 확인해야 확정 가능.

### B300 Memory

B300 1장 약 288GB HBM이라고 보면:

```text
1 server = 8 GPUs
≈ 2.3TB HBM

2 servers
≈ 4.6TB HBM
```

### GLM-5.3 FP4 단순 Weight

```text
744B × 0.5 byte
≈ 372GB
```

실제 quantization overhead 포함 시 더 커질 수 있다.

### Replica 하나가 B300 4장이라면

```text
4 × 288GB
≈ 1.15TB HBM
```

대략:

```text
Weight ≈ 400GB 전후+
KV Cache = 상당한 나머지
Activation
Runtime
Communication buffers
```

### 남은 VRAM과 Training

같은 GPU에서 vLLM Serving과 Training을 동시에 하는 것은:

```text
VRAM
GPU Compute
Memory Bandwidth
```

를 경쟁하므로 운영이 까다롭다.

더 깔끔한 구조:

```text
Serving 전용 GPU
+
Training / Experiment 전용 GPU
```

### 30명만 보면 과해 보일 수 있지만

일반 Chat + 짧은 Context라면 과할 수 있다.

하지만:

```text
30 Developers
+
1M Context
+
Coding Agent workload
```

면 완전히 다른 Capacity 요구가 된다.

---

## 7.3 PagedAttention

PagedAttention:

> KV Cache를 큰 연속 공간으로 잡지 않고 작은 Block/Page 단위로 관리

### 기존 문제

요청마다 앞으로 얼마나 길어질지 모르므로 큰 연속 공간을 미리 잡으면 낭비 발생.

### Block 기반

```text
GPU KV Cache
[Block][Block][Block][Block]...
```

Request마다 필요한 Block만 할당.

### 효과

```text
Memory waste ↓
Fragmentation ↓
Concurrent sequences ↑
Throughput ↑
```

### 주의

PagedAttention은:
- Weight를 줄이지 않음
- Token 수를 줄이지 않음
- KV Cache 배치를 효율화함

---

## 7.4 Continuous Batching

> 여러 요청을 묶어 처리하되, 끝난 요청 자리에 새 요청을 계속 넣는 방식

### Static Batching 문제

```text
A 20 tokens
B 500 tokens
C 100 tokens
```

A/C가 빨리 끝나도 B 때문에 자리가 비효율적으로 남을 수 있다.

### Continuous Batching

```text
A 종료 → D 투입
C 종료 → E 투입
```

### 효과

```text
GPU utilization ↑
Throughput ↑
```

PagedAttention과 결합:

```text
새 Request
↓
KV Block 할당
↓
Batch 참여
↓
완료
↓
KV Block 반환
↓
새 Request 투입
```

Concurrency를 너무 높이면 Queue/TTFT/TPOT이 악화될 수 있다.

---

## 7.5 Performance Metrics

핵심:

```text
TTFT
TPOT
Tokens/sec
Throughput
Queue Time
```

### TTFT

Time To First Token.

```text
Request
↓
Queue
↓
Prefill
↓
첫 Token
```

### TPOT

Time Per Output Token.

예:

```text
TPOT = 50ms
→ 약 20 tok/s
```

### Throughput

서버 전체 처리량.

```text
output tokens/sec
requests/sec
```

### Queue Time

GPU 처리 전에 기다리는 시간.

### 관계

```text
Request
↓
Queue Time
↓
Prefill
↓
첫 Token ← TTFT
↓
Decode
↓
Token ... ← TPOT / tok/s
```

Concurrency 증가 시 Throughput은 올라갈 수 있지만 어느 시점부터 Queue와 Latency가 급격히 악화된다.

---

## 7.6 Parallelism

핵심:

```text
Tensor Parallelism
Pipeline Parallelism
Data Parallelism
```

### Tensor Parallelism

하나의 Layer 연산을 여러 GPU가 나눠 처리.

```text
GPU 0 ─┐
GPU 1 ─┼→ 같은 Layer
GPU 2 ─┤
GPU 3 ─┘
```

모델이 GPU 한 장에 안 들어갈 때 중요.

### Pipeline Parallelism

Layer 구간을 GPU별로 분할.

```text
GPU0 → Layer 1~20
GPU1 → Layer 21~40
GPU2 → Layer 41~60
GPU3 → Layer 61~80
```

### Data Parallelism

모델 전체 Replica를 여러 개 운영해 요청 분산.

### 조합

```text
GPU 0~3 → Replica A, TP=4
GPU 4~7 → Replica B, TP=4
```

핵심:

```text
모델이 너무 크다
→ TP / PP

사용자가 너무 많다
→ DP / Replica 증가
```

---

## 7.7 Quantization

> 모델 Weight precision을 낮춰 VRAM 사용량과 연산 비용을 줄이는 기술

### Precision

```text
FP32 ≈ 4 bytes
FP16/BF16 ≈ 2 bytes
INT8/FP8 ≈ 1 byte
4-bit/FP4 ≈ 0.5 byte
```

### 효과

```text
Weight VRAM ↓
필요 GPU 수 ↓
비용 ↓
남는 VRAM ↑
KV Cache Capacity ↑
```

### Trade-off

```text
Precision ↓
→ 모델 품질 저하 가능
```

### AWQ / GPTQ

대표적인 low-bit Weight Quantization 방식.

### Weight Quantization과 KV Cache는 별개

```text
Weight = FP8
KV Cache = BF16
```

가능.

---

## 7.8 vLLM API Server

vLLM은 OpenAI-compatible API Server 형태로 Serving 가능.

```text
Client
↓
POST /v1/chat/completions
↓
vLLM
↓
Model
↓
GPU
```

주요 서버 설정:

```text
Model
GPU 수
Tensor Parallel
Max Context
GPU Memory Utilization
Quantization
```

주요 요청 설정:

```text
max_tokens
temperature
top_p
```

---

## 7.9 vLLM on Kubernetes

핵심:

```text
GPU Request
GPU Node Scheduling
Replica
Readiness
Autoscaling
```

### GPU Resource Request

```yaml
resources:
  limits:
    nvidia.com/gpu: 1
```

### GPU Node 배치

```text
Node Label
Node Affinity
Taint
Toleration
```

### Multi-GPU Pod

```text
Tensor Parallel = 4
GPU Request = 4
```

보통 같은 Node의 GPU 4장을 쓰는 게 유리하다.

### Startup / Readiness

```text
Pod Running
≠
Model Ready
```

```text
Container
↓
Model Load
↓
VRAM 할당
↓
KV Cache 준비
↓
Ready
```

### Autoscaling

일반 API보다 Scale-out 시간이 길 수 있다.

```text
Pod 생성
↓
Image Pull
↓
Model Load
↓
GPU Memory Load
↓
Readiness
```

Queue / TTFT / GPU Utilization 등의 지표를 함께 봐야 한다.

GPU가 없으면 Pod Pending.

---

## 7.10 Production Serving

핵심:

```text
Model Startup
Failure Recovery
Scaling
Rolling Update
```

### Failure Recovery

```text
vLLM Pod 장애
↓
Kubernetes 재시작
↓
Model Reload
↓
Readiness
```

Replica 하나뿐이면 Reload 동안 서비스 영향 가능.

### Scaling

```text
Request 증가
↓
Queue / TTFT 악화
↓
vLLM Replica 증가
↓
GPU Capacity 필요
```

### Rolling Update

```text
새 Replica 준비
↓
Readiness 성공
↓
기존 Replica 제거
```

### Production Metrics

```text
GPU Utilization
GPU Memory
Queue Length
TTFT
TPOT
Throughput
Error Rate
Pod Restart Count
```

### Graceful Shutdown

```text
새 요청 차단
↓
기존 요청 마무리
↓
Pod 종료
```

---

<!-- SOURCE CORE END -->

## 보완 — 원문 계산과 적용 조건

검토일: 2026-10-01. 원문은 학습 기록이며 아래는 별도 기술 검토다.

### 7.2 및 네 개의 무번호 계산 절

- **「GLM-5.3 / B200 / B300 실무 계산」:** 744B/40B는 [GLM-5 공식 모델 카드](https://huggingface.co/zai-org/GLM-5)의 수치다. [vLLM GLM-5.3 레시피](https://recipes.vllm.ai/zai-org/GLM-5.3)는 약 743B/39B로 표기한다. 원문의 744B 가정 계산은 유지하되 GLM-5.3의 확정 parameter 수로 읽지 않는다. 같은 레시피는 기본 checkpoint를 FP8, 별도 Inferact NVFP4 checkpoint를 약 465GB로 설명한다. 따라서 372GB와 400GB 전후는 실제 checkpoint 크기를 검증한 값이 아니다.
- **같은 절 및 「B300 2대 / GLM-5.3 FP4 3개 관련 실무 연결」:** [NVIDIA HGX 사양](https://docs.nvidia.com/enterprise-reference-architectures/hgx-ai-factory/latest/components.html)은 B200 SXM 180GB, B300 SXM 288GB와 8 GPU 구성을 명시한다. `744×4/180`의 올림인 17은 Weight만의 산술 하한이다. 지원되는 TP/PP 배치나 실행 가능한 서버 수가 아니다. GB/TB와 GiB/TiB를 섞지 않고 GPU별 가용량·통신 buffer·가중치 분할을 확인한다. 2대/3 replica/TP=4는 확인되지 않은 예시 배치다.
- **「KV Cache와 Context Length」:** 320KiB/token 계산은 제시한 dense-attention 차원 가정에 맞는다. 1K=1,024, 128K=131,072 token일 때 표의 MiB/GiB가 성립한다. Prefix 공유·sliding window·압축 방식에 따라 실제 메모리는 달라진다. MoE의 전체 Weight 필요 설명은 전체 모델을 GPU에 상주시킬 때의 가정이며 offload나 expert 배치에 따라 GPU별 양은 달라진다.
- **「GLM-5.3의 1M Context와 KV Cache」:** [공식 GLM-5.3 config](https://huggingface.co/zai-org/GLM-5.3/blob/main/config.json)는 `kv_lora_rank=512`, `qk_rope_head_dim=64`, `num_hidden_layers=78`, `max_position_embeddings=1048576`을 명시한다. 제시한 계산은 `89,856 bytes/token = 87.75 KiB/token`이다. 1M=1,048,576 token이면 87.75GiB, 1,000,000 token이면 약 83.685GiB다. 30배인 약 2.57TiB는 전자의 BF16 core cache 가정이다. Indexer/MTP/블록 overhead·복제와 실제 backend의 저장 형식은 제외되어 있으므로 전체 serving 용량이나 30명 SLA 보장이 아니다.

### 7.5 / 7.7–7.10 운영 조건

50ms의 역수인 20tok/s는 token 간 간격의 근사이며 첫 token 대기와 서버 전체 throughput을 포함하지 않는다. [vLLM KV cache 문서](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)처럼 FP8 KV는 별도 설정이고 scale calibration 및 attention backend 조건을 확인해야 한다. 메모리 절감만으로 정확도나 latency 개선을 보장하지 않는다.

7.9의 `limits`만 있는 GPU 예시는 request에도 같은 값이 적용된다. 둘 다 지정하면 같아야 한다. GPU가 비어 있어도 affinity·taint·CPU/RAM 등 다른 제약을 만족해야 배치된다. [Kubernetes GPU scheduling](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)

읽기 순서: 먼저 7.1–7.2의 prefill/decode와 memory 구분을 읽고, 계산 절은 가정·단위를 적어 다시 계산한다. 이어 7.3–7.10으로 batching, 측정, 배치, 복구를 연결한다. 실제 GPU·모델 실행이나 성능 측정은 하지 않았다.

## LLM in Practice

### 상황

가상 GLM serving 용량 검토에서 372GB Weight와 30명×1M context만으로 GPU 수를 정하려 한다. [GPU 용량 계획](gpu-infrastructure.md)과 함께 누락된 가정을 찾는 연습이다. 실제 측정 결과가 아니다.

### LLM에 제공할 맥락

모델 revision, quantization, KV dtype, GPU별 가용 VRAM, TP/PP/EP, context 분포, concurrency와 TTFT/TPOT 목표를 익명화해 제공한다. 미수집 값은 미확인으로 둔다.

### 예시 프롬프트

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 serving 용량안을 검토하라.
    관측: GPU별 가용량·Weight 크기·KV dtype는 [제공값], 미수집은 미확인이다.
    가정: 30개 동시 sequence, 각 1M context, FP4 Weight라고 제안되었다.
    제약: 실제 revision과 TP/PP/EP를 확인하기 전 배치를 확정하지 않는다.
    [요청]
    1M=1,000,000과 1,048,576 두 경우를 구분하고 GB/GiB를 통일하라.
    관측 사실 / 가정 / 누락 증거를 먼저 분리하라.
    [출력]
    Weight·KV·overhead·GPU별 배치 표와 반증 가능한 병목 가설을 작성하라.
    다음 확인: config·시작 로그·격리 부하 시험 순서와 기대 관측값을 제시하라.
    [검증]
    메모리에 들어간다는 이유로 TTFT/TPOT 목표 충족을 선언하지 마라.
    설정을 변경하지 말고 공식 문서와 실제 측정으로 검증할 계획을 제안하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Review a hypothetical serving capacity proposal.
    Observations: available memory per GPU, weight size, and KV dtype are [provided values]; missing values are unknown.
    Assumptions: 30 concurrent sequences, each with 1M context, and FP4 weights are proposed.
    Constraint: do not finalize placement before checking the revision and TP/PP/EP.
    [Task]
    Separate 1M=1,000,000 from 1,048,576 and use consistent GB/GiB units.
    Separate observations, assumptions, and missing evidence first.
    [Output]
    Create a weight/KV/overhead/per-GPU placement table and falsifiable bottleneck hypotheses.
    Next checks: order config inspection, startup logs, and isolated load tests with expected observations.
    [Checks]
    Do not claim TTFT/TPOT targets are met merely because the model fits in memory.
    Do not change settings; propose verification using official docs and actual measurements.
    ```

### 기대 출력

Weight·core KV·overhead·GPU별 배치 제약을 구분한 용량표와 측정 계획.

### LLM이 틀릴 수 있는 점

744B를 확정 사양으로 간주하거나 FP4가 모든 tensor에 적용된다고 가정하고, 1M 단위를 섞거나 memory 적합성을 SLA 충족으로 오해할 수 있다.

### 검증 방법

공식 checkpoint config와 실제 시작 로그의 가중치·KV 할당을 대조한다. 단위를 재계산하고 격리된 부하 시험으로 TTFT/TPOT과 품질을 확인한다. LLM 결과는 가설이며 이 예시에서는 모델·GPU를 실행하지 않았다.

## 관련 문서

- [플랫폼 인프라 학습 지도](index.md)
