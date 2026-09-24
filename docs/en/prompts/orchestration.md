---
id: prompts-orchestration
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Data orchestration practical prompts

These six hypothetical, reusable examples apply the existing concepts. They do not report measured usage frequency, execution results, new studied curriculum, or production experience. Replace [placeholders] with non-secret context and synthetic data. Model output is a draft to validate. These prompts do not authorize production actions.

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

**Situation:** A DAG scheduled at 02:00 tries to read input that has not arrived.

**Context to give the LLM:** Schedule, timezone, and data interval: [settings] Input arrival records and readiness definition: [synthetic records and conditions] Sensor or event support and Airflow/provider versions: [settings]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Schedule, timezone, and data interval: [settings]
    Input arrival records and readiness definition: [synthetic records and conditions]
    Sensor or event support and Airflow/provider versions: [settings]

    [Task]
    Review run time and data-readiness conditions separately.
    Check whether partial file arrival is mistaken for complete input.
    Separate observed delay, possible causes, and missing readiness evidence.

    [Output]
    Return a proceed decision table for ready, not ready, and unknown states.
    List applicability checks for polling and event-based options.

    [Checks]
    Compare normal, late, and partial-arrival cases with the readiness condition.
    Check waiting conditions in provider documentation and actual DAG dependencies.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Schedule·timezone·data interval: [설정]
    입력 도착 기록과 준비 완료 정의: [가상 기록·조건]
    Sensor·event 기능과 Airflow/provider 버전: [설정]

    [요청]
    실행 시각과 데이터 준비 조건을 별도로 검토해 주세요.
    일부 파일 도착을 전체 입력 완료로 보는지 확인해 주세요.
    관측된 지연·추정 원인·누락된 준비 근거를 구분해 주세요.

    [출력]
    준비·미준비·확인 불가 상태별 task 진행 판단표를 주세요.
    Polling과 event 방식의 적용 확인 항목을 적어 주세요.

    [검증]
    정상·지연·부분 도착 가상 사례를 준비 조건과 대조해 주세요.
    실제 provider 문서와 DAG 의존성에서 대기 조건을 확인해 주세요.
    ```

**Expected output:** Return a proceed decision table for ready, not ready, and unknown states. List applicability checks for polling and event-based options.

**What the LLM can get wrong:** The LLM may assume a later schedule guarantees readiness or suggest unsupported provider features.

**How to validate:** Compare normal, late, and partial-arrival cases with the readiness condition. Check waiting conditions in provider documentation and actual DAG dependencies.

## Review retries by failure type {#orchestration-02}

**Situation:** One retry policy handles both network timeouts and SQL syntax errors.

**Context to give the LLM:** Sanitized error types, times, and retry records: [logs] Task input interval, write method, and keys: [settings] Partial writes and transaction boundaries: [observations and settings]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Sanitized error types, times, and retry records: [logs]
    Task input interval, write method, and keys: [settings]
    Partial writes and transaction boundaries: [observations and settings]

    [Task]
    Separate transient and permanent failure candidates and the evidence needed.
    Review duplicate risk at each write boundary during retries.
    Do not infer idempotency from MERGE or overwrite names alone.

    [Output]
    Return a table of retry candidates, fixes needed first, and evidence by error.
    Propose a small input to check reruns after partial success.

    [Checks]
    Compare expected rows, keys, and totals after processing one interval twice.
    Check whether actual errors and task settings support each failure classification.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    익명화한 오류 유형·시각·retry 기록: [로그]
    Task의 입력 구간·write 방식·key: [설정]
    부분 쓰기 여부와 transaction 경계: [관찰·설정]

    [요청]
    일시·영구 실패 후보와 판단에 필요한 증거를 분리해 주세요.
    반복 실행의 중복 위험을 write 경계별로 검토해 주세요.
    MERGE·overwrite 이름만으로 멱등성을 인정하지 말아 주세요.

    [출력]
    오류별 재시도 후보·수정 선행 조건·확인 근거 표를 주세요.
    부분 성공 뒤 재실행을 검증할 작은 입력을 제안해 주세요.

    [검증]
    같은 구간을 두 번 처리한 기대 행 수·key·합계를 비교해 주세요.
    실제 오류와 task 설정이 제안한 실패 분류를 뒷받침하는지 확인해 주세요.
    ```

**Expected output:** Return a table of retry candidates, fixes needed first, and evidence by error. Propose a small input to check reruns after partial success.

**What the LLM can get wrong:** The LLM may increase retries for every error or miss duplicate partial writes.

**How to validate:** Compare expected rows, keys, and totals after processing one interval twice. Check whether actual errors and task settings support each failure classification.

## Choose where to resume after a task failure {#orchestration-03}

**Situation:** Extract and Spark succeeded, but dbt failed. Review how to resume the run.

**Context to give the LLM:** DAG dependencies and task states: [synthetic run] Input intervals, output locations, and checks by task: [records] Changed dbt logic and upstream reuse conditions: [change and conditions]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    DAG dependencies and task states: [synthetic run]
    Input intervals, output locations, and checks by task: [records]
    Changed dbt logic and upstream reuse conditions: [change and conditions]

    [Task]
    First assess whether upstream results remain valid for the same interval.
    Separate conditions for resuming at failure from those requiring a broader rerun.
    Separate known state, assumptions, and missing output checks.

    [Output]
    List tasks to reuse, rerun, or hold, with reasons.
    Propose checks before quality validation and publication.

    [Checks]
    Match actual output intervals, schemas, and checks to task records.
    Check that downstream tasks receive valid input in a bounded synthetic failure flow.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    DAG dependency와 task별 상태: [가상 실행]
    각 task의 입력 구간·출력 위치·검증 결과: [기록]
    수정한 dbt logic과 upstream 재사용 조건: [변경·조건]

    [요청]
    기존 upstream 결과가 동일 구간에서 유효한지 먼저 평가해 주세요.
    실패 지점 재개와 더 넓은 재실행이 필요한 조건을 나눠 주세요.
    확인된 상태·가정·누락된 출력 검증을 구분해 주세요.

    [출력]
    재사용·재실행·보류할 task 목록과 이유를 주세요.
    Quality와 publish 전 확인 순서를 제안해 주세요.

    [검증]
    실제 출력의 구간·schema·검증 결과를 task 기록과 맞춰 주세요.
    제한된 가상 실패 흐름에서 downstream이 유효한 입력만 받는지 확인해 주세요.
    ```

**Expected output:** List tasks to reuse, rerun, or hold, with reasons. Propose checks before quality validation and publication.

**What the LLM can get wrong:** The LLM may reuse stale upstream output based only on success status or rerun the whole DAG without need.

**How to validate:** Match actual output intervals, schemas, and checks to task records. Check that downstream tasks receive valid input in a bounded synthetic failure flow.

## Investigate publication after a quality failure {#orchestration-04}

**Situation:** Review a run where publication started after a quality task failed.

**Context to give the LLM:** Quality and publish dependencies and trigger rules: [settings] Upstream success, failed, and skipped states: [synthetic run record] Quality requirements for publication and failure alerts: [policy and samples]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Quality and publish dependencies and trigger rules: [settings]
    Upstream success, failed, and skipped states: [synthetic run record]
    Quality requirements for publication and failure alerts: [policy and samples]

    [Task]
    Review the actual trigger rule for each combination of states.
    Do not treat all_success and all_done as equivalent.
    Separate intended publication conditions from observed execution.

    [Output]
    Return expected and observed publication outcomes by upstream state.
    List missing dependency or setting evidence and minimal change candidates.

    [Checks]
    Compare the actual DAG with trigger-rule documentation for the version in use.
    Check a synthetic publication gate with success, failure, and skipped states.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Quality·publish dependency와 trigger rule: [설정]
    Upstream success·failed·skipped 상태: [가상 실행 기록]
    공개 허용 품질 기준과 실패 알림: [정책·샘플]

    [요청]
    실제 trigger rule을 상태 조합별로 검토해 주세요.
    all_success와 all_done의 결과를 혼동하지 말아 주세요.
    의도한 공개 조건과 관측된 실행을 구분해 주세요.

    [출력]
    Upstream 상태별 publish 기대·관측 결과표를 주세요.
    누락된 dependency·설정 근거와 최소 수정 후보를 적어 주세요.

    [검증]
    실제 DAG와 해당 버전 trigger rule 문서를 대조해 주세요.
    성공·실패·skip 조합으로 가상 publish gate의 동작을 확인해 주세요.
    ```

**Expected output:** Return expected and observed publication outcomes by upstream state. List missing dependency or setting evidence and minimal change candidates.

**What the LLM can get wrong:** The LLM may assume every downstream task is blocked by failure or that skipped always means successful.

**How to validate:** Compare the actual DAG with trigger-rule documentation for the version in use. Check a synthetic publication gate with success, failure, and skipped states.

## Review XCom and worker responsibilities {#orchestration-05}

**Situation:** A DAG passes a large dataset through XCom and transforms it inside a worker.

**Context to give the LLM:** Work and data size by task: [structure and synthetic scale] XCom payload and external storage path format: [non-secret examples] Compute submission, completion checks, and retries: [design]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Work and data size by task: [structure and synthetic scale]
    XCom payload and external storage path format: [non-secret examples]
    Compute submission, completion checks, and retries: [design]

    [Task]
    Review orchestration and compute responsibilities separately.
    Identify candidates for passing small states or paths and checking their validity.
    Mark missing evidence that connects external job success to task success.

    [Output]
    Return input and output contracts across tasks, compute, and storage.
    Provide checks for partial output, retries, and paths for the wrong interval.

    [Checks]
    Check actual payload sizes and how tasks verify external job state.
    Check downstream progress conditions with synthetic missing paths and partial output.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Task별 수행 작업과 데이터 크기: [구조·가상 규모]
    XCom payload와 외부 저장소 경로 형식: [비밀값 없는 예시]
    Compute 제출·완료 확인·retry 흐름: [설계]

    [요청]
    Orchestration과 실제 compute 책임을 분리해 검토해 주세요.
    작은 상태·경로 전달로 바꿀 후보와 유효성 확인을 정리해 주세요.
    외부 job 성공과 task 성공의 연결 근거가 부족하면 표시해 주세요.

    [출력]
    Task·compute·storage 사이의 입력·출력 계약표를 주세요.
    부분 출력·재시도·잘못된 구간 경로의 검증 사례를 주세요.

    [검증]
    Task의 실제 payload 크기와 외부 job 상태 확인 방식을 점검해 주세요.
    가상 누락 경로·부분 출력에서 downstream 진행 조건을 확인해 주세요.
    ```

**Expected output:** Return input and output contracts across tasks, compute, and storage. Provide checks for partial output, retries, and paths for the wrong interval.

**What the LLM can get wrong:** The LLM may assume passing a path solves readiness, interval, and rerun issues by itself.

**How to validate:** Check actual payload sizes and how tasks verify external job state. Check downstream progress conditions with synthetic missing paths and partial output.

## Define repeatable date and time intervals {#orchestration-06}

**Situation:** A rerun for the same past date changes its result because it uses now().

**Context to give the LLM:** Task SQL and use of process_date and data_interval: [synthetic code] Timezone and start and end boundaries: [definitions] Available source intervals and output partitions: [list]

**Example prompt**

=== "English"

    ```text {.prompt}
    [Context]
    Task SQL and use of process_date and data_interval: [synthetic code]
    Timezone and start and end boundaries: [definitions]
    Available source intervals and output partitions: [list]

    [Task]
    Identify inputs tied to run time and inputs tied to explicit intervals.
    Review overlap, gaps, and timezone boundaries between adjacent intervals.
    Separate observed differences from hypotheses about time conditions.

    [Output]
    Return a mapping of interval parameters, input filters, and output partitions.
    Provide expected cases for midnight boundaries and repeated runs of one interval.

    [Checks]
    Check that synthetic boundary-time rows belong to exactly one interval.
    Compare rerun results for fixed inputs with actual parameter interpretation.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Task SQL과 process_date·data_interval 사용: [가상 코드]
    Timezone·시작·종료 경계 정의: [정의]
    Source 가용 구간과 출력 partition: [목록]

    [요청]
    실행 시각에 의존하는 입력과 명시적 구간 입력을 찾아 주세요.
    인접 구간의 중복·누락 및 timezone 변환 경계를 검토해 주세요.
    관측된 차이와 시간 조건에 대한 가설을 분리해 주세요.

    [출력]
    구간 parameter·입력 filter·출력 partition 대응표를 주세요.
    자정 경계와 같은 구간 반복 실행의 기대 사례를 주세요.

    [검증]
    가상 경계 시각의 행이 정확히 한 구간에 포함되는지 확인해 주세요.
    같은 고정 입력의 재실행 결과와 실제 parameter 해석을 대조해 주세요.
    ```

**Expected output:** Return a mapping of interval parameters, input filters, and output partitions. Provide expected cases for midnight boundaries and repeated runs of one interval.

**What the LLM can get wrong:** The LLM may assume matching date strings imply matching timezones and input intervals.

**How to validate:** Check that synthetic boundary-time rows belong to exactly one interval. Compare rerun results for fixed inputs with actual parameter interpretation.
