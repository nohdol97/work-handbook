---
items:
- id: AWSC2-00-01
  knowledge: "# AWS Cloud Basic — Source Markdown (Chapter 6~7)\n\n> 범위: Chapter 5 이후 학습 내용  \n> 포함 범위: Chapter\
    \ 6. AWS Managed Services + Chapter 7. AI/GPU + End-to-End  \n> 원칙:\n> - 세션에서 실제 학습한 내용 기준\n> - 중간 질문/보충 설명\
    \ 포함\n> - 중복 제거\n> - Basic 수준 핵심 중심\n> - Terraform / IaC는 다른 세션에서 이미 학습했으므로 반복하지 않음\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 1–13
  destination: aws-cloud/index.md
- id: AWSC2-00-02
  knowledge: '# Chapter 6~7 최종 요약


    ## Messaging / Event


    ```text

    SQS = Task Queue

    SNS = Pub/Sub / Fan-out

    MSK = Kafka / Event Streaming

    ```


    ## Security


    ```text

    IAM = 권한

    KMS = Encryption Key

    Secrets Manager = Secret 저장 / Rotation

    ```


    ## Observability


    ```text

    CloudWatch = Monitoring

    CloudTrail = Audit

    ```


    ## AI / GPU


    ```text

    GPU EC2 = GPU Compute

    EKS GPU Node = GPU Worker Node

    ECR = Container Image

    S3 = Model / Dataset

    vLLM = GPU 기반 LLM Serving

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 1337–1373
  destination: aws-cloud/index.md
- id: AWSC2-00-03
  knowledge: '# AWS Cloud Basic 최종 학습 완료 상태


    완료:

    - Chapter 1. AWS Foundation ✅

    - Chapter 2. Networking ✅

    - Chapter 3. Compute & Load Balancing ✅

    - Chapter 4. Storage & Database ✅

    - Chapter 5. EKS on AWS ✅

    - Chapter 6. AWS Managed Services ✅

    - Chapter 7. AI/GPU + End-to-End ✅


    최종 핵심 구조:


    ```text

    Network

    → VPC / Subnet / Route / IGW / NAT / SG


    Compute

    → EC2 / ASG / EKS


    Traffic

    → ALB / NLB / Service


    Storage

    → EBS / EFS / S3


    Data

    → RDS / Aurora / ElastiCache


    Messaging

    → SQS / SNS / MSK


    Security

    → IAM / KMS / Secrets Manager


    Observability

    → CloudWatch / CloudTrail


    AI

    → GPU EC2 / EKS GPU Node / ECR / S3 / vLLM

    ```


    각 AWS 서비스가 왜 존재하고, 어디에 배치되며, 무엇과 연결되는지 설명할 수 있으면 AWS Cloud Basic 목표를 달성한 것이다.'
  kind: concept,example,condition,workflow
  source_lines: 1374–1416
  destination: aws-cloud/index.md
- id: AWSC2-06-01
  knowledge: "## 6.1 SQS\n\nSQS = **Simple Queue Service**\n\n> 서비스 사이의 메시지를 Queue에 저장해두고 비동기로 처리하는 AWS Managed\
    \ Message Queue\n\n기본 구조:\n\n```text\nProducer\n   ↓\n  SQS\n   ↓\nConsumer\n```\n\n예:\n\n```text\nAPI Pod\n\
    \ ↓\nSQS\n ↓\nWorker Pod\n```\n\nAPI가 오래 걸리는 작업을 직접 처리하지 않고 Queue에 넣은 뒤 바로 응답할 수 있다.\n\n### 왜 SQS를 쓰는가?\n\n\
    ```text\nUser\n ↓\nAPI\n ↓\nSQS에 Job 저장\n ↓\n즉시 응답\n\nWorker\n ↓\nSQS에서 Job 가져옴\n ↓\n실제 처리\n```\n\n핵심 효과:\n\
    - Producer와 Consumer 분리\n- 트래픽 급증 흡수\n- 비동기 처리\n- 장애 시 재시도 가능\n\n### Consumer Polling\n\nSQS는 Consumer가 Queue에서\
    \ 메시지를 가져간다.\n\n```text\nWorker\n ↓ poll\nSQS\n ↓\nMessage\n```\n\nKafka처럼 Event Stream을 지속적으로 읽는 감각보다는 Queue에\
    \ 쌓인 Task를 Worker가 가져가 처리하는 모델에 가깝다.\n\n### Visibility Timeout\n\nConsumer가 메시지를 가져가도 즉시 삭제되지 않는다.\n\n```text\n\
    Worker A가 Message 수신\n ↓\nVisibility Timeout\n ↓\n다른 Worker에게 잠시 숨김\n```\n\nWorker가 처리 완료 후 Delete하면 메시지가 제거된다.\n\
    \n실패해서 Delete하지 못하면:\n\n```text\n처리 실패\n ↓\nVisibility Timeout 만료\n ↓\nMessage 재노출\n ↓\n다른 Worker가 다시 처리 가능\n\
    ```\n\n### Dead Letter Queue\n\n계속 실패하는 메시지를 별도 Queue로 격리할 수 있다.\n\n```text\nMain Queue\n ↓ 반복 실패\nDLQ\n```\n\
    \n용도:\n- 실패 메시지 분석\n- 오류 원인 확인\n- 수동 재처리\n\n### Standard vs FIFO\n\n#### Standard Queue\n- 높은 처리량\n- 순서가 완전히\
    \ 보장되지는 않음\n- 중복 전달 가능성을 고려해야 함\n- Consumer는 Idempotent하게 만드는 것이 좋음\n\n#### FIFO Queue\nFIFO = First-In-First-Out.\n\
    \n```text\nA\nB\nC\n→ A → B → C\n```\n\n기본 선택 기준:\n\n```text\n일반 비동기 작업\n→ Standard\n\n순서가 중요\n→ FIFO\n```\n\
    \n### EKS와 SQS\n\n```text\nAPI Pods\n   ↓\n  SQS\n   ↓\nWorker Pods\n```\n\nQueue Depth가 늘면 Worker Pod 수를 늘리는\
    \ Auto Scaling 구조도 만들 수 있다.\n\nAI Platform 예:\n\n```text\n사용자 요청\n ↓\nAPI\n ↓\nSQS\n ↓\nEvaluation Worker\n\
    \ ↓\nLLM Evaluation 실행\n```\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 16–178
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-02
  knowledge: "## 6.1.1 SQS vs Kafka\n\n중요한 차이는 **병렬 처리 여부가 아니다.** SQS도 Consumer를 여러 개 두면 병렬 처리가 가능하다.\n\n핵심 차이:\n\
    \n```text\nSQS\n= Task Queue\n\nKafka\n= Event Log / Event Streaming Platform\n```\n\n### SQS\n\n```text\nProducer\n\
    \ ↓\nQueue\n ↓\nWorker A / B / C\n```\n\n느낌:\n\n> \"이 작업을 누군가 한 번 처리해줘.\"\n\n예:\n- 이미지 변환 Job\n- 이메일 발송\n- LLM\
    \ Evaluation Job\n- 주문 후처리\n\n처리 완료 후 메시지는 보통 삭제된다.\n\n### Kafka\n\n```text\nEvent\n ↓\nKafka Topic\n ↓\nConsumer\
    \ Groups\n```\n\n느낌:\n\n> \"이 이벤트가 발생했으니 기록해둘게. 필요한 시스템이 각자 읽어.\"\n\n예:\n\n```text\nclick event\n ↓\nKafka\n\
    ├─ Analytics Group\n├─ Recommendation Group\n└─ Monitoring Group\n```\n\n한 Consumer가 읽었다고 Event가 없어지는 것이 아니다.\n\
    \n### Replay\n\nKafka는 Offset을 되돌려 과거 Event를 다시 읽을 수 있다.\n\n```text\n지난 3일 이벤트\n ↓ Replay\n새 알고리즘으로 재처리\n```\n\
    \nSQS는 이런 장기 Event Log / Replay 용도로 설계된 서비스가 아니다.\n\n### 병렬 처리 방식\n\nSQS:\n\n```text\nQueue\n ↓\nWorker A\n\
    Worker B\nWorker C\n```\n\nKafka:\n\n```text\nTopic\n├─ Partition 0 → Consumer A\n├─ Partition 1 → Consumer\
    \ B\n└─ Partition 2 → Consumer C\n```\n\nPartition이 Kafka의 병렬 처리 단위가 된다.\n\n| 항목 | SQS | Kafka |\n|---|---|---|\n\
    | 모델 | Queue | Distributed Log |\n| 목적 | Task 전달 | Event 보존/Streaming |\n| 처리 후 | Delete | 일정 기간 보존 |\n| Replay\
    \ | 제한적 | Offset 기반 가능 |\n| 여러 독립 Consumer | 별도 구성 | Consumer Group |\n| 병렬 처리 | Consumer 수 | Partition + Consumer\
    \ |\n| 대표 용도 | 비동기 Job | Event Pipeline |\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 179–288
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-03
  knowledge: "## 6.2 SNS\n\nSNS = **Simple Notification Service**\n\n> 하나의 메시지를 여러 Subscriber에게 동시에 전달하는 Managed\
    \ Pub/Sub 서비스\n\n```text\nPublisher\n   ↓\n SNS Topic\n ├─ Subscriber A\n ├─ Subscriber B\n └─ Subscriber C\n\
    ```\n\n### Topic\n\n메시지는 Topic에 Publish한다.\n\n```text\nOrder Service\n   ↓\nSNS Topic\n├─ Email Service\n├─\
    \ Analytics\n└─ Notification Service\n```\n\n### SNS vs SQS\n\n```text\nSQS\n= 1개의 작업을 Worker에게 분배\n\nSNS\n\
    = 1개의 이벤트를 여러 곳에 Broadcast\n```\n\n### SNS + SQS\n\n실무에서 흔한 Fan-out 패턴:\n\n```text\n            SNS Topic\n\
    \          /     |      \\\n         ↓      ↓       ↓\n      SQS A   SQS B   SQS C\n        ↓       ↓      \
    \ ↓\n     Worker   Worker   Worker\n```\n\n장점:\n- 시스템 간 결합도 감소\n- 각 Consumer 속도 차이 흡수\n- 실패/재시도 독립\n- 한 시스템\
    \ 장애가 다른 시스템에 덜 영향\n\n### Subscriber 종류\n\n대표적으로:\n- SQS\n- HTTP/HTTPS Endpoint\n- Lambda\n- Email\n- SMS\n\n\
    Basic에서는 AWS 서비스 간 이벤트 분배에 SNS → SQS / Lambda 조합이 흔하다고 이해하면 충분하다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 289–358
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-04
  knowledge: "## 6.3 Amazon MSK\n\nMSK = **Managed Streaming for Apache Kafka**\n\n> AWS가 Kafka Broker 인프라 운영을 상당\
    \ 부분 대신해주는 Managed Kafka 서비스\n\nKafka 자체 개념은 이미 학습한 것으로 보고 AWS 관점만 다룬다.\n\n### 직접 Kafka 운영 vs MSK\n\n직접 운영:\n\
    \n```text\nEC2 / EKS\n ↓\nKafka Cluster\n├─ Broker\n├─ Storage\n├─ Replication\n├─ Patch\n└─ Failure Handling\n\
    ```\n\nMSK:\n\n```text\nProducer / Consumer\n        ↓\n       MSK\n```\n\n### VPC 내부 배치\n\n보통 Private Subnet에\
    \ Broker를 배치한다.\n\n```text\nVPC\n├─ Private Subnet A\n│  └─ MSK Broker\n├─ Private Subnet B\n│  └─ MSK Broker\n\
    └─ Private Subnet C\n   └─ MSK Broker\n```\n\nEKS Application은 VPC 내부에서 접근한다.\n\n### Multi-AZ\n\n```text\nAZ\
    \ A → Broker\nAZ B → Broker\nAZ C → Broker\n```\n\nKafka Replication과 AWS Multi-AZ를 함께 활용한다.\n\n### Security\n\
    \n```text\nNetwork\n→ VPC / Security Group\n\nAuthentication\n→ Kafka Client 인증\n\nEncryption\n→ 전송 / 저장 암호화\n\
    ```\n\n### EKS + MSK\n\n```text\nUsers / Services\n      ↓\n     EKS\n      ↓\n     MSK\n      ↓\n ┌────┼─────┐\n\
    \ ↓    ↓     ↓\nAnalytics\nData Pipeline\nMonitoring\n```\n\n### SQS vs MSK\n\n```text\nSQS\n= Task Queue\n\n\
    MSK\n= Event Streaming / Event Log\n```\n\n예:\n\n```text\n이미지 변환 Job\n→ SQS\n\n사용자 Click Event\n→ MSK\n```\n\
    \n---"
  kind: concept,example,condition,workflow
  source_lines: 359–466
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-05
  knowledge: '## 6.4 KMS


    KMS = **Key Management Service**


    > AWS Resource를 암호화할 때 사용하는 암호화 Key를 생성하고 관리하는 서비스


    ### 연결되는 대표 서비스


    ```text

    S3 → Object 암호화

    EBS → Disk 암호화

    RDS → DB Storage 암호화

    Secrets Manager → Secret 암호화

    ```


    KMS 자체에 일반 데이터를 저장하는 것이 아니라 다른 AWS 서비스가 데이터를 암호화할 때 사용할 Key를 관리한다.


    ### Encryption at Rest vs In Transit


    ```text

    At Rest

    = 저장 데이터 암호화


    In Transit

    = 전송 데이터 암호화

    ```


    ### AWS Managed Key vs Customer Managed Key


    AWS Managed Key:

    - AWS가 서비스용으로 관리


    Customer Managed Key:

    - 사용자가 직접 생성

    - Key Policy 관리

    - Rotation 설정

    - 환경/서비스별 Key 분리


    ```text

    단순 사용

    → AWS Managed Key


    세밀한 통제 필요

    → Customer Managed Key

    ```


    ### IAM과 KMS


    ```text

    IAM

    = 누가 AWS Resource를 사용할 수 있는가


    KMS

    = 누가 Encryption Key를 사용할 수 있는가

    ```


    KMS로 암호화된 S3 Object를 읽을 때는 상황에 따라:


    ```text

    s3:GetObject

    +

    kms:Decrypt

    ```


    권한이 함께 필요할 수 있다.


    ### Key Rotation


    KMS는 Key Lifecycle과 Rotation 관리 기능을 제공한다.


    ---'
  kind: concept,example,condition,workflow
  source_lines: 467–538
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-06
  knowledge: "## 6.5 Secrets Manager\n\nSecrets Manager:\n\n> DB Password, API Key, Token 같은 민감한 값을 안전하게 저장·조회·교체하는\
    \ AWS Managed 서비스\n\n### 저장 대상\n\n- Database Username / Password\n- API Key\n- OAuth Client Secret\n- External\
    \ Service Token\n\n### IAM과 연결\n\n```text\nAPI Pod\n ↓\nPod Identity\n ↓\nIAM Role\n ↓\nsecretsmanager:GetSecretValue\n\
    \ ↓\nSecrets Manager\n```\n\n### KMS와 Secrets Manager 관계\n\n정확한 흐름:\n\n```text\nPlain Secret\n   ↓\nSecrets\
    \ Manager\n   ↓\nKMS Key 사용\n   ↓\nEncrypted Secret 저장\n```\n\n사용자가 먼저 KMS로 직접 암호화해서 Secrets Manager에 넣는다는 의미가\
    \ 아니라, Secrets Manager가 저장 시 KMS Key를 사용해 암호화한다고 이해한다.\n\n조회 시:\n\n```text\nEKS Pod\n ↓\nIAM Role\n ↓\nSecrets\
    \ Manager\n ↓\nKMS를 이용해 복호화\n ↓\nSecret 반환\n```\n\n역할 정리:\n\n```text\nSecrets Manager\n= Secret 저장 / 조회 / Rotation\n\
    \nKMS\n= Secret 암호화 Key 관리\n\nIAM\n= 누가 Secret과 Key를 사용할 수 있는지 제어\n```\n\n### Secret Rotation\n\n```text\nOld\
    \ Password\n ↓\nRotation\n ↓\nNew Password\n```\n\nRDS Credential 등과 연동해 Secret Lifecycle을 자동화할 수 있다.\n\n###\
    \ Kubernetes Secret과 차이\n\n```text\nKubernetes Secret\n= Kubernetes 내부 Secret Resource\n\nAWS Secrets Manager\n\
    = AWS Managed Secret Store\n```\n\n둘은 별개지만 연동할 수 있다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 539–634
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-07
  knowledge: "## 6.6 CloudWatch\n\nCloudWatch:\n\n> AWS Resource와 Application의 상태를 관찰하는 Monitoring 서비스\n\nBasic에서는\
    \ 세 가지가 핵심이다.\n\n```text\nMetrics\nLogs\nAlarm\n```\n\n### Metrics\n\n예:\n\n```text\nEC2 → CPUUtilization\n\
    ALB → RequestCount / TargetResponseTime\nRDS → CPU / Connection / Storage\nSQS → Queue Message 수\n```\n\n###\
    \ Logs\n\n```text\nEKS Pod\n ↓\nApplication Log\n ↓\nCloudWatch Logs\n```\n\nMetric은 상태 수치, Log는 상세 사건 기록이다.\n\
    \n### Alarm\n\n```text\nCPU > 80%\n5분 지속\n ↓\nCloudWatch Alarm\n```\n\n또는:\n\n```text\nSQS Queue Depth > 1000\n\
    \ ↓\nAlarm\n```\n\n### Auto Scaling과 연결\n\n```text\nCloudWatch Metric\n   ↓\nCPU 80%\n   ↓\nScaling Policy\n\
    \   ↓\nASG Scale Out\n```\n\n### EKS에서\n\n```text\nInfrastructure\n→ Node CPU / Memory\n\nApplication\n→ Pod\
    \ Log / App Metric\n```\n\n### CloudWatch vs Prometheus/Grafana\n\n```text\nCloudWatch\n= AWS Resource 중심 Managed\
    \ Monitoring\n\nPrometheus\n= Metric 수집 / Time Series Monitoring\n\nGrafana\n= Dashboard / Visualization\n```\n\
    \n---"
  kind: concept,example,condition,workflow
  source_lines: 635–725
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-08
  knowledge: "## 6.7 CloudTrail\n\nCloudTrail:\n\n> AWS에서 누가, 언제, 어떤 API를 호출해서 무엇을 했는지 기록하는 Audit 서비스\n\n### 기록\
    \ 정보\n\n```text\nWho → 어떤 User / Role\nWhen → 언제\nWhat → 어떤 AWS API\nWhere → 어떤 Region / Resource\n```\n\n###\
    \ CloudWatch와 차이\n\n```text\nCloudWatch\n= 시스템 상태 / 성능\n\nCloudTrail\n= AWS API 활동 기록\n```\n\n예:\n\n```text\n\
    EC2 CPU 95%\n→ CloudWatch\n\n누가 EC2를 삭제했는가?\n→ CloudTrail\n```\n\n### Console 작업도 API\n\n```text\nAWS Console\n\
    \ ↓\nAWS API\n ↓\nCloudTrail\n```\n\n### 보안 사고 조사\n\nSecurity Group, IAM Policy, S3 설정 등의 변경 주체와 시점을 추적하는 데\
    \ 중요하다.\n\n### CloudTrail + CloudWatch\n\n```text\nCloudTrail\n→ 누가 무엇을 했는지\n\nCloudWatch\n→ 그 결과 시스템 상태가 어떻게\
    \ 변했는지\n```\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 726–786
  destination: aws-cloud/managed-services.md
- id: AWSC2-06-09
  knowledge: '# Chapter 6 전체 요약


    ```text

    SQS = Task Queue

    SNS = Pub/Sub / Fan-out

    MSK = Managed Kafka / Event Streaming

    KMS = Encryption Key 관리

    Secrets Manager = Secret 저장 / 조회 / Rotation

    CloudWatch = Monitoring

    CloudTrail = Audit

    ```


    ---'
  kind: concept,example,condition,workflow
  source_lines: 787–800
  destination: aws-cloud/managed-services.md
- id: AWSC2-07-01
  knowledge: "## 7.1 GPU EC2\n\nGPU EC2:\n\n> GPU가 장착된 EC2 Instance\n\n```text\n일반 EC2\n→ CPU + Memory\n\nGPU EC2\n\
    → CPU + Memory + GPU\n```\n\n대표 용도:\n- LLM Inference\n- Model Training\n- Image / Video AI\n- CUDA Workload\n\
    \n### GPU VRAM\n\nLLM Serving에서는 GPU VRAM이 핵심 자원이다.\n\n```text\nGPU\n├─ Compute\n└─ VRAM\n```\n\n모델이 한 GPU에\
    \ 들어가지 않으면 여러 GPU에 분산할 수 있다.\n\n### GPU EC2도 일반 AWS 구조를 따른다\n\n```text\nVPC\n ↓\nPrivate Subnet\n ↓\nGPU EC2\n\
    ├─ Security Group\n├─ IAM Role\n├─ EBS\n└─ GPU\n```\n\n### Container와 GPU\n\n```text\nECR\n ↓\nGPU EC2\n ↓\n\
    Container\n ↓\nvLLM\n ↓\nGPU\n```\n\n### Model Storage\n\n```text\nECR\n→ vLLM 실행 Image\n\nS3\n→ Model Weight\n\
    ```\n\n실행 흐름:\n\n```text\nGPU EC2\n ↓\nECR에서 Image Pull\n ↓\nS3에서 Model 다운로드\n ↓\nGPU VRAM에 Model Load\n ↓\n\
    Serving Ready\n```\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 803–888
  destination: aws-cloud/ai-gpu-architecture.md
- id: AWSC2-07-02
  knowledge: "## 7.2 EKS GPU Node\n\nEKS GPU Node:\n\n> GPU EC2를 EKS Worker Node로 사용하는 것\n\n```text\nEKS\n├─ General\
    \ Node Group\n│  ├─ CPU EC2\n│  └─ CPU EC2\n└─ GPU Node Group\n   ├─ GPU EC2\n   └─ GPU EC2\n```\n\n### 왜 분리하는가?\n\
    \n```text\nGeneral Node Group\n→ API / Backend / Agent\n\nGPU Node Group\n→ vLLM / AI Inference\n```\n\n###\
    \ 특정 Pod만 GPU Node에 배치\n\nKubernetes Scheduling 기능 활용:\n- Label\n- NodeSelector\n- Taint\n- Toleration\n- Affinity\n\
    \n### GPU Resource Request\n\n```text\nPod\nresources:\n  GPU: 1\n```\n\nScheduler는 GPU Capacity가 남아 있는 Node를\
    \ 찾는다.\n\n### NVIDIA Device Plugin\n\n```text\nGPU EC2\n ↓\nNVIDIA Driver\n ↓\nNVIDIA Device Plugin\n ↓\nKubernetes에서\
    \ GPU Resource 인식\n ↓\nGPU Pod Scheduling\n```\n\n### GPU Node Scaling\n\n```text\nvLLM Pod 증가\n ↓\nGPU Capacity\
    \ 부족\n ↓\nGPU Node Group Scale Out\n ↓\nGPU EC2 추가\n```\n\nGPU는 비싸므로 최소 Node 수, Scale Out 조건, Idle 시간, Spot\
    \ 여부 등을 신중하게 본다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 889–963
  destination: aws-cloud/ai-gpu-architecture.md
- id: AWSC2-07-03
  knowledge: "## 7.3 ECR + S3 Model Storage\n\nAI Serving에서는 실행 코드와 모델을 분리한다.\n\n```text\nECR\n→ 실행 환경 / Container\
    \ Image\n\nS3\n→ Model Weight / Tokenizer / Artifact\n```\n\n### 왜 Model을 ECR Image 안에 넣지 않는가?\n\n모델은 매우 클 수\
    \ 있다.\n\n```text\nImage 크기 증가\n↓\nBuild 느림\n↓\nPush/Pull 느림\n↓\nModel 변경 때 Image 재Build\n```\n\n그래서 Code와 Model\
    \ Lifecycle을 분리한다.\n\n### Pod 시작 흐름\n\n```text\nEKS GPU Node\n ↓\nECR에서 vLLM Image Pull\n ↓\nS3에서 Model 다운로드\n\
    \ ↓\nLocal Disk / Cache 저장\n ↓\nGPU VRAM에 Load\n ↓\nServing Ready\n```\n\n정리:\n\n```text\nECR\n= 무엇을 실행할 것인가\n\
    \nS3\n= 어떤 모델을 실행할 것인가\n```\n\n### IAM 권한\n\n```text\nvLLM Pod\n ↓\nPod Identity\n ↓\nIAM Role\n ↓\ns3:GetObject\n\
    \ ↓\nmodel-prod/*\n```\n\n### Model Versioning\n\n```text\ns3://model-bucket/\n├─ llama-v1/\n├─ llama-v2/\n\
    └─ llama-v3/\n```\n\nContainer Image는 그대로 두고 Model Version만 바꿀 수 있다.\n\n### Model Cache\n\n```text\nS3\n ↓ 최초\
    \ 다운로드\nNode Local Disk / EBS / Cache\n ↓\nGPU Pod\n```\n\nS3는 원본 Model Storage, 실제 Serving에서는 Node 근처에 캐시할\
    \ 수 있다.\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 964–1056
  destination: aws-cloud/ai-gpu-architecture.md
- id: AWSC2-07-04
  knowledge: "## 7.4 vLLM Serving 구조\n\n기본 요청 흐름:\n\n```text\nUser\n ↓ HTTPS\nALB\n ↓\nKubernetes Service\n ↓\n\
    vLLM Pod\n ↓\nGPU\n ↓\nModel\n```\n\n### GPU Node 배치\n\n```text\nEKS\n├─ General Node Group\n│  └─ API / Backend\
    \ Pods\n└─ GPU Node Group\n   └─ vLLM Pods\n```\n\n### API Layer 분리\n\n실무에서는 vLLM을 외부에 직접 노출하지 않고 API Layer를\
    \ 둘 수 있다.\n\n```text\nUser\n ↓\nALB\n ↓\nAPI Pod\n ↓\nvLLM Service\n ↓\nvLLM Pod\n ↓\nGPU\n```\n\nAPI Layer\
    \ 역할 예:\n- 인증\n- Rate Limit\n- 요청 검증\n- Model Routing\n- Usage Logging\n\n### 여러 vLLM Replica\n\n```text\nService\n\
    ├─ vLLM Pod A → GPU A\n├─ vLLM Pod B → GPU B\n└─ vLLM Pod C → GPU C\n```\n\nGPU Memory와 Model Loading 비용이 크므로\
    \ 일반 Web Pod처럼 무작정 Replica를 늘리면 비용이 크다.\n\n### Scaling과 Cold Start\n\n```text\n새 GPU EC2 생성\n ↓\nECR Image Pull\n\
    \ ↓\nS3 Model Download\n ↓\nGPU VRAM Load\n ↓\nReady\n```\n\n실무 고려:\n- 최소 GPU Node 유지\n- Model Cache\n- Autoscaling\n\
    - 트래픽 예측\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 1057–1142
  destination: aws-cloud/ai-gpu-architecture.md
- id: AWSC2-07-05
  knowledge: "## 7.5 End-to-End AWS Architecture\n\n전체 구조:\n\n```text\nAWS Account\n└─ Seoul Region\n   └─ VPC\n\
    \      │\n      ├─ Public Subnets\n      │   ├─ ALB\n      │   └─ NAT Gateway\n      │\n      └─ Private Subnets\n\
    \          ├─ EKS\n          │   ├─ General Node Group\n          │   └─ GPU Node Group\n          ├─ RDS /\
    \ Aurora\n          ├─ ElastiCache\n          └─ MSK\n```\n\nVPC 주변 Managed Services:\n\n```text\nS3\nECR\n\
    SQS / SNS\nKMS\nSecrets Manager\nCloudWatch\nCloudTrail\n```\n\n### 사용자 요청 흐름\n\n일반 API:\n\n```text\nUser\n\
    \ ↓\nInternet\n ↓\nALB\n ↓\nEKS Service\n ↓\nAPI Pod\n ↓\nRDS / ElastiCache\n```\n\nLLM 요청:\n\n```text\nUser\n\
    \ ↓\nALB\n ↓\nAPI Pod\n ↓\nvLLM Service\n ↓\nGPU Pod\n ↓\nGPU\n```\n\n### 데이터 저장 역할\n\n```text\nRDS / Aurora\n\
    → 사용자 / 설정 / Transactional Data\n\nElastiCache\n→ Cache / Session\n\nS3\n→ Dataset / Model / Backup / Object\n\
    \nEBS\n→ Pod 또는 EC2의 Block Disk\n\nEFS\n→ 여러 Pod가 공유하는 File System\n```\n\n### 비동기 / 이벤트\n\n```text\nSQS\n→\
    \ 하나의 작업을 Worker에게 전달\n\nSNS\n→ 하나의 이벤트를 여러 Subscriber에게 전달\n\nMSK\n→ 이벤트를 보존하고 여러 Consumer Group이 독립 소비\n```\n\
    \n예:\n\n```text\nAPI\n ↓\nSQS\n ↓\nEvaluation Worker\n```\n\n또는:\n\n```text\nUser Click\n ↓\nMSK\n├─ Analytics\n\
    ├─ Recommendation\n└─ Monitoring\n```\n\n### Security\n\n```text\nIAM\n→ 누가 AWS Resource에 접근 가능한가\n\nPod Identity\n\
    → Pod별 IAM Role\n\nSecurity Group\n→ Network 접근 제어\n\nKMS\n→ Encryption Key 관리\n\nSecrets Manager\n→ Password\
    \ / API Key 저장\n```\n\n### Observability / Audit\n\n```text\nCloudWatch\n→ Metric / Log / Alarm\n\nCloudTrail\n\
    → AWS API Audit\n```\n\n### 최종 AI/Data Platform 구조\n\n```text\n                         Internet\n         \
    \                   ↓\n                           ALB\n                            ↓\n                     \
    \      EKS\n                 ┌──────────┴──────────┐\n                 │                     │\n        General\
    \ Node Group       GPU Node Group\n                 │                     │\n         API / Agent Pods     \
    \     vLLM Pods\n          /      |      \\               │\n         ↓       ↓       ↓              ↓\n   \
    \    RDS   ElastiCache  SQS          GPU\n                          │              ↑\n                     \
    \     ↓              │\n                       Workers           │\n                                       \
    \  │\nECR ─────────────→ Container Images      │\nS3 ──────────────→ Model / Dataset ─────┘\n\nMSK\n→ Event\
    \ Streaming\n\nSNS\n→ Event Fan-out\n\nKMS\n→ Encryption\n\nSecrets Manager\n→ Secrets\n\nCloudWatch\n→ Monitoring\n\
    \nCloudTrail\n→ Audit\n```\n\n---"
  kind: concept,example,condition,workflow
  source_lines: 1143–1336
  destination: aws-cloud/ai-gpu-architecture.md
---

# AWS 6~7장 지식 추출

번호 절·비교 보충·요약·완료 기록을 원문 내용과 함께 추적한다. 6.1.1을 별도 ID로 유지한다.
