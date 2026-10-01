---
id: platform-infrastructure-litellm
status: studied
last_updated: 2026-10-01
last_reviewed: 2026-10-01
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

These are study notes from the supplied Basic Chapter 8. They do not claim that a gateway was deployed, GPUs were operated, or an external provider was called. See [Platform and infrastructure study scope](index.md) and [Kubernetes core](kubernetes-core.md) for related material.

**Reading guide:** The source core preserves the supplied sentences, numbering, diagrams, and order in translation. Read **Section supplements and corrections** for session affinity in 8.2, feature/storage conditions in 8.5–8.9, and external provider paths and bottleneck interpretation in 8.10. Configurations and numbers are hypothetical examples. They were not run or tested for response quality.

<!-- SOURCE CORE START -->

## 8.1 LiteLLM’s role

LiteLLM is an LLM gateway placed in front of multiple LLM providers and vLLM.

### Basic structure

```text
Applications
↓
LiteLLM
↓
├─ vLLM
├─ OpenAI
├─ Anthropic
└─ Other providers
```

### Main roles

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
Observability integration
```

### Difference from vLLM

```text
vLLM
= Actual model inference

LiteLLM
= Gateway / Control Layer
```

---

## 8.2 Provider Routing

> Decide which actual model / provider / deployment receives a request

### Multiple deployments of the same model

```text
qwen-32b
├─ vLLM A
├─ vLLM B
└─ vLLM C
```

### Different providers

```text
internal-chat
↓
Primary → Internal vLLM
Fallback → External Provider
```

### Routing criteria

```text
Weight
Latency
Load
Rate Limit
Cost
Custom
```

### Session Affinity

Requests in the same conversation can keep going to the same backend when possible.

---

## 8.3 Load Balancing

Distribute requests across multiple backends for the same model.

```text
LiteLLM
├─ vLLM A
├─ vLLM B
└─ vLLM C
```

With LLMs, equal request counts do not mean equal load.

```text
Request A → 1K input
Request B → 100K input
```

Therefore:

```text
Current in-flight request count
Queue
RPM / TPM
Latency
Backend Health
```

These states also matter.

### Difference from a Kubernetes Service

```text
Kubernetes Service
→ Distribute across network endpoints

LiteLLM
→ Distribute at the model / provider / replica level
→ Consider rate limits / latency / health / fallback
```

---

## 8.4 Retry / Fallback

Key concepts:

```text
Retry
Timeout
Fallback
Health-aware routing
```

### Retry

Try again after a temporary failure.

### Retry Storm

```text
Backend overload
↓
Failure
↓
More retries
↓
More overload
```

Therefore, retry limits / timeouts / backoff are needed.

### Fallback

Switch to another model/provider.

```text
GLM
↓ Failure
Qwen
↓ Failure
External Provider
```

### Retry vs Fallback

```text
Retry
= Try the same request again

Fallback
= Another backend / model / provider
```

---

## 8.5 Rate Limiting

> Limit excessive LLM usage by users/teams

Purpose: prevent noisy neighbors.

### RPM

Requests Per Minute.

### TPM

Tokens Per Minute.

With LLMs, token usage can reflect actual GPU load better than request counts.

### Concurrency Limit

Limit the number of requests processed at the same time.

### Scopes

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
= Increase capacity

Rate Limiting
= Limit incoming load
```

---

## 8.6 Budget / Quota

```text
Rate Limit
→ 100 requests per minute

Quota
→ 1 million tokens per day

Budget
→ $100 per month
```

### Token Quota

Daily/monthly token limits for each team.

### Spend Budget

Limit spending on external providers.

### Internal vLLM also needs quotas

Even without API charges:

```text
GPU purchase costs
Electricity
Operating costs
Capacity
```

These costs and constraints require fair allocation across teams.

---

## 8.7 Authentication

Authentication:

> Who made the request?

Typical method: API key.

```text
Authorization: Bearer <API_KEY>
```

### Keys for each team

```text
Team A → Key A
Team B → Key B
Service C → Key C
```

Rate limits / quotas / budgets / model access can be applied using these keys.

### Authentication vs Authorization

```text
Authentication
= Who are you?

Authorization
= What are you allowed to do?
```

Enterprise environments can integrate SSO/IAM.

---

## 8.8 Caching

> Reuse a previous response to the same LLM request

Basic flow:

```text
Request
↓
LiteLLM
↓
Cache
├─ HIT  → Respond immediately
└─ MISS → vLLM / Provider
           ↓
         Store in cache
```

### Redis

Multiple LiteLLM replicas share a cache.

```text
LiteLLM A ─┐
LiteLLM B ─┼→ Redis
LiteLLM C ─┘
```

### Exact Cache

Exactly the same request.

### Semantic Cache

Requests with similar meaning.

Watch for incorrect cache hits in agent / conversational traffic.

### Effects

```text
Latency ↓
GPU usage ↓
External API costs ↓
Throughput headroom ↑
```

---

## 8.9 LiteLLM on Kubernetes

LiteLLM works well as a stateless gateway.

### Deployment

```text
Deployment
replicas: 3
↓
LiteLLM Pod A
LiteLLM Pod B
LiteLLM Pod C
```

### Externalize state

```text
Cache → Redis
Usage / Keys / Configuration → DB / External storage
Secret → Kubernetes Secret / Secret Manager
```

### Scaling

```text
More LiteLLM load
→ More gateway pods

Longer GPU queue
→ More vLLM replicas / GPU nodes
```

Important:

```text
More LiteLLM replicas
≠
More GPU capacity
```

---

## 8.10 LiteLLM + vLLM Architecture

Overall structure:

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

### LiteLLM’s roles

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

### vLLM’s roles

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
6. Select a model pool
7. Select a vLLM replica
8. GPU Inference
9. Response
```

### Scaling layers

```text
LiteLLM Scaling
→ Gateway Capacity

vLLM Scaling
→ Serving Capacity

GPU Node Scaling
→ Compute Capacity
```

### Distinguishing bottlenecks

```text
LiteLLM CPU 100%
→ Gateway bottleneck

Longer vLLM queue
→ Insufficient serving capacity

Insufficient GPU memory
→ KV cache / model issue

GPU Utilization 100%
→ Insufficient compute capacity
```

---

<!-- SOURCE CORE END -->

## Section supplements and corrections

Official documentation was checked on 2026-10-01. LiteLLM documentation changes over time. Check the deployed version, configuration, and license before use. These conditions are outside the source and are not results of running these features here.

### 8.1 and 8.10 Correction: gateway and actual request paths

LiteLLM provides a Python SDK and a gateway (proxy). This chapter focuses on gateway deployment. The diagram in 8.10 must not imply that external LLM calls pass through local `vLLM → GPU`. Self-hosted pools route to their vLLM deployments; external providers route to their APIs. The nine source steps are explanatory, and actual paths vary by endpoint and configuration. [LiteLLM request architecture](https://docs.litellm.ai/docs/proxy/architecture)

### 8.2 and 8.3 Supplement: routing and session affinity

Having several criteria does not mean all are optimized automatically at once. Check the chosen routing strategy and its observations. Session affinity needs explicit configuration and a consistent session ID. Check shared storage when gateway replicas need to share a pin. An unhealthy backend can cause another route to be selected. Affinity does not replace conversation storage or model state replication. [LiteLLM routing](https://docs.litellm.ai/docs/routing)

### 8.4 Supplement: fallback has a separate permission boundary

The external-provider fallback in the source is a feature example, not permission to transmit data externally. Review allowed data transfers, context windows, tool formats, response quality, and cost limits first. Retries and fallbacks across multiple layers can multiply attempts. Set an overall deadline and attempt budget. These operational checks are derived from the source’s retry storm and provider switching examples.

### 8.5–8.7 Supplement: prerequisites for limits and authentication

RPM/TPM, concurrency, cumulative token quotas, and monetary budgets are different policies. Do not assume that every version has the same built-in option for the source’s daily/monthly token quotas. Check supported fields, accounting periods, enforcement, resets, and over-limit requests. Current budget documentation requires database-backed spend checks; do not expect the same budget blocking in a DB-less deployment. [LiteLLM budgets and rate limits](https://docs.litellm.ai/docs/proxy/users)

An API key identifies a caller; allowed models and team policies still need configuration. `<API_KEY>` is a placeholder, not a real credential. SSO/IAM is not one feature that automatically covers every kind of request authentication. First identify the required login, API authentication, or cloud access scope and check the relevant version and product tier.

### 8.8 and 8.9 Supplement: caching and shared state

Enable the response cache explicitly. Exact caching depends on request cache keys; semantic caching depends on embeddings and a similarity threshold. Similar meaning does not imply the same permissions, conversation, or tool state. Validate cache keys, tenant isolation, TTL/invalidation, and incorrect hits. Also distinguish response caching from provider prompt caching. [LiteLLM caching](https://docs.litellm.ai/docs/proxy/caching)

A stateless gateway does not make the whole platform stateless. Current deployment documentation uses PostgreSQL for keys, teams, usage, and configuration, and Redis for cross-replica limit counters, router state, and caches. More gateway replicas do not automatically add shared-state or GPU capacity. [LiteLLM production deployment](https://docs.litellm.ai/docs/proxy/deploy)

### 8.10 Supplement: metrics are clues to bottlenecks

`CPU 100%`, a growing queue, insufficient GPU memory, and GPU utilization are not a definitive cause table. Also inspect the observation window, input/output lengths, cache hits, retries, backend latency, and GPU memory configuration. For example, a growing queue warrants checking long requests or routing skew as well as serving capacity. This is a diagnostic principle applied to the source’s examples, not an actual performance measurement.

## LLM in Practice

### Separate gateway latency from serving bottlenecks

**Situation:** Latency has increased in a hypothetical LiteLLM service. Review the deployment first using 8.3, 8.9, 8.10, and their supplements. Check shared dependencies alongside [Kubernetes core](kubernetes-core.md).

**Context to Give the LLM:** Sanitized version, routing, limit, timeout, retry, and cache settings; DB/Redis connectivity; traces and backend metrics; permitted data transfer scope. Exclude API keys and original user conversations.

**Example Prompt:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 서비스는 LiteLLM replica 3개와 내부 vLLM pool을 사용한다.
    외부 Provider fallback은 아직 승인되지 않았다.
    버전, routing strategy, Redis/DB 연결, limits: [비식별 설정]
    관측 구간과 요청 길이, queue, latency, retry, cache hit: [관측값]
    [요청]
    구성을 먼저 검토하고 지연 증가의 원인 후보를 계층별로 나눠라.
    관측 사실, 가정, 가설, 누락 근거를 분리하라.
    Gateway와 serving capacity, rate limit과 budget을 구분하라.
    외부 Provider 호출이나 semantic cache 활성화를 승인으로 추정하지 말라.
    [출력]
    가설, 이를 가르는 조회, 기대 관측값, 중단 조건 표를 작성하라.
    현재 설정으로 보장되지 않는 한도·상태 공유를 표시하라.
    [검증]
    배포 버전 문서, trace, backend별 지표와 구성으로 대조하라.
    비밀값·원문 사용자 대화는 출력하지 말라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A hypothetical service uses 3 LiteLLM replicas and an internal vLLM pool.
    Fallback to an external provider has not been approved.
    Version, routing strategy, Redis/DB connections, limits: [sanitized configuration]
    Observation window, request lengths, queue, latency, retries, cache hits: [observations]
    [Task]
    Review the configuration first and group latency hypotheses by layer.
    Separate observations, assumptions, hypotheses, and missing evidence.
    Distinguish gateway and serving capacity, and rate limits and budgets.
    Do not assume permission for external calls or enabling semantic caching.
    [Output]
    Give a table of hypotheses, distinguishing checks, expected signals, and stop conditions.
    Mark limits or shared state that the current configuration does not guarantee.
    [Checks]
    Compare version-specific docs, traces, backend metrics, and configuration.
    Do not output secrets or original user conversations.
    ```

**Expected Output:** Hypotheses and check order for the gateway, shared stores, routing, and model backends, with safe stop conditions and remaining uncertainty.

**What the LLM Can Get Wrong:** It may infer a capacity shortage from GPU utilization alone, assume that more gateway replicas solve the GPU queue, or propose an unapproved external fallback.

**How to Validate:** A person checks actual traces, configuration, and version-specific docs. Run any load experiments separately in an approved test environment. This is an authored scenario, not a record of testing a model response or a performance improvement.
