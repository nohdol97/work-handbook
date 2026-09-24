---
id: prompts-spark
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Apache Spark 실무 프롬프트

문서 유형: Reference. [기존 학습 내용](../data-platform/spark.md)을 적용하도록 작성한 가상의 재사용 예시 6개다. 실제 업무 경험, 사용 빈도 조사, 모델 실행 결과를 뜻하지 않는다. 예시를 실행하지 않았다.

상황에 맞는 예시를 고르고 대괄호 입력을 익명화한 자료로 바꾼다. 각 예시는 한국어·English 탭에서 언어를 선택해 복사할 수 있다. LLM의 답은 가설이며 실제 설정·로그·공식 문서·제한된 검증으로 확인한다. 운영 실행이나 권한 변경을 허가하는 문서는 아니다.

[전체 프롬프트 모음](index.md) · [개념과 출처](../data-platform/spark.md)

## 빠르게 고르기

| 목적 | 바로 가기 |
| --- | --- |
| Join 결과 row 폭증 원인 찾기 | [01](#spark-01) |
| Broadcast join의 메모리 적합성 검토 | [02](#spark-02) |
| 출력 파일 수와 task 병렬성 조정 | [03](#spark-03) |
| Cache와 durable 중간 테이블 선택 | [04](#spark-04) |
| foreachBatch 재시도의 중복 효과 검토 | [05](#spark-05) |
| Streaming output mode와 late event 정책 검토 | [06](#spark-06) |

## Join 결과 row 폭증 원인 찾기 {#spark-01}

- **상황:** Join 후 row 수가 크게 늘어난 가상 ETL을 검토한다.
- **제공할 맥락:** 입력 정의: [양쪽 grain·join key·키별 건수·null 처리]; 의도와 실행: [필요한 결과·join 조건·전후 row 수·계획].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    입력 정의: [양쪽 grain·join key·키별 건수·null 처리]
    의도와 실행: [필요한 결과·join 조건·전후 row 수·계획]

    [요청]
    키 중복으로 생기는 다대다 곱과 의도한 관계를 먼저 비교해 줘.
    존재 여부만 필요하다면 semi/anti join의 의미를 검토하고 임의 dedup은 피해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    키별 예상 row 수 계산과 의미를 보존하는 수정 초안을 작성해 줘.

    [검증]
    합성 다대다·미일치·null 표본으로 기대 row와 결과를 대조해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Input definitions: [grain on each side, join keys, counts per key, null handling]
    Intent and execution: [required result, join condition, row counts, plan]

    [Task]
    First compare duplicate-key multiplication with the intended relationship.
    If only existence matters, review semi or anti join semantics; avoid arbitrary deduplication.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return expected counts by key and a draft change that preserves meaning.

    [Checks]
    Compare expected and actual rows for synthetic many-to-many, unmatched, and null-key cases.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 키별 예상 row 수 계산과 의미를 보존하는 수정 초안.
- **오류 가능성:** Broadcast나 repartition만으로 잘못된 grain을 해결하거나 중복 row를 무조건 삭제할 수 있다.
- **검증 방법:** 합성 다대다·미일치·null 표본으로 기대 row와 결과를 대조한다.

## Broadcast join의 메모리 적합성 검토 {#spark-02}

- **상황:** 작은 dimension을 broadcast하자는 가상 성능 제안을 검토한다.
- **제공할 맥락:** 계획과 크기: [현재 physical plan·필터 후 크기·실측 메모리]; 자원과 비용: [executor 자원·동시 task·GC·spill·shuffle bytes].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    계획과 크기: [현재 physical plan·필터 후 크기·실측 메모리]
    자원과 비용: [executor 자원·동시 task·GC·spill·shuffle bytes]

    [요청]
    작다는 이름 대신 실제 크기와 executor별 부담으로 적합성을 평가해 줘.
    Broadcast와 현 join 전략을 비교하고 메모리 압박과 shuffle 감소를 함께 다뤄 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    찬성·반대 근거, 빠진 측정, 제한된 비교 실험을 작성해 줘.

    [검증]
    동일 입력의 실제 계획·peak memory·GC·shuffle·결과 일치를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Plan and size: [current physical plan, size after filtering, observed memory]
    Resources and cost: [executor resources, concurrent tasks, GC, spill, shuffle bytes]

    [Task]
    Assess fit using measured size and per-executor load, not the label small.
    Compare broadcast with the current strategy, including memory pressure and reduced shuffle.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return supporting and opposing evidence, missing measurements, and a bounded comparison.

    [Checks]
    Check actual plans, peak memory, GC, shuffle, and result equality on the same input.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 찬성·반대 근거, 빠진 측정, 제한된 비교 실험.
- **오류 가능성:** 압축 파일 크기를 메모리 크기와 같다고 보거나 모든 join 양쪽에 shuffle이 있다고 할 수 있다.
- **검증 방법:** 동일 입력의 실제 계획·peak memory·GC·shuffle·결과 일치를 확인한다.

## 출력 파일 수와 task 병렬성 조정 {#spark-03}

- **상황:** 작은 Iceberg 파일을 줄이려고 Spark partition 수를 크게 낮추는 가상 제안이다.
- **제공할 맥락:** 현재 분포: [Spark partition 수·task 시간·파일 크기·Iceberg partition]; 쓰기 설정: [repartition/coalesce 위치·분포 key·목표 파일 크기].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    현재 분포: [Spark partition 수·task 시간·파일 크기·Iceberg partition]
    쓰기 설정: [repartition/coalesce 위치·분포 key·목표 파일 크기]

    [요청]
    Repartition의 shuffle 비용과 coalesce의 병렬성 감소를 비교해 줘.
    Task·table partition 경계와 압축률 때문에 목표 파일 크기가 보장되지 않음을 반영해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    작은 후보 집합과 task 시간·파일 분포·쓰기 비용의 평가표를 작성해 줘.

    [검증]
    동일 데이터에서 한 설정씩 바꾸고 tail task 시간·총 파일 수·크기를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Distribution: [Spark partition count, task times, file sizes, Iceberg partitions]
    Write settings: [repartition/coalesce location, distribution keys, target file size]

    [Task]
    Compare repartition shuffle cost with the parallelism loss from coalesce.
    Account for task and table-partition boundaries and compression; target file size is not guaranteed.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a small candidate set and an evaluation table for task times, file distribution, and write cost.

    [Checks]
    Change one setting at a time on the same data and compare slow-task duration, file counts, and sizes.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 작은 후보 집합과 task 시간·파일 분포·쓰기 비용의 평가표.
- **오류 가능성:** Partition 수를 줄이면 항상 빨라지거나 파일 하나를 task 하나와 같다고 가정할 수 있다.
- **검증 방법:** 동일 데이터에서 한 설정씩 바꾸고 tail task 시간·총 파일 수·크기를 비교한다.

## Cache와 durable 중간 테이블 선택 {#spark-04}

- **상황:** 비싼 변환 결과를 여러 분석과 다음 job에서도 쓰는 가상 workflow다.
- **제공할 맥락:** 재사용 패턴: [action 목록·job 경계·재사용 횟수·수명]; 비용과 자원: [계산 시간·데이터 크기·메모리·재시작 요구].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    재사용 패턴: [action 목록·job 경계·재사용 횟수·수명]
    비용과 자원: [계산 시간·데이터 크기·메모리·재시작 요구]

    [요청]
    Lazy evaluation으로 반복 계산되는 구간을 찾고 실제 action을 표시해 줘.
    Cache/persist, 재계산, Iceberg 중간 테이블을 수명과 비용으로 비교해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    선택 근거와 cache 해제 시점, durable 결과의 관리 항목을 작성해 줘.

    [검증]
    실제 재계산 횟수·cache 사용·쓰기/읽기 비용을 측정하고 재시작 시 재사용 요구를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Reuse pattern: [actions, job boundaries, reuse count, lifetime]
    Cost and resources: [compute time, result size, memory, restart needs]

    [Task]
    Find recomputation caused by lazy evaluation and identify the actions that trigger work.
    Compare cache/persist, recomputation, and an intermediate Iceberg table by lifetime and cost.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return the decision basis, when to release cache, and management needs for durable results.

    [Checks]
    Measure recomputation, cache use, and write/read cost; check reuse needs after restart.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 선택 근거와 cache 해제 시점, durable 결과의 관리 항목.
- **오류 가능성:** Cache가 job 간 영구 보존되거나 한 번만 쓰는 데이터에도 항상 이득이라고 할 수 있다.
- **검증 방법:** 실제 재계산 횟수·cache 사용·쓰기/읽기 비용을 측정하고 재시작 시 재사용 요구를 확인한다.

## foreachBatch 재시도의 중복 효과 검토 {#spark-05}

- **상황:** Micro-batch 실패 후 외부 sink에 중복 결과가 보이는 가상 사례다.
- **제공할 맥락:** 처리 정보: [foreachBatch 로직·batchId·checkpoint·재시도 로그]; Sink 계약: [write 방식·멱등 key·commit 경계·부분 성공 처리].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    처리 정보: [foreachBatch 로직·batchId·checkpoint·재시도 로그]
    Sink 계약: [write 방식·멱등 key·commit 경계·부분 성공 처리]

    [요청]
    Source 복구와 sink 효과의 보장 범위를 분리해 현재 로직을 검토해 줘.
    Batch 재실행과 부분 성공에서 같은 효과가 한 번만 남는지 검토해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    실패 지점별 결과 표와 batchId 등 멱등성 수단의 조건을 작성해 줘.

    [검증]
    격리된 sink에서 같은 batch를 두 번 적용하고 부분 성공 후 결과도 대조하는 계획을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Processing details: [foreachBatch logic, batchId, checkpoint, retry logs]
    Sink contract: [write mode, idempotency keys, commit boundary, partial success]

    [Task]
    Review the logic by separating source recovery from sink effects.
    Check whether batch replay and partial success leave only one final effect.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return results by failure point and conditions for idempotency measures such as batchId.

    [Checks]
    Plan applying the same batch twice in an isolated sink and checking results after partial success.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 실패 지점별 결과 표와 batchId 등 멱등성 수단의 조건.
- **오류 가능성:** Checkpoint나 batchId 존재만으로 end-to-end exactly-once를 보장한다고 할 수 있다.
- **검증 방법:** 격리된 sink에서 같은 batch를 두 번 적용하고 부분 성공 후 결과도 대조하는 계획을 작성한다.

## Streaming output mode와 late event 정책 검토 {#spark-06}

- **상황:** 집계 결과가 늦거나 늦은 이벤트가 빠지는 가상 Structured Streaming 작업이다.
- **제공할 맥락:** 집계 정의: [event time·window·watermark·중복 제거 규칙]; 실행 정보: [output mode·sink·Spark 버전·합성 도착 순서].

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    집계 정의: [event time·window·watermark·중복 제거 규칙]
    실행 정보: [output mode·sink·Spark 버전·합성 도착 순서]

    [요청]
    Watermark를 event-time 진행과 state 정리 기준으로 설명해 줘.
    연산·sink의 output mode 지원을 확인할 항목과 late event 결과를 나눠 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    입력 순서별 기대 집계·출력 시점·state 유지 가정을 표로 작성해 줘.

    [검증]
    버전 문서와 제한된 순서 변경·늦은 표본 실험에서 출력과 state 크기를 대조해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Aggregate definition: [event time, window, watermark, deduplication rules]
    Execution details: [output mode, sink, Spark version, synthetic arrival order]

    [Task]
    Explain watermark behavior as event-time progress and a state-cleanup basis.
    Separate checks for operator/sink output-mode support from late-event outcomes.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return expected aggregates, emission timing, and state-retention assumptions by arrival sequence.

    [Checks]
    Compare version docs with bounded out-of-order and late-data tests, including output and state size.
    Provide review and test plans only; do not run or change production.
    ```

- **기대 결과:** 입력 순서별 기대 집계·출력 시점·state 유지 가정에 대한 표.
- **오류 가능성:** Watermark를 wall-clock 타이머로 보거나 모든 mode가 모든 sink에 가능하다고 할 수 있다.
- **검증 방법:** 버전 문서와 제한된 순서 변경·늦은 표본 실험에서 출력과 state 크기를 대조한다.
