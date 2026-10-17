---
id: prompts-analytical-modeling
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 분석 데이터 모델링 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../data-platform/analytical-modeling.md) · [전체 프롬프트 모음](index.md)

| # | 상황 바로 가기 |
| --- | --- |
| 01 | [새 분석 테이블의 grain 정의](#analytical-modeling-01) |
| 02 | [SCD Type 2 유효 구간 join 검토](#analytical-modeling-02) |
| 03 | [대시보드 error rate 정의 통일](#analytical-modeling-03) |
| 04 | [업무 질문에 맞는 fact 유형 선택](#analytical-modeling-04) |
| 05 | [Conformed dimension의 key·의미 정합성](#analytical-modeling-05) |
| 06 | [넓은 테이블의 denormalization 범위 검토](#analytical-modeling-06) |

## 새 분석 테이블의 grain 정의 {#analytical-modeling-01}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Agent 실행·LLM 호출·사용자 event를 한 분석 테이블에 담을지 검토 중이야.
    각 후보 table의 한 행 의미를 먼저 한 문장으로 정의해 주세요.
    서로 다른 grain의 measure가 섞이는 지점을 찾아 주세요.
    필드 이름만으로 관계를 확정하지 말고 누락 근거를 적어 주세요.
    Table·grain·key·measure·dimension 후보 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Review whether agent executions, LLM calls, and user events belong in one analytical table.
    First define the meaning of one row in each candidate table.
    Find where measures at different grains become mixed.
    Do not infer relationships from names alone; list missing evidence.
    Return a table of candidate tables, grains, keys, measures, and dimensions.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 한 행의 업무 의미와 key별 관계 cardinality. 기대 결과를 손으로 계산할 수 있는 작은 반례를 함께 준비한다. 편의를 위해 grain을 합치거나 execution_id가 모든 event의 unique key라고 볼 수 있다. 여러 호출과 호출 없는 실행이 각각 의도한 행 수를 가져야 한다.

## SCD Type 2 유효 구간 join 검토 {#analytical-modeling-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    고객 region 이력과 fact를 join한 뒤 경계 시점의 행이 두 번 나온다.
    같은 natural key의 중첩·공백 구간을 구분해 주세요.
    Fact 시점에 대응하는 version 수를 계산해 주세요.
    현재 속성과 과거 속성 중 어떤 분석을 원하는지 불명확하면 표시해 주세요.
    Fact별 기대 version·실제 후보 수·불일치 이유 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Joining customer region history to facts produces two rows at a validity boundary.
    Separate overlaps and gaps for the same natural key.
    Count matching versions at each fact time.
    Flag unclear requirements about current versus historical attributes.
    Return expected versions, candidate counts, and mismatch reasons for each fact.
    ```

**핵심 사항:** 판단 전에 확인할 근거: valid_to 경계 포함 여부와 분석할 과거 시점. 기대 결과를 손으로 계산할 수 있는 작은 반례를 함께 준비한다. 최신 dimension 한 행만 고르거나 DISTINCT로 중첩 구간 문제를 숨길 수 있다. 경계 직전·정확한 경계·직후 모두 기대 version과 맞아야 한다.

## 대시보드 error rate 정의 통일 {#analytical-modeling-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    두 대시보드의 error rate가 다른데 metric 이름은 같다.
    실행 단위와 호출 단위 metric이 섞였는지 검토해 주세요.
    분자와 분모의 대상 집합·기간·필터 차이를 비교해 주세요.
    정의 차이와 데이터 오류 가설을 분리해 주세요.
    Metric 계약 차이표와 합의가 필요한 업무 질문을 주세요.
    ```

=== "English"

    ```text {.prompt}
    Two dashboards show different error rates under the same metric name.
    Check whether execution-level and call-level metrics are mixed.
    Compare populations, periods, and filters in each numerator and denominator.
    Separate definition differences from data-error hypotheses.
    Return a metric-contract comparison and business questions needing agreement.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 업무상 실패 정의와 분모의 대상 집합. 기대 결과를 손으로 계산할 수 있는 작은 반례를 함께 준비한다. 이름이 같으면 같은 metric으로 보거나 분모가 다른 비율을 그대로 비교할 수 있다. 분모 0·재시도·제외 status의 해석까지 합의해야 한다.

## 업무 질문에 맞는 fact 유형 선택 {#analytical-modeling-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    주문 사건·일별 상태·배송 단계 소요 시간을 같은 구조로 볼지 결정한다.
    Event·transaction·periodic·accumulating 후보를 요구별로 비교해 주세요.
    각 후보의 한 행 의미와 남기는 이력을 명시해 주세요.
    분류를 절대적·상호 배타적 제품 규칙으로 취급하지 말아 주세요.
    질문·fact 후보·grain·갱신 방식·누락 정보 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Decide how to model order events, daily state, and time across delivery milestones.
    Compare event, transaction, periodic, and accumulating candidates by requirement.
    State each candidate’s grain and retained history.
    Do not treat these categories as absolute, exclusive product rules.
    Return questions, fact candidates, grains, update methods, and missing information.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 질문별로 보존해야 할 사건·일별 상태·milestone 시각. 기대 결과를 손으로 계산할 수 있는 작은 반례를 함께 준비한다. 진행 상태 한 행만으로 모든 event 이력을 재구성하거나 일별 상태를 event와 섞을 수 있다. 현재 상태만으로 과거 사건 순서를 복원하는 설계는 보류한다.

## Conformed dimension의 key·의미 정합성 {#analytical-modeling-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    실행 fact와 호출 fact가 같은 team dimension을 공유하려 한다.
    이름이 같은 team 필드가 같은 개념과 key 규칙인지 확인해 주세요.
    현재 소속과 당시 소속의 차이를 fact별로 검토해 주세요.
    공유 가능한 정의와 합의되지 않은 의미를 나눠 주세요.
    Fact별 dimension 연결 계약과 key mapping 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Execution and call facts are intended to share one team dimension.
    Check whether same-named team fields share meaning and key rules.
    Review current versus historical membership for each fact.
    Separate definitions that can be shared from meanings still needing agreement.
    Return dimension-link contracts and key mappings for each fact.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 공유 dimension의 업무 의미와 과거 소속 적용 규칙. 기대 결과를 손으로 계산할 수 있는 작은 반례를 함께 준비한다. 같은 key 이름만으로 의미를 통합하거나 현재 소속으로 모든 과거 fact를 바꿀 수 있다. 같은 이름의 team을 합치기 전에 시점별 소속이 일치하는지 확인한다.

## 넓은 테이블의 denormalization 범위 검토 {#analytical-modeling-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    조회 편의를 위해 주문·항목·고객 이력을 한 테이블로 합치려 한다.
    기존 설계를 평가하고 반복 measure와 혼합 이력 지점을 찾아 주세요.
    조회 편의·join 감소와 갱신·이력 관리 비용을 비교해 주세요.
    측정 없이 성능 향상을 확정하지 말아 주세요.
    Column별 grain·반복 허용·집계 제약·갱신 책임 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    A wide table is proposed to combine orders, items, and customer history for easier queries.
    Assess the current design and locate repeated measures and mixed history.
    Compare simpler queries and fewer joins with update and history costs.
    Do not claim a performance gain without measurement.
    Return each column’s grain, allowed repetition, aggregation limits, and update owner.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 대표 조회의 grain과 반복 measure 허용 범위. 기대 결과를 손으로 계산할 수 있는 작은 반례를 함께 준비한다. 한 테이블이 항상 빠르다고 하거나 grain이 다른 금액을 그대로 합산할 수 있다. 조회 단축과 함께 이력 정확성·갱신 비용이 검증되어야 한다.
