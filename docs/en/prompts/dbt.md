---
id: prompts-dbt
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# dbt practical prompts

These six hypothetical, reusable examples apply the existing concepts. They do not report measured usage frequency, execution results, new studied curriculum, or production experience. Replace [placeholders] with non-secret context and synthetic data. Model output is a draft to validate. These prompts do not authorize production actions.

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

**Situation:** Several models repeat the same join and business rules. Review their responsibilities.

**Context to give the LLM:** SQL and input and output grain by model: [synthetic code and definitions] Repeated logic and consuming marts: [list] Source cleanup rules and final metric definitions: [rules]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    SQL and input and output grain by model: [synthetic code and definitions]
    Repeated logic and consuming marts: [list]
    Source cleanup rules and final metric definitions: [rules]

    [Task]
    Separate renaming and type cleanup from reusable business logic.
    Assess current layers before suggesting the smallest moves.
    Judge the need for an intermediate layer from actual reuse evidence.

    [Output]
    Return each rule’s location, responsibility, consumers, and reason for any move.
    List grains, keys, and metrics that must stay the same.

    [Checks]
    Check the repeated logic in actual SQL and ref dependencies.
    Compare keys, row counts, and business totals on synthetic input before and after changes.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Model별 SQL·입출력 grain: [가상 코드·정의]
    반복 logic과 사용 mart: [목록]
    Source 정리 규칙과 최종 metric 정의: [규칙]

    [요청]
    Rename·type 정리와 재사용 business logic을 구분해 주세요.
    현재 계층을 먼저 평가한 뒤 최소 이동 후보를 제안해 주세요.
    Intermediate가 꼭 필요한지 실제 재사용 근거로 판단해 주세요.

    [출력]
    Logic별 현재 위치·책임·재사용처·이동 이유 표를 주세요.
    변경 전후 동일해야 할 grain·key·metric 목록을 주세요.

    [검증]
    실제 SQL과 ref 의존성에서 반복 범위를 확인해 주세요.
    가상 입력에서 변경 전후 key·행 수·업무 합계를 비교해 주세요.
    ```

**Expected output:** Return each rule’s location, responsibility, consumers, and reason for any move. List grains, keys, and metrics that must stay the same.

**What the LLM can get wrong:** The LLM may map layers directly to Bronze/Silver/Gold or split every small model.

**How to validate:** Check the repeated logic in actual SQL and ref dependencies. Compare keys, row counts, and business totals on synthetic input before and after changes.

## Check ref, source, and environment dependencies {#dbt-02}

**Situation:** Development SQL uses a fixed table name from another environment, hiding a dependency.

**Context to give the LLM:** Model SQL and fixed relation references: [synthetic code] Internal dbt models and external sources: [list] Relation mapping by environment and current DAG: [synthetic settings and graph]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Model SQL and fixed relation references: [synthetic code]
    Internal dbt models and external sources: [list]
    Relation mapping by environment and current DAG: [synthetic settings and graph]

    [Task]
    Classify internal models as ref candidates and external inputs as source candidates.
    Review how fixed names affect execution order and lineage.
    Keep ingestion and BI paths outside dbt as scope needing separate evidence.

    [Output]
    Return current relations, intended environments, and dependency declarations by reference.
    Provide a minimal SQL draft and missing graph evidence.

    [Checks]
    Check that compiled SQL in each environment uses the intended relation.
    Compare the actual graph and external dependency list separately.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Model SQL과 고정 relation 참조: [가상 코드]
    dbt 내부 model·외부 source 분류: [목록]
    환경별 relation 해석과 현재 DAG: [가상 설정·graph]

    [요청]
    내부 model은 ref, 외부 입력은 source 후보로 분류해 주세요.
    고정 이름이 실행 순서·lineage에 미치는 영향을 검토해 주세요.
    dbt 밖의 수집·BI 경로는 추적 확인이 필요한 범위로 남겨 주세요.

    [출력]
    참조별 현재 relation·의도한 환경·의존성 선언 표를 주세요.
    최소 수정 SQL 초안과 누락된 graph 근거를 주세요.

    [검증]
    각 환경의 compiled SQL이 의도한 relation을 참조하는지 확인해 주세요.
    실제 graph와 외부 의존성 목록을 나누어 대조해 주세요.
    ```

**Expected output:** Return current relations, intended environments, and dependency declarations by reference. Provide a minimal SQL draft and missing graph evidence.

**What the LLM can get wrong:** The LLM may turn every table into a ref or treat the dbt graph as full platform lineage.

**How to validate:** Check that compiled SQL in each environment uses the intended relation. Compare the actual graph and external dependency list separately.

## Find gaps between data tests and business rules {#dbt-03}

**Situation:** Basic tests pass, but a mart contains a business state that should not be allowed.

**Context to give the LLM:** Model grain, keys, and states: [schema and business rules] Current not_null, unique, relationships, and accepted_values tests: [definitions] Synthetic invalid rows and expected handling: [samples and policy]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Model grain, keys, and states: [schema and business rules]
    Current not_null, unique, relationships, and accepted_values tests: [definitions]
    Synthetic invalid rows and expected handling: [samples and policy]

    [Task]
    Separate conditions checked by basic tests from meanings they do not check.
    Propose custom test candidates and counterexamples for business rules.
    List missing evidence connecting test failure to publication blocking.

    [Output]
    Return a mapping of rules, tests, failing samples, and expected outcomes.
    State which quality properties remain unproven after tests pass.

    [Checks]
    Check that valid and invalid synthetic rows produce the expected test outcomes.
    Check how actual orchestration connects test results to the quality gate.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Model grain·key·상태 정의: [schema·업무 규칙]
    현재 not_null·unique·relationships·accepted_values: [정의]
    가상 오류 행과 기대 처리: [샘플·정책]

    [요청]
    기본 test가 확인하는 조건과 확인하지 않는 의미를 구분해 주세요.
    업무 규칙별 custom test 후보와 반례를 제안해 주세요.
    Test 실패와 실제 publish 차단 연결의 누락 근거를 적어 주세요.

    [출력]
    규칙·검사·실패 샘플·기대 결과의 대응표를 주세요.
    통과해도 보장할 수 없는 품질 범위를 명시해 주세요.

    [검증]
    정상·오류 가상 행이 각각 통과·실패하는지 확인해 주세요.
    실제 orchestration의 품질 gate와 test 결과 연결을 확인해 주세요.
    ```

**Expected output:** Return a mapping of rules, tests, failing samples, and expected outcomes. State which quality properties remain unproven after tests pass.

**What the LLM can get wrong:** The LLM may confuse basic test success with correct meaning or automatic publication blocking.

**How to validate:** Check that valid and invalid synthetic rows produce the expected test outcomes. Check how actual orchestration connects test results to the quality gate.

## Compare snapshot and CDC history needs {#dbt-04}

**Situation:** Review whether a table with CDC history also needs a dbt snapshot.

**Context to give the LLM:** Current history coverage, keys, and delete handling: [definitions] Required attribute history and analysis times: [requirements] Snapshot interval and change-detection rules: [proposal]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Current history coverage, keys, and delete handling: [definitions]
    Required attribute history and analysis times: [requirements]
    Snapshot interval and change-detection rules: [proposal]

    [Task]
    Separate requirements covered by current history from gaps.
    Explain limits on preserving changes between snapshot observations.
    Tie the Type 1 or Type 2 choice to historical analysis needs.

    [Output]
    Return coverage and assumptions for CDC history and snapshots by requirement.
    List overlapping responsibilities and a change timeline to check.

    [Checks]
    Compare results for an attribute that changes several times between two snapshots.
    Compare actual history and version-specific snapshot behavior with requirements.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    현재 history의 보존 범위·key·삭제 처리: [정의]
    필요한 속성 이력과 분석 시점: [요구]
    Snapshot 주기·변경 감지 기준: [제안]

    [요청]
    현재 history로 충족되는 요구와 부족한 요구를 분리해 주세요.
    Snapshot 관측 사이 중간 변경의 보존 한계를 설명해 주세요.
    Type 1과 Type 2의 선택을 과거 분석 요구에 연결해 주세요.

    [출력]
    요구별 CDC history·snapshot 충족 여부와 가정 표를 주세요.
    추가 snapshot의 중복 책임과 검증할 변경 타임라인을 주세요.

    [검증]
    두 snapshot 사이 여러 번 바뀌는 가상 속성으로 결과를 대조해 주세요.
    실제 history 내용과 버전별 snapshot 동작을 요구에 대조해 주세요.
    ```

**Expected output:** Return coverage and assumptions for CDC history and snapshots by requirement. List overlapping responsibilities and a change timeline to check.

**What the LLM can get wrong:** The LLM may assume snapshots capture every change or CDC meets every history need.

**How to validate:** Compare results for an attribute that changes several times between two snapshots. Compare actual history and version-specific snapshot behavior with requirements.

## Review incremental keys and the first-run contract {#dbt-05}

**Situation:** A model works incrementally but fails on the first run or with null keys.

**Context to give the LLM:** Model SQL and incremental branches: [synthetic code] Grain, unique_key, and duplicate or null input: [definitions and samples] Adapter and engine versions and strategy: [settings]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Model SQL and incremental branches: [synthetic code]
    Grain, unique_key, and duplicate or null input: [definitions and samples]
    Adapter and engine versions and strategy: [settings]

    [Task]
    Review SQL paths for the first full run and later runs separately.
    Check whether the key matches the grain and has a real uniqueness test.
    State uncertainty about strategy support and key handling.

    [Output]
    Return expected results for empty targets, existing targets, nulls, and duplicate keys.
    Provide minimal change candidates and required compiled SQL evidence.

    [Checks]
    Compare compiled SQL for first and repeated runs with official adapter documentation.
    Check repeated results for fixed synthetic input and detection of null and duplicate keys.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Model SQL과 incremental 분기: [가상 코드]
    Grain·unique_key·중복/null 가상 입력: [정의·샘플]
    Adapter·engine 버전과 strategy: [설정]

    [요청]
    최초 전체 실행과 이후 실행의 SQL 경로를 따로 검토해 주세요.
    Key가 grain에 맞는지와 실제 uniqueness 검사가 있는지 확인해 주세요.
    Strategy 지원과 key 처리의 불확실성을 명시해 주세요.

    [출력]
    빈 대상·기존 대상·null·중복 key별 기대 결과표를 주세요.
    최소 수정 후보와 필요한 compiled SQL 근거를 주세요.

    [검증]
    최초·반복 실행의 compiled SQL을 공식 adapter 문서와 대조해 주세요.
    동일 가상 입력의 반복 결과와 null·중복 key 검출을 확인해 주세요.
    ```

**Expected output:** Return expected results for empty targets, existing targets, nulls, and duplicate keys. Provide minimal change candidates and required compiled SQL evidence.

**What the LLM can get wrong:** The LLM may assume unique_key runs a uniqueness test or every adapter has the same MERGE behavior.

**How to validate:** Compare compiled SQL for first and repeated runs with official adapter documentation. Check repeated results for fixed synthetic input and detection of null and duplicate keys.

## Review full-refresh scope after a logic change {#dbt-06}

**Situation:** A changed business formula leaves older rows outside the incremental input unchanged.

**Context to give the LLM:** Old and new SQL and the change period: [synthetic code and interval] Incremental filter and source retention: [settings] Downstream marts, metric dependencies, and output grain: [list]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Old and new SQL and the change period: [synthetic code and interval]
    Incremental filter and source retention: [settings]
    Downstream marts, metric dependencies, and output grain: [list]

    [Task]
    Compare historical rows affected by the new logic with the current processing range.
    Review input availability for full refresh and bounded reprocessing options.
    Assess the current design, then separate facts, assumptions, and missing data.

    [Output]
    Return affected periods, models, recalculation options, and unavailable ranges.
    Provide metric comparisons and acceptance checks before publication.

    [Checks]
    Cross-check actual source availability and model dependencies.
    Check expected differences between formulas on one small fixed past interval.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    이전·새 SQL과 변경 적용 기간: [가상 코드·기간]
    Incremental filter·source 보존 범위: [설정]
    Downstream mart·metric 의존성과 출력 grain: [목록]

    [요청]
    새 logic이 바꾸는 과거 행과 현재 처리 범위를 비교해 주세요.
    Full refresh와 제한된 재처리 후보의 입력 복원 가능성을 검토해 주세요.
    기존 설계를 평가한 뒤 알려진 사실·가정·자료 부족을 구분해 주세요.

    [출력]
    영향 기간·모델·재계산 후보·불가능한 범위 표를 주세요.
    변경 전후 metric 비교와 publish 전 확인 기준을 주세요.

    [검증]
    실제 source 가용 구간과 모델 의존성을 대조해 주세요.
    작은 고정 과거 구간에서 두 계산식의 기대 차이를 확인해 주세요.
    ```

**Expected output:** Return affected periods, models, recalculation options, and unavailable ranges. Provide metric comparisons and acceptance checks before publication.

**What the LLM can get wrong:** The LLM may assume full refresh restores missing source data or new-row processing changes all historical values.

**How to validate:** Cross-check actual source availability and model dependencies. Check expected differences between formulas on one small fixed past interval.
