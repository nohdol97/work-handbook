---
id: prompts-data-observability
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 데이터 관측성 실무 프롬프트

기존 학습 개념에서 파생해 작성한 재사용 가능한 가상 실무 예시다. 모델 호출·실제 운영·실험을 수행한 기록이 아니다. 대괄호 입력을 공개 가능한 비식별 정보로 채우고, 결과를 가설과 초안으로 검토한다.

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

**상황:** 대시보드가 늦는데 원본·파이프라인·화면 갱신 중 지연 구간이 불명확하다.

**LLM에 제공할 맥락:** 이벤트·수집·단계 완료·화면 갱신 시각: [같은 partition의 시각] / 시간대·측정 시각·단계별 SLO: [정의]

**예시 프롬프트:**

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

**기대 결과:** 단계 / 시각 근거 / 관측 지연 / 누락 시각 / 다음 확인 표를 주세요.

**LLM 오류 가능성:** 서로 다른 시계나 partition의 시각을 빼서 가짜 병목을 만들 수 있다.

**검증 방법:** 동일 partition·시간대의 로그와 갱신 기록을 대조하세요.

## 요일 변화와 건수 이상 구분 {#data-observability-02}

**상황:** 주말 건수가 줄어 알림이 울리지만 정상 패턴인지 불명확하다.

**LLM에 제공할 맥락:** 최근 일별·요일별 건수와 partition별 건수: [이력] / 수집·producer·filter 변경과 업무 일정: [비식별 기록]

**예시 프롬프트:**

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

**기대 결과:** 정상 패턴 후보 / 이상 구간 / 추가 증거 / 알림 조정 질문을 주세요.

**LLM 오류 가능성:** 주말이라는 이유만으로 모든 감소를 정상으로 처리할 수 있다.

**검증 방법:** 과거 같은 요일·현재 partition 목록·변경 이력으로 각 설명을 확인하세요.

## 정상 건수 속 실패율 변화 조사 {#data-observability-03}

**상황:** 총건수는 평소와 같지만 FAILED 비율이 크게 달라졌다.

**LLM에 제공할 맥락:** status별 건수·분모·NULL률·기간별 분포: [집계] / status 매핑·producer 버전·실패 로그 변경: [이력]

**예시 프롬프트:**

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

**기대 결과:** 가설 / 예상 분포 / 확인 로그 / 반박 조건 표를 주세요.

**LLM 오류 가능성:** 범주 이름 변경을 실제 장애 증가로 오해할 수 있다.

**검증 방법:** 같은 status 정의로 집계하고 비식별 실패 로그 표본과 대조하세요.

## schema 변경 알림의 영향 우선순위 {#data-observability-04}

**상황:** 여러 column 변경이 동시에 감지되어 소비자 확인 순서를 정한다.

**LLM에 제공할 맥락:** 추가·삭제·rename·type·nullable 전후 schema: [차이] / 수집된 lineage·consumer 기대 schema·수집 누락: [목록]

**예시 프롬프트:**

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

**기대 결과:** 변경 / 소비자 / 실패 가능 조건 / 확인 순서 / 근거 표를 주세요.

**LLM 오류 가능성:** column 추가는 항상 안전하거나 그래프에 없는 consumer는 영향이 없다고 단정할 수 있다.

**검증 방법:** 실제 consumer schema·변환식·대표 입력으로 호환성을 확인하세요.

## 반복 알림을 대응 가능한 알림으로 바꾸기 {#data-observability-05}

**상황:** 임계값 근처에서 ALERT와 RECOVERY가 반복되어 대응이 어렵다.

**LLM에 제공할 맥락:** 지표 시계열·알림 및 복구 시각·누락 장애: [기록] / 데이터셋 tier·SLO·owner·partition·실행 링크 대신 비식별 참조: [문맥]

**예시 프롬프트:**

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

**기대 결과:** 알림 문안 초안과 정책 후보별 오탐·누락 검토 표를 주세요.

**LLM 오류 가능성:** 알림 수가 줄면 품질이 좋아졌다고 단정할 수 있다.

**검증 방법:** 기록된 정상·장애 구간에 후보 정책을 대입해 감지·누락을 비교하세요.

## 파이프라인 상태와 데이터 상태 대조 {#data-observability-06}

**상황:** job·CPU 지표는 정상이지만 사용자가 결과를 신뢰하지 못한다.

**LLM에 제공할 맥락:** job 상태·lag·runtime·자원 지표: [구간별 측정] / freshness·volume·schema·NULL·중복·분포: [같은 구간 측정]

**예시 프롬프트:**

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

**기대 결과:** 구간 / pipeline 상태 / data 상태 / 소비 영향 / 다음 증거 표를 주세요.

**LLM 오류 가능성:** 낮은 CPU나 성공한 job을 올바른 데이터의 증거로 사용할 수 있다.

**검증 방법:** 동일 구간의 실제 query 결과와 사용자 화면을 품질 지표에 대조하세요.
