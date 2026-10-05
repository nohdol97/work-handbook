---
id: ai-model-development-adapter-compatibility
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-02-01
  - AIMFT-02-02
  - AIMFT-02-03
  - AIMFT-02-04
---

# Chapter 2. Adapter Reuse and Base Model Changes

This page preserves the source numbering, order, and examples. For compatibility in 2.1–2.4, distinguish successful loading from actual quality. Read the separate supplement for model revisions, module settings, and tokenizer conditions. No adapter transfer or retraining was performed.

<!-- SOURCE CORE START -->

## 2.1 Can an Adapter Be Applied Unchanged to Another Model?

As a general rule, assume that an existing LoRA adapter cannot be applied unchanged to a different base model.

Example:

```text
Llama-3.1-8B
+
LoRA adapter for Llama
→ Possible
```

However:

```text
Mistral-7B
+
LoRA adapter for Llama
→ Generally not possible
```

The adapter was trained for the layer structure and dimensions of a specific base model.

---

## 2.2 Target Module Dependencies

LoRA attaches to specific linear layers inside a Transformer.

Example:

```text
q_proj
k_proj
v_proj
o_proj

gate_proj
up_proj
down_proj
```

The adapter configuration records which modules were trained.

Example:

```text
target_modules:
- q_proj
- v_proj
```

The same adapter weights cannot be applied if the target model's layer structure or dimensions differ.

---

## 2.3 Be Careful Even Within the Same Model Family

Being in the same Llama family does not guarantee adapter compatibility.

Example:

```text
Llama 8B Adapter
→ Llama 70B
```

This transfer cannot be made unchanged because the weight dimensions differ.

Manage at least the following information alongside the adapter.

```text
Base Model Name
Base Model Version / Revision
Adapter Type
LoRA Rank
LoRA Alpha
Target Modules
Training Dataset Version
```

---

## 2.4 What to Do When Changing the Base Model

When changing the base model, do not simply move the existing adapter.
Instead, fine-tune the new base model using the same training dataset.

Example:

```text
Training Dataset v3
      │
      ├─ Llama-3.1-8B
      │      ↓
      │   QLoRA
      │      ↓
      │   Adapter A
      │
      └─ Qwen
             ↓
          QLoRA
             ↓
          Adapter B
```

The adapter alone is not the only important long-term asset.

```text
Dataset
+
Training Configuration
+
Evaluation Dataset
+
Experiment History
```

Manage these assets together.

---

<!-- SOURCE CORE END -->

## Supplement — Loading Compatibility and Quality Checks

Official PEFT and Transformers documentation checked on 2026-10-05. These explanations and review recommendations are separate from the source; no transfer experiment was run. Check differences between `main` documentation and installed versions.

### 2.1 / 2.3 The Same Structure Does Not Guarantee the Same Result

Record the base model name and revision with the adapter configuration. A PEFT checkpoint does not contain the base weights themselves. [PEFT checkpoint](https://huggingface.co/docs/peft/main/en/developer_guides/checkpoint)

Review recommendation: matching dimensions may allow loading, but weights from another revision may differ from those used in training. Do not judge compatibility from names or successful loading alone. Check the actual base revision, tokenizer, chat template, and evaluation results together. [Evaluation data and model versions](../data-platform/ai-evaluation.md)

### 2.2 Target Module Names Depend on the Model

Names such as `q_proj` and `v_proj` are examples. PEFT `target_modules` accepts name lists, patterns, or supported broad selections, and must match the model structure. Implementations can extend LoRA beyond linear layers, so the source is not a list of every supported layer type. [PEFT LoRA configuration](https://huggingface.co/docs/peft/main/package_reference/lora)

### 2.4 Review Input Format When Reusing Data

Even when training samples keep the same meaning, models may use different tokenizers, special tokens, and chat templates. “The same dataset” in the source does not mean reusing the old model's token IDs unchanged. Check inputs and outputs processed for the new base model and keep evaluation conditions explicit. [Transformers chat templates](https://huggingface.co/docs/transformers/chat_templating)

## Related Topics

- [AI model development study map](index.md)
- [QLoRA and artifacts](qlora-artifacts.md)
- [Training datasets](training-datasets.md)
- [AI evaluation data platform](../data-platform/ai-evaluation.md)
