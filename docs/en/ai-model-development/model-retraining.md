---
id: ai-model-development-model-retraining
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AIMFT-06-01
  - AIMFT-06-02
  - AIMFT-06-03
---

# Chapter 6. Model Change and Re-Training

The models and settings are study examples, not results of training, evaluation, or deployment.

<!-- SOURCE CORE START -->

## 6.1 Flow When Replacing the Base Model

Changing a base model is like replacing an engine while keeping its old tuning settings. Training data may be reused, but the adapter and evaluation must be checked for the new model.

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

**Base Replacement and Dataset Reuse**

When loading a PEFT adapter, check its match with the base used for training. A Llama adapter cannot simply be assumed to work on Qwen. Record the base revision, architecture, and target modules; train and evaluate a new adapter instead of changing a name. [PEFT troubleshooting](https://huggingface.co/docs/peft/main/developer_guides/troubleshooting)

Raw conversations may be reusable, but do not pass old token IDs unchanged to a new tokenizer. Prepare data again using the new model's tokenizer, chat template, special tokens, and length limit. Different models can require different token formats for the same conversation. [Chat templates](https://huggingface.co/docs/transformers/main/chat_templating)

Review recommendation: recheck dataset permissions, model licenses, and task scope. Use the same evaluation questions and criteria, but record each model's input format and serving settings. Define acceptable quality, cost, and latency ranges and a rollback target. Withhold promotion when evidence is insufficient.

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

**Lasting Assets Still Need Updates**

Data, evaluation, and experiment history are reusable assets, but their criteria do not stay correct forever. Update dataset versions and evaluation rules when policies, labels, or permissions change. Record the reason and a common evaluation scope to preserve comparison with older models. Review selection bias from repeated golden-set use with sections 5.5–5.6 of [Evaluation and promotion](evaluation-promotion.md).

---

<!-- SOURCE CORE END -->

## Key points

Do not carry an old adapter unchanged to a new base model. Even when data can be reused, recheck input format, training, and independent evaluation.


## Related Pages

[Adapter compatibility](adapter-compatibility.md) · [Training datasets](training-datasets.md) · [Evaluation and promotion](evaluation-promotion.md) · [Artifacts and lineage](artifact-lineage.md)
