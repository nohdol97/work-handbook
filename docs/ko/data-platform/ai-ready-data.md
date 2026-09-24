---
id: data-platform-ai-ready-data
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-15-01
  - DPE-15-02
  - DPE-15-02A
  - DPE-15-03
  - DPE-15-04
  - DPE-15-05
  - DPE-15-06
  - DPE-15-07
  - DPE-15-08
  - DPE-15-09
---

# AI가 활용할 수 있는 데이터

원문의 Chapter 15를 개념별로 정리했다. `studied`는 개념 학습을 뜻하며 실제 구축·운영 또는 실행 검증을 뜻하지 않는다. 예시의 버전과 숫자는 설명용이다.

## 15.1 What Makes Data AI-Ready

AI-Ready Data는 특정 File Format이 아니다.

> **AI가 신뢰하고 반복해서 사용할 수 있도록 품질·최신성·버전·Metadata·Governance가 갖춰진 데이터**

핵심 특성:

### Trustworthy

Data Quality.

### Fresh

충분히 최신.

### Versioned

Dataset/Prompt/Model/Agent 버전 관리.

### Discoverable

Catalog/Metadata로 찾을 수 있음.

### Governed

Access/Masking/Retention/Audit.

기존 Data Platform 기능이 AI-Ready의 기반이다.

---

## 15.2 AI Telemetry Model

AI 서비스 실행을 분석하기 위한 Telemetry.

전체 흐름:

```text
User Prompt
 ↓
Agent
 ↓
LLM Call
 ↓
Tool Call
 ↓
LLM Call
 ↓
Response
 ↓
Feedback
```

주요 수집 데이터:

### Prompt / Response

평가/개선의 기본.

### Model

Model ID/Version.

### Agent

Agent ID/Version.

### Tool Call

Tool name, input/output, latency, status.

### Latency

- total
- llm
- tool

### Token / Cost

- input tokens
- output tokens
- total cost

### Feedback

- thumbs up/down
- human label
- judge score

### Trace / Execution / Session ID

모든 이벤트를 하나의 실행 흐름으로 연결.

AI Telemetry는 단순 로그가 아니라:

- Evaluation Dataset
- Failure Analysis
- Model Comparison
- Prompt Comparison
- Regression Test
- Cost Optimization

에 활용되는 데이터 자산이다.

---

## 15.2A Langfuse as AI Telemetry / Evaluation Layer

학습 질문: “Langfuse가 AI telemetry를 담당할 수 있는가?” 역할은 아래처럼 대응하지만 실제 수집 범위는 계측과 연동에 달려 있다.

Langfuse는 AI Telemetry 영역을 상당 부분 담당할 수 있다.

개념 대응:

```text
Agent 실행
→ Trace

LLM Call / Tool Call
→ Observation

Conversation 묶음
→ Session

Prompt / Response
→ Input / Output

Token / Cost
→ Usage / Cost

Latency
→ Timing

User / Human / Judge 평가
→ Score

Evaluation Data
→ Dataset

변경 비교
→ Experiment
```

역할 분리:

```text
Langfuse
→ AI Telemetry
→ AI Observability
→ Evaluation

Iceberg / Data Platform
→ 장기 데이터 자산화
→ 통합 분석
→ Governance
```

학습용 개념 구조(검증된 연동 구현이 아님):

```text
Application / Agent
   ↓
Langfuse
   ↓
Trace / Observation / Score
   ├─→ Langfuse UI
   └─→ Data Platform / Iceberg
          ↓
       Spark / dbt
          ↓
       BI / Long-term Analysis
```

Langfuse가 Data Platform 전체를 대체하는 것은 아니다.

---

## 15.3 Dataset Versioning

Evaluation Dataset은 시간에 따라 변한다.

예:

```text
eval_v1
→ 1,000 cases

eval_v2
→ 1,500 cases
→ hard cases 추가
→ 정답 수정
```

Model Score 비교에서 Dataset Version이 다르면 공정한 비교가 아닐 수 있다.

함께 기록:

- dataset_version
- model_version
- prompt_version
- agent_version
- evaluator_version
- score

Iceberg Snapshot과 Dataset Version은 동일하지 않다.

```text
Iceberg Snapshot
→ 테이블 메타데이터가 가리키는 파일 집합의 일관된 상태

Dataset Version
→ AI/업무 관점의 논리적 Dataset 버전
```

---

## 15.4 Reproducibility

Reproducibility:

> **과거 AI 실험 조건을 다시 구성할 수 있는 능력**

필요:

- Dataset Version
- Model Version
- Prompt Version
- Agent Version
- Evaluator Version
- Runtime Config

예:

```text
dataset_v5
model_v3
prompt_v12
agent_v7
judge_v2
temperature=0
```

Lineage와 차이:

```text
Lineage
→ 어디서 만들어졌나?

Reproducibility
→ 동일한 실험 조건을 다시 구성할 수 있나?
```

LLM은 stochastic할 수 있으므로 재현성은 항상 동일 문장을 생성한다는 뜻이 아니라 **조건을 정확히 재구성하는 것**이 핵심이다.

---

## 15.5 Evaluation Dataset Construction

Evaluation Dataset:

> **Model/Prompt/Agent 품질을 반복적으로 평가하는 Test Dataset**

좋은 Source:

- Production Trace
- User Feedback
- 실제 Failure
- Edge Case
- Hard Case

성공 사례만 넣으면 안 된다.

포함 예:

- Normal
- Hard
- Failure
- Edge Case
- Safety
- Tool Usage

### Regression Dataset

실제 Production Bug/Failure를 수정한 뒤 해당 사례를 Dataset에 추가한다.

```text
Production Failure
 ↓
Fix
 ↓
Regression Case 추가
 ↓
이후 모든 Version에서 재평가
```

Expected Answer가 항상 필요한 것은 아니다.

Expected Behavior / Rubric도 가능.

예:

```text
올바른 Tool을 호출해야 함
권한 없는 정보 노출 금지
특정 Citation 필요
```

---

## 15.6 Embedding Data

RAG Pipeline:

```text
Source Document
 ↓
Chunk
 ↓
Embedding Model
 ↓
Vector
 ↓
Vector DB / Search
```

Vector만 저장하면 부족하다.

같이 관리:

### Document

- document_id
- document_version
- source
- owner

### Chunk

- chunk_id
- chunk_text
- chunk_index
- chunk_version
- chunking_strategy

### Embedding

- embedding_model
- embedding_model_version
- embedding_vector

Embedding Model이 바뀌면 Vector Space가 달라질 수 있으므로 Version 관리가 중요하다.

Chunk Strategy가 바뀌어도 검색 결과가 달라진다.

---

## 15.7 Retrieval Metadata

RAG Retrieval 결과에 함께 저장:

- document_id
- chunk_id
- source
- retrieval_score
- document_version
- access_level

### Access Metadata

사내 RAG에서는 권한 없는 문서를 **검색 후 숨기는 것보다 Retrieval 단계에서 제외**하는 것이 중요하다.

```text
User Permission
 ↓
Metadata Filter
 ↓
Authorized Chunks only
```

Retrieval Trace를 남기면:

```text
정답 문서를 못 가져옴
→ Retrieval Problem

정답 문서는 가져왔는데 답이 틀림
→ Generation Problem
```

으로 구분할 수 있다.

---

## 15.8 Provenance

Provenance:

> **데이터/AI 결과의 출처와 생성 과정을 넓게 추적하는 정보**

Lineage보다 더 넓게:

```text
Original Document
 ↓
Chunk
 ↓
Embedding
 ↓
Retrieval
 ↓
Model
 ↓
Response
```

까지 포함할 수 있다.

관계:

```text
Lineage
→ 데이터 이동/변환

Provenance
→ 출처와 생성 과정

Reproducibility
→ 그 조건을 다시 구성
```

Governance와 연결하면 특정 Source 사용 금지/삭제 시 파생 데이터 영향 추적에 도움이 된다.

---

## 15.9 Feature / Label Freshness

### Feature

Model 입력 데이터.

예:

- 최근 로그인 횟수
- 최근 구매
- 사용자 상태

Feature가 오래되면 Prediction 품질이 떨어질 수 있다.

### Label

Model이 맞혀야 하는 정답.

예:

```text
Feature:
최근 30일 사용량

Label:
다음 7일 내 탈퇴 여부
```

Label은 실제 결과가 확정될 때까지 지연될 수 있다.

예:

```text
구매
 ↓
30일 대기
 ↓
반품 여부 확정
 ↓
Label 생성
```

미확정 Label을 Training/Evaluation에 사용하면 왜곡될 수 있다.

LLM/Agent에서도 유사:

```text
Feature-like
→ 최신 Context / Tool State

Label-like
→ Human Feedback / Judge Score
```

---

## 확인한 범위와 보완

Trace는 요청·작업의 논리적 묶음, observation은 LLM·tool·retrieval 같은 개별 단계, session은 여러 trace를 묶는 단위다. 실제 저장 구현을 이 개념 그림에서 추론하지 않는다. [Langfuse data model](https://langfuse.com/docs/observability/data-model).

Langfuse dataset item 변경에는 시각 기반 버전이 생기지만 dataset schema 변경은 같은 버전 관리 범위가 아니다. 실험을 재구성하려면 입력 버전 외에 schema와 평가 설정도 보존한다. [Langfuse datasets](https://langfuse.com/docs/evaluation/experiments/datasets).

권한 metadata를 넣는 것만으로 접근 통제가 생기지는 않는다. 신뢰할 수 있는 사용자 identity에서 권한을 계산하고 검색 요청마다 검사해야 한다. 프롬프트·응답·tool input/output에도 민감 정보가 들어갈 수 있으므로 수집 범위·마스킹·보존 기간을 정한다. 검색 결과를 LLM에 넘긴 뒤 UI에서만 숨기는 방식은 유출 방지 경계가 아니다. [Azure AI Search security filters](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search).

## LLM in Practice: 평가 조건 비교

- **상황:** 두 agent 버전의 점수가 달라졌다.
- **제공 맥락:** 비식별 실험 metadata, dataset·model·prompt·agent·evaluator 버전, runtime config, 표본 수와 실패 사례.
- **예시 prompt:**

```text
Compare these two experiment records.
List changed conditions and missing version metadata.
Separate observed score changes from possible causes.
Do not claim that a model change caused the difference.
Suggest a controlled comparison using the same dataset and evaluator.
```

- **기대 결과:** 바뀐 조건·누락 정보와 통제 비교 계획.
- **오류 가능성:** 점수 차이를 model 성능 차이로 단정하거나 temperature=0을 완전한 결정성으로 오해할 수 있다.
- **검증:** 실제 dataset 항목·설정·trace를 확인하고 같은 조건으로 반복 평가한다. 이 문서에서는 실험을 실행하지 않았다.

## 관련 주제

[온라인 평가](online-evaluation.md) · [거버넌스](governance.md) · [계보와 메타데이터](lineage-metadata.md) · [전체 구조](architecture.md)
