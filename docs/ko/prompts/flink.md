---
id: prompts-flink
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Apache Flink 실무 프롬프트

문서 유형: Reference. [기존 학습 내용](../data-platform/flink.md)을 적용하도록 작성한 가상의 재사용 예시 6개다. 실제 업무 경험, 사용 빈도 조사, 모델 실행 결과를 뜻하지 않는다. 예시를 실행하지 않았다.

상황에 맞는 예시를 고르고 대괄호 입력을 익명화한 자료로 바꾼다. 각 예시는 한국어·English 탭에서 언어를 선택해 복사할 수 있다. LLM의 답은 가설이며 실제 설정·로그·공식 문서·제한된 검증으로 확인한다. 운영 실행이나 권한 변경을 허가하는 문서는 아니다.

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

- **상황:** 고정 구간 오류율과 사용자 활동 묶음을 하나의 방식으로 계산하려는 가상 설계다.
- **제공할 맥락:** 지표 요구: [고정 구간·이동 구간·활동 간격·응답 목표]; 시간과 입력: [event time·watermark 정책·합성 이벤트 순서].

예시 프롬프트:

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

- **기대 결과:** 표본별 window 소속과 기대 결과, 늦은 이벤트 정책 질문.
- **오류 가능성:** Session 종료를 단순 wall-clock 대기로 보거나 sliding window의 겹침을 계산 오류로 볼 수 있다.
- **검증 방법:** 경계 시각·긴 무활동·늦은 입력을 포함한 표본의 수작업 결과와 비교한다.

## State TTL의 업무 의미와 정리 방식 검토 {#flink-02}

- **상황:** State가 계속 커져 TTL을 짧게 줄이자는 가상 제안을 검토한다.
- **제공할 맥락:** State 용도: [key·state 종류·값 의미·재방문 간격]; 설정과 관찰: [TTL·갱신 기준·만료값 가시성·cleanup·크기 추이].

예시 프롬프트:

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

- **기대 결과:** 짧은 TTL의 의미 손실·상태 비용과 버전별 확인 항목.
- **오류 가능성:** TTL을 event-time 보장으로 보거나 시간이 지나면 모든 바이트가 즉시 사라진다고 할 수 있다.
- **검증 방법:** 갱신·조회·재방문 순서를 바꾼 제한 테스트에서 값 가시성과 state 크기를 확인한다.

## Checkpoint 지연에서 aligned·unaligned 비교 {#flink-03}

- **상황:** Backpressure가 있는 가상 job에서 checkpoint 시간이 늘어나는 현상을 검토한다.
- **제공할 맥락:** 관찰 지표: [alignment 시간·state 크기·checkpoint 크기·실패 로그]; 환경: [입력별 속도·backpressure·저장 대역폭·복구 목표·버전].

예시 프롬프트:

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

- **기대 결과:** 선택 조건, 누락 지표, checkpoint·복구를 함께 측정할 실험.
- **오류 가능성:** Unaligned를 단순 alignment 생략이나 at-least-once 모드와 같다고 설명할 수 있다.
- **검증 방법:** 격리된 입력으로 checkpoint 완료 시간·크기·복구 시간·결과를 비교한다.

## Savepoint 기반 업그레이드·rescaling 검토 {#flink-04}

- **상황:** State를 유지한 채 가상 job의 코드와 parallelism을 바꾸려는 사례다.
- **제공할 맥락:** 변경 내역: [이전·새 topology·operator identity·state schema]; 운영 조건: [버전·savepoint 정보·source 보존·sink 계약·복구 목표].

예시 프롬프트:

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

- **기대 결과:** 사전 점검·격리 복원·검증·되돌림 판단의 순서.
- **오류 가능성:** Savepoint가 있으면 모든 코드·state 변경과 rescaling이 자동으로 안전하다고 할 수 있다.
- **검증 방법:** 운영 변경 명령 없이 복원 결과의 key별 state·offset·sink 효과를 비교하는 계획을 작성한다.

## Backpressure에서 병렬성 증가의 효과 판단 {#flink-05}

- **상황:** Consumer lag이 늘어 source와 sink parallelism을 늘리자는 가상 사례다.
- **제공할 맥락:** 구조: [Kafka partition 수·source/operator parallelism·keyBy key]; 지표: [operator 처리율·busy/backpressure·키 분포·sink 지연·오류].

예시 프롬프트:

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

- **기대 결과:** 가설별 추가 측정과 부하를 제한한 한 가지 실험.
- **오류 가능성:** Slot을 CPU core와 같다고 보거나 이미 포화된 sink에 병렬 쓰기를 더 권할 수 있다.
- **검증 방법:** 한 설정씩 바꾸며 lag 감소뿐 아니라 sink 오류·지연·전체 처리율을 함께 확인한다.

## 외부 sink까지의 exactly-once 범위 검토 {#flink-06}

- **상황:** Checkpoint는 성공하지만 복구 후 외부 결과에 중복이 생기는 가상 사례다.
- **제공할 맥락:** 경로: [source offset·keyed state·sink write·commit 흐름]; 근거: [connector/version·transaction 또는 멱등성·실패 지점 로그].

예시 프롬프트:

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

- **기대 결과:** 실패 행렬과 end-to-end 보장을 아직 주장할 수 없는 부분.
- **오류 가능성:** Checkpoint 성공이 외부 transaction 성공을 모두 증명하거나 source replay가 중복을 없앤다고 할 수 있다.
- **검증 방법:** 격리된 sink에서 제한된 실패·복구 실험의 event별 최종 효과를 대조하는 계획을 작성한다.
