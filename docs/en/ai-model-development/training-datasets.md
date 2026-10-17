---
id: ai-model-development-training-datasets
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AIMFT-03-01
  - AIMFT-03-02
  - AIMFT-03-03
  - AIMFT-03-04
  - AIMFT-03-05
  - AIMFT-03-06
  - AIMFT-03-07
---

# Chapter 3. Training Datasets and Golden Datasets

The models and settings are study examples, not results of training, evaluation, or deployment.

<!-- SOURCE CORE START -->

## 3.1 Core Assets for Fine-Tuning

Mixing training and evaluation data is like seeing exam questions while studying. Track similar samples from the same source as one group to judge performance honestly.

The base model can change over time.

Example:

```text
Llama
↓
Qwen
↓
Another new base model
```

Good training and evaluation datasets can be reused with new models.

From a platform perspective:

```text
Model Artifact
```

The following are just as important:

```text
Training Dataset
Golden Dataset
Dataset Version
Evaluation Result
```

These assets matter too.

---

## 3.2 Raw Documents and Training Datasets Are Different

Simply giving company document files to a model is not enough for fine-tuning.

Convert raw data into samples that fit the training objective.

```text
Raw Document
↓
Clean the data
↓
Extract the required information
↓
Create instructions / responses
↓
Training Sample
```

Example:

```text
User:
What should I check when Kafka consumer lag increases?

Assistant:
1. Check consumer processing speed
2. Check lag differences across partitions
3. Check downstream latency
4. Check whether rebalancing occurred
```

**Raw Text, Chat Templates, and Loss Scope**

TRL SFT supports language modeling and prompt-completion datasets, in both plain text and conversation formats. Converting data to instruction/response samples is one approach for a chosen objective. Not every training task requires QA conversion. Process the `messages` example with a chat template suited to the model. [TRL SFTTrainer](https://huggingface.co/docs/trl/main/en/sft_trainer)

User/assistant roles in `messages` do not by themselves restrict training to assistant tokens. TRL `assistant_only_loss=True` requires a chat template that provides the relevant loss mask. Check final tokens, labels, and truncation to ensure the target response remains in the training input. [TRL assistant-only loss](https://huggingface.co/docs/trl/main/en/sft_trainer#train-on-assistant-messages-only)

---

## 3.3 Chat-Format Training Samples

For LLM SFT, training datasets can use a format like this.

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What should I check when Kafka consumer lag increases?"
    },
    {
      "role": "assistant",
      "content": "Check consumer processing speed, lag by partition, downstream latency, and whether rebalancing occurred."
    }
  ]
}
```

Key idea:

```text
Input
→ Question / context given to the model

Target Output
→ The response you want the model to learn
```

These are their roles.

---

## 3.4 Dataset Separation

Separate and manage datasets by purpose.

```text
Full dataset
      │
      ├─ Training Dataset
      │
      ├─ Validation Dataset
      │
      └─ Golden Dataset
```

### Training Dataset

Used for actual gradient updates.

```text
Training Sample
↓
Forward
↓
Loss
↓
Backpropagation
↓
Adapter Update
```

### Validation Dataset

Used during training to check performance and overfitting.

### Golden Dataset

A fixed evaluation set for comparing the final models' actual quality.

**Split Units and Golden Dataset Use**

Golden dataset here means a fixed final evaluation holdout. Repeatedly selecting models or prompts based on its score can leak evaluation information into tuning, even without direct gradient updates. Use validation for selection and manage the independence of final evaluation. [Cross-validation and test sets](https://scikit-learn.org/stable/modules/cross_validation.html)

Application recommendation: if one document, conversation, or user produces multiple samples, consider keeping each source group in one split. Check duplicate documents and paraphrases as well as exact text matches. The 8,500/1,000/500 split is an example. Also check coverage of task categories, time periods, and rare failures. [Group splitting](https://scikit-learn.org/stable/modules/cross_validation.html#group-k-fold)

---

## 3.5 Role of the Golden Dataset

Think of a golden dataset as a set of exam questions.

```text
Base Model
↓
Golden Dataset Evaluation

Fine-Tuned Model A
↓
Evaluation on the same golden dataset

Fine-Tuned Model B
↓
Evaluation on the same golden dataset
```

Use the same questions to compare model quality.

Do not mix the golden dataset into the training dataset.

```text
Golden Dataset
→ Do not use for training
→ Use for final evaluation
```

---

## 3.6 Example Dataset Split

For example, with 10,000 samples:

```text
Training
→ 8,500

Validation
→ 1,000

Golden
→ 500
```

You could split them like this.

The exact ratio can vary with data volume and task characteristics,
but **separating the roles** of the datasets is important.

---

## 3.7 Dataset Versioning

Datasets need version control just like models.

Example:

```text
training-dataset-v1
training-dataset-v2
training-dataset-v3

golden-dataset-v1
golden-dataset-v2
```

Why it matters:

```text
Why model performance improved
```

Possible reasons:

```text
A model change
A dataset change
A training configuration change
```

You need to distinguish these causes.

**Versions and Evaluation Conditions**

The same dataset version does not make every comparison condition identical. Record model, tokenizer, template, rubric, generation settings, and preprocessing revisions together. Keep evaluation data out of preprocessing statistics and selection rules learned from data. [Avoiding data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage), [AI-ready data versions](../data-platform/ai-ready-data.md)

---

<!-- SOURCE CORE END -->

## Related Topics

- [AI model development study map](index.md)
- [QLoRA and artifacts](qlora-artifacts.md)
- [Adapter compatibility](adapter-compatibility.md)
- [AI-ready data](../data-platform/ai-ready-data.md)
- [AI evaluation data platform](../data-platform/ai-evaluation.md)

## Key points

Manage split rules and dataset versions together to prevent leakage and reproduce results.

## LLM in Practice: Review Data Leakage Before Training

**Prompt:**

=== "한국어"

    ```text {.prompt}
    학습 데이터와 golden 평가 데이터가 같은 원본 문서에서 나온 QA를 공유할 가능성이 있어. 현재 분할 규칙과 sample 출처를 검토해 원본 중복, 의역 중복, 시간 누수와 반복 튜닝 위험을 찾아 줘. 데이터를 옮기거나 학습을 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    Training and golden evaluation sets may contain QA samples from the same source document. Review the split rules and sample provenance for source overlap, paraphrases, time leakage, and repeated tuning against the golden set. Do not move data or run training.
    ```

**Key point:** A table separating confirmed leakage from hypotheses, affected samples and evaluation scope, minimal change candidates, and independent evaluation criteria. It may treat different strings as independent samples, miss paraphrases from the same document, or assume no leakage because golden data was not used for gradient updates. Compare actual group IDs and lineage, exact and approximate duplicate checks, split code/manifests, and model-selection and evaluation history. Check split independence and sample counts by task category separately after changes. This is a review example, not a completed leakage check or training run.
