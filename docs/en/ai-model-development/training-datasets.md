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

This page preserves the source numbering, order, and JSON example. See the separate supplement for training formats and loss scope in 3.2–3.3, and split leakage and golden dataset conditions in 3.4–3.7. These are not results from dataset construction, training, or evaluation.

<!-- SOURCE CORE START -->

## 3.1 Core Assets for Fine-Tuning

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
    하나의 원본 문서에서 만든 여러 QA sample이 train과 golden 양쪽에 들어갔을 가능성을 검토하는 가상 사례다.
    먼저 현재 분할을 평가하고 관측·가정·누수 가설을 구분하라.
    원본 group 중복, 의역·정답 중복, 시간 누수, golden 점수 반복 튜닝을 따로 점검하라.
    필수 근거가 없으면 우선순위 질문 최대 3개를 제시하고 해당 결론을 유보하라.
    누수 경로 / 근거 ID / 영향 범위 / 미확인 정보 / 최소 수정 후보 / 확인 기준 표를 작성하라.
    비밀값은 요구하거나 출력하지 말고, 검토안만 작성해 줘. 변경은 실행하지 마.
    ```

=== "English"

    ```text {.prompt}
    A hypothetical review of whether multiple QA samples from one source document appear in both training and golden splits.
    Assess the existing split first. Separate observations, assumptions, and leakage hypotheses.
    Check source-group overlap, paraphrase or answer overlap, time leakage, and repeated tuning on golden scores separately.
    Make a table: leakage path / evidence IDs / scope / unknowns / minimal change candidate / check criteria.
    Do not request or reveal secrets. Draft a review only; do not apply changes.
    ```

**Key point:** A table separating confirmed leakage from hypotheses, affected samples and evaluation scope, minimal change candidates, and independent evaluation criteria. It may treat different strings as independent samples, miss paraphrases from the same document, or assume no leakage because golden data was not used for gradient updates. Compare actual group IDs and lineage, exact and approximate duplicate checks, split code/manifests, and model-selection and evaluation history. Check split independence and sample counts by task category separately after changes. This is a review example, not a completed leakage check or training run.

## Supplement — Training Inputs and Data Leakage

Official TRL and scikit-learn documentation checked on 2026-10-05. Some recommendations apply scikit-learn evaluation and splitting principles to the source's LLM datasets. TRL `main` is development documentation; check the installed version's behavior. No training or evaluation was run.

### 3.2 / 3.3 Raw Text, Chat Templates, and Loss Scope

TRL SFT supports language modeling and prompt-completion datasets, in both plain text and conversation formats. Converting data to instruction/response samples is one approach for a chosen objective. Not every training task requires QA conversion. Process the `messages` example with a chat template suited to the model. [TRL SFTTrainer](https://huggingface.co/docs/trl/main/en/sft_trainer)

User/assistant roles in `messages` do not by themselves restrict training to assistant tokens. TRL `assistant_only_loss=True` requires a chat template that provides the relevant loss mask. Check final tokens, labels, and truncation to ensure the target response remains in the training input. [TRL assistant-only loss](https://huggingface.co/docs/trl/main/en/sft_trainer#train-on-assistant-messages-only)

### 3.4–3.6 Split Units and Golden Dataset Use

Golden dataset here means a fixed final evaluation holdout. Repeatedly selecting models or prompts based on its score can leak evaluation information into tuning, even without direct gradient updates. Use validation for selection and manage the independence of final evaluation. [Cross-validation and test sets](https://scikit-learn.org/stable/modules/cross_validation.html)

Application recommendation: if one document, conversation, or user produces multiple samples, consider keeping each source group in one split. Check duplicate documents and paraphrases as well as exact text matches. The 8,500/1,000/500 split is an example. Also check coverage of task categories, time periods, and rare failures. [Group splitting](https://scikit-learn.org/stable/modules/cross_validation.html#group-k-fold)

### 3.7 Versions and Evaluation Conditions

The same dataset version does not make every comparison condition identical. Record model, tokenizer, template, rubric, generation settings, and preprocessing revisions together. Keep evaluation data out of preprocessing statistics and selection rules learned from data. [Avoiding data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage), [AI-ready data versions](../data-platform/ai-ready-data.md)
