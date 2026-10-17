---
id: prompts-orchestration
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 데이터 오케스트레이션 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[개념 문서](../data-platform/orchestration.md) · [전체 프롬프트 모음](index.md)

| # | 상황 바로 가기 |
| --- | --- |
| 01 | [Schedule과 입력 준비 조건 분리](#orchestration-01) |
| 02 | [실패 유형별 retry 정책 검토](#orchestration-02) |
| 03 | [실패 task부터 재개할 범위 결정](#orchestration-03) |
| 04 | [품질 실패 후 publish 실행 원인 조사](#orchestration-04) |
| 05 | [XCom과 worker의 역할 경계 검토](#orchestration-05) |
| 06 | [재실행 가능한 날짜·시간 구간 계약](#orchestration-06) |

## Schedule과 입력 준비 조건 분리 {#orchestration-01}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    02시에 실행한 DAG가 아직 도착하지 않은 입력을 읽는다.
    실행 시각과 데이터 준비 조건을 별도로 검토해 주세요.
    일부 파일 도착을 전체 입력 완료로 보는지 확인해 주세요.
    관측된 지연·추정 원인·누락된 준비 근거를 구분해 주세요.
    준비·미준비·확인 불가 상태별 task 진행 판단표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A DAG scheduled at 02:00 tries to read input that has not arrived.
    Review run time and data-readiness conditions separately.
    Check whether partial file arrival is mistaken for complete input.
    Separate observed delay, possible causes, and missing readiness evidence.
    Return a proceed decision table for ready, not ready, and unknown states.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 입력 전체의 준비 완료 기준. DAG 설정과 task 실행 기록을 섞지 말고 각각 출처를 붙인다. Schedule만 늦추면 준비 상태가 보장된다고 하거나 없는 provider 기능을 제안할 수 있다. 일부 파일만 도착한 사례가 downstream 진행으로 처리되면 채택하지 않는다.

## 실패 유형별 retry 정책 검토 {#orchestration-02}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    동일 retry 정책이 network timeout과 SQL syntax error에 적용된다.
    일시·영구 실패 후보와 판단에 필요한 증거를 분리해 주세요.
    반복 실행의 중복 위험을 write 경계별로 검토해 주세요.
    MERGE·overwrite 이름만으로 멱등성을 인정하지 말아 주세요.
    오류별 재시도 후보·수정 선행 조건·확인 근거 표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    One retry policy handles both network timeouts and SQL syntax errors.
    Separate transient and permanent failure candidates and the evidence needed.
    Review duplicate risk at each write boundary during retries.
    Do not infer idempotency from MERGE or overwrite names alone.
    Return a table of retry candidates, fixes needed first, and evidence by error.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 부분 write 여부와 동일 구간 재실행의 최종 효과. DAG 설정과 task 실행 기록을 섞지 말고 각각 출처를 붙인다. 모든 실패에 retry 수를 늘리거나 부분 쓰기의 중복을 놓칠 수 있다. retry 횟수 증가 전에 부분 성공과 중복 효과를 검증한다.

## 실패 task부터 재개할 범위 결정 {#orchestration-03}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Extract와 Spark는 성공했고 dbt가 실패한 실행을 복구하려 한다.
    기존 upstream 결과가 동일 구간에서 유효한지 먼저 평가해 주세요.
    실패 지점 재개와 더 넓은 재실행이 필요한 조건을 나눠 주세요.
    확인된 상태·가정·누락된 출력 검증을 구분해 주세요.
    재사용·재실행·보류할 task 목록과 이유를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Extract and Spark succeeded, but dbt failed. Review how to resume the run.
    First assess whether upstream results remain valid for the same interval.
    Separate conditions for resuming at failure from those requiring a broader rerun.
    Separate known state, assumptions, and missing output checks.
    List tasks to reuse, rerun, or hold, with reasons.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 재사용할 upstream 출력의 구간·버전·검증 상태. DAG 설정과 task 실행 기록을 섞지 말고 각각 출처를 붙인다. 성공 표시만 보고 낡은 upstream 결과를 재사용하거나 전체 DAG를 불필요하게 재실행할 수 있다. 성공 표시가 있어도 수정된 downstream 계약과 맞지 않으면 재사용하지 않는다.

## 품질 실패 후 publish 실행 원인 조사 {#orchestration-04}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    Quality task가 실패했는데 publish task가 실행된 상태를 검토 중이야.
    실제 trigger rule을 상태 조합별로 검토해 주세요.
    all_success와 all_done의 결과를 혼동하지 말아 주세요.
    의도한 공개 조건과 관측된 실행을 구분해 주세요.
    Upstream 상태별 publish 기대·관측 결과표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review a run where publication started after a quality task failed.
    Review the actual trigger rule for each combination of states.
    Do not treat all_success and all_done as equivalent.
    Separate intended publication conditions from observed execution.
    Return expected and observed publication outcomes by upstream state.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 trigger rule과 success·failed·skipped 조합. DAG 설정과 task 실행 기록을 섞지 말고 각각 출처를 붙인다. 모든 downstream은 실패에 자동 차단된다고 설명하거나 skip을 성공으로 단정할 수 있다. 품질 실패뿐 아니라 skip 경로에서도 잘못 공개되지 않아야 한다.

## XCom과 worker의 역할 경계 검토 {#orchestration-05}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    DAG task가 대량 데이터를 XCom으로 전달하고 worker에서 변환한다.
    Orchestration과 실제 compute 책임을 분리해 검토해 주세요.
    작은 상태·경로 전달로 바꿀 후보와 유효성 확인을 정리해 주세요.
    외부 job 성공과 task 성공의 연결 근거가 부족하면 표시해 주세요.
    Task·compute·storage 사이의 입력·출력 계약표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A DAG passes a large dataset through XCom and transforms it inside a worker.
    Review orchestration and compute responsibilities separately.
    Identify candidates for passing small states or paths and checking their validity.
    Mark missing evidence that connects external job success to task success.
    Return input and output contracts across tasks, compute, and storage.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제 XCom payload 크기와 외부 job 완료 확인 방식. DAG 설정과 task 실행 기록을 섞지 말고 각각 출처를 붙인다. 데이터 대신 경로만 넘기면 출력 준비·구간·재실행 문제가 모두 해결된다고 볼 수 있다. 경로만 바꾼 뒤에도 부분 출력·잘못된 구간을 거부하는지 확인한다.

## 재실행 가능한 날짜·시간 구간 계약 {#orchestration-06}

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    같은 과거 날짜의 DAG를 재실행했는데 now() 때문에 결과가 달라진다.
    실행 시각에 의존하는 입력과 명시적 구간 입력을 찾아 주세요.
    인접 구간의 중복·누락 및 timezone 변환 경계를 검토해 주세요.
    관측된 차이와 시간 조건에 대한 가설을 분리해 주세요.
    구간 parameter·입력 filter·출력 partition 대응표를 주세요.
    검토만 하고 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A rerun for the same past date changes its result because it uses now().
    Identify inputs tied to run time and inputs tied to explicit intervals.
    Review overlap, gaps, and timezone boundaries between adjacent intervals.
    Separate observed differences from hypotheses about time conditions.
    Return a mapping of interval parameters, input filters, and output partitions.
    Review only; do not apply changes.
    ```

**핵심 사항:** 판단 전에 확인할 근거: data interval의 시작·종료 포함 규칙과 timezone. DAG 설정과 task 실행 기록을 섞지 말고 각각 출처를 붙인다. 날짜 문자열만 같으면 timezone과 실제 입력 범위도 같다고 가정할 수 있다. 같은 날짜 문자열이 아닌 같은 입력 집합으로 결과가 재현되어야 한다.
