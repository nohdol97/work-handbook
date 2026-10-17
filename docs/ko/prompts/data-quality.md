---
id: prompts-data-quality
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 데이터 품질 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

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

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    신규 호출 데이터셋에 어떤 품질 검사를 어느 계층에 둘지 정한다.
    완전성·유일성·유효성·일관성·최신성·정확성·양을 검토하세요.
    각 규칙을 계층에 배치하고 뒤 계층에도 필요한 검사를 설명하세요.
    계층 / 규칙 / 실패 예시 / 담당자 / 확인 증거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Decide which quality checks belong in each layer of a new call dataset.
    Review completeness, uniqueness, validity, consistency, freshness, accuracy, and volume.
    Place each rule in a layer and explain which later checks are still needed.
    Give a table of layer, rule, failure example, owner, and evidence.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 데이터셋 grain과 소비자가 승인한 품질 요구. 정상·오류 표본을 구분하고 업무 담당자가 정한 기대 결과를 붙인다. 형식이 맞으면 정확하다고 단정하거나 앞 계층 검사로 Gold 검증을 생략할 수 있다. 앞 계층 통과가 뒤 계층 업무 계산의 정확성을 대신하지 않아야 한다.

## 필수 값과 참조 관계 오류 구분 {#data-quality-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    model_id 오류가 필수 값 누락인지 참조 테이블 불일치인지 분류한다.
    not_null·relationships·accepted_values·unique 검사의 역할을 나누세요.
    각 실패에서 확인할 레코드와 참조 데이터 갱신 시각을 지정하세요.
    검사 / 검출 대상 / 놓치는 오류 / 추가 증거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Classify model_id errors as missing required values or broken table references.
    Separate the roles of not_null, relationships, accepted_values, and unique checks.
    State which records and reference refresh times to inspect for each failure.
    Give a table of check, detected error, missed error, and further evidence.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 참조 table의 기준 시점과 key NULL 허용 규칙. 정상·오류 표본을 구분하고 업무 담당자가 정한 기대 결과를 붙인다. NULL 제거를 참조 일관성 해결로 오해하거나 유일성 grain을 임의로 정할 수 있다. 참조 갱신 지연 때문에 정상 데이터를 잘못 거부하지 않는지 확인한다.

## 격리 데이터 재처리 준비 {#data-quality-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    격리 레코드가 누적되어 수정 후 재처리 순서를 준비한다.
    수정으로 해결된 유형과 아직 해결되지 않은 유형을 구분하세요.
    검증 경로 재진입과 중복 확인을 포함한 재처리 순서를 제안하세요.
    대상 구간 / 선행 조건 / 중단 조건 / 재검사 / 남은 격리 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Quarantined records are growing, so prepare a reprocessing sequence after a fix.
    Separate error types covered by the fix from those still unresolved.
    Propose reprocessing through validation again, including duplicate checks.
    Give a table of scope, prerequisites, stop conditions, rechecks, and remaining quarantine.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 수정이 적용된 오류 유형과 replay 가능한 원본 구간. 정상·오류 표본을 구분하고 업무 담당자가 정한 기대 결과를 붙인다. 격리 전체를 무조건 다시 넣거나 raw payload를 공개해도 된다고 여길 수 있다. 해결 안 된 오류를 다시 흘려보내거나 raw payload를 공개하지 않는다.

## 품질 SLO 측정 정의 작성 {#data-quality-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    두 소비자가 같은 데이터셋에 서로 다른 최신성 목표를 요구한다.
    SLI 측정 정의와 제안 SLO 목표를 분리하세요.
    최신성·완전성·중복률의 시간 기준과 분모를 명시하세요.
    소비자 / SLI 식 / 구간 / 제안 목표 / 합의 질문 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Two consumers need different freshness targets for the same dataset.
    Separate SLI measurement definitions from proposed SLO targets.
    State the clocks and denominators for freshness, completeness, and duplicate rate.
    Give a table of consumer, SLI formula, window, proposed target, and agreement questions.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 소비자별 마감·허용 지연과 측정 분모. 정상·오류 표본을 구분하고 업무 담당자가 정한 기대 결과를 붙인다. 문서의 5분·99.9% 같은 가상 수치를 승인된 기본값으로 사용할 수 있다. 예시 수치를 승인된 목표로 사용하지 않고 담당자 합의를 남긴다.

## 호출 비용과 청구 합계 대조 {#data-quality-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    비용 필드가 모두 유효하지만 호출 합계와 청구 합계가 다르다.
    유효성 통과와 실제 금액의 정확성을 구분하세요.
    기간·단위·중복·도착 지연 가설별 대조 순서를 제시하세요.
    차이 구간 / 가능한 설명 / 지지·반박 증거 / 다음 대조 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Cost fields are valid, but call totals differ from billing totals.
    Separate valid values from accurate amounts.
    Order checks for window, unit, duplicate, and late-arrival hypotheses.
    Give a table of difference, possible explanation, supporting or opposing evidence, and next check.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 양쪽 금액의 통화·마감·과금 범위. 정상·오류 표본을 구분하고 업무 담당자가 정한 기대 결과를 붙인다. 청구서와 다른 값을 모두 잘못된 호출 기록으로 단정할 수 있다. 근거 없이 차액을 보정하거나 한쪽 금액을 정답으로 고정하지 않는다.

## 재처리 후 소비 재개 조건 {#data-quality-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    오류 데이터를 재처리한 뒤 대시보드를 다시 열지 검토 중이야.
    Detect·Contain·Fix·Reprocess·Verify 단계별 완료 근거를 점검하세요.
    작업 성공과 데이터 복구를 구분하고 재개 보류 조건을 찾으세요.
    소비자 / 복구 증거 / 미충족 검사 / 재개 조건 / 담당자 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review whether a dashboard can resume after bad data was reprocessed.
    Check completion evidence for Detect, Contain, Fix, Reprocess, and Verify.
    Separate job success from data recovery and identify reasons to hold use.
    Give a table of consumer, recovery evidence, failed checks, resume criteria, and owner.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 영향 partition 전체의 검사 결과와 소비자별 재개 기준. 정상·오류 표본을 구분하고 업무 담당자가 정한 기대 결과를 붙인다. 작업 성공만으로 중복·누락·downstream 집계 오류가 해결됐다고 말할 수 있다. 성공한 재처리 job만으로 재개하지 않고 소비 결과까지 대조한다.
