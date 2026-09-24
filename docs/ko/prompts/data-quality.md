---
id: prompts-data-quality
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 데이터 품질 실무 프롬프트

기존 학습 개념에서 파생해 작성한 재사용 가능한 가상 실무 예시다. 모델 호출·실제 운영·실험을 수행한 기록이 아니다. 대괄호 입력을 공개 가능한 비식별 정보로 채우고, 결과를 가설과 초안으로 검토한다.

[개념 문서](../data-platform/data-quality.md) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [계층별 품질 검사 배치](#data-quality-01) |
| 02 | [필수 값과 참조 관계 오류 구분](#data-quality-02) |
| 03 | [격리 데이터 재처리 준비](#data-quality-03) |
| 04 | [품질 SLO 측정 정의 작성](#data-quality-04) |
| 05 | [호출 비용과 청구 합계 대조](#data-quality-05) |
| 06 | [재처리 후 소비 재개 조건](#data-quality-06) |

## 계층별 품질 검사 배치 {#data-quality-01}

**상황:** 신규 호출 데이터셋에 어떤 품질 검사를 어느 계층에 둘지 정한다.

**LLM에 제공할 맥락:** 스키마·필수 필드·이벤트 grain: [비식별 정의] / Ingestion·Silver·Gold 변환과 KPI 요구: [목록]

**예시 프롬프트:**

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

**기대 결과:** 계층 / 규칙 / 실패 예시 / 담당자 / 확인 증거 표를 주세요.

**LLM 오류 가능성:** 형식이 맞으면 정확하다고 단정하거나 앞 계층 검사로 Gold 검증을 생략할 수 있다.

**검증 방법:** 각 규칙에 정상·오류 가상 레코드를 대입하고 KPI 요구와 대조하세요.

## 필수 값과 참조 관계 오류 구분 {#data-quality-02}

**상황:** model_id 오류가 필수 값 누락인지 참조 테이블 불일치인지 분류한다.

**LLM에 제공할 맥락:** 호출·모델 테이블 grain과 키: [스키마] / NULL·미참조 키·허용 상태 집계: [측정 구간과 값]

**예시 프롬프트:**

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

**기대 결과:** 검사 / 검출 대상 / 놓치는 오류 / 추가 증거 표를 주세요.

**LLM 오류 가능성:** NULL 제거를 참조 일관성 해결로 오해하거나 유일성 grain을 임의로 정할 수 있다.

**검증 방법:** 제공된 키 정의와 가상 실패 레코드로 검사 범위를 확인하세요.

## 격리 데이터 재처리 준비 {#data-quality-03}

**상황:** 격리 레코드가 누적되어 수정 후 재처리 순서를 준비한다.

**LLM에 제공할 맥락:** 오류 유형별 건수·수신 구간·수정 이력: [요약] / 격리 필드·이벤트 키·접근 및 보관 규칙: [비식별 정의]

**예시 프롬프트:**

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

**기대 결과:** 대상 구간 / 선행 조건 / 중단 조건 / 재검사 / 남은 격리 표를 주세요.

**LLM 오류 가능성:** 격리 전체를 무조건 다시 넣거나 raw payload를 공개해도 된다고 여길 수 있다.

**검증 방법:** 격리 전후 건수와 오류 사유·중복률을 비교하고 원문 노출 없이 확인하세요.

## 품질 SLO 측정 정의 작성 {#data-quality-04}

**상황:** 두 소비자가 같은 데이터셋에 서로 다른 최신성 목표를 요구한다.

**LLM에 제공할 맥락:** 대시보드·보고서 업무 마감과 허용 지연: [요구사항] / 시각 필드·필수 값·중복 키·측정 구간: [정의]

**예시 프롬프트:**

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

**기대 결과:** 소비자 / SLI 식 / 구간 / 제안 목표 / 합의 질문 표를 주세요.

**LLM 오류 가능성:** 문서의 5분·99.9% 같은 가상 수치를 승인된 기본값으로 사용할 수 있다.

**검증 방법:** 가상 측정치로 식을 계산하고 업무 담당자 요구와 목표를 대조하세요.

## 호출 비용과 청구 합계 대조 {#data-quality-05}

**상황:** 비용 필드가 모두 유효하지만 호출 합계와 청구 합계가 다르다.

**LLM에 제공할 맥락:** 호출 비용 집계·청구 요약: [동일 구간의 비식별 값] / 통화·단위·집계 grain·중복 검사·마감 시각: [정의]

**예시 프롬프트:**

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

**기대 결과:** 차이 구간 / 가능한 설명 / 지지·반박 증거 / 다음 대조 표를 주세요.

**LLM 오류 가능성:** 청구서와 다른 값을 모두 잘못된 호출 기록으로 단정할 수 있다.

**검증 방법:** 같은 범위·단위·마감 기준으로 집계를 다시 비교하고 미확인 금액을 남기세요.

## 재처리 후 소비 재개 조건 {#data-quality-06}

**상황:** 오류 데이터를 재처리한 뒤 대시보드를 다시 열지 검토한다.

**LLM에 제공할 맥락:** 영향 partition·수정 내용·재처리 실행 결과: [요약] / 전후 품질 지표·KPI 합계·downstream 목록: [증거]

**예시 프롬프트:**

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

**기대 결과:** 소비자 / 복구 증거 / 미충족 검사 / 재개 조건 / 담당자 표를 주세요.

**LLM 오류 가능성:** 작업 성공만으로 중복·누락·downstream 집계 오류가 해결됐다고 말할 수 있다.

**검증 방법:** 영향 범위의 품질 검사와 소비자 집계를 대조하고 담당자가 재개를 판단하게 하세요.
