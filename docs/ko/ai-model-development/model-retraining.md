---
id: ai-model-development-model-retraining
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-06-01
  - AIMFT-06-02
  - AIMFT-06-03
---

# Chapter 6. Model Change와 Re-Training

**읽기 안내:** 원문의 제목·번호·표·예시·text 도식을 그대로 보존했다. 원문 뒤의 **원문 절별 보완과 적용 조건**에서 실제 적용 조건을 함께 읽는다. 수치와 설정은 학습용 예시이며 이 문서에서 학습·배포·성능 시험을 실행하지 않았다.

<!-- SOURCE CORE START -->

## 6.1 Base Model 교체 시 흐름

운영 모델을 Llama에서 Qwen으로 변경한다고 가정한다.

기존:

```text
Llama
+
Adapter v4
```

변경:

```text
Qwen
+
새 Adapter
```

기존 Llama Adapter를 그대로 사용하는 것이 아니라
기존 Training Dataset을 이용해 새로운 Qwen Adapter를 학습한다.

---

## 6.2 Model 교체 Process

```text
1. 새로운 Base Model 준비
↓
2. 기존 Training Dataset 선택
↓
3. 새로운 Base Model에 QLoRA Fine-Tuning
↓
4. 새로운 Adapter 생성
↓
5. 동일 Golden Dataset으로 평가
↓
6. 기존 Production Model과 비교
↓
7. Quality / Cost / Latency 기준 확인
↓
8. Promote 또는 Reject
```

이 구조를 갖추면 Base Model이 바뀌어도 동일한 기준으로 비교할 수 있다.

---

## 6.3 Dataset이 장기 자산인 이유

Model은 빠르게 교체될 수 있다.

하지만 다음은 계속 사용할 수 있다.

```text
Training Dataset
Validation Dataset
Golden Dataset
Evaluation Logic
Business Metric
```

따라서 장기적인 AI Asset은:

```text
Model
```

하나가 아니라:

```text
Data
+
Evaluation
+
Experiment History
```

까지 포함한다.

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 적용 조건

2026-10-05에 아래 공식 자료를 확인했다. 다음은 모델 교체 전 검토 조건이며 Llama/Qwen 학습을 수행한 결과가 아니다.

### 6.1–6.2: Base 교체와 Dataset 재사용의 조건

PEFT adapter를 load할 때는 학습한 base model과의 대응을 확인해야 한다. Llama용 adapter를 Qwen에 그대로 붙일 수 있다는 뜻이 아니다. 이름만 바꾸기보다 base revision·구조·target module을 기록하고 새 adapter를 학습·평가한다. [PEFT troubleshooting](https://huggingface.co/docs/peft/main/developer_guides/troubleshooting)

기존 raw 대화 데이터는 재사용할 수 있어도 tokenized ID를 새 tokenizer에 그대로 넘기지 않는다. 새 모델의 tokenizer·chat template·special token과 길이 제한으로 다시 준비한다. 서로 다른 모델이 같은 대화를 다른 token 형식으로 받는다는 점을 반영한다. [Chat templates](https://huggingface.co/docs/transformers/main/chat_templating)

검토 권고: Dataset 사용 권한·모델 라이선스·업무 범위를 다시 확인한다. 비교에는 동일한 평가 질문과 기준을 쓰되 각 모델에 맞는 입력 형식과 serving 설정도 기록한다. 품질·비용·latency의 허용 범위와 rollback 대상을 정하고, 결과가 부족하면 승격을 보류한다.

### 6.3: 오래 쓰는 자산도 갱신이 필요하다

Data·평가·실험 이력은 재사용 자산이지만 영구히 정확한 기준은 아니다. 업무 정책·label·권한이 바뀌면 dataset 버전과 평가 기준도 갱신한다. 이전 모델과의 비교 가능성을 위해 변경 이유와 공통 평가 범위를 남긴다. Golden set 반복 사용의 선택 편향은 [5.5–5.6 보완](evaluation-promotion.md)과 함께 검토한다.

## 관련 문서

[Adapter 호환성](adapter-compatibility.md) · [학습 데이터셋](training-datasets.md) · [평가와 승격](evaluation-promotion.md) · [Artifact와 Lineage](artifact-lineage.md)
