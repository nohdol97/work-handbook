---
id: ai-model-development-adapter-compatibility
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-02-01
  - AIMFT-02-02
  - AIMFT-02-03
  - AIMFT-02-04
---

# Chapter 2. Adapter 재사용과 Base Model 변경

제공된 학습 원문의 번호·순서·예시를 보존했다. 2.1–2.4의 호환성은 로딩 가능 여부와 실제 품질을 구분해야 한다. 모델 revision·module 설정·tokenizer 조건은 뒤의 별도 보완을 함께 읽는다. 실제 Adapter 이식이나 재학습을 수행한 기록이 아니다.

<!-- SOURCE CORE START -->

## 2.1 다른 모델에 Adapter를 그대로 적용할 수 있는가

원칙적으로 다른 Base Model에 기존 LoRA Adapter를 그대로 적용할 수 없다고 이해하면 된다.

예:

```text
Llama-3.1-8B
+
Llama용 LoRA Adapter
→ 가능
```

하지만:

```text
Mistral-7B
+
Llama용 LoRA Adapter
→ 일반적으로 불가능
```

이유는 Adapter가 특정 Base Model의 Layer 구조와 Dimension을 기준으로 학습되기 때문이다.

---

## 2.2 Target Module 의존성

LoRA는 Transformer 내부의 특정 Linear Layer에 붙는다.

예:

```text
q_proj
k_proj
v_proj
o_proj

gate_proj
up_proj
down_proj
```

Adapter 설정에는 어떤 Module을 학습했는지가 포함된다.

예:

```text
target_modules:
- q_proj
- v_proj
```

대상 모델에서 해당 Layer 구조나 Dimension이 다르면 같은 Adapter Weight를 적용할 수 없다.

---

## 2.3 같은 계열 모델도 주의

같은 Llama 계열이라고 무조건 Adapter가 호환되는 것은 아니다.

예:

```text
Llama 8B Adapter
→ Llama 70B
```

는 Weight Dimension이 다르기 때문에 그대로 적용할 수 없다.

따라서 Adapter에는 최소한 다음 정보를 함께 관리해야 한다.

```text
Base Model Name
Base Model Version / Revision
Adapter Type
LoRA Rank
LoRA Alpha
Target Modules
Training Dataset Version
```

---

## 2.4 Base Model 변경 시 해야 하는 일

Base Model을 변경하면 기존 Adapter를 옮기는 것이 아니라
동일한 Training Dataset을 이용해서 새로운 Base Model을 다시 Fine-Tuning하는 방식으로 접근한다.

예:

```text
Training Dataset v3
      │
      ├─ Llama-3.1-8B
      │      ↓
      │   QLoRA
      │      ↓
      │   Adapter A
      │
      └─ Qwen
             ↓
          QLoRA
             ↓
          Adapter B
```

즉 장기적으로 중요한 자산은 Adapter 하나만이 아니다.

```text
Dataset
+
Training Configuration
+
Evaluation Dataset
+
Experiment History
```

를 함께 관리해야 한다.

---

<!-- SOURCE CORE END -->

## 보완 — 로딩 호환성과 품질 검증

2026-10-05 공식 PEFT·Transformers 문서를 확인했다. 아래는 원문 밖의 설명·검토 권고이며 실제 이식 실험이 아니다. `main` 문서와 설치 버전의 차이를 확인한다.

### 2.1 / 2.3 같은 구조도 같은 결과를 보장하지 않는다

Base model 이름과 revision을 adapter 설정과 함께 기록한다. PEFT checkpoint는 base weight 자체를 포함하지 않는다. [PEFT checkpoint](https://huggingface.co/docs/peft/main/en/developer_guides/checkpoint)

검토 권고: 차원이 같아 로드되더라도 다른 revision의 weight가 학습 당시와 같다는 뜻은 아니다. 이름·파일 로딩 성공만으로 호환성을 판정하지 않고, 실제 base revision·tokenizer·chat template·평가 결과를 함께 확인한다. [평가 데이터와 Model Version](../data-platform/ai-evaluation.md)

### 2.2 Target Module 이름은 모델별 설정

원문의 `q_proj`·`v_proj` 등은 예시다. PEFT의 `target_modules`는 이름 목록·패턴 또는 지원되는 일괄 선택을 사용하며 모델 구조에 맞아야 한다. LoRA 적용 범위는 구현에 따라 linear layer 외에도 확장될 수 있으므로 원문을 모든 지원 유형의 목록으로 읽지 않는다. [PEFT LoRA 설정](https://huggingface.co/docs/peft/main/package_reference/lora)

### 2.4 Dataset 재사용 시 입력 형식도 검토

같은 의미의 학습 sample을 재사용하더라도 모델별 tokenizer·special token·chat template은 다를 수 있다. 원문의 “동일한 Dataset”은 이전 모델의 token ID를 그대로 재사용한다는 뜻이 아니다. 새 base model의 형식으로 다시 처리한 입력과 출력, 평가 조건을 확인한다. [Transformers chat templates](https://huggingface.co/docs/transformers/chat_templating)

## 관련 문서

- [AI 모델 개발 학습 지도](index.md)
- [QLoRA와 Artifact](qlora-artifacts.md)
- [Training Dataset](training-datasets.md)
- [AI 평가 데이터 플랫폼](../data-platform/ai-evaluation.md)
