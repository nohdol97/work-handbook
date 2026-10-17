---
id: ai-model-development-model-platform-collaboration
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AIMFT-09-01
  - AIMFT-09-02
  - AIMFT-09-03
---

# Chapter 9. AI Model Developers and AI Platform Engineers

The models and settings are study examples, not results of training, evaluation, or deployment.

<!-- SOURCE CORE START -->

## 9.1 Differences Between the Roles

Handing work from model development to the platform is like passing over both a design and the finished part. A model file alone can omit its base revision, tokenizer, resource needs, and evaluation evidence.

An AI model developer focuses on model quality.

```text
Which dataset?
Which base model?
Which fine-tuning method?
Which hyperparameters?
Did performance improve?
Why did it fail?
```

An AI platform engineer builds a platform that makes this process reliable and repeatable.

```text
Where should datasets be managed?
How should GPU training jobs run?
Where should artifacts be stored?
How should experiments be tracked?
How should evaluation be automated?
How should the model registry be organized?
How should models be served?
How should monitoring / rollback work?
```

---

## 9.2 Collaboration Example

Model developer request:

```text
Qwen
+
training-dataset-v12
+
QLoRA Rank 32
+
3 Epoch
```

The platform runs this request.

```text
Dataset Registry
↓
Training Job
↓
GPU
↓
Adapter Artifact
↓
S3
↓
Model Registry
↓
Golden Evaluation
↓
Deployment
```

After evaluation, the model developer reviews the results.

```text
Insufficient reasoning performance
↓
Improve training data
↓
Dataset v13
↓
Retraining
```

**Execution Requests and Deployment Decisions**

`Rank 32` and `3 Epoch` are example request values, not recommended defaults or quality guarantees. Recommendation: identify the exact base model revision, data and configuration versions, resource and cost limits, and evaluation criteria. Distinguish running an evaluation from passing quality criteria and having authority to enter production. Read sections 10.1 and 10.3 of [End-to-end training platform](training-platform-architecture.md) and the approval and capacity boundaries in [Developer platform](../platform-infrastructure/developer-platform.md).

**The Adapter Handoff Contract**

A PEFT adapter checkpoint usually does not include the entire base model. Handing over adapter files alone does not provide a complete serving model. Identify the exact base model revision, adapter configuration and weights, tokenizer and template, and compatible environment together. [PEFT checkpoint format](https://huggingface.co/docs/peft/developer_guides/checkpoint)

Recommendation: model developers record quality criteria, failure categories, and the intent of data changes. Platform owners record artifact links, execution environments, deployment state, and rollback paths. The organization should assign final decision owners for quantization, GPU memory, latency, packaging, and automated evaluation. Do not infer deployment authority from a role title alone.

---

## 9.3 Responsibility Boundaries Between Model Developers and the Platform

Conceptually:

```text
Model Developer
= What to learn and how to improve quality

AI Platform Engineer
= How to provide reliable training / evaluation / deployment processes
```

The roles are not fully separate. They have many areas of collaboration.

Examples:

```text
Quantization
GPU Memory
Serving Latency
Model Packaging
Evaluation Automation
```

These can be decided together.

---

<!-- SOURCE CORE END -->

## Key points

Model developers provide artifacts and quality evidence; the platform team assesses deployment, capacity, and safety. The handoff must identify versions and owners.


## Related Topics

- [The AI model developer's role](model-developer.md)
- [End-to-end training platform](training-platform-architecture.md)
- [AWS GPU model storage and permissions](../aws-cloud/ai-gpu-architecture.md)
- [CI/CD and GitOps](../platform-infrastructure/cicd-gitops.md)
