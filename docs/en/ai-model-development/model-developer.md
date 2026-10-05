---
id: ai-model-development-model-developer
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AIMFT-08-01
  - AIMFT-08-02
  - AIMFT-08-03
  - AIMFT-08-04
  - AIMFT-08-05
  - AIMFT-08-06
  - AIMFT-08-07
  - AIMFT-08-08
---

# Chapter 8. The AI Model Developer's Role

These notes preserve AI Model / QLoRA Training Basic Chapter 8. They do not claim real model-training or deployment experience.

**Reading guide:** The source headings, numbers, paragraphs, lists, and text diagrams are preserved in translation. Read **Supplements and Conditions by Source Section** for training-method categories in 8.4, evaluation independence in 8.3, 8.5, and 8.7–8.8, and quantization effects in 8.6–8.7. Code and commands were not run.

<!-- SOURCE CORE START -->

## 8.1 Core Role of an AI Model Developer

An AI model developer who fine-tunes an existing foundation model for a company or service
is more than someone who runs a training script.

The core work is:

```text
Which problem should we solve?
↓
Which data should we use?
↓
Which model should we choose?
↓
How should we train it?
↓
How should we evaluate it?
↓
Why did it fail?
↓
How can we improve it?
```

Make these decisions repeatedly.

---

## 8.2 Problem Definition

First, define what you want to improve.

Examples:

```text
Accuracy on business tasks
A specific output format
Instruction Following
Classification
Reasoning Pattern
Tool Use
```

Then:

```text
Is fine-tuning needed?
Can RAG solve the problem?
Is prompt engineering enough?
```

Decide among these options.

---

## 8.3 Dataset Design

Dataset design is an important part of an AI model developer's role.

Tasks include:

- Select good samples
- Remove incorrect answers
- Remove duplicate data
- Remove low-quality data
- Convert data to the required instruction / response format
- Check the data distribution
- Separate train / validation / golden sets
- Manage dataset versions

In other words:

```text
Garbage Data
↓
Hard to build a good model
```

This is why dataset quality matters so much.

---

## 8.4 Choosing a Training Strategy

Choose a training method based on the problem and available resources.

Examples:

```text
Full Fine-Tuning
LoRA
QLoRA
SFT
Preference Training
```

For example, if GPU resources are limited:

```text
Large Model Full Fine-Tuning
→ High cost

Smaller Model + QLoRA
→ A more practical option
```

These are decisions you may make.

---

## 8.5 Hyperparameter Tuning

Common values to tune:

```text
Learning Rate
Batch Size
Epoch
LoRA Rank
LoRA Alpha
Target Modules
Sequence Length
Optimizer
```

Compare several experiments instead of using only one configuration.

```text
Experiment A
↓
Evaluate

Experiment B
↓
Evaluate

Experiment C
↓
Evaluate
```

Then choose the best result.

---

## 8.6 Considering Quantization

AI model developers may also decide on quantization based on training and serving resources.

Distinction:

```text
Training Quantization
→ QLoRA and similar methods
→ Reduce GPU memory for training

Serving Quantization
→ FP8 / INT8 / INT4 and similar formats
→ Reduce inference memory / cost
```

These two areas have different goals.

Serving quantization can be decided together with an AI serving / platform engineer.

---

## 8.7 Evaluation

Evaluation is a core responsibility of model developers.

Questions to check:

```text
Did fine-tuning actually improve the model?
Did some areas improve while others got worse?
Did hallucinations increase?
Does it follow the output format?
Does it meet production latency requirements?
```

Therefore:

```text
Golden Dataset
+
Evaluation Metric
+
Error Analysis
```

These are important.

---

## 8.8 Error Analysis and Dataset Improvement

Inspect incorrect model answers to determine whether the issue lies in the data or the model.

```text
Evaluation Failure
↓
Classify failure categories
↓
Identify gaps in the dataset
↓
Add / clean data
↓
Dataset New Version
↓
Retraining
```

Repeat this loop to improve the model.

---

<!-- SOURCE CORE END -->

## Supplements and Conditions by Source Section

Official documents were checked on 2026-10-05. These additions sit outside the source and are not results from training or evaluating a model.

### 8.4: Different Ways to Classify Training Methods

Full fine-tuning and LoRA mainly differ in which parameters are trained. QLoRA combines a quantized base model with LoRA training. SFT and preference training describe training objectives and data signals. These are not five mutually exclusive choices. For example, SFT can use QLoRA. [PEFT quantization](https://huggingface.co/docs/peft/developer_guides/quantization), [TRL SFT Trainer](https://huggingface.co/docs/trl/sft_trainer)

### 8.3, 8.5, 8.7–8.8: Selection Data and Independent Evaluation

Data used repeatedly to choose hyperparameters or models influences that choice. Calling it golden does not guarantee an independent final evaluation. Recommendation: separate a fixed regression suite from an unused holdout checked after final selection. Learn general training needs from failure categories, but do not copy final evaluation answers into training. Distinguish performance selected through repeated checks on the same cases from performance on new cases. [Cross-validation and test-set separation](https://scikit-learn.org/stable/modules/cross_validation.html)

### 8.6–8.7: Quantization and Production Performance

Training and serving quantization differ in purpose. Also check supported kernels, hardware, and formats. Lower precision does not always guarantee lower latency or cost. Recommendation: measure quality, TTFT/TPOT, throughput, and memory together under the same evaluation conditions on the target GPU. [vLLM quantization support](https://docs.vllm.ai/en/latest/features/quantization/)

## Related Topics

- [Model developer and platform collaboration](model-platform-collaboration.md)
- [End-to-end training platform](training-platform-architecture.md)
- [GPU infrastructure and capacity](../platform-infrastructure/gpu-infrastructure.md)
- [vLLM serving](../platform-infrastructure/vllm.md)
