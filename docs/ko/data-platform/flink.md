---
id: data-platform-flink
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-05-01
  - DPE-05-02
  - DPE-05-03
  - DPE-05-04
  - DPE-05-05
  - DPE-05-06
  - DPE-05-07
  - DPE-05-08
  - DPE-05-09
  - DPE-05-10
  - DPE-05-11
  - DPE-05-12
  - DPE-05-13
  - DPE-05-14
---

# Apache Flink

문서 유형: Learn. 제공된 학습 자료의 개념과 설계 예시를 정리했다. `studied`는 개념 학습을 뜻하며, 직접 구현하거나 운영 검증했다는 뜻이 아니다. SQL과 수치는 설명용 예시이며 실행하지 않았다.

## 5.1 Why Flink

핵심:

> **Spark는 Batch-first에서 Streaming으로 확장되었고, Flink는 Streaming-first로 설계되었다.**

Spark Structured Streaming은 주로 Micro-batch로 이해할 수 있다.

Flink는 이벤트가 들어오는 대로 지속적으로 처리하는 continuous streaming model이 중심이다.

Flink가 강한 영역:

- Event Time
- Watermark
- Window
- State
- Timer
- Stateful Streaming
- 낮은 latency
- 복잡한 실시간 처리

대표 예:

- 실시간 이상 탐지
- Session 분석
- 최근 5분 Error Rate
- 실시간 Feature 계산

핵심:

> **Flink = Stateful Stream Processing Engine**

## 5.2 Flink Architecture

### JobManager

전체 Job 관리.

Spark Driver와 개념적으로 유사.

### TaskManager

실제 Task 실행.

Spark Executor와 개념적으로 유사.

### Operator

처리 단계.

예:

```text
Source → Filter → KeyBy → Window → Aggregate → Sink
```

### Parallelism

동일 Operator를 여러 개 병렬 실행.

### Task Slot

TaskManager 내부의 논리적 실행 공간.

## 5.3 DataStream Model

기본 흐름:

```text
Source
 ↓
Transformation
 ↓
Sink
```

### Source

Kafka / CDC / File 등.

### Transformation

filter / map / keyBy / window / aggregate.

### Sink

Iceberg / Kafka / DB / Search Store.

### KeyBy

같은 key를 같은 논리 처리 단위로 묶는다.

```text
keyBy(user_id)
```

이후 Keyed State를 유지할 수 있다.

핵심:

```text
Stream
 ↓
KeyBy
 ↓
Stateful Processing
```

## 5.4 Event Time

주요 시간:

- Event Time
- Processing Time
- Ingestion Time

Event Time은 실제 사건 발생 시각이다. Processing Time은 operator가 처리하는 시각이고 Ingestion Time은 시스템에 들어온 시각이다.

Streaming에서는 Event가 늦거나 순서가 바뀔 수 있다.

이를 **Out-of-order arrival**이라고 한다.

Event Time 기준 처리 덕분에 실제 발생 시간에 맞는 분석이 가능하다.

## 5.5 Watermark

Watermark:

> **이 시간보다 이전 Event는 대부분 도착했다고 판단하는 진행 기준**

예:

```text
최신 Event Time = 10:01:10
허용 지연 = 5초

Watermark ≈ 10:01:05
```

Watermark가 모든 Event의 도착을 보장하는 것은 아니다.

Watermark보다 과거 Event가 나중에 오면 **Late Event**가 된다.

Late Event 처리:

- 버리기
- Allowed Lateness
- 별도 처리

Trade-off:

```text
Watermark 느림
→ late event를 더 포함할 가능성 ↑
→ 결과 latency ↑

Watermark 빠름
→ latency ↓
→ late event 누락 가능
```

Idle Partition 때문에 Watermark 진행이 막힐 수 있어 idle detection 같은 처리가 필요할 수 있다.

## 5.6 Window

Streaming은 끝이 없으므로 일정 구간으로 잘라 집계한다.

### Tumbling Window

겹치지 않는 고정 구간.

```text
10:00~10:01
10:01~10:02
```

### Sliding Window

겹치는 이동 구간.

```text
최근 5분 데이터를 1분마다 계산
```

### Session Window

일정 시간 Event가 없으면 Session 종료.

예:

```text
User activity
→ 10분 inactivity
→ Session close
```

Watermark와 Window는 함께 사용된다.

## 5.7 State

State:

> **이전에 처리한 정보를 Flink가 기억하는 것**

예:

```text
user A → click_count = 3
user B → click_count = 1
```

### Keyed State

`keyBy()` 이후 key별 상태.

### ValueState

값 하나.

### ListState

값 목록.

### MapState

Key-Value 형태.

### State TTL

설정된 갱신·만료·cleanup 규칙에 따라 오래된 State를 정리하는 기능.

Window도 내부적으로 State를 사용한다고 이해할 수 있다.

## 5.8 Checkpoint

Checkpoint:

> **Flink의 실행 State와 처리 위치를 주기적으로 저장하는 복구 지점**

장애 발생:

```text
TaskManager failure
 ↓
Checkpoint 복원
 ↓
Kafka Offset 복원
 ↓
처리 재개
```

### Distributed Snapshot

여러 TaskManager/Operator의 상태를 일관된 Checkpoint로 저장.

### Checkpoint Barrier

Stream에 Barrier가 흐르며 어느 지점까지 Snapshot에 포함할지 맞춘다.

### Aligned Checkpoint

여러 Input Barrier를 맞춰 진행.

### Unaligned Checkpoint

Backpressure 상황 등에서 in-flight data까지 포함해 빠르게 Snapshot할 수 있다.

Checkpoint는 일반 Backup이 아니라 **Streaming Job을 이어서 실행하기 위한 실행 상태 저장**이다.

## 5.9 Savepoint

Savepoint:

> **운영자가 의도적으로 만드는 Job State Snapshot**

주요 용도:

- Job Upgrade
- Migration
- Rescaling
- Planned Stop/Restart

차이:

```text
Checkpoint
→ 자동
→ 장애 복구 중심

Savepoint
→ 의도적
→ 운영 변경 중심
```

Parallelism 4 → 8 변경 같은 Rescaling에도 활용 가능.

State 구조 변경 시 State Migration / Compatibility도 고려해야 한다.

## 5.10 Exactly-Once Processing

Exactly-once:

> **각 Event의 효과가 최종 결과에 한 번만 반영되는 것**

중요:

> **Flink 내부 exactly-once와 End-to-End exactly-once는 다르다.**

필요한 범위:

```text
Source Offset
+
Flink State
+
Sink Consistency
```

Sink가 중복 Write를 허용하면 전체 시스템은 exactly-once가 아니다.

대안:

```text
At-Least-Once
+
Idempotent Sink
```

## 5.11 Backpressure

Backpressure:

> **뒤 단계가 느려 앞 단계까지 처리 속도가 느려지는 현상**

예:

```text
Kafka
 ↓
Filter
 ↓
Aggregate
 ↓
Slow Database

Database 느림
→ Aggregate 밀림
→ Filter 밀림
→ Kafka 소비 느림
```

결과로 Kafka Consumer Lag이 증가할 수 있다.

원인:

- 느린 Sink
- 무거운 Operator
- Network
- Skew
- 외부 DB/API 병목

대응:

- Parallelism 증가
- Sink 개선
- Batch Write
- 외부 시스템 Scaling
- Skew 해소

Backpressure 자체는 overload로부터 시스템을 보호하는 자연스러운 flow control이기도 하다.

## 5.12 Flink + Kafka

역할:

```text
Kafka
→ Event 저장/전달

Flink
→ Stateful Stream Processing
```

### Kafka Partition과 Flink Parallelism

Kafka Partition 수는 Source 병렬 소비 상한에 영향을 준다.

```text
Kafka Partitions = 4
Source Parallelism = 8
```

이어도 동시에 유효하게 읽을 Partition은 4개뿐이다.

### Offset

Flink Checkpoint와 함께 Kafka Offset을 관리해 복구한다.

### Timestamp

Kafka/Event timestamp를 Event Time으로 사용할 수 있다.

### Ordering

Kafka는 Partition 내부 순서를 유지하지만 global ordering은 보장하지 않는다.

### Kafka Partitioning vs Flink keyBy

목적이 다르다.

```text
Kafka Partition
→ Event 저장/병렬 소비 위치

Flink keyBy
→ State 처리 단위 재분배
```

## 5.13 Flink + Iceberg

목적:

> **Streaming 결과를 Lakehouse에 지속 저장**

```text
Application
 ↓
Kafka
 ↓
Flink
 ↓
Iceberg
```

### Streaming Append

새 Event를 계속 append.

### Commit Coordination

Flink Task가 File을 만들고 Iceberg Commit으로 Snapshot 반영.

### Small File Problem

자주 Commit하면 작은 File이 많이 생길 수 있다.

### Compaction

작은 File을 큰 File로 합친다.

### Flink + Spark Role Split

```text
Flink
→ 실시간 처리/적재

Spark
→ Batch Transform / Backfill / Compaction
```

### Update / Upsert

Current-State Table 등에서는 UPDATE / DELETE / MERGE가 필요할 수 있다.

## 5.14 Flink vs Spark

### Flink가 잘 맞는 경우

- 낮은 latency
- Stateful Streaming
- Event Time
- Watermark
- Session
- 복잡한 실시간 Rule

### Spark가 잘 맞는 경우

- 대규모 Batch
- ETL
- Large Join
- Backfill
- Silver/Gold 생성
- ML Dataset

둘 다 Batch/Streaming이 가능하지만 강점이 다르다.

작은 규모에서는 굳이 Flink를 추가하지 않고 Spark Structured Streaming만으로 충분할 수 있다.

핵심:

```text
Spark
→ Large-scale processing

Flink
→ Stateful real-time streaming
```

## 적용 시 보완할 점

Spark/Flink의 역사적 출발점은 선택을 돕는 모델이며 현재 실행 모드의 전체 목록은 아니다. Task slot은 논리적 자원 할당 단위로 CPU core와 단순히 같지 않다. Source parallelism과 downstream operator parallelism도 구분한다.

Watermark 예시의 5초는 out-of-order 허용 가정이지 정확한 모든 구현의 수식이 아니다. 여러 입력의 watermark는 보통 가장 느린 입력의 진행에 묶인다. Idleness 설정과 late-event 정책을 같이 점검한다. 느리게 진행시켜도 정확도가 자동 보장되지 않으며 state 비용도 늘 수 있다. Event-time session 종료는 단순 wall-clock 대기만으로 결정되지 않는다. [Flink watermark](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/event-time/generating_watermarks/)

State TTL은 단순한 즉시 자동 삭제가 아니다. 확인한 DataStream state 문서는 processing-time TTL을 설명한다. 갱신 기준·만료값 가시성·cleanup 방식을 확인해야 한다. [Flink state](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/state/)

Checkpoint는 외부 시스템 전체의 backup이 아니다. Unaligned checkpoint는 in-flight data를 함께 기록하는 방식이며 단순히 alignment를 건너뛰는 at-least-once 모드와 같지 않다. 복구 시 원본 replay와 state 복원이 가능해도 sink의 transaction/idempotency는 별도로 필요하다. Savepoint 복원에서는 operator identity와 state schema 호환성도 확인한다. [Flink stateful processing](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/)

느린 외부 sink가 이미 포화 상태라면 parallelism 증가가 악화시킬 수도 있다. Flink Iceberg upsert는 connector·format·key 제약을 따른다. 확인한 문서는 v2와 primary key/identifier fields 및 partition 원본 열의 equality fields 포함을 요구한다. Spark SQL MERGE를 Flink sink에 그대로 대입하지 않는다. [Iceberg Flink 쓰기](https://iceberg.apache.org/docs/latest/flink-writes/)

## 연결해서 읽기

[이벤트 의미](event-architecture.md), [Spark](spark.md), [Iceberg](lakehouse-iceberg.md).

## LLM 실전: Watermark 정체 진단

- 상황: 가상 streaming job에서 입력은 오는데 window 결과가 늦다.
- 제공할 맥락: 입력별 timestamp/watermark, idle 설정, lag, backpressure, checkpoint duration, sink latency를 제공한다.
- 기대 결과: Idle input과 느린 처리의 구분, late-event 영향, 검증 단계다.
- 오류 가능성: Watermark를 wall clock으로 보거나 checkpoint 성공을 sink 정확성으로 오해할 수 있다.
- 검증 방법: 입력별 최소 watermark와 late-event 결과를 확인하고 제한된 재현에서 state·sink 결과도 비교한다.

예시 프롬프트:

=== "한국어"

    ```text {.prompt}
    [맥락]
    입력 진행: [timestamp·입력별 watermark·idle 설정·lag]
    처리 지표: [backpressure·checkpoint duration·sink latency]

    [요청]
    Event-time 진행이 막힌 이유를 검토해 줘.
    관찰 사실·idle input 가설·느린 sink 가설·누락 근거를 구분해 줘.

    [출력]
    Late-data 위험과 입력 정체·느린 처리의 차이를 설명해 줘.

    [검증]
    State 삭제나 운영 retention 변경 없이 제한된 검증 실험을 제안해 줘.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Input progress: [timestamps, per-input watermarks, idle settings, lag]
    Processing metrics: [backpressure, checkpoint duration, sink latency]

    [Task]
    Assess why event-time progress is stalled.
    Separate observed facts, idle-input hypotheses, slow-sink hypotheses, and missing evidence.

    [Output]
    Explain late-data risks and distinguish idle input from slow processing.

    [Checks]
    Propose a bounded test without dropping state or changing production retention.
    ```

[이 주제의 실무 프롬프트 6개 더 보기](../prompts/flink.md)

LLM 출력은 작업 가설이다. 공식 문서와 실제 설정·로그·측정으로 검증한다. 외부 문서 확인일: 2026-09-24. 구현 버전을 시험했다는 의미는 아니다.
