---
id: prompts-flink
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Apache Flink 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[전체 프롬프트 모음](index.md) · [개념과 출처](../data-platform/flink.md)

## 빠르게 고르기

| 목적 | 바로 가기 |
| --- | --- |
| 지표 정의에 맞는 window 선택 | [01](#flink-01) |
| State TTL의 업무 의미와 정리 방식 검토 | [02](#flink-02) |
| Checkpoint 지연에서 aligned·unaligned 비교 | [03](#flink-03) |
| Savepoint 기반 업그레이드·rescaling 검토 | [04](#flink-04) |
| Backpressure에서 병렬성 증가의 효과 판단 | [05](#flink-05) |
| 외부 sink까지의 exactly-once 범위 검토 | [06](#flink-06) |

## 지표 정의에 맞는 window 선택 {#flink-01}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    고정 구간 오류율과 사용자 활동 묶음을 하나의 방식으로 계산하려는 설계다.
    Tumbling, sliding, session window를 지표 정의에 맞춰 비교해 줘.
    겹치는 구간의 중복 포함과 event-time session 종료 조건을 명확히 해 줘.
    표본별 window 소속과 기대 결과, 늦은 이벤트 정책 질문을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    This design uses one window method for interval error rates and user activity groups.
    Compare tumbling, sliding, and session windows against the metric definitions.
    Clarify overlap between windows and the conditions for event-time session completion.
    Return window membership and expected results for each sample, plus late-event policy questions.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 업무 지표의 구간 경계와 늦은 이벤트 허용 규칙. source·operator·sink 근거를 같은 실행과 시각 범위로 묶는다. Session 종료를 단순 wall-clock 대기로 보거나 sliding window의 겹침을 계산 오류로 볼 수 있다. 중첩 window의 중복 포함이 의도인지 업무 정의로 확인한다.

## State TTL의 업무 의미와 정리 방식 검토 {#flink-02}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    State가 계속 커져 TTL을 짧게 줄이자는 제안을 검토 중이야.
    업무에 필요한 기억 기간과 processing-time TTL의 영향을 구분해 줘.
    논리 만료, 값 가시성, 실제 cleanup을 구분하고 즉시 삭제로 설명하지 마.
    짧은 TTL의 의미 손실·상태 비용과 버전별 확인 항목을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review a proposal to shorten TTL because state keeps growing.
    Separate the required memory period from the effects of processing-time TTL.
    Distinguish logical expiry, value visibility, and cleanup; do not describe them as immediate deletion.
    Return semantic loss and state-cost trade-offs for a shorter TTL, plus version checks.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: key 재방문 간격과 만료 후 기대 행동. source·operator·sink 근거를 같은 실행과 시각 범위로 묶는다. TTL을 event-time 보장으로 보거나 시간이 지나면 모든 바이트가 즉시 사라진다고 할 수 있다. 만료값 비가시성과 실제 저장 공간 회수를 구분해 판정한다.

## Checkpoint 지연에서 aligned·unaligned 비교 {#flink-03}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Backpressure가 있는 job에서 checkpoint 시간이 늘어나는 현상을 검토 중이야.
    Barrier 대기와 state 저장 비용을 구분하고 병목 가설을 비교해 줘.
    Unaligned의 in-flight data 기록과 저장·복구 비용을 함께 검토해 줘.
    선택 조건, 누락 지표, checkpoint·복구를 함께 측정할 실험을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review rising checkpoint duration in a job with backpressure.
    Separate barrier waiting from state-storage cost and compare bottleneck hypotheses.
    Review in-flight data recorded by unaligned checkpoints and the storage and recovery costs.
    Return choice criteria, missing metrics, and an experiment measuring checkpoints and recovery.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: alignment 대기와 저장 I/O를 분리한 checkpoint 지표. source·operator·sink 근거를 같은 실행과 시각 범위로 묶는다. Unaligned를 단순 alignment 생략이나 at-least-once 모드와 같다고 설명할 수 있다. checkpoint 단축과 복구 시간 악화를 함께 기록한다.

## Savepoint 기반 업그레이드·rescaling 검토 {#flink-04}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    State를 유지한 채 job의 코드와 parallelism을 바꾸려는 상황이야.
    Operator identity와 state schema 호환성을 확인할 항목부터 검토해 줘.
    Checkpoint 복구와 계획된 savepoint 변경을 구분하고 호환성을 가정하지 마.
    사전 점검·격리 복원·검증·되돌림 판단의 순서를 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    This change updates job code and parallelism while preserving state.
    Start by reviewing checks for operator identity and state-schema compatibility.
    Distinguish checkpoint recovery from a planned savepoint change; do not assume compatibility.
    Return the sequence for preflight, isolated restore, validation, and deciding whether to roll back.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: operator identity·state schema 대응과 복원 가능한 source 구간. source·operator·sink 근거를 같은 실행과 시각 범위로 묶는다. Savepoint가 있으면 모든 코드·state 변경과 rescaling이 자동으로 안전하다고 할 수 있다. savepoint 생성 성공만으로 새 코드 복원 성공을 대신하지 않는다.

## Backpressure에서 병렬성 증가의 효과 판단 {#flink-05}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Consumer lag이 늘어 source와 sink parallelism을 늘리자는 상황이야.
    Kafka source의 유효 병렬성 상한과 downstream 병렬성을 구분해 줘.
    Hot key, 무거운 operator, 외부 sink 포화 가설을 근거로 비교해 줘.
    가설별 추가 측정과 부하를 제한한 한 가지 실험을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Rising consumer lag leads to a proposal to increase source and sink parallelism.
    Distinguish the upper bound on useful Kafka source concurrency from downstream parallelism.
    Compare hot-key, expensive-operator, and external-sink saturation hypotheses using evidence.
    Return missing measurements and one load-bounded experiment for each hypothesis.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: operator별 처리율과 sink 포화 여부. source·operator·sink 근거를 같은 실행과 시각 범위로 묶는다. Slot을 CPU core와 같다고 보거나 이미 포화된 sink에 병렬 쓰기를 더 권할 수 있다. source lag 감소가 sink 오류 증가를 가리지 않아야 한다.

## 외부 sink까지의 exactly-once 범위 검토 {#flink-06}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    Checkpoint는 성공하지만 복구 후 외부 결과에 중복이 생기는 상황이야.
    Flink 내부 상태와 외부 sink의 보장을 나누고 경계마다 필요한 조건을 적어 줘.
    Write 전·후와 checkpoint 전·후 실패에서 반복 효과를 추적해 줘.
    실패 행렬과 end-to-end 보장을 아직 주장할 수 없는 부분을 작성해 줘.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Checkpoints succeed but external results duplicate after recovery.
    Separate Flink state guarantees from external sink guarantees and list conditions at each boundary.
    Trace repeated effects for failures before and after writes and checkpoints.
    Return a failure matrix and the gaps that prevent an end-to-end guarantee.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: sink commit 경계와 해당 connector의 복구 계약. source·operator·sink 근거를 같은 실행과 시각 범위로 묶는다. Checkpoint 성공이 외부 transaction 성공을 모두 증명하거나 source replay가 중복을 없앤다고 할 수 있다. 최종 sink 효과를 event별로 확인하지 못하면 end-to-end 보장을 보류한다.
