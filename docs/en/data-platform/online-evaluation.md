---
id: data-platform-online-evaluation
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - DPE-16-01
  - DPE2-16-01
---

# Chapter 16 — AI Evaluation Data Platform

The first source studied only section 16.1 of Phase 16. The added source extends that material. This page records the concepts in 16.1; it does not claim a production implementation. Continue with sections 16.2–16.12 in [AI evaluation data platform](ai-evaluation.md).


The core below preserves section 16.1 of the latest complete source. The earlier Langfuse explanation and evaluation conditions remain in the separate supplement.

**Reading note:** The source core below keeps the original order and form. Read the section-specific corrections, conditions, and additions in the supplement after the source material; some original statements are simplified.

<!-- SOURCE CORE START -->

## 16.1 Online Evaluation Events

Online Evaluation means:

> **Evaluating AI executions that actually happened in production and attaching evaluation data to those traces.**

Basic flow:

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

Possible evaluation events:

```text
thumbs_up / thumbs_down
rating
user_feedback
llm_judge_score
rule_based_score
error_type
```

A score alone is not enough.

Bad:

```text
score = 0.4
```

Better:

```text
trace_id
execution_id
agent_version
prompt_version
model_version
score
feedback
```

This allows the platform to answer:

```text
Why was this response bad?
Which prompt was used?
Which model generated it?
Which tools were called?
Which agent release produced it?
```

### User feedback

The simplest online evaluation is:

```text
Response
  ↓
👍 / 👎
```

More detailed forms may include:

```text
rating = 1~5
reason = inaccurate
comment = "wrong tool was selected"
```

### Automatic evaluation

Production responses can also be evaluated automatically.

```text
Response
 ↓
LLM Judge
 ↓
Score
```

or:

```text
Response
 ↓
Rule Check
 ↓
Pass / Fail
```

Checks may include:

- Is generated SQL executable?
- Is a required citation present?
- Does the output contain prohibited information?
- Does the response follow the expected schema?
- Did the agent call the correct or authorized tool?

Core idea:

> **Online Evaluation tells us how the AI behaves under real production conditions.**

Offline tests can miss:

- new user behavior,
- changing data,
- tool failures,
- long context,
- permissions,
- production-only edge cases.

---

<!-- SOURCE CORE END -->

## Supplement: 16.1 Langfuse links and evaluation conditions

### Langfuse connection from the earlier source

Concept:

```text
Langfuse Trace
 ├─ Prompt
 ├─ LLM Call
 ├─ Tool Call
 ├─ Response
 └─ Score / Feedback
```

Uses:

- Find traces with low scores.
- Investigate thumbs-down cases.
- Compare specific agent versions.
- Add production failures to evaluation datasets.

The goal of online evaluation:

> **Continuously observe quality under real user conditions.**

Offline tests may miss:

- new user questions,
- tool failures,
- long context,
- actual permissions,
- changes in production data.

---

**Tool evaluation conditions:** Expected schema compliance and tool authorization are separate checks. Check both whether the selected tool is appropriate and whether its use is authorized. A score does not prove the root cause.

Online evaluation scores live traffic; offline evaluation compares changes on fixed inputs. Human feedback, rules, and LLM judges provide different signals. A score is not absolute truth. [Langfuse evaluation concepts](https://langfuse.com/docs/evaluation/core-concepts).

Evaluation may finish immediately or asynchronously. Record its definition, evaluator version, time, and failure or unscored status to avoid treating missing scores as success. This is a design recommendation extending the source's trace-linking principle, not an implemented or measured result. Check SQL execution in an isolated environment. Citation presence does not prove citation accuracy.

## LLM in Practice: investigate low scores

- **Situation:** A new agent version has more low-score cases.
- **Context to give:** De-identified traces, tool status, evaluation rules and versions, evaluator failure counts, before/after samples, and traffic composition.
- **Example prompt:**

=== "English"

    ```text {.prompt}
    [Context]
    Low-score traces and evaluation records: [sanitized samples]
    Tool state, evaluation rules, versions, and evaluator failure counts: [material]
    Before/after samples and traffic mix: [comparison windows]
    [Task]
    Group observed failures by retrieval, generation, tool, and permission symptoms.
    Keep unscored requests separate from successful requests.
    [Output]
    List missing evidence and the next checks for each hypothesis.
    Link symptoms to the related traces and evaluation evidence.
    [Checks]
    Do not execute tools or infer a root cause from the score alone.
    Compare original traces and evaluations and draft a safe reproduction plan.
    Separate judge errors from agent errors; do not claim checks were run.
    ```

=== "한국어"

    ```text {.prompt}
    [맥락]
    낮은 점수 trace와 평가 기록: [비식별 표본]
    tool 상태·평가 규칙·버전·평가 실패 수: [자료]
    전후 표본·traffic 구성: [비교 구간]
    [요청]
    retrieval·generation·tool·permission 증상별로 관측 실패를 묶으세요.
    미평가 요청을 성공 요청과 구분하세요.
    [출력]
    각 가설의 누락 근거와 다음 확인을 나열하세요.
    증상에 해당 trace와 평가 근거를 연결하세요.
    [검증]
    tool을 실행하거나 점수만으로 근본 원인을 추론하지 마세요.
    원본 trace·평가를 대조하고 안전한 재현 계획을 적으세요.
    judge 오류와 agent 오류를 구분하고 실행했다고 주장하지 마세요.
    ```

- **Expected output:** Evidence-linked symptoms and next checks.
- **What can go wrong:** The LLM may mistake a judge error for an agent error or count unscored requests as healthy.
- **How to validate:** Review the original traces and evaluations, then reproduce failures in a safe environment. No runtime validation was performed here.

[AI-ready data](ai-ready-data.md) · [Study scope and remaining curriculum](curriculum.md)

[More practical prompts](../prompts/online-evaluation.md)
