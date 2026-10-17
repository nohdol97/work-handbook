---
id: platform-infrastructure-litellm
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - PIS2-08-01
  - PIS2-08-02
  - PIS2-08-03
  - PIS2-08-04
  - PIS2-08-05
  - PIS2-08-06
  - PIS2-08-07
  - PIS2-08-08
  - PIS2-08-09
  - PIS2-08-10
---

# Chapter 8. LiteLLM

예시 구성과 명령은 학습용이며 실제 배포·장애 실험 결과가 아니다.

관련: [플랫폼·인프라 학습 범위](index.md)

<!-- SOURCE CORE START -->

## 8.1 LiteLLM 역할

LiteLLM Gateway는 여러 모델 제공 경로를 연결하는 교환대와 비슷하다. 요청을 어디로 보낼지와 실제 모델 서버가 얼마나 빨리 처리하는지는 다른 문제다.

LiteLLM은 여러 LLM Provider와 vLLM 앞에 두는 LLM Gateway다.

### 기본 구조

```text
Applications
↓
LiteLLM
↓
├─ vLLM
├─ OpenAI
├─ Anthropic
└─ 기타 Provider
```

### 주요 역할

```text
Unified API
Routing
Load Balancing
Retry / Fallback
Authentication
Rate Limit
Quota / Budget
Cost Tracking
Caching
Observability 연동
```

### vLLM과 차이

```text
vLLM
= 실제 모델 Inference

LiteLLM
= Gateway / Control Layer
```

**Gateway와 실제 요청 경로**

LiteLLM은 Python SDK와 Gateway(Proxy)를 제공한다. 이 장은 Gateway 배치를 중심으로 설명한다. 8.10의 도식에서 외부 LLM 호출까지 로컬 `vLLM → GPU`를 통과한다고 읽으면 잘못이다. 자체 호스팅 pool은 해당 vLLM으로, 외부 provider는 해당 API로 갈라진다. 원문의 9단계도 설명용 순서이며 endpoint·설정에 따라 실제 경로가 달라진다. [LiteLLM request architecture](https://docs.litellm.ai/docs/proxy/architecture)

---

## 8.2 Provider Routing

> 요청을 어떤 실제 모델 / Provider / Deployment로 보낼지 결정

### 같은 모델 여러 Deployment

```text
qwen-32b
├─ vLLM A
├─ vLLM B
└─ vLLM C
```

### 서로 다른 Provider

```text
internal-chat
↓
Primary → 사내 vLLM
Fallback → External Provider
```

### Routing 기준

```text
Weight
Latency
Load
Rate Limit
Cost
Custom
```

### Session Affinity

같은 Conversation을 가능하면 같은 Backend에 계속 보낼 수 있다.

**routing과 session affinity**

여러 판단 기준이 존재한다고 모든 기준을 동시에 자동 최적화하는 것은 아니다. 선택한 routing strategy와 관측값을 확인한다. Session affinity도 명시적인 설정과 일관된 session ID가 필요하며, 여러 Gateway replica에서 같은 pin을 공유하려면 공유 저장소 구성을 확인해야 한다. 건강하지 않은 backend에는 다른 경로가 선택될 수 있다. Affinity가 대화 이력 저장이나 모델 상태 복제를 대신하지 않는다. [LiteLLM routing](https://docs.litellm.ai/docs/routing)

---

## 8.3 Load Balancing

같은 모델 Backend 여러 개에 요청 분산.

```text
LiteLLM
├─ vLLM A
├─ vLLM B
└─ vLLM C
```

LLM에서는 요청 수만 같다고 부하가 같은 게 아니다.

```text
Request A → 1K input
Request B → 100K input
```

따라서:

```text
현재 처리 요청 수
Queue
RPM / TPM
Latency
Backend Health
```

같은 상태도 중요하다.

### Kubernetes Service와 차이

```text
Kubernetes Service
→ Network Endpoint 분산

LiteLLM
→ Model / Provider / Replica 수준 분산
→ Rate Limit / Latency / Health / Fallback 고려
```

---

## 8.4 Retry / Fallback

핵심:

```text
Retry
Timeout
Fallback
Health-aware routing
```

### Retry

일시적 실패 시 다시 시도.

### Retry Storm

```text
Backend 과부하
↓
실패
↓
Retry 증가
↓
더 과부하
```

따라서 Retry 횟수 제한 / Timeout / Backoff가 필요.

### Fallback

다른 모델/Provider로 우회.

```text
GLM
↓ 실패
Qwen
↓ 실패
External Provider
```

### Retry vs Fallback

```text
Retry
= 같은 요청 재시도

Fallback
= 다른 Backend / Model / Provider
```

**fallback은 별도 허용 범위**

원문의 외부 provider fallback은 기능 예시이며 외부 전송의 승인이 아니다. 적용 전 데이터 반출 허용 범위, 모델의 context window·tool 형식·응답 품질, 비용 한도를 검토한다. Retry와 fallback을 여러 계층에서 중첩하면 시도 횟수가 증가할 수 있으므로 전체 deadline·시도 예산을 정한다. 이 항목들은 원문의 retry storm과 provider 전환에서 도출한 운영 검토 조건이다.

---

## 8.5 Rate Limiting

> 사용자/팀의 과도한 LLM 사용 제한

목적: Noisy Neighbor 방지.

### RPM

Requests Per Minute.

### TPM

Tokens Per Minute.

LLM에서는 요청 수보다 Token 사용량이 실제 GPU 부하를 더 잘 반영할 수 있다.

### Concurrency Limit

동시에 처리 가능한 요청 수 제한.

### 적용 단위

```text
User
Team
API Key
Application
Tenant
```

### Rate Limit vs Autoscaling

```text
Autoscaling
= Capacity 늘림

Rate Limiting
= 들어오는 부하 제한
```

**한도와 인증 기능의 전제**

RPM·TPM, concurrency, 누적 token quota, 금액 budget은 서로 다른 정책이다. 원문의 일간·월간 token quota 예를 모든 버전에서 같은 기본 옵션으로 설정할 수 있다고 단정하지 않는다. 실제 지원 필드·집계 기간·강제 방식·리셋과 초과 요청을 확인한다. 현재 문서의 budget 기능은 DB에 저장된 사용액을 검사하므로 DB 없는 배포에 동일한 budget 차단을 기대하지 않는다. [LiteLLM budgets and rate limits](https://docs.litellm.ai/docs/proxy/users)

API key는 식별 수단이고 허용 모델·팀 정책의 구성이 별도로 필요하다. `<API_KEY>`는 자리표시자이며 실제 credential이 아니다. SSO/IAM도 모든 종류의 요청 인증에 자동 적용되는 단일 기능이 아니다. 원하는 로그인·API 인증·클라우드 접근의 범위와 해당 버전·제품 등급을 먼저 확인한다.

---

## 8.6 Budget / Quota

```text
Rate Limit
→ 1분 100 requests

Quota
→ 하루 100만 tokens

Budget
→ 월 $100
```

### Token Quota

팀별 일간/월간 Token 한도.

### Spend Budget

외부 Provider 비용 제한.

### 내부 vLLM도 Quota 필요

API 비용이 없어도:

```text
GPU 구매 비용
전력
운영 비용
Capacity
```

가 있기 때문에 팀별 공정성 관리가 필요하다.

---

## 8.7 Authentication

Authentication:

> 누가 요청했는가?

대표: API Key.

```text
Authorization: Bearer <API_KEY>
```

### 팀별 Key

```text
Team A → Key A
Team B → Key B
Service C → Key C
```

이를 기준으로 Rate Limit / Quota / Budget / Model Access를 적용할 수 있다.

### Authentication vs Authorization

```text
Authentication
= 누구인가?

Authorization
= 무엇을 할 수 있는가?
```

기업 환경에서는 SSO/IAM과 연동할 수 있다.

---

## 8.8 Caching

> 같은 LLM 요청의 이전 응답 재사용

기본 흐름:

```text
Request
↓
LiteLLM
↓
Cache
├─ HIT  → 바로 응답
└─ MISS → vLLM / Provider
           ↓
         Cache 저장
```

### Redis

여러 LiteLLM Replica가 Cache 공유.

```text
LiteLLM A ─┐
LiteLLM B ─┼→ Redis
LiteLLM C ─┘
```

### Exact Cache

완전히 같은 요청.

### Semantic Cache

의미가 비슷한 요청.

Agent / 대화형 traffic에서는 잘못된 Cache Hit에 주의.

### 효과

```text
Latency ↓
GPU 사용량 ↓
외부 API 비용 ↓
Throughput 여유 ↑
```

**cache와 공유 상태**

Response cache는 명시적으로 활성화해야 한다. Exact cache는 요청의 cache key, semantic cache는 embedding과 유사도 기준에 의존한다. 의미가 비슷하다는 이유만으로 권한·대화·tool 상태까지 같은 것은 아니므로 cache key와 tenant 격리, TTL·무효화, 부정확한 hit를 검증한다. Response cache와 provider의 prompt cache도 구분한다. [LiteLLM caching](https://docs.litellm.ai/docs/proxy/caching)

Stateless Gateway는 플랫폼 전체에 상태가 없다는 뜻이 아니다. 현재 배포 문서는 PostgreSQL에 key·team·사용량·설정을, Redis에 replica 간 limit counter·router·cache 상태를 두는 구성을 설명한다. Gateway replica 수만 늘려도 공유 상태나 GPU capacity가 자동으로 늘어나지는 않는다. [LiteLLM production deployment](https://docs.litellm.ai/docs/proxy/deploy)

---

## 8.9 LiteLLM on Kubernetes

LiteLLM은 Stateless Gateway로 운영하기 좋다.

### Deployment

```text
Deployment
replicas: 3
↓
LiteLLM Pod A
LiteLLM Pod B
LiteLLM Pod C
```

### 상태 외부화

```text
Cache → Redis
Usage / Key / 설정 → DB / 외부 저장소
Secret → Kubernetes Secret / Secret Manager
```

### Scaling

```text
LiteLLM 부하 증가
→ Gateway Pod 증가

GPU Queue 증가
→ vLLM Replica / GPU Node 증가
```

중요:

```text
LiteLLM Replica 증가
≠
GPU Capacity 증가
```

---

## 8.10 LiteLLM + vLLM Architecture

전체 구조:

```text
Applications
↓
Load Balancer
↓
LiteLLM Replicas
↓
├─ Qwen Pool
├─ GLM Pool
└─ External LLM
↓
vLLM
↓
GPU
```

### LiteLLM 역할

```text
Authentication
Authorization
Routing
Load Balancing
Retry
Fallback
Rate Limit
Quota / Budget
Caching
```

### vLLM 역할

```text
Model Weight Loading
GPU Inference
KV Cache
PagedAttention
Continuous Batching
Token Generation
```

### Request Flow

```text
1. Request
2. Authentication
3. Authorization
4. Rate Limit / Quota
5. Cache
6. Model Pool 선택
7. vLLM Replica 선택
8. GPU Inference
9. Response
```

### Scaling 계층

```text
LiteLLM Scaling
→ Gateway Capacity

vLLM Scaling
→ Serving Capacity

GPU Node Scaling
→ Compute Capacity
```

### 병목 구분

```text
LiteLLM CPU 100%
→ Gateway 병목

vLLM Queue 증가
→ Serving 부족

GPU Memory 부족
→ KV Cache / Model 문제

GPU Utilization 100%
→ Compute 부족
```

**지표는 병목의 증거 후보**

`CPU 100%`, queue 증가, GPU memory 부족, GPU utilization은 원인 확정표가 아니다. 관측 구간과 요청의 input/output 길이, cache hit, retry, backend별 latency, GPU 메모리 구성을 함께 본다. 예를 들어 queue 증가는 serving capacity 부족뿐 아니라 긴 요청이나 routing 편중도 조사할 이유가 된다. 이것은 원문 병목 예에 대한 진단 원칙이며 실제 성능 측정 결과가 아니다.

---

<!-- SOURCE CORE END -->

## 핵심 정리

LiteLLM은 요청을 모델 제공 경로로 연결한다. 라우팅, 인증, 비용과 실패 처리를 모델 서버 동작과 구분한다.

## LLM in Practice
### Gateway 지연과 serving 병목 분리

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    LiteLLM Gateway의 지연·오류·비용이 늘었어. 요청 trace와 routing·retry·cache 설정을 보고 Gateway, 공유 저장소, 내부 vLLM, 외부 API 중 병목 후보를 구분해 줘. 비밀값을 출력하거나 설정을 변경하지 마.
    ```

=== "English"

    ```text {.prompt}
    LiteLLM Gateway latency, errors, and cost increased. Use request traces and routing, retry, and cache settings to separate gateway, shared-store, internal vLLM, and external API bottlenecks. Do not reveal secrets or change settings.
    ```

**핵심 사항:** Gateway·저장소·router·backend별 병목/비용 근거표와 retry·limit·cache 설정 PR 검토 의견. Gateway 증설을 GPU queue 해결로 보거나 외부 fallback·semantic cache를 자료 없이 활성화하라고 제안할 수 있다. 같은 요청의 전체 시도 횟수·trace 구간·token 비용을 연결하고 budget 저장소·cache 격리·fallback 허용 근거를 확인한다. backend queue를 Gateway 증설로 해결한다고 단정한 답변은 재검토한다.

관련: [Kubernetes 핵심](kubernetes-core.md)
