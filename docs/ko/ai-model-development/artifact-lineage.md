---
id: ai-model-development-artifact-lineage
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-07-01
  - AIMFT-07-02
  - AIMFT-07-03
  - AIMFT-07-04
---

# Chapter 7. Model / Dataset Artifact 관리

**읽기 안내:** 원문의 제목·번호·표·예시·text 도식을 그대로 보존했다. 원문 뒤의 **원문 절별 보완과 적용 조건**에서 실제 적용 조건을 함께 읽는다. 수치와 설정은 학습용 예시이며 이 문서에서 학습·배포·성능 시험을 실행하지 않았다.

<!-- SOURCE CORE START -->

## 7.1 S3 구조 예시

```text
s3://ai-platform/
├─ datasets/
│  ├─ training/
│  │  ├─ v1/
│  │  ├─ v2/
│  │  └─ v3/
│  │
│  ├─ validation/
│  │  └─ v3/
│  │
│  └─ golden/
│     └─ v5/
│
└─ models/
   ├─ llama-3.1-8b/
   │  └─ adapters/
   │     ├─ v1/
   │     └─ v2/
   │
   └─ qwen/
      └─ adapters/
         └─ v1/
```

Object Storage는 실제 파일을 저장한다.

하지만 파일만 저장해서는 어떤 Experiment에서 만들어졌는지 알기 어렵다.

---

## 7.2 Metadata 연결

Adapter에는 다음 Metadata를 연결할 수 있다.

```text
Adapter v5
├─ Base Model: Qwen
├─ Base Model Revision
├─ Training Dataset: train-v12
├─ Validation Dataset: validation-v12
├─ Golden Dataset: golden-v5
├─ Training Config: qlora-config-v2
├─ Training Run: run-20261005-001
└─ Evaluation Result: eval-20261005-003
```

이렇게 연결하면 재현 가능한 Training Pipeline을 만들 수 있다.

---

## 7.3 Model Registry의 역할

S3는 Artifact 파일을 저장하는 역할이다.

Model Registry는 그 Artifact의 의미와 상태를 관리하는 역할을 할 수 있다.

예:

```text
S3
= 실제 Adapter / Model File

Model Registry
= Version / Metadata / Stage / Lineage 관리
```

Stage 예:

```text
Candidate
↓
Validated
↓
Staging
↓
Production
↓
Archived
```

---

## 7.4 Training Lineage

중요한 것은 다음 관계를 추적할 수 있는 것이다.

```text
Dataset Version
↓
Training Run
↓
Base Model
↓
Training Config
↓
Adapter Artifact
↓
Evaluation Result
↓
Deployment
```

문제가 발생했을 때:

```text
현재 Production Model은
어떤 Dataset으로 학습했고
어떤 Config를 사용했고
어떤 Evaluation을 통과했는가?
```

를 추적할 수 있어야 한다.

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 적용 조건

2026-10-05에 아래 공식 자료를 확인했다. S3 경로와 run/eval ID는 학습용 예시이며 실제 저장소나 학습 실행을 가리키지 않는다.

### 7.1: Prefix와 불변 Artifact

`v1/` 같은 prefix는 이름일 뿐 내용 덮어쓰기를 막지 않는다. S3 Versioning은 object의 여러 version을 유지한다. 재현할 artifact에는 key와 versionId 또는 검증 가능한 content hash를 연결하는 것이 좋다. Versioning 자체를 삭제 방지나 write-once 보장으로 읽지 않는다. [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

### 7.2·7.4: 추적 가능성과 재현성

검토 권고: 원문 metadata에 tokenizer/chat template revision, code commit, library/container version, seed, quantization·generation 설정과 dataset/artifact hash를 더한다. 학습 재개가 필요하면 checkpoint 상태도 별도로 관리한다. 연결 정보를 갖췄다는 사실만으로 결과가 bitwise 동일함을 보장하지 않는다. PyTorch도 deterministic algorithm 설정 하나만으로 전체 애플리케이션 재현성이 보장되지는 않는다고 설명한다. [PyTorch deterministic algorithms](https://docs.pytorch.org/docs/main/generated/torch.use_deterministic_algorithms.html)

7.4의 직선 화살표는 추적할 항목의 개념도다. 실제 lineage에서는 dataset·base model·training config가 run의 입력이고, adapter는 출력이며 evaluation과 deployment가 그 artifact를 참조한다. 관계 방향을 구분해야 어떤 입력 변경이 어느 배포에 영향을 주는지 찾을 수 있다. [Lineage와 Metadata](../data-platform/lineage-metadata.md)

### 7.3: 개념 Stage와 Registry 구현

원문의 Candidate→Validated→Staging→Production→Archived는 설계 예시다. 모든 registry가 이 상태를 그대로 제공한다는 뜻은 아니다. MLflow의 Model Stages는 2.9.0부터 deprecated이며 현재 문서는 aliases·tags와 환경 분리를 안내한다. 구현할 제품과 버전에 맞게 상태·승인·artifact 참조 규칙을 정한다. Registry 상태 변경과 실제 serving 배포 성공도 구분한다. [MLflow Model Registry workflows](https://mlflow.org/docs/latest/ml/model-registry/workflow/)

## 관련 문서

[QLoRA Artifact](qlora-artifacts.md) · [평가와 승격](evaluation-promotion.md) · [S3 Storage](../aws-cloud/storage-databases.md) · [Lineage와 Metadata](../data-platform/lineage-metadata.md)
