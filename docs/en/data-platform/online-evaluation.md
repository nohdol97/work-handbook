---
id: data-platform-online-evaluation
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-16-01
---

# Online AI evaluation events

Only section 16.1 of Phase 16 was studied in the source. This page records those concepts; it does not claim a production implementation.

## 16.1 Online evaluation events

Online evaluation attaches evaluation data to real AI executions in production:

```text
User request → Agent → LLM / Tool → Response → Evaluation
```

Events may contain thumbs up/down, a rating, user feedback, an LLM judge score, a rule-based score, or an error type. A value such as `score = 0.4` is not enough by itself. Connect it to the execution with `trace_id`, `execution_id`, `model_version`, `prompt_version`, `agent_version`, `score`, and `feedback`.

### User feedback

A thumbs-up or thumbs-down response is a simple form of production evaluation: `Response → Feedback`.

### Automatic evaluation

A judge or rule check can evaluate the response. Example questions are: is the SQL executable, is a citation present, does the output contain prohibited information, and does it follow the required format?

### Langfuse connection

The conceptual trace groups the prompt, LLM calls, tool calls, response, and scores or feedback. It supports finding low-score traces, studying thumbs-down cases, comparing agent versions, and moving production failures into evaluation datasets.

The goal is to observe quality in real user conditions. Offline tests may miss new questions, tool outages, long context, actual permissions, and changes in production data.

## Limits of evaluation data

Online evaluation scores live traffic; offline evaluation compares changes on fixed inputs. Human feedback, rules, and LLM judges provide different signals. A score is not absolute truth. [Langfuse evaluation concepts](https://langfuse.com/docs/evaluation/core-concepts).

Evaluation may finish immediately or asynchronously. Record its definition, evaluator version, time, and failure or unscored status to avoid treating missing scores as success. This is a design recommendation extending the source's trace-linking principle, not an implemented or measured result. Check SQL execution in an isolated environment. Citation presence does not prove citation accuracy.

## LLM in Practice: investigate low scores

- **Situation:** A new agent version has more low-score cases.
- **Context to give:** De-identified traces, tool status, evaluation rules and versions, evaluator failure counts, before/after samples, and traffic composition.
- **Example prompt:**

```text
Inspect these low-score traces and evaluation records.
Group observed failures by retrieval, generation, tool, and permission symptoms.
Keep unscored requests separate from successful requests.
List missing evidence and the next checks for each hypothesis.
Do not execute tools or infer a root cause from the score alone.
```

- **Expected output:** Evidence-linked symptoms and next checks.
- **What can go wrong:** The LLM may mistake a judge error for an agent error or count unscored requests as healthy.
- **How to validate:** Review the original traces and evaluations, then reproduce failures in a safe environment. No runtime validation was performed here.

[AI-ready data](ai-ready-data.md) · [Study scope and remaining curriculum](curriculum.md)
