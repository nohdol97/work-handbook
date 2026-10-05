---
id: ai-model-development-qlora-artifacts
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-01-01
  - AIMFT-01-02
  - AIMFT-01-03
  - AIMFT-01-04
  - AIMFT-01-05
  - AIMFT-01-06
  - AIMFT-01-07
  - AIMFT-01-08
---

# Chapter 1. QLoRA and Training Artifacts

This page preserves the source numbering, order, and examples. **The A/B matrix dimensions in 1.2 do not match the `B × A` formula.** See the correction after the source, along with precision in 1.3, saved files in 1.4, and serving/merge conditions in 1.7–1.8. No training, model saving, or deployment was performed.

<!-- SOURCE CORE START -->

## 1.1 QLoRA Fundamentals

QLoRA does not directly train all the base model weights.
It trains only small LoRA adapters while keeping the base model quantized.

Basic structure:

```text
Base Model
Examples: Llama / Qwen / Gemma
↓
4-bit Quantization
↓
Frozen Base Model
+
Trainable LoRA Adapter
↓
Fine-Tuning
```

Key points:

```text
Base Model Weight
→ Mostly frozen

LoRA Adapter Weight
→ Trainable
```

The result of QLoRA training is therefore usually not a new full model,
but **an adapter used together with the base model**.

---

## 1.2 What LoRA Learns

For an existing weight `W`, LoRA learns a small update instead of changing the whole weight.

```text
W' = W + ΔW
```

LoRA represents `ΔW` with two small matrices.

```text
ΔW = B × A
```

Example:

```text
Original Weight
4096 x 4096

LoRA
A: 4096 x 16
B: 16 x 4096
```

This can greatly reduce the number of trainable parameters compared with training all the weights again.

---

## 1.3 What Quantization Means in QLoRA

The `Q` in QLoRA stands for quantization.

Regular LoRA:

```text
Base Model
FP16 / BF16
+
LoRA Adapter
```

QLoRA:

```text
Base Model
4-bit
+
LoRA Adapter
```

Conceptually:

```text
Model weight storage
→ 4-bit

Actual computation
→ Can use higher precision such as BF16
```

Goals:

- Reduce GPU memory use
- Fine-tune large models with fewer GPU resources
- Reduce training cost compared with full fine-tuning

---

## 1.4 QLoRA Training Artifacts

Training results can be saved in files such as these.

```text
adapter_model.safetensors
adapter_config.json
tokenizer.json
tokenizer_config.json
training_args.json
metadata.json
```

Core artifact:

```text
adapter_model.safetensors
```

This file stores the trained LoRA adapter weights.

---

## 1.5 Storing Artifacts in S3

An AI platform can store training results in object storage.

AWS example:

```text
s3://model-artifacts/
└─ customer-support-v1/
   ├─ adapter_model.safetensors
   ├─ adapter_config.json
   ├─ tokenizer.json
   ├─ training_args.json
   └─ metadata.json
```

In other words:

```text
Training Job
↓
Create a LoRA adapter
↓
Store artifacts in S3
↓
Register in the model registry
↓
Evaluation / Deployment
```

These steps can form a workflow.

---

## 1.6 Relationship Between the Base Model and Adapter

Inference uses the base model and adapter together.

```text
Base Model
Qwen / Llama
     +
LoRA Adapter
     ↓
Fine-Tuned Behavior
```

Example:

```text
Llama-3.1-8B
+
SQL Adapter
```

Or:

```text
Llama-3.1-8B
+
Customer Support Adapter
```

Adapters for different purposes can be created for the same base model, as shown here.

---

## 1.7 Operating Multiple Adapters

Multiple adapters can be managed separately for one base model.

```text
Llama-3.1-8B
├─ Adapter A: SQL
├─ Adapter B: Coding
├─ Adapter C: Customer Support
└─ Adapter D: Internal QA
```

If the serving engine supports loading LoRA adapters,
you can share a base model and select an adapter for each request.

Concept:

```text
                    ┌─ Finance Adapter
                    │
Base Model ─────────┼─ Coding Adapter
                    │
                    └─ Internal QA Adapter
```

This can reduce the cost of storing or loading the base model onto GPUs multiple times.

---

## 1.8 Merging an Adapter into a Full Model

LoRA adapters can also be merged into the base model weights.

```text
Base Model
+
LoRA Adapter
↓
Merge
↓
Fine-Tuned Full Model
```

Example:

```text
Qwen Base Model
+
Adapter v3
↓
Merged Model
```

Storage comparison:

```text
Store only the adapter
→ Relatively small

Store the merged full model
→ Includes all base model weights
→ Much larger
```

For a platform managing several fine-tuned versions,
managing base models and adapters separately is often efficient.

---

<!-- SOURCE CORE END -->

## Supplement — Matrix Correction and Artifact Conditions

LoRA and QLoRA papers and official PEFT, Transformers, and vLLM documentation checked on 2026-10-05. `main`/`latest` documentation can change; pin the actual installed versions separately. Nothing was executed for this page.

### 1.1–1.3 Frozen Weights and Storage/Compute Precision

The QLoRA paper passes gradients through a frozen 4-bit base model into LoRA adapters. “Mostly frozen” in the source does not mean that standard QLoRA updates base weights. NF4, double quantization, and paged optimizers are also part of the paper's memory-saving design. Four-bit storage does not mean every operation uses four bits. Check settings such as bitsandbytes `bnb_4bit_compute_dtype` separately. [QLoRA paper](https://arxiv.org/abs/2305.14314), [Transformers BitsAndBytesConfig](https://huggingface.co/docs/transformers/main_classes/quantization#transformers.BitsAndBytesConfig)

### 1.2 Correcting A/B Dimensions

For a `4096 × 4096` weight `W` and `ΔW = B × A`, standard LoRA notation uses `A: 16 × 4096` and `B: 4096 × 16`. With the source's dimensions, `B × A` instead produces `16 × 16`, which cannot be added to `W`. Keeping those dimensions would require `A × B`. Basic LoRA also uses `α/r` scaling; the source's conceptual formula omits that factor. [LoRA paper §4.1](https://arxiv.org/html/2106.09685)

### 1.4 / 1.8 Saved Files and Merging

A PEFT adapter primarily needs adapter weights and `adapter_config.json`. Tokenizer files, training arguments, and custom metadata depend on separate saving steps. The source list is not every tool's automatic output. Merge support varies by method and quantization settings. The result of `merge_and_unload()` does not retain PEFT adapter switching. [PEFT checkpoint](https://huggingface.co/docs/peft/main/en/developer_guides/checkpoint)

### 1.7 Check Serving Support

With vLLM, check model LoRA support and settings such as `enable_lora`, `max_loras`, and `max_lora_rank`. Having multiple adapter files does not guarantee per-request switching or target throughput under concurrency. [vLLM LoRA](https://docs.vllm.ai/en/latest/features/lora/)

## Related Topics

- [AI model development study map](index.md)
- [Adapter compatibility](adapter-compatibility.md)
- [Training datasets](training-datasets.md)
- [vLLM serving](../platform-infrastructure/vllm.md)
- [AWS object storage](../aws-cloud/storage-databases.md)
