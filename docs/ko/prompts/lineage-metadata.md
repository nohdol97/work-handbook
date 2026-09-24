---
id: prompts-lineage-metadata
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Lineage와 metadata 실무 프롬프트

기존 학습 개념에서 파생해 작성한 재사용 가능한 가상 실무 예시다. 모델 호출·실제 운영·실험을 수행한 기록이 아니다. 대괄호 입력을 공개 가능한 비식별 정보로 채우고, 결과를 가설과 초안으로 검토한다.

[개념 문서](../data-platform/lineage-metadata.md) · [프롬프트 모음](index.md)

| 사례 | 바로가기 |
| --- | --- |
| 01 | [catalog 등록 정보의 빈칸 찾기](#lineage-metadata-01) |
| 02 | [KPI 설명과 계산 정의 맞추기](#lineage-metadata-02) |
| 03 | [실행 기록과 lineage 수집 누락 대조](#lineage-metadata-03) |
| 04 | [KPI 오류를 upstream으로 추적](#lineage-metadata-04) |
| 05 | [민감 column의 파생 경로 조사](#lineage-metadata-05) |
| 06 | [catalog 정보의 출처와 충돌 정리](#lineage-metadata-06) |

## catalog 등록 정보의 빈칸 찾기 {#lineage-metadata-01}

**상황:** 새 테이블의 catalog 항목이 schema만 있어 사용자가 의미와 상태를 알기 어렵다.

**LLM에 제공할 맥락:** 테이블·column·type·partition·format: [정의] / 갱신·건수·job·설명·owner·KPI·분류: [알려진 값과 빈칸]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    테이블·column·type·partition·format: [정의]
    갱신·건수·job·설명·owner·KPI·분류: [알려진 값과 빈칸]
    [요청]
    Technical·Operational·Business metadata로 항목을 분류하세요.
    추측으로 채우지 말고 빈칸별 확인할 정보 출처를 지정하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    항목 / 분류 / 현재 근거 / 누락 / 확인 대상 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 schema·실행 기록·승인된 업무 정의와 항목을 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Table, columns, types, partitions, and format: [definitions]
    Updates, counts, jobs, description, owner, KPIs, and classification: [known values and gaps]
    [Task]
    Group fields into technical, operational, and business metadata.
    Do not invent missing values; name the source to check for each gap.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of field, category, current evidence, gap, and source to check.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare entries with real schemas, run records, and approved business definitions.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 항목 / 분류 / 현재 근거 / 누락 / 확인 대상 표를 주세요.

**LLM 오류 가능성:** column 이름에서 KPI 의미나 소유자를 지어낼 수 있다.

**검증 방법:** 실제 schema·실행 기록·승인된 업무 정의와 항목을 대조하세요.

## KPI 설명과 계산 정의 맞추기 {#lineage-metadata-02}

**상황:** Revenue 설명은 같지만 두 대시보드의 합계가 다르다.

**LLM에 제공할 맥락:** 업무 정의·VAT·refund 처리 합의: [문서 발췌] / 두 계산식·grain·기간·통화·변환 경로: [비식별 정의]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    업무 정의·VAT·refund 처리 합의: [문서 발췌]
    두 계산식·grain·기간·통화·변환 경로: [비식별 정의]
    [요청]
    Business metadata의 설명과 실행 가능한 metric 정의를 분리하세요.
    중복 차감·범위·grain 차이를 점검하고 아직 합의되지 않은 의미를 찾으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    정의 항목 / 계산 A / 계산 B / 차이 근거 / 담당자 질문 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    동일 가상 입력에 두 식을 적용하고 승인된 업무 정의와 비교하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Business definition and agreed VAT and refund treatment: [excerpts]
    Both formulas, grains, periods, currencies, and transformations: [sanitized definitions]
    [Task]
    Separate business descriptions from executable metric definitions.
    Check double subtraction, scope, and grain differences, and find unsettled meanings.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of definition, calculation A, calculation B, evidence of differences, and owner questions.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Apply both formulas to the same synthetic inputs and compare with the approved definition.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 정의 항목 / 계산 A / 계산 B / 차이 근거 / 담당자 질문 표를 주세요.

**LLM 오류 가능성:** 설명 한 문장만으로 회계 규칙이나 올바른 식을 확정할 수 있다.

**검증 방법:** 동일 가상 입력에 두 식을 적용하고 승인된 업무 정의와 비교하세요.

## 실행 기록과 lineage 수집 누락 대조 {#lineage-metadata-03}

**상황:** 실행은 있었는데 lineage 화면에 일부 경로가 보이지 않는다.

**LLM에 제공할 맥락:** job 정의·run 이력·입출력 dataset: [비식별 목록] / 수집 이벤트·수집 시각·연동 대상·알려진 누락: [기록]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    job 정의·run 이력·입출력 dataset: [비식별 목록]
    수집 이벤트·수집 시각·연동 대상·알려진 누락: [기록]
    [요청]
    Job·Run·Dataset 식별자를 구분해 실제 실행과 이벤트를 대조하세요.
    run에 연결되지 않는 metadata event도 고려해 누락 후보를 찾으세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    실행 또는 metadata / 기대 정보 / 수집 증거 / 미확인 구간 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 실행 로그·이벤트 원본·조회 결과를 같은 식별자로 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Job definitions, run history, and input/output datasets: [sanitized list]
    Collected events, collection times, integrations, and known gaps: [record]
    [Task]
    Separate Job, Run, and Dataset identifiers and compare runs with events.
    Account for metadata events without runs when finding possible gaps.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of run or metadata, expected information, collection evidence, and unknown scope.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare run logs, event records, and query results using the same identifiers.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 실행 또는 metadata / 기대 정보 / 수집 증거 / 미확인 구간 표를 주세요.

**LLM 오류 가능성:** 모든 event를 run으로 세거나 화면에 없으면 실행도 없었다고 볼 수 있다.

**검증 방법:** 실제 실행 로그·이벤트 원본·조회 결과를 같은 식별자로 대조하세요.

## KPI 오류를 upstream으로 추적 {#lineage-metadata-04}

**상황:** 매출 KPI가 틀렸지만 어느 변환부터 값이 달라졌는지 모른다.

**LLM에 제공할 맥락:** KPI·dataset·column lineage와 변환식: [비식별 경로] / 같은 구간의 단계별 값·run 상태·품질 결과: [증거]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    KPI·dataset·column lineage와 변환식: [비식별 경로]
    같은 구간의 단계별 값·run 상태·품질 결과: [증거]
    [요청]
    대시보드에서 원본 방향으로 확인 경로를 정리하세요.
    연결이 있다는 사실과 특정 run이 정확했다는 증거를 구분하세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    상류 단계 / 비교할 값 / 의심 변환 / 반박할 증거 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    동일 grain·기간의 중간 결과와 실제 SQL을 단계별로 대조하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    KPI, dataset and column lineage, and formulas: [sanitized paths]
    Stage values, run states, and quality results for one window: [evidence]
    [Task]
    Order checks from the dashboard back toward the source.
    Separate an existing graph edge from evidence that a run was correct.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of upstream stage, values to compare, suspect transformation, and evidence against it.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare intermediate results and actual SQL at the same grain and time period.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 상류 단계 / 비교할 값 / 의심 변환 / 반박할 증거 표를 주세요.

**LLM 오류 가능성:** 처음 보이는 upstream을 원인으로 단정하거나 table 연결만으로 column 계산을 추정할 수 있다.

**검증 방법:** 동일 grain·기간의 중간 결과와 실제 SQL을 단계별로 대조하세요.

## 민감 column의 파생 경로 조사 {#lineage-metadata-05}

**상황:** 민감 column이 어떤 파생 테이블과 KPI로 전달되는지 확인한다.

**LLM에 제공할 맥락:** column 분류·table 및 column lineage: [비식별 metadata] / 변환식·consumer 목록·수집 범위: [확인된 정보]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    column 분류·table 및 column lineage: [비식별 metadata]
    변환식·consumer 목록·수집 범위: [확인된 정보]
    [요청]
    직접 전달·변환·집계 경로를 구분하고 알 수 없는 구간을 남기세요.
    그래프 정보와 접근 정책의 실제 적용 증거를 혼동하지 마세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    파생 대상 / 입력 column / 변환 / 분류 확인 / 누락 근거 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    실제 변환식·분류 정책·consumer 목록을 대조하고 미수집 경로를 별도 확인하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Column classification and table/column lineage: [sanitized metadata]
    Transformations, consumers, and collection scope: [confirmed information]
    [Task]
    Separate direct, transformed, and aggregated paths and mark unknown segments.
    Do not confuse graph information with proof that access policies are enforced.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of target, input column, transformation, classification check, and missing evidence.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare formulas, classification policy, and consumers, then inspect paths not collected.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 파생 대상 / 입력 column / 변환 / 분류 확인 / 누락 근거 표를 주세요.

**LLM 오류 가능성:** 집계됐다는 이유로 민감성이 사라졌다고 단정하거나 lineage 누락을 무영향으로 볼 수 있다.

**검증 방법:** 실제 변환식·분류 정책·consumer 목록을 대조하고 미수집 경로를 별도 확인하세요.

## catalog 정보의 출처와 충돌 정리 {#lineage-metadata-06}

**상황:** catalog의 owner·freshness·의존성 정보가 각 원본 시스템과 다르다.

**LLM에 제공할 맥락:** Iceberg·dbt·Airflow·lineage·품질 도구의 항목: [비식별 값] / 각 항목 수집 시각·갱신 책임·현재 catalog 값: [기록]

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Iceberg·dbt·Airflow·lineage·품질 도구의 항목: [비식별 값]
    각 항목 수집 시각·갱신 책임·현재 catalog 값: [기록]
    [요청]
    구조·문서·실행·계보·품질 정보의 원본을 구분하세요.
    수집 지연과 의미 차이 가설을 나누고 임의로 값을 덮어쓰지 마세요.
    관찰·가정·가설·누락 근거를 구분하세요.
    [출력]
    항목 / 원본 / 충돌 값 / 갱신 시각 / 조정할 담당자 표를 주세요.
    불확실한 항목과 담당자가 다음에 확인할 순서를 적으세요.
    [검증]
    원본 metadata와 수집 기록을 대조하고 담당자가 정의를 확인하게 하세요.
    위 검증은 계획이며 실행했다고 주장하지 마세요.
    실제 시스템 변경·데이터 삭제·외부 전송은 실행하지 마세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Entries from Iceberg, dbt, Airflow, lineage, and quality tools: [sanitized values]
    Collection times, update owners, and current catalog values: [record]
    [Task]
    Separate sources for structure, docs, runs, lineage, and quality.
    Separate collection-delay and meaning-difference hypotheses; do not overwrite values.
    Separate observations, assumptions, hypotheses, and missing evidence.
    [Output]
    Give a table of field, source, conflicting values, update time, and owner to consult.
    List uncertainties and the order of checks for the owner.
    [Checks]
    Compare source metadata and collection records, and have owners confirm definitions.
    These checks are a plan; do not claim they were run.
    Do not change systems, delete data, or send data externally.
    ```

**기대 결과:** 항목 / 원본 / 충돌 값 / 갱신 시각 / 조정할 담당자 표를 주세요.

**LLM 오류 가능성:** 가장 최근 값을 무조건 정답으로 보거나 catalog 표시를 정책 강제로 오해할 수 있다.

**검증 방법:** 원본 metadata와 수집 기록을 대조하고 담당자가 정의를 확인하게 하세요.
