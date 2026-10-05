---
id: ai-model-development-artifact-lineage
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-07-01
  - AIMFT-07-02
  - AIMFT-07-03
  - AIMFT-07-04
---

# Chapter 7. Model / Dataset Artifact Management

**Reading guide:** Source headings, numbers, tables, examples, and text diagrams are preserved in translation. Read **Supplements and Conditions by Source Section** after the source for conditions that affect real use. Values and settings are study examples. Training, deployment, and performance tests were not run for this page.

<!-- SOURCE CORE START -->

## 7.1 Example S3 Structure

```text
s3://ai-platform/
├─ datasets/
│  ├─ training/
│  │  ├─ v1/
│  │  ├─ v2/
│  │  └─ v3/
│  │
│  ├─ validation/
│  │  └─ v3/
│  │
│  └─ golden/
│     └─ v5/
│
└─ models/
   ├─ llama-3.1-8b/
   │  └─ adapters/
   │     ├─ v1/
   │     └─ v2/
   │
   └─ qwen/
      └─ adapters/
         └─ v1/
```

Object Storage holds the actual files.

Files alone do not easily show which Experiment produced them.

---

## 7.2 Link Metadata

The following Metadata can be linked to an Adapter.

```text
Adapter v5
├─ Base Model: Qwen
├─ Base Model Revision
├─ Training Dataset: train-v12
├─ Validation Dataset: validation-v12
├─ Golden Dataset: golden-v5
├─ Training Config: qlora-config-v2
├─ Training Run: run-20261005-001
└─ Evaluation Result: eval-20261005-003
```

These links make it possible to build a reproducible Training Pipeline.

---

## 7.3 The Role of the Model Registry

S3 stores Artifact files.

A Model Registry can manage the meaning and status of those Artifacts.

Example:

```text
S3
= Actual Adapter / Model Files

Model Registry
= Version / Metadata / Stage / Lineage Management
```

Example Stages:

```text
Candidate
↓
Validated
↓
Staging
↓
Production
↓
Archived
```

---

## 7.4 Training Lineage

The key is being able to trace the following relationships.

```text
Dataset Version
↓
Training Run
↓
Base Model
↓
Training Config
↓
Adapter Artifact
↓
Evaluation Result
↓
Deployment
```

When a problem occurs:

```text
For the current Production Model,
which Dataset was used for training,
which Config was used,
and which Evaluation did it pass?
```

You must be able to trace these details.

---

<!-- SOURCE CORE END -->

## Supplements and Conditions by Source Section

The official sources below were checked on 2026-10-05. S3 paths and run/eval IDs are study examples, not references to an actual repository or training run.

### 7.1: Prefixes and Immutable Artifacts

A prefix such as `v1/` is only a name; it does not prevent overwrites. S3 Versioning retains multiple object versions. For reproducible artifact references, record the key and versionId or a verifiable content hash. Versioning alone does not guarantee deletion protection or write-once storage. [S3 Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)

### 7.2, 7.4: Traceability and Reproducibility

Review recommendation: add tokenizer/chat-template revisions, code commits, library/container versions, seeds, quantization/generation settings, and dataset/artifact hashes to the source metadata. Keep checkpoint state separately if training must resume. These links alone do not guarantee bitwise identical results. PyTorch also notes that its deterministic-algorithm setting alone does not guarantee reproducibility for an entire application. [PyTorch deterministic algorithms](https://docs.pytorch.org/docs/main/generated/torch.use_deterministic_algorithms.html)

The straight arrows in 7.4 list concepts to trace. In actual lineage, the dataset, base model, and training config are run inputs. The adapter is an output, and evaluation and deployment refer to that artifact. Distinguish relation directions to trace which deployments a changed input affects. [Lineage and metadata](../data-platform/lineage-metadata.md)

### 7.3: Conceptual Stages and Registry Implementation

Candidate→Validated→Staging→Production→Archived is a design example. Not every registry provides these exact states. MLflow Model Stages have been deprecated since 2.9.0; current docs describe aliases, tags, and separate environments. Define states, approvals, and artifact references for your product and version. A registry state change also differs from successful serving deployment. [MLflow Model Registry workflows](https://mlflow.org/docs/latest/ml/model-registry/workflow/)

## Related Pages

[QLoRA artifacts](qlora-artifacts.md) · [Evaluation and promotion](evaluation-promotion.md) · [S3 storage](../aws-cloud/storage-databases.md) · [Lineage and metadata](../data-platform/lineage-metadata.md)
