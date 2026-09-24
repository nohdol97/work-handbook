<!-- 반입 기록
범위: 업로드 Markdown 전체 1~6081행, Chapter 1~18 및 Final Mental Model.
읽기: 영역별 전체 읽기와 개인정보 검토 완료. 접근하지 못한 본문 없음.
한계: 원래 대화 및 Chapter 1~4 복원 전 자료는 제공되지 않음.
개인정보: generic 예시와 공개 제품명만 확인; 제거할 실제 민감 정보 없음.
원본 bytes: 88486; SHA-256: 25edd5ffd0f0e4ab05a4e1a144b17b9eaaca1aa1a0c9ea5dcf598c98d2ca8427
정규화: 아래 ledger에 명시한 행 끝 공백만 제거. 본문·행 순서·내용은 보존.
원문 행 번호는 경계 다음부터 셈. 공백 복원 후 업로드와 bytes 일치 검증 완료.
whitespace_restoration: [{"line": 3, "removed": "  "}, {"line": 6, "removed": "  "}, {"line": 16, "removed": "  "}, {"line": 17, "removed": "  "}, {"line": 669, "removed": "  "}, {"line": 1844, "removed": "  "}]
-->
<!-- ORIGINAL SOURCE START -->
# Data Platform Engineering Study Session — Source Markdown

> **문서 목적**
> 이 문서는 이 세션에서 학습한 Data Platform Engineering 내용을 이후 문서화/핸드북 생성의 **source markdown**으로 재사용하기 위한 원본 노트다.
>
> **학습 방식**
> 이 세션은 각 기술의 내부 구현을 지나치게 깊게 파기보다 아래 질문에 답할 수 있는 수준을 목표로 했다.
>
> - 왜 이 기술이 필요한가?
> - 어떤 문제를 해결하는가?
> - 핵심 기능은 무엇인가?
> - 다른 기술과 어떻게 연결되는가?
> - 비슷한 기술과 역할이 어떻게 다른가?
> - 전체 Data Platform Architecture에서 어디에 위치하는가?
>
> **주의**
> Chapter 1~4는 이미 완료된 학습 범위를 기준으로 이 세션의 학습 수준에 맞춰 복원했다.
> Chapter 5 이후는 이 세션에서 실제로 이어서 학습한 흐름을 기준으로 정리했다.

---

# Table of Contents

1. Data Engineering Foundations
2. Event Data Architecture
3. Lakehouse / Iceberg
4. Spark
5. Flink
6. CDC / Debezium
7. Orchestration
8. dbt
9. Analytical Data Modeling
10. Trino
11. Data Quality Engineering
12. Data Observability
13. Lineage & Metadata Platform
14. Data Governance
15. AI-Ready Data
16. AI Evaluation Data Platform
17. Supplementary Clarifications
18. Current Progress and Remaining Curriculum

---

# Chapter 1 — Data Engineering Foundations

## 1.1 OLTP vs OLAP

### OLTP

OLTP는 **Online Transaction Processing**의 약자다.

주요 목적은 서비스의 실시간 트랜잭션 처리다.

예:

- 사용자 회원가입
- 주문 생성
- 결제
- 재고 변경
- 게시글 작성

특징:

- 작은 범위의 row를 자주 읽고 쓴다.
- INSERT / UPDATE / DELETE가 많다.
- 빠른 단건 응답이 중요하다.
- 정규화된 데이터 모델을 많이 사용한다.

대표적인 시스템:

- PostgreSQL
- MySQL

예:

```text
users
orders
payments
```

서비스 애플리케이션은 보통 이런 OLTP DB를 사용한다.

---

### OLAP

OLAP는 **Online Analytical Processing**의 약자다.

목적은 대량 데이터를 분석하는 것이다.

예:

```text
지난 1년 동안
팀별 LLM 사용 비용은?

모델별 평균 latency는?

지난 6개월 사용자 행동 패턴은?
```

특징:

- 매우 많은 row를 읽는다.
- 대규모 Scan / Aggregation / Join이 많다.
- Write보다 Read 비중이 크다.
- Columnar Storage와 잘 맞는다.
- 비정규화 또는 Star Schema 같은 분석 모델을 많이 사용한다.

---

### PostgreSQL이 분석 이력에 점점 불리해지는 이유

PostgreSQL이 분석을 못 하는 것은 아니다.

하지만 데이터가 계속 쌓이면서:

```text
수억 ~ 수십억 rows
+
대규모 scan
+
대규모 aggregation
+
긴 기간 history
```

가 필요해지면 서비스 트랜잭션 DB와 분석 workload가 충돌할 수 있다.

그래서 흔히:

```text
Application
   ↓
PostgreSQL
   ↓
CDC / Event Pipeline
   ↓
Lakehouse / Warehouse
```

형태로 운영계와 분석계를 분리한다.

핵심:

> **OLTP는 서비스의 현재 상태를 빠르게 처리하고, OLAP는 대량 이력을 분석한다.**

---

## 1.2 Row-Oriented vs Column-Oriented Storage

### Row-Oriented

Row 기반 저장은 한 row의 값들을 같이 저장한다.

개념적으로:

```text
Row 1: user_id, name, age, team
Row 2: user_id, name, age, team
```

OLTP에서 유리하다.

예를 들어 사용자 한 명의 모든 정보를 읽는다면 row 단위 저장이 자연스럽다.

---

### Column-Oriented

Column 기반 저장은 같은 column의 값들을 같이 저장한다.

개념적으로:

```text
user_id: 1, 2, 3, 4 ...
age:     20, 30, 40, 50 ...
team:    A, A, B, A ...
```

분석 Query는 특정 column만 읽는 경우가 많다.

예:

```sql
SELECT AVG(latency_ms)
FROM llm_calls
```

이때 `prompt`, `response`, `user_id`까지 모두 읽을 필요가 없다.

그래서 Columnar Format이 OLAP에 잘 맞는다.

---

### Compression

같은 column에는 비슷한 값이 반복되는 경우가 많다.

예:

```text
team_id:
A
A
A
A
B
B
B
```

같은 형태는 압축 효율이 좋다.

따라서 Columnar Storage는:

- 읽는 데이터 감소
- 압축 효율 향상
- 분석 Query 성능 향상

에 유리하다.

---

### Column Pruning

Query에서 필요한 column만 읽는 최적화다.

예:

```sql
SELECT model_id, latency_ms
FROM fact_llm_call
```

이면 필요한 column만 읽는다.

핵심:

> **Parquet을 columnar file format이라고 하는 이유는 데이터를 column 중심으로 저장해 분석 시 필요한 column만 효율적으로 읽을 수 있기 때문이다.**

---

## 1.3 Parquet

Parquet은 대표적인 **Columnar File Format**이다.

역할:

> **대량 분석 데이터를 효율적으로 저장하는 파일 포맷**

Parquet 자체는 Database가 아니다.

```text
S3
├─ part-0001.parquet
├─ part-0002.parquet
└─ part-0003.parquet
```

처럼 Object Storage에 파일로 저장할 수 있다.

---

### Row Group

Parquet 파일 내부 데이터는 큰 단위인 **Row Group**으로 나뉜다.

```text
Parquet File
├─ Row Group 1
├─ Row Group 2
└─ Row Group 3
```

각 Row Group 내부에서 데이터는 column 단위로 저장된다.

---

### Page

Row Group 내부의 column 데이터는 다시 Page 단위로 나뉠 수 있다.

큰 그림:

```text
Parquet File
  ↓
Row Group
  ↓
Column Chunk
  ↓
Page
```

이 세션에서는 내부 binary format까지 깊게 들어갈 필요는 없고, **Parquet이 데이터를 계층적인 단위로 나누고 통계 정보를 이용해 불필요한 Scan을 줄인다** 정도가 핵심이다.

---

### Encoding / Compression

Parquet은 column별 특성에 따라 encoding과 compression을 적용한다.

목적:

```text
저장 공간 감소
+
I/O 감소
```

예:

- 반복되는 값
- 숫자 데이터
- 문자열 dictionary

등이 효율적으로 압축될 수 있다.

---

### Statistics

Parquet은 Row Group이나 Page에 대해 통계를 가질 수 있다.

예:

```text
latency_ms
min = 100
max = 500
```

Query가:

```sql
WHERE latency_ms > 1000
```

이라면 해당 Row Group을 읽을 필요가 없다.

이런 최적화가 **Min/Max Pruning**이다.

---

### Predicate Pushdown / Pruning

조건을 이용해 불필요한 데이터를 읽지 않는다.

예:

```sql
WHERE event_date = '2026-09-24'
```

가능한 경우 필요한 Row Group/File만 읽는다.

---

### Column Pruning

필요한 column만 읽는다.

Parquet의 중요한 장점은:

```text
필요한 row 범위만
+
필요한 column만
```

읽을 수 있다는 점이다.

---

## 1.4 Object Storage

대표적인 Object Storage:

- Amazon S3
- S3-compatible storage
- Azure Blob Storage
- Google Cloud Storage

Lakehouse에서 Object Storage를 많이 사용하는 이유:

- 매우 큰 데이터 저장 가능
- Compute와 Storage 분리 가능
- 상대적으로 저렴한 대용량 저장
- 여러 Compute Engine이 같은 데이터를 공유 가능

---

### Object vs Block/File Storage

Object Storage에서는 데이터를 object 단위로 관리한다.

예:

```text
s3://bucket/path/file.parquet
```

전통적인 local filesystem처럼 random write를 자주 하는 형태보다 큰 immutable-like object를 저장하는 데 잘 맞는다.

---

### Storage / Compute Separation

전통적인 Database는 Compute와 Storage가 한 시스템에 강하게 결합되는 경우가 많다.

Lakehouse는:

```text
Storage
→ S3

Compute
→ Spark / Trino / Flink / Databricks
```

처럼 분리할 수 있다.

장점:

- Compute를 독립적으로 확장
- 같은 데이터를 여러 Engine에서 읽기
- Compute를 꺼도 Storage는 유지

---

### Remote I/O

Compute와 Storage가 분리되어 있으므로 네트워크를 통해 파일을 읽어야 한다.

따라서:

- 불필요한 Scan 줄이기
- 파일 크기 최적화
- pruning
- caching

등이 중요해진다.

---

## 1.5 File Layout Engineering

Lakehouse에서는 파일 하나의 크기도 성능에 영향을 준다.

---

### Small File Problem

예:

```text
file1.parquet  1MB
file2.parquet  2MB
file3.parquet  800KB
...
수백만 개
```

파일이 너무 작으면:

- Metadata 증가
- 파일 open 비용 증가
- Query planning 비용 증가
- Task 수 과다
- Object Storage request 증가

문제가 생긴다.

---

### Too-Large File

반대로 파일이 지나치게 크면:

- 병렬 처리 단위가 줄어듦
- 특정 Task가 오래 걸릴 수 있음
- Rewrite 비용 증가

등의 문제가 생길 수 있다.

따라서 workload에 맞는 **Target File Size**가 필요하다.

---

### Compaction

작은 파일들을 큰 파일로 합친다.

```text
5MB
10MB
8MB
7MB
  ↓
Compaction
  ↓
적절한 크기의 Parquet File
```

Streaming → Lakehouse 구조에서는 특히 중요하다.

---

### Write Amplification

데이터 일부를 수정하기 위해 큰 파일 전체를 다시 쓰게 되면 실제 변경량보다 훨씬 많은 write가 발생할 수 있다.

이런 비용도 File Layout과 Table Format 설계에서 고려해야 한다.

---

## 1.6 Partitioning Fundamentals

Partitioning은 데이터를 특정 기준으로 물리적/논리적으로 나누는 것이다.

예:

```text
event_date=2026-09-23
event_date=2026-09-24
```

---

### Partition Pruning

Query:

```sql
WHERE event_date = '2026-09-24'
```

이면 해당 날짜 Partition만 읽도록 할 수 있다.

즉:

> **전체 데이터를 Scan하지 않고 필요한 Partition만 읽는다.**

---

### Cardinality

Partition Key를 선택할 때 cardinality가 중요하다.

낮은 cardinality 예:

```text
country
status
```

높은 cardinality 예:

```text
user_id
request_id
```

`user_id`처럼 값 종류가 매우 많은 column을 직접 Partition Key로 사용하면 너무 많은 Partition이 생길 수 있다.

---

### Good / Bad Partition Keys

좋은 Partition Key:

- Query에서 자주 필터링
- Partition 수가 과도하지 않음
- 데이터가 너무 한쪽에 몰리지 않음

대표적으로 시간 기반:

```text
day
hour
```

등이 자주 사용된다.

---

### Over-Partitioning

Partition이 너무 세분화되면:

- 작은 파일 증가
- Metadata 증가
- 관리 복잡성 증가

가 발생한다.

---

### Partition vs File

Partition은 논리적인 데이터 구분이고, 하나의 Partition 안에 여러 파일이 존재할 수 있다.

```text
date=2026-09-24
├─ file1.parquet
├─ file2.parquet
└─ file3.parquet
```

---

## 1.7 Bucketing / Sorting / Indexing

### Bucketing

Hash를 이용해 데이터를 일정 개수 bucket으로 나눈다.

예:

```text
bucket(user_id, 32)
```

고 cardinality key를 직접 Partition으로 만들지 않고 일정한 개수로 분산할 수 있다.

---

### Sorting

파일 내부 데이터를 특정 key 기준으로 정렬한다.

예:

```text
sort by user_id
```

같은 값이 비슷한 위치에 모이면 file min/max statistics가 더 유용해질 수 있다.

---

### Clustering

자주 같이 조회되는 데이터를 물리적으로 가까이 배치해 Scan 범위를 줄이는 설계다.

---

### Lakehouse Indexing vs OLTP Index

OLTP DB에서는 B-Tree 같은 row-level index를 자주 사용한다.

Lakehouse는 대량 Scan workload가 중심이므로:

- Partition
- File Statistics
- Sort Order
- Data Skipping
- Clustering

같은 방식으로 읽는 범위를 줄이는 경우가 많다.

---

# Chapter 2 — Event Data Architecture

> Kafka Broker 운영, ISR, Replica 운영 같은 인프라 상세는 별도 Platform 세션의 범위다.
> 이 장에서는 Data Engineering 관점의 Event Semantics에 집중한다.

## 2.1 Event Modeling

Event는 과거에 발생한 사실을 표현하는 데이터다.

예:

```text
user clicked button
order created
agent executed
llm called
tool failed
```

좋은 Event는 가능하면 immutable하게 설계한다.

즉 과거 Event를 수정하기보다 새로운 Event를 추가한다.

---

### 주요 필드

#### Event ID

이벤트 고유 식별자.

```text
event_id
```

중복 제거와 추적에 중요하다.

#### Event Time

실제로 사건이 발생한 시간.

#### Ingestion Time

데이터 플랫폼이 이벤트를 받은 시간.

둘은 다를 수 있다.

```text
event_time     = 10:00:01
ingestion_time = 10:00:05
```

#### Producer Timestamp

Producer가 기록한 생성 시각.

#### Trace / Session Identifier

여러 이벤트를 하나의 실행이나 사용자 세션으로 연결한다.

예:

```text
trace_id
session_id
execution_id
```

---

## 2.2 Event Contracts

Event Contract는 Producer와 Consumer 사이에서 Event의 의미를 합의하는 것이다.

예:

```text
field: latency_ms
type: integer
unit: millisecond
required: true
owner: AI Platform Team
```

Contract에 포함할 수 있는 항목:

- Required / Optional
- Data Type
- Unit
- Semantic Definition
- Ownership
- Version
- Compatibility Rule

핵심:

> **Schema만 같다고 의미까지 같은 것은 아니다.**

예를 들어 `latency=5`가:

- 5ms
- 5초

중 무엇인지 Contract가 정의해야 한다.

---

## 2.3 Schema Evolution

Event Schema는 시간이 지나며 변한다.

예:

```text
v1:
event_id
user_id
event_time

v2:
event_id
user_id
event_time
device_type
```

---

### JSON vs Avro vs Protobuf

#### JSON

장점:
- 사람이 읽기 쉬움
- 유연함

단점:
- Schema 강제력이 약할 수 있음
- 데이터 크기가 상대적으로 큼

#### Avro

Schema 기반 serialization에 자주 사용된다.

Kafka + Schema Registry 환경에서 많이 볼 수 있다.

#### Protobuf

명확한 Schema와 compact binary format을 제공한다.

---

### Schema Registry

Event Schema를 중앙 관리한다.

역할:

```text
Schema Version 관리
Compatibility 검사
Breaking Change 방지
```

---

### Backward Compatibility

새 Consumer가 과거 데이터를 읽을 수 있는가.

### Forward Compatibility

과거 Consumer가 새로운 데이터를 처리할 수 있는가.

### Breaking Change

기존 Consumer를 깨뜨릴 수 있는 변경.

예:

- 필수 field 삭제
- incompatible type 변경
- 의미 변경

---

## 2.4 Delivery Semantics

### At-Most-Once

최대 한 번 전달.

중복은 적지만 유실 가능.

```text
0회 또는 1회
```

### At-Least-Once

최소 한 번 전달.

유실 방지에 유리하지만 중복 가능.

```text
1회 이상
```

### Exactly-Once

중요한 질문:

> **Exactly-once가 어디부터 어디까지 보장되는가?**

Kafka 내부, Stream Processor State, Sink까지 범위가 다를 수 있다.

Data Engineering에서는 흔히:

```text
At-Least-Once
+
Idempotency
+
Deduplication
```

으로 최종 결과를 한 번만 반영되도록 설계하기도 한다.

---

### Idempotency

같은 작업을 여러 번 실행해도 최종 결과가 같아야 한다.

```text
event A 처리
event A 다시 처리

최종 결과 동일
```

### Deduplication

동일 이벤트가 여러 번 도착했을 때 하나만 남기는 것.

예:

```text
event_id
```

를 이용해 중복을 찾을 수 있다.

---

## 2.5 Replay

Kafka 같은 Event Log의 중요한 장점은 과거 Event를 다시 읽을 수 있다는 것이다.

### Offset Replay

특정 offset부터 다시 읽는다.

```text
offset 100
→ 101
→ 102
...
```

### Downstream Rebuild

예:

```text
Kafka
  ↓ replay
새로운 Search Index
```

또는:

```text
Kafka
  ↓
새로운 Lakehouse Table
```

을 다시 만들 수 있다.

### Backfill from Kafka

과거 Event를 다시 처리해 누락된 데이터나 새 로직을 채울 수 있다.

### Replay Safety

Replay에서는 중복 이벤트가 발생할 수 있으므로:

- Idempotency
- Deduplication
- Deterministic processing

이 중요하다.

---

## 2.6 Event → Serving + Lakehouse Dual Path

하나의 논리적 Event가 여러 목적에 materialize될 수 있다.

```text
Application
   ↓
Kafka
   ├─→ Search Store
   ├─→ Operational Serving Store
   └─→ Lakehouse / Iceberg
```

예를 들어 사용자 click event 하나가:

- 실시간 Dashboard
- 검색/추천
- 장기 분석
- AI Evaluation

에 동시에 사용될 수 있다.

핵심:

> **Event Stream은 전달 경로이고, 하나의 Event가 목적에 따라 여러 저장 형태로 materialize될 수 있다.**

---

# Chapter 3 — Lakehouse / Iceberg

## 3.1 Lakehouse Architecture

Lakehouse는 Data Lake의 열린 Storage와 Data Warehouse의 Table Management 기능을 결합하려는 구조다.

큰 그림:

```text
Object Storage
   ↓
Parquet Files
   +
Table Format
   ↓
Iceberg
   ↓
Compute
Spark / Trino / Flink
   ↓
Catalog / Governance
```

주요 계층:

- Storage Layer
- Compute Layer
- Table Format
- Catalog
- Governance / Control Plane

---

### Data Plane vs Control Plane

Data Plane:

- 실제 Parquet 파일
- 실제 Query / Read / Write

Control Plane:

- Metadata
- Catalog
- Access Policy
- Governance
- Table Definition

정도로 개념적으로 나눌 수 있다.

---

## 3.2 Iceberg Metadata Internals

Iceberg의 핵심은 단순히 Parquet 파일을 저장하는 것이 아니라 **Table Metadata를 관리하는 것**이다.

구조를 단순화하면:

```text
Iceberg Table
   ↓
Metadata JSON
   ↓
Snapshot
   ↓
Manifest List
   ↓
Manifest Files
   ↓
Data Files
```

---

### Metadata JSON

Table의 현재 상태를 설명한다.

포함될 수 있는 정보:

- 현재 Snapshot
- Schema
- Partition Spec
- Sort Order
- Snapshot History

---

### Current Snapshot

현재 Table 상태를 가리키는 Snapshot.

---

### Snapshot Log

과거 Snapshot 이력을 기록한다.

따라서 Metadata JSON이 시간에 따라 여러 버전 존재할 수 있다.

질문:

> Iceberg에 Table Metadata가 여러 개일 수 있는가?

답:

> 가능하다. Table 상태 변화에 따라 새로운 Metadata 파일이 만들어지고 Catalog/metadata pointer가 현재 Metadata를 가리키는 방식으로 이해할 수 있다.

---

### Manifest List / Manifest File

Snapshot이 직접 모든 Data File을 하나씩 들고 있는 대신 중간 Metadata 계층을 사용한다.

개념:

```text
Snapshot
  ↓
Manifest List
  ↓
Manifest
  ↓
Data File
```

이를 통해 대규모 Table의 File 목록과 Statistics를 효율적으로 관리한다.

---

### Data Files

실제 데이터가 있는 Parquet/ORC/Avro 파일.

### Delete Files

Merge-on-Read 같은 방식에서 삭제 정보를 별도 파일로 관리할 수 있다.

---

## 3.3 Snapshot Semantics

Snapshot은 특정 시점의 Table 상태다.

중요한 점:

> Snapshot마다 모든 파일을 새로 복사하는 것이 아니다.

여러 Snapshot이 동일한 Data File을 공유할 수 있다.

```text
Snapshot 1
→ A, B, C

Snapshot 2
→ A, B, C, D
```

A/B/C는 그대로 공유되고 D만 추가될 수 있다.

---

### Time Travel

과거 Snapshot을 기준으로 Query할 수 있다.

### Rollback

Table을 과거 Snapshot 상태로 되돌릴 수 있다.

### Consistent Read

Query는 특정 Snapshot 기준으로 일관된 Table 상태를 읽는다.

### Snapshot Isolation Intuition

동시에 Write가 발생하더라도 Query는 중간 상태가 아니라 특정 Snapshot의 일관된 상태를 읽는다고 이해하면 된다.

---

## 3.4 Atomic Commit Model

여러 Writer가 동시에 Table을 변경할 수 있다.

Iceberg는 **Optimistic Concurrency** 방식으로 이해할 수 있다.

개념적으로:

```text
현재 Metadata = M1

Writer A
→ M1 기준 변경

Writer B
→ M1 기준 변경
```

한 Writer가 먼저 Commit하면 현재 Metadata가 바뀐다.

다른 Writer는:

- Conflict 확인
- 필요한 경우 retry

할 수 있다.

---

### Compare-and-Swap Intuition

"내가 작업을 시작했을 때의 Table 상태가 아직 현재 상태인가?"를 확인하고 Commit한다고 이해하면 된다.

---

### Orphan Files

File은 만들어졌는데 Commit에 실패하면 Table Metadata에서 참조되지 않는 파일이 남을 수 있다.

이런 File은 나중에 cleanup 대상이 된다.

---

## 3.5 Partitioning in Iceberg

Iceberg는 **Hidden Partitioning** 개념이 중요하다.

사용자는 Query에서 Partition Column을 직접 의식하지 않고 논리 column 조건을 사용할 수 있다.

예:

```sql
WHERE event_time >= ...
```

Iceberg가 내부 Partition Transform을 이용해 Pruning할 수 있다.

---

### Partition Transforms

대표:

- day
- hour
- bucket
- truncate

예:

```text
day(event_time)
bucket(32, user_id)
```

---

### Partition Evolution

Table을 다시 전체 Rewrite하지 않고 Partition Spec을 변경할 수 있다.

예:

```text
기존: day(event_time)
변경: hour(event_time)
```

과거 데이터와 새 데이터가 서로 다른 Partition Spec을 사용해도 Metadata를 통해 관리할 수 있다.

---

### High Cardinality Design

`user_id`처럼 cardinality가 높은 값은 직접 Partition하지 않고 bucket transform 등을 고려할 수 있다.

---

## 3.6 Query Pruning

Iceberg Query 성능에서 핵심은:

> **얼마나 적은 데이터를 읽게 할 수 있는가**

Pruning 단계:

```text
Partition Pruning
   ↓
Manifest Pruning
   ↓
Data File Pruning
   ↓
Parquet Row Group Pruning
   ↓
Column Pruning
```

---

### Scan Amplification

실제로 필요한 데이터보다 훨씬 많은 데이터를 읽으면 Scan Amplification이 크다고 볼 수 있다.

좋은 Layout은 이를 줄인다.

---

## 3.7 Sort Order and Clustering

File min/max statistics가 효과적이려면 값이 어느 정도 모여 있는 것이 좋다.

예:

```text
random user_id distribution
```

보다:

```text
user_id 순으로 어느 정도 정렬
```

되어 있으면 특정 user 범위를 찾을 때 File Pruning이 더 유리할 수 있다.

핵심:

> **Sort / Clustering은 Query Pattern을 기준으로 설계해야 한다.**

---

## 3.8 UPDATE / DELETE / MERGE

Object Storage의 Parquet 파일은 일반 DB row처럼 작은 단위로 즉시 수정하기 어렵다.

Iceberg는 Table Format 차원에서 Update/Delete를 지원한다.

---

### Copy-on-Write

변경된 row가 포함된 Data File을 다시 작성한다.

장점:
- 읽기가 단순

단점:
- Write 비용 증가

---

### Merge-on-Read

원본 Data File은 유지하고 변경/삭제 정보를 별도 파일로 저장한 뒤 Read할 때 합친다.

장점:
- 빠른 Write 가능

단점:
- Read가 복잡해질 수 있음
- Delete File 관리 필요

---

### Position Delete

특정 File의 특정 row position을 삭제 대상으로 표시.

### Equality Delete

특정 key/value 조건에 해당하는 row를 삭제 대상으로 표현.

---

### UPDATE

개념적으로:

```text
기존 row 삭제
+
새 row 삽입
```

처럼 이해할 수 있다.

### MERGE

CDC Upsert 등에 사용 가능하지만 큰 Table에서는 비용을 고려해야 한다.

---

## 3.9 Maintenance

Lakehouse는 파일 기반이므로 Maintenance가 중요하다.

### Data File Compaction

작은 Data File들을 적절한 크기로 합친다.

### Delete File Rewrite

Delete File이 너무 많이 쌓이면 Rewrite한다.

### Manifest Rewrite

Manifest가 비효율적으로 많아질 경우 재정리한다.

### Snapshot Expiration

오래된 Snapshot을 제거한다.

### Orphan Cleanup

Metadata에서 더 이상 참조되지 않는 File을 제거한다.

핵심:

> **Iceberg를 도입했다고 Maintenance가 사라지는 것은 아니다.**

---

## 3.10 Catalogs

Iceberg Table을 운영하려면 현재 Metadata를 찾을 수 있어야 한다.

Catalog의 역할:

- Table 이름 등록
- 현재 Metadata 위치 관리
- Namespace 관리

대표 Catalog:

- Hive Metastore
- AWS Glue
- REST Catalog
- JDBC Catalog
- Nessie
- Unity Catalog concepts

---

## 3.11 Catalog vs Governance

둘은 관련 있지만 같은 개념이 아니다.

### Catalog 기본 역할

```text
table name
→ current metadata
```

같은 Table Registration / Discovery.

### Governance

더 넓은 역할:

- Access Policy
- Ownership
- Classification
- Audit
- Lineage
- Masking

---

### Unity Catalog와 Iceberg Catalog

질문:

> Unity Catalog는 Iceberg Catalog에 여러 정보를 추가한 형태인가?

단순히 동일하다고 보기는 어렵다.

개념적으로:

```text
Iceberg Catalog
→ Iceberg Table을 찾고 Metadata pointer를 관리

Unity Catalog
→ Catalog 기능 + Access Control + Lineage + Governance + 여러 Data/AI Asset 관리
```

즉 Unity Catalog는 훨씬 넓은 Governance Layer로 이해하는 것이 맞다.

---

# Chapter 4 — Spark

## 4.1 Spark Architecture

Spark Application의 기본 구성:

```text
Application
   ↓
Driver
   ↓
Executors
```

### Driver

- Application 전체 관리
- Job planning
- Task scheduling
- Executor coordination

### Executor

- 실제 Task 실행
- 데이터 처리
- Cache 유지

### Cluster Manager

Spark Resource를 할당하는 시스템.

예:

- Kubernetes
- YARN
- Standalone

Spark on Kubernetes는 Kubernetes가 Driver/Executor Pod의 실행 Resource를 관리하는 형태로 이해할 수 있다.

---

## 4.2 Execution Model

Spark 실행 단위:

```text
Application
  ↓
Job
  ↓
Stage
  ↓
Task
```

### Job

Action이 실행되면서 생성되는 큰 작업 단위.

### Stage

Shuffle Boundary 등에 따라 나뉘는 실행 단계.

### Task

하나의 Spark Partition을 처리하는 실제 실행 단위.

### Spark Partition

Spark가 병렬 처리하는 논리적인 데이터 단위.

### DAG

Transformation 의존 관계를 그래프로 표현한다.

---

## 4.3 Lazy Evaluation

Spark Transformation은 호출 즉시 실행되지 않는다.

예:

```text
filter
map
join
```

을 정의해도 실제 계산은 Action이 호출될 때 시작된다.

### Transformation

새 Dataset을 정의.

### Action

실제 실행을 유발.

예:

- count
- collect
- write

---

### Query Planning

개념적으로:

```text
User Code
  ↓
Logical Plan
  ↓
Optimized Logical Plan
  ↓
Physical Plan
  ↓
Execution
```

Spark SQL/DataFrame에서는 Catalyst Optimizer가 Query Plan을 최적화한다.

`explain()`을 통해 계획을 확인할 수 있다.

---

## 4.4 Narrow vs Wide Dependencies

### Narrow Dependency

각 Output Partition이 소수 Input Partition에만 의존.

예:

```text
map
filter
```

데이터가 Worker 사이를 크게 이동하지 않을 수 있다.

### Wide Dependency

여러 Partition의 데이터가 재분배되어야 함.

예:

```text
groupBy
join
repartition
```

이때 Shuffle이 발생한다.

---

## 4.5 Shuffle

Shuffle은 Spark 성능에서 매우 중요한 개념이다.

```text
Worker A ─┐
Worker B ─┼→ Network Redistribution
Worker C ─┘
```

발생 가능한 비용:

- Network I/O
- Shuffle Write
- Shuffle Read
- Sort
- Serialization
- Disk Spill
- Stage Boundary

핵심:

> **대규모 Join / GroupBy가 비싼 이유는 데이터가 Worker 사이를 이동하기 때문이다.**

---

## 4.6 Join Strategies

### Broadcast Hash Join

큰 Fact + 작은 Dimension.

```text
Large Fact
+
Small Dimension
```

작은 Table을 모든 Executor에 Broadcast한다.

장점:
- 큰 Table Shuffle 감소

주의:
- Broadcast 대상이 너무 크면 Memory 문제

---

### Sort-Merge Join

두 큰 Table을 Join할 때 자주 사용되는 전략.

개념적으로:

```text
양쪽을 Join Key 기준으로 Shuffle
↓
Sort
↓
Merge
```

---

### Shuffle Hash Join

양쪽 데이터를 Partitioning 후 Hash Join.

---

### Fact + Dimension

일반적인 분석 Join Pattern.

### Large-Large Join

둘 다 크면 Shuffle 비용이 매우 커질 수 있다.

### Semi / Anti Join

존재 여부 또는 제외 조건에 사용된다.

### Join Cardinality / Join Explosion

Join Key 중복이 많으면 결과 row 수가 예상보다 크게 늘어날 수 있다.

---

## 4.7 Partition Management

### repartition

Partition을 다시 나눈다.

Shuffle 발생 가능.

사용:
- 병렬성 증가
- 특정 key 기준 재분배
- Output file 수 조절

### coalesce

주로 Partition 수를 줄일 때 사용.

항상 full shuffle이 필요한 것은 아니다.

---

### Keyed Repartitioning

특정 key 기준으로 같은 값이 같은 Partition으로 가도록 할 수 있다.

### Task Parallelism

Spark Partition 수가 Task 병렬성과 직접 연결된다.

### Target Partition Size / Output File Count

Partition 수는:
- Task 수
- File 수
- Memory pressure

와 연결된다.

---

## 4.8 Cache / Persist

Spark는 중간 결과를 Memory/Disk에 유지할 수 있다.

### 왜 사용하나

같은 데이터를 여러 번 계산하면 재계산 비용이 크다.

```text
Expensive Transform
  ↓
Cache
  ├─ Query A
  └─ Query B
```

### unpersist

더 이상 필요 없는 Cache는 해제해야 한다.

### Cache가 항상 좋은 것은 아님

- 한 번만 사용하는 데이터
- 매우 큰 Dataset
- Memory가 부족한 환경

에서는 오히려 불리할 수 있다.

### Durable Iceberg Intermediate Table

장시간 또는 Job 간 재사용해야 하는 결과라면 Cache보다 Iceberg Intermediate Table 같은 durable storage가 더 적합할 수 있다.

---

## 4.9 Data Skew

Data Skew는 데이터가 특정 Partition에 몰리는 현상이다.

예:

```text
team_id = A → 80%
나머지 → 20%
```

그러면 한 Task만 매우 오래 걸릴 수 있다.

### Hot Key

특정 key에 데이터가 집중.

### Skewed Join / Aggregation

Join이나 GroupBy에서 특정 key가 병목.

### Null / Default Key Skew

`NULL`, `UNKNOWN`, `0` 같은 기본값에 데이터가 몰릴 수 있다.

### Salting

Hot Key에 추가 salt를 붙여 여러 key로 분산한 뒤 나중에 합친다.

단, **원래 key ordering이 중요한 Streaming/Event 처리에는 그대로 적용하기 어렵다.**
Spark Batch의 Join/Aggregation skew 해결과 Kafka Ordering 문제는 구분해야 한다.

### Pre-Aggregation

미리 부분 집계해 Shuffle 데이터량을 줄인다.

### Heavy-Key Special Path

특정 Hot Key만 별도 처리.

### AQE

Adaptive Query Execution이 runtime statistics를 이용해 일부 skew 최적화를 할 수 있다.

---

## 4.10 Spark Performance Engineering

대표 병목:

- CPU
- Executor Memory
- Heap Pressure
- GC
- Disk Spill
- Network
- Shuffle
- S3 Scan
- Small Files
- Straggler

### Executor Sizing

Executor Memory/Core를 workload에 맞게 조정.

### Spill

Memory에 다 못 담은 중간 데이터를 Disk로 내림.

### Straggler

특정 Task 하나가 매우 늦게 끝나는 현상.

Skew 등이 원인이 될 수 있다.

### Speculative Execution

유난히 느린 Task를 다른 Executor에서 중복 실행해 먼저 끝나는 결과를 사용할 수 있다.

### Spark UI

어느 Stage/Task가 병목인지 진단하는 데 중요하다.

---

## 4.11 Spark + Iceberg

Spark는 Iceberg 데이터를 Batch 처리하는 주요 Compute Engine 중 하나다.

```text
Iceberg
  ↓
Spark
  ↓
Transform
  ↓
Iceberg
```

### Iceberg Scan Planning

Iceberg Metadata를 이용해 읽어야 할 File을 결정한다.

### Predicate Pushdown / Pruning

불필요한 File/Row Group을 읽지 않는다.

### Spark Tasks vs Iceberg Files

하나의 File이 반드시 하나의 Task와 1:1은 아니지만 File Layout이 Task 병렬성과 Scan 효율에 영향을 준다.

### Write Distribution

데이터를 적절히 분산해서 File을 생성해야 한다.

### Target File Size

너무 작은 File을 만들지 않도록 관리한다.

### Sort Order

Query Pattern에 맞춰 Layout을 최적화할 수 있다.

### MERGE

CDC Current-State Table 구성 등에 사용 가능.

### Write Skew

특정 Partition/Key에 Write가 몰릴 수 있다.

### Commit Behavior

Spark Task가 File을 만들고 Iceberg Commit을 통해 새 Snapshot을 Table에 반영한다.

### Maintenance Debt

Streaming Write, MERGE, 작은 File 등이 쌓이면 Compaction 등 Maintenance가 필요해진다.

---

## 4.12 Structured Streaming

Spark Structured Streaming은 Streaming 데이터를 Table처럼 다루는 모델을 제공한다.

주로 **Micro-batch** 방식으로 이해할 수 있다.

```text
Kafka
 ↓
Micro Batch
 ↓
Spark
 ↓
Sink
```

### Kafka Source

Kafka Topic을 Streaming Source로 사용.

### Checkpoint

처리 상태와 offset 등의 복구 정보 저장.

### State

Streaming Aggregation / Deduplication 등에 필요한 상태 유지.

### Event Time

실제 Event 발생 시간.

### Late Events

늦게 도착한 Event.

### Watermark

얼마나 늦은 Event까지 기다릴지 판단하는 기준.

### Window

시간 구간 단위 집계.

### Deduplication

중복 Event 제거.

### Output Modes

Aggregation 결과를 어떤 방식으로 출력할지 결정.

### foreachBatch

각 Micro Batch를 Batch Logic으로 처리할 수 있다.

### Streaming → Iceberg

실시간에 가깝게 Iceberg에 적재 가능.

주의:

```text
자주 쓰기
→ 작은 File
→ Compaction 필요
```

### Streaming vs Batch Backfill

실시간 처리는 Streaming, 과거 대규모 재처리는 Batch Spark가 자연스럽다.

---

## 4.13 Spark의 역할

질문:

> Spark 역할이 무엇인가?

핵심:

> **Spark는 대규모 분산 데이터 처리 엔진이다.**

주요 활용:

- 대규모 ETL
- Join
- Aggregation
- Backfill
- Lakehouse Transform
- ML Dataset 생성
- Batch Processing
- Structured Streaming

Spark는 Storage가 아니다.

```text
Iceberg / S3
→ Storage/Table

Spark
→ Compute
```

---

## 4.14 Spark를 써도 dbt가 필요한가?

역할이 다르다.

```text
Spark
→ 대규모 데이터 처리 엔진

dbt
→ SQL Transformation 관리 계층
```

함께 사용할 수 있다.

예:

```text
Raw
 ↓
Spark
 ↓
Silver
 ↓
dbt
 ↓
Gold / Mart
```

반대로 단순 SQL Transformation이면 Spark 없이 dbt + Trino/Warehouse만으로 처리할 수도 있다.

---

# Chapter 5 — Flink

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

---

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

---

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

---

## 5.4 Event Time

주요 시간:

- Event Time
- Processing Time
- Ingestion Time

Event Time은 실제 사건 발생 시각이다.

Streaming에서는 Event가 늦거나 순서가 바뀔 수 있다.

이를 **Out-of-order arrival**이라고 한다.

Event Time 기준 처리 덕분에 실제 발생 시간에 맞는 분석이 가능하다.

---

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
→ 정확도 ↑
→ 결과 latency ↑

Watermark 빠름
→ latency ↓
→ late event 누락 가능
```

Idle Partition 때문에 Watermark 진행이 막힐 수 있어 idle detection 같은 처리가 필요할 수 있다.

---

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

---

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

오래 사용되지 않은 State 자동 정리.

Window도 내부적으로 State를 사용한다고 이해할 수 있다.

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

# Chapter 6 — CDC / Debezium

## 6.1 CDC Fundamentals

CDC = Change Data Capture.

목적:

> **DB의 INSERT / UPDATE / DELETE 변경을 지속적으로 다른 시스템에 전달**

Polling 방식:

```sql
SELECT *
FROM orders
WHERE updated_at > last_time
```

문제:

- DB Query 부하
- DELETE 감지 어려움
- 변경 순서 관리 어려움
- 실시간성 제한

CDC는 DB Transaction Log를 읽는다.

PostgreSQL:

```text
WAL
Write-Ahead Log
```

구조:

```text
PostgreSQL
 ↓
WAL
 ↓
Debezium
 ↓
Kafka
```

---

## 6.2 Debezium Architecture

### Debezium Connector

DB별 CDC Reader.

예:
- PostgreSQL
- MySQL
- SQL Server

### Kafka Connect

Connector 실행/관리 Platform.

### Offset

DB Log를 어디까지 읽었는지 기억.

### Snapshot

CDC 시작 전에 이미 존재하던 데이터를 초기 복제.

---

## 6.3 Initial Snapshot

처음 CDC를 시작하면 기존 데이터가 이미 존재한다.

```text
Existing Table
 ↓
Initial Snapshot
 ↓
WAL Streaming CDC
```

Snapshot 동안에도 변경이 발생할 수 있으므로 WAL 위치를 관리해 Snapshot 이후 변경을 이어서 읽는다.

목표:

```text
기존 데이터
+
Snapshot 중 변경
+
이후 변경
```

을 모두 놓치지 않는 것.

Connector Restart 때마다 전체 Snapshot을 다시 하는 것은 아니다.

Offset이 있으면 이어서 읽는다.

---

## 6.4 CDC Event Structure

대표 정보:

- before
- after
- operation type
- source metadata
- transaction metadata

### INSERT

```text
before = null
after = new row
```

### UPDATE

```text
before = old row
after  = new row
```

### DELETE

```text
before = old row
after = null
```

Operation 예:

- c: create
- u: update
- d: delete
- r: snapshot read

Source Metadata:

- database
- schema
- table
- WAL position
- timestamp

Transaction Metadata:

- transaction id
- order information

---

## 6.5 Ordering

핵심:

> **CDC에서는 global ordering보다 같은 entity/key의 변경 순서가 중요하다.**

Kafka는 Partition 내부 Ordering은 유지하지만 Partition 간 global order는 보장하지 않는다.

같은 Primary Key를 같은 Partition으로 보내면 같은 entity의 순서를 유지하기 쉽다.

```text
order 100:
CREATED
→ PAID
→ SHIPPED
```

DB Transaction 하나에서 여러 Table 변경이 발생하더라도 Kafka에서는 여러 Event가 되어 서로 다른 Partition으로 갈 수 있다.

---

## 6.6 Deletes

### DELETE Event

실제 DB 삭제를 표현.

### Tombstone

Kafka Log Compaction에서 특정 key가 삭제되었음을 표현하는 `key + null value` record.

DELETE Event와 Tombstone은 목적이 다르다.

### Physical Delete

Downstream에서도 실제 삭제.

### Logical Delete

```text
deleted = true
```

같이 상태로 보존.

### History vs Current State

```text
Bronze History
→ 삭제 Event 포함 모든 변경 보존

Silver Current State
→ 현재 존재하는 row만 유지
```

---

## 6.7 Schema Changes

Source DB Schema는 바뀔 수 있다.

예:

- Column 추가
- Column 삭제
- Rename
- Type 변경
- Nullable 변경

상대적으로 안전한 변경:

```text
nullable column 추가
```

위험한 변경:

```text
type 변경
column 삭제
rename
```

CDC에서는 Schema Change가:

```text
Source
→ Kafka
→ Flink/Spark
→ Iceberg
→ dbt
→ BI
```

전체에 영향을 줄 수 있다.

따라서:

```text
감지
→ Compatibility 확인
→ downstream 반영
```

이 중요하다.

---

## 6.8 CDC → Iceberg

대표 구조:

```text
PostgreSQL
 ↓
Debezium
 ↓
Kafka
 ↓
Flink / Spark
 ↓
Iceberg
```

### History Table

모든 변경 Event를 저장.

```text
order 100 CREATED
order 100 PAID
order 100 SHIPPED
```

### Current-State Table

최신 상태만 유지.

```text
order 100 SHIPPED
```

### MERGE / Upsert

```text
new row
→ INSERT

existing row
→ UPDATE
```

### Late Change

오래된 변경이 최신 상태를 덮어쓰지 않도록 sequence/source position 등을 고려해야 한다.

### Idempotency

Replay로 같은 CDC Event가 다시 와도 결과가 깨지지 않아야 한다.

---

## 6.9 CDC Failure Recovery

정상적인 복구:

```text
Connector Failure
 ↓
Restart
 ↓
Stored Offset
 ↓
WAL Replay
```

Replay 때문에 Duplicate가 발생할 수 있다.

따라서 Downstream은 Idempotent해야 한다.

Offset을 잃거나 필요한 WAL이 이미 삭제됐다면 새 Snapshot이 필요할 수 있다.

핵심:

```text
Offset
→ 처리 위치

Replay
→ 다시 처리

Idempotency
→ 중복 안전성

Snapshot Recovery
→ 복구 불가능 시 재초기화
```

---

# Chapter 7 — Orchestration

## 7.1 DAG Fundamentals

Airflow는:

> **여러 데이터 작업의 순서, 시간, 실패, 재실행을 관리하는 Orchestrator**

이다.

### DAG

전체 Workflow.

### Task

개별 실행 단위.

### Dependency

Task 실행 순서.

### Schedule

DAG 실행 시점.

예:

```text
Extract
 ↓
Spark Transform
 ↓
dbt
 ↓
Quality Check
 ↓
Publish
```

Airflow는 데이터를 직접 대규모로 처리하기보다 다른 시스템을 지휘한다.

---

## 7.2 Operators / Tasks

Operator:

> Task를 어떤 방식으로 실행할지 정의.

예:

- Python Operator
- SQL Operator
- Bash Operator
- Spark Job
- dbt command

Airflow 역할:

```text
Airflow
→ Orchestrate

Spark
→ Compute

dbt
→ Transformation

Trino
→ Query
```

---

## 7.3 Retries

Task Failure는 두 종류로 생각할 수 있다.

### Transient Failure

- Network timeout
- DB connection
- 일시적 cluster issue

Retry가 효과적.

### Permanent Failure

- SQL syntax error
- 잘못된 Schema
- Code bug

Retry해도 해결되지 않음.

### Idempotency

Retry-safe Task는 여러 번 실행해도 최종 결과가 같아야 한다.

나쁜 예:

```text
무조건 append
```

좋은 예:

```text
Partition overwrite
MERGE
replace
```

---

## 7.4 Backfills

Backfill:

> **과거 데이터를 다시 계산하는 작업**

사용 상황:

- Pipeline 장애
- Logic bug 수정
- 데이터 누락
- 새 컬럼 추가
- Business Logic 변경

### Full Backfill

전체 기간 재처리.

### Partial / Partition Backfill

필요한 날짜/Partition만 재처리.

Backfill도 Idempotency가 중요하다.

---

## 7.5 Sensors / Event Dependencies

Sensor:

> **특정 조건이 만족될 때까지 기다리는 Task**

예:

- S3 File 도착
- Upstream DAG 완료
- 데이터 준비 완료

Schedule과 Dependency는 다르다.

```text
02:00 실행 시도
+
실제 데이터 준비 확인
```

Polling 방식도 있고 Event-driven 방식도 있다.

---

## 7.6 Parameterization

같은 DAG를 다양한 조건으로 재사용.

예:

```text
process_date
start_date
end_date
environment
data_interval
```

좋은 Pipeline:

```text
"오늘 데이터 처리"
```

보다:

```text
"2026-09-24 데이터를 처리"
```

처럼 명시적인 Data Interval을 받는 것이 재실행/Backfill에 유리하다.

---

## 7.7 Failure Handling

Task별 상태를 관리하므로 DAG 전체를 처음부터 다시 돌릴 필요가 없다.

```text
Extract ✅
Spark ✅
dbt ❌
Quality -
Publish -
```

dbt 문제 수정 후 해당 Task부터 재실행 가능.

일반적으로 Upstream 실패 시 Downstream 실행을 막는다.

Alert에는:

- DAG
- Task
- 실패 시각
- Retry 수
- Error

등의 Context가 있어야 한다.

---

## 7.8 Orchestrator Anti-Patterns

피해야 할 것:

1. Airflow Worker 안에서 대규모 Compute 직접 수행
2. XCom으로 대용량 Data 전달
3. DAG 간 과도하게 복잡한 의존성
4. Airflow를 Streaming Engine처럼 사용

좋은 역할 분리:

```text
Airflow
→ Orchestration

Spark
→ Batch Compute

Flink
→ Streaming

dbt
→ SQL Transformation

Iceberg
→ Storage/Table
```

---

# Chapter 8 — dbt

## 8.1 Project Structure

dbt:

> **SQL 기반 Transformation을 체계적으로 관리하는 도구**

핵심 구성:

### Models

SQL Transformation 단위.

### Sources

dbt 밖에서 만들어진 원본 Table.

### Tests

데이터 품질 규칙.

### Macros

반복 SQL Logic 재사용.

일반 구조:

```text
models/
  staging/
  intermediate/
  marts/

tests/
macros/
```

---

## 8.2 ref()

`ref()`:

> **다른 dbt Model을 참조하며 Dependency를 선언**

예:

```sql
SELECT *
FROM {{ ref('stg_orders') }}
```

효과:

- 실행 순서 계산
- DAG 생성
- Lineage 생성
- 환경별 Relation 처리

`source()`:

```text
dbt 외부 원본
```

`ref()`:

```text
다른 dbt model
```

---

## 8.3 Staging Models

Staging:

> **원본을 깨끗하게 정리하는 첫 변환 계층**

주요 역할:

- Rename
- Type normalization
- Basic null handling
- 날짜 형식 통일
- 필요한 Column 선택

복잡한 Business Logic은 많이 넣지 않는다.

---

## 8.4 Intermediate Models

Intermediate:

> **Staging Data를 Join/Aggregation해 재사용 가능한 Business Logic을 만드는 계층**

예:

```text
stg_orders
+
stg_customers
 ↓
int_orders_with_customer
```

여러 Mart가 이를 재사용할 수 있다.

작은 Project는 Intermediate를 생략할 수도 있다.

---

## 8.5 Marts

Mart:

> **최종 분석/소비 목적에 맞게 만든 Data Layer**

### Fact

사건/측정값.

### Dimension

Fact 설명 속성.

### Consumption Table

Dashboard/Report가 바로 사용할 수 있도록 미리 집계한 Table.

Lakehouse의 Gold Layer와 개념적으로 많이 겹친다.

```text
Staging
→ Intermediate
→ Mart

≈

Bronze/Silver
→ Gold
```

---

## 8.6 Incremental Models

매번 전체 Table을 다시 계산하지 않고 변경분만 처리.

### Append

새 데이터 추가만.

### Merge

INSERT + UPDATE.

### Incremental Filter

예:

```sql
WHERE event_time > last_processed_time
```

Late Arrival을 고려해 최근 며칠을 다시 읽고 MERGE할 수도 있다.

### Full Refresh

Logic 변경 등 필요 시 전체 재생성.

---

## 8.7 dbt Tests

대표 Test:

- not_null
- unique
- relationships
- accepted_values
- custom test

Pipeline 예:

```text
dbt run
 ↓
dbt test
 ↓
Pass
 ↓
Publish
```

dbt Test는 Data Quality 전체가 아니라 기본적인 Model/Table 규칙 검증에 특히 적합하다.

---

## 8.8 Snapshots

dbt Snapshot:

> **현재 Table을 비교해 변경 이력을 보존**

주로 SCD Type 2와 연결.

### Type 1

기존 값 overwrite.

### Type 2

과거 row 유지 + 새 version row 생성.

CDC History가 이미 충분히 있다면 별도의 Snapshot이 반드시 필요한 것은 아니다.

---

## 8.9 Documentation / Lineage

Table/Column 설명을 Metadata로 관리할 수 있다.

`source()`와 `ref()` 관계를 이용해 dbt Model Lineage를 생성한다.

예:

```text
raw.llm_calls
 ↓
stg_llm_calls
 ↓
int_llm_calls
 ↓
fact_llm_call
 ↓
mart_daily_usage
```

dbt Lineage는 전체 Data Platform Lineage의 일부다.

---

## 8.10 dbt + Databricks / Snowflake / Trino

dbt는 Compute Engine이 아니다.

```text
dbt
 ↓ SQL 생성/관리
Databricks / Snowflake / Trino
 ↓
실제 Compute
```

역할:

```text
dbt
→ Transformation Definition

Engine
→ Query / Compute Execution
```

Spark와 dbt는 경쟁 관계가 아니라 함께 사용할 수 있다.

---

# Chapter 9 — Analytical Data Modeling

## 9.1 Grain

Grain:

> **Table 한 row가 무엇을 의미하는가**

예:

```text
fact_order
→ 1 row = 1 order

fact_order_item
→ 1 row = 1 order item

fact_llm_call
→ 1 row = 1 LLM call
```

Grain을 잘못 이해하면 Join 후 중복 집계가 발생한다.

Data Modeling 순서:

```text
1. Grain
2. Fact
3. Dimension
4. Metric
```

---

## 9.2 Fact Tables

Fact Table:

> **발생한 사건이나 측정값**

### Event Fact

클릭, API 호출 등.

### Transaction Fact

주문, 결제 등.

### Periodic Snapshot Fact

일별 재고, 일별 잔액 등 일정 주기 상태.

### Accumulating Snapshot Fact

하나의 프로세스 진행 상태.

예:

```text
order_created_at
paid_at
shipped_at
delivered_at
```

---

## 9.3 Dimension Tables

Dimension:

> **Fact를 설명하는 속성 정보**

예:

```text
dim_customer
dim_product
dim_model
dim_team
```

### Natural Key

원본 시스템 식별자.

### Surrogate Key

분석 시스템에서 별도로 만든 Key.

SCD Type 2 버전을 구분할 때 유용하다.

---

## 9.4 Star Schema

중앙 Fact Table + 주변 Dimension.

```text
             dim_agent
                 |
dim_team — fact_llm_call — dim_model
                 |
              dim_date
```

장점:

- 이해 쉬움
- BI Query 쉬움
- 역할 명확

---

## 9.5 SCD

SCD = Slowly Changing Dimension.

### Type 1

Overwrite.

현재 값만 중요.

### Type 2

과거 상태 보존.

예:

```text
customer_sk | customer_id | region | valid_from | valid_to
```

과거 시점 분석 가능.

---

## 9.6 Denormalization

분석 Query를 단순화하고 Join을 줄이기 위해 일부 중복을 허용.

OLTP:

```text
Normalization 중심
```

OLAP:

```text
조회 편의와 성능을 위해 일부 Denormalization
```

너무 과도하게 모든 정보를 한 Table에 넣는 것도 문제다.

---

## 9.7 AI Platform Modeling

Grain을 섞지 않는 것이 중요하다.

### fact_agent_execution

```text
1 row = Agent 실행 1회
```

예 필드:

- execution_id
- agent_id
- user_id
- team_id
- started_at
- completed_at
- status
- total_latency
- total_cost

### fact_llm_call

```text
1 row = LLM 호출 1회
```

예:

- llm_call_id
- execution_id
- model_id
- input_tokens
- output_tokens
- latency
- cost

### fact_user_event

```text
1 row = 사용자 Event 1개
```

### dim_agent

Agent 설명.

### dim_model

Model 설명.

### dim_team

조직 설명.

같은 Dimension을 여러 Fact가 공유하는 구조를 Conformed Dimension으로 볼 수 있다.

핵심:

```text
Agent Execution
≠ LLM Call
≠ User Event
```

---

## 9.8 Metrics Modeling

목적:

> **KPI 정의를 일관되게 관리**

예:

```text
agent_execution_error_rate
=
failed execution count / total execution count
```

### Base Metric

- execution_count
- token_count
- cost

### Derived Metric

- error_rate
- cost_per_execution

### Semantic Layer

비즈니스 Metric 의미와 계산법을 중앙 정의.

예:

```text
DAU
Total Cost
Error Rate
Average Latency
```

Dashboard, Analyst, AI Agent가 동일한 정의를 사용하게 한다.

---

# Chapter 10 — Trino

## 10.1 Architecture

Trino:

> **외부 데이터 저장소를 빠르게 SQL로 조회하는 분산 SQL Query Engine**

Trino 자체가 주 Storage는 아니다.

### Coordinator

- SQL 분석
- Query Plan
- Stage/Task 관리

### Worker

- 실제 Scan
- Join
- Aggregation

개념 비교:

```text
Trino Coordinator ≈ Spark Driver
Trino Worker ≈ Spark Executor
```

---

## 10.2 Connector Model

Connector는 Trino와 외부 시스템 사이 Adapter.

예:

- Iceberg Connector
- PostgreSQL Connector
- Hive Connector

Trino Catalog 이름 구조:

```text
catalog.schema.table
```

예:

```text
iceberg.analytics.fact_llm_call
postgres.public.users
```

Trino Catalog와 Iceberg Catalog는 의미가 다르다.

Trino Catalog:

> 어떤 Connector/Data Source를 사용할지 구분.

Federated Query로 서로 다른 시스템을 한 SQL에서 Join할 수도 있지만 성능을 무조건 보장하는 것은 아니다.

---

## 10.3 Query Execution

구조:

```text
SQL
 ↓
Query Plan
 ↓
Stage
 ↓
Task
 ↓
Split
```

### Stage

큰 실행 단계.

### Task

특정 Worker에서 실행되는 Stage 일부.

### Split

Scan의 작은 작업 단위.

### Exchange

Worker 간 Data Redistribution.

Spark Shuffle과 비슷한 개념.

Join / GroupBy에서 Exchange가 많이 발생할 수 있다.

---

## 10.4 Pushdown

목적:

> **가능한 연산을 데이터가 있는 쪽에서 먼저 수행해 이동/Scan을 줄인다.**

### Predicate Pushdown

`WHERE` 조건을 Source로 내려보냄.

### Projection Pushdown

필요한 Column만.

### Aggregation Pushdown

가능하면 COUNT/SUM 등을 Source에서 수행.

Iceberg에서는 Partition/File/Row Group/Column Pruning이 비슷한 목적을 수행한다.

---

## 10.5 Join Strategies

### Broadcast Join

작은 Table을 모든 Worker에 복사.

```text
Huge Fact
+
Tiny Dimension
```

### Partitioned Join

큰 Table끼리 Join Key 기준 재분배.

Exchange 비용 발생.

### Data Skew

특정 key가 특정 Worker에 몰릴 수 있다.

---

## 10.6 Memory

Trino는 Join/Aggregation/Sort의 중간 데이터를 Memory에 유지한다.

주요 개념:

- Worker Memory
- Query Memory
- Spill

Spill:

```text
Memory 부족
 ↓
Disk 사용
```

Query 실패를 피할 수 있지만 느려진다.

---

## 10.7 Trino vs Spark

핵심:

```text
Trino
→ Interactive SQL / Query Serving

Spark
→ Large-scale Processing / Transformation
```

Trino:

- BI
- Ad-hoc Query
- 다수 사용자 동시 SQL

Spark:

- ETL
- Backfill
- Large Join
- ML Dataset
- Batch Transform

함께 사용:

```text
Spark
→ Data 생성

Trino
→ 생성된 Data 조회
```

---

## 10.8 Trino + Iceberg

구조:

```text
S3
 ↓
Parquet
 +
Iceberg Metadata
 ↓
Trino
 ↓
BI / Analyst
```

Trino는 Iceberg Metadata를 이용해 필요한 File을 찾고 Parquet Columnar 특성을 이용해 필요한 Column만 읽는다.

역할:

```text
S3
→ 실제 File

Parquet
→ File Format

Iceberg
→ Table Metadata / Snapshot

Trino
→ SQL Query
```

---

# Chapter 11 — Data Quality Engineering

## 11.1 Quality Dimensions

### Completeness

필수 데이터가 빠지지 않았는가.

### Uniqueness

중복되면 안 되는 값이 중복되지 않았는가.

### Validity

허용된 형식/범위인가.

### Consistency

다른 데이터와 모순되지 않는가.

### Freshness

제시간에 들어왔는가.

### Accuracy

실제 세계의 값과 맞는가.

### Volume

데이터 양이 정상 범위인가.

AI 예:

```text
fact_llm_call

Completeness
→ model_id NULL?

Uniqueness
→ llm_call_id 중복?

Validity
→ negative latency?

Consistency
→ model_id가 dim_model에 존재?

Freshness
→ 최근 Event 5분 이내?

Accuracy
→ billing과 cost 일치?

Volume
→ 호출량 급증/급감?
```

---

## 11.2 Validation Layers

### Ingestion Validation

- Schema
- Format
- Required Field
- Parsing

### Silver Validation

- Dedup
- Relationships
- Business Rules
- Valid Values

### Gold Validation

- KPI
- Freshness
- Aggregate Consistency
- Expected Volume

핵심:

```text
초기
→ 형식

중간
→ 데이터 논리

최종
→ 비즈니스 결과
```

---

## 11.3 Quarantine Patterns

Invalid Data를 버리지 않고 별도 보관.

```text
Incoming
 ↓
Validation
 ↙      ↘
Valid   Invalid
 ↓        ↓
Silver   Quarantine
```

Quarantine에:

- Raw payload
- Error type
- Error message
- Received time

등을 저장.

문제 수정 후 Reprocessing.

Quarantine이 쌓이기만 하면 안 되며 Volume/Error Reason Monitoring도 필요하다.

---

## 11.4 dbt Tests

Data Quality 관점의 dbt Test:

- not_null
- unique
- relationships
- accepted_values

강점:
- Model/Table 수준 정적 검증

부족할 수 있는 영역:
- Volume anomaly
- Distribution drift
- Freshness anomaly

---

## 11.5 Soda / Great Expectations / Deequ

공통:

> **Data Quality Rule 자동 검사 도구**

### Soda

Rule/check 중심.

### Great Expectations

Expectation 기반 검증.

### Deequ

Spark 환경 대규모 Data Quality 검사에 친화적.

세 도구는 기능이 많이 겹치며 이 세션에서는 각각의 구현보다 범주를 이해하는 것이 목표였다.

---

## 11.6 Data Quality SLOs

SLI:

> 실제 측정값.

SLO:

> 목표 수준.

예:

```text
Freshness < 5 min
Completeness > 99.9%
Duplicate Rate < 0.01%
```

Dataset마다 SLO가 달라야 한다.

실시간 Dashboard와 월간 Report는 필요한 Freshness가 다르다.

---

## 11.7 Incident Handling

흐름:

```text
Detect
 ↓
Contain
 ↓
Fix
 ↓
Reprocess
 ↓
Verify
```

### Detect

SLO 위반 감지.

### Contain

잘못된 Data의 Downstream 전파 차단.

### Fix

Root Cause 수정.

### Reprocess

Backfill / Replay.

### Verify

Quality Check 후 재개.

중요:

> **서비스가 살아 있어도 데이터가 틀리면 Data Incident다.**

---

# Chapter 12 — Data Observability

## 12.1 Data Freshness

### Source Freshness

원본 데이터가 제시간에 생성/수집되는가.

### Pipeline Freshness

Kafka → Bronze → Silver → Gold 처리 지연.

### Downstream Freshness

Dashboard/BI가 최신 데이터를 보여주는가.

단계별 Freshness를 보면 어느 구간부터 지연됐는지 찾을 수 있다.

---

## 12.2 Volume Monitoring

평소 대비 데이터 건수 급감/급증 탐지.

급감 원인 예:

- 수집 장애
- Producer 문제
- Filter Bug

급증 원인 예:

- Duplicate
- Replay
- Retry Storm
- Traffic Spike

Missing Partition도 중요한 Signal.

단순 절대값이 아니라:

- 최근 평균
- 같은 요일
- Seasonal pattern

등과 비교할 수 있다.

---

## 12.3 Schema Monitoring

감시:

- Column 추가
- 삭제
- Rename
- Type 변경
- Nullable 변경

Breaking Change는 Downstream Consumer를 깨뜨릴 수 있다.

Schema Monitoring + Lineage를 연결하면 영향 범위를 찾을 수 있다.

---

## 12.4 Distribution Drift

Volume은 정상인데 값 분포가 달라질 수 있다.

대표 Signal:

- Null Rate Drift
- Cardinality Drift
- Value Distribution Drift
- Numeric Distribution Drift

예:

```text
평소 FAILED = 5%
오늘 FAILED = 45%
```

Volume은 정상이어도 Data Health는 이상할 수 있다.

---

## 12.5 Pipeline Health vs Data Health

Pipeline Health:

- Job Status
- Kafka Lag
- Runtime
- CPU/Memory
- Failure

Data Health:

- Freshness
- Volume
- Schema
- Null
- Duplicate
- Distribution

중요 문장:

> **Green Pipeline ≠ Healthy Data**

Job이 성공해도 Query Logic이 잘못돼 결과가 0 rows일 수 있다.

---

## 12.6 Data SLIs / SLOs

Observability 관점에서 Data State를 지속 측정한다.

SLI 예:

```text
Freshness = 3분
NULL Rate = 0.5%
Volume = 98M
```

SLO 예:

```text
Freshness < 5분
NULL Rate < 1%
Volume Deviation < 20%
```

여러 Signal을 동시에 본다.

---

## 12.7 Alert Design

목표:

> **이상을 최대한 많이 알리는 것이 아니라 실제 대응할 가치가 있는 Alert를 만드는 것**

### Noisy Alert

Threshold 근처에서 ALERT/RECOVERY가 반복.

### Actionable Alert

알림만 보고도 어디를 조사할지 알 수 있음.

좋은 Alert:

```text
Threshold
+
Duration
+
Severity
+
Context
```

Warning / Critical을 나눌 수 있다.

Dataset 중요도 Tier별 Alert 정책도 가능.

Alert Fatigue를 방지해야 한다.

---

# Chapter 13 — Lineage & Metadata Platform

## 13.1 Metadata Types

Metadata:

> **데이터를 설명하는 데이터**

### Technical Metadata

- Table
- Column
- Type
- Schema
- Partition
- File Format

질문:

> 구조가 어떻게 생겼는가?

### Operational Metadata

- Last Updated
- Job Status
- Freshness
- Row Count
- Processing Time

질문:

> 지금 정상적으로 운영되는가?

### Business Metadata

- Description
- Owner
- KPI Definition
- Business Term
- Classification

질문:

> 이 데이터는 업무적으로 무엇을 의미하는가?

---

## 13.1A Business Metadata vs Semantic Layer

세션 중 보충 질문:

> Business Metadata는 Semantic Layer와 유사해 보인다.

답:

> **겹치는 부분은 많지만 동일하지 않다.**

Business Metadata:

> 데이터의 의미를 설명.

예:

```text
Revenue
→ VAT 제외
→ Refund 제외
→ Owner: Finance
```

Semantic Layer:

> 의미를 실제 계산 가능한 Metric/Dimension 정의로 제공.

예:

```text
Revenue
=
SUM(order_amount)
- SUM(refund)
- SUM(vat)
```

관계:

```text
Business Metadata
→ "Revenue가 무엇인가?"

Semantic Layer
→ "Revenue를 어떻게 계산하는가?"

BI / Dashboard / AI
→ 동일 정의 사용
```

Semantic Layer는 Business Metadata의 **실행 가능한 분석 정의**를 구체화한 계층으로 이해하면 좋다.

---

## 13.2 Dataset Lineage

Dataset Lineage:

> **Source → Job → Target 관계**

예:

```text
raw_user_events
 ↓
Spark Job
 ↓
silver_user_events
 ↓
dbt
 ↓
mart_daily_users
```

### Upstream

나를 만드는 쪽.

### Downstream

나를 사용하는 쪽.

활용:

- Root Cause
- Impact Analysis
- Data Trust

---

## 13.3 OpenLineage

OpenLineage:

> **서로 다른 Data Tool이 Lineage 정보를 공통 형식으로 표현하는 표준**

핵심 Entity:

### Job

어떤 작업인가.

### Run

특정 Job의 실행 1회.

### Dataset

Input / Output Data.

예:

```text
bronze.orders
 ↓
Job: transform_orders
 ↓
silver.orders
```

OpenLineage는 UI 자체라기보다 **Lineage Event Standard**다.

---

## 13.4 Column-Level Lineage

Table-Level보다 더 세밀한 Column 관계.

예:

```text
raw_orders.amount ────┐
                      ├→ silver_orders.net_amount
raw_orders.discount ──┘
```

활용:

- KPI Root Cause
- Schema Change Impact
- Sensitive Data Tracking

---

## 13.5 Impact Analysis

Lineage를 이용해 변경/장애 영향 확인.

### Upstream Analysis

문제 원인을 거슬러 올라감.

### Downstream Impact Analysis

변경이 어디까지 영향을 주는지 확인.

예:

```text
raw_orders.amount type 변경
 ↓
stg_orders
 ↓
fact_sales
 ↓
mart_daily_sales
 ↓
Dashboard
```

---

## 13.6 Marquez

Marquez:

> **OpenLineage Event를 저장하고 조회/시각화하는 Lineage System**

관계:

```text
OpenLineage
→ 표준

Marquez
→ 수집/저장/UI/API
```

Marquez는 Catalog 전체보다 Lineage/Run 관계에 초점이 강하다.

---

## 13.7 Catalog Integration

Catalog에 여러 정보를 통합.

```text
Iceberg
→ Technical Metadata

dbt
→ Model / Documentation / Dependencies

Airflow
→ Pipeline / Runs

OpenLineage
→ Lineage

Quality Tool
→ Data Quality
```

Catalog에서 볼 수 있는 정보:

- Description
- Owner
- Freshness
- Quality
- Upstream / Downstream
- Classification
- Access Policy

현대 Catalog는 단순 Table 목록이 아니라:

```text
Discovery
+
Metadata
+
Lineage
+
Governance
```

로 발전한다.

---

# Chapter 14 — Data Governance

## 14.1 Dataset Ownership

Dataset마다 책임 주체를 명확히 한다.

### Technical Owner

- Pipeline
- Schema
- Quality
- SLO

### Business Owner

- 의미
- KPI
- 업무 정의

Owner가 없으면 문제/변경 대응이 어려워진다.

---

## 14.2 Classification

데이터 중요도/민감도 분류.

예:

- Public
- Internal
- Confidential
- PII
- Sensitive

Column-level Classification도 중요하다.

예:

```text
email → PII
team_id → Internal
```

Classification은 Access / Masking / Retention Policy와 연결된다.

---

## 14.3 Retention Policies

Retention:

> **얼마나 오래 보관할 것인가**

기준:

- 비용
- 법/규제
- 민감도
- 분석 가치

예:

```text
Debug Log → 14일
User Event → 1년
Aggregated Metrics → 장기 보관
```

Hot / Cold / Archive Tier로 나눌 수도 있다.

Iceberg Snapshot Expiration도 Retention과 연결된다.

---

## 14.4 Deletion Policies

Deletion:

> **언제, 어디서, 어떤 방식으로 실제 제거할 것인가**

원본만 삭제해서 끝나지 않을 수 있다.

```text
PostgreSQL
 ↓
Kafka
 ↓
Bronze
 ↓
Silver
 ↓
Gold
 ↓
Backup
```

모든 Copy/Derived Data를 고려해야 한다.

### Logical Delete

삭제 표시.

### Physical Delete

실제 제거.

Iceberg에서는 현재 Snapshot에서 안 보인다고 물리적으로 완전히 삭제된 것은 아닐 수 있다.

과거 Snapshot/File cleanup까지 고려해야 한다.

---

## 14.5 Masking

민감한 실제 값을 가려서 보여준다.

### Static Masking

가린 값 자체를 별도 저장.

### Dynamic Masking

조회 User/Role에 따라 다르게 표시.

Classification과 연결:

```text
PII
 ↓
Masking Policy
```

AI Prompt/Response에도 PII Masking이 필요할 수 있다.

Masking과 Encryption은 다르다.

---

## 14.6 Row / Column Access

### Row-Level Access

사용자/팀별로 볼 수 있는 row 제한.

### Column-Level Access

민감 column 자체 조회 제한.

Masking과 차이:

```text
Column Access
→ Column을 못 봄

Masking
→ Column은 보이지만 값이 가려짐
```

### RBAC

Role 단위 권한 관리.

---

## 14.7 Auditability

누가 언제 어떤 데이터에 접근/변경했는지 기록.

Access Audit:

```text
user
dataset
time
action
query
```

Change Audit:

- Schema 변경
- Policy 변경
- Owner 변경
- Retention 변경

Observability와 차이:

```text
Observability
→ 시스템/데이터가 정상인가?

Audit
→ 누가 무엇을 했는가?
```

---

## 14.8 Data Contracts

Producer와 Consumer 사이 데이터 약속.

포함 가능:

- Schema
- Semantics
- Quality
- SLO
- Ownership
- Version

예:

```text
event_id
→ required + unique

latency_ms
→ integer
→ millisecond
→ >= 0

Freshness
→ < 5 min

Owner
→ AI Platform Team
```

Schema Contract보다 넓은 개념이다.

---

## 14.9 Governance Platforms

### Databricks Unity Catalog

큰 그림:

- Catalog / Discovery
- Access Control
- Row / Column Control
- Masking
- Classification
- Lineage
- Audit
- Data/AI Governance

Databricks Lakehouse의 중앙 Governance Layer로 이해.

### AWS Lake Formation

AWS S3 Data Lake 중심 Governance.

- Glue Data Catalog
- Table/Column/Row 권한
- AWS Analytics Service와 연계

### Snowflake Horizon Catalog

Snowflake 중심 Governance.

- Catalog
- Classification
- Tags
- Masking
- Row Access
- Access History
- Lineage
- Data Quality / AI Governance

세 제품은 결국 다음 질문을 해결한다.

```text
이 데이터는 무엇인가?
누가 Owner인가?
누가 볼 수 있는가?
민감한가?
어디서 왔는가?
어디에 쓰이는가?
누가 접근했는가?
정상인가?
```

---

# Chapter 15 — AI-Ready Data

## 15.1 What Makes Data AI-Ready

AI-Ready Data는 특정 File Format이 아니다.

> **AI가 신뢰하고 반복해서 사용할 수 있도록 품질·최신성·버전·Metadata·Governance가 갖춰진 데이터**

핵심 특성:

### Trustworthy

Data Quality.

### Fresh

충분히 최신.

### Versioned

Dataset/Prompt/Model/Agent 버전 관리.

### Discoverable

Catalog/Metadata로 찾을 수 있음.

### Governed

Access/Masking/Retention/Audit.

기존 Data Platform 기능이 AI-Ready의 기반이다.

---

## 15.2 AI Telemetry Model

AI 서비스 실행을 분석하기 위한 Telemetry.

전체 흐름:

```text
User Prompt
 ↓
Agent
 ↓
LLM Call
 ↓
Tool Call
 ↓
LLM Call
 ↓
Response
 ↓
Feedback
```

주요 수집 데이터:

### Prompt / Response

평가/개선의 기본.

### Model

Model ID/Version.

### Agent

Agent ID/Version.

### Tool Call

Tool name, input/output, latency, status.

### Latency

- total
- llm
- tool

### Token / Cost

- input tokens
- output tokens
- total cost

### Feedback

- thumbs up/down
- human label
- judge score

### Trace / Execution / Session ID

모든 이벤트를 하나의 실행 흐름으로 연결.

AI Telemetry는 단순 로그가 아니라:

- Evaluation Dataset
- Failure Analysis
- Model Comparison
- Prompt Comparison
- Regression Test
- Cost Optimization

에 활용되는 데이터 자산이다.

---

## 15.2A Langfuse as AI Telemetry / Evaluation Layer

세션 중 질문:

> Langfuse를 쓰면 되겠다.

맞다.

Langfuse는 AI Telemetry 영역을 상당 부분 담당할 수 있다.

개념 대응:

```text
Agent 실행
→ Trace

LLM Call / Tool Call
→ Observation

Conversation 묶음
→ Session

Prompt / Response
→ Input / Output

Token / Cost
→ Usage / Cost

Latency
→ Timing

User / Human / Judge 평가
→ Score

Evaluation Data
→ Dataset

변경 비교
→ Experiment
```

역할 분리:

```text
Langfuse
→ AI Telemetry
→ AI Observability
→ Evaluation

Iceberg / Data Platform
→ 장기 데이터 자산화
→ 통합 분석
→ Governance
```

권장 개념 구조:

```text
Application / Agent
   ↓
Langfuse
   ↓
Trace / Observation / Score
   ├─→ Langfuse UI
   └─→ Data Platform / Iceberg
          ↓
       Spark / dbt
          ↓
       BI / Long-term Analysis
```

Langfuse가 Data Platform 전체를 대체하는 것은 아니다.

---

## 15.3 Dataset Versioning

Evaluation Dataset은 시간에 따라 변한다.

예:

```text
eval_v1
→ 1,000 cases

eval_v2
→ 1,500 cases
→ hard cases 추가
→ 정답 수정
```

Model Score 비교에서 Dataset Version이 다르면 공정한 비교가 아닐 수 있다.

함께 기록:

- dataset_version
- model_version
- prompt_version
- agent_version
- evaluator_version
- score

Iceberg Snapshot과 Dataset Version은 동일하지 않다.

```text
Iceberg Snapshot
→ 물리적 Table 상태 버전

Dataset Version
→ AI/업무 관점의 논리적 Dataset 버전
```

---

## 15.4 Reproducibility

Reproducibility:

> **과거 AI 실험 조건을 다시 구성할 수 있는 능력**

필요:

- Dataset Version
- Model Version
- Prompt Version
- Agent Version
- Evaluator Version
- Runtime Config

예:

```text
dataset_v5
model_v3
prompt_v12
agent_v7
judge_v2
temperature=0
```

Lineage와 차이:

```text
Lineage
→ 어디서 만들어졌나?

Reproducibility
→ 동일한 실험 조건을 다시 구성할 수 있나?
```

LLM은 stochastic할 수 있으므로 재현성은 항상 동일 문장을 생성한다는 뜻이 아니라 **조건을 정확히 재구성하는 것**이 핵심이다.

---

## 15.5 Evaluation Dataset Construction

Evaluation Dataset:

> **Model/Prompt/Agent 품질을 반복적으로 평가하는 Test Dataset**

좋은 Source:

- Production Trace
- User Feedback
- 실제 Failure
- Edge Case
- Hard Case

성공 사례만 넣으면 안 된다.

포함 예:

- Normal
- Hard
- Failure
- Edge Case
- Safety
- Tool Usage

### Regression Dataset

실제 Production Bug/Failure를 수정한 뒤 해당 사례를 Dataset에 추가한다.

```text
Production Failure
 ↓
Fix
 ↓
Regression Case 추가
 ↓
이후 모든 Version에서 재평가
```

Expected Answer가 항상 필요한 것은 아니다.

Expected Behavior / Rubric도 가능.

예:

```text
올바른 Tool을 호출해야 함
권한 없는 정보 노출 금지
특정 Citation 필요
```

---

## 15.6 Embedding Data

RAG Pipeline:

```text
Source Document
 ↓
Chunk
 ↓
Embedding Model
 ↓
Vector
 ↓
Vector DB / Search
```

Vector만 저장하면 부족하다.

같이 관리:

### Document

- document_id
- document_version
- source
- owner

### Chunk

- chunk_id
- chunk_text
- chunk_index
- chunk_version
- chunking_strategy

### Embedding

- embedding_model
- embedding_model_version
- embedding_vector

Embedding Model이 바뀌면 Vector Space가 달라질 수 있으므로 Version 관리가 중요하다.

Chunk Strategy가 바뀌어도 검색 결과가 달라진다.

---

## 15.7 Retrieval Metadata

RAG Retrieval 결과에 함께 저장:

- document_id
- chunk_id
- source
- retrieval_score
- document_version
- access_level

### Access Metadata

사내 RAG에서는 권한 없는 문서를 **검색 후 숨기는 것보다 Retrieval 단계에서 제외**하는 것이 중요하다.

```text
User Permission
 ↓
Metadata Filter
 ↓
Authorized Chunks only
```

Retrieval Trace를 남기면:

```text
정답 문서를 못 가져옴
→ Retrieval Problem

정답 문서는 가져왔는데 답이 틀림
→ Generation Problem
```

으로 구분할 수 있다.

---

## 15.8 Provenance

Provenance:

> **데이터/AI 결과의 출처와 생성 과정을 넓게 추적하는 정보**

Lineage보다 더 넓게:

```text
Original Document
 ↓
Chunk
 ↓
Embedding
 ↓
Retrieval
 ↓
Model
 ↓
Response
```

까지 포함할 수 있다.

관계:

```text
Lineage
→ 데이터 이동/변환

Provenance
→ 출처와 생성 과정

Reproducibility
→ 그 조건을 다시 구성
```

Governance와 연결하면 특정 Source 사용 금지/삭제 시 파생 데이터 영향 추적에 도움이 된다.

---

## 15.9 Feature / Label Freshness

### Feature

Model 입력 데이터.

예:

- 최근 로그인 횟수
- 최근 구매
- 사용자 상태

Feature가 오래되면 Prediction 품질이 떨어질 수 있다.

### Label

Model이 맞혀야 하는 정답.

예:

```text
Feature:
최근 30일 사용량

Label:
다음 7일 내 탈퇴 여부
```

Label은 실제 결과가 확정될 때까지 지연될 수 있다.

예:

```text
구매
 ↓
30일 대기
 ↓
반품 여부 확정
 ↓
Label 생성
```

미확정 Label을 Training/Evaluation에 사용하면 왜곡될 수 있다.

LLM/Agent에서도 유사:

```text
Feature-like
→ 최신 Context / Tool State

Label-like
→ Human Feedback / Judge Score
```

---

# Chapter 16 — AI Evaluation Data Platform

## 16.1 Online Evaluation Events

Online Evaluation:

> **실제 Production에서 발생한 AI 실행에 평가 데이터를 붙이는 것**

흐름:

```text
User Request
 ↓
Agent
 ↓
LLM / Tool
 ↓
Response
 ↓
Evaluation
```

Evaluation Event 예:

- thumbs_up / thumbs_down
- rating
- user_feedback
- LLM judge score
- rule-based score
- error type

중요:

```text
score = 0.4
```

만 저장하면 부족하다.

Trace와 연결해야 한다.

함께 연결:

- trace_id
- execution_id
- model_version
- prompt_version
- agent_version
- score
- feedback

---

### User Feedback

Production Online Evaluation의 가장 단순한 형태.

```text
Response
 ↓
👍 / 👎
```

---

### Automatic Evaluation

Response 직후:

```text
LLM Judge
Rule Check
```

등으로 평가 가능.

예:

- SQL 실행 가능?
- Citation 존재?
- 금지 정보 포함?
- Output Format 준수?

---

### Langfuse 연결

개념:

```text
Langfuse Trace
 ├─ Prompt
 ├─ LLM Call
 ├─ Tool Call
 ├─ Response
 └─ Score / Feedback
```

활용:

- 낮은 Score Trace 검색
- Thumbs-down 사례 분석
- 특정 Agent Version 비교
- Production Failure → Eval Dataset 추가

Online Evaluation의 목적:

> **실제 사용자 환경의 품질을 지속 관찰**

Offline Test에서 드러나지 않는:

- 새로운 사용자 질문
- Tool 장애
- 긴 Context
- 실제 Permission
- Production Data 변화

를 관찰할 수 있다.

---

# Chapter 17 — Supplementary Clarifications

## 17.1 전체 기술 역할 맵

이 세션에서 반복적으로 연결한 역할은 다음과 같다.

```text
Applications
   ↓
Kafka
   ↓
Flink / Spark Streaming
   ↓
Iceberg Bronze
   ↓
Spark / dbt
   ↓
Silver / Gold
   ↓
Trino
   ↓
BI / Analyst / AI Evaluation
```

PostgreSQL Operational Data:

```text
PostgreSQL
   ↓
Debezium
   ↓
Kafka
```

주변 시스템:

```text
Airflow
→ Orchestration

Data Quality
→ Trust

Data Observability
→ Freshness / Volume / Drift

OpenLineage
→ Lineage Standard

Catalog
→ Discovery / Metadata

Governance
→ Access / Classification / Audit

Langfuse
→ AI Telemetry / Evaluation
```

---

## 17.2 Storage / Table / Compute / Query / Transformation 구분

```text
S3
→ Object Storage

Parquet
→ Columnar File Format

Iceberg
→ Table Format / Metadata / Snapshot

Spark
→ Large-scale Compute

Flink
→ Stateful Streaming Compute

Trino
→ Distributed SQL Query Engine

dbt
→ SQL Transformation Management

Airflow
→ Orchestration
```

이 역할 구분은 전체 Data Platform을 이해하는 핵심이다.

---

## 17.3 Data Quality vs Data Observability

### Data Quality

질문:

> 데이터가 우리가 정한 규칙을 만족하는가?

예:

- not null
- unique
- accepted values
- accuracy

### Data Observability

질문:

> 데이터 상태가 운영 중 어떻게 변하고 있으며 어디서 이상이 발생했는가?

예:

- freshness
- volume
- schema
- distribution
- anomaly
- alert

Quality Rule을 Observability가 지속적으로 관찰하는 구조로 연결할 수 있다.

---

## 17.4 Metadata / Catalog / Semantic Layer 차이

### Metadata

데이터를 설명하는 정보.

### Catalog

Metadata를 검색/탐색할 수 있는 시스템.

### Business Metadata

데이터의 업무 의미.

### Semantic Layer

Metric/Dimension 의미와 계산법을 실제 Query에 재사용 가능한 형태로 정의.

### Lineage

데이터의 생성/변환 관계.

### Governance

누가 어떻게 데이터를 사용해야 하는지에 대한 정책.

---

## 17.5 AI Observability vs General Data Platform

Langfuse 같은 AI Observability/Evaluation Tool은 다음을 잘 처리한다.

- Trace
- LLM Call
- Tool Call
- Prompt
- Response
- Token
- Cost
- Latency
- Score
- Dataset
- Experiment

하지만 장기적인:

- Enterprise Analytics
- Lakehouse Storage
- Cross-domain Join
- Data Governance
- Long-term History
- Unified Catalog

까지 모두 대체하는 것은 아니다.

권장 역할 분리:

```text
Langfuse
→ AI execution-level telemetry/evaluation

Data Platform
→ durable analytical data asset
```

---

# Chapter 18 — Current Progress and Remaining Curriculum

## 완료

- Phase 1 — Data Engineering Foundations ✅
- Phase 2 — Event Data Architecture ✅
- Phase 3 — Lakehouse / Iceberg ✅
- Phase 4 — Spark ✅
- Phase 5 — Flink ✅
- Phase 6 — CDC / Debezium ✅
- Phase 7 — Orchestration ✅
- Phase 8 — dbt ✅
- Phase 9 — Analytical Data Modeling ✅
- Phase 10 — Trino ✅
- Phase 11 — Data Quality Engineering ✅
- Phase 12 — Data Observability ✅
- Phase 13 — Lineage & Metadata Platform ✅
- Phase 14 — Data Governance ✅
- Phase 15 — AI-Ready Data ✅

## 진행 중

### Phase 16 — AI Evaluation Data Platform

완료:

- 16.1 Online Evaluation Events ✅

남은 항목:

- 16.2 Offline Evaluation Datasets
- 16.3 Human Feedback
- 16.4 Model-as-Judge Outputs
- 16.5 Prompt Versions
- 16.6 Model Versions
- 16.7 Agent Versions
- 16.8 Experiment Tracking
- 16.9 Regression Datasets
- 16.10 Cost / Quality / Latency Analysis
- 16.11 Langfuse + Iceberg Integration

---

## 이후 남은 Phase

### Phase 17 — Databricks Deep Dive

- Lakehouse Architecture
- Spark Runtime
- SQL Warehouses
- Unity Catalog
- Workflows
- Lakeflow
- Delta / Iceberg interoperability
- Lineage / Governance
- MLflow
- AI / Vector capabilities
- Cost Model
- Which self-managed components Databricks replaces

### Phase 18 — Snowflake Deep Dive

- Architecture
- Micro-partitions
- Pruning
- Clustering
- Streams
- Tasks
- Dynamic Tables
- Snowpipe
- Iceberg Tables
- Governance
- Cortex / AI capabilities
- Cost / Scaling Model

### Phase 19 — Databricks vs Snowflake vs Open Lakehouse

Compare:

- Storage Ownership
- Iceberg Openness
- Compute Model
- Streaming
- Batch
- SQL
- Governance
- Lineage
- AI Ecosystem
- Portability
- Operational Complexity
- Vendor Lock-in
- Total Cost

### Phase 20 — Production Data Platform Engineering

- Backfills
- Reprocessing
- Incident Drills
- Capacity Planning
- Cost Engineering
- DR / Recovery
- Data Platform SLOs

### Phase 21 — Final End-to-End Project

Target Architecture:

```text
Applications
    ↓
Kafka
    ↓
Flink / Spark Streaming
    ↓
Bronze Iceberg
    ↓
Spark / dbt
    ↓
Silver
    ↓
Gold
    ↓
Trino / BI / AI Evaluation

PostgreSQL
    ↓
Debezium
    ↓
Kafka
```

Around it:

```text
Airflow
→ Orchestration

Data Quality
→ Trust

OpenLineage
→ Lineage

Catalog
→ Discovery / Governance

Data Observability
→ Freshness / Correctness

Langfuse
→ AI Telemetry / Evaluation
```

최종적으로 설명할 수 있어야 할 질문:

- 왜 각 Component가 존재하는가?
- Failure 시 어떻게 동작하는가?
- Backfill은 어떻게 하는가?
- Consistency Model은 무엇인가?
- Scale은 어떻게 하는가?
- Cost는 어디서 발생하는가?
- Data Contract는 어떻게 적용하는가?
- SLO는 어떻게 정의하는가?
- Recovery는 어떻게 하는가?
- 규모가 작다면 어떤 Component를 제거할 수 있는가?

---

# Final Mental Model

이 세션 전체를 한 그림으로 압축하면 다음과 같다.

```text
                    ┌─────────────────────────┐
                    │      Applications       │
                    └────────────┬────────────┘
                                 │
                      Events / Transactions
                                 │
             ┌───────────────────┴───────────────────┐
             │                                       │
          Kafka                                  PostgreSQL
             │                                       │
             │                                    Debezium
             │                                       │
             └───────────────────┬───────────────────┘
                                 │
                         Flink / Streaming
                                 │
                         Iceberg Bronze
                                 │
                              Spark
                                 │
                          Iceberg Silver
                                 │
                               dbt
                                 │
                         Gold / Data Mart
                                 │
                              Trino
                                 │
                 BI / Analyst / AI Evaluation
```

Cross-cutting capabilities:

```text
Airflow
→ Workflow orchestration

Data Quality
→ Can we trust the data?

Data Observability
→ Is the data healthy right now?

Metadata / Catalog
→ What data exists and what does it mean?

Lineage
→ Where did it come from and where does it go?

Governance
→ Who can use it and under what policy?

Langfuse
→ What happened inside AI execution and how good was it?

AI-Ready Data
→ Can AI safely and reproducibly use this data?
```

가장 중요한 역할 구분:

```text
Kafka
→ Event Transport / Durable Log

Flink
→ Stateful Real-Time Processing

Spark
→ Large-Scale Data Processing

Parquet
→ Analytical File Format

Iceberg
→ Lakehouse Table Format

dbt
→ SQL Transformation Management

Trino
→ Interactive SQL Query

Airflow
→ Orchestration

OpenLineage
→ Lineage Standard

Catalog
→ Metadata Discovery

Governance
→ Policy / Access / Audit

Langfuse
→ AI Telemetry / Evaluation
```

이 역할 구분을 잃지 않는 것이 전체 Data Platform Architecture를 이해하는 핵심이다.
