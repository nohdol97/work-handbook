---
id: ai-model-development-model-developer
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-08-01
  - AIMFT-08-02
  - AIMFT-08-03
  - AIMFT-08-04
  - AIMFT-08-05
  - AIMFT-08-06
  - AIMFT-08-07
  - AIMFT-08-08
---

# Chapter 8. AI Model Developer의 역할

제공된 AI Model / QLoRA Training Basic Chapter 8의 학습 기록이다. 실제 모델 학습·배포 경험을 뜻하지 않는다.

**본문 안내:** 원문 제목·번호·문단·목록·text 도식을 그대로 보존했다. 8.4의 학습 방법 분류, 8.3·8.5·8.7–8.8의 평가 데이터 독립성, 8.6–8.7의 quantization 효과는 뒤의 **원문 절별 보완과 적용 조건**을 함께 읽는다. 코드·명령은 실행하지 않았다.

<!-- SOURCE CORE START -->

## 8.1 AI Model Developer의 핵심 역할

기존 Foundation Model을 회사나 서비스 목적에 맞게 Fine-Tuning하는 AI Model Developer는
단순히 Training Script를 실행하는 사람이 아니다.

핵심은:

```text
어떤 문제를 풀 것인가
↓
어떤 Data를 사용할 것인가
↓
어떤 Model을 선택할 것인가
↓
어떻게 Training할 것인가
↓
어떻게 Evaluation할 것인가
↓
왜 실패했는가
↓
어떻게 개선할 것인가
```

를 반복적으로 판단하는 것이다.

---

## 8.2 Problem Definition

먼저 무엇을 개선하려는지 정의한다.

예:

```text
업무 Task Accuracy
특정 Output Format
Instruction Following
Classification
Reasoning Pattern
Tool Use
```

그리고:

```text
Fine-Tuning이 필요한가?
RAG로 해결할 수 있는가?
Prompt Engineering으로 충분한가?
```

를 판단한다.

---

## 8.3 Dataset Design

AI Model Developer의 중요한 역할 중 하나가 Dataset 설계다.

해야 하는 일:

- 좋은 Sample 선별
- 잘못된 정답 제거
- 중복 데이터 제거
- 저품질 데이터 제거
- 원하는 Instruction / Response 형태로 변환
- 데이터 분포 확인
- Train / Validation / Golden 분리
- Dataset Version 관리

즉:

```text
Garbage Data
↓
좋은 Model을 만들기 어려움
```

이므로 Dataset Quality가 매우 중요하다.

---

## 8.4 Training Strategy 선택

문제와 Resource에 따라 Training 방법을 선택한다.

예:

```text
Full Fine-Tuning
LoRA
QLoRA
SFT
Preference Training
```

예를 들어 GPU Resource가 제한되어 있다면:

```text
Large Model Full Fine-Tuning
→ 비용 큼

Smaller Model + QLoRA
→ 상대적으로 현실적인 선택
```

같은 판단을 할 수 있다.

---

## 8.5 Hyperparameter Tuning

대표적으로 조정하는 값:

```text
Learning Rate
Batch Size
Epoch
LoRA Rank
LoRA Alpha
Target Modules
Sequence Length
Optimizer
```

한 번의 설정만 사용하는 것이 아니라 여러 Experiment를 비교한다.

```text
Experiment A
↓
Evaluate

Experiment B
↓
Evaluate

Experiment C
↓
Evaluate
```

그리고 가장 좋은 결과를 선택한다.

---

## 8.6 Quantization 고려

AI Model Developer는 Training Resource와 Serving Resource를 고려해 Quantization도 판단할 수 있다.

구분:

```text
Training Quantization
→ QLoRA 등
→ 학습 GPU Memory 절감

Serving Quantization
→ FP8 / INT8 / INT4 등
→ Inference Memory / Cost 절감
```

두 영역은 목적이 다르다.

Serving Quantization은 AI Serving / Platform Engineer와 함께 판단할 수 있다.

---

## 8.7 Evaluation

모델 개발자에게 Evaluation은 핵심 역할이다.

확인해야 하는 것:

```text
Fine-Tuning 후 정말 좋아졌는가?
특정 영역만 좋아지고 다른 영역은 나빠지지 않았는가?
Hallucination이 증가하지 않았는가?
Output Format을 지키는가?
Production 요구 Latency를 만족하는가?
```

따라서:

```text
Golden Dataset
+
Evaluation Metric
+
Error Analysis
```

가 중요하다.

---

## 8.8 Error Analysis와 Dataset 개선

모델이 틀린 문제를 보고 Data 문제인지 Model 문제인지 분석한다.

```text
Evaluation Failure
↓
Failure Category 분류
↓
Dataset 부족 확인
↓
Data 추가 / 정제
↓
Dataset New Version
↓
Retraining
```

이 Loop를 반복하면서 모델을 개선한다.

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 적용 조건

2026-10-05에 공식 문서를 확인했다. 다음은 원문 밖의 보완이며 실제 모델 학습·평가 결과가 아니다.

### 8.4: Training 방법의 분류축

Full Fine-Tuning과 LoRA는 주로 어떤 파라미터를 학습하는지의 차이이며, QLoRA는 양자화한 base model과 LoRA 학습을 결합한다. SFT와 preference training은 학습 목적·데이터 신호의 구분이다. 서로 배타적인 다섯 선택지가 아니므로, 예를 들어 SFT를 QLoRA 방식으로 수행할 수 있다. [PEFT quantization](https://huggingface.co/docs/peft/developer_guides/quantization), [TRL SFT Trainer](https://huggingface.co/docs/trl/sft_trainer)

### 8.3·8.5·8.7–8.8: 비교에 쓴 데이터와 독립 평가

Hyperparameter와 모델 선택에 반복 사용한 데이터는 선택 과정에 영향을 준다. Golden이라는 이름만으로 독립적인 최종 평가가 보장되지 않는다. 권고: 반복 회귀 검사에 쓰는 고정 suite와 최종 선택 후 확인하는 미사용 holdout을 구분한다. 실패 유형에서 일반적인 학습 과제를 찾되, 최종 평가 정답을 training으로 복사하지 않는다. 같은 사례를 반복 확인하며 선택한 성능과 새 사례에 대한 성능을 구분한다. [교차검증과 test set 분리](https://scikit-learn.org/stable/modules/cross_validation.html)

### 8.6–8.7: Quantization과 운영 성능

학습용 양자화와 serving용 양자화는 목적뿐 아니라 지원 kernel·hardware·format도 확인해야 한다. 낮은 정밀도가 항상 더 낮은 latency나 비용을 보장하는 것은 아니다. 권고: 같은 평가 조건과 실제 목표 GPU에서 품질, TTFT/TPOT, throughput, memory를 함께 측정한다. [vLLM quantization 지원표](https://docs.vllm.ai/en/latest/features/quantization/)

## 관련 내용

- [모델 개발자와 플랫폼 협업](model-platform-collaboration.md)
- [학습 플랫폼 전체 구조](training-platform-architecture.md)
- [GPU 인프라와 capacity](../platform-infrastructure/gpu-infrastructure.md)
- [vLLM serving](../platform-infrastructure/vllm.md)
