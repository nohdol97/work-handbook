---
id: prompts-event-architecture
status: overview
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids: []
---

# Event data architecture practical prompts

Copy these examples with the relevant SQL, settings, logs, or proposed changes. Use sanitized material and check suggestions against real evidence and permissions. An example does not authorize system changes or data deletion. These are not measured usage or model-performance results.

[All prompts](index.md) · [Concepts and sources](../data-platform/event-architecture.md)

## Quick selection

| Purpose | Jump to |
| --- | --- |
| Review event units and meaning | [01](#event-architecture-01) |
| Review compatibility with historical schemas | [02](#event-architecture-02) |
| Check deduplication retention against replay | [03](#event-architecture-03) |
| Investigate serving and lakehouse differences | [04](#event-architecture-04) |
| Find confusion between event and ingestion time | [05](#event-architecture-05) |
| Represent a correction as a new event | [06](#event-architecture-06) |

## Review event units and meaning {#event-architecture-01}

Example prompt:

=== "English"

    ```text {.prompt}
    Latency fields from different producers feed one dashboard.
    Find fields with matching types but different units or measurement start and end points.
    Review gaps in required and optional fields, meaning, ownership, and version-change rules.
    Return ambiguities and a revised contract draft with synthetic examples.
    ```

=== "한국어"

    ```text {.prompt}
    서로 다른 producer의 latency 필드가 같은 대시보드에 합쳐지는 상황이야.
    타입이 같아도 단위나 측정 시작·종료가 다른 필드를 찾아 줘.
    필수·선택 필드, 의미, 소유권, 버전 변경 규칙의 누락을 검토해 줘.
    모호성 목록과 합성 예시를 포함한 계약 보완 초안을 작성해 줘.
    ```

**Key point:** Evidence to check first: latency start, end, and unit definitions for each producer. Keep stable event identifiers across samples while replacing sensitive values. The LLM may equate schema validity with semantic agreement or infer units from a name. Do not combine identical numbers or types into one metric when their measurement intervals differ.

## Review compatibility with historical schemas {#event-architecture-02}

Example prompt:

=== "English"

    ```text {.prompt}
    A new consumer must read historical and current events.
    Separate a new reader reading old data from an old reader reading new data.
    Distinguish previous-version and transitive checks, and review semantic changes separately.
    Return a version-pair test matrix and changes that remain unverified.
    ```

=== "한국어"

    ```text {.prompt}
    새 consumer가 최신 이벤트뿐 아니라 과거 이력도 읽어야 하는 변경이다.
    새 reader가 옛 데이터를 읽는 경우와 옛 reader가 새 데이터를 읽는 경우를 나눠 줘.
    직전 버전 검사와 transitive 검사를 구분하고 의미 변경도 별도로 찾아 줘.
    버전 조합별 검증 행렬과 아직 확인하지 못한 변경을 작성해 줘.
    ```

**Key point:** Evidence to check first: retained schema versions and the replay range. Keep stable event identifiers across samples while replacing sensitive values. The LLM may reverse backward and forward compatibility or apply one format's rules to another. Do not label a latest-two-version check as compatibility with all history.

## Check deduplication retention against replay {#event-architecture-03}

Example prompt:

=== "English"

    ```text {.prompt}
    This request reprocesses a period longer than the deduplication state lifetime.
    Analyze duplicates while state exists and duplicates arriving after it expires.
    Review possible event-ID collisions or regeneration and mark the exactly-once boundary.
    Return a timeline of duplicate risks and required sink properties.
    ```

=== "한국어"

    ```text {.prompt}
    중복 제거 상태보다 긴 기간을 다시 처리하려는 요청이다.
    상태가 남아 있는 중복과 만료 후 다시 들어오는 중복을 나눠 분석해 줘.
    Event ID 충돌과 재생성 가능성도 검토하고 exactly-once 범위를 표시해 줘.
    시간축별 중복 위험과 sink에 필요한 조건을 표로 작성해 줘.
    ```

**Key point:** Evidence to check first: deduplication expiry rules and the oldest replay point. Keep stable event identifiers across samples while replacing sensitive values. The LLM may claim deduplication removes duplicates even beyond its retention period. Require a counterexample with a duplicate arriving after state expiry.

## Investigate serving and lakehouse differences {#event-architecture-04}

Example prompt:

=== "English"

    ```text {.prompt}
    Two paths receiving the same events show different daily counts.
    Review the current design and separate definition, delay, duplicate, and loss hypotheses.
    First check whether the comparison uses the same time basis and event set.
    Return evidence, falsification checks, and ordered read-only checks for each hypothesis.
    ```

=== "한국어"

    ```text {.prompt}
    동일 이벤트를 받는 두 경로의 일별 건수가 다른 상황이야.
    정의 차이, 지연, 중복, 유실 가설을 분리해서 현재 설계를 검토해 줘.
    같은 시간 기준과 동일한 event 집합으로 비교할 수 있는지 먼저 확인해 줘.
    가설별 근거·반증 조건·읽기 전용 확인 순서를 작성해 줘.
    ```

**Key point:** Evidence to check first: a matching event set and time basis across both paths. Keep stable event identifiers across samples while replacing sensitive values. The LLM may infer loss from count differences or assume both paths must match immediately. Do not classify differences in a still-lagging interval as loss.

## Find confusion between event and ingestion time {#event-architecture-05}

Example prompt:

=== "English"

    ```text {.prompt}
    Late events enter a different day's metrics.
    Explain the current aggregate by separating occurrence, producer recording, and platform arrival time.
    Identify the time basis that matches the metric and missing time-zone or delay details.
    Return each synthetic event's current and required reporting date in a table.
    ```

=== "한국어"

    ```text {.prompt}
    늦게 도착한 이벤트가 다른 날짜의 지표에 포함되는 상황이야.
    사건 발생·생성 기록·플랫폼 도착 시각을 구분해 현재 집계를 설명해 줘.
    의도한 지표 정의에 맞는 기준과 누락된 시간대·지연 정보를 찾아 줘.
    합성 이벤트별 현재 포함 날짜와 요구되는 포함 날짜를 표로 작성해 줘.
    ```

**Key point:** Evidence to check first: the business reporting date and timezone definition. Keep stable event identifiers across samples while replacing sensitive values. The LLM may treat producer timestamps as occurrence time or attribute every time gap to network delay. Have the owner confirm expected dates at date boundaries, with applicable daylight-saving rules and late arrivals.

## Represent a correction as a new event {#event-architecture-06}

Example prompt:

=== "English"

    ```text {.prompt}
    This design compares overwriting an event with adding a correction event.
    Separate the original fact from the correction and review ambiguities in the current contract.
    Explain duplicate, reordering, and replay effects on each consumer when using a new event.
    Return contract questions, a synthetic event sequence, and expected results for each consumer.
    ```

=== "한국어"

    ```text {.prompt}
    기존 이벤트 값을 덮어쓸지 정정 이벤트를 추가할지 논의하는 설계다.
    과거 사실과 정정 사실의 의미를 나누고 현재 계약의 모호성을 검토해 줘.
    새 이벤트 방식에서 중복·순서 변경·replay가 각 consumer에 미치는 영향을 설명해 줘.
    필요한 계약 질문과 합성 이벤트 흐름, consumer별 기대 결과를 작성해 줘.
    ```

**Key point:** Evidence to check first: the key linking a correction to its event and correction semantics for each consumer. Keep stable event identifiers across samples while replacing sensitive values. The LLM may assume immutable events automatically define corrections and consistent final state. Require both the original fact and the corrected query meaning to remain explainable.
