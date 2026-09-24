---
id: prompts-data-observability
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Data observability practical prompts

These reusable, hypothetical work examples were authored from existing study concepts. They are not records of model runs, production work, or experiments. Fill placeholders with sanitized information safe to share. Treat results as hypotheses and drafts.

[Concept guide](../data-platform/data-observability.md) · [Prompt library](index.md)

| Case | Jump to example |
| --- | --- |
| 01 | [Locate the stage where freshness lag starts](#data-observability-01) |
| 02 | [Separate weekday patterns from volume anomalies](#data-observability-02) |
| 03 | [Investigate failure-rate drift at normal volume](#data-observability-03) |
| 04 | [Prioritize schema-change alerts by impact](#data-observability-04) |
| 05 | [Turn repeated alerts into actionable alerts](#data-observability-05) |
| 06 | [Compare pipeline health with data health](#data-observability-06) |

## Locate the stage where freshness lag starts {#data-observability-01}

**Situation:** A dashboard is late, but the delay could be in the source, pipeline, or refresh.

**Context to Give the LLM:** Event, collection, stage completion, and refresh times: [one partition] / Time zones, measurement time, and stage SLOs: [definitions]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Event, collection, stage completion, and refresh times: [one partition]
    Time zones, measurement time, and stage SLOs: [definitions]
    [Task]
    Separate source, pipeline, and downstream freshness.
    Compare adjacent-stage delays and choose the first stage to inspect.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of stage, time evidence, observed delay, missing times, and next check.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare logs and refresh records for the same partition and time zone.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    이벤트·수집·단계 완료·화면 갱신 시각: [같은 partition의 시각]
    시간대·측정 시각·단계별 SLO: [정의]
    [요청]
    Source·Pipeline·Downstream freshness를 구분하세요.
    각 인접 단계의 지연을 비교하고 가장 먼저 확인할 구간을 고르세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    단계 / 시각 근거 / 관측 지연 / 누락 시각 / 다음 확인 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    동일 partition·시간대의 로그와 갱신 기록을 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of stage, time evidence, observed delay, missing times, and next check.

**What the LLM Can Get Wrong:** It may subtract times from different clocks or partitions and invent a bottleneck.

**How to Validate:** Compare logs and refresh records for the same partition and time zone.

## Separate weekday patterns from volume anomalies {#data-observability-02}

**Situation:** A weekend volume drop triggers an alert, but it may be a normal pattern.

**Context to Give the LLM:** Recent daily, weekday, and per-partition counts: [history] / Collection, producer, and filter changes and business schedule: [sanitized record]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Recent daily, weekday, and per-partition counts: [history]
    Collection, producer, and filter changes and business schedule: [sanitized record]
    [Task]
    Compare both recent averages and same-weekday baselines.
    Check separately for missing partitions that total counts may hide.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give normal-pattern candidates, unusual scopes, further evidence, and alert-tuning questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check each explanation against past weekdays, current partitions, and change history.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    최근 일별·요일별 건수와 partition별 건수: [이력]
    수집·producer·filter 변경과 업무 일정: [비식별 기록]
    [요청]
    최근 평균과 같은 요일 기준선을 각각 비교하세요.
    전체 합계가 가릴 수 있는 partition 누락을 별도로 점검하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    정상 패턴 후보 / 이상 구간 / 추가 증거 / 알림 조정 질문을 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    과거 같은 요일·현재 partition 목록·변경 이력으로 각 설명을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give normal-pattern candidates, unusual scopes, further evidence, and alert-tuning questions.

**What the LLM Can Get Wrong:** It may call every weekend decline normal.

**How to Validate:** Check each explanation against past weekdays, current partitions, and change history.

## Investigate failure-rate drift at normal volume {#data-observability-03}

**Situation:** Total volume is normal, but the FAILED share changed sharply.

**Context to Give the LLM:** Counts by status, denominators, NULL rates, and time distributions: [aggregates] / Status mapping, producer versions, and failure-log changes: [history]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Counts by status, denominators, NULL rates, and time distributions: [aggregates]
    Status mapping, producer versions, and failure-log changes: [history]
    [Task]
    Form hypotheses that separate real failures from changes in status recording.
    Locate distribution changes without treating normal volume as proof of health.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of hypothesis, expected distribution, logs to check, and rejection conditions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Aggregate under the same status definition and compare sanitized failure-log samples.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    status별 건수·분모·NULL률·기간별 분포: [집계]
    status 매핑·producer 버전·실패 로그 변경: [이력]
    [요청]
    실제 실패 증가와 status 기록 변경을 구분할 가설을 세우세요.
    전체 volume만으로 정상이라고 판단하지 말고 분포 변화 구간을 찾으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    가설 / 예상 분포 / 확인 로그 / 반박 조건 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    같은 status 정의로 집계하고 비식별 실패 로그 표본과 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of hypothesis, expected distribution, logs to check, and rejection conditions.

**What the LLM Can Get Wrong:** It may mistake a category rename for a real failure increase.

**How to Validate:** Aggregate under the same status definition and compare sanitized failure-log samples.

## Prioritize schema-change alerts by impact {#data-observability-04}

**Situation:** Several column changes are detected, so prioritize consumer checks.

**Context to Give the LLM:** Before-and-after additions, removals, renames, types, and nullable flags: [diff] / Collected lineage, consumer schema needs, and collection gaps: [list]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Before-and-after additions, removals, renames, types, and nullable flags: [diff]
    Collected lineage, consumer schema needs, and collection gaps: [list]
    [Task]
    Link change types to consumer needs and find possible breaking changes.
    Rank checks while separating observed links from unknown dependencies.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of change, consumer, possible failure condition, check order, and evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Check compatibility with actual consumer schemas, transformations, and sample inputs.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    추가·삭제·rename·type·nullable 전후 schema: [차이]
    수집된 lineage·consumer 기대 schema·수집 누락: [목록]
    [요청]
    변경 종류와 consumer 요구를 연결해 잠재적 breaking change를 찾으세요.
    관측된 연결과 아직 모르는 의존성을 구분해 확인 순서를 매기세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    변경 / 소비자 / 실패 가능 조건 / 확인 순서 / 근거 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 consumer schema·변환식·대표 입력으로 호환성을 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of change, consumer, possible failure condition, check order, and evidence.

**What the LLM Can Get Wrong:** It may assume additions are always safe or absent consumers have no impact.

**How to Validate:** Check compatibility with actual consumer schemas, transformations, and sample inputs.

## Turn repeated alerts into actionable alerts {#data-observability-05}

**Situation:** Repeated ALERT and RECOVERY states near a threshold make response difficult.

**Context to Give the LLM:** Metric series, alert and recovery times, and missed incidents: [record] / Dataset tier, SLO, owner, partition, and sanitized run references: [context]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Metric series, alert and recovery times, and missed incidents: [record]
    Dataset tier, SLO, owner, partition, and sanitized run references: [context]
    [Task]
    Find missing definitions for threshold, duration, severity, and context.
    Compare noise reduced and real issues hidden by each duration choice.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Draft an alert message and a table of false-alert and missed-issue risks for each policy.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Apply candidate policies to recorded normal and incident windows and compare detection and misses.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    지표 시계열·알림 및 복구 시각·누락 장애: [기록]
    데이터셋 tier·SLO·owner·partition·실행 링크 대신 비식별 참조: [문맥]
    [요청]
    threshold·duration·severity·context의 빠진 정의를 찾으세요.
    지속 시간별로 줄어드는 잡음과 가려질 수 있는 실제 이상을 비교하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    알림 문안 초안과 정책 후보별 오탐·누락 검토 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    기록된 정상·장애 구간에 후보 정책을 대입해 감지·누락을 비교하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Draft an alert message and a table of false-alert and missed-issue risks for each policy.

**What the LLM Can Get Wrong:** It may treat fewer alerts as proof of better quality.

**How to Validate:** Apply candidate policies to recorded normal and incident windows and compare detection and misses.

## Compare pipeline health with data health {#data-observability-06}

**Situation:** Job and CPU metrics look normal, but users do not trust the output.

**Context to Give the LLM:** Job status, lag, runtime, and resource metrics: [windowed measurements] / Freshness, volume, schema, NULLs, duplicates, and distributions: [same windows]

**Example Prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Job status, lag, runtime, and resource metrics: [windowed measurements]
    Freshness, volume, schema, NULLs, duplicates, and distributions: [same windows]
    [Task]
    Separate pipeline and data signals and find windows where they disagree.
    Link SLOs to the user-facing results that still need checks.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of window, pipeline health, data health, consumer impact, and next evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare actual query results and user views with quality metrics for the same windows.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    job 상태·lag·runtime·자원 지표: [구간별 측정]
    freshness·volume·schema·NULL·중복·분포: [같은 구간 측정]
    [요청]
    파이프라인 신호와 데이터 신호를 나누어 서로 모순되는 구간을 찾으세요.
    어떤 사용자 결과를 추가로 확인해야 하는지 SLO와 연결하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    구간 / pipeline 상태 / data 상태 / 소비 영향 / 다음 증거 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    동일 구간의 실제 query 결과와 사용자 화면을 품질 지표에 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

**Expected Output:** Give a table of window, pipeline health, data health, consumer impact, and next evidence.

**What the LLM Can Get Wrong:** It may use low CPU or successful jobs as evidence of correct data.

**How to Validate:** Compare actual query results and user views with quality metrics for the same windows.
