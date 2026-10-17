---
id: prompts-flink
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Apache Flink practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

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

Example prompt:

=== "English"

    ```text {.prompt}
    This design uses one window method for interval error rates and user activity groups.
    Compare tumbling, sliding, and session windows against the metric definitions.
    Clarify overlap between windows and the conditions for event-time session completion.
    Return window membership and expected results for each sample, plus late-event policy questions.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    고정 구간 오류율과 사용자 활동 묶음을 하나의 방식으로 계산하려는 설계다.
    Tumbling, sliding, session window를 지표 정의에 맞춰 비교해 줘.
    겹치는 구간의 중복 포함과 event-time session 종료 조건을 명확히 해 줘.
    표본별 window 소속과 기대 결과, 늦은 이벤트 정책 질문을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: business window boundaries and late-event rules. Group source, operator, and sink evidence by run and time range. The LLM may treat session completion as wall-clock waiting or mistake sliding-window overlap for an error. Check intended overlap against the business metric definition.

## Review state TTL meaning and cleanup {#flink-02}

Example prompt:

=== "English"

    ```text {.prompt}
    Review a proposal to shorten TTL because state keeps growing.
    Separate the required memory period from the effects of processing-time TTL.
    Distinguish logical expiry, value visibility, and cleanup; do not describe them as immediate deletion.
    Return semantic loss and state-cost trade-offs for a shorter TTL, plus version checks.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    State가 계속 커져 TTL을 짧게 줄이자는 제안을 검토 중이야.
    업무에 필요한 기억 기간과 processing-time TTL의 영향을 구분해 줘.
    논리 만료, 값 가시성, 실제 cleanup을 구분하고 즉시 삭제로 설명하지 마.
    짧은 TTL의 의미 손실·상태 비용과 버전별 확인 항목을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: key return intervals and expected behavior after expiry. Group source, operator, and sink evidence by run and time range. The LLM may treat TTL as an event-time guarantee or promise immediate removal of all bytes. Judge expired-value visibility separately from physical space reclamation.

## Compare aligned and unaligned checkpoints {#flink-03}

Example prompt:

=== "English"

    ```text {.prompt}
    Review rising checkpoint duration in a job with backpressure.
    Separate barrier waiting from state-storage cost and compare bottleneck hypotheses.
    Review in-flight data recorded by unaligned checkpoints and the storage and recovery costs.
    Return choice criteria, missing metrics, and an experiment measuring checkpoints and recovery.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Backpressure가 있는 job에서 checkpoint 시간이 늘어나는 현상을 검토 중이야.
    Barrier 대기와 state 저장 비용을 구분하고 병목 가설을 비교해 줘.
    Unaligned의 in-flight data 기록과 저장·복구 비용을 함께 검토해 줘.
    선택 조건, 누락 지표, checkpoint·복구를 함께 측정할 실험을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: checkpoint metrics separating alignment waits from storage I/O. Group source, operator, and sink evidence by run and time range. The LLM may equate unaligned checkpoints with simply skipping alignment or with at-least-once mode. Record checkpoint improvements together with any worse recovery time.

## Review an upgrade or rescaling from a savepoint {#flink-04}

Example prompt:

=== "English"

    ```text {.prompt}
    This change updates job code and parallelism while preserving state.
    Start by reviewing checks for operator identity and state-schema compatibility.
    Distinguish checkpoint recovery from a planned savepoint change; do not assume compatibility.
    Return the sequence for preflight, isolated restore, validation, and deciding whether to roll back.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    State를 유지한 채 job의 코드와 parallelism을 바꾸려는 상황이야.
    Operator identity와 state schema 호환성을 확인할 항목부터 검토해 줘.
    Checkpoint 복구와 계획된 savepoint 변경을 구분하고 호환성을 가정하지 마.
    사전 점검·격리 복원·검증·되돌림 판단의 순서를 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: operator identity/state-schema mapping and the restorable source range. Group source, operator, and sink evidence by run and time range. The LLM may assume a savepoint makes any code change, state change, or rescaling safe. Do not treat savepoint creation as proof that new code can restore it.

## Assess parallelism changes under backpressure {#flink-05}

Example prompt:

=== "English"

    ```text {.prompt}
    Rising consumer lag leads to a proposal to increase source and sink parallelism.
    Distinguish the upper bound on useful Kafka source concurrency from downstream parallelism.
    Compare hot-key, expensive-operator, and external-sink saturation hypotheses using evidence.
    Return missing measurements and one load-bounded experiment for each hypothesis.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Consumer lag이 늘어 source와 sink parallelism을 늘리자는 상황이야.
    Kafka source의 유효 병렬성 상한과 downstream 병렬성을 구분해 줘.
    Hot key, 무거운 operator, 외부 sink 포화 가설을 근거로 비교해 줘.
    가설별 추가 측정과 부하를 제한한 한 가지 실험을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: per-operator throughput and whether the sink is saturated. Group source, operator, and sink evidence by run and time range. The LLM may equate slots with CPU cores or add concurrent writes to an already saturated sink. Ensure lower source lag does not hide rising sink errors.

## Review the exactly-once boundary through the sink {#flink-06}

Example prompt:

=== "English"

    ```text {.prompt}
    Checkpoints succeed but external results duplicate after recovery.
    Separate Flink state guarantees from external sink guarantees and list conditions at each boundary.
    Trace repeated effects for failures before and after writes and checkpoints.
    Return a failure matrix and the gaps that prevent an end-to-end guarantee.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Checkpoint는 성공하지만 복구 후 외부 결과에 중복이 생기는 상황이야.
    Flink 내부 상태와 외부 sink의 보장을 나누고 경계마다 필요한 조건을 적어 줘.
    Write 전·후와 checkpoint 전·후 실패에서 반복 효과를 추적해 줘.
    실패 행렬과 end-to-end 보장을 아직 주장할 수 없는 부분을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the sink commit boundary and connector recovery contract. Group source, operator, and sink evidence by run and time range. The LLM may treat checkpoint success as proof of every external transaction or assume replay removes duplicates. Hold an end-to-end guarantee until final sink effects are checked per event.
