---
id: prompts-spark
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Apache Spark 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

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

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Join 후 row 수가 크게 늘어난 ETL을 검토 중이야.
    키 중복으로 생기는 다대다 곱과 의도한 관계를 먼저 비교해 줘.
    존재 여부만 필요하다면 semi/anti join의 의미를 검토하고 임의 dedup은 피해 줘.
    키별 예상 row 수 계산과 의미를 보존하는 수정 초안을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Review an ETL whose row count grows sharply after a join.
    First compare duplicate-key multiplication with the intended relationship.
    If only existence matters, review semi or anti join semantics; avoid arbitrary deduplication.
    Return expected counts by key and a draft change that preserves meaning.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 양쪽 grain과 key별 기대 매칭 수. 계획·task 지표·샘플 결과가 같은 실행을 가리키게 준비한다. Broadcast나 repartition만으로 잘못된 grain을 해결하거나 중복 row를 무조건 삭제할 수 있다. DISTINCT로 행 수만 맞춘 결과는 원래 집계 의미와 대조한다.

## Broadcast join의 메모리 적합성 검토 {#spark-02}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    작은 dimension을 broadcast하자는 성능 제안을 검토 중이야.
    작다는 이름 대신 실제 크기와 executor별 부담으로 적합성을 평가해 줘.
    Broadcast와 현 join 전략을 비교하고 메모리 압박과 shuffle 감소를 함께 다뤄 줘.
    찬성·반대 근거, 빠진 측정, 제한된 비교 실험을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Review a proposal to broadcast a small dimension table.
    Assess fit using measured size and per-executor load, not the label small.
    Compare broadcast with the current strategy, including memory pressure and reduced shuffle.
    Return supporting and opposing evidence, missing measurements, and a bounded comparison.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 필터 뒤 build 데이터의 실측 메모리와 executor 여유. 계획·task 지표·샘플 결과가 같은 실행을 가리키게 준비한다. 압축 파일 크기를 메모리 크기와 같다고 보거나 모든 join 양쪽에 shuffle이 있다고 할 수 있다. 파일 압축 크기를 메모리 수요로 대신하지 않는다.

## 출력 파일 수와 task 병렬성 조정 {#spark-03}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    작은 Iceberg 파일을 줄이려고 Spark partition 수를 크게 낮추는 제안이다.
    Repartition의 shuffle 비용과 coalesce의 병렬성 감소를 비교해 줘.
    Task·table partition 경계와 압축률 때문에 목표 파일 크기가 보장되지 않음을 반영해 줘.
    작은 후보 집합과 task 시간·파일 분포·쓰기 비용의 평가표를 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    This proposal sharply reduces Spark partitions to produce fewer small Iceberg files.
    Compare repartition shuffle cost with the parallelism loss from coalesce.
    Account for task and table-partition boundaries and compression; target file size is not guaranteed.
    Return a small candidate set and an evaluation table for task times, file distribution, and write cost.
    ```

**핵심 사항:** 판단 전에 확인할 근거: table partition별 출력 분포와 tail task 시간. 계획·task 지표·샘플 결과가 같은 실행을 가리키게 준비한다. Partition 수를 줄이면 항상 빨라지거나 파일 하나를 task 하나와 같다고 가정할 수 있다. 파일 감소와 함께 느려진 쓰기·skew를 확인한다.

## Cache와 durable 중간 테이블 선택 {#spark-04}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    비싼 변환 결과를 여러 분석과 다음 job에서도 쓰는 workflow다.
    Lazy evaluation으로 반복 계산되는 구간을 찾고 실제 action을 표시해 줘.
    Cache/persist, 재계산, Iceberg 중간 테이블을 수명과 비용으로 비교해 줘.
    선택 근거와 cache 해제 시점, durable 결과의 관리 항목을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    This workflow reuses an expensive result in several analyses and a later job.
    Find recomputation caused by lazy evaluation and identify the actions that trigger work.
    Compare cache/persist, recomputation, and an intermediate Iceberg table by lifetime and cost.
    Return the decision basis, when to release cache, and management needs for durable results.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 재사용이 같은 애플리케이션 안인지 다른 job인지. 계획·task 지표·샘플 결과가 같은 실행을 가리키게 준비한다. Cache가 job 간 영구 보존되거나 한 번만 쓰는 데이터에도 항상 이득이라고 할 수 있다. 재시작 후 필요한 결과를 cache만으로 보존한다고 가정하지 않는다.

## foreachBatch 재시도의 중복 효과 검토 {#spark-05}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Micro-batch 실패 후 외부 sink에 중복 결과가 보이는 상황이야.
    Source 복구와 sink 효과의 보장 범위를 분리해 현재 로직을 검토해 줘.
    Batch 재실행과 부분 성공에서 같은 효과가 한 번만 남는지 검토해 줘.
    실패 지점별 결과 표와 batchId 등 멱등성 수단의 조건을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    An external sink shows duplicates after a micro-batch failure.
    Review the logic by separating source recovery from sink effects.
    Check whether batch replay and partial success leave only one final effect.
    Return results by failure point and conditions for idempotency measures such as batchId.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 부분 write 성공 기록과 batch 식별자의 유효 범위. 계획·task 지표·샘플 결과가 같은 실행을 가리키게 준비한다. Checkpoint나 batchId 존재만으로 end-to-end exactly-once를 보장한다고 할 수 있다. 같은 batch 재시도와 새 checkpoint에서의 재처리를 구분한다.

## Streaming output mode와 late event 정책 검토 {#spark-06}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    집계 결과가 늦거나 늦은 이벤트가 빠지는 Structured Streaming 작업이다.
    Watermark를 event-time 진행과 state 정리 기준으로 설명해 줘.
    연산·sink의 output mode 지원을 확인할 항목과 late event 결과를 나눠 줘.
    입력 순서별 기대 집계·출력 시점·state 유지 가정을 표로 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    This Structured Streaming aggregate is delayed or omits late events.
    Explain watermark behavior as event-time progress and a state-cleanup basis.
    Separate checks for operator/sink output-mode support from late-event outcomes.
    Return expected aggregates, emission timing, and state-retention assumptions by arrival sequence.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 output mode·sink 지원과 늦은 입력의 처리 계약. 계획·task 지표·샘플 결과가 같은 실행을 가리키게 준비한다. Watermark를 wall-clock 타이머로 보거나 모든 mode가 모든 sink에 가능하다고 할 수 있다. watermark가 진행되지 않는 표본과 경계 밖 입력을 포함한다.
