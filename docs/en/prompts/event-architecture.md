---
id: prompts-event-architecture
status: overview
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids: []
---

# Event data architecture practical prompts

Page type: Reference. These six authored, hypothetical examples apply the [existing study material](../data-platform/event-architecture.md). They do not claim production experience, measured usage frequency, or model results. The examples were not run.

Choose a case and replace bracketed inputs with sanitized information. Each prompt has 한국어 and English tabs for language selection and copying. Treat LLM output as a hypothesis. Check actual settings, logs, official docs, and bounded tests. This page does not authorize production actions or permission changes.

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

- **Situation:** In this hypothetical case, latency fields from different producers feed one dashboard.
- **Context to give the LLM:** Contract draft: [fields, types, units, required fields, meaning]; Usage: [measurement interval by producer, consumer aggregates, owner roles].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Contract draft: [fields, types, units, required fields, meaning]
    Usage: [measurement interval by producer, consumer aggregates, owner roles]

    [Task]
    Find fields with matching types but different units or measurement start and end points.
    Review gaps in required and optional fields, meaning, ownership, and version-change rules.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return ambiguities and a revised contract draft with synthetic examples.

    [Checks]
    List checks for unit conversion and consumer aggregates using synthetic producer inputs.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    계약 초안: [필드·타입·단위·필수 여부·의미]
    사용 맥락: [producer별 측정 구간·consumer 집계·소유자 역할]

    [요청]
    타입이 같아도 단위나 측정 시작·종료가 다른 필드를 찾아 줘.
    필수·선택 필드, 의미, 소유권, 버전 변경 규칙의 누락을 검토해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    모호성 목록과 합성 예시를 포함한 계약 보완 초안을 작성해 줘.

    [검증]
    Producer별 합성 입력의 단위 변환과 consumer 집계 결과를 확인할 항목을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Ambiguities and a revised contract draft with synthetic examples.
- **What the LLM can get wrong:** The LLM may equate schema validity with semantic agreement or infer units from a name.
- **How to validate:** List checks for unit conversion and consumer aggregates using synthetic producer inputs.

## Review compatibility with historical schemas {#event-architecture-02}

- **Situation:** In this hypothetical change, a new consumer must read historical and current events.
- **Context to give the LLM:** Schema history: [format, changes by version, field defaults]; Compatibility needs: [registry settings, reader/writer versions, replay range].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Schema history: [format, changes by version, field defaults]
    Compatibility needs: [registry settings, reader/writer versions, replay range]

    [Task]
    Separate a new reader reading old data from an old reader reading new data.
    Distinguish previous-version and transitive checks, and review semantic changes separately.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a version-pair test matrix and changes that remain unverified.

    [Checks]
    Compare official rules for the actual format and settings with synthetic serialization and deserialization tests.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    Schema 이력: [포맷·버전별 변경·필드 기본값]
    호환성 요구: [registry 설정·reader/writer 버전·replay 범위]

    [요청]
    새 reader가 옛 데이터를 읽는 경우와 옛 reader가 새 데이터를 읽는 경우를 나눠 줘.
    직전 버전 검사와 transitive 검사를 구분하고 의미 변경도 별도로 찾아 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    버전 조합별 검증 행렬과 아직 확인하지 못한 변경을 작성해 줘.

    [검증]
    실제 포맷·설정의 공식 규칙과 합성 payload의 직렬화·역직렬화 결과를 대조해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A version-pair test matrix and changes that remain unverified.
- **What the LLM can get wrong:** The LLM may reverse backward and forward compatibility or apply one format's rules to another.
- **How to validate:** Compare official rules for the actual format and settings with synthetic serialization and deserialization tests.

## Check deduplication retention against replay {#event-architecture-03}

- **Situation:** This hypothetical request reprocesses a period longer than the deduplication state lifetime.
- **Context to give the LLM:** Identity and retention: [event-ID rules, state retention, log retention]; Processing scope: [replay range, retry path, sink idempotency].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Identity and retention: [event-ID rules, state retention, log retention]
    Processing scope: [replay range, retry path, sink idempotency]

    [Task]
    Analyze duplicates while state exists and duplicates arriving after it expires.
    Review possible event-ID collisions or regeneration and mark the exactly-once boundary.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return a timeline of duplicate risks and required sink properties.

    [Checks]
    Plan repeated processing of one synthetic event before and after state expiry and compare final effects.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    식별과 보존: [event ID 생성 규칙·상태 보존 기간·로그 보존]
    처리 범위: [replay 기간·재시도 경로·sink 멱등성]

    [요청]
    상태가 남아 있는 중복과 만료 후 다시 들어오는 중복을 나눠 분석해 줘.
    Event ID 충돌과 재생성 가능성도 검토하고 exactly-once 범위를 표시해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    시간축별 중복 위험과 sink에 필요한 조건을 표로 작성해 줘.

    [검증]
    상태 만료 전·후 같은 합성 이벤트를 재처리해 최종 효과를 비교하는 계획을 적어 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** A timeline of duplicate risks and required sink properties.
- **What the LLM can get wrong:** The LLM may claim deduplication removes duplicates even beyond its retention period.
- **How to validate:** Plan repeated processing of one synthetic event before and after state expiry and compare final effects.

## Investigate serving and lakehouse differences {#event-architecture-04}

- **Situation:** In this hypothetical case, two paths receiving the same events show different daily counts.
- **Context to give the LLM:** Both paths: [transforms, filters, sink writes, recovery state]; Comparison evidence: [event-ID samples, lag, event/ingestion time, aggregate scope].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Both paths: [transforms, filters, sink writes, recovery state]
    Comparison evidence: [event-ID samples, lag, event/ingestion time, aggregate scope]

    [Task]
    Review the current design and separate definition, delay, duplicate, and loss hypotheses.
    First check whether the comparison uses the same time basis and event set.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return evidence, falsification checks, and ordered read-only checks for each hypothesis.

    [Checks]
    Compare presence by event ID and duplicate counts in a bounded range after lag has cleared.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    두 경로: [변환·필터·sink 방식·복구 상태]
    비교 근거: [event ID 표본·lag·event/ingestion time·집계 범위]

    [요청]
    정의 차이, 지연, 중복, 유실 가설을 분리해서 현재 설계를 검토해 줘.
    같은 시간 기준과 동일한 event 집합으로 비교할 수 있는지 먼저 확인해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    가설별 근거·반증 조건·읽기 전용 확인 순서를 작성해 줘.

    [검증]
    Lag가 해소된 제한 구간에서 event ID별 존재 여부와 중복 수를 대조하도록 해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Evidence, falsification checks, and ordered read-only checks for each hypothesis.
- **What the LLM can get wrong:** The LLM may infer loss from count differences or assume both paths must match immediately.
- **How to validate:** Compare presence by event ID and duplicate counts in a bounded range after lag has cleared.

## Find confusion between event and ingestion time {#event-architecture-05}

- **Situation:** In this hypothetical case, late events enter a different day's metrics.
- **Context to give the LLM:** Time fields: [event time, ingestion time, producer timestamp definitions]; Processing rules: [aggregate SQL, time zone, late-event policy, synthetic sample].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Time fields: [event time, ingestion time, producer timestamp definitions]
    Processing rules: [aggregate SQL, time zone, late-event policy, synthetic sample]

    [Task]
    Explain the current aggregate by separating occurrence, producer recording, and platform arrival time.
    Identify the time basis that matches the metric and missing time-zone or delay details.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return each synthetic event's current and required reporting date in a table.

    [Checks]
    Compare manual expected results with aggregates for date-boundary and out-of-order samples.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    시간 필드: [event time·ingestion time·producer timestamp 정의]
    처리 규칙: [집계 SQL·시간대·늦은 이벤트 정책·합성 표본]

    [요청]
    사건 발생·생성 기록·플랫폼 도착 시각을 구분해 현재 집계를 설명해 줘.
    의도한 지표 정의에 맞는 기준과 누락된 시간대·지연 정보를 찾아 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    합성 이벤트별 현재 포함 날짜와 요구되는 포함 날짜를 표로 작성해 줘.

    [검증]
    날짜 경계와 순서가 뒤바뀐 표본으로 수작업 기대값과 집계 결과를 비교해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Each synthetic event's current and required reporting date in a table.
- **What the LLM can get wrong:** The LLM may treat producer timestamps as occurrence time or attribute every time gap to network delay.
- **How to validate:** Compare manual expected results with aggregates for date-boundary and out-of-order samples.

## Represent a correction as a new event {#event-architecture-06}

- **Situation:** This hypothetical design compares overwriting an event with adding a correction event.
- **Context to give the LLM:** Facts and needs: [original event meaning, correction reason, retention needs]; Consumption: [event IDs, linking identifiers, consumer materialization, replay rules].

Example prompt:

=== "English"

    ```text {.prompt}
    [Context]
    Facts and needs: [original event meaning, correction reason, retention needs]
    Consumption: [event IDs, linking identifiers, consumer materialization, replay rules]

    [Task]
    Separate the original fact from the correction and review ambiguities in the current contract.
    Explain duplicate, reordering, and replay effects on each consumer when using a new event.
    Separate observations, assumptions, hypotheses, and missing evidence.

    [Output]
    Return contract questions, a synthetic event sequence, and expected results for each consumer.

    [Checks]
    Check expected results for bounded replay before and after correction, with duplicates and reordering.
    Provide review and test plans only; do not run or change production.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    사실과 요구: [원래 이벤트 의미·정정 이유·보존 요구]
    소비 방식: [event ID·연결 식별자·consumer별 materialization·replay 규칙]

    [요청]
    과거 사실과 정정 사실의 의미를 나누고 현재 계약의 모호성을 검토해 줘.
    새 이벤트 방식에서 중복·순서 변경·replay가 각 consumer에 미치는 영향을 설명해 줘.
    관찰, 가정, 가설, 부족한 근거를 구분해 줘.

    [출력]
    필요한 계약 질문과 합성 이벤트 흐름, consumer별 기대 결과를 작성해 줘.

    [검증]
    정정 전·후, 중복 정정, 순서 변경을 포함한 제한 replay의 기대 결과를 확인해 줘.
    운영 실행·변경 없이 검토와 검증 계획만 제시해 줘.
    ```

- **Expected output:** Contract questions, a synthetic event sequence, and expected results for each consumer.
- **What the LLM can get wrong:** The LLM may assume immutable events automatically define corrections and consistent final state.
- **How to validate:** Check expected results for bounded replay before and after correction, with duplicates and reordering.
