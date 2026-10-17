---
id: prompts-foundations
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 데이터 엔지니어링 기초 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

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

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    운영 DB의 응답이 분석 쿼리 실행 시간대에 느려지는 상황이야.
    현재 workload를 OLTP와 OLAP로 나누고 충돌 근거를 평가해 줘.
    현 구조 유지와 분석계 분리를 비교하고 row 수만으로 결론 내리지 마.
    선택지별 응답 시간·신선도·운영 비용·추가 근거 표를 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Service responses slow down while analytical queries run.
    Classify the current workload as OLTP or OLAP and assess evidence of contention.
    Compare keeping the design with separating analytics; do not decide by row count alone.
    Return a table of latency, freshness, operating cost, and evidence needed for each option.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 분석 실행 전후 같은 시간대의 지연·자원 기록. 분석 실행과 지연의 상관관계만으로 원인을 확정하거나 PostgreSQL은 분석이 불가능하다고 할 수 있다. 평균 지연만 좋아지고 서비스의 느린 요청이 악화되는 안은 채택하지 않는다.

## 필요한 열만 읽는 쿼리 검토 {#foundations-02}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    넓은 이벤트 테이블에서 소수 열만 필요한 집계의 scan bytes가 큰 상황이야.
    결과에 필요한 열과 불필요한 열을 구분하고 projection을 검토해 줘.
    Column pruning과 row 필터를 구분하고 동일 결과를 내는 쿼리 초안을 제안해 줘.
    열별 사용 이유, 변경 SQL 초안, 예상 I/O 변화와 한계를 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    An aggregate needs few columns but scans many bytes in a wide event table.
    Identify required and unused columns and review the projection.
    Separate column pruning from row filtering and draft an equivalent query.
    Return each column's purpose, a SQL draft, expected I/O change, and limits.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 소비자가 사용하는 열과 결과 계약. SELECT 열을 줄이면 모든 엔진에서 동일한 효과를 보장하거나 필터와 column pruning을 혼동할 수 있다. 열 삭제가 downstream schema 계약을 깨지 않는지 확인한다.

## Parquet 통계로 건너뛸 수 있는 범위 찾기 {#foundations-03}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    조건이 선택적인데도 많은 row group을 읽는 분석 쿼리를 검토 중이야.
    각 row group을 제외 가능·읽기 필요·정보 부족으로 분류해 줘.
    Predicate pushdown과 pruning을 나누고 임의의 row lookup처럼 설명하지 마.
    통계 근거 표와 정렬 변경을 검토할 조건을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Review a query that reads many row groups despite a selective filter.
    Classify each row group as skippable, needing a read, or lacking evidence.
    Distinguish predicate pushdown from pruning; do not describe either as arbitrary row lookup.
    Return a statistics evidence table and conditions for considering a sort-layout change.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 필터에 해당하는 row group 통계와 reader 지원 근거. Min/max 범위가 겹치면 실제 일치 row가 반드시 있다고 하거나 통계 부재를 값 부재로 볼 수 있다. NULL·통계 누락을 포함해 제외된 구간에 필요한 행이 없는지 확인한다.

## 일·시간 partition의 세분화 비교 {#foundations-04}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    날짜 partition을 시간 단위로 바꾸자는 제안을 평가한다.
    일·시간 partition에서 pruning 이득과 작은 파일 증가를 비교해 줘.
    빈 시간대와 유입이 몰리는 시간대를 따로 보고 partition과 파일을 구분해 줘.
    후보별 partition 수·파일 부담·쿼리 영향 추정과 가정을 적어 줘.
    ```

=== "English"

    ```text {.prompt}
    Evaluate a proposal to change daily partitions to hourly partitions.
    Compare pruning benefits and small-file growth for daily and hourly partitions.
    Treat empty and busy hours separately, and distinguish a partition from a file.
    Return estimated partition counts, file overhead, query effects, and assumptions for each option.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 대표 조회 기간별 실행 빈도와 파일 분포. Partition을 더 작게 나누면 항상 빨라진다고 하거나 한 partition이 한 파일이라고 가정할 수 있다. 조회 이득과 쓰기·정비 부담을 같은 기간의 부하로 비교한다.

## 고 cardinality 키의 bucket·sort 선택 {#foundations-05}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    사용자별 조회를 위해 사용자 ID로 직접 partition하자는 설계를 검토 중이야.
    직접 partition, 고정 bucket, 정렬을 현재 쿼리에 맞춰 비교해 줘.
    Hot key와 넓게 겹치는 min/max를 포함하고 OLTP index와 차이를 설명해 줘.
    후보별 파일 수·skew·pruning의 trade-off와 필요한 통계를 적어 줘.
    ```

=== "English"

    ```text {.prompt}
    Review a design that partitions directly by user ID for user-level queries.
    Compare direct partitioning, fixed buckets, and sorting for the current queries.
    Include hot keys and broad overlapping min/max ranges; explain the difference from an OLTP index.
    Return trade-offs for file count, skew, and pruning, plus the statistics needed.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 키별 분포와 실제 필터 선택도. Hash bucket이면 hot key도 자동 분산되거나 정렬이 B-tree와 같은 row 접근을 제공한다고 할 수 있다. 평균 파일 수뿐 아니라 가장 큰 키와 빈 bucket을 확인한다.

## Object Storage 읽기 비용의 원인 분리 {#foundations-06}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Compute를 분리한 뒤 원격 읽기 시간과 요청 비용이 커진 상황이야.
    저장 용량, 요청, 전송, compute 비용을 분리해서 평가해 줘.
    Pruning, cache, 파일 크기 조정의 효과와 재작성 비용을 비교해 줘.
    단가를 꾸며내지 말고 입력 단가를 쓰는 비용식과 측정 우선순위를 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Remote read time and request cost rise after compute is separated.
    Assess storage, requests, transfer, and compute cost separately.
    Compare pruning, caching, and file-size changes, including rewrite cost.
    Use supplied prices, not invented prices; return cost formulas and measurement priorities.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 동일 기간의 요청·전송·compute 사용량과 적용 단가. 저장 단가만으로 총비용을 판단하거나 cache 적중률과 파일별 task 수를 임의로 가정할 수 있다. 측정 범위·재작성 비용·cache 만료를 빠뜨린 절감률은 채택하지 않는다.
