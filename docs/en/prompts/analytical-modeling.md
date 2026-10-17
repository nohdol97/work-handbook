---
id: prompts-analytical-modeling
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Analytical modeling practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

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

**Prompt:**

=== "English"

    ```text {.prompt}
    Review whether agent executions, LLM calls, and user events belong in one analytical table.
    First define the meaning of one row in each candidate table.
    Find where measures at different grains become mixed.
    Do not infer relationships from names alone; list missing evidence.
    Return a table of candidate tables, grains, keys, measures, and dimensions.
    ```

=== "한국어"

    ```text {.prompt}
    Agent 실행·LLM 호출·사용자 event를 한 분석 테이블에 담을지 검토 중이야.
    각 후보 table의 한 행 의미를 먼저 한 문장으로 정의해 주세요.
    서로 다른 grain의 measure가 섞이는 지점을 찾아 주세요.
    필드 이름만으로 관계를 확정하지 말고 누락 근거를 적어 주세요.
    Table·grain·key·measure·dimension 후보 표를 주세요.
    ```

**Key point:** Evidence to check first: the business meaning of one row and relationship cardinality by key. Include small counterexamples whose expected results can be calculated by hand. The LLM may combine grains for convenience or treat execution_id as unique for every event. Require intended row counts for executions with several calls and with no calls.

## Review SCD Type 2 validity joins {#analytical-modeling-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Joining customer region history to facts produces two rows at a validity boundary.
    Separate overlaps and gaps for the same natural key.
    Count matching versions at each fact time.
    Flag unclear requirements about current versus historical attributes.
    Return expected versions, candidate counts, and mismatch reasons for each fact.
    ```

=== "한국어"

    ```text {.prompt}
    고객 region 이력과 fact를 join한 뒤 경계 시점의 행이 두 번 나온다.
    같은 natural key의 중첩·공백 구간을 구분해 주세요.
    Fact 시점에 대응하는 version 수를 계산해 주세요.
    현재 속성과 과거 속성 중 어떤 분석을 원하는지 불명확하면 표시해 주세요.
    Fact별 기대 version·실제 후보 수·불일치 이유 표를 주세요.
    ```

**Key point:** Evidence to check first: whether valid_to is inclusive and the historical analysis time. Include small counterexamples whose expected results can be calculated by hand. The LLM may choose only the newest dimension row or hide overlap with DISTINCT. Require the expected version before, at, and after each boundary.

## Align dashboard error-rate definitions {#analytical-modeling-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Two dashboards show different error rates under the same metric name.
    Check whether execution-level and call-level metrics are mixed.
    Compare populations, periods, and filters in each numerator and denominator.
    Separate definition differences from data-error hypotheses.
    Return a metric-contract comparison and business questions needing agreement.
    ```

=== "한국어"

    ```text {.prompt}
    두 대시보드의 error rate가 다른데 metric 이름은 같다.
    실행 단위와 호출 단위 metric이 섞였는지 검토해 주세요.
    분자와 분모의 대상 집합·기간·필터 차이를 비교해 주세요.
    정의 차이와 데이터 오류 가설을 분리해 주세요.
    Metric 계약 차이표와 합의가 필요한 업무 질문을 주세요.
    ```

**Key point:** Evidence to check first: the business failure definition and denominator population. Include small counterexamples whose expected results can be calculated by hand. The LLM may equate matching names or compare rates with different denominators. Require agreement on zero denominators, retries, and excluded statuses.

## Choose fact types from business questions {#analytical-modeling-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Decide how to model order events, daily state, and time across delivery milestones.
    Compare event, transaction, periodic, and accumulating candidates by requirement.
    State each candidate’s grain and retained history.
    Do not treat these categories as absolute, exclusive product rules.
    Return questions, fact candidates, grains, update methods, and missing information.
    ```

=== "한국어"

    ```text {.prompt}
    주문 사건·일별 상태·배송 단계 소요 시간을 같은 구조로 볼지 결정한다.
    Event·transaction·periodic·accumulating 후보를 요구별로 비교해 주세요.
    각 후보의 한 행 의미와 남기는 이력을 명시해 주세요.
    분류를 절대적·상호 배타적 제품 규칙으로 취급하지 말아 주세요.
    질문·fact 후보·grain·갱신 방식·누락 정보 표를 주세요.
    ```

**Key point:** Evidence to check first: required events, daily states, and milestone times for each question. Include small counterexamples whose expected results can be calculated by hand. The LLM may reconstruct all events from one progress row or mix daily state with events. Hold designs that try to reconstruct event history from current state alone.

## Check conformed-dimension keys and meaning {#analytical-modeling-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Execution and call facts are intended to share one team dimension.
    Check whether same-named team fields share meaning and key rules.
    Review current versus historical membership for each fact.
    Separate definitions that can be shared from meanings still needing agreement.
    Return dimension-link contracts and key mappings for each fact.
    ```

=== "한국어"

    ```text {.prompt}
    실행 fact와 호출 fact가 같은 team dimension을 공유하려 한다.
    이름이 같은 team 필드가 같은 개념과 key 규칙인지 확인해 주세요.
    현재 소속과 당시 소속의 차이를 fact별로 검토해 주세요.
    공유 가능한 정의와 합의되지 않은 의미를 나눠 주세요.
    Fact별 dimension 연결 계약과 key mapping 표를 주세요.
    ```

**Key point:** Evidence to check first: the shared dimension's business meaning and historical membership rules. Include small counterexamples whose expected results can be calculated by hand. The LLM may unify meanings from key names alone or apply current membership to every past fact. Check time-specific membership before merging fields merely named team.

## Review denormalization in a wide table {#analytical-modeling-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    A wide table is proposed to combine orders, items, and customer history for easier queries.
    Assess the current design and locate repeated measures and mixed history.
    Compare simpler queries and fewer joins with update and history costs.
    Do not claim a performance gain without measurement.
    Return each column’s grain, allowed repetition, aggregation limits, and update owner.
    ```

=== "한국어"

    ```text {.prompt}
    조회 편의를 위해 주문·항목·고객 이력을 한 테이블로 합치려 한다.
    기존 설계를 평가하고 반복 measure와 혼합 이력 지점을 찾아 주세요.
    조회 편의·join 감소와 갱신·이력 관리 비용을 비교해 주세요.
    측정 없이 성능 향상을 확정하지 말아 주세요.
    Column별 grain·반복 허용·집계 제약·갱신 책임 표를 주세요.
    ```

**Key point:** Evidence to check first: representative query grains and where repeated measures are allowed. Include small counterexamples whose expected results can be calculated by hand. The LLM may claim one table is always faster or sum amounts from different grains. Require checks of historical accuracy and update cost alongside faster queries.
