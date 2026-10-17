---
id: prompts-data-observability
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Data observability practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

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

**Prompt:**

=== "English"

    ```text {.prompt}
    A dashboard is late, but the delay could be in the source, pipeline, or refresh.
    Separate source, pipeline, and downstream freshness.
    Compare adjacent-stage delays and choose the first stage to inspect.
    Give a table of stage, time evidence, observed delay, missing times, and next check.
    ```

=== "한국어"

    ```text {.prompt}
    대시보드가 늦는데 원본·파이프라인·화면 갱신 중 지연 구간이 불명확하다.
    Source·Pipeline·Downstream freshness를 구분하세요.
    각 인접 단계의 지연을 비교하고 가장 먼저 확인할 구간을 고르세요.
    단계 / 시각 근거 / 관측 지연 / 누락 시각 / 다음 확인 표를 주세요.
    ```

**Key point:** Evidence to check first: stage timestamps and clock definitions for the same partition. Align alerts, changes, and run metrics on one timeline. It may subtract times from different clocks or partitions and invent a bottleneck. Exclude delay estimates formed by subtracting unrelated clocks or partitions.

## Separate weekday patterns from volume anomalies {#data-observability-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    A weekend volume drop triggers an alert, but it may be a normal pattern.
    Compare both recent averages and same-weekday baselines.
    Check separately for missing partitions that total counts may hide.
    Give normal-pattern candidates, unusual scopes, further evidence, and alert-tuning questions.
    ```

=== "한국어"

    ```text {.prompt}
    주말 건수가 줄어 알림이 울리지만 정상 패턴인지 불명확하다.
    최근 평균과 같은 요일 기준선을 각각 비교하세요.
    전체 합계가 가릴 수 있는 partition 누락을 별도로 점검하세요.
    정상 패턴 후보 / 이상 구간 / 추가 증거 / 알림 조정 질문을 주세요.
    ```

**Key point:** Evidence to check first: comparable weekday history and a missing-partition list. Align alerts, changes, and run metrics on one timeline. It may call every weekend decline normal. Keep missing partitions as separate failures even when totals look normal.

## Investigate failure-rate drift at normal volume {#data-observability-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Total volume is normal, but the FAILED share changed sharply.
    Form hypotheses that separate real failures from changes in status recording.
    Locate distribution changes without treating normal volume as proof of health.
    Give a table of hypothesis, expected distribution, logs to check, and rejection conditions.
    ```

=== "한국어"

    ```text {.prompt}
    총건수는 평소와 같지만 FAILED 비율이 크게 달라졌다.
    실제 실패 증가와 status 기록 변경을 구분할 가설을 세우세요.
    전체 volume만으로 정상이라고 판단하지 말고 분포 변화 구간을 찾으세요.
    가설 / 예상 분포 / 확인 로그 / 반박 조건 표를 주세요.
    ```

**Key point:** Evidence to check first: denominators under one status definition and producer-change times. Align alerts, changes, and run metrics on one timeline. It may mistake a category rename for a real failure increase. Separate status renames and rising NULLs from real failure growth.

## Prioritize schema-change alerts by impact {#data-observability-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Several column changes are detected, so prioritize consumer checks.
    Link change types to consumer needs and find possible breaking changes.
    Rank checks while separating observed links from unknown dependencies.
    Give a table of change, consumer, possible failure condition, check order, and evidence.
    ```

=== "한국어"

    ```text {.prompt}
    여러 column 변경이 동시에 감지되어 소비자 확인 순서를 정한다.
    변경 종류와 consumer 요구를 연결해 잠재적 breaking change를 찾으세요.
    관측된 연결과 아직 모르는 의존성을 구분해 확인 순서를 매기세요.
    변경 / 소비자 / 실패 가능 조건 / 확인 순서 / 근거 표를 주세요.
    ```

**Key point:** Evidence to check first: the change diff and consumers with confirmed dependencies. Align alerts, changes, and run metrics on one timeline. It may assume additions are always safe or absent consumers have no impact. Do not classify consumers absent from lineage as unaffected.

## Turn repeated alerts into actionable alerts {#data-observability-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Repeated ALERT and RECOVERY states near a threshold make response difficult.
    Find missing definitions for threshold, duration, severity, and context.
    Compare noise reduced and real issues hidden by each duration choice.
    Draft an alert message and a table of false-alert and missed-issue risks for each policy.
    ```

=== "한국어"

    ```text {.prompt}
    임계값 근처에서 ALERT와 RECOVERY가 반복되어 대응이 어렵다.
    threshold·duration·severity·context의 빠진 정의를 찾으세요.
    지속 시간별로 줄어드는 잡음과 가려질 수 있는 실제 이상을 비교하세요.
    알림 문안 초안과 정책 후보별 오탐·누락 검토 표를 주세요.
    ```

**Key point:** Evidence to check first: historical incident windows and required detection time. Align alerts, changes, and run metrics on one timeline. It may treat fewer alerts as proof of better quality. Prioritize incident detection and response criteria over reducing alert counts.

## Compare pipeline health with data health {#data-observability-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    Job and CPU metrics look normal, but users do not trust the output.
    Separate pipeline and data signals and find windows where they disagree.
    Link SLOs to the user-facing results that still need checks.
    Give a table of window, pipeline health, data health, consumer impact, and next evidence.
    ```

=== "한국어"

    ```text {.prompt}
    job·CPU 지표는 정상이지만 사용자가 결과를 신뢰하지 못한다.
    파이프라인 신호와 데이터 신호를 나누어 서로 모순되는 구간을 찾으세요.
    어떤 사용자 결과를 추가로 확인해야 하는지 SLO와 연결하세요.
    구간 / pipeline 상태 / data 상태 / 소비 영향 / 다음 증거 표를 주세요.
    ```

**Key point:** Evidence to check first: the user-visible result in question and quality metrics for that interval. Align alerts, changes, and run metrics on one timeline. It may use low CPU or successful jobs as evidence of correct data. Do not use low CPU or job success as the sole basis for declaring data healthy.
