---
id: prompts-foundations
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# 데이터 엔지니어링 기초 실무 프롬프트

문서 유형: Reference. [기존 학습 내용](../data-platform/foundations.md)을 적용하도록 작성한 가상의 재사용 예시 6개다. 실제 업무 경험, 사용 빈도 조사, 모델 실행 결과를 뜻하지 않는다. 예시를 실행하지 않았다.

상황에 맞는 예시를 고르고 대괄호 입력을 익명화한 자료로 바꾼다. 각 예시는 한국어·English 탭에서 언어를 선택해 복사할 수 있다. LLM의 답은 가설이며 실제 설정·로그·공식 문서·제한된 검증으로 확인한다. 운영 실행이나 권한 변경을 허가하는 문서는 아니다.

[전체 프롬프트 모음](index.md) · [개념과 출처](../data-platform/foundations.md)

## 빠르게 고르기

| 목적 | 바로 가기 |
| --- | --- |
| 운영 DB에서 분석 부하를 분리할지 판단 | [01](#foundations-01) |
| 필요한 열만 읽는 쿼리 검토 | [02](#foundations-02) |
| Parquet 통계로 건너뛸 수 있는 범위 찾기 | [03](#foundations-03) |
| 일·시간 partition의 세분화 비교 | [04](#foundations-04) |
| 고 cardinality 키의 bucket·sort 선택 | [05](#foundations-05) |
| Object Storage 읽기 비용의 원인 분리 | [06](#foundations-06) |

## 운영 DB에서 분석 부하를 분리할지 판단 {#foundations-01}

- **상황:** 운영 DB의 응답이 분석 쿼리 실행 시간대에 느려지는 가상 사례다.
- **제공할 맥락:** 쿼리와 실행 빈도: [익명화한 SQL·주기]; 영향과 제약: [트랜잭션 지연·자원·비용·신선도 목표].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    쿼리와 실행 빈도: [익명화한 SQL·주기]
    영향과 제약: [트랜잭션 지연·자원·비용·신선도 목표]

    [요청]
    현재 workload를 OLTP와 OLAP로 나누고 충돌 근거를 평가해 줘.
    현 구조 유지와 분석계 분리를 비교하고 row 수만으로 결론 내리지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    선택지별 응답 시간·신선도·운영 비용·추가 근거 표를 작성해 줘.

    [검증]
    동일 workload에서 분석 실행 유무별 지연과 자원 지표를 비교하는 제한된 실험을 제안해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Queries and frequency: [sanitized SQL and schedule]
    Impact and limits: [transaction latency, resources, cost, freshness target]

    [Task]
    Classify the current workload as OLTP or OLAP and assess evidence of contention.
    Compare keeping the design with separating analytics; do not decide by row count alone.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a table of latency, freshness, operating cost, and evidence needed for each option.

    [Checks]
    Propose a bounded comparison of latency and resources with and without the analytical work.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 선택지별 응답 시간·신선도·운영 비용·추가 근거 표.
- **오류 가능성:** 분석 실행과 지연의 상관관계만으로 원인을 확정하거나 PostgreSQL은 분석이 불가능하다고 할 수 있다.
- **검증 방법:** 동일 workload에서 분석 실행 유무별 지연과 자원 지표를 비교하는 제한된 실험을 계획한다.

## 필요한 열만 읽는 쿼리 검토 {#foundations-02}

- **상황:** 넓은 이벤트 테이블에서 소수 열만 필요한 집계의 scan bytes가 큰 가상 사례다.
- **제공할 맥락:** 쿼리와 스키마: [SQL·열 목록·필요한 결과]; 실행 근거: [reader 버전·계획·scan bytes·파일 형식].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    쿼리와 스키마: [SQL·열 목록·필요한 결과]
    실행 근거: [reader 버전·계획·scan bytes·파일 형식]

    [요청]
    결과에 필요한 열과 불필요한 열을 구분하고 projection을 검토해 줘.
    Column pruning과 row 필터를 구분하고 동일 결과를 내는 쿼리 초안을 제안해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    열별 사용 이유, 변경 SQL 초안, 예상 I/O 변화와 한계를 작성해 줘.

    [검증]
    같은 입력에서 결과 일치와 실제 읽은 열·scan bytes를 확인하는 방법을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Query and schema: [SQL, column list, required result]
    Execution evidence: [reader version, plan, scan bytes, file format]

    [Task]
    Identify required and unused columns and review the projection.
    Separate column pruning from row filtering and draft an equivalent query.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return each column's purpose, a SQL draft, expected I/O change, and limits.

    [Checks]
    Describe how to compare results, columns actually read, and scan bytes on the same input.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 열별 사용 이유, 변경 SQL 초안, 예상 I/O 변화와 한계.
- **오류 가능성:** SELECT 열을 줄이면 모든 엔진에서 동일한 효과를 보장하거나 필터와 column pruning을 혼동할 수 있다.
- **검증 방법:** 같은 입력에서 결과 일치와 실제 읽은 열·scan bytes를 확인하는 방법을 작성한다.

## Parquet 통계로 건너뛸 수 있는 범위 찾기 {#foundations-03}

- **상황:** 조건이 선택적인데도 많은 row group을 읽는 가상 분석 쿼리를 검토한다.
- **제공할 맥락:** 조건과 통계: [필터·row group별 min/max·null 정보]; 저장·읽기 설정: [정렬 상태·page index 유무·reader 지원].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    조건과 통계: [필터·row group별 min/max·null 정보]
    저장·읽기 설정: [정렬 상태·page index 유무·reader 지원]

    [요청]
    각 row group을 제외 가능·읽기 필요·정보 부족으로 분류해 줘.
    Predicate pushdown과 pruning을 나누고 임의의 row lookup처럼 설명하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    통계 근거 표와 정렬 변경을 검토할 조건을 작성해 줘.

    [검증]
    실행 계획과 읽은 row group 수로 예측을 확인하고 통계가 없는 경우도 포함해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Filters and statistics: [predicate, row-group min/max, null information]
    Storage and reader details: [sort layout, page indexes, reader support]

    [Task]
    Classify each row group as skippable, needing a read, or lacking evidence.
    Distinguish predicate pushdown from pruning; do not describe either as arbitrary row lookup.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a statistics evidence table and conditions for considering a sort-layout change.

    [Checks]
    Check the prediction with the plan and row groups read; include a case with missing statistics.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 통계 근거 표와 정렬 변경을 검토할 조건.
- **오류 가능성:** Min/max 범위가 겹치면 실제 일치 row가 반드시 있다고 하거나 통계 부재를 값 부재로 볼 수 있다.
- **검증 방법:** 실행 계획과 읽은 row group 수로 예측을 확인하고 통계가 없는 경우도 포함한다.

## 일·시간 partition의 세분화 비교 {#foundations-04}

- **상황:** 날짜 partition을 시간 단위로 바꾸자는 가상 제안을 평가한다.
- **제공할 맥락:** 접근 패턴: [기간별 쿼리·필터 빈도·신선도 요구]; 분포: [시간별 유입량·partition별 파일 수·크기].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    접근 패턴: [기간별 쿼리·필터 빈도·신선도 요구]
    분포: [시간별 유입량·partition별 파일 수·크기]

    [요청]
    일·시간 partition에서 pruning 이득과 작은 파일 증가를 비교해 줘.
    빈 시간대와 유입이 몰리는 시간대를 따로 보고 partition과 파일을 구분해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    후보별 partition 수·파일 부담·쿼리 영향 추정과 가정을 적어 줘.

    [검증]
    대표 시간 범위별 scan bytes·planning time·파일 분포를 비교하는 계획을 작성해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Access patterns: [query time ranges, filter frequency, freshness needs]
    Distribution: [hourly volume, files per partition, file sizes]

    [Task]
    Compare pruning benefits and small-file growth for daily and hourly partitions.
    Treat empty and busy hours separately, and distinguish a partition from a file.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return estimated partition counts, file overhead, query effects, and assumptions for each option.

    [Checks]
    Plan a comparison of scan bytes, planning time, and file distribution for representative time ranges.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 후보별 partition 수·파일 부담·쿼리 영향 추정과 가정.
- **오류 가능성:** Partition을 더 작게 나누면 항상 빨라진다고 하거나 한 partition이 한 파일이라고 가정할 수 있다.
- **검증 방법:** 대표 시간 범위별 scan bytes·planning time·파일 분포를 비교하는 계획을 작성한다.

## 고 cardinality 키의 bucket·sort 선택 {#foundations-05}

- **상황:** 사용자별 조회를 위해 사용자 ID로 직접 partition하자는 가상 설계를 검토한다.
- **제공할 맥락:** 키와 조회: [익명화한 cardinality·키 분포·필터 예시]; 배치 정보: [현 partition·파일별 min/max·엔진 버전].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    키와 조회: [익명화한 cardinality·키 분포·필터 예시]
    배치 정보: [현 partition·파일별 min/max·엔진 버전]

    [요청]
    직접 partition, 고정 bucket, 정렬을 현재 쿼리에 맞춰 비교해 줘.
    Hot key와 넓게 겹치는 min/max를 포함하고 OLTP index와 차이를 설명해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    후보별 파일 수·skew·pruning의 trade-off와 필요한 통계를 적어 줘.

    [검증]
    엔진의 transform 문법을 확인하고 동일 필터의 파일 선택 수와 scan bytes를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Keys and queries: [sanitized cardinality, key distribution, filter examples]
    Layout details: [current partitions, file min/max, engine version]

    [Task]
    Compare direct partitioning, fixed buckets, and sorting for the current queries.
    Include hot keys and broad overlapping min/max ranges; explain the difference from an OLTP index.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return trade-offs for file count, skew, and pruning, plus the statistics needed.

    [Checks]
    Check the engine's transform syntax and compare selected files and scan bytes for the same filters.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 후보별 파일 수·skew·pruning의 trade-off와 필요한 통계.
- **오류 가능성:** Hash bucket이면 hot key도 자동 분산되거나 정렬이 B-tree와 같은 row 접근을 제공한다고 할 수 있다.
- **검증 방법:** 엔진의 transform 문법을 확인하고 동일 필터의 파일 선택 수와 scan bytes를 비교한다.

## Object Storage 읽기 비용의 원인 분리 {#foundations-06}

- **상황:** Compute를 분리한 뒤 원격 읽기 시간과 요청 비용이 커진 가상 사례다.
- **제공할 맥락:** 사용량: [파일 수·크기·요청 수·전송량·scan bytes]; 제약: [요금 항목·반복 조회 패턴·cache 수명·응답 목표].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    사용량: [파일 수·크기·요청 수·전송량·scan bytes]
    제약: [요금 항목·반복 조회 패턴·cache 수명·응답 목표]

    [요청]
    저장 용량, 요청, 전송, compute 비용을 분리해서 평가해 줘.
    Pruning, cache, 파일 크기 조정의 효과와 재작성 비용을 비교해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    단가를 꾸며내지 말고 입력 단가를 쓰는 비용식과 측정 우선순위를 작성해 줘.

    [검증]
    동일 쿼리의 cold·warm 실행에서 요청 수·전송량·시간을 비교하는 검증을 제안해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Usage: [file count, sizes, request count, transfer volume, scan bytes]
    Limits: [price components, repeated queries, cache lifetime, latency target]

    [Task]
    Assess storage, requests, transfer, and compute cost separately.
    Compare pruning, caching, and file-size changes, including rewrite cost.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Use supplied prices, not invented prices; return cost formulas and measurement priorities.

    [Checks]
    Propose cold and warm runs of the same query to compare requests, transfer, and elapsed time.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 입력 단가를 쓰는 비용식과 측정 우선순위.
- **오류 가능성:** 저장 단가만으로 총비용을 판단하거나 cache 적중률과 파일별 task 수를 임의로 가정할 수 있다.
- **검증 방법:** 동일 쿼리의 cold·warm 실행에서 요청 수·전송량·시간을 비교하는 검증을 계획한다.
