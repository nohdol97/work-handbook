---
id: prompts-lineage-metadata
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Lineage and metadata practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

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

**Prompt:**

=== "English"

    ```text {.prompt}
    A new catalog entry lists only a schema, so users cannot understand its meaning or health.
    Group fields into technical, operational, and business metadata.
    Do not invent missing values; name the source to check for each gap.
    Give a table of field, category, current evidence, gap, and source to check.
    ```

=== "한국어"

    ```text {.prompt}
    새 테이블의 catalog 항목이 schema만 있어 사용자가 의미와 상태를 알기 어렵다.
    Technical·Operational·Business metadata로 항목을 분류하세요.
    추측으로 채우지 말고 빈칸별 확인할 정보 출처를 지정하세요.
    항목 / 분류 / 현재 근거 / 누락 / 확인 대상 표를 주세요.
    ```

**Key point:** Evidence to check first: the source for each field and whether its owner can confirm it. Separate observed links from paths that have not been collected. It may invent KPI meaning or ownership from column names. Do not fill in meaning or ownership from column names alone.

## Align KPI descriptions and calculations {#lineage-metadata-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    Two dashboards describe Revenue the same way but show different totals.
    Separate business descriptions from executable metric definitions.
    Check double subtraction, scope, and grain differences, and find unsettled meanings.
    Give a table of definition, calculation A, calculation B, evidence of differences, and owner questions.
    ```

=== "한국어"

    ```text {.prompt}
    Revenue 설명은 같지만 두 대시보드의 합계가 다르다.
    Business metadata의 설명과 실행 가능한 metric 정의를 분리하세요.
    중복 차감·범위·grain 차이를 점검하고 아직 합의되지 않은 의미를 찾으세요.
    정의 항목 / 계산 A / 계산 B / 차이 근거 / 담당자 질문 표를 주세요.
    ```

**Key point:** Evidence to check first: the agreed revenue definition and VAT/refund rules. Separate observed links from paths that have not been collected. It may infer accounting rules or a correct formula from one description. Require an explanation of which rule creates the difference on identical input.

## Compare job runs with lineage collection {#lineage-metadata-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Jobs ran, but some paths are absent from the lineage view.
    Separate Job, Run, and Dataset identifiers and compare runs with events.
    Account for metadata events without runs when finding possible gaps.
    Give a table of run or metadata, expected information, collection evidence, and unknown scope.
    ```

=== "한국어"

    ```text {.prompt}
    실행은 있었는데 lineage 화면에 일부 경로가 보이지 않는다.
    Job·Run·Dataset 식별자를 구분해 실제 실행과 이벤트를 대조하세요.
    run에 연결되지 않는 metadata event도 고려해 누락 후보를 찾으세요.
    실행 또는 metadata / 기대 정보 / 수집 증거 / 미확인 구간 표를 주세요.
    ```

**Key point:** Evidence to check first: run records and collected lineage events linked by matching identifiers. Separate observed links from paths that have not been collected. It may count every event as a run or assume an absent path never ran. Do not infer absent runs or dependencies solely from an empty view.

## Trace a KPI error upstream {#lineage-metadata-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    A sales KPI is wrong, but the first transformation with a wrong value is unknown.
    Order checks from the dashboard back toward the source.
    Separate an existing graph edge from evidence that a run was correct.
    Give a table of upstream stage, values to compare, suspect transformation, and evidence against it.
    ```

=== "한국어"

    ```text {.prompt}
    매출 KPI가 틀렸지만 어느 변환부터 값이 달라졌는지 모른다.
    대시보드에서 원본 방향으로 확인 경로를 정리하세요.
    연결이 있다는 사실과 특정 run이 정확했다는 증거를 구분하세요.
    상류 단계 / 비교할 값 / 의심 변환 / 반박할 증거 표를 주세요.
    ```

**Key point:** Evidence to check first: intermediate results at the same grain and time range. Separate observed links from paths that have not been collected. It may blame the first upstream node or infer column logic from a table edge. Do not establish causation merely because an upstream edge exists.

## Trace derived paths from a sensitive column {#lineage-metadata-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    Check which derived tables and KPIs use a sensitive column.
    Separate direct, transformed, and aggregated paths and mark unknown segments.
    Do not confuse graph information with proof that access policies are enforced.
    Give a table of target, input column, transformation, classification check, and missing evidence.
    ```

=== "한국어"

    ```text {.prompt}
    민감 column이 어떤 파생 테이블과 KPI로 전달되는지 확인한다.
    직접 전달·변환·집계 경로를 구분하고 알 수 없는 구간을 남기세요.
    그래프 정보와 접근 정책의 실제 적용 증거를 혼동하지 마세요.
    파생 대상 / 입력 column / 변환 / 분류 확인 / 누락 근거 표를 주세요.
    ```

**Key point:** Evidence to check first: column transformations, actual consumers, and uncollected paths. Separate observed links from paths that have not been collected. It may assume aggregation removes sensitivity or missing lineage means no impact. Check policy evidence before treating aggregation or hashing as removal of sensitivity.

## Resolve catalog metadata sources and conflicts {#lineage-metadata-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    Catalog ownership, freshness, and dependencies differ from their source systems.
    Separate sources for structure, docs, runs, lineage, and quality.
    Separate collection-delay and meaning-difference hypotheses; do not overwrite values.
    Give a table of field, source, conflicting values, update time, and owner to consult.
    ```

=== "한국어"

    ```text {.prompt}
    catalog의 owner·freshness·의존성 정보가 각 원본 시스템과 다르다.
    구조·문서·실행·계보·품질 정보의 원본을 구분하세요.
    수집 지연과 의미 차이 가설을 나누고 임의로 값을 덮어쓰지 마세요.
    항목 / 원본 / 충돌 값 / 갱신 시각 / 조정할 담당자 표를 주세요.
    ```

**Key point:** Evidence to check first: update ownership and collection times for each field. Separate observed links from paths that have not been collected. It may treat the newest value as correct or a displayed policy as enforcement. Do not overwrite source business definitions merely because another value is newer.
