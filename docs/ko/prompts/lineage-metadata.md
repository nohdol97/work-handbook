---
id: prompts-lineage-metadata
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Lineage와 metadata 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

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

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    새 테이블의 catalog 항목이 schema만 있어 사용자가 의미와 상태를 알기 어렵다.
    Technical·Operational·Business metadata로 항목을 분류하세요.
    추측으로 채우지 말고 빈칸별 확인할 정보 출처를 지정하세요.
    항목 / 분류 / 현재 근거 / 누락 / 확인 대상 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    A new catalog entry lists only a schema, so users cannot understand its meaning or health.
    Group fields into technical, operational, and business metadata.
    Do not invent missing values; name the source to check for each gap.
    Give a table of field, category, current evidence, gap, and source to check.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 항목별 정보 원본과 owner 확인 가능 여부. 관측된 연결과 아직 수집하지 못한 경로를 명시적으로 구분한다. column 이름에서 KPI 의미나 소유자를 지어낼 수 있다. column 이름만으로 의미·담당자를 자동 채워 넣지 않는다.

## KPI 설명과 계산 정의 맞추기 {#lineage-metadata-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Revenue 설명은 같지만 두 대시보드의 합계가 다르다.
    Business metadata의 설명과 실행 가능한 metric 정의를 분리하세요.
    중복 차감·범위·grain 차이를 점검하고 아직 합의되지 않은 의미를 찾으세요.
    정의 항목 / 계산 A / 계산 B / 차이 근거 / 담당자 질문 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Two dashboards describe Revenue the same way but show different totals.
    Separate business descriptions from executable metric definitions.
    Check double subtraction, scope, and grain differences, and find unsettled meanings.
    Give a table of definition, calculation A, calculation B, evidence of differences, and owner questions.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 승인된 매출 정의와 VAT·refund 처리 기준. 관측된 연결과 아직 수집하지 못한 경로를 명시적으로 구분한다. 설명 한 문장만으로 회계 규칙이나 올바른 식을 확정할 수 있다. 같은 입력에서 두 계산의 차액이 어떤 규칙에서 생기는지 설명되어야 한다.

## 실행 기록과 lineage 수집 누락 대조 {#lineage-metadata-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    실행은 있었는데 lineage 화면에 일부 경로가 보이지 않는다.
    Job·Run·Dataset 식별자를 구분해 실제 실행과 이벤트를 대조하세요.
    run에 연결되지 않는 metadata event도 고려해 누락 후보를 찾으세요.
    실행 또는 metadata / 기대 정보 / 수집 증거 / 미확인 구간 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Jobs ran, but some paths are absent from the lineage view.
    Separate Job, Run, and Dataset identifiers and compare runs with events.
    Account for metadata events without runs when finding possible gaps.
    Give a table of run or metadata, expected information, collection evidence, and unknown scope.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 같은 식별자로 연결한 실행 이력과 lineage 수집 이벤트. 관측된 연결과 아직 수집하지 못한 경로를 명시적으로 구분한다. 모든 event를 run으로 세거나 화면에 없으면 실행도 없었다고 볼 수 있다. 화면에 없다는 이유만으로 실제 실행이나 의존성이 없었다고 쓰지 않는다.

## KPI 오류를 upstream으로 추적 {#lineage-metadata-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    매출 KPI가 틀렸지만 어느 변환부터 값이 달라졌는지 모른다.
    대시보드에서 원본 방향으로 확인 경로를 정리하세요.
    연결이 있다는 사실과 특정 run이 정확했다는 증거를 구분하세요.
    상류 단계 / 비교할 값 / 의심 변환 / 반박할 증거 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    A sales KPI is wrong, but the first transformation with a wrong value is unknown.
    Order checks from the dashboard back toward the source.
    Separate an existing graph edge from evidence that a run was correct.
    Give a table of upstream stage, values to compare, suspect transformation, and evidence against it.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 동일 grain·기간의 단계별 중간 결과. 관측된 연결과 아직 수집하지 못한 경로를 명시적으로 구분한다. 처음 보이는 upstream을 원인으로 단정하거나 table 연결만으로 column 계산을 추정할 수 있다. 연결된 upstream이라는 사실만으로 원인을 확정하지 않는다.

## 민감 column의 파생 경로 조사 {#lineage-metadata-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    민감 column이 어떤 파생 테이블과 KPI로 전달되는지 확인한다.
    직접 전달·변환·집계 경로를 구분하고 알 수 없는 구간을 남기세요.
    그래프 정보와 접근 정책의 실제 적용 증거를 혼동하지 마세요.
    파생 대상 / 입력 column / 변환 / 분류 확인 / 누락 근거 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Check which derived tables and KPIs use a sensitive column.
    Separate direct, transformed, and aggregated paths and mark unknown segments.
    Do not confuse graph information with proof that access policies are enforced.
    Give a table of target, input column, transformation, classification check, and missing evidence.
    ```

**핵심 사항:** 판단 전에 확인할 근거: column 변환식과 실제 consumer·미수집 경로. 관측된 연결과 아직 수집하지 못한 경로를 명시적으로 구분한다. 집계됐다는 이유로 민감성이 사라졌다고 단정하거나 lineage 누락을 무영향으로 볼 수 있다. 집계·hash 처리만 보고 비민감으로 바꾸지 않고 정책 근거를 확인한다.

## catalog 정보의 출처와 충돌 정리 {#lineage-metadata-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    catalog의 owner·freshness·의존성 정보가 각 원본 시스템과 다르다.
    구조·문서·실행·계보·품질 정보의 원본을 구분하세요.
    수집 지연과 의미 차이 가설을 나누고 임의로 값을 덮어쓰지 마세요.
    항목 / 원본 / 충돌 값 / 갱신 시각 / 조정할 담당자 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Catalog ownership, freshness, and dependencies differ from their source systems.
    Separate sources for structure, docs, runs, lineage, and quality.
    Separate collection-delay and meaning-difference hypotheses; do not overwrite values.
    Give a table of field, source, conflicting values, update time, and owner to consult.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 항목별 갱신 책임과 수집 시각. 관측된 연결과 아직 수집하지 못한 경로를 명시적으로 구분한다. 가장 최근 값을 무조건 정답으로 보거나 catalog 표시를 정책 강제로 오해할 수 있다. 최근 값이라는 이유만으로 원본의 업무 정의를 덮어쓰지 않는다.
