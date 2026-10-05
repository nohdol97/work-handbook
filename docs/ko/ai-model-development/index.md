---
id: ai-model-development-overview
status: studied
last_updated: '2026-10-05'
last_reviewed: '2026-10-05'
knowledge_ids:
- AIMFT-00-01
- AIMFT-00-02
- AIMFT-00-03
- AIMFT-00-04
- AIMFT-00-05
- AIMFT-00-06
- AIMFT-00-07
- AIMFT-00-08
- AIMFT-00-09
- AIMFT-00-10
---

# AI 모델 개발·QLoRA 학습

제공된 기초 자료 1~10장의 원문과 최종 요약을 반영했다. QLoRA·데이터 설계·학습·평가·모델 교체·artifact 추적·개발자와 플랫폼의 역할을 연결한다. 실제 GPU 학습·모델 성능 평가·배포를 수행한 기록은 아니다.

**본문 안내:** 원문 번호·예시·도식을 보존했다. 1.2의 LoRA 행렬 차원 정정, adapter 호환 조건, golden dataset의 독립성, 재현성 한계는 각 장 뒤의 보완 설명에서 확인한다. 아래 원문 요약도 해당 조건과 함께 읽는다.

| 장 | 학습 문서 |
|---|---|
| 1 | [QLoRA·학습 결과물](qlora-artifacts.md) |
| 2 | [Adapter 호환성](adapter-compatibility.md) |
| 3 | [Training·Golden Dataset](training-datasets.md) |
| 4 | [QLoRA 학습 과정](qlora-training.md) |
| 5 | [평가·Model Promotion](evaluation-promotion.md) |
| 6 | [모델 교체·재학습](model-retraining.md) |
| 7 | [Artifact·Lineage](artifact-lineage.md) |
| 8 | [AI Model Developer 역할](model-developer.md) |
| 9 | [모델·플랫폼 협업](model-platform-collaboration.md) |
| 10 | [Fine-Tuning 플랫폼 구조](training-platform-architecture.md) |

## 함께 읽기

[AI 데이터 준비](../data-platform/ai-ready-data.md), [AI 평가](../data-platform/ai-evaluation.md), [GPU 인프라](../platform-infrastructure/gpu-infrastructure.md), [vLLM](../platform-infrastructure/vllm.md), [AWS AI/GPU](../aws-cloud/ai-gpu-architecture.md)와 연결된다. [실전 영어 학습](../english-study/index.md)에서 설명에 쓸 어휘와 문장을 연습한다.

<!-- SOURCE INTRO START -->

# AI Model Fine-Tuning / QLoRA Basic
## Source Markdown — QLoRA, Dataset, Training, Evaluation, Model Developer Role

> 이 문서는 이 학습 세션에서 진행한 **QLoRA 기반 LLM Fine-Tuning과 AI Model Developer 역할**을 정리한 source markdown이다.  
> 범위: **QLoRA Artifact → Dataset / Golden Dataset → Training Process → Evaluation → Model Developer / AI Platform 역할 구분**

---

<!-- SOURCE INTRO END -->

<!-- SOURCE SUMMARY START -->

# Final Summary

이번 세션의 핵심은 다음과 같다.

## QLoRA

```text
Base Model을 4-bit로 사용
+
LoRA Adapter만 학습
```

Base Model 전체를 수정하지 않고 작은 Adapter를 학습한다.

---

## Artifact

QLoRA Training 결과는 주로:

```text
adapter_model.safetensors
adapter_config.json
```

형태이며 S3 같은 Object Storage에 저장할 수 있다.

---

## Adapter Compatibility

```text
같은 Base Model
→ Adapter 사용 가능

다른 Base Model / 다른 Size / 다른 Architecture
→ 기존 Adapter 그대로 사용 어려움
→ 새로운 Fine-Tuning 필요
```

따라서 Base Model 변경에 대비해 Training Dataset을 잘 관리해야 한다.

---

## Dataset

```text
Training Dataset
→ 실제 학습

Validation Dataset
→ 학습 중 검증

Golden Dataset
→ 최종 품질 비교
```

Golden Dataset은 Training Data에 포함시키지 않는다.

---

## Training

```text
Dataset
↓
Tokenizer
↓
Base Model + LoRA
↓
Prediction
↓
Loss
↓
Backpropagation
↓
LoRA Adapter Update
```

이를 여러 Batch / Epoch에 걸쳐 반복한다.

---

## Evaluation

```text
Base Model
vs
Fine-Tuned Model
```

을 동일 Golden Dataset으로 비교한다.

Training Loss뿐 아니라 실제 Task Metric을 기준으로 판단한다.

---

## Model Developer

AI Model Developer의 핵심 역할:

```text
Problem Definition
↓
Dataset Design
↓
Model Selection
↓
Training Strategy
↓
Hyperparameter Tuning
↓
Evaluation
↓
Error Analysis
↓
Dataset Improvement
```

즉 단순히 Training Script를 실행하는 역할이 아니다.

---

## AI Platform Engineer

AI Platform Engineer는 위 과정이 반복 가능하게 돌아가도록 만든다.

```text
Dataset Registry
Training Infrastructure
GPU Job
Artifact Storage
Experiment Tracking
Model Registry
Evaluation Pipeline
Serving
Monitoring
Rollback
```

을 Platform으로 제공한다.

---

## 가장 중요한 관점

장기적으로 AI 시스템의 자산은 특정 Model 하나만이 아니다.

```text
Training Dataset
+
Golden Dataset
+
Evaluation System
+
Training / Experiment History
+
Model Artifact
```

전체가 자산이다.

Base Model은 계속 바뀔 수 있지만,
잘 만들어진 Dataset과 Evaluation 체계가 있으면 새로운 Model을 다시 학습하고 동일한 기준으로 검증할 수 있다.

<!-- SOURCE SUMMARY END -->
