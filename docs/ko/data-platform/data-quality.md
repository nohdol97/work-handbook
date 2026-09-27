---
id: data-platform-data-quality
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-11-01
  - DPE-11-02
  - DPE-11-03
  - DPE-11-04
  - DPE-11-05
  - DPE-11-06
  - DPE-11-07
---

# Chapter 11 — Data Quality Engineering

이 문서는 데이터 품질의 개념과 가상 운영 예시를 학습한 Learn 문서다. 실제 시스템 구축이나 장애 대응을 수행했다는 뜻은 아니다. 품질은 “데이터를 믿고 사용할 수 있는가?”라는 질문이며, 서비스가 응답해도 결과가 틀리면 데이터 장애다.

**본문 안내:** 아래 원문 구역은 원래 순서와 형태를 보존한 본문이다. 원문의 단순화된 설명에 대한 정정·적용 조건과 추가 설명은 문서 뒤 보완 구역에서 해당 절 번호와 함께 확인한다.

<!-- SOURCE CORE START -->

## 11.1 Quality Dimensions

### Completeness

필수 데이터가 빠지지 않았는가.

### Uniqueness

중복되면 안 되는 값이 중복되지 않았는가.

### Validity

허용된 형식/범위인가.

### Consistency

다른 데이터와 모순되지 않는가.

### Freshness

제시간에 들어왔는가.

### Accuracy

실제 세계의 값과 맞는가.

### Volume

데이터 양이 정상 범위인가.

AI 예:

```text
fact_llm_call

Completeness
→ model_id NULL?

Uniqueness
→ llm_call_id 중복?

Validity
→ negative latency?

Consistency
→ model_id가 dim_model에 존재?

Freshness
→ 최근 Event 5분 이내?

Accuracy
→ billing과 cost 일치?

Volume
→ 호출량 급증/급감?
```

---

## 11.2 Validation Layers

### Ingestion Validation

- Schema
- Format
- Required Field
- Parsing

### Silver Validation

- Dedup
- Relationships
- Business Rules
- Valid Values

### Gold Validation

- KPI
- Freshness
- Aggregate Consistency
- Expected Volume

핵심:

```text
초기
→ 형식

중간
→ 데이터 논리

최종
→ 비즈니스 결과
```

---

## 11.3 Quarantine Patterns

Invalid Data를 버리지 않고 별도 보관.

```text
Incoming
 ↓
Validation
 ↙      ↘
Valid   Invalid
 ↓        ↓
Silver   Quarantine
```

Quarantine에:

- Raw payload
- Error type
- Error message
- Received time

등을 저장.

문제 수정 후 Reprocessing.

Quarantine이 쌓이기만 하면 안 되며 Volume/Error Reason Monitoring도 필요하다.

---

## 11.4 dbt Tests

Data Quality 관점의 dbt Test:

- not_null
- unique
- relationships
- accepted_values

강점:
- Model/Table 수준 정적 검증

부족할 수 있는 영역:
- Volume anomaly
- Distribution drift
- Freshness anomaly

---

## 11.5 Soda / Great Expectations / Deequ

공통:

> **Data Quality Rule 자동 검사 도구**

### Soda

Rule/check 중심.

### Great Expectations

Expectation 기반 검증.

### Deequ

Spark 환경 대규모 Data Quality 검사에 친화적.

세 도구는 기능이 많이 겹치며 이 세션에서는 각각의 구현보다 범주를 이해하는 것이 목표였다.

---

## 11.6 Data Quality SLOs

SLI:

> 실제 측정값.

SLO:

> 목표 수준.

예:

```text
Freshness < 5 min
Completeness > 99.9%
Duplicate Rate < 0.01%
```

Dataset마다 SLO가 달라야 한다.

실시간 Dashboard와 월간 Report는 필요한 Freshness가 다르다.

---

## 11.7 Incident Handling

흐름:

```text
Detect
 ↓
Contain
 ↓
Fix
 ↓
Reprocess
 ↓
Verify
```

### Detect

SLO 위반 감지.

### Contain

잘못된 Data의 Downstream 전파 차단.

### Fix

Root Cause 수정.

### Reprocess

Backfill / Replay.

### Verify

Quality Check 후 재개.

중요:

> **서비스가 살아 있어도 데이터가 틀리면 Data Incident다.**

---

<!-- SOURCE CORE END -->

## 부록: 기존 보완 설명

위 본문은 제공된 Markdown의 9~11장 중 이 페이지에 해당하는 장을 원문 형식 그대로 보존했다. 아래는 원문과 구분한 기존 설명·주의사항이다.

### 품질 차원과 검증 계층

하나의 정상 지표가 다른 모든 차원을 보장하지 않는다. 형식이 유효하다고 실제 청구 금액까지 정확한 것은 아니다. 5분 freshness는 예시이며 모든 dataset의 기본 목표가 아니다.

앞 검증 계층을 통과했다고 뒤 계층의 검사를 생략하지 않는다.

### Quarantine의 보관과 접근

Raw payload와 오류 메시지도 민감정보를 포함할 수 있다. 보관 범위와 접근 권한은 [거버넌스 정책](governance.md)과 함께 정한다. 이 문서에는 실제 payload가 없다.

### dbt와 품질 도구의 범위

원문의 “정적 검증”은 규칙이 고정되어 있다는 뜻이다. dbt data test는 실제 데이터에 SQL을 실행하며 단순한 코드 정적 분석이 아니다. 사용자 정의 SQL 검사로 비즈니스 규칙도 표현할 수 있다. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)

기본 네 가지 검사만으로 모든 이상 탐지를 해결하지 못한다는 설명이 dbt의 freshness 검사 불가를 뜻하지는 않는다. Source freshness는 별도 기능이다. 통계적 이상 탐지에는 이력과 기준선 설계도 필요하다. [dbt source freshness](https://docs.getdbt.com/docs/deploy/source-freshness)

도구를 적용할 때 확인할 범위:

- Soda: 규칙과 연결된 데이터 source의 지원 범위.
- Great Expectations: 실행 환경과 데이터 연결 방식.
- Deequ: Spark와 해당 library version의 호환성.

제품 설명은 2026-09-24에 공식 문서로 확인한 범위를 유지했다. 이번 편집에서 새로 확인하거나 구현·우열을 시험하지 않았다. [SodaCL v3](https://docs.soda.io/soda-documentation/soda-v3/sodacl-reference/metrics-and-checks), [GX Core](https://docs.greatexpectations.io/docs/core/define_expectations/), [Deequ](https://github.com/awslabs/deequ)

### SLO와 복구 확인

본문의 SLO 수치는 학습용 목표 예시이며 실측 결과나 승인된 운영 기준이 아니다.

운영 SLO에는 시간 기준, 측정 구간, 분모, 대상 dataset을 명시한다.

Job 성공만으로 복구를 종료하지 않는다. 재처리 범위, 중복 가능성, downstream 결과를 확인한다. [데이터 관측성](data-observability.md)은 지속적인 상태 측정을, [lineage](lineage-metadata.md)는 영향 경로 확인을 돕는다.

### 기존 개념도

원문의 text 그림과 별도로 기존 Mermaid 그림을 보존한다.

```mermaid
flowchart TD
    Incoming --> Validation
    Validation -->|Valid| Silver
    Validation -->|Invalid| Quarantine
    Quarantine --> Repair[Fix the cause]
    Repair --> Reprocess
    Reprocess --> Validation
```

## LLM in Practice: 품질 장애의 검사 순서 검토

**상황:** 작업은 성공했으나 가상의 호출 테이블에 중복이 증가했다.

**LLM에 제공할 맥락:** 개인정보를 제거한 스키마, 이벤트 키, 배치 구간, retry/replay 이력, 중복률, 관련 SLO, downstream 목록을 제공한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    작업은 성공했지만 llm_call_id 중복이 늘었습니다.
    스키마·이벤트 키·배치 구간: [비식별 정의]
    retry·replay 이력과 중복률: [측정과 로그]
    SLO와 downstream 데이터셋: [목록]
    [요청]
    재설계를 제안하기 전에 이 데이터 장애를 검토하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    전파 차단 선택지와 다음 확인 순서를 주세요.
    안전한 재처리 범위와 downstream 재개 전 품질 검사를 주세요.
    [검증]
    키 정의·로그·재처리 구간·전후 품질·downstream 집계로 확인하세요.
    가설을 운영 승인으로 취급하거나 실제 조치를 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    The job succeeded, but duplicate llm_call_id values increased.
    Schema, event key, and batch window: [sanitized definitions]
    Retry and replay history and duplicate rate: [measurements and logs]
    SLOs and downstream datasets: [list]
    [Task]
    Review this data incident before proposing a redesign.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give containment options and the next checks.
    Give a safe reprocessing scope and quality checks before downstream use resumes.
    [Checks]
    Check key definitions, logs, replay windows, quality changes, and downstream totals.
    Do not treat hypotheses as approval or execute operational actions.
    ```

**기대 결과:** 원인 가설, 우선 확인할 증거, 전파 차단 선택지, 재처리와 재개 조건을 구분한 점검안이다.

**틀릴 수 있는 부분:** retry와 중복의 상관관계를 원인으로 확정하거나 deduplication 키와 grain을 잘못 가정할 수 있다.

**검증 방법:** 실제 키 정의, 로그, 재처리 구간, 전후 품질 측정값과 downstream 집계를 확인한다. LLM 출력은 가설이며 운영 승인을 대신하지 않는다.

[핸드북 홈](../index.md)

[더 많은 실무 프롬프트](../prompts/data-quality.md)
