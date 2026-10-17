---
id: prompts-dbt
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# dbt practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/dbt.md) · [All prompts](index.md)

| # | Jump to a situation |
| --- | --- |
| 01 | [Review staging, intermediate, and mart responsibilities](#dbt-01) |
| 02 | [Check ref, source, and environment dependencies](#dbt-02) |
| 03 | [Find gaps between data tests and business rules](#dbt-03) |
| 04 | [Compare snapshot and CDC history needs](#dbt-04) |
| 05 | [Review incremental keys and the first-run contract](#dbt-05) |
| 06 | [Review full-refresh scope after a logic change](#dbt-06) |

## Review staging, intermediate, and mart responsibilities {#dbt-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    Several models repeat the same join and business rules. Review their responsibilities.
    Separate renaming and type cleanup from reusable business logic.
    Assess current layers before suggesting the smallest moves.
    Judge the need for an intermediate layer from actual reuse evidence.
    Return each rule’s location, responsibility, consumers, and reason for any move.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    여러 모델에 같은 join과 업무 규칙이 반복되어 책임을 정리하려고 해.
    Rename·type 정리와 재사용 business logic을 구분해 주세요.
    현재 계층을 먼저 평가한 뒤 최소 이동 후보를 제안해 주세요.
    Intermediate가 꼭 필요한지 실제 재사용 근거로 판단해 주세요.
    Logic별 현재 위치·책임·재사용처·이동 이유 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: actual consumers of repeated logic and each model's grain. Distinguish model SQL from compiled SQL and add line numbers to the diff. The LLM may map layers directly to Bronze/Silver/Gold or split every small model. Require keys, row counts, and business totals to remain unchanged after deduplication.

## Check ref, source, and environment dependencies {#dbt-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Development SQL uses a fixed table name from another environment, hiding a dependency.
    Classify internal models as ref candidates and external inputs as source candidates.
    Review how fixed names affect execution order and lineage.
    Keep ingestion and BI paths outside dbt as scope needing separate evidence.
    Return current relations, intended environments, and dependency declarations by reference.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    개발 SQL이 다른 환경의 고정 table 이름을 참조해 dependency가 빠진다.
    내부 model은 ref, 외부 입력은 source 후보로 분류해 주세요.
    고정 이름이 실행 순서·lineage에 미치는 영향을 검토해 주세요.
    dbt 밖의 수집·BI 경로는 추적 확인이 필요한 범위로 남겨 주세요.
    참조별 현재 relation·의도한 환경·의존성 선언 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: relation resolution by environment and internal/external ownership boundaries. Distinguish model SQL from compiled SQL and add line numbers to the diff. The LLM may turn every table into a ref or treat the dbt graph as full platform lineage. Check successful compilation separately from reading the intended environment.

## Find gaps between data tests and business rules {#dbt-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Basic tests pass, but a mart contains a business state that should not be allowed.
    Separate conditions checked by basic tests from meanings they do not check.
    Propose custom test candidates and counterexamples for business rules.
    List missing evidence connecting test failure to publication blocking.
    Return a mapping of rules, tests, failing samples, and expected outcomes.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    기본 test는 통과하지만 허용되지 않은 업무 상태가 mart에 들어간다.
    기본 test가 확인하는 조건과 확인하지 않는 의미를 구분해 주세요.
    업무 규칙별 custom test 후보와 반례를 제안해 주세요.
    Test 실패와 실제 publish 차단 연결의 누락 근거를 적어 주세요.
    규칙·검사·실패 샘플·기대 결과의 대응표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: agreed business rules and publication policy when tests fail. Distinguish model SQL from compiled SQL and add line numbers to the diff. The LLM may confuse basic test success with correct meaning or automatic publication blocking. Do not mark the work complete while publication can proceed after a failed test.

## Compare snapshot and CDC history needs {#dbt-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Review whether a table with CDC history also needs a dbt snapshot.
    Separate requirements covered by current history from gaps.
    Explain limits on preserving changes between snapshot observations.
    Tie the Type 1 or Type 2 choice to historical analysis needs.
    Return coverage and assumptions for CDC history and snapshots by requirement.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    이미 CDC history가 있는 table에 dbt snapshot을 추가할지 검토 중이야.
    현재 history로 충족되는 요구와 부족한 요구를 분리해 주세요.
    Snapshot 관측 사이 중간 변경의 보존 한계를 설명해 주세요.
    Type 1과 Type 2의 선택을 과거 분석 요구에 연결해 주세요.
    요구별 CDC history·snapshot 충족 여부와 가정 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: historical questions and deletion history that CDC must support. Distinguish model SQL from compiled SQL and add line numbers to the diff. The LLM may assume snapshots capture every change or CDC meets every history need. Do not treat snapshots alone as sufficient for questions needing several changes between observations.

## Review incremental keys and the first-run contract {#dbt-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    A model works incrementally but fails on the first run or with null keys.
    Review SQL paths for the first full run and later runs separately.
    Check whether the key matches the grain and has a real uniqueness test.
    State uncertainty about strategy support and key handling.
    Return expected results for empty targets, existing targets, nulls, and duplicate keys.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Model이 incremental 실행은 되지만 최초 실행 또는 null key에서 실패한다.
    최초 전체 실행과 이후 실행의 SQL 경로를 따로 검토해 주세요.
    Key가 grain에 맞는지와 실제 uniqueness 검사가 있는지 확인해 주세요.
    Strategy 지원과 key 처리의 불확실성을 명시해 주세요.
    빈 대상·기존 대상·null·중복 key별 기대 결과표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: actual adapter strategy and compiled SQL for first and repeated runs. Distinguish model SQL from compiled SQL and add line numbers to the diff. The LLM may assume unique_key runs a uniqueness test or every adapter has the same MERGE behavior. Check input and output uniqueness separately from a unique_key declaration.

## Review full-refresh scope after a logic change {#dbt-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    A changed business formula leaves older rows outside the incremental input unchanged.
    Compare historical rows affected by the new logic with the current processing range.
    Review input availability for full refresh and bounded reprocessing options.
    Assess the current design, then separate facts, assumptions, and missing data.
    Return affected periods, models, recalculation options, and unavailable ranges.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    업무 계산식을 바꿨지만 incremental 입력 밖의 과거 행은 이전 값을 유지한다.
    새 logic이 바꾸는 과거 행과 현재 처리 범위를 비교해 주세요.
    Full refresh와 제한된 재처리 후보의 입력 복원 가능성을 검토해 주세요.
    기존 설계를 평가한 뒤 알려진 사실·가정·자료 부족을 구분해 주세요.
    영향 기간·모델·재계산 후보·불가능한 범위 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the effective period of the logic change and available source ranges. Distinguish model SQL from compiled SQL and add line numbers to the diff. The LLM may assume full refresh restores missing source data or new-row processing changes all historical values. Do not claim full recovery when older source data is unavailable.
