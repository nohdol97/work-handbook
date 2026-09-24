---
id: prompts-cdc-debezium
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# CDC·Debezium 실무 프롬프트

기존 개념을 응용해 작성한 가상의 재사용 예시 6개다. 실제 업무 빈도나 실행 성능을 측정한 결과가 아니며, 새 학습 과정이나 실제 운영 경험으로 기록하지 않는다. [대괄호]를 비밀값 없는 맥락과 가상 데이터로 채운다. 모델의 제안은 검증할 작업 초안이다. 실제 production 실행 권한을 부여하지 않는다.

[개념 문서](../data-platform/cdc-debezium.md) · [전체 프롬프트 모음](index.md)

| # | 상황 바로 가기 |
| --- | --- |
| 01 | [초기 snapshot 중단 후 재개 판단](#cdc-debezium-01) |
| 02 | [삭제 이벤트와 tombstone 처리 계약](#cdc-debezium-02) |
| 03 | [스키마 변경의 downstream 영향 검토](#cdc-debezium-03) |
| 04 | [여러 테이블 transaction의 관측 범위](#cdc-debezium-04) |
| 05 | [Polling에서 CDC로 바꿀 때 삭제 누락 점검](#cdc-debezium-05) |
| 06 | [History와 current state 대사 설계](#cdc-debezium-06) |

## 초기 snapshot 중단 후 재개 판단 {#cdc-debezium-01}

**상황:** 초기 적재 중 connector가 멈춰 snapshot을 다시 시작할지 판단한다.

**LLM에 제공할 맥락:** Connector·DB 버전과 snapshot mode: [버전·설정] Snapshot 완료 기록과 저장 offset: [익명화한 상태] Replication slot·필요 WAL 가용성: [관찰 기록]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Connector·DB 버전과 snapshot mode: [버전·설정]
    Snapshot 완료 기록과 저장 offset: [익명화한 상태]
    Replication slot·필요 WAL 가용성: [관찰 기록]

    [요청]
    관찰한 완료 상태와 추정한 복구 가능성을 구분해 주세요.
    Offset과 WAL 근거별로 재개·재초기화 후보를 비교해 주세요.
    확인되지 않은 snapshot 동작은 버전별 확인 항목으로 남겨 주세요.

    [출력]
    조건별 판단표와 부족한 증거를 작성해 주세요.
    Current state와 중간 변경 이력의 복구 범위를 따로 적어 주세요.

    [검증]
    공식 connector 문서와 실제 offset·slot 상태를 대조해 주세요.
    제한된 복구 검증의 key·삭제·중복 확인 항목만 제안해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Connector and DB versions and snapshot mode: [versions and settings]
    Snapshot completion record and stored offset: [sanitized state]
    Replication slot and required WAL availability: [observations]

    [Task]
    Separate observed completion state from assumed recovery options.
    Compare resume and reinitialization options using offset and WAL evidence.
    List unconfirmed snapshot behavior as version-specific checks.

    [Output]
    Return a decision table and missing evidence for each condition.
    State recovery scope for current state and intermediate history separately.

    [Checks]
    Cross-check connector documentation with actual offset and slot state.
    Propose bounded recovery checks for keys, deletes, and duplicates.
    ```

**기대 결과:** 조건별 판단표와 부족한 증거를 작성해 주세요. Current state와 중간 변경 이력의 복구 범위를 따로 적어 주세요.

**LLM이 틀릴 수 있는 부분:** 재시작이 항상 snapshot을 생략하거나 사라진 이력을 복원한다고 단정할 수 있다.

**검증 방법:** 공식 connector 문서와 실제 offset·slot 상태를 대조해 주세요. 제한된 복구 검증의 key·삭제·중복 확인 항목만 제안해 주세요.

## 삭제 이벤트와 tombstone 처리 계약 {#cdc-debezium-02}

**상황:** 소스에서 삭제한 행이 current-state 조회에 남아 있다.

**LLM에 제공할 맥락:** 가상 DELETE·tombstone 샘플: [key·op·before·after·value] History와 current-state 쓰기 규칙: [규칙] 소비 쿼리와 논리 삭제 필터: [SQL·조건]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 DELETE·tombstone 샘플: [key·op·before·after·value]
    History와 current-state 쓰기 규칙: [규칙]
    소비 쿼리와 논리 삭제 필터: [SQL·조건]

    [요청]
    DB 삭제 사실과 Kafka compaction record를 구분해 주세요.
    Physical·logical delete별 저장 결과와 조회 조건을 검토해 주세요.
    before의 전체 행이 없을 때 필요한 key 근거를 찾아 주세요.

    [출력]
    입력 event별 history·current-state 기대 결과표를 만들어 주세요.
    누락 원인 가설과 각 가설을 반박할 증거를 적어 주세요.

    [검증]
    가상 INSERT→DELETE와 DELETE 재전송 결과를 비교해 주세요.
    실제 event 형식·삭제 정책·소비 필터로 기대 결과를 확인해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Synthetic DELETE and tombstone samples: [key, op, before, after, value]
    History and current-state write rules: [rules]
    Consumer query and logical-delete filter: [SQL and conditions]

    [Task]
    Separate a database delete from a Kafka compaction record.
    Review stored results and query conditions for physical and logical deletes.
    Identify required key evidence when before lacks the full old row.

    [Output]
    Return expected history and current-state results for each input event.
    List missing-delete hypotheses and evidence that could reject each one.

    [Checks]
    Compare synthetic INSERT→DELETE and repeated DELETE results.
    Check expected results against event format, delete policy, and consumer filters.
    ```

**기대 결과:** 입력 event별 history·current-state 기대 결과표를 만들어 주세요. 누락 원인 가설과 각 가설을 반박할 증거를 적어 주세요.

**LLM이 틀릴 수 있는 부분:** Tombstone을 업무 삭제와 동일시하거나 논리 삭제 행을 기본 조회에 포함할 수 있다.

**검증 방법:** 가상 INSERT→DELETE와 DELETE 재전송 결과를 비교해 주세요. 실제 event 형식·삭제 정책·소비 필터로 기대 결과를 확인해 주세요.

## 스키마 변경의 downstream 영향 검토 {#cdc-debezium-03}

**상황:** 원본 column을 rename하기 전에 CDC부터 BI까지 영향을 확인한다.

**LLM에 제공할 맥락:** 변경 전후 schema와 변경 목적: [가상 정의] Kafka·처리 engine·Iceberg·dbt·BI 의존성: [목록] Connector 버전과 schema 감지·배포 절차: [설정]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    변경 전후 schema와 변경 목적: [가상 정의]
    Kafka·처리 engine·Iceberg·dbt·BI 의존성: [목록]
    Connector 버전과 schema 감지·배포 절차: [설정]

    [요청]
    Rename·type·nullable 변경을 각 소비자의 기대 schema와 비교해 주세요.
    CDC가 DDL event를 모두 보낸다고 가정하지 말아 주세요.
    확인된 영향과 호환성 가설, 누락된 소비자를 구분해 주세요.

    [출력]
    구성 요소별 실패 조건·확인 담당·검증 근거 표를 주세요.
    변경 전후 샘플 계약과 단계별 검토 순서를 제안해 주세요.

    [검증]
    실제 schema 비교와 소비 SQL·설정으로 영향 경로를 확인해 주세요.
    가상 구·신 event의 각 단계 수용·거부 조건을 검증해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Before and after schemas and purpose: [synthetic definitions]
    Kafka, compute, Iceberg, dbt, and BI dependencies: [list]
    Connector version and schema detection and rollout process: [settings]

    [Task]
    Compare rename, type, and nullability changes with consumer expectations.
    Do not assume CDC emits every DDL event.
    Separate confirmed impact, compatibility assumptions, and missing consumers.

    [Output]
    Return a table of failure conditions, check owners, and evidence by component.
    Propose sample contracts and an ordered review plan for both schemas.

    [Checks]
    Check the impact path against actual schemas, consumer SQL, and settings.
    Check acceptance and rejection conditions for synthetic old and new events at each stage.
    ```

**기대 결과:** 구성 요소별 실패 조건·확인 담당·검증 근거 표를 주세요. 변경 전후 샘플 계약과 단계별 검토 순서를 제안해 주세요.

**LLM이 틀릴 수 있는 부분:** Nullable 추가를 무조건 안전하다고 보거나 rename을 자동 전파한다고 가정할 수 있다.

**검증 방법:** 실제 schema 비교와 소비 SQL·설정으로 영향 경로를 확인해 주세요. 가상 구·신 event의 각 단계 수용·거부 조건을 검증해 주세요.

## 여러 테이블 transaction의 관측 범위 {#cdc-debezium-04}

**상황:** 주문과 결제가 같은 DB transaction에서 바뀌지만 소비자가 다른 시점에 본다.

**LLM에 제공할 맥락:** 가상 table별 event·key·partition 순서: [샘플] Source·transaction metadata와 활성화 설정: [필드·설정] 소비자의 일관성 요구와 관측 시각: [요구·기록]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 table별 event·key·partition 순서: [샘플]
    Source·transaction metadata와 활성화 설정: [필드·설정]
    소비자의 일관성 요구와 관측 시각: [요구·기록]

    [요청]
    DB transaction 경계와 Kafka partition 순서 범위를 나눠 주세요.
    같은 key의 순서와 테이블 사이 도착 차이를 따로 분석해 주세요.
    Metadata 지원·설정이 확인되지 않은 부분은 가정으로 표시해 주세요.

    [출력]
    관측 가능한 순서와 보장되지 않는 순서의 표를 주세요.
    소비 시점 불일치 가설과 필요한 추가 event 근거를 적어 주세요.

    [검증]
    가상 테이블별 지연을 바꿔 읽는 순서의 차이를 확인해 주세요.
    실제 partition mapping과 지원되는 transaction metadata를 대조해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Synthetic events, keys, and partition order by table: [samples]
    Source and transaction metadata and enablement: [fields and settings]
    Consumer consistency needs and observation times: [requirements and records]

    [Task]
    Separate DB transaction boundaries from Kafka partition ordering scope.
    Analyze same-key order and cross-table arrival differences separately.
    Mark unverified metadata support and settings as assumptions.

    [Output]
    Return a table of observable order and order that is not guaranteed.
    List timing-mismatch hypotheses and additional event evidence needed.

    [Checks]
    Check reading-order differences with synthetic delays for each table.
    Cross-check actual partition mapping and supported transaction metadata.
    ```

**기대 결과:** 관측 가능한 순서와 보장되지 않는 순서의 표를 주세요. 소비 시점 불일치 가설과 필요한 추가 event 근거를 적어 주세요.

**LLM이 틀릴 수 있는 부분:** DB의 원자성이 downstream 전체의 동시 관측을 보장한다고 오해할 수 있다.

**검증 방법:** 가상 테이블별 지연을 바꿔 읽는 순서의 차이를 확인해 주세요. 실제 partition mapping과 지원되는 transaction metadata를 대조해 주세요.

## Polling에서 CDC로 바꿀 때 삭제 누락 점검 {#cdc-debezium-05}

**상황:** updated_at polling으로 채운 대상 테이블에 삭제된 행이 남아 수집 방식의 한계를 정리한다.

**LLM에 제공할 맥락:** Polling SQL·주기·저장 시점: [설정] 가상 INSERT·UPDATE·DELETE 타임라인: [샘플] 필요한 현재 상태·이력·지연 조건: [요구]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    Polling SQL·주기·저장 시점: [설정]
    가상 INSERT·UPDATE·DELETE 타임라인: [샘플]
    필요한 현재 상태·이력·지연 조건: [요구]

    [요청]
    각 변경을 polling query가 관측할 수 있는지 표시해 주세요.
    CDC 후보의 snapshot·offset·로그 보존 책임을 함께 검토해 주세요.
    설계 변경 전에 관측 사실·가정·추가 요구를 분리해 주세요.

    [출력]
    Polling과 로그 기반 CDC의 요구 충족 비교표를 주세요.
    삭제·순서·반복 쿼리 부하를 확인할 작은 사례를 제안해 주세요.

    [검증]
    삭제 전후 query 결과를 가상 샘플로 비교해 주세요.
    CDC 설정·로그 가용성과 실제 필요한 이력 범위를 확인해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Polling SQL, interval, and stored time: [settings]
    Synthetic INSERT, UPDATE, and DELETE timeline: [sample]
    Required current state, history, and latency: [requirements]

    [Task]
    Mark whether the polling query can observe each change.
    Review snapshot, offset, and log-retention duties for the CDC option.
    Separate observations, assumptions, and missing requirements before a redesign.

    [Output]
    Return a requirements comparison for polling and log-based CDC.
    Propose small cases to check deletes, order, and repeated-query load.

    [Checks]
    Compare query results before and after a delete using synthetic rows.
    Check CDC settings, log availability, and the required history scope.
    ```

**기대 결과:** Polling과 로그 기반 CDC의 요구 충족 비교표를 주세요. 삭제·순서·반복 쿼리 부하를 확인할 작은 사례를 제안해 주세요.

**LLM이 틀릴 수 있는 부분:** Polling 간격을 줄이면 삭제 감지와 모든 중간 이력 문제가 해결된다고 볼 수 있다.

**검증 방법:** 삭제 전후 query 결과를 가상 샘플로 비교해 주세요. CDC 설정·로그 가용성과 실제 필요한 이력 범위를 확인해 주세요.

## History와 current state 대사 설계 {#cdc-debezium-06}

**상황:** 동일 수집 흐름에서 이력 테이블과 현재 상태 테이블의 검증 기준이 필요하다.

**LLM에 제공할 맥락:** 가상 key별 변경 이력과 source position: [샘플] History 중복 정책과 current-state 삭제 정책: [정의] Source와 대상의 비교 기준 시점: [기준·관측 상태]

**예시 프롬프트**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 key별 변경 이력과 source position: [샘플]
    History 중복 정책과 current-state 삭제 정책: [정의]
    Source와 대상의 비교 기준 시점: [기준·관측 상태]

    [요청]
    이력 행 수와 현재 존재하는 key 수를 같은 기준으로 보지 말아 주세요.
    동일 source 범위의 순서·중복·삭제 규칙으로 기대 상태를 구해 주세요.
    동기화 지연과 실제 불일치 가설을 구분해 주세요.

    [출력]
    Key별 최신 상태·삭제 여부·이력 보존 확인표를 주세요.
    대사 SQL 의사 코드와 비교할 수 없는 구간을 적어 주세요.

    [검증]
    가상 생성·수정·삭제·중복 key의 기대 결과를 손으로 대조해 주세요.
    동일 비교 시점과 삭제 정책이 적용됐는지 실제 상태로 확인해 주세요.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Synthetic per-key history and source positions: [samples]
    History duplicate policy and current-state delete policy: [definitions]
    Source and target comparison point: [cutoff and observed state]

    [Task]
    Do not treat history row count and current key count as the same measure.
    Derive expected state from order, duplicate, and delete rules within one source scope.
    Separate synchronization delay from true mismatch hypotheses.

    [Output]
    Return per-key checks for latest state, deletion, and retained history.
    Provide reconciliation pseudocode and intervals that cannot be compared.

    [Checks]
    Manually check expected results for synthetic create, update, delete, and duplicate cases.
    Use actual state to verify the same comparison point and delete policy.
    ```

**기대 결과:** Key별 최신 상태·삭제 여부·이력 보존 확인표를 주세요. 대사 SQL 의사 코드와 비교할 수 없는 구간을 적어 주세요.

**LLM이 틀릴 수 있는 부분:** History 전체 건수를 source 현재 행 수와 비교하거나 source 간 position을 정렬할 수 있다.

**검증 방법:** 가상 생성·수정·삭제·중복 key의 기대 결과를 손으로 대조해 주세요. 동일 비교 시점과 삭제 정책이 적용됐는지 실제 상태로 확인해 주세요.
