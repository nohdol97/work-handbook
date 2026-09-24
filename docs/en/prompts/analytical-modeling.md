---
id: prompts-analytical-modeling
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Analytical modeling practical prompts

These six hypothetical, reusable examples apply the existing concepts. They do not report measured usage frequency, execution results, new studied curriculum, or production experience. Replace [placeholders] with non-secret context and synthetic data. Model output is a draft to validate. These prompts do not authorize production actions.

[Concept guide](../data-platform/analytical-modeling.md) · [All prompts](index.md)

| # | Jump to a situation |
| --- | --- |
| 01 | [Define grain for new analytical tables](#analytical-modeling-01) |
| 02 | [Review SCD Type 2 validity joins](#analytical-modeling-02) |
| 03 | [Align dashboard error-rate definitions](#analytical-modeling-03) |
| 04 | [Choose fact types from business questions](#analytical-modeling-04) |
| 05 | [Check conformed-dimension keys and meaning](#analytical-modeling-05) |
| 06 | [Review denormalization in a wide table](#analytical-modeling-06) |

## Define grain for new analytical tables {#analytical-modeling-01}

**Situation:** Review whether agent executions, LLM calls, and user events belong in one analytical table.

**Context to give the LLM:** Event types and synthetic samples: [executions, calls, and user events] Questions, metrics, and reporting periods: [analysis needs] Keys and relationship cardinality: [synthetic schema]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Event types and synthetic samples: [executions, calls, and user events]
    Questions, metrics, and reporting periods: [analysis needs]
    Keys and relationship cardinality: [synthetic schema]

    [Task]
    First define the meaning of one row in each candidate table.
    Find where measures at different grains become mixed.
    Do not infer relationships from names alone; list missing evidence.

    [Output]
    Return a table of candidate tables, grains, keys, measures, and dimensions.
    Provide expected row counts for several calls and no-call cases.

    [Checks]
    Map synthetic samples to row definitions and check duplicate keys.
    Compare actual analysis needs with each measure’s original aggregation unit.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Event 종류와 가상 샘플: [실행·호출·사용자 event]
    질문·metric·집계 기간: [분석 요구]
    Key와 관계 cardinality: [가상 schema]

    [요청]
    각 후보 table의 한 행 의미를 먼저 한 문장으로 정의해 주세요.
    서로 다른 grain의 measure가 섞이는 지점을 찾아 주세요.
    필드 이름만으로 관계를 확정하지 말고 누락 근거를 적어 주세요.

    [출력]
    Table·grain·key·measure·dimension 후보 표를 주세요.
    여러 호출·호출 없음 사례의 기대 행 수를 주세요.

    [검증]
    가상 샘플을 한 행 정의에 맞춰 배치해 key 중복을 확인해 주세요.
    실제 분석 요구와 measure의 원래 집계 단위를 대조해 주세요.
    ```

**Expected output:** Return a table of candidate tables, grains, keys, measures, and dimensions. Provide expected row counts for several calls and no-call cases.

**What the LLM can get wrong:** The LLM may combine grains for convenience or treat execution_id as unique for every event.

**How to validate:** Map synthetic samples to row definitions and check duplicate keys. Compare actual analysis needs with each measure’s original aggregation unit.

## Review SCD Type 2 validity joins {#analytical-modeling-02}

**Situation:** Joining customer region history to facts produces two rows at a validity boundary.

**Context to give the LLM:** Synthetic natural and surrogate keys and valid_from and valid_to: [samples] Fact times and join SQL: [synthetic data and SQL] End-boundary and open-interval rules: [definitions]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Synthetic natural and surrogate keys and valid_from and valid_to: [samples]
    Fact times and join SQL: [synthetic data and SQL]
    End-boundary and open-interval rules: [definitions]

    [Task]
    Separate overlaps and gaps for the same natural key.
    Count matching versions at each fact time.
    Flag unclear requirements about current versus historical attributes.

    [Output]
    Return expected versions, candidate counts, and mismatch reasons for each fact.
    Provide a minimal join change that preserves the boundary rule.

    [Checks]
    Check synthetic facts before, at, and after the boundary and with no match.
    Validate expected versions against actual interval rules and historical analysis needs.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 natural·surrogate key와 valid_from·valid_to: [샘플]
    Fact 발생 시점과 join SQL: [가상 데이터·SQL]
    유효 구간의 종료 경계·열린 구간 규칙: [정의]

    [요청]
    같은 natural key의 중첩·공백 구간을 구분해 주세요.
    Fact 시점에 대응하는 version 수를 계산해 주세요.
    현재 속성과 과거 속성 중 어떤 분석을 원하는지 불명확하면 표시해 주세요.

    [출력]
    Fact별 기대 version·실제 후보 수·불일치 이유 표를 주세요.
    경계 규칙을 보존하는 최소 join 수정 후보를 주세요.

    [검증]
    경계 직전·정확한 경계·직후·미매칭 가상 fact를 확인해 주세요.
    실제 유효 구간 규칙과 과거 분석 요구로 기대 version을 검증해 주세요.
    ```

**Expected output:** Return expected versions, candidate counts, and mismatch reasons for each fact. Provide a minimal join change that preserves the boundary rule.

**What the LLM can get wrong:** The LLM may choose only the newest dimension row or hide overlap with DISTINCT.

**How to validate:** Check synthetic facts before, at, and after the boundary and with no match. Validate expected versions against actual interval rules and historical analysis needs.

## Align dashboard error-rate definitions {#analytical-modeling-03}

**Situation:** Two dashboards show different error rates under the same metric name.

**Context to give the LLM:** Each SQL, numerator, denominator, and grain: [synthetic definitions] Period, timezone, and status exclusions: [conditions] Zero-denominator handling and business failure definition: [rules]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Each SQL, numerator, denominator, and grain: [synthetic definitions]
    Period, timezone, and status exclusions: [conditions]
    Zero-denominator handling and business failure definition: [rules]

    [Task]
    Check whether execution-level and call-level metrics are mixed.
    Compare populations, periods, and filters in each numerator and denominator.
    Separate definition differences from data-error hypotheses.

    [Output]
    Return a metric-contract comparison and business questions needing agreement.
    Provide a shared definition candidate and synthetic calculations including zero denominators.

    [Checks]
    Manually check both formulas on the same synthetic population.
    Compare agreed business definitions with each SQL and semantic-layer setting.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    각 SQL·분자·분모·grain: [가상 정의]
    기간·timezone·status 제외 조건: [조건]
    분모 0 처리와 업무상 실패 정의: [규칙]

    [요청]
    실행 단위와 호출 단위 metric이 섞였는지 검토해 주세요.
    분자와 분모의 대상 집합·기간·필터 차이를 비교해 주세요.
    정의 차이와 데이터 오류 가설을 분리해 주세요.

    [출력]
    Metric 계약 차이표와 합의가 필요한 업무 질문을 주세요.
    공통 정의 후보와 0 분모 포함 가상 기대 계산을 주세요.

    [검증]
    같은 가상 모집단에서 두 계산식을 손으로 검산해 주세요.
    확정된 업무 정의를 각 SQL·semantic layer 설정과 대조해 주세요.
    ```

**Expected output:** Return a metric-contract comparison and business questions needing agreement. Provide a shared definition candidate and synthetic calculations including zero denominators.

**What the LLM can get wrong:** The LLM may equate matching names or compare rates with different denominators.

**How to validate:** Manually check both formulas on the same synthetic population. Compare agreed business definitions with each SQL and semantic-layer setting.

## Choose fact types from business questions {#analytical-modeling-04}

**Situation:** Decide how to model order events, daily state, and time across delivery milestones.

**Context to give the LLM:** Analysis questions and required time references: [requirements] Order events, daily observations, and milestone times: [synthetic samples] Current schema, keys, and update method: [definitions]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Analysis questions and required time references: [requirements]
    Order events, daily observations, and milestone times: [synthetic samples]
    Current schema, keys, and update method: [definitions]

    [Task]
    Compare event, transaction, periodic, and accumulating candidates by requirement.
    State each candidate’s grain and retained history.
    Do not treat these categories as absolute, exclusive product rules.

    [Output]
    Return questions, fact candidates, grains, update methods, and missing information.
    Show synthetic representations for incomplete delivery and several state changes.

    [Checks]
    Check whether each synthetic representation answers the original question.
    Cross-check retained history and the meaning of milestone times.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    분석 질문과 필요한 시간 기준: [요구]
    주문 event와 일별 관측·단계 시각: [가상 샘플]
    현재 schema·key·변경 방식: [정의]

    [요청]
    Event·transaction·periodic·accumulating 후보를 요구별로 비교해 주세요.
    각 후보의 한 행 의미와 남기는 이력을 명시해 주세요.
    분류를 절대적·상호 배타적 제품 규칙으로 취급하지 말아 주세요.

    [출력]
    질문·fact 후보·grain·갱신 방식·누락 정보 표를 주세요.
    미완료 배송과 여러 상태 변경의 가상 표현을 주세요.

    [검증]
    각 가상 표현에서 원래 질문에 답할 수 있는지 확인해 주세요.
    실제 보존 이력과 milestone 시각의 의미를 대조해 주세요.
    ```

**Expected output:** Return questions, fact candidates, grains, update methods, and missing information. Show synthetic representations for incomplete delivery and several state changes.

**What the LLM can get wrong:** The LLM may reconstruct all events from one progress row or mix daily state with events.

**How to validate:** Check whether each synthetic representation answers the original question. Cross-check retained history and the meaning of milestone times.

## Check conformed-dimension keys and meaning {#analytical-modeling-05}

**Situation:** Execution and call facts are intended to share one team dimension.

**Context to give the LLM:** Each fact’s grain and business meaning of team: [definitions] Natural and surrogate key mapping and history policy: [synthetic schema] Unmatched and changed-membership samples and analysis times: [samples and needs]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Each fact’s grain and business meaning of team: [definitions]
    Natural and surrogate key mapping and history policy: [synthetic schema]
    Unmatched and changed-membership samples and analysis times: [samples and needs]

    [Task]
    Check whether same-named team fields share meaning and key rules.
    Review current versus historical membership for each fact.
    Separate definitions that can be shared from meanings still needing agreement.

    [Output]
    Return dimension-link contracts and key mappings for each fact.
    List unmatched and history-boundary cases that affect shared metrics.

    [Checks]
    Check expected dimension versions for facts before and after a synthetic membership change.
    Compare meaning, key mappings, and history rules with each fact owner’s requirements.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Fact별 grain과 team의 업무 의미: [정의]
    Natural·surrogate key mapping과 이력 정책: [가상 schema]
    미매칭·소속 변경 샘플과 분석 시점: [샘플·요구]

    [요청]
    이름이 같은 team 필드가 같은 개념과 key 규칙인지 확인해 주세요.
    현재 소속과 당시 소속의 차이를 fact별로 검토해 주세요.
    공유 가능한 정의와 합의되지 않은 의미를 나눠 주세요.

    [출력]
    Fact별 dimension 연결 계약과 key mapping 표를 주세요.
    공통 metric에 영향을 주는 미매칭·이력 경계 사례를 주세요.

    [검증]
    가상 소속 변경 전후 fact가 기대 version에 연결되는지 확인해 주세요.
    실제 업무 의미·key mapping·이력 규칙을 각 fact 소유자 기준과 대조해 주세요.
    ```

**Expected output:** Return dimension-link contracts and key mappings for each fact. List unmatched and history-boundary cases that affect shared metrics.

**What the LLM can get wrong:** The LLM may unify meanings from key names alone or apply current membership to every past fact.

**How to validate:** Check expected dimension versions for facts before and after a synthetic membership change. Compare meaning, key mappings, and history rules with each fact owner’s requirements.

## Review denormalization in a wide table {#analytical-modeling-06}

**Situation:** A wide table is proposed to combine orders, items, and customer history for easier queries.

**Context to give the LLM:** Candidate columns, source grains, and update intervals: [design] Typical queries and required historical attributes: [synthetic SQL and needs] Join cardinality and maintenance constraints: [definitions]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Candidate columns, source grains, and update intervals: [design]
    Typical queries and required historical attributes: [synthetic SQL and needs]
    Join cardinality and maintenance constraints: [definitions]

    [Task]
    Assess the current design and locate repeated measures and mixed history.
    Compare simpler queries and fewer joins with update and history costs.
    Do not claim a performance gain without measurement.

    [Output]
    Return each column’s grain, allowed repetition, aggregation limits, and update owner.
    Propose boundaries to retain and a small comparison plan.

    [Checks]
    Check totals and past attributes with synthetic multi-item and attribute-change data.
    Validate design assumptions with actual query plans and maintenance requirements.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    후보 column·원본 grain·갱신 주기: [설계]
    대표 조회와 필요한 과거 속성: [가상 SQL·요구]
    Join cardinality와 유지보수 제약: [정의]

    [요청]
    기존 설계를 평가하고 반복 measure와 혼합 이력 지점을 찾아 주세요.
    조회 편의·join 감소와 갱신·이력 관리 비용을 비교해 주세요.
    측정 없이 성능 향상을 확정하지 말아 주세요.

    [출력]
    Column별 grain·반복 허용·집계 제약·갱신 책임 표를 주세요.
    유지할 분리 경계와 작은 비교 검증 계획을 주세요.

    [검증]
    여러 항목·속성 변경 가상 데이터로 합계와 과거 속성을 확인해 주세요.
    실제 query plan과 유지보수 요구로 설계 가정을 검증해 주세요.
    ```

**Expected output:** Return each column’s grain, allowed repetition, aggregation limits, and update owner. Propose boundaries to retain and a small comparison plan.

**What the LLM can get wrong:** The LLM may claim one table is always faster or sum amounts from different grains.

**How to validate:** Check totals and past attributes with synthetic multi-item and attribute-change data. Validate design assumptions with actual query plans and maintenance requirements.
