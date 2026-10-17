---
id: data-platform-foundations
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-01-01
  - DPE-01-02
  - DPE-01-03
  - DPE-01-04
  - DPE-01-05
  - DPE-01-06
  - DPE-01-07
---

# Chapter 1 — Data Engineering Foundations

데이터 플랫폼을 처음 볼 때는 주문을 처리하는 계산대와 하루 매출을 살피는 장부를 떠올리면 된다. **OLTP**는 개별 거래를 빠르게 기록하는 처리 방식이고, **OLAP**는 많은 기록을 묶어 분석하는 방식이다. 아래 1.1~1.7은 분석 목적에 따라 저장 형식과 파일 배치를 고르는 흐름으로 읽는다.

<!-- SOURCE CORE START -->

## 1.1 OLTP vs OLAP

서비스는 주문 한 건을 즉시 저장하고, 분석가는 여러 달의 주문을 한꺼번에 살핀다. 이 차이 때문에 거래 처리(OLTP)와 분석 처리(OLAP)는 저장 방식과 성능 목표가 다르다.

### OLTP

OLTP는 **Online Transaction Processing**의 약자다.

서비스에서 회원가입이나 결제처럼 한 번에 적은 기록을 빠르고 정확하게 처리할 때 쓴다.

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

많은 기록을 모아 추세나 합계를 알아볼 때 쓴다.

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

Row는 한 기록의 값을 함께 두고, column은 같은 항목의 값을 모아 둔다. 한 고객의 전체 정보를 찾을 때와 모든 주문의 금액만 합산할 때 필요한 읽기 방식이 다르기 때문에 이 구분이 중요하다.

### Row-Oriented

Row 기반 저장은 한 사람의 이름·나이·팀처럼 한 기록의 값을 가까이 둔다.

개념적으로:

```text
Row 1: user_id, name, age, team
Row 2: user_id, name, age, team
```

OLTP에서 유리하다.

예를 들어 사용자 한 명의 모든 정보를 읽는다면 row 단위 저장이 자연스럽다.

---

### Column-Oriented

Column 기반 저장은 여러 기록의 같은 항목을 모아 둔다. 분석에서 그 항목만 읽기 좋다.

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

<!-- INLINE ADDITION COMPRESSION START -->

#### 대표 압축 기술 (추가 설명) {#compression-techniques}

[Compression](#compression)과 [Encoding / Compression](#encoding-compression)에 등장하는 대표 기술은 다음과 같다. 앞의 네 가지는 값의 표현을 줄이는 **인코딩**, 마지막은 인코딩한 바이트를 압축하는 **코덱**이다.

- **RLE (Run-Length Encoding):** 연속된 같은 값을 값과 반복 횟수로 표현한다. 개념적으로 `A,A,A,B,B → (A,3),(B,2)`다.
- **Dictionary Encoding:** 중복 값을 사전에 한 번 저장하고 각 값은 작은 정수 ID로 표현한다. 값 종류가 적은 column에 유리하다.
- **Delta Encoding:** 첫 값과 이후 값 사이의 차이를 저장한다. 개념적으로 `100,101,102 → 100,+1,+1`이다.
- **Bit packing:** 작은 정수를 필요한 비트 수로 묶는다. 예를 들어 `0~7`은 값당 3비트로 표현할 수 있다.
- **Snappy·LZ4·Zstandard(Zstd)·Gzip:** 바이트를 무손실 압축하는 코덱이다. Parquet의 LZ4는 구형 `LZ4` 대신 `LZ4_RAW` 표기를 확인한다.

Parquet은 인코딩과 코덱을 조합할 수 있다. 압축률과 CPU 비용은 데이터·설정에 따라 달라진다. 위 예시는 실제 파일 바이트가 아닌 개념 표기다. [공식 인코딩 설명](https://parquet.apache.org/docs/file-format/data-pages/encodings/), [공식 압축 코덱 설명](https://parquet.apache.org/docs/file-format/data-pages/compression/) — 확인일: 2026-10-06.

<!-- INLINE ADDITION COMPRESSION END -->

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

대량 분석에서는 읽을 데이터량이 성능에 큰 영향을 준다. Parquet을 사용하는 이유는 필요한 column과 저장 단위만 골라 I/O를 줄이기 위해서다.

Parquet은 값을 열(column)별로 묶어 저장하는 대표적인 분석용 파일 형식이며, 데이터베이스처럼 쿼리를 직접 실행하지는 않는다.

역할:

> **대량 분석 데이터를 효율적으로 저장하는 파일 포맷**

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

Parquet에는 row group이나 page의 최솟값·최댓값 같은 통계가 있을 수 있다. Reader가 이를 사용하면 조건에 맞지 않는 단위를 건너뛸 수 있다.

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

Object storage는 데이터를 파일 같은 object로 오래 보관하는 서비스다. 계산 엔진과 별도로 유지할 수 있어 같은 분석 파일을 Spark나 Trino가 읽는 구조에 자주 쓴다.

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

같은 데이터량이라도 파일이 아주 많거나 너무 크면 읽기와 재작성 비용이 달라진다. 따라서 파일 배치는 저장 공간뿐 아니라 쿼리 계획, 병렬 처리, 유지보수까지 고려하는 설계다.

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

Partition은 데이터를 날짜처럼 자주 거르는 기준으로 나눈 단위다. 서류를 월별 서랍에 넣으면 필요한 달만 열 수 있지만, 사람마다 서랍을 하나씩 만들면 서랍 관리가 더 어려워지는 것과 같다. 필요한 날짜만 찾을 수 있지만 너무 잘게 나누면 작은 파일과 metadata가 늘 수 있으므로 쿼리 패턴을 보고 정한다.

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

Partition으로 큰 범위를 줄인 뒤에도 파일 안에 값이 흩어져 있으면 많이 읽을 수 있다. Bucketing, sorting, clustering은 값을 배치해 읽기나 join을 돕는 방법이며 효과는 엔진과 쿼리 조건에 따라 확인해야 한다.

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

<!-- SOURCE CORE END -->

## 연결해서 읽기

[이벤트 아키텍처](event-architecture.md), [Iceberg](lakehouse-iceberg.md), [Spark](spark.md).

## 이 장의 핵심

거래 처리와 분석의 읽기 패턴이 다르므로 저장 형식·partition·파일 크기를 함께 설계한다. 최적화 효과는 실제 쿼리의 읽기량, 실행 계획, 비용으로 확인한다.

## LLM 실전: 파일 배치 검토

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    작은 파일이 많고 날짜 필터 쿼리가 느린 가상 사례다.
    변경 제안 전에 현재 파일 배치를 검토하고 compaction·partition·정렬 후보를 비교해 줘.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A hypothetical workload has many small files and slow date-filtered queries.
    Review the current file layout before suggesting changes.
    Compare compaction, partition changes, and sorting.
    Review the material; do not apply changes.
    ```

**핵심 사항:** 비용 원인 후보, 선택지별 trade-off, 측정 계획이다. 작은 파일만을 원인으로 단정하거나 보편적인 목표 크기를 만들 수 있다. 동일 쿼리·동일 입력에서 planning time, scan bytes, task 분포를 비교한다.

[이 주제의 실무 프롬프트 6개 더 보기](../prompts/foundations.md)

LLM 출력은 작업 가설이다. 공식 문서와 실제 설정·로그·측정으로 검증한다. 외부 문서 확인일: 2026-09-24. 구현 버전을 시험했다는 의미는 아니다.

## 적용 시 보완할 점

위 설명은 저장 구조를 이해하기 위한 기본 모델이다. PostgreSQL에서 분석계를 분리하는 기준을 row 수 하나로 정하지 않는다. 실제 쿼리, 트랜잭션 영향, 비용과 응답 시간으로 판단한다. Object Storage 비용에도 요청·전송 비용이 포함되며 공급자와 workload에 따라 달라진다.

Parquet의 column chunk는 row group 내부에 있다. 통계나 page index의 존재와 이를 사용하는 reader에 따라 pruning 효과가 달라진다. Predicate pushdown은 필터를 하위 처리 계층으로 전달하는 것이고, pruning은 일치할 수 없는 저장 단위를 건너뛰는 것이다. row index처럼 임의의 row만 바로 찾는 기능으로 이해하지 않는다. Encoding과 compression도 서로 다른 단계다. [Apache Parquet 파일 형식](https://parquet.apache.org/docs/file-format/)

큰 Parquet 파일도 여러 scan split으로 나뉠 수 있으므로 파일 하나와 task 하나를 항상 같다고 보면 안 된다. 목표 파일 크기는 병렬성·재작성 비용·요청 비용을 함께 보고 정한다. Bucket 예시는 개념 표기이며 실제 인수 순서와 SQL 문법은 엔진마다 확인한다. Iceberg transform의 개념 표기는 `bucket(32, user_id)`다.

### 1.3·1.6 보완: 통계와 cardinality

원문 [1.3](#13-parquet)의 “필요한 row 범위만”은 위에서 설명한 row group 등 저장 단위의 pruning을 뜻한다.

Cardinality는 서로 다른 값의 개수다. 날짜 partition의 day/hour 세분화도 실제 데이터 양과 query pattern에 맞춰 정한다.
