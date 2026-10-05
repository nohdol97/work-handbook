---
id: aws-cloud-managed-services
status: studied
last_updated: 2026-10-05
last_reviewed: 2026-10-05
knowledge_ids:
  - AWSC2-06-01
  - AWSC2-06-02
  - AWSC2-06-03
  - AWSC2-06-04
  - AWSC2-06-05
  - AWSC2-06-06
  - AWSC2-06-07
  - AWSC2-06-08
  - AWSC2-06-09
---

# Chapter 6. AWS Managed Services

제공된 6장 원문의 번호·순서·예시와 6.1.1·전체 요약을 보존했다. SQS/FIFO의 중복·순서, SNS subscriber 종류, MSK 운영 책임, KMS·Secrets Manager 암호화, CloudWatch·CloudTrail 수집 범위는 뒤의 별도 보완 조건과 함께 읽는다. 실제 AWS 운영이나 실험을 수행한 기록이 아니다.

<!-- SOURCE CORE START -->

## 6.1 SQS

SQS = **Simple Queue Service**

> 서비스 사이의 메시지를 Queue에 저장해두고 비동기로 처리하는 AWS Managed Message Queue

기본 구조:

```text
Producer
   ↓
  SQS
   ↓
Consumer
```

예:

```text
API Pod
 ↓
SQS
 ↓
Worker Pod
```

API가 오래 걸리는 작업을 직접 처리하지 않고 Queue에 넣은 뒤 바로 응답할 수 있다.

### 왜 SQS를 쓰는가?

```text
User
 ↓
API
 ↓
SQS에 Job 저장
 ↓
즉시 응답

Worker
 ↓
SQS에서 Job 가져옴
 ↓
실제 처리
```

핵심 효과:
- Producer와 Consumer 분리
- 트래픽 급증 흡수
- 비동기 처리
- 장애 시 재시도 가능

### Consumer Polling

SQS는 Consumer가 Queue에서 메시지를 가져간다.

```text
Worker
 ↓ poll
SQS
 ↓
Message
```

Kafka처럼 Event Stream을 지속적으로 읽는 감각보다는 Queue에 쌓인 Task를 Worker가 가져가 처리하는 모델에 가깝다.

### Visibility Timeout

Consumer가 메시지를 가져가도 즉시 삭제되지 않는다.

```text
Worker A가 Message 수신
 ↓
Visibility Timeout
 ↓
다른 Worker에게 잠시 숨김
```

Worker가 처리 완료 후 Delete하면 메시지가 제거된다.

실패해서 Delete하지 못하면:

```text
처리 실패
 ↓
Visibility Timeout 만료
 ↓
Message 재노출
 ↓
다른 Worker가 다시 처리 가능
```

### Dead Letter Queue

계속 실패하는 메시지를 별도 Queue로 격리할 수 있다.

```text
Main Queue
 ↓ 반복 실패
DLQ
```

용도:
- 실패 메시지 분석
- 오류 원인 확인
- 수동 재처리

### Standard vs FIFO

#### Standard Queue
- 높은 처리량
- 순서가 완전히 보장되지는 않음
- 중복 전달 가능성을 고려해야 함
- Consumer는 Idempotent하게 만드는 것이 좋음

#### FIFO Queue
FIFO = First-In-First-Out.

```text
A
B
C
→ A → B → C
```

기본 선택 기준:

```text
일반 비동기 작업
→ Standard

순서가 중요
→ FIFO
```

### EKS와 SQS

```text
API Pods
   ↓
  SQS
   ↓
Worker Pods
```

Queue Depth가 늘면 Worker Pod 수를 늘리는 Auto Scaling 구조도 만들 수 있다.

AI Platform 예:

```text
사용자 요청
 ↓
API
 ↓
SQS
 ↓
Evaluation Worker
 ↓
LLM Evaluation 실행
```

---

## 6.1.1 SQS vs Kafka

중요한 차이는 **병렬 처리 여부가 아니다.** SQS도 Consumer를 여러 개 두면 병렬 처리가 가능하다.

핵심 차이:

```text
SQS
= Task Queue

Kafka
= Event Log / Event Streaming Platform
```

### SQS

```text
Producer
 ↓
Queue
 ↓
Worker A / B / C
```

느낌:

> "이 작업을 누군가 한 번 처리해줘."

예:
- 이미지 변환 Job
- 이메일 발송
- LLM Evaluation Job
- 주문 후처리

처리 완료 후 메시지는 보통 삭제된다.

### Kafka

```text
Event
 ↓
Kafka Topic
 ↓
Consumer Groups
```

느낌:

> "이 이벤트가 발생했으니 기록해둘게. 필요한 시스템이 각자 읽어."

예:

```text
click event
 ↓
Kafka
├─ Analytics Group
├─ Recommendation Group
└─ Monitoring Group
```

한 Consumer가 읽었다고 Event가 없어지는 것이 아니다.

### Replay

Kafka는 Offset을 되돌려 과거 Event를 다시 읽을 수 있다.

```text
지난 3일 이벤트
 ↓ Replay
새 알고리즘으로 재처리
```

SQS는 이런 장기 Event Log / Replay 용도로 설계된 서비스가 아니다.

### 병렬 처리 방식

SQS:

```text
Queue
 ↓
Worker A
Worker B
Worker C
```

Kafka:

```text
Topic
├─ Partition 0 → Consumer A
├─ Partition 1 → Consumer B
└─ Partition 2 → Consumer C
```

Partition이 Kafka의 병렬 처리 단위가 된다.

| 항목 | SQS | Kafka |
|---|---|---|
| 모델 | Queue | Distributed Log |
| 목적 | Task 전달 | Event 보존/Streaming |
| 처리 후 | Delete | 일정 기간 보존 |
| Replay | 제한적 | Offset 기반 가능 |
| 여러 독립 Consumer | 별도 구성 | Consumer Group |
| 병렬 처리 | Consumer 수 | Partition + Consumer |
| 대표 용도 | 비동기 Job | Event Pipeline |

---

## 6.2 SNS

SNS = **Simple Notification Service**

> 하나의 메시지를 여러 Subscriber에게 동시에 전달하는 Managed Pub/Sub 서비스

```text
Publisher
   ↓
 SNS Topic
 ├─ Subscriber A
 ├─ Subscriber B
 └─ Subscriber C
```

### Topic

메시지는 Topic에 Publish한다.

```text
Order Service
   ↓
SNS Topic
├─ Email Service
├─ Analytics
└─ Notification Service
```

### SNS vs SQS

```text
SQS
= 1개의 작업을 Worker에게 분배

SNS
= 1개의 이벤트를 여러 곳에 Broadcast
```

### SNS + SQS

실무에서 흔한 Fan-out 패턴:

```text
            SNS Topic
          /     |      \
         ↓      ↓       ↓
      SQS A   SQS B   SQS C
        ↓       ↓       ↓
     Worker   Worker   Worker
```

장점:
- 시스템 간 결합도 감소
- 각 Consumer 속도 차이 흡수
- 실패/재시도 독립
- 한 시스템 장애가 다른 시스템에 덜 영향

### Subscriber 종류

대표적으로:
- SQS
- HTTP/HTTPS Endpoint
- Lambda
- Email
- SMS

Basic에서는 AWS 서비스 간 이벤트 분배에 SNS → SQS / Lambda 조합이 흔하다고 이해하면 충분하다.

---

## 6.3 Amazon MSK

MSK = **Managed Streaming for Apache Kafka**

> AWS가 Kafka Broker 인프라 운영을 상당 부분 대신해주는 Managed Kafka 서비스

Kafka 자체 개념은 이미 학습한 것으로 보고 AWS 관점만 다룬다.

### 직접 Kafka 운영 vs MSK

직접 운영:

```text
EC2 / EKS
 ↓
Kafka Cluster
├─ Broker
├─ Storage
├─ Replication
├─ Patch
└─ Failure Handling
```

MSK:

```text
Producer / Consumer
        ↓
       MSK
```

### VPC 내부 배치

보통 Private Subnet에 Broker를 배치한다.

```text
VPC
├─ Private Subnet A
│  └─ MSK Broker
├─ Private Subnet B
│  └─ MSK Broker
└─ Private Subnet C
   └─ MSK Broker
```

EKS Application은 VPC 내부에서 접근한다.

### Multi-AZ

```text
AZ A → Broker
AZ B → Broker
AZ C → Broker
```

Kafka Replication과 AWS Multi-AZ를 함께 활용한다.

### Security

```text
Network
→ VPC / Security Group

Authentication
→ Kafka Client 인증

Encryption
→ 전송 / 저장 암호화
```

### EKS + MSK

```text
Users / Services
      ↓
     EKS
      ↓
     MSK
      ↓
 ┌────┼─────┐
 ↓    ↓     ↓
Analytics
Data Pipeline
Monitoring
```

### SQS vs MSK

```text
SQS
= Task Queue

MSK
= Event Streaming / Event Log
```

예:

```text
이미지 변환 Job
→ SQS

사용자 Click Event
→ MSK
```

---

## 6.4 KMS

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

---

## 6.5 Secrets Manager

Secrets Manager:

> DB Password, API Key, Token 같은 민감한 값을 안전하게 저장·조회·교체하는 AWS Managed 서비스

### 저장 대상

- Database Username / Password
- API Key
- OAuth Client Secret
- External Service Token

### IAM과 연결

```text
API Pod
 ↓
Pod Identity
 ↓
IAM Role
 ↓
secretsmanager:GetSecretValue
 ↓
Secrets Manager
```

### KMS와 Secrets Manager 관계

정확한 흐름:

```text
Plain Secret
   ↓
Secrets Manager
   ↓
KMS Key 사용
   ↓
Encrypted Secret 저장
```

사용자가 먼저 KMS로 직접 암호화해서 Secrets Manager에 넣는다는 의미가 아니라, Secrets Manager가 저장 시 KMS Key를 사용해 암호화한다고 이해한다.

조회 시:

```text
EKS Pod
 ↓
IAM Role
 ↓
Secrets Manager
 ↓
KMS를 이용해 복호화
 ↓
Secret 반환
```

역할 정리:

```text
Secrets Manager
= Secret 저장 / 조회 / Rotation

KMS
= Secret 암호화 Key 관리

IAM
= 누가 Secret과 Key를 사용할 수 있는지 제어
```

### Secret Rotation

```text
Old Password
 ↓
Rotation
 ↓
New Password
```

RDS Credential 등과 연동해 Secret Lifecycle을 자동화할 수 있다.

### Kubernetes Secret과 차이

```text
Kubernetes Secret
= Kubernetes 내부 Secret Resource

AWS Secrets Manager
= AWS Managed Secret Store
```

둘은 별개지만 연동할 수 있다.

---

## 6.6 CloudWatch

CloudWatch:

> AWS Resource와 Application의 상태를 관찰하는 Monitoring 서비스

Basic에서는 세 가지가 핵심이다.

```text
Metrics
Logs
Alarm
```

### Metrics

예:

```text
EC2 → CPUUtilization
ALB → RequestCount / TargetResponseTime
RDS → CPU / Connection / Storage
SQS → Queue Message 수
```

### Logs

```text
EKS Pod
 ↓
Application Log
 ↓
CloudWatch Logs
```

Metric은 상태 수치, Log는 상세 사건 기록이다.

### Alarm

```text
CPU > 80%
5분 지속
 ↓
CloudWatch Alarm
```

또는:

```text
SQS Queue Depth > 1000
 ↓
Alarm
```

### Auto Scaling과 연결

```text
CloudWatch Metric
   ↓
CPU 80%
   ↓
Scaling Policy
   ↓
ASG Scale Out
```

### EKS에서

```text
Infrastructure
→ Node CPU / Memory

Application
→ Pod Log / App Metric
```

### CloudWatch vs Prometheus/Grafana

```text
CloudWatch
= AWS Resource 중심 Managed Monitoring

Prometheus
= Metric 수집 / Time Series Monitoring

Grafana
= Dashboard / Visualization
```

---

## 6.7 CloudTrail

CloudTrail:

> AWS에서 누가, 언제, 어떤 API를 호출해서 무엇을 했는지 기록하는 Audit 서비스

### 기록 정보

```text
Who → 어떤 User / Role
When → 언제
What → 어떤 AWS API
Where → 어떤 Region / Resource
```

### CloudWatch와 차이

```text
CloudWatch
= 시스템 상태 / 성능

CloudTrail
= AWS API 활동 기록
```

예:

```text
EC2 CPU 95%
→ CloudWatch

누가 EC2를 삭제했는가?
→ CloudTrail
```

### Console 작업도 API

```text
AWS Console
 ↓
AWS API
 ↓
CloudTrail
```

### 보안 사고 조사

Security Group, IAM Policy, S3 설정 등의 변경 주체와 시점을 추적하는 데 중요하다.

### CloudTrail + CloudWatch

```text
CloudTrail
→ 누가 무엇을 했는지

CloudWatch
→ 그 결과 시스템 상태가 어떻게 변했는지
```

---

# Chapter 6 전체 요약

```text
SQS = Task Queue
SNS = Pub/Sub / Fan-out
MSK = Managed Kafka / Event Streaming
KMS = Encryption Key 관리
Secrets Manager = Secret 저장 / 조회 / Rotation
CloudWatch = Monitoring
CloudTrail = Audit
```

---

<!-- SOURCE CORE END -->

## 보완 — 전달 보장·암호화·관측의 적용 조건

2026-10-05 AWS 공식 문서를 확인했다. 아래는 원문을 바꾸지 않고 추가한 조건과 설명이며 AWS Resource 생성·권한 변경·메시지 처리·Secret 조회를 실행한 결과가 아니다.

### 6.1 / 6.1.1 SQS의 중복·순서와 병렬 처리

Standard Queue는 at-least-once 전달이며 중복 수신을 고려해야 한다. FIFO의 순서는 `MessageGroupId` 내부에서 보장하며 서로 다른 group은 병렬 처리할 수 있다. FIFO에서도 메시지를 처리한 뒤 삭제하지 못하고 visibility timeout이 만료되면 다시 수신할 수 있으므로, 외부 DB 변경 같은 처리 효과까지 정확히 한 번이라고 가정하지 않는다. [SQS standard delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html), [FIFO delivery logic](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html), [Visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)

6.1.1의 “Consumer 수”는 병렬성의 한 요소다. 실제 처리량은 FIFO group 수, 작업 시간, 처리 자원과 downstream 한계에도 영향을 받는다. Kafka의 replay 역시 보존 중인 event 범위 안에서 가능하다. [Kafka의 partition·retention·consumer group](../platform-infrastructure/kafka.md)

### 6.2 SNS subscriber는 Topic 종류에 따라 다르다

원문의 “동시에 전달”은 fan-out 개념이며 모든 subscriber가 같은 시각에 처리한다는 보장이 아니다. 나열한 Email·SMS·HTTP(S)와 직접 Lambda 구독은 Standard Topic 범위로 읽는다. SNS FIFO Topic은 SQS Standard/FIFO Queue로 전달하며, Lambda에는 SQS를 거쳐 연결한다. Standard Queue를 구독하면 FIFO의 전체 전달 보장이 그대로 유지되는 것은 아니다. [SNS FIFO message delivery](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html)

### 6.3 Managed Kafka에도 애플리케이션 책임이 남는다

MSK는 broker 인프라 운영 부담을 줄이지만 topic·partition·retention 설계와 producer/consumer 동작까지 대신 설계하지는 않는다. 원문의 broker·subnet 그림은 Provisioned 구성을 이해하기 위한 예다. MSK Serverless와 Provisioned의 용량 관리 책임을 구분한다. [MSK 소개](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html), [MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html)

### 6.4 KMS 권한·키 종류·Rotation

KMS 접근은 Key Policy, IAM Policy, grant 등을 함께 평가한다. IAM Allow만으로 충분하다고 가정하지 않고, Key Policy가 IAM을 통한 권한 부여를 허용하는지도 확인한다. AWS 서비스의 저장 데이터 암호화에는 대칭 암호화 KMS key를 사용한다. 비대칭 key는 public/private key 쌍이며 용도가 다르다. [KMS key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html), [KMS asymmetric keys](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html)

KMS key material rotation은 기존 데이터를 다시 암호화하거나 DB 비밀번호를 교체하지 않는다. AWS_KMS origin key는 과거 key material을 보관해 기존 암호문을 복호화한다. 자동 rotation은 AWS KMS가 생성한 key material을 가진 대칭 암호화 key에 적용되며 비대칭 key에는 같은 자동 방식을 적용할 수 없다. [KMS key rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)

### 6.5 Secrets Manager의 envelope encryption과 조회 권한

정확히는 KMS key가 data key를 보호하고, Secrets Manager가 그 data key로 Secret 값을 암호화하는 envelope encryption이다. Customer managed key를 쓰는 Secret 조회에는 `secretsmanager:GetSecretValue`와 해당 key의 `kms:Decrypt` 권한이 필요하다. [Secret encryption](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html), [GetSecretValue](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)

`GetSecretValue` 호출은 CloudTrail에 기록되지만 응답의 `SecretString`·`SecretBinary` 값은 해당 기록에 포함하지 않는다. 애플리케이션이 직접 남기는 로그에서도 비밀값을 제외해야 한다. Secret 비밀번호 교체와 KMS key material rotation은 다른 작업이다. [GetSecretValue logging](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)

### 6.6 CloudWatch 수집 경로를 따로 구성

Node memory·Pod log·사용자 정의 app metric이 EKS 생성만으로 모두 수집된다는 뜻은 아니다. CloudWatch agent 등 수집기와 대상 metric/log 설정, 전송 권한이 필요하다. 원문의 임계값은 학습 예시이며 실제 Alarm 평가 기간과 scaling 정책을 검증한 값은 아니다. [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)

### 6.7 CloudTrail이 기록하는 범위

기본 Event history는 해당 Region의 최근 90일 management event를 보여준다. 모든 API·S3 object 접근 등 data event가 여기에 자동 포함되는 것은 아니다. 지속 보관이나 필요한 data event는 trail/event data store의 수집 대상과 보존 설정을 별도로 확인한다. [CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)

## 관련 문서

- [AWS 학습 범위](index.md)
- [EKS](eks.md)
- [스토리지와 데이터베이스](storage-databases.md)
- [Kafka](../platform-infrastructure/kafka.md)
- [Platform 보안](../platform-infrastructure/platform-security.md)
