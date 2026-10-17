---
id: data-platform-ai-ready-data
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
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

# Chapter 15 — AI-Ready Data

원문의 Chapter 15를 개념별로 정리했다. `studied`는 개념 학습을 뜻하며 실제 구축·운영 또는 실행 검증을 뜻하지 않는다. 예시의 버전과 숫자는 설명용이다.

<!-- SOURCE CORE START -->

## 15.1 What Makes Data AI-Ready

AI-ready 데이터는 특정 파일 형식이 아니라 AI에 쓰기 전에 확인할 상태다. 요리 재료에 이름표만 있어도 원산지·신선도·사용 가능 여부를 모르면 바로 쓰기 어려운 것과 같다. 데이터의 품질·최신성·버전·발견 가능성·권한을 함께 확인해야 결과를 믿고 다시 평가할 수 있다.

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

품질·카탈로그·권한 같은 기존 데이터 플랫폼 기능이 AI 활용의 출발점이다.

---

## 15.2 AI Telemetry Model

Telemetry(실행 관찰 기록)는 AI 요청에서 prompt, model, tool, 응답, 비용, 피드백이 어떻게 이어졌는지 남기는 정보다. 예를 들어 답이 틀렸을 때 trace ID로 한 실행의 검색 결과와 tool 호출을 묶어 봐야 검색 문제인지 생성 문제인지 좁힐 수 있다. 수집할 민감정보와 보관 기간도 함께 정한다.

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

무엇을 요청했고 무엇을 답했는지 남겨 평가와 개선에 쓴다.

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

요청과 단계별 이벤트를 ID로 연결해 한 실행의 흐름을 따라간다.

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

Langfuse는 trace·observation·score 같은 실행·평가 기록을 다루는 도구의 예다. Trace는 한 요청의 흐름, observation은 그 안의 단계, session은 관련 trace의 묶음이다. 이 도구의 기록을 장기 분석용 테이블과 연결할 수 있지만, 그림의 화살표만으로 자동 수집·동기화가 보장되지는 않는다.

세션 중 질문:

> Langfuse를 쓰면 되겠다.

맞다.

Langfuse는 AI 실행 기록과 평가를 다루는 여러 기능을 제공한다.

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

권장 개념 구조:

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

Langfuse만으로 장기 데이터 통합 분석과 전체 거버넌스를 해결한다고 가정하지 않는다.

---

## 15.3 Dataset Versioning

Dataset version(데이터셋 버전)은 어떤 평가 항목과 정답·기준을 사용했는지 묶어 식별한다. 시험지가 달라지면 점수를 그대로 비교하기 어렵듯, `eval_v1`과 `eval_v2`의 점수도 사례 구성이 다를 수 있다.

평가 데이터셋은 실패 사례나 정답이 추가·수정되면서 바뀐다.

예:

```text
eval_v1
→ 1,000 cases

eval_v2
→ 1,500 cases
→ hard cases 추가
→ 정답 수정
```

서로 다른 평가 데이터셋 버전의 모델 점수를 바로 비교하면 사례 난이도 차이가 섞일 수 있다.

함께 기록:

- dataset_version
- model_version
- prompt_version
- agent_version
- evaluator_version
- score

Iceberg snapshot은 테이블 파일 상태이고, 평가 데이터셋 버전은 어떤 사례를 평가에 썼는지 나타낸다.

```text
Iceberg Snapshot
→ 물리적 Table 상태 버전

Dataset Version
→ AI/업무 관점의 논리적 Dataset 버전
```

---

## 15.4 Reproducibility

과거 점수 차이를 조사하려면 당시 입력과 설정을 다시 찾을 수 있어야 한다. 같은 model 이름만 남기면 prompt나 평가자 버전의 차이를 놓친다. 따라서 아래 버전 묶음과 runtime 설정을 함께 기록한다. 생성 모델의 확률적 성질 때문에 조건을 복원해도 문장이 항상 똑같이 나오지는 않는다.

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

Lineage와 재현성이 답하는 질문은 다르다:

```text
Lineage
→ 어디서 만들어졌나?

Reproducibility
→ 동일한 실험 조건을 다시 구성할 수 있나?
```

LLM은 같은 조건에서도 다른 표현을 만들 수 있다. 따라서 재현성의 핵심은 문장까지 똑같이 만드는 것이 아니라 **입력과 설정을 다시 구성하는 것**이다.

---

## 15.5 Evaluation Dataset Construction

Evaluation dataset(평가 데이터셋)은 prompt·model·agent의 변경을 같은 사례로 반복 점검할 때 쓴다. 시험지를 매번 바꾸면 학생의 실력이 달라진 건지 문제 난도가 달라진 건지 알기 어려운 것과 같다. 실제 실패를 고친 뒤 그 사례를 회귀(regression) 사례로 추가하면 다음 릴리스에서 같은 문제가 되살아나는지 볼 수 있다.

Evaluation Dataset:

> **Model/Prompt/Agent 품질을 반복적으로 평가하는 Test Dataset**

좋은 Source:

- Production Trace
- User Feedback
- 실제 Failure
- Edge Case
- Hard Case

성공 사례만 모으면 실제 실패를 다시 발견하기 어렵다.

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

정답 문장 하나가 없어도 기대 행동이나 평가 기준표(rubric)로 검사할 수 있다.

예:

```text
올바른 Tool을 호출해야 함
권한 없는 정보 노출 금지
특정 Citation 필요
```

---

## 15.6 Embedding Data

Embedding(임베딩)은 문서 조각의 의미를 숫자 벡터로 표현해 비슷한 내용을 검색하도록 돕는다. RAG(Retrieval-Augmented Generation)는 검색한 자료를 답변 생성의 맥락으로 쓰는 방식이다.

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

숫자 벡터만 남기면 원문과 버전을 추적할 수 없으므로 함께 관리해야 한다.

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

임베딩 모델이 바뀌면 벡터의 위치와 검색 결과가 달라질 수 있으므로 모델 버전을 기록한다.

문서를 자르는 방법이 바뀌어도 검색되는 조각이 달라질 수 있다.

---

## 15.7 Retrieval Metadata

Retrieval metadata(검색 메타데이터)는 어떤 문서·조각·버전을 가져왔는지 설명한다. 검색 점수는 관련성 신호이지 열람 허가가 아니다. 사내 문서를 사용할 때는 신뢰할 수 있는 사용자 권한으로 검색 단계에서 허용된 조각만 고르고, 뒤늦게 화면에서 숨기는 방식에 기대지 않는다.

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

Provenance(출처·생성 이력)는 원문에서 문서 조각, 임베딩, 검색, 응답까지 근거의 경로를 설명한다. Lineage가 데이터 이동과 변환을 추적한다면 provenance는 AI 결과의 근거까지 넓혀 볼 수 있다. 출처 문서를 삭제하거나 사용을 중단할 때 어떤 파생 결과를 검토할지 찾는 데 유용하다.

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

거버넌스 정책으로 원본 사용을 중단하거나 삭제할 때 연결된 조각·임베딩·응답을 찾는 데 도움이 된다.

---

## 15.9 Feature / Label Freshness

Feature는 예측에 넣는 값이고 label은 나중에 확인한 정답이다. 예를 들어 최근 30일 사용량으로 다음 7일의 탈퇴를 예측하면 사용량은 feature, 실제 탈퇴 여부는 label이다. 정답이 확정되기 전에 학습·평가에 넣으면 결과가 왜곡될 수 있으므로 각각의 생성 시각과 사용 시점을 구분한다.

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

아직 결과가 확정되지 않은 label을 학습이나 평가에 넣으면 정답을 잘못 기록할 수 있다.

LLM/Agent에서도 유사:

```text
Feature-like
→ 최신 Context / Tool State

Label-like
→ Human Feedback / Judge Score
```

---

---

<!-- SOURCE CORE END -->

## 관련 주제

[온라인 평가](ai-evaluation.md#161-online-evaluation-events) · [거버넌스](governance.md) · [계보와 메타데이터](lineage-metadata.md) · [전체 구조](architecture.md)

[더 많은 실무 프롬프트](../prompts/ai-ready-data.md)

## 이 장의 핵심

- AI에 쓰는 데이터는 품질·신선도·버전·발견 가능성·권한을 함께 갖춰야 한다.
- Trace와 데이터셋 버전을 연결해야 평가 차이의 조건을 다시 확인할 수 있다.
- Embedding은 검색을 돕지만 접근을 허용하지 않는다. 검색 권한과 출처 확인은 별도 단계다.

## LLM in Practice: 평가 조건 비교

- **예시 prompt:**

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    두 agent 버전의 점수가 달라졌다.
    두 실험을 비교하고 바뀐 조건과 누락 버전 metadata를 찾으세요.
    관측된 점수 변화와 가능한 원인을 구분하세요.
    model 변경이 차이의 원인이라고 단정하지 마세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Scores differ between two agent versions.
    Compare the experiments and list changed conditions and missing version metadata.
    Separate observed score changes from possible causes.
    Do not claim that a model change caused the difference.
    Review the material; do not apply changes.
    ```

**핵심 사항:** 바뀐 조건·누락 정보와 통제 비교 계획. 점수 차이를 model 성능 차이로 단정하거나 temperature=0을 완전한 결정성으로 오해할 수 있다. 실제 dataset 항목·설정·trace를 확인하고 같은 조건으로 반복 평가한다. 이 문서에서는 실험을 실행하지 않았다.

## 원문 적용 시 보완 {#source-notes}

### 15.2A Langfuse 데이터 모델

Trace는 요청·작업의 논리적 묶음, observation은 LLM·tool·retrieval 같은 개별 단계, session은 여러 trace를 묶는 단위다. 실제 저장 구현을 이 개념 그림에서 추론하지 않는다. [Langfuse data model](https://langfuse.com/docs/observability/data-model).

### 15.3~15.4 Dataset version 범위

Langfuse dataset item 변경에는 시각 기반 버전이 생기지만 dataset schema 변경은 같은 버전 관리 범위가 아니다. 실험을 재구성하려면 입력 버전 외에 schema와 평가 설정도 보존한다. [Langfuse datasets](https://langfuse.com/docs/evaluation/experiments/datasets).

### 15.2·15.7 수집과 권한 통제

권한 metadata를 넣는 것만으로 접근 통제가 생기지는 않는다. 신뢰할 수 있는 사용자 identity에서 권한을 계산하고 검색 요청마다 검사해야 한다. 프롬프트·응답·tool input/output에도 민감 정보가 들어갈 수 있으므로 수집 범위·마스킹·보존 기간을 정한다. 검색 결과를 LLM에 넘긴 뒤 UI에서만 숨기는 방식은 유출 방지 경계가 아니다. [Azure AI Search security filters](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search).

### 15.2A 수집 범위와 15.3 snapshot 설명

Langfuse의 실제 수집 범위는 계측과 연동에 달려 있다. 원문 그림은 학습용 개념 구조이며 검증된 연동 구현이 아니다.

15.3의 “물리적 Table 상태 버전”은 table metadata가 참조하는 파일 집합의 일관된 상태로 구체화해 이해한다. Iceberg snapshot과 AI/업무 dataset version은 같은 식별자나 같은 경계가 아니다.
