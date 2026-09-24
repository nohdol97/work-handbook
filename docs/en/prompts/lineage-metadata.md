---
id: prompts-lineage-metadata
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Lineage and metadata practical prompts

These reusable, hypothetical work examples were authored from existing study concepts. They are not records of model runs, production work, or experiments. Fill placeholders with sanitized information safe to share. Treat results as hypotheses and drafts.

[Concept guide](../data-platform/lineage-metadata.md) · [Prompt library](index.md)

| Case | Jump to example |
| --- | --- |
| 01 | [Find gaps in a catalog entry](#lineage-metadata-01) |
| 02 | [Align KPI descriptions and calculations](#lineage-metadata-02) |
| 03 | [Compare job runs with lineage collection](#lineage-metadata-03) |
| 04 | [Trace a KPI error upstream](#lineage-metadata-04) |
| 05 | [Trace derived paths from a sensitive column](#lineage-metadata-05) |
| 06 | [Resolve catalog metadata sources and conflicts](#lineage-metadata-06) |

## Find gaps in a catalog entry {#lineage-metadata-01}

**Situation:** A new catalog entry lists only a schema, so users cannot understand its meaning or health.

**Context to Give the LLM:** Table, columns, types, partitions, and format: [definitions] / Updates, counts, jobs, description, owner, KPIs, and classification: [known values and gaps]

**Example Prompt:**

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

**Expected Output:** Give a table of field, category, current evidence, gap, and source to check.

**What the LLM Can Get Wrong:** It may invent KPI meaning or ownership from column names.

**How to Validate:** Compare entries with real schemas, run records, and approved business definitions.

## Align KPI descriptions and calculations {#lineage-metadata-02}

**Situation:** Two dashboards describe Revenue the same way but show different totals.

**Context to Give the LLM:** Business definition and agreed VAT and refund treatment: [excerpts] / Both formulas, grains, periods, currencies, and transformations: [sanitized definitions]

**Example Prompt:**

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

**Expected Output:** Give a table of definition, calculation A, calculation B, evidence of differences, and owner questions.

**What the LLM Can Get Wrong:** It may infer accounting rules or a correct formula from one description.

**How to Validate:** Apply both formulas to the same synthetic inputs and compare with the approved definition.

## Compare job runs with lineage collection {#lineage-metadata-03}

**Situation:** Jobs ran, but some paths are absent from the lineage view.

**Context to Give the LLM:** Job definitions, run history, and input/output datasets: [sanitized list] / Collected events, collection times, integrations, and known gaps: [record]

**Example Prompt:**

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

**Expected Output:** Give a table of run or metadata, expected information, collection evidence, and unknown scope.

**What the LLM Can Get Wrong:** It may count every event as a run or assume an absent path never ran.

**How to Validate:** Compare run logs, event records, and query results using the same identifiers.

## Trace a KPI error upstream {#lineage-metadata-04}

**Situation:** A sales KPI is wrong, but the first transformation with a wrong value is unknown.

**Context to Give the LLM:** KPI, dataset and column lineage, and formulas: [sanitized paths] / Stage values, run states, and quality results for one window: [evidence]

**Example Prompt:**

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

**Expected Output:** Give a table of upstream stage, values to compare, suspect transformation, and evidence against it.

**What the LLM Can Get Wrong:** It may blame the first upstream node or infer column logic from a table edge.

**How to Validate:** Compare intermediate results and actual SQL at the same grain and time period.

## Trace derived paths from a sensitive column {#lineage-metadata-05}

**Situation:** Check which derived tables and KPIs use a sensitive column.

**Context to Give the LLM:** Column classification and table/column lineage: [sanitized metadata] / Transformations, consumers, and collection scope: [confirmed information]

**Example Prompt:**

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

**Expected Output:** Give a table of target, input column, transformation, classification check, and missing evidence.

**What the LLM Can Get Wrong:** It may assume aggregation removes sensitivity or missing lineage means no impact.

**How to Validate:** Compare formulas, classification policy, and consumers, then inspect paths not collected.

## Resolve catalog metadata sources and conflicts {#lineage-metadata-06}

**Situation:** Catalog ownership, freshness, and dependencies differ from their source systems.

**Context to Give the LLM:** Entries from Iceberg, dbt, Airflow, lineage, and quality tools: [sanitized values] / Collection times, update owners, and current catalog values: [record]

**Example Prompt:**

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

**Expected Output:** Give a table of field, source, conflicting values, update time, and owner to consult.

**What the LLM Can Get Wrong:** It may treat the newest value as correct or a displayed policy as enforcement.

**How to Validate:** Compare source metadata and collection records, and have owners confirm definitions.
