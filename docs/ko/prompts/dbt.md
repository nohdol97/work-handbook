---
id: prompts-dbt
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# dbt 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

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

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    여러 모델에 같은 join과 업무 규칙이 반복되어 책임을 정리하려고 해.
    Rename·type 정리와 재사용 business logic을 구분해 주세요.
    현재 계층을 먼저 평가한 뒤 최소 이동 후보를 제안해 주세요.
    Intermediate가 꼭 필요한지 실제 재사용 근거로 판단해 주세요.
    Logic별 현재 위치·책임·재사용처·이동 이유 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Several models repeat the same join and business rules. Review their responsibilities.
    Separate renaming and type cleanup from reusable business logic.
    Assess current layers before suggesting the smallest moves.
    Judge the need for an intermediate layer from actual reuse evidence.
    Return each rule’s location, responsibility, consumers, and reason for any move.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 중복 logic을 실제 사용하는 모델과 각 모델 grain. 모델 SQL과 compiled SQL을 구분하고 변경 diff에 줄 번호를 붙인다. 계층 이름을 Bronze/Silver/Gold와 일대일로 맞추거나 작은 모델도 무조건 분리할 수 있다. 중복 제거 뒤에도 key·행 수·업무 합계가 유지되어야 한다.

## ref·source 누락과 환경 의존성 점검 {#dbt-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    개발 SQL이 다른 환경의 고정 table 이름을 참조해 dependency가 빠진다.
    내부 model은 ref, 외부 입력은 source 후보로 분류해 주세요.
    고정 이름이 실행 순서·lineage에 미치는 영향을 검토해 주세요.
    dbt 밖의 수집·BI 경로는 추적 확인이 필요한 범위로 남겨 주세요.
    참조별 현재 relation·의도한 환경·의존성 선언 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Development SQL uses a fixed table name from another environment, hiding a dependency.
    Classify internal models as ref candidates and external inputs as source candidates.
    Review how fixed names affect execution order and lineage.
    Keep ingestion and BI paths outside dbt as scope needing separate evidence.
    Return current relations, intended environments, and dependency declarations by reference.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 환경별 relation 해석과 내부·외부 소유 경계. 모델 SQL과 compiled SQL을 구분하고 변경 diff에 줄 번호를 붙인다. 모든 table을 ref로 바꾸거나 dbt graph가 플랫폼 전체 lineage라고 단정할 수 있다. 컴파일 성공과 의도한 환경을 읽는지는 따로 확인한다.

## 품질 test와 업무 규칙의 빈틈 찾기 {#dbt-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    기본 test는 통과하지만 허용되지 않은 업무 상태가 mart에 들어간다.
    기본 test가 확인하는 조건과 확인하지 않는 의미를 구분해 주세요.
    업무 규칙별 custom test 후보와 반례를 제안해 주세요.
    Test 실패와 실제 publish 차단 연결의 누락 근거를 적어 주세요.
    규칙·검사·실패 샘플·기대 결과의 대응표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Basic tests pass, but a mart contains a business state that should not be allowed.
    Separate conditions checked by basic tests from meanings they do not check.
    Propose custom test candidates and counterexamples for business rules.
    List missing evidence connecting test failure to publication blocking.
    Return a mapping of rules, tests, failing samples, and expected outcomes.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 승인된 업무 규칙과 test 실패 시 publish 정책. 모델 SQL과 compiled SQL을 구분하고 변경 diff에 줄 번호를 붙인다. 기본 test 통과를 데이터 의미의 정확성이나 자동 publish 차단과 혼동할 수 있다. test가 실패해도 publish가 진행되는 경로가 남으면 완료로 보지 않는다.

## Snapshot과 CDC 이력의 역할 비교 {#dbt-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    이미 CDC history가 있는 table에 dbt snapshot을 추가할지 검토 중이야.
    현재 history로 충족되는 요구와 부족한 요구를 분리해 주세요.
    Snapshot 관측 사이 중간 변경의 보존 한계를 설명해 주세요.
    Type 1과 Type 2의 선택을 과거 분석 요구에 연결해 주세요.
    요구별 CDC history·snapshot 충족 여부와 가정 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review whether a table with CDC history also needs a dbt snapshot.
    Separate requirements covered by current history from gaps.
    Explain limits on preserving changes between snapshot observations.
    Tie the Type 1 or Type 2 choice to historical analysis needs.
    Return coverage and assumptions for CDC history and snapshots by requirement.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: CDC history로 답해야 할 과거 질문과 삭제 보존 범위. 모델 SQL과 compiled SQL을 구분하고 변경 diff에 줄 번호를 붙인다. Snapshot이 모든 중간 변경을 포착하거나 CDC가 있으면 모든 이력 요구가 충족된다고 볼 수 있다. 두 관측 사이 여러 변경이 필요한 질문은 snapshot만으로 충족한다고 보지 않는다.

## Incremental key와 최초 실행 계약 {#dbt-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Model이 incremental 실행은 되지만 최초 실행 또는 null key에서 실패한다.
    최초 전체 실행과 이후 실행의 SQL 경로를 따로 검토해 주세요.
    Key가 grain에 맞는지와 실제 uniqueness 검사가 있는지 확인해 주세요.
    Strategy 지원과 key 처리의 불확실성을 명시해 주세요.
    빈 대상·기존 대상·null·중복 key별 기대 결과표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A model works incrementally but fails on the first run or with null keys.
    Review SQL paths for the first full run and later runs separately.
    Check whether the key matches the grain and has a real uniqueness test.
    State uncertainty about strategy support and key handling.
    Return expected results for empty targets, existing targets, nulls, and duplicate keys.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 adapter strategy와 최초·반복 실행 compiled SQL. 모델 SQL과 compiled SQL을 구분하고 변경 diff에 줄 번호를 붙인다. unique_key 설정 자체가 uniqueness를 검사하거나 모든 adapter에 같은 MERGE 동작이 있다고 볼 수 있다. unique_key 선언과 별개로 실제 입력·출력 uniqueness를 확인한다.

## Logic 변경 후 full refresh 범위 검토 {#dbt-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    업무 계산식을 바꿨지만 incremental 입력 밖의 과거 행은 이전 값을 유지한다.
    새 logic이 바꾸는 과거 행과 현재 처리 범위를 비교해 주세요.
    Full refresh와 제한된 재처리 후보의 입력 복원 가능성을 검토해 주세요.
    기존 설계를 평가한 뒤 알려진 사실·가정·자료 부족을 구분해 주세요.
    영향 기간·모델·재계산 후보·불가능한 범위 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A changed business formula leaves older rows outside the incremental input unchanged.
    Compare historical rows affected by the new logic with the current processing range.
    Review input availability for full refresh and bounded reprocessing options.
    Assess the current design, then separate facts, assumptions, and missing data.
    Return affected periods, models, recalculation options, and unavailable ranges.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 계산 변경의 적용 기간과 재계산할 원본 가용 구간. 모델 SQL과 compiled SQL을 구분하고 변경 diff에 줄 번호를 붙인다. Full refresh가 보존되지 않은 원본까지 복원하거나 최신 행 처리만으로 과거 계산도 바뀐다고 볼 수 있다. 오래된 원본이 없으면 전체 복구 가능이라고 쓰지 않는다.
