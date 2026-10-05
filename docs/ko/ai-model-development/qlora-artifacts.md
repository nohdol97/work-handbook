---
id: ai-model-development-qlora-artifacts
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-01-01
  - AIMFT-01-02
  - AIMFT-01-03
  - AIMFT-01-04
  - AIMFT-01-05
  - AIMFT-01-06
  - AIMFT-01-07
  - AIMFT-01-08
---

# Chapter 1. QLoRA와 학습 결과물

제공된 학습 원문의 번호·순서·예시를 보존했다. **1.2의 A/B 행렬 차원은 `B × A` 수식과 맞지 않는다.** 원문 뒤 보완에서 정정하며, 1.3의 precision, 1.4의 저장 파일, 1.7–1.8의 serving·merge 조건도 함께 확인한다. 실제 학습·모델 저장·배포를 실행한 기록이 아니다.

<!-- SOURCE CORE START -->

## 1.1 QLoRA 기본 개념

QLoRA는 Base Model 전체 Weight를 직접 학습하는 방식이 아니라,
Base Model을 Quantization한 상태에서 작은 LoRA Adapter만 학습하는 방식이다.

기본 구조:

```text
Base Model
예: Llama / Qwen / Gemma
↓
4-bit Quantization
↓
Frozen Base Model
+
Trainable LoRA Adapter
↓
Fine-Tuning
```

핵심:

```text
Base Model Weight
→ 대부분 고정

LoRA Adapter Weight
→ 학습
```

따라서 QLoRA 학습 결과물은 일반적으로 새로운 Full Model 전체라기보다
**Base Model에 추가해서 사용하는 Adapter**이다.

---

## 1.2 LoRA가 학습하는 것

기존 Weight를 `W`라고 하면 LoRA는 Weight 전체를 수정하는 대신 작은 변화량을 학습한다.

```text
W' = W + ΔW
```

LoRA는 `ΔW`를 작은 두 Matrix로 표현한다.

```text
ΔW = B × A
```

예:

```text
Original Weight
4096 x 4096

LoRA
A: 4096 x 16
B: 16 x 4096
```

따라서 전체 Weight를 다시 학습하는 것보다 학습해야 하는 Parameter 수를 크게 줄일 수 있다.

---

## 1.3 QLoRA에서 Quantization의 의미

QLoRA의 `Q`는 Quantization을 의미한다.

일반 LoRA:

```text
Base Model
FP16 / BF16
+
LoRA Adapter
```

QLoRA:

```text
Base Model
4-bit
+
LoRA Adapter
```

개념적으로:

```text
Model Weight 저장
→ 4-bit

실제 연산
→ BF16 등의 더 높은 Precision 사용 가능
```

목적:

- GPU Memory 사용량 감소
- 큰 모델을 상대적으로 적은 GPU Resource로 Fine-Tuning
- Full Fine-Tuning 대비 학습 비용 감소

---

## 1.4 QLoRA 학습 결과 Artifact

학습 결과는 다음과 같은 파일로 저장할 수 있다.

```text
adapter_model.safetensors
adapter_config.json
tokenizer.json
tokenizer_config.json
training_args.json
metadata.json
```

핵심 Artifact:

```text
adapter_model.safetensors
```

이 파일에 학습된 LoRA Adapter Weight가 저장된다.

---

## 1.5 S3에 Artifact 저장

AI Platform에서는 학습 결과를 Object Storage에 저장할 수 있다.

AWS 예:

```text
s3://model-artifacts/
└─ customer-support-v1/
   ├─ adapter_model.safetensors
   ├─ adapter_config.json
   ├─ tokenizer.json
   ├─ training_args.json
   └─ metadata.json
```

즉:

```text
Training Job
↓
LoRA Adapter 생성
↓
S3 Artifact 저장
↓
Model Registry 등록
↓
Evaluation / Deployment
```

형태로 연결할 수 있다.

---

## 1.6 Base Model과 Adapter 관계

Inference 시에는 Base Model과 Adapter를 함께 사용한다.

```text
Base Model
Qwen / Llama
     +
LoRA Adapter
     ↓
Fine-Tuned Behavior
```

예:

```text
Llama-3.1-8B
+
SQL Adapter
```

또는:

```text
Llama-3.1-8B
+
Customer Support Adapter
```

처럼 같은 Base Model에 서로 다른 목적의 Adapter를 만들 수 있다.

---

## 1.7 여러 Adapter 운영

하나의 Base Model에 여러 Adapter를 따로 관리할 수 있다.

```text
Llama-3.1-8B
├─ Adapter A: SQL
├─ Adapter B: Coding
├─ Adapter C: Customer Support
└─ Adapter D: Internal QA
```

Serving Engine이 LoRA Adapter Loading을 지원한다면
Base Model을 공유하면서 요청에 따라 Adapter를 선택하는 형태도 가능하다.

개념:

```text
                    ┌─ Finance Adapter
                    │
Base Model ─────────┼─ Coding Adapter
                    │
                    └─ Internal QA Adapter
```

이 구조는 Base Model을 여러 번 저장하거나 GPU에 여러 번 올리는 비용을 줄이는 데 도움이 될 수 있다.

---

## 1.8 Adapter와 Full Model Merge

LoRA Adapter는 Base Model Weight에 Merge할 수도 있다.

```text
Base Model
+
LoRA Adapter
↓
Merge
↓
Fine-Tuned Full Model
```

예:

```text
Qwen Base Model
+
Adapter v3
↓
Merged Model
```

저장 방식 비교:

```text
Adapter만 저장
→ 상대적으로 작음

Merged Full Model 저장
→ Base Model 전체 Weight 포함
→ 훨씬 큼
```

여러 Fine-Tuning 버전을 관리하는 Platform이라면
Base Model과 Adapter를 분리해 관리하는 방식이 효율적인 경우가 많다.

---

<!-- SOURCE CORE END -->

## 보완 — 행렬 차원 정정과 Artifact 사용 조건

2026-10-05 LoRA·QLoRA 논문과 공식 PEFT·Transformers·vLLM 문서를 확인했다. `main`/`latest` 문서는 변할 수 있으므로 실제 설치 버전을 별도로 고정해야 한다. 이 문서에서는 실행하지 않았다.

### 1.1–1.3 QLoRA의 고정 Weight와 저장·연산 Precision

QLoRA 논문은 고정된 4-bit base model을 통해 LoRA adapter로 gradient를 전달한다. 원문의 “대부분 고정”은 일반적인 QLoRA에서 base weight를 업데이트한다는 뜻이 아니다. NF4, double quantization, paged optimizer도 논문의 메모리 절감 구성이다. 4-bit 저장은 모든 연산이 4-bit라는 뜻이 아니며 bitsandbytes의 `bnb_4bit_compute_dtype` 같은 설정을 별도로 확인한다. [QLoRA 논문](https://arxiv.org/abs/2305.14314), [Transformers BitsAndBytesConfig](https://huggingface.co/docs/transformers/main_classes/quantization#transformers.BitsAndBytesConfig)

### 1.2 A/B 차원 정정

`W`가 `4096 × 4096`이고 `ΔW = B × A`라면, 표준 LoRA 표기에서 `A`는 `16 × 4096`, `B`는 `4096 × 16`이어야 한다. 원문에 적힌 차원 그대로 `B × A`를 계산하면 `16 × 16`이 되어 `W`에 더할 수 없다. 원문의 차원을 유지한다면 곱의 순서는 `A × B`여야 한다. 기본 LoRA에는 `α/r` scaling도 있으므로 원문 수식은 그 계수를 생략한 개념식이다. [LoRA 논문 §4.1](https://arxiv.org/html/2106.09685)

### 1.4 / 1.8 저장 파일과 Merge

PEFT adapter 저장의 핵심은 adapter weight와 `adapter_config.json`이다. Tokenizer·학습 인자·사용자 정의 metadata는 별도 저장 절차에 따라 달라진다. 원문의 파일 목록이 모든 도구의 자동 출력 목록은 아니다. Merge는 방법·quantization 설정에 따라 지원이 다르며, `merge_and_unload()` 결과는 PEFT adapter 전환 기능을 유지하지 않는다. [PEFT checkpoint](https://huggingface.co/docs/peft/main/en/developer_guides/checkpoint)

### 1.7 Serving 지원 확인

vLLM에서는 대상 모델의 LoRA 지원과 `enable_lora`, `max_loras`, `max_lora_rank` 같은 설정을 확인한다. 여러 adapter 파일이 있다는 사실만으로 요청별 전환이나 목표 동시 처리량이 보장되지는 않는다. [vLLM LoRA](https://docs.vllm.ai/en/latest/features/lora/)

## 관련 문서

- [AI 모델 개발 학습 지도](index.md)
- [Adapter 호환성](adapter-compatibility.md)
- [Training Dataset](training-datasets.md)
- [vLLM 서빙](../platform-infrastructure/vllm.md)
- [AWS Object Storage](../aws-cloud/storage-databases.md)
