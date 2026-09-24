---
id: data-platform-ai-ready-data
status: studied
last_updated: 2026-09-24
last_reviewed: 2026-09-24
knowledge_ids:
  - DPE-15-01
  - DPE-15-02
  - DPE-15-02A
  - DPE-15-03
  - DPE-15-04
  - DPE-15-05
  - DPE-15-06
  - DPE-15-07
  - DPE-15-08
  - DPE-15-09
---

# AI-ready data

This page organizes the concepts from source Chapter 15. `studied` means conceptual study, not a deployed or tested system. Version names and numbers below are examples.

## 15.1 What makes data AI-ready

AI-ready data is not a file format. It has the quality, freshness, versions, metadata, and governance needed for repeated, trusted AI use.

| Property | Meaning |
|---|---|
| Trustworthy | Data quality is checked. |
| Fresh | Data is recent enough for its use. |
| Versioned | Dataset, prompt, model, and agent versions are recorded. |
| Discoverable | Catalogs and metadata help people find it. |
| Governed | Access, masking, retention, and audit policies apply. |

Existing data platform capabilities provide this foundation.

## 15.2 AI telemetry model

A typical flow is `User prompt → Agent → LLM call → Tool call → LLM call → Response → Feedback`.

Record the following fields when policy permits:

- Prompt and response for evaluation and improvement.
- Model ID/version and agent ID/version.
- Tool name, input, output, latency, and status.
- Total, LLM, and tool latency.
- Input tokens, output tokens, and total cost.
- Thumbs up/down, human labels, and judge scores.
- Trace, execution, and session IDs to connect related events.

Telemetry supports evaluation datasets, failure analysis, model and prompt comparisons, regression tests, and cost optimization. It is a reusable data asset.

## 15.2A Langfuse as the telemetry and evaluation layer

Study question: can Langfuse handle AI telemetry? The concepts map as follows, but actual coverage depends on instrumentation and integrations.

| Application concept | Langfuse concept |
|---|---|
| Agent execution | Trace |
| LLM or tool call | Observation |
| Related conversations | Session |
| Prompt and response | Input and output |
| Tokens and cost | Usage and cost |
| Latency | Timing |
| User, human, or judge evaluation | Score |
| Evaluation data | Dataset |
| Comparing changes | Experiment |

Langfuse covers AI telemetry, observability, and evaluation. An Iceberg-based data platform supports durable data assets, combined analytics, and governance. Langfuse does not replace the entire data platform.

This is a learning design, not a tested integration:

```text
Application / Agent
  → Langfuse
  → Trace / Observation / Score
      ├→ Langfuse UI
      └→ Data Platform / Iceberg
           → Spark / dbt
           → BI / Long-term Analysis
```

## 15.3 Dataset versioning

An evaluation dataset changes over time. For example, `eval_v1` has 1,000 cases, while `eval_v2` has 1,500 cases, extra hard cases, and corrected answers. Scores from different dataset versions may not be comparable.

Record `dataset_version`, `model_version`, `prompt_version`, `agent_version`, `evaluator_version`, and `score` together.

An Iceberg snapshot describes a consistent set of files referenced by table metadata. A dataset version describes a logical dataset for AI or business use. These are not the same identifier or boundary.

## 15.4 Reproducibility

Reproducibility means rebuilding the conditions of a past AI experiment. Preserve the dataset, model, prompt, agent, and evaluator versions, plus runtime configuration. Example:

```text
dataset_v5
model_v3
prompt_v12
agent_v7
judge_v2
temperature=0
```

Lineage asks where the data came from. Reproducibility asks whether the experiment conditions can be restored. An LLM can be stochastic; restoring conditions does not promise identical sentences.

## 15.5 Building evaluation datasets

An evaluation dataset repeatedly tests a model, prompt, or agent. Useful sources include production traces, user feedback, actual failures, edge cases, and hard cases. Include normal, hard, failure, edge, safety, and tool-use cases. Success cases alone are not enough.

A regression loop is `Production failure → Fix → Add regression case → Evaluate later versions`.

A case need not have one exact expected answer. It may define expected behavior or a rubric: call the correct tool, avoid unauthorized disclosure, or include a required citation.

## 15.6 Embedding data

A RAG pipeline often follows `Source document → Chunk → Embedding model → Vector → Vector DB / Search`. Vectors alone are not enough.

| Entity | Fields to retain |
|---|---|
| Document | `document_id`, `document_version`, `source`, `owner` |
| Chunk | `chunk_id`, `chunk_text`, `chunk_index`, `chunk_version`, `chunking_strategy` |
| Embedding | `embedding_model`, `embedding_model_version`, `embedding_vector` |

A model change can change the vector space. A chunking change can change retrieval results. Track both.

## 15.7 Retrieval metadata

Record `document_id`, `chunk_id`, `source`, `retrieval_score`, `document_version`, and `access_level` with retrieved results.

For enterprise RAG, exclude unauthorized documents during retrieval, before content reaches the model: `User permission → Metadata filter → Authorized chunks only`.

Retrieval traces help separate two failures. If the correct document was not retrieved, investigate retrieval. If it was retrieved but the answer is wrong, investigate generation.

## 15.8 Provenance

Provenance tracks sources and how data or AI output was produced. Its scope can include `Original document → Chunk → Embedding → Retrieval → Model → Response`.

Lineage describes data movement and transformation. Provenance records origin and production context more broadly. Reproducibility restores those conditions. Together with governance, they help trace affected outputs when a source must be deleted or cannot be used.

## 15.9 Feature and label freshness

A feature is model input, such as recent logins, purchases, or user state. Stale features can reduce prediction quality.

A label is the outcome to predict. For example, features describe the last 30 days of use, while the label states whether the user leaves within the next 7 days. Some labels arrive late: `Purchase → Wait 30 days → Return outcome confirmed → Label created`.

Using an unconfirmed label can distort training and evaluation. For LLMs and agents, current context and tool state play a feature-like role; human feedback and judge scores play a label-like role.

## Verified scope and qualifications

A trace groups a request or operation. An observation is a step such as an LLM call, tool call, or retrieval. A session groups traces. Do not infer physical storage from this conceptual diagram. [Langfuse data model](https://langfuse.com/docs/observability/data-model).

Changes to Langfuse dataset items create timestamp-based versions; schema changes are outside that versioning scope. Preserve the schema and evaluation settings as well as the input version. [Langfuse datasets](https://langfuse.com/docs/evaluation/experiments/datasets).

Access metadata alone does not enforce access. Derive permissions from a trusted identity and check every search request. Prompts, responses, and tool inputs/outputs can also contain sensitive data, so define collection, masking, and retention rules. Hiding a result only in the UI after sending it to an LLM does not prevent disclosure. [Azure AI Search security filters](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search).

## LLM in Practice: compare evaluation conditions

- **Situation:** Scores differ between two agent versions.
- **Context to give:** De-identified experiment metadata; dataset, model, prompt, agent, and evaluator versions; runtime settings; sample sizes; and failure cases.
- **Example prompt:**

```text
Compare these two experiment records.
List changed conditions and missing version metadata.
Separate observed score changes from possible causes.
Do not claim that a model change caused the difference.
Suggest a controlled comparison using the same dataset and evaluator.
```

- **Expected output:** Changed conditions, missing evidence, and a controlled comparison plan.
- **What can go wrong:** The LLM may blame the model for a score change or treat temperature=0 as fully deterministic.
- **How to validate:** Inspect actual dataset items, settings, and traces. Repeat evaluations under the same conditions. No experiment was run for this page.

## Related topics

[Online evaluation](online-evaluation.md) · [Governance](governance.md) · [Lineage and metadata](lineage-metadata.md) · [Architecture](architecture.md)
