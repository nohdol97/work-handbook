---
id: prompts-orchestration
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Data orchestration practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[Concept guide](../data-platform/orchestration.md) · [All prompts](index.md)

| # | Jump to a situation |
| --- | --- |
| 01 | [Separate a schedule from input readiness](#orchestration-01) |
| 02 | [Review retries by failure type](#orchestration-02) |
| 03 | [Choose where to resume after a task failure](#orchestration-03) |
| 04 | [Investigate publication after a quality failure](#orchestration-04) |
| 05 | [Review XCom and worker responsibilities](#orchestration-05) |
| 06 | [Define repeatable date and time intervals](#orchestration-06) |

## Separate a schedule from input readiness {#orchestration-01}

**Prompt:**

=== "English"

    ```text {.prompt}
    A DAG scheduled at 02:00 tries to read input that has not arrived.
    Review run time and data-readiness conditions separately.
    Check whether partial file arrival is mistaken for complete input.
    Separate observed delay, possible causes, and missing readiness evidence.
    Return a proceed decision table for ready, not ready, and unknown states.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    02시에 실행한 DAG가 아직 도착하지 않은 입력을 읽는다.
    실행 시각과 데이터 준비 조건을 별도로 검토해 주세요.
    일부 파일 도착을 전체 입력 완료로 보는지 확인해 주세요.
    관측된 지연·추정 원인·누락된 준비 근거를 구분해 주세요.
    준비·미준비·확인 불가 상태별 task 진행 판단표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: the readiness condition for the complete input. Label DAG configuration and task-run records as separate evidence. The LLM may assume a later schedule guarantees readiness or suggest unsupported provider features. Reject a proposal that lets partial file arrival advance downstream tasks.

## Review retries by failure type {#orchestration-02}

**Prompt:**

=== "English"

    ```text {.prompt}
    One retry policy handles both network timeouts and SQL syntax errors.
    Separate transient and permanent failure candidates and the evidence needed.
    Review duplicate risk at each write boundary during retries.
    Do not infer idempotency from MERGE or overwrite names alone.
    Return a table of retry candidates, fixes needed first, and evidence by error.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    동일 retry 정책이 network timeout과 SQL syntax error에 적용된다.
    일시·영구 실패 후보와 판단에 필요한 증거를 분리해 주세요.
    반복 실행의 중복 위험을 write 경계별로 검토해 주세요.
    MERGE·overwrite 이름만으로 멱등성을 인정하지 말아 주세요.
    오류별 재시도 후보·수정 선행 조건·확인 근거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: partial-write state and final effects of rerunning the same interval. Label DAG configuration and task-run records as separate evidence. The LLM may increase retries for every error or miss duplicate partial writes. Verify partial success and duplicate effects before increasing retries.

## Choose where to resume after a task failure {#orchestration-03}

**Prompt:**

=== "English"

    ```text {.prompt}
    Extract and Spark succeeded, but dbt failed. Review how to resume the run.
    First assess whether upstream results remain valid for the same interval.
    Separate conditions for resuming at failure from those requiring a broader rerun.
    Separate known state, assumptions, and missing output checks.
    List tasks to reuse, rerun, or hold, with reasons.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Extract와 Spark는 성공했고 dbt가 실패한 실행을 복구하려 한다.
    기존 upstream 결과가 동일 구간에서 유효한지 먼저 평가해 주세요.
    실패 지점 재개와 더 넓은 재실행이 필요한 조건을 나눠 주세요.
    확인된 상태·가정·누락된 출력 검증을 구분해 주세요.
    재사용·재실행·보류할 task 목록과 이유를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: interval, version, and validation state of upstream output to reuse. Label DAG configuration and task-run records as separate evidence. The LLM may reuse stale upstream output based only on success status or rerun the whole DAG without need. Do not reuse successful output that fails the changed downstream contract.

## Investigate publication after a quality failure {#orchestration-04}

**Prompt:**

=== "English"

    ```text {.prompt}
    Review a run where publication started after a quality task failed.
    Review the actual trigger rule for each combination of states.
    Do not treat all_success and all_done as equivalent.
    Separate intended publication conditions from observed execution.
    Return expected and observed publication outcomes by upstream state.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    Quality task가 실패했는데 publish task가 실행된 상태를 검토 중이야.
    실제 trigger rule을 상태 조합별로 검토해 주세요.
    all_success와 all_done의 결과를 혼동하지 말아 주세요.
    의도한 공개 조건과 관측된 실행을 구분해 주세요.
    Upstream 상태별 publish 기대·관측 결과표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: actual trigger rules and combinations of success, failed, and skipped states. Label DAG configuration and task-run records as separate evidence. The LLM may assume every downstream task is blocked by failure or that skipped always means successful. Require safe publication behavior for skipped paths as well as failed quality checks.

## Review XCom and worker responsibilities {#orchestration-05}

**Prompt:**

=== "English"

    ```text {.prompt}
    A DAG passes a large dataset through XCom and transforms it inside a worker.
    Review orchestration and compute responsibilities separately.
    Identify candidates for passing small states or paths and checking their validity.
    Mark missing evidence that connects external job success to task success.
    Return input and output contracts across tasks, compute, and storage.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    DAG task가 대량 데이터를 XCom으로 전달하고 worker에서 변환한다.
    Orchestration과 실제 compute 책임을 분리해 검토해 주세요.
    작은 상태·경로 전달로 바꿀 후보와 유효성 확인을 정리해 주세요.
    외부 job 성공과 task 성공의 연결 근거가 부족하면 표시해 주세요.
    Task·compute·storage 사이의 입력·출력 계약표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: actual XCom payload size and external-job completion checks. Label DAG configuration and task-run records as separate evidence. The LLM may assume passing a path solves readiness, interval, and rerun issues by itself. Check that path-based handoff still rejects partial output and wrong intervals.

## Define repeatable date and time intervals {#orchestration-06}

**Prompt:**

=== "English"

    ```text {.prompt}
    A rerun for the same past date changes its result because it uses now().
    Identify inputs tied to run time and inputs tied to explicit intervals.
    Review overlap, gaps, and timezone boundaries between adjacent intervals.
    Separate observed differences from hypotheses about time conditions.
    Return a mapping of interval parameters, input filters, and output partitions.
    Review only; do not apply changes.
    ```

=== "한국어"

    ```text {.prompt}
    같은 과거 날짜의 DAG를 재실행했는데 now() 때문에 결과가 달라진다.
    실행 시각에 의존하는 입력과 명시적 구간 입력을 찾아 주세요.
    인접 구간의 중복·누락 및 timezone 변환 경계를 검토해 주세요.
    관측된 차이와 시간 조건에 대한 가설을 분리해 주세요.
    구간 parameter·입력 filter·출력 partition 대응표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

**Key point:** Evidence to check first: interval start/end inclusion rules and timezone. Label DAG configuration and task-run records as separate evidence. The LLM may assume matching date strings imply matching timezones and input intervals. Require reproducibility for the same input set, not merely the same date string.
