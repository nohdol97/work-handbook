---
id: prompts-flink
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Apache Flink practical prompts

Page type: Reference. These six authored, hypothetical examples apply the [existing study material](../data-platform/flink.md). They do not claim production experience, measured usage frequency, or model results. The examples were not run.

Choose a case and replace bracketed inputs with sanitized information. Each prompt has 한국어 and English tabs for language selection and copying. Treat LLM output as a hypothesis. Check actual settings, logs, official docs, and bounded tests. This page does not authorize production actions or permission changes.

[All prompts](index.md) · [Concepts and sources](../data-platform/flink.md)

## Quick selection

| Purpose | Jump to |
| --- | --- |
| Choose a window that matches the metric | [01](#flink-01) |
| Review state TTL meaning and cleanup | [02](#flink-02) |
| Compare aligned and unaligned checkpoints | [03](#flink-03) |
| Review an upgrade or rescaling from a savepoint | [04](#flink-04) |
| Assess parallelism changes under backpressure | [05](#flink-05) |
| Review the exactly-once boundary through the sink | [06](#flink-06) |

## Choose a window that matches the metric {#flink-01}

- **Situation:** This hypothetical design uses one window method for interval error rates and user activity groups.
- **Context to give the LLM:** Metric needs: [fixed ranges, rolling ranges, activity gaps, latency target]; Time and input: [event time, watermark policy, synthetic event order].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Metric needs: [fixed ranges, rolling ranges, activity gaps, latency target]
    Time and input: [event time, watermark policy, synthetic event order]

    [Task]
    Compare tumbling, sliding, and session windows against the metric definitions.
    Clarify overlap between windows and the conditions for event-time session completion.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return window membership and expected results for each sample, plus late-event policy questions.

    [Checks]
    Compare with manual results for boundary times, long inactivity, and late inputs.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    지표 요구: [고정 구간·이동 구간·활동 간격·응답 목표]
    시간과 입력: [event time·watermark 정책·합성 이벤트 순서]

    [요청]
    Tumbling, sliding, session window를 지표 정의에 맞춰 비교해 줘.
    겹치는 구간의 중복 포함과 event-time session 종료 조건을 명확히 해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    표본별 window 소속과 기대 결과, 늦은 이벤트 정책 질문을 작성해 줘.

    [검증]
    경계 시각·긴 무활동·늦은 입력을 포함한 표본의 수작업 결과와 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Window membership and expected results for each sample, plus late-event policy questions.
- **What the LLM can get wrong:** The LLM may treat session completion as wall-clock waiting or mistake sliding-window overlap for an error.
- **How to validate:** Compare with manual results for boundary times, long inactivity, and late inputs.

## Review state TTL meaning and cleanup {#flink-02}

- **Situation:** Review a hypothetical proposal to shorten TTL because state keeps growing.
- **Context to give the LLM:** State purpose: [keys, state type, value meaning, return interval]; Settings and observations: [TTL, update rule, expired-value visibility, cleanup, size trend].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    State purpose: [keys, state type, value meaning, return interval]
    Settings and observations: [TTL, update rule, expired-value visibility, cleanup, size trend]

    [Task]
    Separate the required memory period from the effects of processing-time TTL.
    Distinguish logical expiry, value visibility, and cleanup; do not describe them as immediate deletion.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return semantic loss and state-cost trade-offs for a shorter TTL, plus version checks.

    [Checks]
    Check value visibility and state size in bounded tests with different updates, reads, and return times.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    State 용도: [key·state 종류·값 의미·재방문 간격]
    설정과 관찰: [TTL·갱신 기준·만료값 가시성·cleanup·크기 추이]

    [요청]
    업무에 필요한 기억 기간과 processing-time TTL의 영향을 구분해 줘.
    논리 만료, 값 가시성, 실제 cleanup을 구분하고 즉시 삭제로 설명하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    짧은 TTL의 의미 손실·상태 비용과 버전별 확인 항목을 작성해 줘.

    [검증]
    갱신·조회·재방문 순서를 바꾼 제한 테스트에서 값 가시성과 state 크기를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Semantic loss and state-cost trade-offs for a shorter TTL, plus version checks.
- **What the LLM can get wrong:** The LLM may treat TTL as an event-time guarantee or promise immediate removal of all bytes.
- **How to validate:** Check value visibility and state size in bounded tests with different updates, reads, and return times.

## Compare aligned and unaligned checkpoints {#flink-03}

- **Situation:** Review rising checkpoint duration in a hypothetical job with backpressure.
- **Context to give the LLM:** Observed metrics: [alignment time, state size, checkpoint size, failure logs]; Environment: [input rates, backpressure, storage bandwidth, recovery target, version].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Observed metrics: [alignment time, state size, checkpoint size, failure logs]
    Environment: [input rates, backpressure, storage bandwidth, recovery target, version]

    [Task]
    Separate barrier waiting from state-storage cost and compare bottleneck hypotheses.
    Review in-flight data recorded by unaligned checkpoints and the storage and recovery costs.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return choice criteria, missing metrics, and an experiment measuring checkpoints and recovery.

    [Checks]
    Compare completion time, size, recovery time, and results with isolated input.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    관찰 지표: [alignment 시간·state 크기·checkpoint 크기·실패 로그]
    환경: [입력별 속도·backpressure·저장 대역폭·복구 목표·버전]

    [요청]
    Barrier 대기와 state 저장 비용을 구분하고 병목 가설을 비교해 줘.
    Unaligned의 in-flight data 기록과 저장·복구 비용을 함께 검토해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    선택 조건, 누락 지표, checkpoint·복구를 함께 측정할 실험을 작성해 줘.

    [검증]
    격리된 입력으로 checkpoint 완료 시간·크기·복구 시간·결과를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Choice criteria, missing metrics, and an experiment measuring checkpoints and recovery.
- **What the LLM can get wrong:** The LLM may equate unaligned checkpoints with simply skipping alignment or with at-least-once mode.
- **How to validate:** Compare completion time, size, recovery time, and results with isolated input.

## Review an upgrade or rescaling from a savepoint {#flink-04}

- **Situation:** This hypothetical change updates job code and parallelism while preserving state.
- **Context to give the LLM:** Change details: [old and new topology, operator identities, state schemas]; Operating conditions: [versions, savepoint details, source retention, sink contract, recovery target].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Change details: [old and new topology, operator identities, state schemas]
    Operating conditions: [versions, savepoint details, source retention, sink contract, recovery target]

    [Task]
    Start by reviewing checks for operator identity and state-schema compatibility.
    Distinguish checkpoint recovery from a planned savepoint change; do not assume compatibility.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return the sequence for preflight, isolated restore, validation, and deciding whether to roll back.

    [Checks]
    Without production-change commands, plan comparisons of restored keyed state, offsets, and sink effects.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    변경 내역: [이전·새 topology·operator identity·state schema]
    운영 조건: [버전·savepoint 정보·source 보존·sink 계약·복구 목표]

    [요청]
    Operator identity와 state schema 호환성을 확인할 항목부터 검토해 줘.
    Checkpoint 복구와 계획된 savepoint 변경을 구분하고 호환성을 가정하지 마.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    사전 점검·격리 복원·검증·되돌림 판단의 순서를 작성해 줘.

    [검증]
    운영 변경 명령 없이 복원 결과의 key별 state·offset·sink 효과를 비교하는 계획을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** The sequence for preflight, isolated restore, validation, and deciding whether to roll back.
- **What the LLM can get wrong:** The LLM may assume a savepoint makes any code change, state change, or rescaling safe.
- **How to validate:** Without production-change commands, plan comparisons of restored keyed state, offsets, and sink effects.

## Assess parallelism changes under backpressure {#flink-05}

- **Situation:** In this hypothetical case, rising consumer lag leads to a proposal to increase source and sink parallelism.
- **Context to give the LLM:** Topology: [Kafka partitions, source/operator parallelism, keyBy keys]; Metrics: [operator rates, busy/backpressure, key distribution, sink latency, errors].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Topology: [Kafka partitions, source/operator parallelism, keyBy keys]
    Metrics: [operator rates, busy/backpressure, key distribution, sink latency, errors]

    [Task]
    Distinguish the upper bound on useful Kafka source concurrency from downstream parallelism.
    Compare hot-key, expensive-operator, and external-sink saturation hypotheses using evidence.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return missing measurements and one load-bounded experiment for each hypothesis.

    [Checks]
    Change one setting at a time and check sink errors, latency, and total throughput as well as lag.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    구조: [Kafka partition 수·source/operator parallelism·keyBy key]
    지표: [operator 처리율·busy/backpressure·키 분포·sink 지연·오류]

    [요청]
    Kafka source의 유효 병렬성 상한과 downstream 병렬성을 구분해 줘.
    Hot key, 무거운 operator, 외부 sink 포화 가설을 근거로 비교해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    가설별 추가 측정과 부하를 제한한 한 가지 실험을 작성해 줘.

    [검증]
    한 설정씩 바꾸며 lag 감소뿐 아니라 sink 오류·지연·전체 처리율을 함께 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Missing measurements and one load-bounded experiment for each hypothesis.
- **What the LLM can get wrong:** The LLM may equate slots with CPU cores or add concurrent writes to an already saturated sink.
- **How to validate:** Change one setting at a time and check sink errors, latency, and total throughput as well as lag.

## Review the exactly-once boundary through the sink {#flink-06}

- **Situation:** In this hypothetical case, checkpoints succeed but external results duplicate after recovery.
- **Context to give the LLM:** Path: [source offsets, keyed state, sink writes, commit flow]; Evidence: [connector/version, transactions or idempotency, failure-point logs].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Path: [source offsets, keyed state, sink writes, commit flow]
    Evidence: [connector/version, transactions or idempotency, failure-point logs]

    [Task]
    Separate Flink state guarantees from external sink guarantees and list conditions at each boundary.
    Trace repeated effects for failures before and after writes and checkpoints.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a failure matrix and the gaps that prevent an end-to-end guarantee.

    [Checks]
    Plan bounded failure-and-recovery tests in an isolated sink and compare final effects by event.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    경로: [source offset·keyed state·sink write·commit 흐름]
    근거: [connector/version·transaction 또는 멱등성·실패 지점 로그]

    [요청]
    Flink 내부 상태와 외부 sink의 보장을 나누고 경계마다 필요한 조건을 적어 줘.
    Write 전·후와 checkpoint 전·후 실패에서 반복 효과를 추적해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    실패 행렬과 end-to-end 보장을 아직 주장할 수 없는 부분을 작성해 줘.

    [검증]
    격리된 sink에서 제한된 실패·복구 실험의 event별 최종 효과를 대조하는 계획을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A failure matrix and the gaps that prevent an end-to-end guarantee.
- **What the LLM can get wrong:** The LLM may treat checkpoint success as proof of every external transaction or assume replay removes duplicates.
- **How to validate:** Plan bounded failure-and-recovery tests in an isolated sink and compare final effects by event.
