---
id: ai-model-development-model-retraining
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-06-01
  - AIMFT-06-02
  - AIMFT-06-03
---

# Chapter 6. Model Change and Re-Training

**Reading guide:** Source headings, numbers, tables, examples, and text diagrams are preserved in translation. Read **Supplements and Conditions by Source Section** after the source for conditions that affect real use. Values and settings are study examples. Training, deployment, and performance tests were not run for this page.

<!-- SOURCE CORE START -->

## 6.1 Flow When Replacing the Base Model

Suppose the production model changes from Llama to Qwen.

Before:

```text
Llama
+
Adapter v4
```

After:

```text
Qwen
+
New Adapter
```

Instead of reusing the existing Llama Adapter unchanged,
train a new Qwen Adapter with the existing Training Dataset.

---

## 6.2 Model Replacement Process

```text
1. Prepare the new Base Model
↓
2. Select the existing Training Dataset
↓
3. Apply QLoRA Fine-Tuning to the new Base Model
↓
4. Create a new Adapter
↓
5. Evaluate on the same Golden Dataset
↓
6. Compare with the current Production Model
↓
7. Check Quality / Cost / Latency criteria
↓
8. Promote or Reject
```

This process allows comparison under the same criteria even when the Base Model changes.

---

## 6.3 Why Datasets Are Long-Term Assets

Models can be replaced quickly.

The following can still be reused.

```text
Training Dataset
Validation Dataset
Golden Dataset
Evaluation Logic
Business Metric
```

Long-term AI Assets therefore go beyond:

```text
Model
```

and also include:

```text
Data
+
Evaluation
+
Experiment History
```

These are part of the lasting assets.

---

<!-- SOURCE CORE END -->

## Supplements and Conditions by Source Section

The official sources below were checked on 2026-10-05. These are review conditions before model replacement, not results from training Llama or Qwen.

### 6.1–6.2: Base Replacement and Dataset Reuse

When loading a PEFT adapter, check its match with the base used for training. A Llama adapter cannot simply be assumed to work on Qwen. Record the base revision, architecture, and target modules; train and evaluate a new adapter instead of changing a name. [PEFT troubleshooting](https://huggingface.co/docs/peft/main/developer_guides/troubleshooting)

Raw conversations may be reusable, but do not pass old token IDs unchanged to a new tokenizer. Prepare data again using the new model's tokenizer, chat template, special tokens, and length limit. Different models can require different token formats for the same conversation. [Chat templates](https://huggingface.co/docs/transformers/main/chat_templating)

Review recommendation: recheck dataset permissions, model licenses, and task scope. Use the same evaluation questions and criteria, but record each model's input format and serving settings. Define acceptable quality, cost, and latency ranges and a rollback target. Withhold promotion when evidence is insufficient.

### 6.3: Lasting Assets Still Need Updates

Data, evaluation, and experiment history are reusable assets, but their criteria do not stay correct forever. Update dataset versions and evaluation rules when policies, labels, or permissions change. Record the reason and a common evaluation scope to preserve comparison with older models. Review selection bias from repeated golden-set use with the [5.5–5.6 supplement](evaluation-promotion.md).

## Related Pages

[Adapter compatibility](adapter-compatibility.md) · [Training datasets](training-datasets.md) · [Evaluation and promotion](evaluation-promotion.md) · [Artifacts and lineage](artifact-lineage.md)
