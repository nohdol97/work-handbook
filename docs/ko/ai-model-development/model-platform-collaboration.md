---
id: ai-model-development-model-platform-collaboration
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-09-01
  - AIMFT-09-02
  - AIMFT-09-03
---

# Chapter 9. AI Model Developer와 AI Platform Engineer

제공된 AI Model / QLoRA Training Basic Chapter 9의 학습 기록이다. 실제 모델 학습·배포 경험을 뜻하지 않는다.

**본문 안내:** 원문 제목·번호·문단·목록·text 도식을 그대로 보존했다. 9.2의 요청·평가·배포 판단 경계와 9.2–9.3의 adapter 전달 조건은 뒤의 **원문 절별 보완과 적용 조건**을 함께 읽는다. 코드·명령은 실행하지 않았다.

<!-- SOURCE CORE START -->

## 9.1 역할 차이

AI Model Developer는 모델 품질을 중심으로 본다.

```text
어떤 Dataset?
어떤 Base Model?
어떤 Fine-Tuning 방법?
어떤 Hyperparameter?
성능이 좋아졌는가?
왜 실패했는가?
```

AI Platform Engineer는 이 과정이 안정적이고 반복 가능하게 실행되도록 Platform을 만든다.

```text
Dataset을 어디서 관리할 것인가?
GPU Training Job을 어떻게 실행할 것인가?
Artifact를 어디에 저장할 것인가?
Experiment를 어떻게 추적할 것인가?
Evaluation을 어떻게 자동화할 것인가?
Model Registry는 어떻게 구성할 것인가?
Serving은 어떻게 할 것인가?
Monitoring / Rollback은 어떻게 할 것인가?
```

---

## 9.2 협업 예시

Model Developer 요청:

```text
Qwen
+
training-dataset-v12
+
QLoRA Rank 32
+
3 Epoch
```

Platform은 이를 실행한다.

```text
Dataset Registry
↓
Training Job
↓
GPU
↓
Adapter Artifact
↓
S3
↓
Model Registry
↓
Golden Evaluation
↓
Deployment
```

평가 후 Model Developer가 결과를 확인한다.

```text
Reasoning 성능 부족
↓
Training Data 개선
↓
Dataset v13
↓
Retraining
```

---

## 9.3 Model Developer와 Platform의 책임 경계

개념적으로:

```text
Model Developer
= 무엇을 학습하고 어떻게 품질을 높일 것인가

AI Platform Engineer
= 그 학습 / 평가 / 배포 과정을 어떻게 안정적으로 제공할 것인가
```

둘은 완전히 분리된 역할이 아니라 협업 영역이 많다.

예:

```text
Quantization
GPU Memory
Serving Latency
Model Packaging
Evaluation Automation
```

등은 함께 판단할 수 있다.

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 적용 조건

2026-10-05에 공식 문서를 확인했다. 원문의 역할 구분과 요청 흐름은 협업 예시이며 실제 조직의 승인 규칙이나 배포 실행 기록이 아니다.

### 9.2: 실행 요청과 배포 결정

`Rank 32`와 `3 Epoch`는 요청 예시이며 권장 기본값이나 품질 보장이 아니다. 권고: 요청은 base model의 정확한 revision, 데이터·설정 버전, 자원·비용 한도, 평가 기준까지 식별한다. 평가를 실행했다는 사실과 품질 기준 통과, 운영 전환 권한을 구분한다. [학습 플랫폼 전체 구조](training-platform-architecture.md)의 10.1·10.3 보완과 [개발자 플랫폼](../platform-infrastructure/developer-platform.md)의 승인·용량 경계를 함께 읽는다.

### 9.2–9.3: Adapter 전달 계약

PEFT adapter checkpoint는 보통 base model 전체를 포함하지 않는다. 학습팀이 adapter 파일만 넘겼다고 serving 가능한 model이 완성되는 것은 아니다. 정확한 base model revision과 adapter config·weights, tokenizer와 template, 호환 환경을 함께 식별한다. [PEFT checkpoint format](https://huggingface.co/docs/peft/developer_guides/checkpoint)

권고: 모델 개발자는 품질 기준·실패 범주·데이터 변경 의도를, 플랫폼 담당자는 artifact 추적·실행 환경·배포 상태·rollback 경로를 기록한다. Quantization, GPU memory, latency, packaging과 평가 자동화의 최종 판단 담당자를 실제 조직에서 정한다. 역할 이름만으로 배포 권한을 추론하지 않는다.

## 관련 내용

- [AI 모델 개발자의 역할](model-developer.md)
- [학습 플랫폼 전체 구조](training-platform-architecture.md)
- [AWS GPU model storage와 권한](../aws-cloud/ai-gpu-architecture.md)
- [CI/CD와 GitOps](../platform-infrastructure/cicd-gitops.md)
