---
id: prompts-trino
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Trino 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../data-platform/trino.md) · [전체 프롬프트 모음](index.md)

| # | 상황 바로 가기 |
| --- | --- |
| 01 | [Predicate·projection pushdown 확인](#trino-01) |
| 02 | [Broadcast join의 메모리 적합성](#trino-02) |
| 03 | [일부 task 지연과 key skew 조사](#trino-03) |
| 04 | [Spill·재시도 실행의 적용 조건 검토](#trino-04) |
| 05 | [Iceberg pruning과 저장 계층 역할 확인](#trino-05) |
| 06 | [Trino와 Spark 작업 배치 판단](#trino-06) |

## Predicate·projection pushdown 확인 {#trino-01}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Filter를 추가해도 scan bytes가 줄지 않아 pushdown 여부를 확인한다.
    Plan에서 source로 내려간 조건과 남은 연산을 구분해 주세요.
    Predicate·projection 지원을 query 형태와 connector별로 검토해 주세요.
    Scan 차이의 관측과 원인 가설, 필요한 근거를 분리해 주세요.
    연산별 plan 근거·지원 확인·반증할 비교표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Scan bytes do not fall after adding a filter. Check whether pushdown occurs.
    Separate work pushed to the source from work retained in the plan.
    Review predicate and projection support by query shape and connector.
    Separate observed scan differences, cause hypotheses, and needed evidence.
    Return plan evidence, support checks, and comparisons that can reject each hypothesis.
    ```

**핵심 사항:** 판단 전에 확인할 근거: connector 지원 근거와 실제 EXPLAIN의 남은 연산. 동일 query ID의 plan·실행 지표를 묶고 connector 정보를 제공한다. WHERE가 있으면 pushdown이 된다고 보거나 출력 행 감소를 scan 감소로 혼동할 수 있다. 출력 행 수 감소와 읽은 bytes 감소를 별개 측정으로 확인한다.

## Broadcast join의 메모리 적합성 {#trino-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    작다고 생각한 dimension의 broadcast join에서 worker 메모리 오류가 난다.
    각 worker에 복제되는 데이터와 전체 입력 크기를 구분해 주세요.
    Broadcast와 partitioned 후보의 memory·exchange 비용을 비교해 주세요.
    증거 없이 join 방식만 바꾸는 해결책으로 단정하지 말아 주세요.
    메모리 원인 가설·지지 근거·추가 확인표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    A broadcast join with a supposedly small dimension causes a worker memory error.
    Separate data copied to each worker from total input size.
    Compare memory and exchange costs for broadcast and partitioned options.
    Do not assume changing join distribution alone solves the problem.
    Return memory hypotheses, supporting evidence, and further checks.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 build side 크기와 worker별 동시 query 메모리. 동일 query ID의 plan·실행 지표를 묶고 connector 정보를 제공한다. Dimension이라는 이름만으로 작은 table이라고 보거나 partitioned join의 비용을 무시할 수 있다. 평균 메모리가 아니라 가장 큰 worker 부담으로 안전 여유를 확인한다.

## 일부 task 지연과 key skew 조사 {#trino-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    대부분 task는 끝났지만 일부 worker가 join 또는 집계를 오래 수행한다.
    Scan 불균형과 key 재분배 이후 불균형을 나눠 주세요.
    느린 task와 특정 key 집중의 연관을 원인 확정과 구분해 주세요.
    Skew 가설을 반박할 수 있는 누락 통계를 적어 주세요.
    Stage별 병목 후보·key 근거·다음 확인표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Most tasks finish, but some workers spend much longer on a join or aggregation.
    Separate uneven scans from imbalance after key redistribution.
    Separate correlation between slow tasks and hot keys from confirmed cause.
    List missing statistics that could reject the skew hypothesis.
    Return bottleneck candidates, key evidence, and next checks by stage.
    ```

**핵심 사항:** 판단 전에 확인할 근거: stage별 task 입력량과 재분배 key 분포. 동일 query ID의 plan·실행 지표를 묶고 connector 정보를 제공한다. 긴 task만 보고 skew로 확정하거나 worker 수 증가만으로 해결된다고 볼 수 있다. 느린 task만으로 skew를 확정하지 말고 I/O·부하 대안도 반박한다.

## Spill·재시도 실행의 적용 조건 검토 {#trino-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    OOM 대응안으로 spill을 켜자는 제안의 적용 범위를 검토 중이야.
    관측된 OOM 위치와 spill이 다룰 수 있다는 가정을 나눠 주세요.
    버전별 spill 상태와 fault-tolerant 실행 적용 조건을 확인 항목으로 적어 주세요.
    해결을 보장하지 말고 memory·disk·재시도 비용을 비교해 주세요.
    선택지별 사전 조건·불확실성·중단 기준 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Review a proposal to enable spill in response to out-of-memory failures.
    Separate observed OOM locations from assumptions about spill coverage.
    List version-specific spill status and fault-tolerant execution conditions to check.
    Compare memory, disk, and retry costs without promising a fix.
    Return prerequisites, uncertainties, and stop conditions for each option.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 설치 버전의 spill·retry 지원과 exchange 저장소 구성. 동일 query ID의 plan·실행 지표를 묶고 connector 정보를 제공한다. Spill이 모든 OOM을 해결하거나 exchange manager 없는 재시도도 같은 기능이라고 볼 수 있다. 실행 성공 외에 disk I/O·시간·재시도 비용을 확인한다.

## Iceberg pruning과 저장 계층 역할 확인 {#trino-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    작은 날짜 구간을 조회하는데 예상보다 많은 Iceberg file을 읽는다.
    S3·Parquet·Iceberg·Trino 역할을 읽기 경로에 맞춰 나눠 주세요.
    Partition·file·row group·column pruning 근거를 따로 평가해 주세요.
    Remote DB aggregation pushdown과 같은 동작으로 취급하지 말아 주세요.
    Pruning 단계별 기대·관측·누락 근거 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    A query for a small date interval reads more Iceberg files than expected.
    Map S3, Parquet, Iceberg, and Trino roles to the read path.
    Assess evidence for partition, file, row-group, and column pruning separately.
    Do not equate these checks with remote DB aggregation pushdown.
    Return expected behavior, observations, and missing evidence at each pruning step.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 동일 snapshot의 파일 통계와 실제 scan 기록. 동일 query ID의 plan·실행 지표를 묶고 connector 정보를 제공한다. 날짜 filter만 있으면 모든 계층에서 pruning이 되거나 Trino가 파일 저장소라고 설명할 수 있다. partition·file·row group·column의 효과를 한 수치로 합치지 않는다.

## Trino와 Spark 작업 배치 판단 {#trino-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    대화형 BI 조회와 대규모 과거 재계산이 같은 자원을 두고 경합한다.
    현재 경합 근거를 평가한 뒤 query serving과 변환 책임을 비교해 주세요.
    Trino·Spark의 일반적 역할을 절대적 기능 한계로 취급하지 말아 주세요.
    작업 배치 결정에 필요한 비용·성능 근거가 없으면 명시해 주세요.
    작업별 요구·배치 후보·trade-off·미확인 항목 표를 주세요.
    ```

=== "English"

    ```text {.prompt}
    Interactive BI queries and large historical recalculations compete for resources.
    Assess contention evidence before comparing query-serving and transformation roles.
    Do not treat common Trino and Spark roles as absolute feature limits.
    State missing cost and performance evidence needed for a placement decision.
    Return requirements, placement candidates, trade-offs, and unknowns by job.
    ```

**핵심 사항:** 판단 전에 확인할 근거: BI 지연 목표·backfill 마감과 동시 실행 근거. 동일 query ID의 plan·실행 지표를 묶고 connector 정보를 제공한다. 느린 query는 모두 Spark로 옮기거나 제품 이름만으로 성능을 보장할 수 있다. 엔진 이름만으로 더 빠르다고 쓰지 말고 두 업무의 목표 충족을 확인한다.
