---
id: prompts-dbt
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# dbt 실무 프롬프트

기존 개념을 응용해 작성한 가상의 재사용 예시 6개다. 실제 업무 빈도나 실행 성능을 측정한 결과가 아니며, 새 학습 과정이나 실제 운영 경험으로 기록하지 않는다. [대괄호]를 비밀값 없는 맥락과 가상 데이터로 채운다. 모델의 제안은 검증할 작업 초안이다. 실제 production 실행 권한을 부여하지 않는다.

[개념 문서](../data-platform/dbt.md) · [전체 프롬프트 모음](index.md)

| # | 상황 바로 가기 |
| --- | --- |
| 01 | [Staging·intermediate·mart 책임 정리](#dbt-01) |
| 02 | [ref·source 누락과 환경 의존성 점검](#dbt-02) |
| 03 | [품질 test와 업무 규칙의 빈틈 찾기](#dbt-03) |
| 04 | [Snapshot과 CDC 이력의 역할 비교](#dbt-04) |
| 05 | [Incremental key와 최초 실행 계약](#dbt-05) |
| 06 | [Logic 변경 후 full refresh 범위 검토](#dbt-06) |

## Staging·intermediate·mart 책임 정리 {#dbt-01}

**상황:** 여러 모델에 같은 join과 업무 규칙이 반복되어 책임을 정리한다.

**LLM에 제공할 맥락:** Model별 SQL·입출력 grain: [가상 코드·정의] 반복 logic과 사용 mart: [목록] Source 정리 규칙과 최종 metric 정의: [규칙]

**예시 프롬프트**

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

**기대 결과:** Logic별 현재 위치·책임·재사용처·이동 이유 표를 주세요. 변경 전후 동일해야 할 grain·key·metric 목록을 주세요.

**LLM이 틀릴 수 있는 부분:** 계층 이름을 Bronze/Silver/Gold와 일대일로 맞추거나 작은 모델도 무조건 분리할 수 있다.

**검증 방법:** 실제 SQL과 ref 의존성에서 반복 범위를 확인해 주세요. 가상 입력에서 변경 전후 key·행 수·업무 합계를 비교해 주세요.

## ref·source 누락과 환경 의존성 점검 {#dbt-02}

**상황:** 개발 SQL이 다른 환경의 고정 table 이름을 참조해 dependency가 빠진다.

**LLM에 제공할 맥락:** Model SQL과 고정 relation 참조: [가상 코드] dbt 내부 model·외부 source 분류: [목록] 환경별 relation 해석과 현재 DAG: [가상 설정·graph]

**예시 프롬프트**

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

**기대 결과:** 참조별 현재 relation·의도한 환경·의존성 선언 표를 주세요. 최소 수정 SQL 초안과 누락된 graph 근거를 주세요.

**LLM이 틀릴 수 있는 부분:** 모든 table을 ref로 바꾸거나 dbt graph가 플랫폼 전체 lineage라고 단정할 수 있다.

**검증 방법:** 각 환경의 compiled SQL이 의도한 relation을 참조하는지 확인해 주세요. 실제 graph와 외부 의존성 목록을 나누어 대조해 주세요.

## 품질 test와 업무 규칙의 빈틈 찾기 {#dbt-03}

**상황:** 기본 test는 통과하지만 허용되지 않은 업무 상태가 mart에 들어간다.

**LLM에 제공할 맥락:** Model grain·key·상태 정의: [schema·업무 규칙] 현재 not_null·unique·relationships·accepted_values: [정의] 가상 오류 행과 기대 처리: [샘플·정책]

**예시 프롬프트**

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

**기대 결과:** 규칙·검사·실패 샘플·기대 결과의 대응표를 주세요. 통과해도 보장할 수 없는 품질 범위를 명시해 주세요.

**LLM이 틀릴 수 있는 부분:** 기본 test 통과를 데이터 의미의 정확성이나 자동 publish 차단과 혼동할 수 있다.

**검증 방법:** 정상·오류 가상 행이 각각 통과·실패하는지 확인해 주세요. 실제 orchestration의 품질 gate와 test 결과 연결을 확인해 주세요.

## Snapshot과 CDC 이력의 역할 비교 {#dbt-04}

**상황:** 이미 CDC history가 있는 table에 dbt snapshot을 추가할지 검토한다.

**LLM에 제공할 맥락:** 현재 history의 보존 범위·key·삭제 처리: [정의] 필요한 속성 이력과 분석 시점: [요구] Snapshot 주기·변경 감지 기준: [제안]

**예시 프롬프트**

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

**기대 결과:** 요구별 CDC history·snapshot 충족 여부와 가정 표를 주세요. 추가 snapshot의 중복 책임과 검증할 변경 타임라인을 주세요.

**LLM이 틀릴 수 있는 부분:** Snapshot이 모든 중간 변경을 포착하거나 CDC가 있으면 모든 이력 요구가 충족된다고 볼 수 있다.

**검증 방법:** 두 snapshot 사이 여러 번 바뀌는 가상 속성으로 결과를 대조해 주세요. 실제 history 내용과 버전별 snapshot 동작을 요구에 대조해 주세요.

## Incremental key와 최초 실행 계약 {#dbt-05}

**상황:** Model이 incremental 실행은 되지만 최초 실행 또는 null key에서 실패한다.

**LLM에 제공할 맥락:** Model SQL과 incremental 분기: [가상 코드] Grain·unique_key·중복/null 가상 입력: [정의·샘플] Adapter·engine 버전과 strategy: [설정]

**예시 프롬프트**

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

**기대 결과:** 빈 대상·기존 대상·null·중복 key별 기대 결과표를 주세요. 최소 수정 후보와 필요한 compiled SQL 근거를 주세요.

**LLM이 틀릴 수 있는 부분:** unique_key 설정 자체가 uniqueness를 검사하거나 모든 adapter에 같은 MERGE 동작이 있다고 볼 수 있다.

**검증 방법:** 최초·반복 실행의 compiled SQL을 공식 adapter 문서와 대조해 주세요. 동일 가상 입력의 반복 결과와 null·중복 key 검출을 확인해 주세요.

## Logic 변경 후 full refresh 범위 검토 {#dbt-06}

**상황:** 업무 계산식을 바꿨지만 incremental 입력 밖의 과거 행은 이전 값을 유지한다.

**LLM에 제공할 맥락:** 이전·새 SQL과 변경 적용 기간: [가상 코드·기간] Incremental filter·source 보존 범위: [설정] Downstream mart·metric 의존성과 출력 grain: [목록]

**예시 프롬프트**

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

**기대 결과:** 영향 기간·모델·재계산 후보·불가능한 범위 표를 주세요. 변경 전후 metric 비교와 publish 전 확인 기준을 주세요.

**LLM이 틀릴 수 있는 부분:** Full refresh가 보존되지 않은 원본까지 복원하거나 최신 행 처리만으로 과거 계산도 바뀐다고 볼 수 있다.

**검증 방법:** 실제 source 가용 구간과 모델 의존성을 대조해 주세요. 작은 고정 과거 구간에서 두 계산식의 기대 차이를 확인해 주세요.
