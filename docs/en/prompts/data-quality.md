---
id: prompts-data-quality
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Data quality practical prompts

These reusable, hypothetical work examples were authored from existing study concepts. They are not records of model runs, production work, or experiments. Fill placeholders with sanitized information safe to share. Treat results as hypotheses and drafts.

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

**Situation:** Decide which quality checks belong in each layer of a new call dataset.

**Context to Give the LLM:** Schema, required fields, and event grain: [sanitized definitions] / Ingestion, Silver, and Gold steps and KPI needs: [list]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Schema, required fields, and event grain: [sanitized definitions]
    Ingestion, Silver, and Gold steps and KPI needs: [list]
    [Task]
    Review completeness, uniqueness, validity, consistency, freshness, accuracy, and volume.
    Place each rule in a layer and explain which later checks are still needed.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of layer, rule, failure example, owner, and evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check each rule against valid and invalid synthetic records and the KPI needs.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    스키마·필수 필드·이벤트 grain: [비식별 정의]
    Ingestion·Silver·Gold 변환과 KPI 요구: [목록]
    [요청]
    완전성·유일성·유효성·일관성·최신성·정확성·양을 검토하세요.
    각 규칙을 계층에 배치하고 뒤 계층에도 필요한 검사를 설명하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    계층 / 규칙 / 실패 예시 / 담당자 / 확인 증거 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    각 규칙에 정상·오류 가상 레코드를 대입하고 KPI 요구와 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of layer, rule, failure example, owner, and evidence.

**What the LLM Can Get Wrong:** It may confuse valid format with accuracy or skip Gold checks after earlier checks pass.

**How to Validate:** Check each rule against valid and invalid synthetic records and the KPI needs.

## Separate missing values from broken references {#data-quality-02}

**Situation:** Classify model_id errors as missing required values or broken table references.

**Context to Give the LLM:** Call and model table grains and keys: [schemas] / NULL, unmatched key, and allowed-status counts: [window and values]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Call and model table grains and keys: [schemas]
    NULL, unmatched key, and allowed-status counts: [window and values]
    [Task]
    Separate the roles of not_null, relationships, accepted_values, and unique checks.
    State which records and reference refresh times to inspect for each failure.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of check, detected error, missed error, and further evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check coverage against the supplied key definitions and synthetic failing records.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    호출·모델 테이블 grain과 키: [스키마]
    NULL·미참조 키·허용 상태 집계: [측정 구간과 값]
    [요청]
    not_null·relationships·accepted_values·unique 검사의 역할을 나누세요.
    각 실패에서 확인할 레코드와 참조 데이터 갱신 시각을 지정하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    검사 / 검출 대상 / 놓치는 오류 / 추가 증거 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    제공된 키 정의와 가상 실패 레코드로 검사 범위를 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of check, detected error, missed error, and further evidence.

**What the LLM Can Get Wrong:** It may treat removing NULLs as a fix for references or invent the uniqueness grain.

**How to Validate:** Check coverage against the supplied key definitions and synthetic failing records.

## Prepare quarantined data for reprocessing {#data-quality-03}

**Situation:** Quarantined records are growing, so prepare a reprocessing sequence after a fix.

**Context to Give the LLM:** Counts by error type, receipt windows, and fix history: [summary] / Quarantine fields, event keys, access and retention rules: [sanitized definitions]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Counts by error type, receipt windows, and fix history: [summary]
    Quarantine fields, event keys, access and retention rules: [sanitized definitions]
    [Task]
    Separate error types covered by the fix from those still unresolved.
    Propose reprocessing through validation again, including duplicate checks.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of scope, prerequisites, stop conditions, rechecks, and remaining quarantine.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare counts, error reasons, and duplicate rates before and after, without exposing payloads.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    오류 유형별 건수·수신 구간·수정 이력: [요약]
    격리 필드·이벤트 키·접근 및 보관 규칙: [비식별 정의]
    [요청]
    수정으로 해결된 유형과 아직 해결되지 않은 유형을 구분하세요.
    검증 경로 재진입과 중복 확인을 포함한 재처리 순서를 제안하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    대상 구간 / 선행 조건 / 중단 조건 / 재검사 / 남은 격리 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    격리 전후 건수와 오류 사유·중복률을 비교하고 원문 노출 없이 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of scope, prerequisites, stop conditions, rechecks, and remaining quarantine.

**What the LLM Can Get Wrong:** It may replay all quarantined data blindly or treat raw payloads as safe to disclose.

**How to Validate:** Compare counts, error reasons, and duplicate rates before and after, without exposing payloads.

## Define quality SLO measurements {#data-quality-04}

**Situation:** Two consumers need different freshness targets for the same dataset.

**Context to Give the LLM:** Dashboard and report deadlines and allowed delay: [requirements] / Time fields, required values, duplicate keys, and windows: [definitions]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Dashboard and report deadlines and allowed delay: [requirements]
    Time fields, required values, duplicate keys, and windows: [definitions]
    [Task]
    Separate SLI measurement definitions from proposed SLO targets.
    State the clocks and denominators for freshness, completeness, and duplicate rate.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of consumer, SLI formula, window, proposed target, and agreement questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Calculate the formulas with synthetic measurements and compare targets with owner needs.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    대시보드·보고서 업무 마감과 허용 지연: [요구사항]
    시각 필드·필수 값·중복 키·측정 구간: [정의]
    [요청]
    SLI 측정 정의와 제안 SLO 목표를 분리하세요.
    최신성·완전성·중복률의 시간 기준과 분모를 명시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    소비자 / SLI 식 / 구간 / 제안 목표 / 합의 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    가상 측정치로 식을 계산하고 업무 담당자 요구와 목표를 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of consumer, SLI formula, window, proposed target, and agreement questions.

**What the LLM Can Get Wrong:** It may use example values such as five minutes or 99.9% as approved defaults.

**How to Validate:** Calculate the formulas with synthetic measurements and compare targets with owner needs.

## Reconcile call costs with billing totals {#data-quality-05}

**Situation:** Cost fields are valid, but call totals differ from billing totals.

**Context to Give the LLM:** Call cost aggregates and billing summary: [sanitized values for one window] / Currency, units, grain, duplicate checks, and cutoff times: [definitions]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Call cost aggregates and billing summary: [sanitized values for one window]
    Currency, units, grain, duplicate checks, and cutoff times: [definitions]
    [Task]
    Separate valid values from accurate amounts.
    Order checks for window, unit, duplicate, and late-arrival hypotheses.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of difference, possible explanation, supporting or opposing evidence, and next check.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare aggregates with matched scope, units, and cutoff, and mark unresolved amounts.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    호출 비용 집계·청구 요약: [동일 구간의 비식별 값]
    통화·단위·집계 grain·중복 검사·마감 시각: [정의]
    [요청]
    유효성 통과와 실제 금액의 정확성을 구분하세요.
    기간·단위·중복·도착 지연 가설별 대조 순서를 제시하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    차이 구간 / 가능한 설명 / 지지·반박 증거 / 다음 대조 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    같은 범위·단위·마감 기준으로 집계를 다시 비교하고 미확인 금액을 남기세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of difference, possible explanation, supporting or opposing evidence, and next check.

**What the LLM Can Get Wrong:** It may assume every difference means a bad call record.

**How to Validate:** Compare aggregates with matched scope, units, and cutoff, and mark unresolved amounts.

## Define when downstream use can resume {#data-quality-06}

**Situation:** Review whether a dashboard can resume after bad data was reprocessed.

**Context to Give the LLM:** Affected partitions, fix details, and reprocessing results: [summary] / Before-and-after quality metrics, KPI totals, and downstream list: [evidence]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Affected partitions, fix details, and reprocessing results: [summary]
    Before-and-after quality metrics, KPI totals, and downstream list: [evidence]
    [Task]
    Check completion evidence for Detect, Contain, Fix, Reprocess, and Verify.
    Separate job success from data recovery and identify reasons to hold use.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of consumer, recovery evidence, failed checks, resume criteria, and owner.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare quality checks and consumer totals for the affected scope; let owners decide on resuming.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    영향 partition·수정 내용·재처리 실행 결과: [요약]
    전후 품질 지표·KPI 합계·downstream 목록: [증거]
    [요청]
    Detect·Contain·Fix·Reprocess·Verify 단계별 완료 근거를 점검하세요.
    작업 성공과 데이터 복구를 구분하고 재개 보류 조건을 찾으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    소비자 / 복구 증거 / 미충족 검사 / 재개 조건 / 담당자 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    영향 범위의 품질 검사와 소비자 집계를 대조하고 담당자가 재개를 판단하게 하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of consumer, recovery evidence, failed checks, resume criteria, and owner.

**What the LLM Can Get Wrong:** It may treat a successful job as proof that duplicates, gaps, and downstream errors are fixed.

**How to Validate:** Compare quality checks and consumer totals for the affected scope; let owners decide on resuming.
