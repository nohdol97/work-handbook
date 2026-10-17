---
id: data-platform-analytical-modeling
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - DPE-09-01
  - DPE-09-02
  - DPE-09-03
  - DPE-09-04
  - DPE-09-05
  - DPE-09-06
  - DPE-09-07
  - DPE-09-08
---

# Chapter 9 — Analytical Data Modeling

이 문서는 grain, fact, dimension, metric을 학습한 기록이다. AI platform schema는 가상의 설계 예시이며 실제 사용자·조직 데이터나 구현 경험을 담지 않는다.

**분석 데이터 모델링**은 질문에 답할 수 있도록 데이터의 행 의미와 관계를 정하는 일이다. 영수증 한 줄이 상품 한 개를 뜻하는지 주문 한 건을 뜻하는지 먼저 정해야 합계를 맞출 수 있다. 아래 9.1~9.8은 그 행 단위인 grain에서 fact·dimension·metric으로 이어진다.

<!-- SOURCE CORE START -->

## 9.1 Grain

Grain은 테이블의 한 행이 무엇을 뜻하는지 정한 약속이다. 주문 한 건과 주문 상품 한 건은 다른 grain이므로, 합계를 만들기 전에 어느 행을 세는지 먼저 적는다.

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

Grain을 확인하지 않고 1건 주문을 여러 상품 행과 join하면 주문 금액을 여러 번 더할 수 있다.

Data Modeling 순서:

```text
1. Grain
2. Fact
3. Dimension
4. Metric
```

주문 1건을 여러 주문 항목과 join한 뒤 주문 금액을 다시 합산하면 금액이 반복될 수 있다. 물리 column부터 정하기 전에 한 행의 업무 의미를 합의한다. [Kimball: Grain](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/grain/)

Event/transaction 구분은 업무 설명을 위한 것이다. 모든 모델링 방법론에서 서로 배타적인 fact 분류라는 뜻은 아니다.


---

## 9.2 Fact Tables

Fact table은 측정할 사건이나 정해진 시점의 상태를 담는다. 결제 한 건과 매일의 재고 잔량은 모두 fact가 될 수 있지만 행의 grain과 갱신 방식이 다르다.

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

Dimension은 fact를 누구·무엇·언제로 나눠 볼지 설명한다. 고객 지역이 바뀌는 경우 과거 주문을 어느 지역에 집계할지 정하려면 key와 이력 규칙이 필요하다.

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

Star schema는 중앙 fact와 주변 dimension을 연결한다. 분석자가 주문 금액을 날짜와 상품별로 집계할 때 관계를 이해하기 쉽지만 각 join의 key와 grain을 확인해야 한다.

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

SCD(Slowly Changing Dimension)는 시간이 지나며 바뀌는 설명 속성을 다룬다. 고객 주소록에 새 주소만 남길지, 이사 전 주소도 날짜와 함께 남길지 정하는 것과 비슷하다. 고객 등급의 현재 값만 필요한지, 주문 당시의 등급도 필요한지에 따라 Type 1과 Type 2를 고른다.

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

Type 2는 과거 행을 보존하고 새 version을 추가한다. 분석 시점에 맞는 version을 join해야 한다. 같은 natural key의 유효 구간이 겹치면 행이 늘어날 수 있으므로 종료 경계의 의미를 명확히 한다.

OLTP는 정규화로 변경 일관성을 관리하는 경우가 많다.

Denormalization에서는 서로 다른 grain과 변경 주기가 섞이면 반복 값과 집계 오류가 생길 수 있다. 조회 편의성뿐 아니라 이력과 유지보수 비용을 비교한다.


---

## 9.6 Denormalization

Denormalization은 조회를 단순하게 하려고 일부 정보를 함께 저장하는 설계다. Join을 줄일 수 있지만 서로 다른 grain의 금액을 섞으면 같은 값을 여러 번 합산할 수 있다.

중복 저장된 값은 갱신 시 일관성을 맞춰야 한다.

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

AI 플랫폼에서도 실행 한 번과 LLM 호출 한 번은 같은 행 단위가 아니다. 한 실행에 호출이 여러 번이면 비용을 join한 뒤 다시 합산할 때 실행 비용이 반복되지 않도록 한다.

사용자 이벤트 역시 실행이나 호출과 grain이 다르다. 이 grain을 섞어 join하면 비용이나 건수가 부풀 수 있다.

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

하나의 agent 실행에 여러 LLM call이 있을 수 있다. 실행 비용을 호출과 join한 뒤 합산할 때 실행 행이 호출 수만큼 반복되는지 확인한다.

Conformed dimension을 쓰려면 공유 dimension의 의미와 key 규칙이 일관되어야 한다. `fact_user_event`의 필드는 업무별 event schema로 따로 정의한다. `user_id` 같은 이름은 schema 예시이며 실제 개인 식별값을 포함하지 않는다.


---

## 9.8 Metrics Modeling

Metric은 숫자 이름뿐 아니라 계산 범위와 규칙까지 포함한다. 오류율이라면 실패 건수와 전체 건수의 기간·대상·제외 조건을 맞춰야 서로 다른 dashboard에서도 같은 뜻이 된다.

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

Semantic layer는 여러 도구가 같은 metric을 계산하도록 분자·분모·필터·기간 같은 뜻과 규칙을 한곳에 정의한다.

예:

```text
DAU
Total Cost
Error Rate
Average Latency
```

Dashboard, Analyst, AI Agent가 동일한 정의를 사용하게 한다.

분자와 분모는 같은 기간·필터·대상 집합으로 계산한다. 분모가 0일 때의 의미도 정한다. 이름이 같아도 grain이나 제외 조건이 다르면 같은 metric이 아니다.


---

<!-- SOURCE CORE END -->

## 이 장의 핵심

모든 fact와 metric은 먼저 한 행의 의미와 계산 조건을 명시한다. Join과 이력 버전이 합계를 바꾸지 않는지 작은 예제로 확인한다.

## LLM 활용: 비용 중복 집계 검토

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    실행 비용이 호출 수에 비례해 커진다. 함께 볼 자료는 각 table의 grain, key, 관계 cardinality, join SQL, 소규모 가상 sample, metric 정의다.
    각 table에 명시된 grain을 사용해 이 비용 query를 검토해 주세요.
    각 join 이후 행 수와 중복되는 measure를 보여 주세요.
    관찰한 사실·가설·부족한 정보를 구분해 주세요.
    최소 수정안과 합계를 확인하는 작은 예시를 제안해 주세요.
    자료를 검토하되 실제 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    execution cost grows with the number of calls. Use each table's grain, keys, relationship cardinality, join SQL, a small synthetic sample, and metric definitions.
    Review this cost query using the stated grain of each table.
    Show row counts and duplicated measures after each join.
    Separate observed facts from hypotheses and missing information.
    Propose a minimal correction and a small example that checks the total.
    Review the material; do not apply changes.
    ```

**핵심 사항:** 

이 검토에서는 join에서 measure가 반복되는 위치와 검증 예시다. LLM은 `DISTINCT`로 증상을 숨기거나 다른 grain의 비용을 합칠 수 있다. 원본 grain에서 계산한 합계와 join 후 합계를 비교하고 여러 호출·0회 호출·SCD version 경계 사례를 확인한다. 이 문서는 실제 query를 실행한 기록이 아니다.

[dbt](dbt.md) · [Trino](trino.md) · [핸드북 홈](../index.md)

[관련 실무 프롬프트 6개](../prompts/analytical-modeling.md)
