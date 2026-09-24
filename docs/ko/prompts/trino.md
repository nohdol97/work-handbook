---
id: prompts-trino
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Trino 실무 프롬프트

기존 개념을 응용해 작성한 가상의 재사용 예시 6개다. 실제 업무 빈도나 실행 성능을 측정한 결과가 아니며, 새 학습 과정이나 실제 운영 경험으로 기록하지 않는다. [대괄호]를 비밀값 없는 맥락과 가상 데이터로 채운다. 모델의 제안은 검증할 작업 초안이다. 실제 production 실행 권한을 부여하지 않는다.

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

**상황:** Filter를 추가해도 scan bytes가 줄지 않아 pushdown 여부를 확인한다.

**LLM에 제공할 맥락:** 가상 SQL·EXPLAIN·필요 column: [샘플] Connector·버전·source schema: [설정] 동일 구간의 scan/output rows·bytes: [관측]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 SQL·EXPLAIN·필요 column: [샘플]
    Connector·버전·source schema: [설정]
    동일 구간의 scan/output rows·bytes: [관측]

    [요청]
    Plan에서 source로 내려간 조건과 남은 연산을 구분해 주세요.
    Predicate·projection 지원을 query 형태와 connector별로 검토해 주세요.
    Scan 차이의 관측과 원인 가설, 필요한 근거를 분리해 주세요.

    [출력]
    연산별 plan 근거·지원 확인·반증할 비교표를 주세요.
    동일 결과를 유지하는 제한된 query 비교 후보를 주세요.

    [검증]
    실제 connector 문서와 plan을 대조해 주세요.
    고정 입력에서 결과 일치와 실제 scan bytes를 따로 확인해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Synthetic SQL, EXPLAIN, and required columns: [samples]
    Connector, version, and source schema: [settings]
    Scan and output rows and bytes for one interval: [observations]

    [Task]
    Separate work pushed to the source from work retained in the plan.
    Review predicate and projection support by query shape and connector.
    Separate observed scan differences, cause hypotheses, and needed evidence.

    [Output]
    Return plan evidence, support checks, and comparisons that can reject each hypothesis.
    Propose bounded query comparisons that keep the same result.

    [Checks]
    Compare actual connector documentation and plans.
    Check result equality and actual scan bytes separately on fixed input.
    ```

**기대 결과:** 연산별 plan 근거·지원 확인·반증할 비교표를 주세요. 동일 결과를 유지하는 제한된 query 비교 후보를 주세요.

**LLM이 틀릴 수 있는 부분:** WHERE가 있으면 pushdown이 된다고 보거나 출력 행 감소를 scan 감소로 혼동할 수 있다.

**검증 방법:** 실제 connector 문서와 plan을 대조해 주세요. 고정 입력에서 결과 일치와 실제 scan bytes를 따로 확인해 주세요.

## Broadcast join의 메모리 적합성 {#trino-02}

**상황:** 작다고 생각한 dimension의 broadcast join에서 worker 메모리 오류가 난다.

**LLM에 제공할 맥락:** Join SQL·plan과 build side 크기: [가상 예시·관측] Worker별 memory·query memory·동시 작업: [관측] Key 분포·exchange bytes·출력 행 수: [기록]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Join SQL·plan과 build side 크기: [가상 예시·관측]
    Worker별 memory·query memory·동시 작업: [관측]
    Key 분포·exchange bytes·출력 행 수: [기록]

    [요청]
    각 worker에 복제되는 데이터와 전체 입력 크기를 구분해 주세요.
    Broadcast와 partitioned 후보의 memory·exchange 비용을 비교해 주세요.
    증거 없이 join 방식만 바꾸는 해결책으로 단정하지 말아 주세요.

    [출력]
    메모리 원인 가설·지지 근거·추가 확인표를 주세요.
    결과 동일성을 포함한 제한된 비교 계획을 주세요.

    [검증]
    실제 plan의 build side와 worker별 최고 memory를 확인해 주세요.
    동일 입력·동시성 조건에서 교환량과 결과를 비교하도록 해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Join SQL, plan, and build-side size: [synthetic examples and observations]
    Per-worker memory, query memory, and concurrent work: [observations]
    Key distribution, exchange bytes, and output rows: [records]

    [Task]
    Separate data copied to each worker from total input size.
    Compare memory and exchange costs for broadcast and partitioned options.
    Do not assume changing join distribution alone solves the problem.

    [Output]
    Return memory hypotheses, supporting evidence, and further checks.
    Provide a bounded comparison plan that checks result equality.

    [Checks]
    Check the actual build side and peak memory per worker.
    Compare exchange volume and results under the same input and concurrency conditions.
    ```

**기대 결과:** 메모리 원인 가설·지지 근거·추가 확인표를 주세요. 결과 동일성을 포함한 제한된 비교 계획을 주세요.

**LLM이 틀릴 수 있는 부분:** Dimension이라는 이름만으로 작은 table이라고 보거나 partitioned join의 비용을 무시할 수 있다.

**검증 방법:** 실제 plan의 build side와 worker별 최고 memory를 확인해 주세요. 동일 입력·동시성 조건에서 교환량과 결과를 비교하도록 해 주세요.

## 일부 task 지연과 key skew 조사 {#trino-03}

**상황:** 대부분 task는 끝났지만 일부 worker가 join 또는 집계를 오래 수행한다.

**LLM에 제공할 맥락:** Stage·task별 입력 행·시간·memory: [익명화한 통계] Join·GROUP BY key 분포와 null 비율: [가상 분포] Plan·exchange·source scan 분포: [관측]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Stage·task별 입력 행·시간·memory: [익명화한 통계]
    Join·GROUP BY key 분포와 null 비율: [가상 분포]
    Plan·exchange·source scan 분포: [관측]

    [요청]
    Scan 불균형과 key 재분배 이후 불균형을 나눠 주세요.
    느린 task와 특정 key 집중의 연관을 원인 확정과 구분해 주세요.
    Skew 가설을 반박할 수 있는 누락 통계를 적어 주세요.

    [출력]
    Stage별 병목 후보·key 근거·다음 확인표를 주세요.
    결과 의미를 보존하는 작은 분포 비교 실험을 제안해 주세요.

    [검증]
    실제 key 분포와 task 입력·exchange 분포를 대조해 주세요.
    가상 균등·편향 key에서 행 수와 합계가 유지되는지 확인해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Input rows, time, and memory by stage and task: [sanitized statistics]
    Join or GROUP BY key distribution and null share: [synthetic distribution]
    Plan, exchanges, and source-scan distribution: [observations]

    [Task]
    Separate uneven scans from imbalance after key redistribution.
    Separate correlation between slow tasks and hot keys from confirmed cause.
    List missing statistics that could reject the skew hypothesis.

    [Output]
    Return bottleneck candidates, key evidence, and next checks by stage.
    Propose a small distribution comparison that preserves result meaning.

    [Checks]
    Compare actual key distribution with task input and exchange distributions.
    Check row counts and totals with synthetic balanced and skewed keys.
    ```

**기대 결과:** Stage별 병목 후보·key 근거·다음 확인표를 주세요. 결과 의미를 보존하는 작은 분포 비교 실험을 제안해 주세요.

**LLM이 틀릴 수 있는 부분:** 긴 task만 보고 skew로 확정하거나 worker 수 증가만으로 해결된다고 볼 수 있다.

**검증 방법:** 실제 key 분포와 task 입력·exchange 분포를 대조해 주세요. 가상 균등·편향 key에서 행 수와 합계가 유지되는지 확인해 주세요.

## Spill·재시도 실행의 적용 조건 검토 {#trino-04}

**상황:** OOM 대응안으로 spill을 켜자는 제안의 적용 범위를 검토한다.

**LLM에 제공할 맥락:** Trino 버전·connector·query plan: [설정·가상 plan] 오류 종류·worker/query memory·disk I/O: [관측] Retry policy·exchange manager·현재 spill 설정: [설정]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Trino 버전·connector·query plan: [설정·가상 plan]
    오류 종류·worker/query memory·disk I/O: [관측]
    Retry policy·exchange manager·현재 spill 설정: [설정]

    [요청]
    관측된 OOM 위치와 spill이 다룰 수 있다는 가정을 나눠 주세요.
    버전별 spill 상태와 fault-tolerant 실행 적용 조건을 확인 항목으로 적어 주세요.
    해결을 보장하지 말고 memory·disk·재시도 비용을 비교해 주세요.

    [출력]
    선택지별 사전 조건·불확실성·중단 기준 표를 주세요.
    설정 변경 전 필요한 공식 문서·상태 근거를 주세요.

    [검증]
    실제 버전의 공식 문서와 connector 지원·설정을 대조해 주세요.
    제한된 검증에서 성공 여부뿐 아니라 memory·disk·시간도 비교해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Trino version, connector, and query plan: [settings and synthetic plan]
    Error type, worker and query memory, and disk I/O: [observations]
    Retry policy, exchange manager, and current spill settings: [settings]

    [Task]
    Separate observed OOM locations from assumptions about spill coverage.
    List version-specific spill status and fault-tolerant execution conditions to check.
    Compare memory, disk, and retry costs without promising a fix.

    [Output]
    Return prerequisites, uncertainties, and stop conditions for each option.
    List official documentation and state evidence needed before changing settings.

    [Checks]
    Cross-check official version documentation, connector support, and settings.
    In bounded checks, compare memory, disk, and time as well as success.
    ```

**기대 결과:** 선택지별 사전 조건·불확실성·중단 기준 표를 주세요. 설정 변경 전 필요한 공식 문서·상태 근거를 주세요.

**LLM이 틀릴 수 있는 부분:** Spill이 모든 OOM을 해결하거나 exchange manager 없는 재시도도 같은 기능이라고 볼 수 있다.

**검증 방법:** 실제 버전의 공식 문서와 connector 지원·설정을 대조해 주세요. 제한된 검증에서 성공 여부뿐 아니라 memory·disk·시간도 비교해 주세요.

## Iceberg pruning과 저장 계층 역할 확인 {#trino-05}

**상황:** 작은 날짜 구간을 조회하는데 예상보다 많은 Iceberg file을 읽는다.

**LLM에 제공할 맥락:** Filter·선택 column·EXPLAIN: [가상 SQL·plan] Partition·file·metadata 배치와 snapshot: [가상 구성] 읽은 file·rows·bytes와 connector 버전: [관측·버전]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Filter·선택 column·EXPLAIN: [가상 SQL·plan]
    Partition·file·metadata 배치와 snapshot: [가상 구성]
    읽은 file·rows·bytes와 connector 버전: [관측·버전]

    [요청]
    S3·Parquet·Iceberg·Trino 역할을 읽기 경로에 맞춰 나눠 주세요.
    Partition·file·row group·column pruning 근거를 따로 평가해 주세요.
    Remote DB aggregation pushdown과 같은 동작으로 취급하지 말아 주세요.

    [출력]
    Pruning 단계별 기대·관측·누락 근거 표를 주세요.
    동일 snapshot에서 filter와 projection을 비교할 계획을 주세요.

    [검증]
    실제 Iceberg metadata·layout과 connector plan을 대조해 주세요.
    고정 snapshot에서 결과·읽은 file·bytes를 함께 확인해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Filters, selected columns, and EXPLAIN: [synthetic SQL and plan]
    Partition, file, and metadata layout and snapshot: [synthetic layout]
    Files, rows, and bytes read and connector version: [observations and version]

    [Task]
    Map S3, Parquet, Iceberg, and Trino roles to the read path.
    Assess evidence for partition, file, row-group, and column pruning separately.
    Do not equate these checks with remote DB aggregation pushdown.

    [Output]
    Return expected behavior, observations, and missing evidence at each pruning step.
    Provide a filter and projection comparison plan on the same snapshot.

    [Checks]
    Compare actual Iceberg metadata and layout with the connector plan.
    Check results, files read, and bytes on a fixed snapshot.
    ```

**기대 결과:** Pruning 단계별 기대·관측·누락 근거 표를 주세요. 동일 snapshot에서 filter와 projection을 비교할 계획을 주세요.

**LLM이 틀릴 수 있는 부분:** 날짜 filter만 있으면 모든 계층에서 pruning이 되거나 Trino가 파일 저장소라고 설명할 수 있다.

**검증 방법:** 실제 Iceberg metadata·layout과 connector plan을 대조해 주세요. 고정 snapshot에서 결과·읽은 file·bytes를 함께 확인해 주세요.

## Trino와 Spark 작업 배치 판단 {#trino-06}

**상황:** 대화형 BI 조회와 대규모 과거 재계산이 같은 자원을 두고 경합한다.

**LLM에 제공할 맥락:** 작업별 SQL·입력 규모·동시성: [가상 workload] BI 응답 요구와 backfill 완료 요구: [목표] 현재 engine·저장 계층·실행 관측: [구조·통계]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    작업별 SQL·입력 규모·동시성: [가상 workload]
    BI 응답 요구와 backfill 완료 요구: [목표]
    현재 engine·저장 계층·실행 관측: [구조·통계]

    [요청]
    현재 경합 근거를 평가한 뒤 query serving과 변환 책임을 비교해 주세요.
    Trino·Spark의 일반적 역할을 절대적 기능 한계로 취급하지 말아 주세요.
    작업 배치 결정에 필요한 비용·성능 근거가 없으면 명시해 주세요.

    [출력]
    작업별 요구·배치 후보·trade-off·미확인 항목 표를 주세요.
    동일 결과와 동시성 조건을 갖춘 제한된 비교 계획을 주세요.

    [검증]
    실제 plan·runtime·요구 지연을 비교 기준과 대조해 주세요.
    고정 입력의 결과 일치와 BI·backfill 영향이 함께 측정되도록 해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    SQL, input size, and concurrency by job: [synthetic workload]
    BI response needs and backfill completion needs: [targets]
    Current engines, storage layers, and observations: [structure and statistics]

    [Task]
    Assess contention evidence before comparing query-serving and transformation roles.
    Do not treat common Trino and Spark roles as absolute feature limits.
    State missing cost and performance evidence needed for a placement decision.

    [Output]
    Return requirements, placement candidates, trade-offs, and unknowns by job.
    Provide a bounded comparison plan with equal results and concurrency conditions.

    [Checks]
    Compare actual plans, runtime, and required latency with the evaluation criteria.
    Check equal results on fixed input and measure effects on both BI and backfills.
    ```

**기대 결과:** 작업별 요구·배치 후보·trade-off·미확인 항목 표를 주세요. 동일 결과와 동시성 조건을 갖춘 제한된 비교 계획을 주세요.

**LLM이 틀릴 수 있는 부분:** 느린 query는 모두 Spark로 옮기거나 제품 이름만으로 성능을 보장할 수 있다.

**검증 방법:** 실제 plan·runtime·요구 지연을 비교 기준과 대조해 주세요. 고정 입력의 결과 일치와 BI·backfill 영향이 함께 측정되도록 해 주세요.
