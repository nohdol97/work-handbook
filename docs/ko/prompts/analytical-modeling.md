---
id: prompts-analytical-modeling
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 분석 데이터 모델링 실무 프롬프트

기존 개념을 응용해 작성한 가상의 재사용 예시 6개다. 실제 업무 빈도나 실행 성능을 측정한 결과가 아니며, 새 학습 과정이나 실제 운영 경험으로 기록하지 않는다. [대괄호]를 비밀값 없는 맥락과 가상 데이터로 채운다. 모델의 제안은 검증할 작업 초안이다. 실제 production 실행 권한을 부여하지 않는다.

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

**상황:** Agent 실행·LLM 호출·사용자 event를 한 분석 테이블에 담을지 검토한다.

**LLM에 제공할 맥락:** Event 종류와 가상 샘플: [실행·호출·사용자 event] 질문·metric·집계 기간: [분석 요구] Key와 관계 cardinality: [가상 schema]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Event 종류와 가상 샘플: [실행·호출·사용자 event]
    질문·metric·집계 기간: [분석 요구]
    Key와 관계 cardinality: [가상 schema]

    [요청]
    각 후보 table의 한 행 의미를 먼저 한 문장으로 정의해 주세요.
    서로 다른 grain의 measure가 섞이는 지점을 찾아 주세요.
    필드 이름만으로 관계를 확정하지 말고 누락 근거를 적어 주세요.

    [출력]
    Table·grain·key·measure·dimension 후보 표를 주세요.
    여러 호출·호출 없음 사례의 기대 행 수를 주세요.

    [검증]
    가상 샘플을 한 행 정의에 맞춰 배치해 key 중복을 확인해 주세요.
    실제 분석 요구와 measure의 원래 집계 단위를 대조해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Event types and synthetic samples: [executions, calls, and user events]
    Questions, metrics, and reporting periods: [analysis needs]
    Keys and relationship cardinality: [synthetic schema]

    [Task]
    First define the meaning of one row in each candidate table.
    Find where measures at different grains become mixed.
    Do not infer relationships from names alone; list missing evidence.

    [Output]
    Return a table of candidate tables, grains, keys, measures, and dimensions.
    Provide expected row counts for several calls and no-call cases.

    [Checks]
    Map synthetic samples to row definitions and check duplicate keys.
    Compare actual analysis needs with each measure’s original aggregation unit.
    ```

**기대 결과:** Table·grain·key·measure·dimension 후보 표를 주세요. 여러 호출·호출 없음 사례의 기대 행 수를 주세요.

**LLM이 틀릴 수 있는 부분:** 편의를 위해 grain을 합치거나 execution_id가 모든 event의 unique key라고 볼 수 있다.

**검증 방법:** 가상 샘플을 한 행 정의에 맞춰 배치해 key 중복을 확인해 주세요. 실제 분석 요구와 measure의 원래 집계 단위를 대조해 주세요.

## SCD Type 2 유효 구간 join 검토 {#analytical-modeling-02}

**상황:** 고객 region 이력과 fact를 join한 뒤 경계 시점의 행이 두 번 나온다.

**LLM에 제공할 맥락:** 가상 natural·surrogate key와 valid_from·valid_to: [샘플] Fact 발생 시점과 join SQL: [가상 데이터·SQL] 유효 구간의 종료 경계·열린 구간 규칙: [정의]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 natural·surrogate key와 valid_from·valid_to: [샘플]
    Fact 발생 시점과 join SQL: [가상 데이터·SQL]
    유효 구간의 종료 경계·열린 구간 규칙: [정의]

    [요청]
    같은 natural key의 중첩·공백 구간을 구분해 주세요.
    Fact 시점에 대응하는 version 수를 계산해 주세요.
    현재 속성과 과거 속성 중 어떤 분석을 원하는지 불명확하면 표시해 주세요.

    [출력]
    Fact별 기대 version·실제 후보 수·불일치 이유 표를 주세요.
    경계 규칙을 보존하는 최소 join 수정 후보를 주세요.

    [검증]
    경계 직전·정확한 경계·직후·미매칭 가상 fact를 확인해 주세요.
    실제 유효 구간 규칙과 과거 분석 요구로 기대 version을 검증해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Synthetic natural and surrogate keys and valid_from and valid_to: [samples]
    Fact times and join SQL: [synthetic data and SQL]
    End-boundary and open-interval rules: [definitions]

    [Task]
    Separate overlaps and gaps for the same natural key.
    Count matching versions at each fact time.
    Flag unclear requirements about current versus historical attributes.

    [Output]
    Return expected versions, candidate counts, and mismatch reasons for each fact.
    Provide a minimal join change that preserves the boundary rule.

    [Checks]
    Check synthetic facts before, at, and after the boundary and with no match.
    Validate expected versions against actual interval rules and historical analysis needs.
    ```

**기대 결과:** Fact별 기대 version·실제 후보 수·불일치 이유 표를 주세요. 경계 규칙을 보존하는 최소 join 수정 후보를 주세요.

**LLM이 틀릴 수 있는 부분:** 최신 dimension 한 행만 고르거나 DISTINCT로 중첩 구간 문제를 숨길 수 있다.

**검증 방법:** 경계 직전·정확한 경계·직후·미매칭 가상 fact를 확인해 주세요. 실제 유효 구간 규칙과 과거 분석 요구로 기대 version을 검증해 주세요.

## 대시보드 error rate 정의 통일 {#analytical-modeling-03}

**상황:** 두 대시보드의 error rate가 다른데 metric 이름은 같다.

**LLM에 제공할 맥락:** 각 SQL·분자·분모·grain: [가상 정의] 기간·timezone·status 제외 조건: [조건] 분모 0 처리와 업무상 실패 정의: [규칙]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    각 SQL·분자·분모·grain: [가상 정의]
    기간·timezone·status 제외 조건: [조건]
    분모 0 처리와 업무상 실패 정의: [규칙]

    [요청]
    실행 단위와 호출 단위 metric이 섞였는지 검토해 주세요.
    분자와 분모의 대상 집합·기간·필터 차이를 비교해 주세요.
    정의 차이와 데이터 오류 가설을 분리해 주세요.

    [출력]
    Metric 계약 차이표와 합의가 필요한 업무 질문을 주세요.
    공통 정의 후보와 0 분모 포함 가상 기대 계산을 주세요.

    [검증]
    같은 가상 모집단에서 두 계산식을 손으로 검산해 주세요.
    확정된 업무 정의를 각 SQL·semantic layer 설정과 대조해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Each SQL, numerator, denominator, and grain: [synthetic definitions]
    Period, timezone, and status exclusions: [conditions]
    Zero-denominator handling and business failure definition: [rules]

    [Task]
    Check whether execution-level and call-level metrics are mixed.
    Compare populations, periods, and filters in each numerator and denominator.
    Separate definition differences from data-error hypotheses.

    [Output]
    Return a metric-contract comparison and business questions needing agreement.
    Provide a shared definition candidate and synthetic calculations including zero denominators.

    [Checks]
    Manually check both formulas on the same synthetic population.
    Compare agreed business definitions with each SQL and semantic-layer setting.
    ```

**기대 결과:** Metric 계약 차이표와 합의가 필요한 업무 질문을 주세요. 공통 정의 후보와 0 분모 포함 가상 기대 계산을 주세요.

**LLM이 틀릴 수 있는 부분:** 이름이 같으면 같은 metric으로 보거나 분모가 다른 비율을 그대로 비교할 수 있다.

**검증 방법:** 같은 가상 모집단에서 두 계산식을 손으로 검산해 주세요. 확정된 업무 정의를 각 SQL·semantic layer 설정과 대조해 주세요.

## 업무 질문에 맞는 fact 유형 선택 {#analytical-modeling-04}

**상황:** 주문 사건·일별 상태·배송 단계 소요 시간을 같은 구조로 볼지 결정한다.

**LLM에 제공할 맥락:** 분석 질문과 필요한 시간 기준: [요구] 주문 event와 일별 관측·단계 시각: [가상 샘플] 현재 schema·key·변경 방식: [정의]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    분석 질문과 필요한 시간 기준: [요구]
    주문 event와 일별 관측·단계 시각: [가상 샘플]
    현재 schema·key·변경 방식: [정의]

    [요청]
    Event·transaction·periodic·accumulating 후보를 요구별로 비교해 주세요.
    각 후보의 한 행 의미와 남기는 이력을 명시해 주세요.
    분류를 절대적·상호 배타적 제품 규칙으로 취급하지 말아 주세요.

    [출력]
    질문·fact 후보·grain·갱신 방식·누락 정보 표를 주세요.
    미완료 배송과 여러 상태 변경의 가상 표현을 주세요.

    [검증]
    각 가상 표현에서 원래 질문에 답할 수 있는지 확인해 주세요.
    실제 보존 이력과 milestone 시각의 의미를 대조해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Analysis questions and required time references: [requirements]
    Order events, daily observations, and milestone times: [synthetic samples]
    Current schema, keys, and update method: [definitions]

    [Task]
    Compare event, transaction, periodic, and accumulating candidates by requirement.
    State each candidate’s grain and retained history.
    Do not treat these categories as absolute, exclusive product rules.

    [Output]
    Return questions, fact candidates, grains, update methods, and missing information.
    Show synthetic representations for incomplete delivery and several state changes.

    [Checks]
    Check whether each synthetic representation answers the original question.
    Cross-check retained history and the meaning of milestone times.
    ```

**기대 결과:** 질문·fact 후보·grain·갱신 방식·누락 정보 표를 주세요. 미완료 배송과 여러 상태 변경의 가상 표현을 주세요.

**LLM이 틀릴 수 있는 부분:** 진행 상태 한 행만으로 모든 event 이력을 재구성하거나 일별 상태를 event와 섞을 수 있다.

**검증 방법:** 각 가상 표현에서 원래 질문에 답할 수 있는지 확인해 주세요. 실제 보존 이력과 milestone 시각의 의미를 대조해 주세요.

## Conformed dimension의 key·의미 정합성 {#analytical-modeling-05}

**상황:** 실행 fact와 호출 fact가 같은 team dimension을 공유하려 한다.

**LLM에 제공할 맥락:** Fact별 grain과 team의 업무 의미: [정의] Natural·surrogate key mapping과 이력 정책: [가상 schema] 미매칭·소속 변경 샘플과 분석 시점: [샘플·요구]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Fact별 grain과 team의 업무 의미: [정의]
    Natural·surrogate key mapping과 이력 정책: [가상 schema]
    미매칭·소속 변경 샘플과 분석 시점: [샘플·요구]

    [요청]
    이름이 같은 team 필드가 같은 개념과 key 규칙인지 확인해 주세요.
    현재 소속과 당시 소속의 차이를 fact별로 검토해 주세요.
    공유 가능한 정의와 합의되지 않은 의미를 나눠 주세요.

    [출력]
    Fact별 dimension 연결 계약과 key mapping 표를 주세요.
    공통 metric에 영향을 주는 미매칭·이력 경계 사례를 주세요.

    [검증]
    가상 소속 변경 전후 fact가 기대 version에 연결되는지 확인해 주세요.
    실제 업무 의미·key mapping·이력 규칙을 각 fact 소유자 기준과 대조해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Each fact’s grain and business meaning of team: [definitions]
    Natural and surrogate key mapping and history policy: [synthetic schema]
    Unmatched and changed-membership samples and analysis times: [samples and needs]

    [Task]
    Check whether same-named team fields share meaning and key rules.
    Review current versus historical membership for each fact.
    Separate definitions that can be shared from meanings still needing agreement.

    [Output]
    Return dimension-link contracts and key mappings for each fact.
    List unmatched and history-boundary cases that affect shared metrics.

    [Checks]
    Check expected dimension versions for facts before and after a synthetic membership change.
    Compare meaning, key mappings, and history rules with each fact owner’s requirements.
    ```

**기대 결과:** Fact별 dimension 연결 계약과 key mapping 표를 주세요. 공통 metric에 영향을 주는 미매칭·이력 경계 사례를 주세요.

**LLM이 틀릴 수 있는 부분:** 같은 key 이름만으로 의미를 통합하거나 현재 소속으로 모든 과거 fact를 바꿀 수 있다.

**검증 방법:** 가상 소속 변경 전후 fact가 기대 version에 연결되는지 확인해 주세요. 실제 업무 의미·key mapping·이력 규칙을 각 fact 소유자 기준과 대조해 주세요.

## 넓은 테이블의 denormalization 범위 검토 {#analytical-modeling-06}

**상황:** 조회 편의를 위해 주문·항목·고객 이력을 한 테이블로 합치려 한다.

**LLM에 제공할 맥락:** 후보 column·원본 grain·갱신 주기: [설계] 대표 조회와 필요한 과거 속성: [가상 SQL·요구] Join cardinality와 유지보수 제약: [정의]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    후보 column·원본 grain·갱신 주기: [설계]
    대표 조회와 필요한 과거 속성: [가상 SQL·요구]
    Join cardinality와 유지보수 제약: [정의]

    [요청]
    기존 설계를 평가하고 반복 measure와 혼합 이력 지점을 찾아 주세요.
    조회 편의·join 감소와 갱신·이력 관리 비용을 비교해 주세요.
    측정 없이 성능 향상을 확정하지 말아 주세요.

    [출력]
    Column별 grain·반복 허용·집계 제약·갱신 책임 표를 주세요.
    유지할 분리 경계와 작은 비교 검증 계획을 주세요.

    [검증]
    여러 항목·속성 변경 가상 데이터로 합계와 과거 속성을 확인해 주세요.
    실제 query plan과 유지보수 요구로 설계 가정을 검증해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Candidate columns, source grains, and update intervals: [design]
    Typical queries and required historical attributes: [synthetic SQL and needs]
    Join cardinality and maintenance constraints: [definitions]

    [Task]
    Assess the current design and locate repeated measures and mixed history.
    Compare simpler queries and fewer joins with update and history costs.
    Do not claim a performance gain without measurement.

    [Output]
    Return each column’s grain, allowed repetition, aggregation limits, and update owner.
    Propose boundaries to retain and a small comparison plan.

    [Checks]
    Check totals and past attributes with synthetic multi-item and attribute-change data.
    Validate design assumptions with actual query plans and maintenance requirements.
    ```

**기대 결과:** Column별 grain·반복 허용·집계 제약·갱신 책임 표를 주세요. 유지할 분리 경계와 작은 비교 검증 계획을 주세요.

**LLM이 틀릴 수 있는 부분:** 한 테이블이 항상 빠르다고 하거나 grain이 다른 금액을 그대로 합산할 수 있다.

**검증 방법:** 여러 항목·속성 변경 가상 데이터로 합계와 과거 속성을 확인해 주세요. 실제 query plan과 유지보수 요구로 설계 가정을 검증해 주세요.
