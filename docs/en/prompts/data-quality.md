---
id: prompts-data-quality
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Data quality practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/data-quality.md) · [Prompt library](index.md)

| Case | Jump to example |
| --- | --- |
| 01 | [Place quality checks by layer](#data-quality-01) |
| 02 | [Separate missing values from broken references](#data-quality-02) |
| 03 | [Prepare quarantined data for reprocessing](#data-quality-03) |
| 04 | [Define quality SLO measurements](#data-quality-04) |
| 05 | [Reconcile call costs with billing totals](#data-quality-05) |
| 06 | [Define when downstream use can resume](#data-quality-06) |

## Place quality checks by layer {#data-quality-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    Decide which quality checks belong in each layer of a new call dataset.
    Review completeness, uniqueness, validity, consistency, freshness, accuracy, and volume.
    Place each rule in a layer and explain which later checks are still needed.
    Give a table of layer, rule, failure example, owner, and evidence.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    신규 호출 데이터셋에 어떤 품질 검사를 어느 계층에 둘지 정한다.
    완전성·유일성·유효성·일관성·최신성·정확성·양을 검토하세요.
    각 규칙을 계층에 배치하고 뒤 계층에도 필요한 검사를 설명하세요.
    계층 / 규칙 / 실패 예시 / 담당자 / 확인 증거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: dataset grain and quality requirements agreed by consumers. Label valid and invalid samples and include expected results from the business owner. It may confuse valid format with accuracy or skip Gold checks after earlier checks pass. Earlier checks must not substitute for accuracy checks on later business calculations.

## Separate missing values from broken references {#data-quality-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Classify model_id errors as missing required values or broken table references.
    Separate the roles of not_null, relationships, accepted_values, and unique checks.
    State which records and reference refresh times to inspect for each failure.
    Give a table of check, detected error, missed error, and further evidence.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    model_id 오류가 필수 값 누락인지 참조 테이블 불일치인지 분류한다.
    not_null·relationships·accepted_values·unique 검사의 역할을 나누세요.
    각 실패에서 확인할 레코드와 참조 데이터 갱신 시각을 지정하세요.
    검사 / 검출 대상 / 놓치는 오류 / 추가 증거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the reference table cutoff and rules for NULL keys. Label valid and invalid samples and include expected results from the business owner. It may treat removing NULLs as a fix for references or invent the uniqueness grain. Check that reference refresh delays do not incorrectly reject valid data.

## Prepare quarantined data for reprocessing {#data-quality-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Quarantined records are growing, so prepare a reprocessing sequence after a fix.
    Separate error types covered by the fix from those still unresolved.
    Propose reprocessing through validation again, including duplicate checks.
    Give a table of scope, prerequisites, stop conditions, rechecks, and remaining quarantine.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    격리 레코드가 누적되어 수정 후 재처리 순서를 준비한다.
    수정으로 해결된 유형과 아직 해결되지 않은 유형을 구분하세요.
    검증 경로 재진입과 중복 확인을 포함한 재처리 순서를 제안하세요.
    대상 구간 / 선행 조건 / 중단 조건 / 재검사 / 남은 격리 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: error types covered by the fix and available replay input ranges. Label valid and invalid samples and include expected results from the business owner. It may replay all quarantined data blindly or treat raw payloads as safe to disclose. Do not replay unresolved errors or expose raw payloads.

## Define quality SLO measurements {#data-quality-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Two consumers need different freshness targets for the same dataset.
    Separate SLI measurement definitions from proposed SLO targets.
    State the clocks and denominators for freshness, completeness, and duplicate rate.
    Give a table of consumer, SLI formula, window, proposed target, and agreement questions.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    두 소비자가 같은 데이터셋에 서로 다른 최신성 목표를 요구한다.
    SLI 측정 정의와 제안 SLO 목표를 분리하세요.
    최신성·완전성·중복률의 시간 기준과 분모를 명시하세요.
    소비자 / SLI 식 / 구간 / 제안 목표 / 합의 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: deadlines, allowed delay, and measurement denominators for each consumer. Label valid and invalid samples and include expected results from the business owner. It may use example values such as five minutes or 99.9% as approved defaults. Record owner agreement instead of treating example values as approved targets.

## Reconcile call costs with billing totals {#data-quality-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Cost fields are valid, but call totals differ from billing totals.
    Separate valid values from accurate amounts.
    Order checks for window, unit, duplicate, and late-arrival hypotheses.
    Give a table of difference, possible explanation, supporting or opposing evidence, and next check.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    비용 필드가 모두 유효하지만 호출 합계와 청구 합계가 다르다.
    유효성 통과와 실제 금액의 정확성을 구분하세요.
    기간·단위·중복·도착 지연 가설별 대조 순서를 제시하세요.
    차이 구간 / 가능한 설명 / 지지·반박 증거 / 다음 대조 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: currency, cutoff, and billing scope for both amounts. Label valid and invalid samples and include expected results from the business owner. It may assume every difference means a bad call record. Do not adjust unexplained differences or assume one side is automatically correct.

## Define when downstream use can resume {#data-quality-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    Review whether a dashboard can resume after bad data was reprocessed.
    Check completion evidence for Detect, Contain, Fix, Reprocess, and Verify.
    Separate job success from data recovery and identify reasons to hold use.
    Give a table of consumer, recovery evidence, failed checks, resume criteria, and owner.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    오류 데이터를 재처리한 뒤 대시보드를 다시 열지 검토 중이야.
    Detect·Contain·Fix·Reprocess·Verify 단계별 완료 근거를 점검하세요.
    작업 성공과 데이터 복구를 구분하고 재개 보류 조건을 찾으세요.
    소비자 / 복구 증거 / 미충족 검사 / 재개 조건 / 담당자 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: checks covering all affected partitions and resume criteria for each consumer. Label valid and invalid samples and include expected results from the business owner. It may treat a successful job as proof that duplicates, gaps, and downstream errors are fixed. Compare consumer results before resuming, rather than relying only on a successful reprocessing job.
