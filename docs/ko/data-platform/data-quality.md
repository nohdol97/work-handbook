---
id: data-platform-data-quality
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-11-01
  - DPE-11-02
  - DPE-11-03
  - DPE-11-04
  - DPE-11-05
  - DPE-11-06
  - DPE-11-07
---

# Chapter 11 — Data Quality Engineering

이 장은 데이터 품질의 개념과 가상 운영 예시를 다룬다. 실제 시스템 구축이나 장애 대응을 수행했다는 뜻은 아니다. 품질은 “데이터를 믿고 사용할 수 있는가?”라는 질문이며, 서비스가 응답해도 결과가 틀리면 데이터 장애다.

<!-- SOURCE CORE START -->

## 11.1 Quality Dimensions

데이터 품질 차원은 “쓸 수 있는 데이터인가?”를 여러 질문으로 나눈 것이다. 물건을 검사할 때 수량과 내용물을 따로 보듯, `fact_llm_call`도 빠진 값·중복·형식·실제 청구액과의 일치 여부를 각각 확인한다. 한 검사에 통과해도 다른 오류는 남을 수 있다.

### Completeness

필수 값이 모두 들어 있는가.

### Uniqueness

고유해야 하는 값이 두 번 이상 들어오지 않았는가.

### Validity

값이 약속한 형식과 범위에 들어오는가.

### Consistency

관련 테이블이나 값과 서로 모순되지 않는가.

### Freshness

필요한 시각까지 데이터가 도착했는가.

### Accuracy

기록한 값이 실제 청구·사건과 맞는가.

### Volume

건수가 예상한 범위에서 크게 벗어나지 않았는가.

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

하나의 정상 지표가 다른 모든 차원을 보장하지 않는다. 형식이 유효하다고 실제 청구 금액까지 정확한 것은 아니다. 5분 freshness는 예시이며 모든 dataset의 기본 목표가 아니다.


---

## 11.2 Validation Layers

검증 계층은 데이터가 이동할 때마다 그 단계에서 알 수 있는 오류를 확인하는 방식이다. 수집 시점에는 파싱과 필수 필드를, Silver에서는 중복과 관계를, Gold에서는 업무 지표와 집계를 확인한다. 앞 단계가 성공했다고 뒤 단계의 검사가 필요 없어지는 것은 아니다.

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

Quarantine(격리 구역)은 규칙을 통과하지 못한 레코드를 조사와 재처리를 위해 따로 두는 곳이다. 배송 주소가 불분명한 소포를 버리지 않고 확인대에 보관하는 것과 같다. 잘못된 주문 하나를 조용히 버리면 나중에 누락 원인을 찾기 어렵다. 원본과 오류 이유를 보관하되 민감정보 접근과 보관 기간을 함께 제한한다.

규칙을 통과하지 못한 데이터는 버리지 않고 별도 보관한다.

```text
Incoming
 ↓
Validation
 ↙      ↘
Valid   Invalid
 ↓        ↓
Silver   Quarantine
```

격리 구역에는 조사에 필요한 정보를 남긴다:

- Raw payload
- Error type
- Error message
- Received time

등을 저장.

오류 원인을 고친 뒤 격리한 범위만 다시 처리한다.

격리 구역이 쌓이기만 해서는 안 된다. 건수와 오류 이유를 계속 확인한다.

Raw payload와 오류 메시지도 민감정보를 포함할 수 있다. 보관 범위와 접근 권한은 [거버넌스 정책](governance.md)과 함께 정한다. 이 문서에는 실제 payload가 없다.


---

## 11.4 dbt Tests

dbt의 데이터 테스트는 실제 테이블에 SQL 검사를 실행해 `not_null`이나 `unique` 같은 규칙의 위반을 찾는다. 예를 들어 `llm_call_id`의 중복을 배포 전후에 검사할 수 있다. 여기서 “정적”이라는 말은 검사 규칙이 미리 정해졌다는 뜻이지 데이터 실행 없이 코드를 읽기만 한다는 뜻이 아니다.

데이터 품질을 확인할 때 자주 쓰는 dbt 테스트:

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

원문의 “정적 검증”은 규칙이 고정되어 있다는 뜻이다. dbt data test는 실제 데이터에 SQL을 실행하며 단순한 코드 정적 분석이 아니다. 사용자 정의 SQL 검사로 비즈니스 규칙도 표현할 수 있다. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests)

기본 네 가지 검사만으로 모든 이상 탐지를 해결하지 못한다는 설명이 dbt의 freshness 검사 불가를 뜻하지는 않는다. Source freshness는 별도 기능이다. 통계적 이상 탐지에는 이력과 기준선 설계도 필요하다. [dbt source freshness](https://docs.getdbt.com/docs/deploy/source-freshness)

도구를 적용할 때 확인할 범위:

- Soda: 규칙과 연결된 데이터 source의 지원 범위.
- Great Expectations: 실행 환경과 데이터 연결 방식.
- Deequ: Spark와 해당 library version의 호환성.

제품 설명은 2026-09-24에 공식 문서로 확인한 범위를 유지했다. 이번 편집에서 새로 확인하거나 구현·우열을 시험하지 않았다. [SodaCL v3](https://docs.soda.io/soda-documentation/soda-v3/sodacl-reference/metrics-and-checks), [GX Core](https://docs.greatexpectations.io/docs/core/define_expectations/), [Deequ](https://github.com/awslabs/deequ)


---

## 11.5 Soda / Great Expectations / Deequ

Soda, Great Expectations, Deequ는 품질 규칙을 자동으로 검사하는 도구들이다. 반복해서 확인할 데이터셋이 늘어날 때 유용하지만, 도구를 고르기 전에 어떤 규칙을 어느 실행 환경에서 돌릴지 정해야 한다. 같은 결함을 여러 도구가 찾을 수 있어 기능 이름만으로 우열을 판단하지 않는다.

공통:

> **Data Quality Rule 자동 검사 도구**

### Soda

Rule/check 중심.

### Great Expectations

Expectation 기반 검증.

### Deequ

Spark 환경 대규모 Data Quality 검사에 친화적.

세 도구의 기능은 많이 겹친다. 여기서는 구현 방법보다 자동 품질 검사의 역할을 이해하는 것이 목표다.

---

## 11.6 Data Quality SLOs

SLI와 SLO를 혼동하면 측정값과 목표를 잘못 비교한다. 예를 들어 최신 이벤트가 3분 전이면 3분은 SLI이며, “5분 이내”는 이 데이터셋에 정한 SLO일 수 있다. 아래 수치는 학습용 예시이며 실제 목표는 소비자의 필요와 측정 구간에 맞춰 정한다.

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

데이터셋이 쓰이는 목적에 맞춰 SLO를 따로 정한다.

실시간 대시보드는 월간 보고서보다 더 빠른 갱신이 필요할 수 있다.

본문의 SLO 수치는 학습용 목표 예시이며 실측 결과나 승인된 운영 기준이 아니다.

운영 SLO에는 시간 기준, 측정 구간, 분모, 대상 dataset을 명시한다.

Job 성공만으로 복구를 종료하지 않는다. 재처리 범위, 중복 가능성, downstream 결과를 확인한다. [데이터 관측성](data-observability.md)은 지속적인 상태 측정을, [lineage](lineage-metadata.md)는 영향 경로 확인을 돕는다.


---

## 11.7 Incident Handling

데이터 장애는 작업 상태보다 사용자가 받는 결과로 판단한다. 예를 들어 배치가 성공해도 집계에 중복 주문이 섞였다면 먼저 전파를 막고, 원인을 고친 뒤 영향 구간만 재처리해 결과를 다시 확인한다. 이 순서는 탐지에서 재개까지 각 단계의 근거를 남기기 위해 필요하다.

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

이 흐름에서 기억할 점:

> **서비스가 살아 있어도 데이터가 틀리면 Data Incident다.**

---

<!-- SOURCE CORE END -->

## 이 장의 핵심

- 품질 차원은 각각 다른 오류를 찾는다. 정상 작업 완료와 데이터 정확성은 별도로 확인한다.
- 수집·정제·집계 단계에 맞는 검사를 두고, 실패 자료는 격리한 뒤 원인과 재처리 범위를 확인한다.
- 목표 수치와 복구 기준은 데이터셋별로 합의한다. 관측성은 이상을 발견하고 lineage는 영향을 받는 곳을 찾는 데 쓴다.

## LLM in Practice: 품질 장애의 검사 순서 검토

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    작업은 성공했으나 가상의 호출 테이블에 중복이 증가했다.
    재설계를 제안하기 전에 이 데이터 장애를 검토하세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A job succeeded, but duplicates increased in a hypothetical call table.
    Review this data incident before proposing a redesign.
    Review the material; do not apply changes.
    ```

**핵심 사항:** 원인 가설, 우선 확인할 증거, 전파 차단 선택지, 재처리와 재개 조건을 구분한 점검안이다. retry와 중복의 상관관계를 원인으로 확정하거나 deduplication 키와 grain을 잘못 가정할 수 있다. 실제 키 정의, 로그, 재처리 구간, 전후 품질 측정값과 downstream 집계를 확인한다. LLM 출력은 가설이며 운영 승인을 대신하지 않는다.

[핸드북 홈](../index.md)

[더 많은 실무 프롬프트](../prompts/data-quality.md)
