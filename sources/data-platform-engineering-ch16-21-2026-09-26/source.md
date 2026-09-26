<!-- 반입 기록
범위: 업로드 Markdown 전체 1~5480행, Chapters 16~21·완료 현황·원칙·공식 근거 메모.
읽기: 영역별 담당자의 전체 읽기·개인정보 검토 완료. 접근하지 못한 본문 및 발견된 실제 민감정보 없음.
한계: 개념 학습 자료이며 실제 구축·장애 실험·제품 버전 테스트 기록이 아님.
원본 bytes: 72467; SHA-256: b28c7d4792c3e51b5a4dc19898cedf81047ea47d5c051ef8be1d1bed901a1e9b
정규화: 아래 ledger의 행 끝 공백만 제거하며, 경계 뒤 본문에 복원하면 업로드와 동일.
whitespace_restoration: [{"line": 3348, "removed": "  "}]
-->
<!-- ORIGINAL SOURCE START -->
# Data Platform Engineering Study Session — Source Markdown (Chapters 16–21)

> **Purpose**
>
> This file continues the previously extracted source markdown. Chapters 1–15 were already extracted, so this document intentionally starts at **Chapter 16**.
>
> It contains:
>
> - All learning content covered in this session from Chapter 16 onward
> - Supplementary questions and clarifications raised during the session
> - The Databricks and Snowflake material covered in the session
> - Completed Chapter 19, 20, and 21 material so the curriculum can be considered finished
>
> **Learning style**
>
> This study session focused on understanding why a technology exists, what role it plays, how it connects to other parts of a Data Platform, and when it is or is not necessary. It intentionally avoided going too deep into implementation details.

---

# Current Curriculum Completion

Completed:

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
- Phase 16 — AI Evaluation Data Platform ✅
- Phase 17 — Databricks Deep Dive ✅
- Phase 18 — Snowflake Deep Dive ✅
- Phase 19 — Databricks vs Snowflake vs Open Lakehouse ✅
- Phase 20 — Production Data Platform Engineering ✅
- Phase 21 — Final End-to-End Architecture ✅

The study session is now complete.

---

# Chapter 16 — AI Evaluation Data Platform

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

## 16.2 Offline Evaluation Datasets

Offline Evaluation means:

> **Running a fixed evaluation dataset against different Prompt / Model / Agent versions so they can be compared under the same conditions.**

Example:

```text
Evaluation Dataset v5

Case 1
→ normal request

Case 2
→ tool usage request

Case 3
→ permission violation attempt

Case 4
→ difficult RAG request

Case 5
→ known production regression
```

Then:

```text
Dataset v5
  ↓
Agent v10
  ↓
Scores
```

and:

```text
Dataset v5
  ↓
Agent v11
  ↓
Scores
```

Because the dataset is fixed, the comparison is much fairer than comparing different production traffic windows.

### Dataset fields may include

```text
input
expected_output
expected_behavior
expected_tool
rubric
category
difficulty
metadata
```

For agent evaluation, a single exact answer is often not enough.

Example:

```text
Input:
"Show last week's AI cost by team."

Expected behavior:
- call analytics tool
- use authorized dataset
- aggregate by team
- do not expose user-level PII
```

### Category-based evaluation

Useful categories:

```text
General
Tool Usage
RAG
Security
Complex Reasoning
Edge Cases
Regression
```

Instead of only:

```text
Overall Score = 88%
```

also inspect:

```text
General       = 95%
Tool Usage    = 91%
RAG           = 84%
Security      = 100%
Regression    = 70%
```

This makes regression diagnosis easier.

### Online and offline form a loop

```text
Production
   ↓
Online Evaluation
   ↓
Failure discovered
   ↓
Add to Offline Dataset
   ↓
Evaluate new version
   ↓
Deploy
   ↓
Production
```

Important pattern:

> **Production Failure → Offline Regression Case**

---

## 16.3 Human Feedback

Human Feedback means:

> **A human directly evaluates an AI response and produces quality data.**

### Simple feedback

```text
👍
👎
```

Useful for:

- identifying poor traces,
- building failure datasets,
- prioritizing human review.

### Ratings

```text
accuracy    = 4/5
helpfulness = 5/5
relevance   = 3/5
```

### Expert labeling

For specialized or high-stakes domains, experts may review:

```text
technical correctness
tool selection
policy compliance
citation quality
domain-specific accuracy
```

### Rubrics

Instead of asking "Is this answer good?", define a rubric:

```text
Accuracy       0~2
Relevance      0~2
Groundedness   0~2
Tool Selection 0~2
Format         0~2
```

This improves consistency.

### Human feedback is not perfect

Different reviewers can disagree:

```text
Reviewer A → 5
Reviewer B → 3
```

This introduces the concept of **inter-rater agreement**.

The main point:

> Human labels are useful, but they are also noisy data and should be managed accordingly.

### Production feedback loop

```text
Production Trace
   ↓
Thumbs Down
   ↓
Human Review
   ↓
Failure Label
   ↓
Regression Dataset
```

Possible labels:

```text
wrong_tool_selection
hallucination
retrieval_failure
permission_violation
bad_format
```

---

## 16.4 Model-as-Judge Outputs

Model-as-Judge means:

> **Using another LLM as an evaluator of an AI response.**

Flow:

```text
Input
+
Response
+
Optional Context
     ↓
Judge LLM
     ↓
Score + Reason
```

Possible dimensions:

```text
Accuracy
Relevance
Helpfulness
Groundedness
Tool Usage
Format Compliance
Safety
```

For RAG:

```text
Question
+
Retrieved Context
+
Response
     ↓
Judge
```

The Judge can evaluate whether the answer is grounded in supplied documents.

### Store judge metadata

Do not store only:

```text
score = 0.72
```

Also store:

```text
judge_model
judge_model_version
judge_prompt_version
score
reason
timestamp
```

The judge itself can change.

Example:

```text
Judge v1 → 0.85
Judge v2 → 0.72
```

The agent may not have changed at all.

### Judge calibration

Compare human judgments and judge outputs on a sample:

```text
Human Score
vs
Judge Score
```

If they consistently disagree, the judge model/prompt may need adjustment.

### Human + Judge

Practical pattern:

```text
100,000 traces
→ Model-as-Judge

Important 1,000 traces
→ Human Review
```

Model-as-Judge provides scale.

Human Review provides higher-confidence calibration.

---

## 16.5 Prompt Versions

Prompt Versioning means:

> **Treating prompts as versioned AI assets and linking prompt versions to traces and evaluation results.**

Example:

```text
Prompt v1
→ "Answer the user."

Prompt v2
→ "Answer the user.
   Do not guess when evidence is missing.
   Use tools when required."
```

Evaluation:

```text
Prompt v1 → score 0.78
Prompt v2 → score 0.89
```

Useful metadata:

```text
prompt_id
prompt_version
prompt_text
created_at
created_by
change_description
```

Example:

```text
prompt_id      = agent_system_prompt
prompt_version = 12
change         = "Clarified tool usage rules"
```

### Prompt version must be linked to trace

```text
Trace
 ├─ Agent v5
 ├─ Model A
 ├─ Prompt v12
 └─ Score 0.91
```

Then compare:

```text
Prompt v11 vs Prompt v12
```

using:

- Quality
- Tool success
- Cost
- Latency

### A/B testing

```text
50% → Prompt v10
50% → Prompt v11
```

Example:

```text
Prompt v10
success = 87%
cost    = $0.12

Prompt v11
success = 91%
cost    = $0.17
```

The highest-quality prompt may not be the best operational choice.

### Prompt assets are broader than one system prompt

Version separately if needed:

```text
system_prompt
tool_instruction
retrieval_prompt
judge_prompt
summarization_prompt
```

---

## 16.6 Model Versions

Model Versioning means:

> **Recording exactly which model version generated an AI result.**

A model name alone may not be sufficient.

```text
model = model-X
```

But:

```text
model-X in June
≠
model-X in September
```

if the provider updated the serving snapshot.

Useful metadata:

```text
provider
model_name
model_version
deployment_id
endpoint
```

### Evaluation axis

Hold fixed:

```text
Dataset v5
Prompt v12
Agent v7
```

and compare:

```text
Model A
quality = 0.88
latency = 1.2s
cost    = $0.04

Model B
quality = 0.91
latency = 2.0s
cost    = $0.02
```

### Self-hosted models

Versioning remains important with vLLM or internal models.

Possible dimensions:

```text
checkpoint
quantization
tokenizer_version
serving_config
```

### Fine-tuned models

Track:

```text
base_model
training_dataset_version
training_config
checkpoint_version
```

Example:

```text
Base Model   → M1
Training Set → train_v4
Fine-tune    → ft_v7
```

---

## 16.7 Agent Versions

Agent Versioning means:

> **Versioning the full behavior/configuration of an agent, not only its prompt.**

An agent can include:

```text
Agent
├─ System Prompt
├─ Model
├─ Tool Set
├─ Tool Routing Logic
├─ Retrieval
├─ Memory
└─ Workflow
```

Any of these can change behavior.

Example:

```text
Agent v10
→ tools A, B

Agent v11
→ tools A, B, C
→ new routing rule
```

Prompt may stay identical while behavior changes.

Possible metadata:

```text
agent_version
prompt_version
model_version
tool_set_version
workflow_version
retrieval_config_version
memory_config_version
```

Agent Version can be seen as a **bundle version**.

Example:

```text
agent_version = v12
prompt        = v8
model         = model-A-v3
toolset       = v4
workflow      = v6
retrieval     = v2
```

### Evaluate agent versions

```text
Dataset v7

Agent v10
quality = 0.84
cost    = $0.08
latency = 4.2s

Agent v11
quality = 0.91
cost    = $0.11
latency = 5.0s
```

Agent evaluation may include:

```text
quality
cost
latency
tool success
tool error rate
retrieval quality
```

---

## 16.8 Experiment Tracking

Experiment Tracking means:

> **Recording both the configuration of an AI experiment and the resulting metrics.**

Example:

```text
Experiment A

Dataset  = eval_v5
Prompt   = prompt_v12
Model    = model_A
Agent    = agent_v7

Quality  = 0.88
Latency  = 3.2s
Cost     = $0.05
```

Useful experiment fields:

```text
experiment_id
dataset_version
prompt_version
model_version
agent_version
evaluator_version
runtime_config
```

Results may include:

```text
accuracy
groundedness
tool_success_rate
latency
cost
```

### Change one variable when possible

To compare prompts:

```text
Dataset fixed
Model fixed
Agent logic fixed

Prompt v10
vs
Prompt v11
```

If everything changes simultaneously:

```text
Prompt changed
Model changed
Agent changed
Dataset changed
```

the result is hard to interpret.

### Offline vs Online Experiments

Offline:

```text
Fixed Evaluation Dataset
→ Agent A vs B
```

Online:

```text
Production Traffic
→ A/B Split
```

Offline is safer for pre-release testing.

Online gives real-world evidence.

---

## 16.9 Regression Datasets

Regression Dataset:

> **A collection of previously failed cases that must continue to work in future releases.**

Example production failure:

```text
Request:
"Show last week's AI cost by team."

Failure:
wrong tool selected
```

After fixing:

```text
Failure Trace
 ↓
Regression Case
```

Future releases:

```text
Agent v10
Agent v11
Agent v12
   ↓
Regression Dataset
```

Possible categories:

```text
tool_selection_regression
rag_regression
security_regression
format_regression
```

### Release gates

Example:

```text
Critical Security Regression
→ 100% pass required

General Regression
→ >= 98%
```

Dataset evolves:

```text
regression_v1
regression_v2
regression_v3
```

Important pattern:

> **Production Failure → Regression Case → Release Test**

---

## 16.10 Cost / Quality / Latency Analysis

AI optimization requires three major dimensions together:

```text
Quality
Cost
Latency
```

Example:

```text
Model A
Quality = 92
Latency = 5s
Cost    = $0.10

Model B
Quality = 90
Latency = 1.5s
Cost    = $0.02
```

There is no universal best choice without product requirements.

### Quality metrics

Examples:

```text
accuracy
groundedness
success_rate
tool_success_rate
user_satisfaction
judge_score
regression_pass_rate
```

### Cost metrics

Examples:

```text
input_tokens
output_tokens
model_cost
tool_cost
total_cost
cost_per_execution
cost_per_success
cost_per_team
```

`cost_per_success` can be more useful than raw request cost.

### Latency

Possible components:

```text
TTFT
LLM latency
Tool latency
Retrieval latency
Total latency
```

Agent example:

```text
LLM  2s
Tool 5s
LLM  2s
---------
Total 9s
```

Use percentiles, not only averages:

```text
p50
p95
p99
```

### Trade-offs

Common patterns:

```text
Larger model
→ Quality ↑
→ Cost ↑
→ Latency ↑
```

```text
More tool calls
→ Potential Quality ↑
→ Cost ↑
→ Latency ↑
```

```text
Smaller context
→ Cost ↓
→ Latency ↓
→ Quality may ↓
```

Target:

> **Maintain or improve quality while reducing cost and latency where possible.**

---

## 16.11 Langfuse + Iceberg Integration

Core idea:

> **Langfuse operates the AI execution/evaluation layer; Iceberg stores AI data as a long-term analytical asset.**

Role split:

```text
Langfuse
→ Traces
→ LLM calls
→ Tool calls
→ Prompt/Response
→ Scores
→ Feedback
→ Experiments
→ Evaluation Datasets
```

```text
Iceberg
→ long-term history
→ large-scale analytics
→ cross-domain joins
→ governance
→ BI
→ historical version analysis
```

Architecture:

```text
Application / Agent
        ↓
     Langfuse
        ↓
Trace / Observation / Score
        ↓
 Export / API
        ↓
Object Storage
        ↓
     Iceberg
        ↓
Spark / dbt / Trino
        ↓
BI / Cost / Evaluation Analytics
```

### Example Iceberg modeling

Facts:

```text
fact_agent_execution
fact_llm_call
fact_tool_call
fact_evaluation
```

Dimensions:

```text
dim_agent
dim_model
dim_prompt
dim_team
```

### Bronze / Silver / Gold

```text
Langfuse Export
     ↓
Bronze
→ raw traces / observations / scores

     ↓

Silver
→ normalized calls
→ version linkage
→ cost normalization
→ error categorization

     ↓

Gold
→ team AI cost
→ agent success rate
→ prompt quality
→ model p95 latency
→ cost per successful execution
```

### Why not keep everything only in Langfuse?

Enterprise analysis may require:

```text
Langfuse Trace
+
HR Organization Data
+
Finance Cost
+
Product Usage
+
Business KPI
```

This is more natural in a Data Platform.

### Source-of-truth split

```text
Git
→ Agent Code / Workflow / Config

Langfuse
→ AI Trace / Prompt / Evaluation Operations

Iceberg
→ Long-term Analytical History
```

---

## 16.12 Where Are All These Versions Usually Managed?

This was asked as a supplementary question during the session.

Answer:

> **Versions are usually not managed in one single system. They are managed according to asset type and connected with experiment/release identifiers.**

Typical mapping:

| Asset | Common management system |
|---|---|
| Prompt Version | Langfuse / MLflow / Git |
| Model Version | MLflow Model Registry / provider model snapshot |
| Agent Version | Git release / application release |
| Tool / Workflow Version | Git / config registry |
| Evaluation Dataset Version | Langfuse / MLflow / Lakehouse |
| Judge Version | Langfuse / MLflow + Git |
| Embedding Model | Model Registry / config |
| Retrieval Config | Git / config registry |
| Full Experiment | Langfuse / MLflow |

A clean structure:

```text
Git
├─ Agent Code
├─ Tool Logic
├─ Workflow
├─ Retrieval Config
└─ Deployment Config

Langfuse / MLflow
├─ Prompt Versions
├─ Traces
├─ Scores
├─ Feedback
├─ Evaluation Datasets
└─ Experiments

Model Registry
└─ Self-hosted / fine-tuned models

Iceberg
├─ Long-term telemetry history
├─ Long-term evaluation history
└─ Enterprise analytics
```

Example unified experiment record:

```text
experiment_id       = EXP-1042

agent_release       = 1.7.3
git_commit          = abc123

prompt_version      = 12
model_version       = model-A-2026-09
dataset_version     = eval-v8
evaluator_version   = judge-v4

retrieval_version   = v3
toolset_version     = v5

quality_score       = 0.92
latency_p95         = 3.4s
cost_per_execution  = $0.08
```

This record makes evaluation reproducible and explainable.

---

# Chapter 17 — Databricks Deep Dive

## 17.1 Lakehouse Architecture

Databricks can be understood as:

> **A managed Data + AI Platform that combines many components previously studied separately.**

Self-managed architecture might look like:

```text
Kafka
 ↓
Flink
 ↓
Iceberg
 ↓
Spark
 ↓
dbt
 ↓
Trino
 ↓
BI

Around:
Airflow
Catalog
Lineage
Governance
MLflow
```

Databricks integrates many of these responsibilities.

High-level structure:

```text
Sources
  ↓
Ingestion
  ↓
Lakehouse Storage
  ↓
Transformation / Streaming
  ↓
SQL / BI
  ↓
ML / AI

       ↕
  Unity Catalog
```

### Storage / Compute separation

```text
Storage
→ S3 / Cloud Object Storage

Compute
→ Databricks
```

### Table formats

Databricks historically centers on Delta Lake but now also supports Iceberg.

### Compute

Databricks Runtime is Spark-based and also integrates Photon.

### Medallion Architecture

```text
Bronze
→ raw

Silver
→ cleaned / validated / joined

Gold
→ business-ready / fact / dimension / mart
```

### Unified workload idea

Databricks combines:

```text
Data Engineering
+
SQL Warehouse
+
Governance
+
ML
+
AI
```

on the same data foundation.

---

## 17.2 Databricks Runtime and Photon

Databricks Runtime can be understood as:

> **Apache Spark packaged with Databricks optimizations, libraries, connectors, and platform integration.**

Self-managed Spark:

```text
Spark
+
JVM / Python
+
Libraries
+
Connectors
+
Cluster Config
+
Performance Tuning
```

Databricks:

```text
Databricks Runtime
=
Spark
+
Managed Environment
+
Optimization
+
Platform Integration
```

### Runtime versions

Runtime versions bundle:

- Spark version
- JDK
- libraries
- runtime features
- behavior changes

Production should manage runtime upgrades intentionally.

### Photon

Photon:

> **Databricks' native vectorized execution engine for supported SQL/DataFrame operations.**

Concept:

```text
SQL / DataFrame
     ↓
Catalyst Planning
     ↓
Photon
     ↓
Native Execution
```

Useful for:

- scan,
- filter,
- joins,
- aggregation,
- shuffle,
- Parquet operations.

Photon does not conceptually replace Spark.

```text
Spark
→ API / planner / distributed framework

Photon
→ optimized execution layer
```

---

## 17.3 SQL Warehouses

SQL Warehouse:

> **Managed SQL compute for interactive analytics, BI, and dashboard workloads.**

Architecture:

```text
Delta / Iceberg
     ↓
SQL Warehouse
     ↓
BI / Analyst / Dashboard
```

This is similar to the role Trino played in the open architecture.

Use cases:

- Ad-hoc SQL
- BI
- Dashboard
- Reporting
- Analyst exploration
- SQL transformation

Important:

```text
Storage
→ object storage / tables

SQL Warehouse
→ compute
```

### Serverless SQL

Serverless reduces cluster operations:

```text
Query Load ↑
→ Compute scale ↑

Query Load ↓
→ Compute scale ↓
```

### Concurrency

Designed for multiple concurrent SQL consumers.

### Governance

Queries pass through Unity Catalog governance.

### Semantic layer connection

Databricks Metric Views occupy the same conceptual area studied earlier:

```text
central metric definitions
+
dimensions
+
consistent business semantics
```

---

## 17.4 Unity Catalog

Unity Catalog:

> **Databricks' unified governance layer for Data and AI assets.**

Hierarchy:

```text
Metastore
   ↓
Catalog
   ↓
Schema
   ↓
Object
```

Three-part names:

```text
catalog.schema.table
```

Example:

```text
production.ai.fact_llm_call
```

### Object types

Unity Catalog can govern:

```text
Tables
Views
Volumes
Functions
Models
AI-related objects
```

### Volumes

Useful for governed files:

```text
PDF
Image
JSON
Documents
Artifacts
```

RAG example:

```text
PDF / Document
→ Volume

Chunk / Embedding
→ Table
```

### Managed vs External

Managed Table:

```text
UC manages
→ metadata
→ storage location
→ lifecycle
→ optimization
```

External Table:

```text
Data lives at user-managed object path
UC manages
→ metadata
→ access/governance
```

### Access

Objects are securable.

Privileges may apply at:

```text
Catalog
Schema
Table
View
Volume
Model
...
```

Hierarchy enables inherited policy.

---

## 17.5 Lakeflow Jobs

Lakeflow Jobs:

> **Databricks workflow orchestration.**

Airflow mapping:

```text
Airflow DAG
≈ Lakeflow Job
```

Inside a job:

```text
Task
→ dependency
→ schedule / trigger
```

Task types may include:

- Notebook
- SQL
- dbt
- Pipeline
- Python/Spark
- ML

Triggers may include:

```text
time schedule
file arrival
table update
continuous execution
```

### Airflow vs Lakeflow Jobs

```text
Lakeflow Jobs
→ Databricks-centered orchestration

Airflow
→ broader cross-platform orchestration
```

If most workloads live inside Databricks, a separate Airflow may not be necessary.

If workflows span:

```text
Databricks
AWS Lambda
Kubernetes
Snowflake
SaaS APIs
internal systems
```

a general orchestrator can still be useful.

---

## 17.6 Lakeflow Pipelines

Lakeflow high-level view:

```text
Lakeflow
├─ Connect
│   → ingestion
├─ Pipelines
│   → transformation
└─ Jobs
    → orchestration
```

### Jobs vs Pipelines

Jobs:

> **Define task execution order.**

Pipelines:

> **Define dataset transformation relationships declaratively.**

Procedural style:

```text
1. Run Bronze notebook
2. Run Silver notebook
3. Run Gold SQL
```

Declarative style:

```text
bronze_events
      ↓
silver_events
      ↓
gold_metrics
```

The engine manages more of:

- dependencies,
- incremental updates,
- execution order,
- parallelization,
- monitoring.

### Batch + Streaming

Pipelines can process both.

They are conceptually connected to Spark Structured Streaming.

### Important objects

```text
Pipeline
Flow
Streaming Table
Materialized View
```

### DLT naming

Older:

```text
Delta Live Tables (DLT)
```

Current direction:

```text
Lakeflow Pipelines
```

---

## 17.7 Delta / Iceberg Interoperability

Delta and Iceberg solve similar problems:

```text
Object Storage
+
Parquet
+
Table Metadata
```

with:

- transactions,
- snapshots,
- schema evolution,
- time travel,
- table management.

### Databricks default

Delta is still the natural/native path for many Databricks-managed workloads.

### Managed Iceberg

Databricks also supports Unity Catalog managed Iceberg tables.

Concept:

```text
Unity Catalog
   ↓
Managed Iceberg
   ↓
Parquet
```

### UniForm

Core idea:

> **Keep the same Parquet data while exposing compatible Iceberg metadata so Iceberg clients can read the table.**

Conceptual diagram:

```text
           Parquet Files
           /          \
Delta Metadata    Iceberg Metadata
      ↓                 ↓
Databricks       External Iceberg clients
```

This reduces the need to duplicate table data.

### Iceberg REST Catalog

Unity Catalog can participate in Iceberg REST-based interoperability.

External engines such as:

```text
Spark
Flink
Trino
```

can interact through Iceberg-compatible interfaces.

### Important distinction

```text
Delta ≠ Iceberg
```

Interoperability layers do not mean both formats are identical.

### Simple selection intuition

```text
Databricks-centric ecosystem
→ Delta is natural

Multi-engine / open ecosystem
→ Iceberg is natural
```

Modern Databricks supports both far more than before.

---

## 17.8 Lineage / Governance

Unity Catalog combines:

```text
Lineage
Classification
Access Control
Masking
Row Filters
Audit
```

### Lineage

Example:

```text
bronze.llm_calls
      ↓
Spark
      ↓
silver.llm_calls
      ↓
SQL/dbt
      ↓
gold.ai_usage
      ↓
Dashboard
```

Column-level lineage supports impact analysis.

### Classification

Example:

```text
email
→ PII

employee_id
→ Sensitive Internal
```

### Tags

Classification/tagging can drive policies.

```text
PII Tag
   ↓
Masking Policy
```

### RBAC / ABAC

RBAC:

```text
role
→ privilege
```

ABAC:

```text
attribute/tag
→ policy
```

Example:

```text
Tag = PII

General Analyst
→ masked

Security Admin
→ clear text
```

### External lineage

Enterprise lineage may include assets outside Databricks.

### AI governance

Governance scope increasingly includes:

- models,
- model services,
- agents,
- AI services.

---

## 17.9 MLflow

MLflow now spans:

```text
Traditional ML
+
GenAI / Agents
```

### Traditional ML

Experiment Tracking:

```text
Run
├─ Parameters
├─ Metrics
├─ Code Version
└─ Artifacts
```

### Model Registry

Tracks:

```text
model_name
version
alias
tags
lineage
```

In Databricks this integrates with Unity Catalog.

### GenAI Tracing

Concept:

```text
User
 ↓
Agent
 ↓
Retriever
 ↓
LLM
 ↓
Tool
 ↓
Response
```

Trace can capture:

```text
input
output
latency
tokens
cost
tool calls
retrieval
```

### GenAI Evaluation

Supports:

```text
evaluation datasets
scorers
LLM judges
custom rules
```

### Prompt Registry

Prompts can be versioned and evaluated.

### Human Feedback

Review and labeling can be connected to traces/evaluation.

### Langfuse overlap

There is now significant overlap:

| Capability | Langfuse | MLflow 3 |
|---|---|---|
| LLM tracing | Yes | Yes |
| Tool/retrieval tracing | Yes | Yes |
| Prompt management | Yes | Yes |
| Evaluation | Yes | Yes |
| LLM judge | Yes | Yes |
| Human feedback | Yes | Yes |
| Experiments | Yes | Yes |
| Traditional ML | Limited focus | Strong |
| Model Registry | Not core | Core |
| Unity Catalog Integration | External | Native |

If Databricks becomes the main enterprise platform, MLflow may cover many functions that would otherwise require Langfuse.

---

## 17.10 AI / Vector Capabilities

Databricks connects Lakehouse data to AI application capabilities.

High-level:

```text
Lakehouse
   ↓
AI Search
   ↓
Model / Agent
   ↓
Serving
   ↓
Application
```

### AI Search

Role:

> **Retrieve relevant enterprise data for RAG/search.**

Typical flow:

```text
Documents
 ↓
Chunking
 ↓
Embeddings
 ↓
AI Search
 ↓
Retriever
 ↓
LLM
```

### Search index sync

Source tables can be incrementally synchronized into search indexes.

### Model Serving

Models can be exposed as managed endpoints.

Possible models:

```text
custom model
foundation model
external model provider
```

### Agents

Agents can combine:

```text
LLM
AI Search
SQL Tool
MCP
External API
```

### Governance

Unity Catalog permissions should apply before unauthorized data reaches retrieval.

Important principle:

> **Do not retrieve unauthorized documents and hide them later. Prevent unauthorized retrieval in the first place.**

### Integrated AI stack

```text
Unity Catalog
→ governance

MLflow
→ trace/evaluation

Lakehouse
→ data

AI Search
→ retrieval

Model Serving
→ inference
```

---

## 17.11 Databricks Cost Model

Main idea:

> **Compute is the largest controllable cost dimension, with storage/network and AI services added around it.**

### DBU

DBU:

> Databricks normalized billing unit for compute/service usage.

Do not interpret it as a fixed CPU count.

### Classic Compute

Conceptually:

```text
Databricks DBU
+
Cloud VM
+
Storage / Network
```

### Serverless

Infrastructure is managed by Databricks.

Operational burden decreases.

External storage/network costs can still exist.

### Cost sources

```text
Spark Jobs
SQL Warehouse
Lakeflow Pipelines
Serverless
Model Serving
AI Search
Storage
Network
Background optimization
```

### Performance optimization = cost optimization

```text
Partition Pruning
→ Scan ↓
→ Runtime ↓
→ Cost ↓
```

```text
Compaction
→ Query efficiency ↑
→ Cost ↓
```

```text
Incremental Processing
→ Full recompute avoided
→ Cost ↓
```

### Track by tags

Useful dimensions:

```text
team
project
environment
job
workspace
```

### Serverless is not automatically cheaper

It can improve:

- operational simplicity,
- startup time,
- scaling,
- idle reduction.

Actual cost still depends on workload.

---

## 17.12 Which Self-Managed Components Databricks Can Replace

Self-managed architecture:

```text
S3
+
Iceberg
+
Spark
+
Trino
+
Airflow
+
dbt
+
Catalog
+
OpenLineage
+
MLflow
+
Vector DB
+
AI Observability
```

Databricks can consolidate many responsibilities.

### High replacement potential

```text
Spark Cluster
→ Databricks Runtime / Serverless

Trino-like BI serving
→ SQL Warehouse

Custom Spark pipeline framework
→ Lakeflow Pipelines

Catalog / Governance
→ Unity Catalog

OpenLineage / Marquez-like internal lineage
→ Unity Catalog Lineage

Self-hosted MLflow
→ Managed MLflow

Vector DB for Databricks-centric RAG
→ AI Search
```

### Partial replacement

```text
Airflow
→ Lakeflow Jobs can replace it for Databricks-centric workflows

Langfuse
→ MLflow 3 overlaps substantially

dbt
→ Databricks SQL / Pipelines overlap, but dbt remains valid
```

### Usually not a full replacement

```text
Kafka
→ separate durable event log / event bus role

Flink
→ may remain for low-latency complex stateful streaming

Cross-platform orchestrator
→ may remain if the platform spans many systems
```

### Databricks' real value

Not simply:

> "Spark is faster."

But:

> **Reduce the number of platform components that must be installed, upgraded, integrated, secured, monitored, and operated independently.**

Trade-off:

```text
Operational Complexity ↓
Integration Speed ↑

but

Platform Dependency ↑
Vendor Lock-in ↑ possible
Cost ↑ possible
```

---

# Chapter 18 — Snowflake Deep Dive (Condensed)

> The user explicitly requested that Snowflake be summarized once and then skipped.

Snowflake can be summarized as:

> **A managed cloud data platform built around separated storage and compute, historically centered on SQL/Data Warehouse workloads, now expanded into data engineering, Iceberg, governance, and AI.**

---

## 18.1 Architecture

High-level layers:

```text
Cloud Services
     ↓
Virtual Warehouses
     ↓
Storage
```

### Storage

Snowflake-managed or Iceberg-related storage.

### Virtual Warehouse

Independent compute cluster for queries/DML.

Different warehouses provide workload isolation.

### Cloud Services

Handles:

- metadata,
- authentication,
- query optimization,
- access control,
- coordination.

---

## 18.2 Micro-partitions

Snowflake automatically organizes table data into **micro-partitions**.

```text
Table
├─ Micro-partition 1
├─ Micro-partition 2
├─ Micro-partition 3
└─ ...
```

Snowflake tracks metadata such as value ranges.

This helps pruning.

---

## 18.3 Pruning

Query:

```sql
WHERE event_date = '2026-09-26'
```

Snowflake can avoid reading micro-partitions that cannot match.

Conceptually similar goal to:

```text
Iceberg File Pruning
Parquet Row Group Pruning
```

---

## 18.4 Clustering

When data layout becomes poor for frequent filters, clustering can improve pruning efficiency.

Large tables may use clustering keys.

The goal is not to manually partition everything, but to improve physical distribution for query patterns.

---

## 18.5 Streams

Streams track row-level changes to tables.

```text
Table
 ↓
Stream
 ↓
Change Data
```

Useful for incremental processing.

---

## 18.6 Tasks

Tasks schedule or trigger SQL work.

Common combination:

```text
Stream
 ↓
Task
 ↓
MERGE / SQL Transform
```

---

## 18.7 Dynamic Tables

Dynamic Table:

> **Declare the query result and desired freshness; Snowflake manages refresh.**

Example:

```text
Raw
 ↓
Dynamic Table
 ↓
Silver
 ↓
Dynamic Table
 ↓
Gold
```

Use a target lag:

```text
TARGET_LAG = 10 minutes
```

This is conceptually similar to declarative data pipelines.

---

## 18.8 Snowpipe / Snowpipe Streaming

Snowpipe:

```text
Object Storage File
 ↓
Snowpipe
 ↓
Snowflake
```

Snowpipe Streaming allows lower-latency continuous ingestion without relying only on staged files.

---

## 18.9 Iceberg Tables

Snowflake supports Apache Iceberg tables and multi-engine interoperability.

```text
Snowflake
 ↓
Iceberg Table
 ↓
Object Storage
```

Snowflake/Horizon can participate in Iceberg catalog workflows.

External engines such as Spark/Trino can participate in open Iceberg workflows.

---

## 18.10 Governance — Horizon Catalog

Conceptual counterpart to Unity Catalog:

```text
Databricks
→ Unity Catalog

Snowflake
→ Horizon Catalog
```

Horizon provides:

- discovery,
- metadata,
- lineage,
- classification,
- masking,
- row access,
- governance,
- Iceberg visibility,
- semantic/business context.

---

## 18.11 Cortex / AI

Snowflake increasingly integrates AI capabilities:

```text
Cortex AI
Search
Analyst
Agents
AI interfaces
```

The overall product direction is similar to the rest of the industry:

> bring AI closer to governed enterprise data.

---

## 18.12 Cost Model

Compute unit:

```text
Virtual Warehouse
```

Billing is credit-based.

Cost dimensions:

```text
Warehouse Compute
Serverless Compute
Cloud Services
Storage
```

Optimization:

```text
Auto Suspend
Right-size Warehouse
Reduce Scan
Efficient Queries
Use incremental refresh where possible
```

---

## 18.13 Snowflake Mental Model

Remember:

```text
Storage
→ Snowflake-managed / Iceberg

Compute
→ Virtual Warehouse

Layout
→ Micro-partitions

Performance
→ Pruning + Clustering

Pipeline
→ Dynamic Tables
→ Streams + Tasks

Ingestion
→ Snowpipe

Governance
→ Horizon Catalog

AI
→ Cortex / Search / Agents

Billing
→ Credits
```

Historical trajectory:

```text
Databricks
→ Spark / Data Engineering / AI
→ expanded into SQL Warehouse

Snowflake
→ Cloud Data Warehouse / SQL
→ expanded into Data Engineering / Iceberg / AI
```

Today there is significant functional overlap.

---

# Chapter 19 — Databricks vs Snowflake vs Open Lakehouse

This chapter is intentionally comparative rather than product-by-product.

The three broad approaches are:

```text
1. Databricks-centered managed Lakehouse
2. Snowflake-centered managed Data Platform
3. Open Lakehouse assembled from open components
```

An Open Lakehouse could look like:

```text
Object Storage
+
Iceberg
+
Spark
+
Flink
+
Trino
+
Airflow
+
dbt
+
OpenLineage
+
DataHub/OpenMetadata
+
MLflow/Langfuse
```

The goal is not to declare a universal winner.

The goal is to understand trade-offs.

---

## 19.1 Storage Ownership

### Databricks

Typical model:

```text
Cloud Object Storage
+
Delta / Iceberg
+
Unity Catalog
```

Data can remain in cloud storage while Databricks manages table/governance layers.

### Snowflake

Historically:

```text
Snowflake-managed storage
```

But Snowflake increasingly supports Iceberg/external-storage interoperability.

### Open Lakehouse

Most explicit ownership:

```text
Your S3 / ADLS / GCS
+
Your Iceberg Tables
```

The organization directly controls object storage and table metadata architecture.

Mental model:

```text
Open Lakehouse
→ maximum direct storage ownership

Managed Platforms
→ more operational responsibilities moved to vendor
```

---

## 19.2 Iceberg Openness

Apache Iceberg is designed for multi-engine interoperability.

```text
Spark
Flink
Trino
Snowflake
Databricks
other engines
     ↓
Iceberg Table
```

The Iceberg REST Catalog specification exists to make catalogs easier to access across multiple languages and engines.

Modern Databricks supports managed Iceberg and external access.

Snowflake also supports Iceberg and Horizon-based multi-engine scenarios.

Therefore the useful question is no longer:

> "Does the platform support Iceberg?"

Instead ask:

> **How native is Iceberg in the platform, and how much functionality remains available when external engines access the same tables?**

---

## 19.3 Compute Model

### Databricks

Multiple compute styles:

```text
Spark Runtime
Photon
SQL Warehouse
Serverless Jobs
Model Serving
```

Strong connection to general-purpose data processing.

### Snowflake

Core abstraction:

```text
Virtual Warehouse
```

Strong SQL-centric managed compute model with serverless services around it.

### Open Lakehouse

Compute is explicitly composable:

```text
Spark
→ Batch / ETL

Flink
→ Streaming

Trino
→ Interactive SQL

vLLM
→ AI Serving
```

Strong flexibility, higher integration burden.

---

## 19.4 Batch

### Databricks

Very strong fit due to Spark heritage.

Natural for:

- ETL
- backfills
- large joins
- ML dataset generation
- lakehouse transformation

### Snowflake

Very capable SQL-based transformation and Dynamic Tables.

Excellent when transformation is primarily SQL and warehouse-centric.

### Open Lakehouse

Maximum choice.

Can use:

```text
Spark
Trino
dbt
other engines
```

But the organization must operate them.

---

## 19.5 Streaming

### Databricks

Strong via:

```text
Spark Structured Streaming
Lakeflow Pipelines
Lakeflow Connect
```

Good when streaming is integrated with Lakehouse workflows.

### Snowflake

Streaming ingestion and incremental refresh are supported through:

```text
Snowpipe Streaming
Streams
Dynamic Tables
```

### Open Lakehouse

Can use Flink for sophisticated stateful/event-time workloads.

Best when requirements include:

- very low latency,
- large state,
- complex event time,
- fine-grained streaming control.

The price is operational complexity.

---

## 19.6 SQL / BI

### Snowflake

SQL/Data Warehouse is historically the center of the product.

```text
BI / Analyst
 ↓
Virtual Warehouse
 ↓
Snowflake Data
```

### Databricks

SQL Warehouse + Photon make BI/interactive SQL a first-class workload.

### Open Lakehouse

Typical:

```text
Iceberg
 ↓
Trino
 ↓
BI
```

Very open, but SQL service operations remain the user's responsibility.

---

## 19.7 Governance

### Databricks

```text
Unity Catalog
```

Combines:

- access,
- lineage,
- classification,
- audit,
- Data/AI governance.

### Snowflake

```text
Horizon Catalog
```

Combines similar governance concerns.

### Open Lakehouse

May require assembling:

```text
Catalog
+
IAM
+
OpenLineage
+
DataHub/OpenMetadata
+
Policy Engine
+
Audit
```

Open approach gives choice but increases platform work.

---

## 19.8 Lineage

Managed platforms benefit from observing their own execution systems.

Example:

```text
Databricks Job
→ Table
→ Dashboard
```

can often be captured automatically within the platform.

Open Lakehouse lineage may span:

```text
Kafka
Flink
Spark
dbt
Trino
BI
```

which is more flexible but requires standardization/integration.

This is where OpenLineage becomes valuable.

---

## 19.9 AI Ecosystem

### Databricks

Integrated AI direction:

```text
Lakehouse
+
MLflow
+
AI Search
+
Model Serving
+
Agents
+
Unity Catalog
```

Natural when AI workloads need close access to data engineering assets.

### Snowflake

Integrated direction:

```text
Snowflake Data
+
Cortex
+
Search / Analyst
+
Agents
+
Horizon
```

Natural when enterprise data already lives in Snowflake.

### Open Lakehouse

Composable AI stack:

```text
Iceberg
+
Vector DB
+
vLLM
+
LiteLLM
+
Langfuse
+
MLflow
+
Agent Framework
```

Maximum flexibility and portability, but highest integration burden.

---

## 19.10 Portability

### Open Lakehouse

Highest conceptual portability when based on:

```text
Parquet
Iceberg
OpenLineage
Open APIs
```

Compute engines can be replaced more easily.

### Managed Platforms

Modern Databricks and Snowflake both support more open interfaces than before, especially around Iceberg.

However, platform-specific features can still create dependencies.

Examples:

```text
managed workflow definitions
vendor-specific governance policies
serverless execution behavior
AI services
proprietary optimization
```

The table data may be portable while the **operational system** is not fully portable.

---

## 19.11 Operational Complexity

### Open Lakehouse

You may have to operate:

```text
Kafka
Flink
Spark
Trino
Airflow
Catalog
Lineage
MLflow
Observability
Security Integration
```

This gives control but requires a strong platform team.

### Databricks / Snowflake

Reduce:

- installation,
- scaling,
- upgrades,
- compatibility management,
- cross-component auth,
- part of monitoring,
- part of governance integration.

The value is often less about one engine being better and more about:

> **reducing integration and operations work.**

---

## 19.12 Vendor Lock-in

Lock-in is not simply:

```text
"Is the table format open?"
```

Lock-in can happen at many layers:

```text
Data Format
Catalog
Pipeline Definitions
Orchestration
Security Policies
ML Registry
AI Evaluation
Serving
Operational Knowledge
```

Example:

```text
Iceberg Table
→ portable

But

vendor-specific pipeline + governance + AI stack
→ less portable
```

Therefore think in layers.

---

## 19.13 Total Cost

Do not compare only:

```text
$/compute-hour
```

Total Cost includes:

```text
Compute
Storage
Network
Licenses
Platform Engineering Labor
Operations
Upgrades
Incident Response
Security Integration
Governance
Developer Productivity
```

Open Lakehouse may have lower direct software cost but higher people/operations cost.

Managed platforms may have higher service cost but reduce engineering overhead.

The right comparison is **TCO**, not sticker price.

---

## 19.14 Simplified Comparison Table

| Area | Databricks | Snowflake | Open Lakehouse |
|---|---|---|---|
| Historical center | Spark/Data/AI | SQL/DWH | Open data architecture |
| Storage | Object storage + Delta/Iceberg | Managed + Iceberg options | Object storage |
| Batch | Very strong | Strong | Very strong with Spark |
| Streaming | Strong | Increasingly strong | Strongest flexibility with Flink |
| Interactive SQL | SQL Warehouse | Core strength | Trino |
| Governance | Unity Catalog | Horizon Catalog | Assemble tools |
| ML/AI | Very integrated | Increasingly integrated | Fully composable |
| Iceberg | Strong support | Strong support | Native design choice |
| Portability | Medium–High depending on feature | Medium–High depending on feature | Highest |
| Ops burden | Low–Medium | Low–Medium | High |
| Vendor dependency | Medium–High | Medium–High | Low–Medium |
| Platform engineering freedom | Medium | Medium | Highest |

---

## 19.15 Practical Decision Heuristics

Choose a Databricks-centered approach when:

```text
large-scale ETL
Spark expertise
ML/AI workloads
Lakehouse architecture
data engineering + AI integration
```

are central.

Choose a Snowflake-centered approach when:

```text
SQL analytics
enterprise warehouse
BI
managed simplicity
warehouse-centric organization
```

are central.

Choose Open Lakehouse when:

```text
multi-engine flexibility
deep infrastructure control
open standards
portability
custom platform capability
```

are strategically important and the organization can support the operational burden.

A hybrid is normal.

Example:

```text
Kafka/Flink
   ↓
Iceberg
   ↓
Databricks + Trino
```

or:

```text
Iceberg
├─ Snowflake
├─ Spark
└─ Trino
```

The goal is not architectural purity.

The goal is:

> **Use the minimum number of components required to satisfy real workloads and organizational constraints.**

---

# Chapter 20 — Production Data Platform Engineering

This phase combines earlier concepts into **production operations**.

The key shift is:

> Earlier chapters asked "How does this technology work?"
> Production engineering asks "What happens at 3 AM when it breaks?"

---

## 20.1 Backfills

Backfill:

> **Recompute historical data for a defined range.**

Use cases:

- pipeline outage,
- bug fix,
- new business logic,
- missing data,
- schema correction.

Prefer scoped backfills.

```text
Bad:
Recompute all 5 years

Better:
Recompute affected partitions only
```

Examples:

```text
2026-09-01 ~ 2026-09-03
```

or:

```text
event_date partition
```

Requirements:

- idempotent tasks,
- parameterized date ranges,
- predictable output replacement,
- resource controls.

---

## 20.2 Reprocessing

Backfill is one form of reprocessing.

### Kafka Replay

```text
Kafka offset
 ↓
Reconsume events
```

Useful when the Event Log remains the source of truth.

### Bronze Replay

```text
Bronze Raw History
 ↓
new transformation
 ↓
rebuild Silver / Gold
```

This is one reason raw history is valuable.

### Iceberg Snapshot Recovery

If data corruption is recent:

```text
Current bad snapshot
 ↓
previous good snapshot
```

Time travel/rollback may help recovery.

Important question:

> **What is the authoritative source of truth?**

Possible answers:

```text
Operational DB
Kafka
Bronze
Iceberg Snapshot
external source
```

This must be decided before incidents.

---

## 20.3 Incident Drill — Schema Break

Example:

```text
Source:
amount BIGINT

changed to:
amount STRING
```

Possible chain:

```text
Producer
 ↓
CDC / Event
 ↓
Flink/Spark
 ↓
Silver
 ↓
dbt
 ↓
Dashboard
```

Response:

```text
Detect schema change
 ↓
Stop/Quarantine incompatible data
 ↓
Use Lineage for impact analysis
 ↓
Fix producer/consumer
 ↓
Backfill affected data
 ↓
Validate
```

Prevention:

- Data Contracts
- Schema Registry
- Compatibility checks
- CI/CD validation

---

## 20.4 Incident Drill — Bad Data

Examples:

```text
latency_ms = -100
```

or:

```text
90% of user_id is NULL
```

Response:

```text
Quality Alert
 ↓
Contain
 ↓
Quarantine / stop publish
 ↓
Root Cause
 ↓
Fix
 ↓
Reprocess
 ↓
Verify
```

Do not allow a technically successful pipeline to silently publish bad business data.

---

## 20.5 Incident Drill — Data Skew

Symptoms:

```text
Most Spark tasks finish quickly
One task runs forever
```

or:

```text
one Flink key becomes hot
```

Investigate:

- key distribution,
- null/default values,
- join cardinality,
- hot customers/teams.

Possible responses:

```text
salting
pre-aggregation
heavy-key special handling
partition strategy change
AQE
```

For streaming, preserve ordering requirements when considering re-keying/salting.

---

## 20.6 Incident Drill — Small File Explosion

Symptoms:

```text
millions of tiny Parquet files
```

Consequences:

- metadata overhead,
- slow query planning,
- high object storage request count,
- poor task efficiency.

Causes:

- excessive streaming commits,
- too much partitioning,
- too many small writes.

Response:

```text
Compaction
 ↓
adjust target file size
 ↓
adjust write frequency
 ↓
reconsider partition strategy
```

---

## 20.7 Incident Drill — Stale Table

Example:

```text
Current time: 10:00
Gold latest data: 08:40
```

Investigate layer by layer:

```text
Source Freshness?
Kafka?
Bronze?
Silver?
Gold?
Dashboard?
```

This is why freshness should be measured at multiple points.

---

## 20.8 Incident Drill — Corrupt Transformation

Example:

```text
WHERE event_type = 'clik'
```

Job succeeds.

Result:

```text
0 rows
```

Pipeline health:

```text
GREEN
```

Data health:

```text
RED
```

Response:

```text
Volume / Quality anomaly
 ↓
Find changed transformation
 ↓
Fix code
 ↓
Backfill affected interval
```

Important lesson:

> **Green Pipeline ≠ Healthy Data**

---

## 20.9 Incident Drill — CDC Failure

Possible failures:

```text
Connector stopped
Offset lost
Required WAL expired
Duplicate replay
Schema changed
```

Normal recovery:

```text
Restart
 ↓
Stored Offset
 ↓
Replay
 ↓
Idempotent downstream
```

Severe recovery:

```text
Offset unavailable
or WAL unavailable
 ↓
Snapshot / Re-bootstrap
```

---

## 20.10 Capacity Planning

Capacity planning means estimating whether the platform can handle expected volume and concurrency.

Key inputs:

```text
events / second
GB / TB per day
retention days
peak multiplier
number of partitions
file count
Spark concurrency
query concurrency
streaming state size
```

Example:

```text
10k events/sec
× average event size
× 86,400 sec/day
→ daily ingestion volume
```

Do not plan only around averages.

Also consider:

```text
peak traffic
backfill traffic
incident replay
month-end reports
concurrent dashboards
```

---

## 20.11 Kafka Capacity Questions

Useful questions:

```text
How many events/sec?
How many partitions?
What retention?
How many consumers?
How much replay traffic?
```

Too few partitions:

```text
consumer parallelism limited
```

Too many partitions:

```text
operational overhead increases
```

---

## 20.12 Lakehouse Capacity Questions

Track:

```text
TB/day
file count/day
average file size
partition count
snapshot count
delete file growth
```

Data size alone is not enough.

```text
1 TB in 8 files
≠
1 TB in 1,000,000 files
```

Operational characteristics are very different.

---

## 20.13 Spark Capacity Questions

Consider:

```text
concurrent jobs
shuffle volume
executor memory
task count
CPU
backfill overlap
```

A pipeline that works daily may fail when a 90-day backfill starts at the same time.

Backfill needs its own capacity policy.

---

## 20.14 Query Capacity Questions

For Trino / SQL Warehouse / Snowflake:

```text
concurrent users
dashboard refresh rate
query scan size
join complexity
memory
peak BI windows
```

Interactive workloads and batch workloads should not necessarily share the same compute pool.

Workload isolation is useful.

---

## 20.15 Cost Engineering

Major cost drivers:

```text
Compute
Storage
Network
Object Storage Requests
Serving Stores
Compaction
Streaming always-on compute
AI inference
```

### Compute optimization

Reduce:

```text
unnecessary scan
shuffle
recomputation
idle compute
oversized clusters
```

### Storage optimization

Manage:

```text
Retention
Snapshot expiration
Orphan files
Duplicate datasets
Raw data lifespan
```

### Serving cost

Do not send every workload to the expensive analytical engine.

Example:

```text
Heavy analytics
→ Lakehouse

Low-latency operational read
→ Serving Store / Cache
```

### FinOps dimensions

Tag by:

```text
team
project
environment
pipeline
product
```

so cost ownership is clear.

---

## 20.16 DR / Recovery

DR = Disaster Recovery.

Important recovery scenarios:

```text
Catalog loss
Object storage problem
Checkpoint loss
CDC state loss
Region outage
Bad deployment
Credential/policy corruption
```

---

## 20.17 Catalog Recovery

A Lakehouse table is more than files.

If table metadata/catalog is lost:

```text
Parquet files may still exist
but
table may not be immediately usable
```

Therefore catalog metadata is production infrastructure.

Protect it using:

- managed service durability,
- backup/export where available,
- infrastructure-as-code for configuration,
- recovery procedures.

---

## 20.18 Table Recovery

Possible tools:

```text
Iceberg snapshot
time travel
rollback
Bronze replay
source replay
```

The fastest recovery depends on the failure type.

---

## 20.19 Checkpoint Loss

Streaming systems depend on checkpoint/state.

If Spark/Flink checkpoint is lost:

```text
Where should processing resume?
```

Possibilities:

- replay from Kafka,
- recover from Savepoint,
- rebuild state,
- restart from known timestamp.

This can cause:

- duplicate processing,
- long recovery time,
- downstream load spike.

Plan it before an outage.

---

## 20.20 Source-of-Truth Decisions

For every critical dataset, document:

```text
Source of Truth
Recovery Source
Maximum Replay Window
Retention
Owner
SLO
```

Example:

```text
fact_llm_call

Source of Truth:
Kafka raw events for 7 days
+
Iceberg Bronze after ingestion

Recovery:
Replay Kafka if <7 days
Otherwise rebuild from Bronze
```

This turns recovery from improvisation into procedure.

---

## 20.21 Data Platform SLOs

Core SLO categories:

### Freshness

```text
Gold table < 15 min behind source
```

### Correctness

```text
duplicate rate < 0.01%
required field completeness > 99.9%
```

### Availability

```text
Query layer available 99.9%
```

### Recovery Time

RTO:

> How quickly must the platform recover?

Example:

```text
critical dataset RTO < 1 hour
```

### Recovery Point

RPO:

> How much data loss is acceptable?

Example:

```text
RPO < 5 minutes
```

### Query Latency

```text
p95 dashboard query < 5 seconds
```

Different datasets need different SLOs.

Tier them.

```text
Tier 1
→ executive/business-critical
→ strict SLO

Tier 2
→ standard analytics

Tier 3
→ experimental
```

---

## 20.22 Production Runbook Mental Model

For each critical pipeline know:

```text
Owner
Source
Destination
SLO
Alert
Failure Modes
Replay Procedure
Backfill Procedure
Rollback Procedure
Cost Owner
Downstream Impact
```

A mature platform is not defined only by architecture diagrams.

It is also defined by:

> **whether operators know exactly what to do when the architecture fails.**

---

# Chapter 21 — Final End-to-End Data Platform Architecture

This is the final integration of the entire curriculum.

---

## 21.1 Core Architecture

```text
                    Applications
                         │
              ┌──────────┴──────────┐
              │                     │
         Event Data             Operational Data
              │                     │
            Kafka              PostgreSQL
              │                     │
              │                  Debezium
              │                     │
              └──────────┬──────────┘
                         │
                  Stream Processing
                   Flink / Spark
                         │
                         ▼
                  Bronze Iceberg
                         │
                         ▼
                       Spark
                         │
                         ▼
                  Silver Iceberg
                         │
                    dbt / Spark
                         │
                         ▼
                     Gold / Mart
                         │
               ┌─────────┼──────────┐
               │         │          │
             Trino       BI      AI Evaluation
```

---

## 21.2 Why Kafka Exists

Kafka is not the analytical database.

Role:

```text
Durable Event Transport
+
Replayable Event Log
+
Decoupling Producers/Consumers
```

Use when:

- multiple consumers need events,
- replay is valuable,
- asynchronous processing is required,
- event-driven architecture matters.

Do not add Kafka only because "data platforms use Kafka."

At low scale:

```text
Application
 ↓
Database / Direct Batch Export
```

may be enough.

---

## 21.3 Why Flink Exists

Role:

```text
Stateful Real-Time Stream Processing
```

Use when:

- low latency matters,
- Event Time is important,
- Watermarks are needed,
- large stateful streaming exists,
- complex windows/sessions are required.

If latency requirements are relaxed:

```text
Kafka
 ↓
Spark Structured Streaming
 ↓
Iceberg
```

may be simpler.

---

## 21.4 Why Bronze Exists

Bronze preserves data near its source form.

Purpose:

```text
Replay
Audit
Debug
Reprocessing
New transformation
Historical source
```

Without durable raw history, transformation bugs can be harder to recover from.

---

## 21.5 Why Iceberg Exists

Object Storage alone provides files.

Iceberg adds the table abstraction:

```text
Schema
Snapshot
Metadata
Partition evolution
Atomic commits
Time travel
Update/Delete/Merge support
```

It allows multiple engines to work with a shared analytical table.

---

## 21.6 Why Spark Exists

Spark is the heavy data processing engine.

Use for:

```text
large ETL
large joins
aggregation
backfill
compaction
ML datasets
Silver/Gold transformations
```

It is compute, not storage.

---

## 21.7 Why dbt Exists

dbt manages SQL transformation logic.

Use for:

```text
staging
intermediate
marts
tests
documentation
lineage
metric-oriented modeling
```

Spark and dbt are complementary.

```text
Spark
→ heavy processing

dbt
→ SQL transformation management
```

---

## 21.8 Why Gold / Mart Exists

Gold is where data becomes business-consumption ready.

Examples:

```text
fact_agent_execution
fact_llm_call
dim_model
dim_team
mart_daily_ai_usage
```

BI users should not need to understand raw event internals.

---

## 21.9 Why Trino / SQL Warehouse Exists

Analytics users need interactive SQL.

```text
Iceberg Gold
 ↓
Trino
 ↓
Dashboard / Analyst
```

In managed platforms:

```text
Databricks SQL Warehouse
Snowflake Virtual Warehouse
```

can fill this role.

---

## 21.10 Why Airflow / Lakeflow Exists

Data processing is more than individual jobs.

Need:

```text
schedule
dependencies
retries
backfills
failure handling
parameters
alerts
```

Use:

```text
Airflow
→ cross-platform

Lakeflow Jobs
→ Databricks-centric
```

---

## 21.11 Why Data Quality Exists

Question:

> **Can we trust the data?**

Checks include:

```text
Completeness
Uniqueness
Validity
Consistency
Freshness
Accuracy
Volume
```

Use quarantine for invalid data rather than silently dropping it.

---

## 21.12 Why Data Observability Exists

Question:

> **Is the data healthy right now, and where is it becoming unhealthy?**

Observe:

```text
Freshness
Volume
Schema
Distribution
Pipeline Health
Data Health
```

Important:

```text
Pipeline Healthy
≠
Data Healthy
```

---

## 21.13 Why Metadata / Catalog Exists

As data grows, users ask:

```text
What tables exist?
What does this column mean?
Who owns it?
Is it fresh?
Is it trustworthy?
```

Catalog unifies discovery and context.

---

## 21.14 Why Lineage Exists

Lineage answers:

```text
Where did this data come from?
Where does it go?
What breaks if I change it?
```

Useful for:

- root cause,
- impact analysis,
- governance,
- debugging,
- sensitive data tracking.

---

## 21.15 Why Governance Exists

Governance answers:

```text
Who owns it?
Who can access it?
Is it sensitive?
Should it be masked?
How long should it be retained?
Who accessed it?
```

Capabilities:

```text
Ownership
Classification
Retention
Deletion
Masking
Row/Column Access
Audit
Data Contracts
```

---

## 21.16 Why AI-Ready Data Exists

AI-ready data combines:

```text
Trust
Freshness
Versioning
Discovery
Governance
Provenance
```

AI should not consume unmanaged enterprise data blindly.

---

## 21.17 AI Evaluation Architecture

```text
Production Agent
      ↓
Trace / Telemetry
      ↓
Langfuse / MLflow
      ↓
Scores / Feedback / Judge
      ↓
Evaluation Dataset
      ↓
Experiments
      ↓
Regression Dataset
```

Long-term:

```text
Telemetry / Evaluation
      ↓
Iceberg
      ↓
Spark / dbt
      ↓
Enterprise AI Analytics
```

---

## 21.18 Version Chain for Reproducibility

A production/evaluation result should ideally be linkable to:

```text
Agent Version
Prompt Version
Model Version
Tool Version
Retrieval Config
Embedding Version
Dataset Version
Evaluator Version
Git Commit
```

Concept:

```text
result
 ↓
experiment_id / trace_id
 ↓
all relevant versions
```

This is the basis of reproducibility.

---

## 21.19 Failure Behavior

A good architecture explanation must include failures.

### Kafka Failure

Events remain durable according to configured replication/retention.

Consumers can resume/replay.

### Flink Failure

Restore:

```text
Checkpoint / Savepoint
+
Source Offset
```

### Spark Failure

Retry failed tasks/jobs.

Jobs must be idempotent.

### Iceberg Write Failure

Uncommitted files may become orphan files.

Atomic metadata commit protects table consistency.

### Airflow Failure

Resume from failed tasks rather than rebuilding everything.

### CDC Failure

Restart from offsets; snapshot/re-bootstrap when required.

### Data Quality Failure

Contain and quarantine before publishing downstream.

---

## 21.20 Consistency Model

Different parts of the platform have different guarantees.

Examples:

```text
Kafka
→ partition ordering
→ at-least-once / transactional features depending on usage

Flink
→ checkpointed state
→ end-to-end exactly-once depends on source + state + sink

Iceberg
→ snapshot-based consistent table reads
→ atomic commits

dbt / Batch
→ correctness depends heavily on idempotent transformations
```

Never say:

> "The entire platform is exactly-once"

without defining the boundary.

---

## 21.21 Backfill Strategy

Preferred hierarchy:

```text
1. Rebuild only affected partition/range
2. Use Bronze history
3. Kafka replay when within retention
4. Source re-extraction if necessary
```

Backfill requirements:

```text
parameterized time range
idempotency
resource limits
quality verification
lineage awareness
```

---

## 21.22 Scaling Model

### Kafka

Scale with:

```text
partitions
brokers
consumer parallelism
```

### Flink

Scale:

```text
operator parallelism
task managers
state backend/resources
```

### Spark

Scale:

```text
executors
tasks
partitions
cluster/serverless compute
```

### Iceberg

Scale through:

```text
object storage
metadata
file layout
partitioning
compaction
```

### Trino / SQL

Scale:

```text
workers / warehouse size
concurrency
query optimization
```

Scaling one component does not automatically remove bottlenecks in another.

---

## 21.23 Cost Model

Cost appears at different layers:

```text
Kafka
→ brokers/storage/network

Flink
→ always-on stream compute/state

Spark
→ batch compute

Iceberg
→ object storage + maintenance

Trino
→ query compute

BI
→ concurrency

AI
→ tokens/inference/search
```

Platform cost optimization is architecture-wide.

Examples:

```text
Reduce unnecessary raw retention
Reduce scans
Improve file layout
Use incremental transforms
Avoid duplicate materialization
Right-size compute
```

---

## 21.24 What to Remove at Smaller Scale

This was one of the original curriculum goals:

> **Explain what should be removed when scale is smaller.**

### Very small system

Possible:

```text
Application
 ↓
PostgreSQL
 ↓
dbt / SQL
 ↓
BI
```

No Kafka.

No Flink.

No Iceberg.

No Trino.

No separate metadata platform.

### Small analytics platform

```text
PostgreSQL / Files
 ↓
Object Storage
 ↓
Spark or managed SQL
 ↓
Warehouse / Lakehouse
 ↓
BI
```

Still possibly no Kafka/Flink.

### Medium event-driven platform

```text
Application
 ↓
Kafka
 ↓
Spark Structured Streaming
 ↓
Iceberg
 ↓
Spark/dbt
 ↓
Trino
```

Flink may still be unnecessary.

### Large real-time platform

```text
Kafka
 ↓
Flink
 ↓
Iceberg
 ↓
Spark
 ↓
Trino
```

Add:

```text
Catalog
Observability
Quality
Governance
```

when organizational/data complexity justifies them.

### Principle

> **Do not deploy technology because it exists in a reference architecture. Add it when its problem actually exists.**

---

## 21.25 What Changes if Databricks Is Adopted

Self-managed:

```text
Spark
Trino
Airflow
Catalog
Lineage
MLflow
Vector DB
```

may partially collapse into:

```text
Databricks Runtime
SQL Warehouse
Lakeflow
Unity Catalog
MLflow
AI Search
```

Possible remaining components:

```text
Kafka
Flink
External dbt
Cross-platform Airflow
Special-purpose stores
```

Architecture becomes simpler operationally.

Trade-off:

```text
less platform engineering
+
faster integration

vs

more vendor dependency
+
platform cost
```

---

## 21.26 What Changes if Snowflake Is Adopted

Possible consolidation:

```text
Warehouse
SQL compute
Transformation
Dynamic Tables
Governance
Iceberg access
AI services
```

may move into Snowflake.

Possible remaining components:

```text
Kafka
Flink
external Spark
Airflow
special-purpose operational systems
```

Snowflake is especially natural when the organization is SQL/analytics-centered.

---

## 21.27 Open Lakehouse Final Architecture

A fully open-oriented implementation could be:

```text
Applications
    ↓
Kafka
    ↓
Flink
    ↓
Iceberg on S3
    ↓
Spark
    ↓
dbt
    ↓
Trino
    ↓
BI
```

Surrounding components:

```text
Airflow
→ orchestration

OpenLineage
→ lineage event standard

DataHub / OpenMetadata
→ catalog

Soda / Great Expectations
→ quality

Prometheus / Grafana
→ system observability

Data observability layer
→ freshness / volume / drift

MLflow / Langfuse
→ AI lifecycle
```

Strength:

```text
flexibility
portability
control
```

Weakness:

```text
integration burden
operations
upgrades
security integration
on-call complexity
```

---

## 21.28 Managed Platform Final Architecture

Databricks-centered example:

```text
Sources
 ↓
Kafka / Lakeflow Connect
 ↓
Lakeflow Pipelines / Spark Streaming
 ↓
Delta / Iceberg
 ↓
Databricks Runtime / dbt
 ↓
Gold
 ↓
SQL Warehouse
 ↓
BI

Unity Catalog
→ governance + lineage

Lakeflow Jobs
→ orchestration

MLflow
→ ML/AI lifecycle

AI Search
→ retrieval

Model Serving
→ inference
```

Snowflake-centered example:

```text
Sources
 ↓
Snowpipe / Streaming / External ingestion
 ↓
Snowflake / Iceberg
 ↓
Dynamic Tables / SQL Transform
 ↓
Data Marts
 ↓
Virtual Warehouses
 ↓
BI

Horizon
→ governance

Cortex / Search / Agents
→ AI
```

---

## 21.29 Final Architecture Decision Checklist

Before adding any component ask:

### Kafka

```text
Do we need replayable event transport?
Do multiple consumers need the same event?
```

### Flink

```text
Do we really need stateful low-latency streaming?
```

### Iceberg

```text
Do we need open object-storage analytical tables,
snapshots, multi-engine access, and large history?
```

### Spark

```text
Do we have large-scale transformation/backfill workloads?
```

### dbt

```text
Do we need SQL transformation governance and reusable models?
```

### Trino

```text
Do we need interactive SQL over open lakehouse data?
```

### Airflow

```text
Do workflows span multiple systems and need orchestration?
```

### Catalog / Lineage

```text
Has the organization reached a point where users cannot
reliably find, understand, or assess impact on data?
```

### Data Quality / Observability

```text
Would wrong or stale data create meaningful business damage?
```

### Managed Platform

```text
Is reducing operations/integration work worth the vendor cost/dependency?
```

---

# Final Mental Model

The entire study session can be compressed into this model:

```text
Sources
│
├─ Operational DB
│     ↓
│   CDC
│
└─ Events
      ↓
    Kafka
      ↓
Streaming Processing
      ↓
Raw / Bronze
      ↓
Lakehouse Table
      ↓
Batch Transformation
      ↓
Silver
      ↓
Modeling / dbt
      ↓
Gold / Marts
      ↓
SQL Serving
      ↓
BI / Analytics / AI
```

Cross-cutting planes:

```text
Orchestration
→ when and in what order

Quality
→ can we trust the data

Observability
→ is the data healthy now

Metadata / Catalog
→ what data exists

Lineage
→ where did it come from and where does it go

Governance
→ who can use it and how

AI Evaluation
→ how good are model/agent outputs

Versioning
→ what exact system produced this result

Cost
→ what resources are consumed

Recovery
→ how do we restore correct state after failure
```

Technology role map:

```text
PostgreSQL
→ operational state

Kafka
→ event log / transport

Debezium
→ database changes → event stream

Flink
→ stateful real-time processing

Spark
→ large-scale distributed processing

Parquet
→ columnar analytical file format

Iceberg
→ open lakehouse table format

dbt
→ SQL transformation management

Trino
→ interactive distributed SQL

Airflow / Lakeflow Jobs
→ orchestration

Data Quality tools
→ validation

Data Observability
→ freshness / volume / drift

OpenLineage
→ lineage event standard

Catalog
→ discovery / metadata

Governance
→ access / classification / audit

Langfuse / MLflow
→ AI telemetry / evaluation / experiments

Databricks / Snowflake
→ managed platforms that consolidate many of the above roles
```

---

# Final Engineering Principles

## Principle 1 — Start from the problem, not the tool

Bad:

```text
"We should use Kafka because modern platforms use Kafka."
```

Better:

```text
"We need replayable events consumed independently by five systems."
→ Kafka may be justified.
```

---

## Principle 2 — Keep roles clear

Avoid confusing:

```text
Storage
Table Format
Compute
Transformation
Query Engine
Orchestrator
Catalog
```

Example:

```text
S3
→ storage

Parquet
→ file format

Iceberg
→ table format

Spark
→ compute

dbt
→ transformation management

Trino
→ query engine

Airflow
→ orchestration
```

---

## Principle 3 — Design for reprocessing

Production pipelines will eventually need:

```text
retry
replay
backfill
rollback
```

Therefore:

- keep raw history when justified,
- make tasks idempotent,
- parameterize time ranges,
- version transformations,
- define source of truth.

---

## Principle 4 — Data correctness is separate from system health

```text
Job Success
≠
Correct Data
```

Observe both.

---

## Principle 5 — Version AI systems as systems

An AI output is produced by more than a model.

Version:

```text
Data
Prompt
Model
Agent
Tools
Retrieval
Evaluator
Code
```

---

## Principle 6 — Managed platforms trade control for integration

Open:

```text
more control
more portability
more platform work
```

Managed:

```text
less integration work
faster delivery
more vendor dependency
```

Neither is universally correct.

---

## Principle 7 — Remove components when they are not earning their operational cost

A mature platform is not one with the most technologies.

A mature platform is one where:

> **Every component exists because a real requirement justifies its complexity.**

---

# Study Session Status

**Data Platform Engineering overview curriculum completed.**

The learner should now be able to explain, at a high level:

- why OLTP and OLAP differ,
- why Parquet is columnar,
- why object storage is used,
- why Iceberg exists,
- how Spark and Flink differ,
- why Kafka exists,
- how CDC works,
- what Airflow/dbt/Trino do,
- how analytical models are structured,
- how quality and observability differ,
- what metadata, lineage, catalog, and governance do,
- what AI-ready data means,
- how AI telemetry/evaluation/versioning work,
- where Langfuse and MLflow fit,
- what Databricks consolidates,
- what Snowflake consolidates,
- how Open Lakehouse differs,
- how to reason about production failure/recovery,
- and how to simplify the architecture when scale is smaller.

This concludes the study session.

---

# Reference Notes for Current Platform Features

The conceptual comparison in Chapters 17–19 was aligned with current official documentation available during this session.

Key references used in the session include:

- Databricks Unity Catalog documentation
- Databricks Lakeflow Jobs documentation
- Databricks managed Delta/Iceberg table documentation
- Apache Iceberg REST Catalog specification
- Snowflake Dynamic Tables documentation
- Snowflake Horizon Catalog documentation
- Snowflake Iceberg documentation

These references are useful for checking product-specific behavior because managed-platform capabilities evolve quickly.
