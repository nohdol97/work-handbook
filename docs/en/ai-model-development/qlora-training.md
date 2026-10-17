---
id: ai-model-development-qlora-training
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AIMFT-04-01
  - AIMFT-04-02
  - AIMFT-04-03
  - AIMFT-04-04
  - AIMFT-04-05
  - AIMFT-04-06
  - AIMFT-04-07
  - AIMFT-04-08
  - AIMFT-04-09
  - AIMFT-04-10
  - AIMFT-04-11
  - AIMFT-04-12
  - AIMFT-04-13
  - AIMFT-04-14
---

# Chapter 4. QLoRA Training Process

The models and settings are study examples, not results of training, evaluation, or deployment.

<!-- SOURCE CORE START -->

## 4.1 Overall Training Flow

QLoRA trains a small set of adjustment knobs instead of rebuilding a whole machine. It reduces resource needs, but data format, loss scope, and saving conditions still determine what the model learns.

The overall flow of QLoRA-based SFT is as follows.

```text
Define the problem
↓
Prepare the Training Dataset
↓
Select the Base Model
↓
4-bit Quantization
↓
Configure the LoRA Adapter
↓
Training
↓
Validation
↓
Save the Adapter Artifact
↓
Golden Dataset Evaluation
↓
Promote / Reject
```

---

## 4.2 Step 1 — Define the Training Goal

First, decide what to improve in the model.

Example:

```text
A response style suited to a specific task
Following a specific output Format
Improving classification accuracy
How to use Tools
Responses that follow company work Processes
```

The key point is:

> Not every problem needs to be solved with Fine-Tuning.

This is the principle to keep in mind.

---

## 4.3 Fine-Tuning vs RAG

Fine-Tuning mainly changes model behavior or how it performs tasks.

Example:

```text
"Answer in this format"
"Perform this task in this order"
"Apply these Classification criteria"
```

RAG may be more suitable for information that changes often or for searching company documents.

```text
"What is the current company policy?"
"Show me recently updated internal documents"
```

Conceptually:

```text
Behavior / Skill
→ Fine-Tuning

Changing Knowledge
→ RAG

Behavior + Knowledge
→ Fine-Tuning + RAG
```

---

## 4.4 Step 2 — Select the Base Model

Select the Base Model to fine-tune.

Example:

```text
Llama
Qwen
Gemma
Mistral
```

Factors to consider:

```text
Model Size
Model Quality
License
Language Performance
Context Length
GPU Requirement
Serving Cost
```

---

## 4.5 Step 3 — Base Model Quantization

QLoRA loads the Base Model in 4-bit form.

```text
Base Model
↓
4-bit Quantization
↓
Lower GPU Memory use
```

Keep the Base Model Weights Frozen
and train only the LoRA Adapter Parameters.

**, 4.10: Storage Precision and Trainable Parameters**

QLoRA trains adapters by passing gradients through a frozen 4-bit base. Frozen means the optimizer does not update base weights. It does not mean wrapping all base operations in `no_grad`. Weight storage precision and compute dtype are separate. [QLoRA paper](https://arxiv.org/abs/2305.14314), [PEFT quantization](https://huggingface.co/docs/peft/main/developer_guides/quantization)

Names such as `q_proj` and `v_proj` depend on the architecture. PEFT offers `target_modules="all-linear"` for QLoRA-style targeting. Rank 16 and alpha 32 are examples. Check actual modules and trainable parameters; evaluate performance separately. [PEFT quantization](https://huggingface.co/docs/peft/main/developer_guides/quantization)

---

## 4.6 Step 4 — Set LoRA Target Modules

Decide which Linear Layers in the Transformer will receive LoRA.

Example:

```text
Attention
├─ q_proj
├─ k_proj
├─ v_proj
└─ o_proj

Feed Forward
├─ gate_proj
├─ up_proj
└─ down_proj
```

Example configuration:

```text
LoRA Rank = 16
LoRA Alpha = 32
Target Modules = q_proj, v_proj
```

You can also target multiple Linear Layers in a QLoRA-style setup.

---

## 4.7 Step 5 — Tokenization

A Training Sample does not enter the Neural Network as raw text.

The Tokenizer converts Text to Token IDs.

```text
Text
↓
Tokenizer
↓
Token
↓
Token ID
↓
Model Input
```

Example:

```text
"Explain the difference between Redis and Kafka"
↓
[151644, 872, 25, ...]
```

The result takes this form.

**Tokenizers and the Meaning of Loss**

The token IDs are illustrative, not universal IDs for that sentence. Use the tokenizer and chat template for the base model. Check roles, special tokens, and EOS handling in training samples. [Chat templates](https://huggingface.co/docs/transformers/main/chat_templating)

Typical causal SFT loss uses predictions for target tokens. It is not a simple comparison of two output sentences. TRL settings such as `assistant_only_loss` change which tokens contribute to loss and require supported templates. Inspect the actual labels and masks. [TRL SFT Trainer](https://huggingface.co/docs/trl/main/sft_trainer)

---

## 4.8 Step 6 — Forward Pass

The model receives Tokenized Input and predicts next-token probabilities.

```text
Training Sample
↓
Tokenizer
↓
Base Model + LoRA
↓
Prediction
```

Example:

```text
Ground Truth:
Redis is an In-Memory Data Store, and Kafka is an Event Streaming Platform.

Model Prediction:
Redis and Kafka are both Databases.
```

As shown above, the Prediction may differ from the correct answer.

---

## 4.9 Step 7 — Calculate Loss

Loss measures the difference between the model's predictions and the correct answers.

```text
Prediction
↕
Ground Truth
↓
Loss
```

Example:

```text
Loss = 2.41
```

Training aims to reduce Loss.

---

## 4.10 Step 8 — Backpropagation

Calculate Gradients from the Loss.

QLoRA does not update all the Base Model Weights.

```text
Base Model Weight
→ Frozen
→ Update X

LoRA Adapter
→ Trainable
→ Update O
```

In other words:

```text
Loss
↓
Gradient
↓
LoRA A / B Weight Update
```

Repeat this process.

---

## 4.11 Step 9 — Batch / Step / Epoch

Training can repeat over the entire Training Dataset several times.

Example:

```text
Training Dataset
10,000 Samples

Epoch 1
→ Train on the entire Dataset

Epoch 2
→ Train on the entire Dataset again

Epoch 3
→ Train on the entire Dataset again
```

One pass through the entire Dataset is an Epoch.

In actual Training, Samples are processed in Batches and Parameters are updated.

**Microbatches and Optimizer Steps**

Gradient accumulation combines gradients from several microbatches before an optimizer update. “Update by Batch” does not mean every microbatch updates parameters. In standard data parallelism, effective batch size is `per-device batch × data-parallel workers × accumulation steps`; check incomplete final batches separately. [Transformers Trainer](https://huggingface.co/docs/transformers/main/main_classes/trainer)

Review recommendation: Experiments A and B change both learning rate and rank. Do not attribute a result to one variable alone. Also record the dataset, lengths, masks, seed, and evaluation conditions. Low loss alone does not establish better quality.

---

## 4.12 Key Training Parameters

Common Parameters that an AI Model Developer adjusts:

```text
Learning Rate
Batch Size
Epoch
Sequence Length
LoRA Rank
LoRA Alpha
Target Modules
Optimizer
Gradient Accumulation
```

Example:

```text
Experiment A
Learning Rate = 1e-4
Rank = 16

Experiment B
Learning Rate = 2e-4
Rank = 32

Experiment C
Dataset = v2
Rank = 16
```

A Training Run can be seen as the following combination.

```text
Dataset
+
Base Model
+
Training Configuration
=
Experiment
```

---

## 4.13 Metrics to Check During Training

You can check the following during training.

```text
Training Loss
Validation Loss
Learning Rate
Gradient Norm
GPU Memory
Training Throughput
```

Reducing Training Loss alone is not the goal.

Also check Validation performance and Evaluation on real work tasks.

---

## 4.14 Save Training Results

Save the Adapter after training.

```text
Training Job
↓
QLoRA Adapter
↓
adapter_model.safetensors
adapter_config.json
↓
S3
```

It can then be linked to Metadata in the Model Registry.

**Adapter Saving and Training Resume**

PEFT adapter checkpoints do not contain base model weights. Saving the two source files does not create a standalone full model. To resume training, also check optimizer, scheduler, RNG, and other resume state. [PEFT checkpoint](https://huggingface.co/docs/peft/main/developer_guides/checkpoint), [Transformers Trainer](https://huggingface.co/docs/transformers/main/main_classes/trainer)

---

<!-- SOURCE CORE END -->

## Related Pages

[Training datasets](training-datasets.md) · [Evaluation and promotion](evaluation-promotion.md) · [Artifacts and lineage](artifact-lineage.md) · [GPU infrastructure](../platform-infrastructure/gpu-infrastructure.md)

## Key points

QLoRA freezes the base model and trains a small adapter to reduce resource needs. Keep configuration, data versions, and evaluation results together for reproducibility.

## LLM in Practice: Review a QLoRA Training Configuration

**Prompt:**

=== "한국어"

    ```text {.prompt}
    이 저장소의 QLoRA 학습 설정과 저장 계획을 검토해 줘. Base Model 버전, quantization, target module, tokenization, loss 범위, 유효 batch와 optimizer step이 서로 맞는지 확인하고 근거가 부족한 설정은 질문으로 남겨 줘. 비밀값을 노출하거나 학습을 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Review this repository’s QLoRA training configuration and saving plan. Check whether the base-model version, quantization, target modules, tokenization, loss scope, effective batch, and optimizer steps fit together. Flag missing evidence as questions. Do not reveal secrets or run training.
    ```

**Key point:** A review table by training stage, an effective batch calculation of 32 under standard data-parallel assumptions, essential unknowns, and checks for training and promotion decisions. It may guarantee memory fit or quality from rank alone, assume all models use the same target names, or recommend deployment based only on low loss. Compare actual modules, label masks, installed versions, and settings. In an authorized small test, check updates, saving, and reloading; then use separate evaluation. This page does not record running that test or training.
