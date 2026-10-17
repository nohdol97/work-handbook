---
id: prompts-data-observability
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 데이터 관측성 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../data-platform/data-observability.md) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [최신성 지연 구간 찾기](#data-observability-01) |
| 02 | [요일 변화와 건수 이상 구분](#data-observability-02) |
| 03 | [정상 건수 속 실패율 변화 조사](#data-observability-03) |
| 04 | [schema 변경 알림의 영향 우선순위](#data-observability-04) |
| 05 | [반복 알림을 대응 가능한 알림으로 바꾸기](#data-observability-05) |
| 06 | [파이프라인 상태와 데이터 상태 대조](#data-observability-06) |

## 최신성 지연 구간 찾기 {#data-observability-01}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    대시보드가 늦는데 원본·파이프라인·화면 갱신 중 지연 구간이 불명확하다.
    Source·Pipeline·Downstream freshness를 구분하세요.
    각 인접 단계의 지연을 비교하고 가장 먼저 확인할 구간을 고르세요.
    단계 / 시각 근거 / 관측 지연 / 누락 시각 / 다음 확인 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    A dashboard is late, but the delay could be in the source, pipeline, or refresh.
    Separate source, pipeline, and downstream freshness.
    Compare adjacent-stage delays and choose the first stage to inspect.
    Give a table of stage, time evidence, observed delay, missing times, and next check.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 같은 partition의 각 단계 시각과 시계 기준. 알림·변경 이력·실행 지표를 같은 시간축으로 정렬한다. 서로 다른 시계나 partition의 시각을 빼서 가짜 병목을 만들 수 있다. 서로 다른 clock·partition을 빼서 만든 지연은 근거에서 제외한다.

## 요일 변화와 건수 이상 구분 {#data-observability-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    주말 건수가 줄어 알림이 울리지만 정상 패턴인지 불명확하다.
    최근 평균과 같은 요일 기준선을 각각 비교하세요.
    전체 합계가 가릴 수 있는 partition 누락을 별도로 점검하세요.
    정상 패턴 후보 / 이상 구간 / 추가 증거 / 알림 조정 질문을 주세요.
    ```

=== "English"

    ```text {.prompt}
    A weekend volume drop triggers an alert, but it may be a normal pattern.
    Compare both recent averages and same-weekday baselines.
    Check separately for missing partitions that total counts may hide.
    Give normal-pattern candidates, unusual scopes, further evidence, and alert-tuning questions.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 비교 가능한 요일 이력과 누락 partition 목록. 알림·변경 이력·실행 지표를 같은 시간축으로 정렬한다. 주말이라는 이유만으로 모든 감소를 정상으로 처리할 수 있다. 전체 합계가 정상이어도 특정 partition 누락은 별도 실패로 남긴다.

## 정상 건수 속 실패율 변화 조사 {#data-observability-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    총건수는 평소와 같지만 FAILED 비율이 크게 달라졌다.
    실제 실패 증가와 status 기록 변경을 구분할 가설을 세우세요.
    전체 volume만으로 정상이라고 판단하지 말고 분포 변화 구간을 찾으세요.
    가설 / 예상 분포 / 확인 로그 / 반박 조건 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Total volume is normal, but the FAILED share changed sharply.
    Form hypotheses that separate real failures from changes in status recording.
    Locate distribution changes without treating normal volume as proof of health.
    Give a table of hypothesis, expected distribution, logs to check, and rejection conditions.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 같은 status 정의로 계산한 분모와 producer 변경 시점. 알림·변경 이력·실행 지표를 같은 시간축으로 정렬한다. 범주 이름 변경을 실제 장애 증가로 오해할 수 있다. status rename·NULL 증가가 실제 실패 증가로 섞이지 않아야 한다.

## schema 변경 알림의 영향 우선순위 {#data-observability-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    여러 column 변경이 동시에 감지되어 소비자 확인 순서를 정한다.
    변경 종류와 consumer 요구를 연결해 잠재적 breaking change를 찾으세요.
    관측된 연결과 아직 모르는 의존성을 구분해 확인 순서를 매기세요.
    변경 / 소비자 / 실패 가능 조건 / 확인 순서 / 근거 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Several column changes are detected, so prioritize consumer checks.
    Link change types to consumer needs and find possible breaking changes.
    Rank checks while separating observed links from unknown dependencies.
    Give a table of change, consumer, possible failure condition, check order, and evidence.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 변경 diff와 영향이 확인된 consumer 목록. 알림·변경 이력·실행 지표를 같은 시간축으로 정렬한다. column 추가는 항상 안전하거나 그래프에 없는 consumer는 영향이 없다고 단정할 수 있다. lineage에 없는 consumer를 영향 없음으로 분류하지 않는다.

## 반복 알림을 대응 가능한 알림으로 바꾸기 {#data-observability-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    임계값 근처에서 ALERT와 RECOVERY가 반복되어 대응이 어렵다.
    threshold·duration·severity·context의 빠진 정의를 찾으세요.
    지속 시간별로 줄어드는 잡음과 가려질 수 있는 실제 이상을 비교하세요.
    알림 문안 초안과 정책 후보별 오탐·누락 검토 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Repeated ALERT and RECOVERY states near a threshold make response difficult.
    Find missing definitions for threshold, duration, severity, and context.
    Compare noise reduced and real issues hidden by each duration choice.
    Draft an alert message and a table of false-alert and missed-issue risks for each policy.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 과거 장애 구간과 놓치면 안 되는 감지 시간. 알림·변경 이력·실행 지표를 같은 시간축으로 정렬한다. 알림 수가 줄면 품질이 좋아졌다고 단정할 수 있다. 알림 수 감소보다 실제 장애 검출과 대응 시간 기준을 우선한다.

## 파이프라인 상태와 데이터 상태 대조 {#data-observability-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    job·CPU 지표는 정상이지만 사용자가 결과를 신뢰하지 못한다.
    파이프라인 신호와 데이터 신호를 나누어 서로 모순되는 구간을 찾으세요.
    어떤 사용자 결과를 추가로 확인해야 하는지 SLO와 연결하세요.
    구간 / pipeline 상태 / data 상태 / 소비 영향 / 다음 증거 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Job and CPU metrics look normal, but users do not trust the output.
    Separate pipeline and data signals and find windows where they disagree.
    Link SLOs to the user-facing results that still need checks.
    Give a table of window, pipeline health, data health, consumer impact, and next evidence.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 사용자가 문제로 보는 실제 결과와 해당 구간 품질 지표. 알림·변경 이력·실행 지표를 같은 시간축으로 정렬한다. 낮은 CPU나 성공한 job을 올바른 데이터의 증거로 사용할 수 있다. 낮은 CPU·job 성공을 데이터 정상 판정의 단독 근거로 쓰지 않는다.
