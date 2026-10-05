---
items:
- id: AIMFT-00-01
  knowledge: "# AI Model Fine-Tuning / QLoRA Basic\n## Source Markdown — QLoRA, Dataset,\
    \ Training, Evaluation, Model Developer Role\n\n> 이 문서는 이 학습 세션에서 진행한 **QLoRA\
    \ 기반 LLM Fine-Tuning과 AI Model Developer 역할**을 정리한 source markdown이다.  \n> 범위:\
    \ **QLoRA Artifact → Dataset / Golden Dataset → Training Process → Evaluation\
    \ → Model Developer / AI Platform 역할 구분**\n\n---"
  kind: scope
  source_lines: 1–8
  destination: ai-model-development/index.md
- id: AIMFT-01-01
  knowledge: '## 1.1 QLoRA 기본 개념


    QLoRA는 Base Model 전체 Weight를 직접 학습하는 방식이 아니라,

    Base Model을 Quantization한 상태에서 작은 LoRA Adapter만 학습하는 방식이다.


    기본 구조:


    ```text

    Base Model

    예: Llama / Qwen / Gemma

    ↓

    4-bit Quantization

    ↓

    Frozen Base Model

    +

    Trainable LoRA Adapter

    ↓

    Fine-Tuning

    ```


    핵심:


    ```text

    Base Model Weight

    → 대부분 고정


    LoRA Adapter Weight

    → 학습

    ```


    따라서 QLoRA 학습 결과물은 일반적으로 새로운 Full Model 전체라기보다

    **Base Model에 추가해서 사용하는 Adapter**이다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 11–45
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-02
  knowledge: '## 1.2 LoRA가 학습하는 것


    기존 Weight를 `W`라고 하면 LoRA는 Weight 전체를 수정하는 대신 작은 변화량을 학습한다.


    ```text

    W'' = W + ΔW

    ```


    LoRA는 `ΔW`를 작은 두 Matrix로 표현한다.


    ```text

    ΔW = B × A

    ```


    예:


    ```text

    Original Weight

    4096 x 4096


    LoRA

    A: 4096 x 16

    B: 16 x 4096

    ```


    따라서 전체 Weight를 다시 학습하는 것보다 학습해야 하는 Parameter 수를 크게 줄일 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 46–74
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-03
  knowledge: '## 1.3 QLoRA에서 Quantization의 의미


    QLoRA의 `Q`는 Quantization을 의미한다.


    일반 LoRA:


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


    개념적으로:


    ```text

    Model Weight 저장

    → 4-bit


    실제 연산

    → BF16 등의 더 높은 Precision 사용 가능

    ```


    목적:


    - GPU Memory 사용량 감소

    - 큰 모델을 상대적으로 적은 GPU Resource로 Fine-Tuning

    - Full Fine-Tuning 대비 학습 비용 감소


    ---'
  kind: concept,example,condition,workflow
  source_lines: 75–114
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-04
  knowledge: '## 1.4 QLoRA 학습 결과 Artifact


    학습 결과는 다음과 같은 파일로 저장할 수 있다.


    ```text

    adapter_model.safetensors

    adapter_config.json

    tokenizer.json

    tokenizer_config.json

    training_args.json

    metadata.json

    ```


    핵심 Artifact:


    ```text

    adapter_model.safetensors

    ```


    이 파일에 학습된 LoRA Adapter Weight가 저장된다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 115–137
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-05
  knowledge: "## 1.5 S3에 Artifact 저장\n\nAI Platform에서는 학습 결과를 Object Storage에 저장할\
    \ 수 있다.\n\nAWS 예:\n\n```text\ns3://model-artifacts/\n└─ customer-support-v1/\n\
    \   ├─ adapter_model.safetensors\n   ├─ adapter_config.json\n   ├─ tokenizer.json\n\
    \   ├─ training_args.json\n   └─ metadata.json\n```\n\n즉:\n\n```text\nTraining\
    \ Job\n↓\nLoRA Adapter 생성\n↓\nS3 Artifact 저장\n↓\nModel Registry 등록\n↓\nEvaluation\
    \ / Deployment\n```\n\n형태로 연결할 수 있다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 138–171
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-06
  knowledge: "## 1.6 Base Model과 Adapter 관계\n\nInference 시에는 Base Model과 Adapter를\
    \ 함께 사용한다.\n\n```text\nBase Model\nQwen / Llama\n     +\nLoRA Adapter\n     ↓\n\
    Fine-Tuned Behavior\n```\n\n예:\n\n```text\nLlama-3.1-8B\n+\nSQL Adapter\n```\n\
    \n또는:\n\n```text\nLlama-3.1-8B\n+\nCustomer Support Adapter\n```\n\n처럼 같은 Base\
    \ Model에 서로 다른 목적의 Adapter를 만들 수 있다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 172–204
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-07
  knowledge: "## 1.7 여러 Adapter 운영\n\n하나의 Base Model에 여러 Adapter를 따로 관리할 수 있다.\n\n\
    ```text\nLlama-3.1-8B\n├─ Adapter A: SQL\n├─ Adapter B: Coding\n├─ Adapter C:\
    \ Customer Support\n└─ Adapter D: Internal QA\n```\n\nServing Engine이 LoRA Adapter\
    \ Loading을 지원한다면\nBase Model을 공유하면서 요청에 따라 Adapter를 선택하는 형태도 가능하다.\n\n개념:\n\n\
    ```text\n                    ┌─ Finance Adapter\n                    │\nBase Model\
    \ ─────────┼─ Coding Adapter\n                    │\n                    └─ Internal\
    \ QA Adapter\n```\n\n이 구조는 Base Model을 여러 번 저장하거나 GPU에 여러 번 올리는 비용을 줄이는 데 도움이\
    \ 될 수 있다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 205–233
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-01-08
  knowledge: '## 1.8 Adapter와 Full Model Merge


    LoRA Adapter는 Base Model Weight에 Merge할 수도 있다.


    ```text

    Base Model

    +

    LoRA Adapter

    ↓

    Merge

    ↓

    Fine-Tuned Full Model

    ```


    예:


    ```text

    Qwen Base Model

    +

    Adapter v3

    ↓

    Merged Model

    ```


    저장 방식 비교:


    ```text

    Adapter만 저장

    → 상대적으로 작음


    Merged Full Model 저장

    → Base Model 전체 Weight 포함

    → 훨씬 큼

    ```


    여러 Fine-Tuning 버전을 관리하는 Platform이라면

    Base Model과 Adapter를 분리해 관리하는 방식이 효율적인 경우가 많다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 234–273
  destination: ai-model-development/qlora-artifacts.md
- id: AIMFT-02-01
  knowledge: '## 2.1 다른 모델에 Adapter를 그대로 적용할 수 있는가


    원칙적으로 다른 Base Model에 기존 LoRA Adapter를 그대로 적용할 수 없다고 이해하면 된다.


    예:


    ```text

    Llama-3.1-8B

    +

    Llama용 LoRA Adapter

    → 가능

    ```


    하지만:


    ```text

    Mistral-7B

    +

    Llama용 LoRA Adapter

    → 일반적으로 불가능

    ```


    이유는 Adapter가 특정 Base Model의 Layer 구조와 Dimension을 기준으로 학습되기 때문이다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 276–301
  destination: ai-model-development/adapter-compatibility.md
- id: AIMFT-02-02
  knowledge: '## 2.2 Target Module 의존성


    LoRA는 Transformer 내부의 특정 Linear Layer에 붙는다.


    예:


    ```text

    q_proj

    k_proj

    v_proj

    o_proj


    gate_proj

    up_proj

    down_proj

    ```


    Adapter 설정에는 어떤 Module을 학습했는지가 포함된다.


    예:


    ```text

    target_modules:

    - q_proj

    - v_proj

    ```


    대상 모델에서 해당 Layer 구조나 Dimension이 다르면 같은 Adapter Weight를 적용할 수 없다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 302–332
  destination: ai-model-development/adapter-compatibility.md
- id: AIMFT-02-03
  knowledge: '## 2.3 같은 계열 모델도 주의


    같은 Llama 계열이라고 무조건 Adapter가 호환되는 것은 아니다.


    예:


    ```text

    Llama 8B Adapter

    → Llama 70B

    ```


    는 Weight Dimension이 다르기 때문에 그대로 적용할 수 없다.


    따라서 Adapter에는 최소한 다음 정보를 함께 관리해야 한다.


    ```text

    Base Model Name

    Base Model Version / Revision

    Adapter Type

    LoRA Rank

    LoRA Alpha

    Target Modules

    Training Dataset Version

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 333–359
  destination: ai-model-development/adapter-compatibility.md
- id: AIMFT-02-04
  knowledge: "## 2.4 Base Model 변경 시 해야 하는 일\n\nBase Model을 변경하면 기존 Adapter를 옮기는 것이\
    \ 아니라\n동일한 Training Dataset을 이용해서 새로운 Base Model을 다시 Fine-Tuning하는 방식으로 접근한다.\n\
    \n예:\n\n```text\nTraining Dataset v3\n      │\n      ├─ Llama-3.1-8B\n      │\
    \      ↓\n      │   QLoRA\n      │      ↓\n      │   Adapter A\n      │\n    \
    \  └─ Qwen\n             ↓\n          QLoRA\n             ↓\n          Adapter\
    \ B\n```\n\n즉 장기적으로 중요한 자산은 Adapter 하나만이 아니다.\n\n```text\nDataset\n+\nTraining\
    \ Configuration\n+\nEvaluation Dataset\n+\nExperiment History\n```\n\n를 함께 관리해야\
    \ 한다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 360–398
  destination: ai-model-development/adapter-compatibility.md
- id: AIMFT-03-01
  knowledge: '## 3.1 Fine-Tuning의 핵심 자산


    Base Model은 시간이 지나면서 변경될 수 있다.


    예:


    ```text

    Llama

    ↓

    Qwen

    ↓

    다른 새로운 Base Model

    ```


    하지만 좋은 Training Dataset과 Evaluation Dataset은 새로운 모델에도 다시 활용할 수 있다.


    따라서 Platform 관점에서는:


    ```text

    Model Artifact

    ```


    만큼이나:


    ```text

    Training Dataset

    Golden Dataset

    Dataset Version

    Evaluation Result

    ```


    가 중요하다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 401–435
  destination: ai-model-development/training-datasets.md
- id: AIMFT-03-02
  knowledge: '## 3.2 Raw Document와 Training Dataset은 다르다


    Fine-Tuning에서 회사 문서 파일을 단순히 모델에 넣는 것만으로는 충분하지 않다.


    Raw Data를 학습 목적에 맞는 Sample로 변환해야 한다.


    ```text

    Raw Document

    ↓

    정제

    ↓

    필요한 정보 추출

    ↓

    Instruction / Response 생성

    ↓

    Training Sample

    ```


    예:


    ```text

    User:

    Kafka consumer lag이 증가하면 무엇을 확인해야 해?


    Assistant:

    1. Consumer 처리 속도 확인

    2. Partition별 Lag 편차 확인

    3. Downstream Latency 확인

    4. Rebalance 여부 확인

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 436–468
  destination: ai-model-development/training-datasets.md
- id: AIMFT-03-03
  knowledge: "## 3.3 Chat 형태 Training Sample\n\nLLM SFT에서는 다음과 같은 형태로 Training Dataset을\
    \ 만들 수 있다.\n\n```json\n{\n  \"messages\": [\n    {\n      \"role\": \"user\",\n\
    \      \"content\": \"Kafka consumer lag이 증가하면 무엇을 확인해야 해?\"\n    },\n    {\n\
    \      \"role\": \"assistant\",\n      \"content\": \"Consumer 처리 속도, partition별\
    \ lag, downstream latency, rebalance 여부를 확인합니다.\"\n    }\n  ]\n}\n```\n\n핵심은:\n\
    \n```text\nInput\n→ 모델에게 주는 질문 / Context\n\nTarget Output\n→ 모델이 배우기를 원하는 답변\n\
    ```\n\n이다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 469–501
  destination: ai-model-development/training-datasets.md
- id: AIMFT-03-04
  knowledge: "## 3.4 Dataset 분리\n\nDataset은 용도에 따라 분리해서 관리한다.\n\n```text\n전체 Dataset\n\
    \      │\n      ├─ Training Dataset\n      │\n      ├─ Validation Dataset\n  \
    \    │\n      └─ Golden Dataset\n```\n\n### Training Dataset\n\n실제 Gradient Update에\
    \ 사용한다.\n\n```text\nTraining Sample\n↓\nForward\n↓\nLoss\n↓\nBackpropagation\n\
    ↓\nAdapter Update\n```\n\n### Validation Dataset\n\n학습 과정에서 성능과 Overfitting 여부를\
    \ 확인한다.\n\n### Golden Dataset\n\n최종 모델의 실제 품질을 비교하는 고정 Evaluation Set이다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 502–541
  destination: ai-model-development/training-datasets.md
- id: AIMFT-03-05
  knowledge: '## 3.5 Golden Dataset의 역할


    Golden Dataset은 시험 문제와 비슷하게 생각할 수 있다.


    ```text

    Base Model

    ↓

    Golden Dataset Evaluation


    Fine-Tuned Model A

    ↓

    같은 Golden Dataset Evaluation


    Fine-Tuned Model B

    ↓

    같은 Golden Dataset Evaluation

    ```


    동일한 문제를 사용해야 모델 간 품질 비교가 가능하다.


    따라서 Golden Dataset을 Training Dataset에 섞으면 안 된다.


    ```text

    Golden Dataset

    → Training에 사용 X

    → Final Evaluation에 사용

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 542–571
  destination: ai-model-development/training-datasets.md
- id: AIMFT-03-06
  knowledge: '## 3.6 Dataset 예시 분할


    예를 들어 10,000개의 Sample이 있다면:


    ```text

    Training

    → 8,500


    Validation

    → 1,000


    Golden

    → 500

    ```


    처럼 나눌 수 있다.


    정확한 비율은 데이터 양과 업무 특성에 따라 달라질 수 있지만

    각 Dataset의 **역할을 분리하는 것**이 중요하다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 572–593
  destination: ai-model-development/training-datasets.md
- id: AIMFT-03-07
  knowledge: '## 3.7 Dataset Versioning


    Dataset도 Model과 마찬가지로 Version 관리가 필요하다.


    예:


    ```text

    training-dataset-v1

    training-dataset-v2

    training-dataset-v3


    golden-dataset-v1

    golden-dataset-v2

    ```


    왜 필요한가:


    ```text

    Model 성능이 좋아진 이유

    ```


    가:


    ```text

    Model 변경 때문인지

    Dataset 변경 때문인지

    Training Config 변경 때문인지

    ```


    구분할 수 있어야 하기 때문이다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 594–626
  destination: ai-model-development/training-datasets.md
- id: AIMFT-04-01
  knowledge: '## 4.1 전체 Training Flow


    QLoRA 기반 SFT의 전체 흐름은 다음과 같다.


    ```text

    문제 정의

    ↓

    Training Dataset 준비

    ↓

    Base Model 선택

    ↓

    4-bit Quantization

    ↓

    LoRA Adapter 구성

    ↓

    Training

    ↓

    Validation

    ↓

    Adapter Artifact 저장

    ↓

    Golden Dataset Evaluation

    ↓

    Promote / Reject

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 629–656
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-02
  knowledge: '## 4.2 Step 1 — 학습 목표 정의


    먼저 모델에서 무엇을 개선할지 정한다.


    예:


    ```text

    특정 업무에 맞는 답변 방식

    특정 출력 Format 준수

    분류 정확도 향상

    Tool 사용 방식

    회사 업무 Process에 맞는 응답

    ```


    여기서 중요한 것은:


    > 모든 문제를 Fine-Tuning으로 해결할 필요는 없다.


    이다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 657–678
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-03
  knowledge: '## 4.3 Fine-Tuning과 RAG의 구분


    Fine-Tuning은 주로 모델의 행동이나 업무 수행 방식을 바꾸는 데 사용한다.


    예:


    ```text

    "이 형식으로 답해라"

    "이 업무를 이런 순서로 수행해라"

    "이 Classification 기준을 적용해라"

    ```


    반면 자주 바뀌는 정보나 회사 문서 검색은 RAG가 더 적합할 수 있다.


    ```text

    "현재 회사 정책이 뭐야?"

    "최근 업데이트된 사내 문서를 알려줘"

    ```


    개념적으로:


    ```text

    Behavior / Skill

    → Fine-Tuning


    Changing Knowledge

    → RAG


    Behavior + Knowledge

    → Fine-Tuning + RAG

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 679–712
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-04
  knowledge: '## 4.4 Step 2 — Base Model 선택


    Fine-Tuning할 Base Model을 선택한다.


    예:


    ```text

    Llama

    Qwen

    Gemma

    Mistral

    ```


    선택 시 고려할 수 있는 것:


    ```text

    Model Size

    Model Quality

    License

    Language Performance

    Context Length

    GPU Requirement

    Serving Cost

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 713–739
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-05
  knowledge: '## 4.5 Step 3 — Base Model Quantization


    QLoRA에서는 Base Model을 4-bit 형태로 Loading한다.


    ```text

    Base Model

    ↓

    4-bit Quantization

    ↓

    GPU Memory 사용 감소

    ```


    Base Model Weight는 Frozen 상태로 두고

    LoRA Adapter Parameter만 학습 대상으로 둔다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 740–756
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-06
  knowledge: '## 4.6 Step 4 — LoRA Target Module 설정


    Transformer 내부의 어떤 Linear Layer에 LoRA를 붙일지 결정한다.


    예:


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


    설정 예:


    ```text

    LoRA Rank = 16

    LoRA Alpha = 32

    Target Modules = q_proj, v_proj

    ```


    또는 QLoRA 스타일로 여러 Linear Layer를 대상으로 설정할 수도 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 757–787
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-07
  knowledge: '## 4.7 Step 5 — Tokenization


    Training Sample은 그대로 Neural Network에 들어가는 것이 아니다.


    Tokenizer가 Text를 Token ID로 변환한다.


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


    예:


    ```text

    "Redis와 Kafka의 차이를 설명해줘"

    ↓

    [151644, 872, 25, ...]

    ```


    형태로 변환된다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 788–817
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-08
  knowledge: '## 4.8 Step 6 — Forward Pass


    Tokenized Input을 모델에 넣으면 모델이 다음 Token Probability를 예측한다.


    ```text

    Training Sample

    ↓

    Tokenizer

    ↓

    Base Model + LoRA

    ↓

    Prediction

    ```


    예:


    ```text

    Ground Truth:

    Redis는 In-Memory Data Store이고 Kafka는 Event Streaming Platform이다.


    Model Prediction:

    Redis와 Kafka는 모두 Database이다.

    ```


    처럼 Prediction과 정답이 다를 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 818–845
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-09
  knowledge: '## 4.9 Step 7 — Loss 계산


    모델이 예측한 결과와 정답의 차이를 Loss로 계산한다.


    ```text

    Prediction

    ↕

    Ground Truth

    ↓

    Loss

    ```


    예:


    ```text

    Loss = 2.41

    ```


    Loss가 작아지는 방향으로 학습을 진행한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 846–867
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-10
  knowledge: '## 4.10 Step 8 — Backpropagation


    Loss를 기준으로 Gradient를 계산한다.


    하지만 QLoRA에서는 Base Model Weight 전체를 업데이트하지 않는다.


    ```text

    Base Model Weight

    → Frozen

    → Update X


    LoRA Adapter

    → Trainable

    → Update O

    ```


    즉:


    ```text

    Loss

    ↓

    Gradient

    ↓

    LoRA A / B Weight Update

    ```


    과정을 반복한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 868–897
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-11
  knowledge: '## 4.11 Step 9 — Batch / Step / Epoch


    Training Dataset 전체를 여러 번 반복해서 학습할 수 있다.


    예:


    ```text

    Training Dataset

    10,000 Samples


    Epoch 1

    → 전체 Dataset 학습


    Epoch 2

    → 전체 Dataset 다시 학습


    Epoch 3

    → 전체 Dataset 다시 학습

    ```


    한 번의 전체 Dataset 학습을 Epoch라고 이해하면 된다.


    실제 Training에서는 Batch 단위로 Sample을 처리하고 Parameter를 Update한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 898–923
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-12
  knowledge: '## 4.12 주요 Training Parameter


    AI Model Developer가 조정하는 대표 Parameter:


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


    예:


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


    즉 하나의 Training Run은 다음 조합으로 볼 수 있다.


    ```text

    Dataset

    +

    Base Model

    +

    Training Configuration

    =

    Experiment

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 924–969
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-13
  knowledge: '## 4.13 Training 중 확인하는 Metric


    학습 중에는 다음을 확인할 수 있다.


    ```text

    Training Loss

    Validation Loss

    Learning Rate

    Gradient Norm

    GPU Memory

    Training Throughput

    ```


    단순히 Training Loss만 낮아지는 것이 목표는 아니다.


    Validation 성능과 실제 업무 Evaluation을 같이 봐야 한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 970–988
  destination: ai-model-development/qlora-training.md
- id: AIMFT-04-14
  knowledge: '## 4.14 Training 결과 저장


    학습 완료 후 Adapter를 저장한다.


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


    이후 Model Registry에서 Metadata와 연결할 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 989–1007
  destination: ai-model-development/qlora-training.md
- id: AIMFT-05-01
  knowledge: '## 5.1 Training 완료가 Production 완료는 아니다


    Fine-Tuning이 끝났다고 바로 Production에 배포하면 안 된다.


    ```text

    Training Complete

    ≠

    Production Ready

    ```


    학습 결과를 Golden Dataset으로 검증해야 한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1010–1023
  destination: ai-model-development/evaluation-promotion.md
- id: AIMFT-05-02
  knowledge: "## 5.2 Base Model과 Fine-Tuned Model 비교\n\n동일한 Golden Dataset으로 비교한다.\n\
    \n```text\nGolden Dataset\n      │\n      ├─ Base Model\n      │\n      ├─ Fine-Tuned\
    \ Model A\n      │\n      └─ Fine-Tuned Model B\n```\n\n예:\n\n| Metric | Base\
    \ | Fine-Tuned |\n|---|---:|---:|\n| Task Accuracy | 76% | 89% |\n| Format Pass\
    \ | 81% | 97% |\n| Hallucination | 9% | 4% |\n| Latency | 120ms | 135ms |\n\n\
    중요:\n\n> Training Loss가 낮다는 이유만으로 좋은 모델이라고 판단할 수 없다.\n\n실제 업무에서 필요한 Metric으로 평가해야\
    \ 한다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 1024–1054
  destination: ai-model-development/evaluation-promotion.md
- id: AIMFT-05-03
  knowledge: '## 5.3 Evaluation Metric


    업무에 따라 다음과 같은 Metric을 사용할 수 있다.


    ```text

    Accuracy

    Task Success Rate

    Format Pass Rate

    Hallucination Rate

    Safety

    Human Preference

    Latency

    Token Usage

    Cost

    ```


    즉 Model Quality뿐 아니라 Serving 측면까지 함께 볼 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1055–1074
  destination: ai-model-development/evaluation-promotion.md
- id: AIMFT-05-04
  knowledge: '## 5.4 Quality Gate


    Evaluation 결과가 기준을 통과했을 때만 Production Candidate로 승격할 수 있다.


    ```text

    Fine-Tuned Model

    ↓

    Golden Evaluation

    ↓

    Quality Gate

    ├─ PASS → Promote

    └─ FAIL → Reject / Retrain

    ```


    예:


    ```text

    Accuracy >= 90%

    Format Pass >= 98%

    Hallucination <= 3%

    Latency <= Target

    ```


    과 같은 기준을 둘 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1075–1101
  destination: ai-model-development/evaluation-promotion.md
- id: AIMFT-05-05
  knowledge: '## 5.5 Error Analysis


    Evaluation에서 실패한 Sample을 분석하는 과정이 중요하다.


    예:


    ```text

    SAP 질문

    → 잘함


    Kafka 기본 질문

    → 잘함


    복잡한 장애 분석

    → 성능 낮음

    ```


    그러면 원인을 분석한다.


    ```text

    복잡한 장애 분석 Sample 부족

    ↓

    관련 Training Data 추가

    ↓

    Dataset v4 생성

    ↓

    재학습

    ↓

    재평가

    ```


    즉 Fine-Tuning은 한 번의 작업이 아니라 반복적인 개선 Loop이다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1102–1136
  destination: ai-model-development/evaluation-promotion.md
- id: AIMFT-05-06
  knowledge: '## 5.6 Model Improvement Loop


    전체 Loop:


    ```text

    문제 정의

    ↓

    Data 수집 / 정제

    ↓

    Training Dataset 생성

    ↓

    Fine-Tuning

    ↓

    Evaluation

    ↓

    Error Analysis

    ↓

    Dataset 개선

    ↓

    Retraining

    ```


    모델 개발에서 Dataset과 Evaluation이 중요한 이유가 여기에 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1137–1162
  destination: ai-model-development/evaluation-promotion.md
- id: AIMFT-06-01
  knowledge: '## 6.1 Base Model 교체 시 흐름


    운영 모델을 Llama에서 Qwen으로 변경한다고 가정한다.


    기존:


    ```text

    Llama

    +

    Adapter v4

    ```


    변경:


    ```text

    Qwen

    +

    새 Adapter

    ```


    기존 Llama Adapter를 그대로 사용하는 것이 아니라

    기존 Training Dataset을 이용해 새로운 Qwen Adapter를 학습한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1165–1189
  destination: ai-model-development/model-retraining.md
- id: AIMFT-06-02
  knowledge: '## 6.2 Model 교체 Process


    ```text

    1. 새로운 Base Model 준비

    ↓

    2. 기존 Training Dataset 선택

    ↓

    3. 새로운 Base Model에 QLoRA Fine-Tuning

    ↓

    4. 새로운 Adapter 생성

    ↓

    5. 동일 Golden Dataset으로 평가

    ↓

    6. 기존 Production Model과 비교

    ↓

    7. Quality / Cost / Latency 기준 확인

    ↓

    8. Promote 또는 Reject

    ```


    이 구조를 갖추면 Base Model이 바뀌어도 동일한 기준으로 비교할 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1190–1213
  destination: ai-model-development/model-retraining.md
- id: AIMFT-06-03
  knowledge: '## 6.3 Dataset이 장기 자산인 이유


    Model은 빠르게 교체될 수 있다.


    하지만 다음은 계속 사용할 수 있다.


    ```text

    Training Dataset

    Validation Dataset

    Golden Dataset

    Evaluation Logic

    Business Metric

    ```


    따라서 장기적인 AI Asset은:


    ```text

    Model

    ```


    하나가 아니라:


    ```text

    Data

    +

    Evaluation

    +

    Experiment History

    ```


    까지 포함한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1214–1247
  destination: ai-model-development/model-retraining.md
- id: AIMFT-07-01
  knowledge: "## 7.1 S3 구조 예시\n\n```text\ns3://ai-platform/\n├─ datasets/\n│  ├─ training/\n\
    │  │  ├─ v1/\n│  │  ├─ v2/\n│  │  └─ v3/\n│  │\n│  ├─ validation/\n│  │  └─ v3/\n\
    │  │\n│  └─ golden/\n│     └─ v5/\n│\n└─ models/\n   ├─ llama-3.1-8b/\n   │  └─\
    \ adapters/\n   │     ├─ v1/\n   │     └─ v2/\n   │\n   └─ qwen/\n      └─ adapters/\n\
    \         └─ v1/\n```\n\nObject Storage는 실제 파일을 저장한다.\n\n하지만 파일만 저장해서는 어떤 Experiment에서\
    \ 만들어졌는지 알기 어렵다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 1250–1282
  destination: ai-model-development/artifact-lineage.md
- id: AIMFT-07-02
  knowledge: '## 7.2 Metadata 연결


    Adapter에는 다음 Metadata를 연결할 수 있다.


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


    이렇게 연결하면 재현 가능한 Training Pipeline을 만들 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1283–1302
  destination: ai-model-development/artifact-lineage.md
- id: AIMFT-07-03
  knowledge: '## 7.3 Model Registry의 역할


    S3는 Artifact 파일을 저장하는 역할이다.


    Model Registry는 그 Artifact의 의미와 상태를 관리하는 역할을 할 수 있다.


    예:


    ```text

    S3

    = 실제 Adapter / Model File


    Model Registry

    = Version / Metadata / Stage / Lineage 관리

    ```


    Stage 예:


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


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1303–1334
  destination: ai-model-development/artifact-lineage.md
- id: AIMFT-07-04
  knowledge: '## 7.4 Training Lineage


    중요한 것은 다음 관계를 추적할 수 있는 것이다.


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


    문제가 발생했을 때:


    ```text

    현재 Production Model은

    어떤 Dataset으로 학습했고

    어떤 Config를 사용했고

    어떤 Evaluation을 통과했는가?

    ```


    를 추적할 수 있어야 한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1335–1367
  destination: ai-model-development/artifact-lineage.md
- id: AIMFT-08-01
  knowledge: '## 8.1 AI Model Developer의 핵심 역할


    기존 Foundation Model을 회사나 서비스 목적에 맞게 Fine-Tuning하는 AI Model Developer는

    단순히 Training Script를 실행하는 사람이 아니다.


    핵심은:


    ```text

    어떤 문제를 풀 것인가

    ↓

    어떤 Data를 사용할 것인가

    ↓

    어떤 Model을 선택할 것인가

    ↓

    어떻게 Training할 것인가

    ↓

    어떻게 Evaluation할 것인가

    ↓

    왜 실패했는가

    ↓

    어떻게 개선할 것인가

    ```


    를 반복적으로 판단하는 것이다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1370–1396
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-02
  knowledge: '## 8.2 Problem Definition


    먼저 무엇을 개선하려는지 정의한다.


    예:


    ```text

    업무 Task Accuracy

    특정 Output Format

    Instruction Following

    Classification

    Reasoning Pattern

    Tool Use

    ```


    그리고:


    ```text

    Fine-Tuning이 필요한가?

    RAG로 해결할 수 있는가?

    Prompt Engineering으로 충분한가?

    ```


    를 판단한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1397–1423
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-03
  knowledge: '## 8.3 Dataset Design


    AI Model Developer의 중요한 역할 중 하나가 Dataset 설계다.


    해야 하는 일:


    - 좋은 Sample 선별

    - 잘못된 정답 제거

    - 중복 데이터 제거

    - 저품질 데이터 제거

    - 원하는 Instruction / Response 형태로 변환

    - 데이터 분포 확인

    - Train / Validation / Golden 분리

    - Dataset Version 관리


    즉:


    ```text

    Garbage Data

    ↓

    좋은 Model을 만들기 어려움

    ```


    이므로 Dataset Quality가 매우 중요하다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1424–1450
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-04
  knowledge: '## 8.4 Training Strategy 선택


    문제와 Resource에 따라 Training 방법을 선택한다.


    예:


    ```text

    Full Fine-Tuning

    LoRA

    QLoRA

    SFT

    Preference Training

    ```


    예를 들어 GPU Resource가 제한되어 있다면:


    ```text

    Large Model Full Fine-Tuning

    → 비용 큼


    Smaller Model + QLoRA

    → 상대적으로 현실적인 선택

    ```


    같은 판단을 할 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1451–1478
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-05
  knowledge: '## 8.5 Hyperparameter Tuning


    대표적으로 조정하는 값:


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


    한 번의 설정만 사용하는 것이 아니라 여러 Experiment를 비교한다.


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


    그리고 가장 좋은 결과를 선택한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1479–1513
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-06
  knowledge: '## 8.6 Quantization 고려


    AI Model Developer는 Training Resource와 Serving Resource를 고려해 Quantization도 판단할
    수 있다.


    구분:


    ```text

    Training Quantization

    → QLoRA 등

    → 학습 GPU Memory 절감


    Serving Quantization

    → FP8 / INT8 / INT4 등

    → Inference Memory / Cost 절감

    ```


    두 영역은 목적이 다르다.


    Serving Quantization은 AI Serving / Platform Engineer와 함께 판단할 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1514–1535
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-07
  knowledge: '## 8.7 Evaluation


    모델 개발자에게 Evaluation은 핵심 역할이다.


    확인해야 하는 것:


    ```text

    Fine-Tuning 후 정말 좋아졌는가?

    특정 영역만 좋아지고 다른 영역은 나빠지지 않았는가?

    Hallucination이 증가하지 않았는가?

    Output Format을 지키는가?

    Production 요구 Latency를 만족하는가?

    ```


    따라서:


    ```text

    Golden Dataset

    +

    Evaluation Metric

    +

    Error Analysis

    ```


    가 중요하다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1536–1563
  destination: ai-model-development/model-developer.md
- id: AIMFT-08-08
  knowledge: '## 8.8 Error Analysis와 Dataset 개선


    모델이 틀린 문제를 보고 Data 문제인지 Model 문제인지 분석한다.


    ```text

    Evaluation Failure

    ↓

    Failure Category 분류

    ↓

    Dataset 부족 확인

    ↓

    Data 추가 / 정제

    ↓

    Dataset New Version

    ↓

    Retraining

    ```


    이 Loop를 반복하면서 모델을 개선한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1564–1585
  destination: ai-model-development/model-developer.md
- id: AIMFT-09-01
  knowledge: '## 9.1 역할 차이


    AI Model Developer는 모델 품질을 중심으로 본다.


    ```text

    어떤 Dataset?

    어떤 Base Model?

    어떤 Fine-Tuning 방법?

    어떤 Hyperparameter?

    성능이 좋아졌는가?

    왜 실패했는가?

    ```


    AI Platform Engineer는 이 과정이 안정적이고 반복 가능하게 실행되도록 Platform을 만든다.


    ```text

    Dataset을 어디서 관리할 것인가?

    GPU Training Job을 어떻게 실행할 것인가?

    Artifact를 어디에 저장할 것인가?

    Experiment를 어떻게 추적할 것인가?

    Evaluation을 어떻게 자동화할 것인가?

    Model Registry는 어떻게 구성할 것인가?

    Serving은 어떻게 할 것인가?

    Monitoring / Rollback은 어떻게 할 것인가?

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1588–1615
  destination: ai-model-development/model-platform-collaboration.md
- id: AIMFT-09-02
  knowledge: '## 9.2 협업 예시


    Model Developer 요청:


    ```text

    Qwen

    +

    training-dataset-v12

    +

    QLoRA Rank 32

    +

    3 Epoch

    ```


    Platform은 이를 실행한다.


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


    평가 후 Model Developer가 결과를 확인한다.


    ```text

    Reasoning 성능 부족

    ↓

    Training Data 개선

    ↓

    Dataset v13

    ↓

    Retraining

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1616–1663
  destination: ai-model-development/model-platform-collaboration.md
- id: AIMFT-09-03
  knowledge: '## 9.3 Model Developer와 Platform의 책임 경계


    개념적으로:


    ```text

    Model Developer

    = 무엇을 학습하고 어떻게 품질을 높일 것인가


    AI Platform Engineer

    = 그 학습 / 평가 / 배포 과정을 어떻게 안정적으로 제공할 것인가

    ```


    둘은 완전히 분리된 역할이 아니라 협업 영역이 많다.


    예:


    ```text

    Quantization

    GPU Memory

    Serving Latency

    Model Packaging

    Evaluation Automation

    ```


    등은 함께 판단할 수 있다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1664–1691
  destination: ai-model-development/model-platform-collaboration.md
- id: AIMFT-10-01
  knowledge: "## 10.1 전체 구조\n\n이번 세션의 내용을 하나로 연결하면 다음과 같다.\n\n```text\nRaw Data /\
    \ Documents\n↓\nData Cleaning / Curation\n↓\nTraining Dataset\nValidation Dataset\n\
    Golden Dataset\n↓\nDataset Versioning\n↓\nTraining Request\n↓\nBase Model 선택\n\
    +\nQLoRA Config\n↓\nGPU Training Job\n↓\nLoRA Adapter\n↓\nS3 Artifact Storage\n\
    ↓\nModel Registry\n↓\nGolden Dataset Evaluation\n↓\nQuality Gate\n├─ FAIL → Error\
    \ Analysis → Dataset 개선 → Retraining\n└─ PASS\n     ↓\nModel Serving\n     ↓\n\
    vLLM / Serving Engine\n     ↓\nProduction\n```\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 1694–1737
  destination: ai-model-development/training-platform-architecture.md
- id: AIMFT-10-02
  knowledge: '## 10.2 Platform 관점의 핵심 Object


    AI Fine-Tuning Platform에서 관리해야 하는 주요 Object:


    ```text

    Base Model

    Dataset

    Dataset Version

    Training Config

    Training Run

    Adapter Artifact

    Evaluation Run

    Evaluation Result

    Model Version

    Deployment

    ```


    각 Object를 연결하는 것이 중요하다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1738–1758
  destination: ai-model-development/training-platform-architecture.md
- id: AIMFT-10-03
  knowledge: '## 10.3 재현 가능한 Training


    좋은 Platform이라면 과거 Training을 다시 재현할 수 있어야 한다.


    예:


    ```text

    Training Run #1024


    Base Model

    → Qwen revision X


    Training Dataset

    → train-v12


    Validation Dataset

    → validation-v12


    Training Config

    → qlora-config-v4


    Code Version

    → git commit abc123


    Artifact

    → adapter-v7

    ```


    이 정보를 이용해서 같은 조건의 Training을 다시 실행할 수 있어야 한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1759–1790
  destination: ai-model-development/training-platform-architecture.md
- id: AIMFT-10-04
  knowledge: '## 10.4 Model 교체에도 대응 가능한 구조


    Base Model이 바뀌더라도 Pipeline 자체는 유지된다.


    ```text

    Llama

    ↓

    Training Dataset v12

    ↓

    QLoRA

    ↓

    Adapter A

    ↓

    Golden Evaluation

    ```


    새 Model:


    ```text

    Qwen

    ↓

    Training Dataset v12

    ↓

    QLoRA

    ↓

    Adapter B

    ↓

    동일 Golden Evaluation

    ```


    그리고 결과를 비교한다.


    ```text

    Quality

    Latency

    Cost

    GPU Memory

    Throughput

    ```


    이를 통해 어떤 Base Model을 Production에 사용할지 결정한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1791–1834
  destination: ai-model-development/training-platform-architecture.md
- id: AIMFT-00-02
  knowledge: '# Final Summary


    이번 세션의 핵심은 다음과 같다.


    ## QLoRA


    ```text

    Base Model을 4-bit로 사용

    +

    LoRA Adapter만 학습

    ```


    Base Model 전체를 수정하지 않고 작은 Adapter를 학습한다.


    ---'
  kind: summary
  source_lines: 1835–1850
  destination: ai-model-development/index.md
- id: AIMFT-00-03
  knowledge: '## Artifact


    QLoRA Training 결과는 주로:


    ```text

    adapter_model.safetensors

    adapter_config.json

    ```


    형태이며 S3 같은 Object Storage에 저장할 수 있다.


    ---'
  kind: summary
  source_lines: 1851–1863
  destination: ai-model-development/index.md
- id: AIMFT-00-04
  knowledge: '## Adapter Compatibility


    ```text

    같은 Base Model

    → Adapter 사용 가능


    다른 Base Model / 다른 Size / 다른 Architecture

    → 기존 Adapter 그대로 사용 어려움

    → 새로운 Fine-Tuning 필요

    ```


    따라서 Base Model 변경에 대비해 Training Dataset을 잘 관리해야 한다.


    ---'
  kind: summary
  source_lines: 1864–1878
  destination: ai-model-development/index.md
- id: AIMFT-00-05
  knowledge: '## Dataset


    ```text

    Training Dataset

    → 실제 학습


    Validation Dataset

    → 학습 중 검증


    Golden Dataset

    → 최종 품질 비교

    ```


    Golden Dataset은 Training Data에 포함시키지 않는다.


    ---'
  kind: summary
  source_lines: 1879–1895
  destination: ai-model-development/index.md
- id: AIMFT-00-06
  knowledge: '## Training


    ```text

    Dataset

    ↓

    Tokenizer

    ↓

    Base Model + LoRA

    ↓

    Prediction

    ↓

    Loss

    ↓

    Backpropagation

    ↓

    LoRA Adapter Update

    ```


    이를 여러 Batch / Epoch에 걸쳐 반복한다.


    ---'
  kind: summary
  source_lines: 1896–1917
  destination: ai-model-development/index.md
- id: AIMFT-00-07
  knowledge: '## Evaluation


    ```text

    Base Model

    vs

    Fine-Tuned Model

    ```


    을 동일 Golden Dataset으로 비교한다.


    Training Loss뿐 아니라 실제 Task Metric을 기준으로 판단한다.


    ---'
  kind: summary
  source_lines: 1918–1931
  destination: ai-model-development/index.md
- id: AIMFT-00-08
  knowledge: '## Model Developer


    AI Model Developer의 핵심 역할:


    ```text

    Problem Definition

    ↓

    Dataset Design

    ↓

    Model Selection

    ↓

    Training Strategy

    ↓

    Hyperparameter Tuning

    ↓

    Evaluation

    ↓

    Error Analysis

    ↓

    Dataset Improvement

    ```


    즉 단순히 Training Script를 실행하는 역할이 아니다.


    ---'
  kind: summary
  source_lines: 1932–1957
  destination: ai-model-development/index.md
- id: AIMFT-00-09
  knowledge: '## AI Platform Engineer


    AI Platform Engineer는 위 과정이 반복 가능하게 돌아가도록 만든다.


    ```text

    Dataset Registry

    Training Infrastructure

    GPU Job

    Artifact Storage

    Experiment Tracking

    Model Registry

    Evaluation Pipeline

    Serving

    Monitoring

    Rollback

    ```


    을 Platform으로 제공한다.


    ---'
  kind: summary
  source_lines: 1958–1978
  destination: ai-model-development/index.md
- id: AIMFT-00-10
  knowledge: '## 가장 중요한 관점


    장기적으로 AI 시스템의 자산은 특정 Model 하나만이 아니다.


    ```text

    Training Dataset

    +

    Golden Dataset

    +

    Evaluation System

    +

    Training / Experiment History

    +

    Model Artifact

    ```


    전체가 자산이다.


    Base Model은 계속 바뀔 수 있지만,

    잘 만들어진 Dataset과 Evaluation 체계가 있으면 새로운 Model을 다시 학습하고 동일한 기준으로 검증할 수 있다.'
  kind: summary
  source_lines: 1979–1998
  destination: ai-model-development/index.md
---

# QLoRA 지식 추출

페이지 작성 전 전체 원문을 분담해 읽고 절별 개념·예시·수치·조건·역할·실험 흐름을 추출했다. 상세 원문을 각 항목에 보존한다.
