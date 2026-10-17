---
id: prompts-event-architecture
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# 이벤트 데이터 아키텍처 실무 프롬프트

실제 SQL·설정·로그·변경안을 붙여 바로 요청할 수 있는 예시다. 비식별 자료만 사용하고, 제안은 실제 근거와 권한에 맞춰 검토한다. 이 예시만으로 시스템 변경이나 데이터 삭제를 승인하지 않는다. 사용 빈도나 모델 성능을 측정한 사례는 아니다.

[전체 프롬프트 모음](index.md) · [개념과 출처](../data-platform/event-architecture.md)

## 빠르게 고르기

| 목적 | 바로 가기 |
| --- | --- |
| 단위와 의미가 명확한 이벤트 계약 검토 | [01](#event-architecture-01) |
| 전체 과거 schema와의 호환성 검토 | [02](#event-architecture-02) |
| Deduplication 보존 기간과 replay 범위 점검 | [03](#event-architecture-03) |
| Serving과 Lakehouse 결과 차이 조사 | [04](#event-architecture-04) |
| 이벤트 시각과 수집 시각의 혼동 찾기 | [05](#event-architecture-05) |
| 수정 사실을 새로운 이벤트로 표현하기 | [06](#event-architecture-06) |

## 단위와 의미가 명확한 이벤트 계약 검토 {#event-architecture-01}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    서로 다른 producer의 latency 필드가 같은 대시보드에 합쳐지는 상황이야.
    타입이 같아도 단위나 측정 시작·종료가 다른 필드를 찾아 줘.
    필수·선택 필드, 의미, 소유권, 버전 변경 규칙의 누락을 검토해 줘.
    모호성 목록과 합성 예시를 포함한 계약 보완 초안을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Latency fields from different producers feed one dashboard.
    Find fields with matching types but different units or measurement start and end points.
    Review gaps in required and optional fields, meaning, ownership, and version-change rules.
    Return ambiguities and a revised contract draft with synthetic examples.
    ```

**핵심 사항:** 판단 전에 확인할 근거: producer별 latency 측정 시작·종료와 단위 정의. 이벤트 표본은 같은 식별자를 유지하고 민감한 값만 치환한다. Schema 검사를 통과하면 의미도 같다고 하거나 단위를 이름만 보고 추정할 수 있다. 같은 숫자·타입이라도 측정 구간이 다르면 같은 metric으로 합치지 않는다.

## 전체 과거 schema와의 호환성 검토 {#event-architecture-02}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    새 consumer가 최신 이벤트뿐 아니라 과거 이력도 읽어야 하는 변경이다.
    새 reader가 옛 데이터를 읽는 경우와 옛 reader가 새 데이터를 읽는 경우를 나눠 줘.
    직전 버전 검사와 transitive 검사를 구분하고 의미 변경도 별도로 찾아 줘.
    버전 조합별 검증 행렬과 아직 확인하지 못한 변경을 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    A new consumer must read historical and current events.
    Separate a new reader reading old data from an old reader reading new data.
    Distinguish previous-version and transitive checks, and review semantic changes separately.
    Return a version-pair test matrix and changes that remain unverified.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 실제로 남아 있는 schema 버전과 replay 범위. 이벤트 표본은 같은 식별자를 유지하고 민감한 값만 치환한다. Backward와 forward를 뒤바꾸거나 특정 포맷의 허용 변경을 다른 포맷에도 적용할 수 있다. 최신 두 버전만 통과한 결과를 전체 이력 호환으로 표시하지 않는다.

## Deduplication 보존 기간과 replay 범위 점검 {#event-architecture-03}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    중복 제거 상태보다 긴 기간을 다시 처리하려는 요청이다.
    상태가 남아 있는 중복과 만료 후 다시 들어오는 중복을 나눠 분석해 줘.
    Event ID 충돌과 재생성 가능성도 검토하고 exactly-once 범위를 표시해 줘.
    시간축별 중복 위험과 sink에 필요한 조건을 표로 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    This request reprocesses a period longer than the deduplication state lifetime.
    Analyze duplicates while state exists and duplicates arriving after it expires.
    Review possible event-ID collisions or regeneration and mark the exactly-once boundary.
    Return a timeline of duplicate risks and required sink properties.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 중복 제거 상태의 만료 규칙과 가장 오래된 replay 시점. 이벤트 표본은 같은 식별자를 유지하고 민감한 값만 치환한다. Deduplication을 켜면 보존 기간 밖의 replay까지 중복이 사라진다고 할 수 있다. 상태 만료 뒤 중복이 다시 들어오는 반례가 포함되어야 한다.

## Serving과 Lakehouse 결과 차이 조사 {#event-architecture-04}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    동일 이벤트를 받는 두 경로의 일별 건수가 다른 상황이야.
    정의 차이, 지연, 중복, 유실 가설을 분리해서 현재 설계를 검토해 줘.
    같은 시간 기준과 동일한 event 집합으로 비교할 수 있는지 먼저 확인해 줘.
    가설별 근거·반증 조건·읽기 전용 확인 순서를 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Two paths receiving the same events show different daily counts.
    Review the current design and separate definition, delay, duplicate, and loss hypotheses.
    First check whether the comparison uses the same time basis and event set.
    Return evidence, falsification checks, and ordered read-only checks for each hypothesis.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 양 경로에서 동일하게 비교할 event 집합과 시각 기준. 이벤트 표본은 같은 식별자를 유지하고 민감한 값만 치환한다. 건수 차이만으로 유실을 확정하거나 두 경로가 즉시 일치해야 한다고 가정할 수 있다. lag가 남은 구간의 차이를 곧바로 유실로 판정하지 않는다.

## 이벤트 시각과 수집 시각의 혼동 찾기 {#event-architecture-05}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    늦게 도착한 이벤트가 다른 날짜의 지표에 포함되는 상황이야.
    사건 발생·생성 기록·플랫폼 도착 시각을 구분해 현재 집계를 설명해 줘.
    의도한 지표 정의에 맞는 기준과 누락된 시간대·지연 정보를 찾아 줘.
    합성 이벤트별 현재 포함 날짜와 요구되는 포함 날짜를 표로 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    Late events enter a different day's metrics.
    Explain the current aggregate by separating occurrence, producer recording, and platform arrival time.
    Identify the time basis that matches the metric and missing time-zone or delay details.
    Return each synthetic event's current and required reporting date in a table.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 업무상 집계 날짜와 timezone 정의. 이벤트 표본은 같은 식별자를 유지하고 민감한 값만 치환한다. Producer timestamp를 검증 없이 실제 발생 시각으로 보거나 시각 차이를 네트워크 지연으로만 볼 수 있다. 날짜 경계·서머타임 적용 여부·늦은 도착의 기대 날짜를 담당자가 확인한다.

## 수정 사실을 새로운 이벤트로 표현하기 {#event-architecture-06}

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    기존 이벤트 값을 덮어쓸지 정정 이벤트를 추가할지 논의하는 설계다.
    과거 사실과 정정 사실의 의미를 나누고 현재 계약의 모호성을 검토해 줘.
    새 이벤트 방식에서 중복·순서 변경·replay가 각 consumer에 미치는 영향을 설명해 줘.
    필요한 계약 질문과 합성 이벤트 흐름, consumer별 기대 결과를 작성해 줘.
    ```

=== "English"

    ```text {.prompt}
    This design compares overwriting an event with adding a correction event.
    Separate the original fact from the correction and review ambiguities in the current contract.
    Explain duplicate, reordering, and replay effects on each consumer when using a new event.
    Return contract questions, a synthetic event sequence, and expected results for each consumer.
    ```

**핵심 사항:** 판단 전에 확인할 근거: 정정 대상 event를 연결하는 키와 consumer별 정정 의미. 이벤트 표본은 같은 식별자를 유지하고 민감한 값만 치환한다. Immutable event만 쓰면 정정의 의미와 최종 상태가 자동으로 일치한다고 할 수 있다. 원 이벤트의 의미와 정정 후 조회 의미를 모두 복원할 수 있어야 한다.
