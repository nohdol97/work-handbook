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

This page preserves the supplied Chapter 6 numbering, order, and examples, including 6.1.1 and the chapter summary. Read the separate supplement for SQS/FIFO duplicates and ordering, SNS subscriber types, MSK responsibilities, KMS and Secrets Manager encryption, and CloudWatch/CloudTrail collection scope. These notes do not record actual AWS operations or experiments.

<!-- SOURCE CORE START -->

## 6.1 SQS

SQS = **Simple Queue Service**

> An AWS managed message queue that stores messages between services for asynchronous processing

Basic structure:

```text
Producer
   ↓
  SQS
   ↓
Consumer
```

Example:

```text
API Pod
 ↓
SQS
 ↓
Worker Pod
```

An API can put a long-running task in a queue and respond immediately instead of processing it directly.

### Why Use SQS?

```text
User
 ↓
API
 ↓
Store a job in SQS
 ↓
Respond immediately

Worker
 ↓
Fetch a job from SQS
 ↓
Process the job
```

Main benefits:
- Decouple producers and consumers
- Absorb traffic spikes
- Asynchronous processing
- Retry after failures

### Consumer Polling

With SQS, consumers fetch messages from the queue.

```text
Worker
 ↓ poll
SQS
 ↓
Message
```

The model is closer to workers fetching and processing queued tasks than to continuously reading an event stream as in Kafka.

### Visibility Timeout

A message is not deleted immediately when a consumer receives it.

```text
Worker A receives a message
 ↓
Visibility Timeout
 ↓
Temporarily hidden from other workers
```

The message is removed when the worker deletes it after processing.

If processing fails and the worker cannot delete it:

```text
Processing fails
 ↓
Visibility timeout expires
 ↓
Message becomes visible again
 ↓
Another worker can process it again
```

### Dead Letter Queue

Messages that keep failing can be isolated in a separate queue.

```text
Main Queue
 ↓ Repeated failure
DLQ
```

Uses:
- Analyze failed messages
- Identify error causes
- Manual reprocessing

### Standard vs FIFO

#### Standard Queue
- High throughput
- Order is not fully guaranteed
- Account for possible duplicate delivery
- Consumers should be idempotent

#### FIFO Queue
FIFO = First-In-First-Out.

```text
A
B
C
→ A → B → C
```

Basic selection criteria:

```text
General asynchronous tasks
→ Standard

Ordering matters
→ FIFO
```

### EKS and SQS

```text
API Pods
   ↓
  SQS
   ↓
Worker Pods
```

You can also build autoscaling that adds worker Pods when queue depth grows.

AI platform example:

```text
User request
 ↓
API
 ↓
SQS
 ↓
Evaluation Worker
 ↓
Run LLM evaluation
```

---

## 6.1.1 SQS vs Kafka

The key difference is **not whether parallel processing is possible.** SQS also supports parallel processing with multiple consumers.

Key difference:

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

Mental model:

> "Someone, please process this task once."

Example:
- Image conversion jobs
- Sending email
- LLM Evaluation Job
- Order follow-up processing

Messages are usually deleted after processing.

### Kafka

```text
Event
 ↓
Kafka Topic
 ↓
Consumer Groups
```

Mental model:

> "This event happened, so I will record it. Each system that needs it can read it."

Example:

```text
click event
 ↓
Kafka
├─ Analytics Group
├─ Recommendation Group
└─ Monitoring Group
```

An event does not disappear when one consumer reads it.

### Replay

Kafka can replay past events by moving offsets back.

```text
Events from the last 3 days
 ↓ Replay
Reprocess with a new algorithm
```

SQS is not designed for this kind of long-term event log and replay.

### How Parallel Processing Works

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

Partitions are the unit of parallel processing in Kafka.

| Item | SQS | Kafka |
|---|---|---|
| Model | Queue | Distributed Log |
| Purpose | Task delivery | Event retention/streaming |
| After processing | Delete | Retain for a period |
| Replay | Limited | Possible using offsets |
| Multiple independent consumers | Separate setup | Consumer Group |
| Parallel processing | Number of consumers | Partition + Consumer |
| Typical use | Asynchronous jobs | Event Pipeline |

---

## 6.2 SNS

SNS = **Simple Notification Service**

> A managed pub/sub service that delivers one message to multiple subscribers at the same time

```text
Publisher
   ↓
 SNS Topic
 ├─ Subscriber A
 ├─ Subscriber B
 └─ Subscriber C
```

### Topic

Publish messages to a topic.

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
= Distribute a task to a worker

SNS
= Broadcast one event to multiple destinations
```

### SNS + SQS

A common fan-out pattern in practice:

```text
            SNS Topic
          /     |      \
         ↓      ↓       ↓
      SQS A   SQS B   SQS C
        ↓       ↓       ↓
     Worker   Worker   Worker
```

Benefits:
- Reduce coupling between systems
- Absorb differences in consumer speed
- Independent failures and retries
- Reduce the impact of one system's failure on others

### Subscriber Types

Common examples:
- SQS
- HTTP/HTTPS Endpoint
- Lambda
- Email
- SMS

At a basic level, understand that SNS → SQS / Lambda is a common combination for distributing events between AWS services.

---

## 6.3 Amazon MSK

MSK = **Managed Streaming for Apache Kafka**

> A managed Kafka service where AWS handles much of the Kafka broker infrastructure operation

This section assumes Kafka concepts have already been studied and covers only the AWS perspective.

### Self-Managed Kafka vs MSK

Self-managed:

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

### Placement Inside a VPC

Brokers are usually placed in private subnets.

```text
VPC
├─ Private Subnet A
│  └─ MSK Broker
├─ Private Subnet B
│  └─ MSK Broker
└─ Private Subnet C
   └─ MSK Broker
```

EKS applications access them from inside the VPC.

### Multi-AZ

```text
AZ A → Broker
AZ B → Broker
AZ C → Broker
```

Use Kafka replication together with AWS Multi-AZ placement.

### Security

```text
Network
→ VPC / Security Group

Authentication
→ Kafka client authentication

Encryption
→ Encryption in transit / at rest
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

Example:

```text
Image conversion job
→ SQS

User click event
→ MSK
```

---

## 6.4 KMS

KMS = **Key Management Service**

> A service that creates and manages encryption keys used to encrypt AWS resources

### Common Integrated Services

```text
S3 → Object encryption
EBS → Disk encryption
RDS → Database storage encryption
Secrets Manager → Secret encryption
```

KMS manages keys that other AWS services use to encrypt data; it is not a store for general data.

### Encryption at Rest vs In Transit

```text
At Rest
= Encryption of stored data

In Transit
= Encryption of data in transit
```

### AWS Managed Key vs Customer Managed Key

AWS Managed Key:
- AWS manages the key for a service

Customer Managed Key:
- Created by the user
- Manage the key policy
- Configure rotation
- Separate keys by environment or service

```text
Simple use
→ AWS Managed Key

Detailed control needed
→ Customer Managed Key
```

### IAM and KMS

```text
IAM
= Who can use AWS resources

KMS
= Who can use encryption keys
```

When reading a KMS-encrypted S3 object, depending on the situation:

```text
s3:GetObject
+
kms:Decrypt
```

Both permissions may be required.

### Key Rotation

KMS provides key lifecycle and rotation management.

---

## 6.5 Secrets Manager

Secrets Manager:

> An AWS managed service for securely storing, retrieving, and rotating sensitive values such as database passwords, API keys, and tokens

### What It Stores

- Database Username / Password
- API Key
- OAuth Client Secret
- External Service Token

### Connection to IAM

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

### Relationship Between KMS and Secrets Manager

The precise flow:

```text
Plain Secret
   ↓
Secrets Manager
   ↓
Use a KMS key
   ↓
Store the encrypted secret
```

This does not mean the user first encrypts a value with KMS and then puts it in Secrets Manager. Secrets Manager uses a KMS key to encrypt the value when storing it.

When retrieving:

```text
EKS Pod
 ↓
IAM Role
 ↓
Secrets Manager
 ↓
Decrypt using KMS
 ↓
Return the secret
```

Roles:

```text
Secrets Manager
= Secret storage / retrieval / rotation

KMS
= Manage secret encryption keys

IAM
= Control who can use secrets and keys
```

### Secret Rotation

```text
Old Password
 ↓
Rotation
 ↓
New Password
```

Integration with RDS credentials and other systems can automate the secret lifecycle.

### Difference from Kubernetes Secrets

```text
Kubernetes Secret
= A Secret resource inside Kubernetes

AWS Secrets Manager
= AWS Managed Secret Store
```

They are separate systems but can be integrated.

---

## 6.6 CloudWatch

CloudWatch:

> A monitoring service for observing the state of AWS resources and applications

At a basic level, three features are central.

```text
Metrics
Logs
Alarm
```

### Metrics

Example:

```text
EC2 → CPUUtilization
ALB → RequestCount / TargetResponseTime
RDS → CPU / Connection / Storage
SQS → Number of queued messages
```

### Logs

```text
EKS Pod
 ↓
Application Log
 ↓
CloudWatch Logs
```

Metrics are numerical measurements of state. Logs are detailed event records.

### Alarm

```text
CPU > 80%
For 5 minutes
 ↓
CloudWatch Alarm
```

Or:

```text
SQS Queue Depth > 1000
 ↓
Alarm
```

### Connection to Auto Scaling

```text
CloudWatch Metric
   ↓
CPU 80%
   ↓
Scaling Policy
   ↓
ASG Scale Out
```

### In EKS

```text
Infrastructure
→ Node CPU / Memory

Application
→ Pod Log / App Metric
```

### CloudWatch vs Prometheus/Grafana

```text
CloudWatch
= Managed monitoring centered on AWS resources

Prometheus
= Metric collection / time series monitoring

Grafana
= Dashboard / Visualization
```

---

## 6.7 CloudTrail

CloudTrail:

> An audit service that records who called which AWS API, when, and what they did

### Recorded Information

```text
Who → Which user / role
When → Time
What → Which AWS API
Where → Which region / resource
```

### Difference from CloudWatch

```text
CloudWatch
= System state / performance

CloudTrail
= AWS API activity records
```

Example:

```text
EC2 CPU 95%
→ CloudWatch

Who deleted the EC2 instance?
→ CloudTrail
```

### Console Actions Also Use APIs

```text
AWS Console
 ↓
AWS API
 ↓
CloudTrail
```

### Security Incident Investigation

It helps trace who changed security groups, IAM policies, S3 settings, and similar resources, and when.

### CloudTrail + CloudWatch

```text
CloudTrail
→ Who did what

CloudWatch
→ How system state changed as a result
```

---

# Chapter 6 Summary

```text
SQS = Task Queue
SNS = Pub/Sub / Fan-out
MSK = Managed Kafka / Event Streaming
KMS = Encryption key management
Secrets Manager = Secret storage / retrieval / rotation
CloudWatch = Monitoring
CloudTrail = Audit
```

---

<!-- SOURCE CORE END -->

## Supplement — Delivery, Encryption, and Observability Conditions

AWS official documentation checked on 2026-10-05. These conditions and explanations are separate from the source. No AWS resources were created, permissions changed, messages processed, or secrets retrieved.

### 6.1 / 6.1.1 SQS Duplicates, Ordering, and Parallelism

Standard queues provide at-least-once delivery, so account for duplicate messages. FIFO ordering applies within a `MessageGroupId`; different groups can run in parallel. Even with FIFO, a processed message can be received again if it was not deleted before visibility timeout expired. Do not assume that external effects, such as database changes, happen exactly once. [SQS standard delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html), [FIFO delivery logic](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html), [Visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)

The consumer count in 6.1.1 is one factor in parallelism. Throughput also depends on FIFO group count, task duration, processing resources, and downstream limits. Kafka replay is also limited to events still retained. [Kafka partitions, retention, and consumer groups](../platform-infrastructure/kafka.md)

### 6.2 SNS Subscribers Depend on Topic Type

“At the same time” in the source describes fan-out. It does not guarantee that all subscribers process a message at the same instant. Read the listed email, SMS, HTTP(S), and direct Lambda subscriptions as Standard Topic options. SNS FIFO Topics deliver to SQS Standard/FIFO Queues; connect Lambda through SQS. Subscribing a Standard Queue does not preserve all FIFO delivery guarantees. [SNS FIFO message delivery](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html)

### 6.3 Managed Kafka Still Has Application Responsibilities

MSK reduces broker infrastructure work. It does not design topics, partitions, retention, or producer/consumer behavior for you. The source broker/subnet diagram illustrates a Provisioned setup. Distinguish capacity management responsibilities for MSK Serverless and Provisioned. [MSK introduction](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html), [MSK Provisioned](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html)

### 6.4 KMS Permissions, Key Types, and Rotation

KMS evaluates key policies, IAM policies, grants, and other applicable controls. Do not assume an IAM Allow is sufficient. Check whether the key policy permits IAM-based authorization. AWS service integrations use symmetric encryption KMS keys for stored data. Asymmetric keys are public/private key pairs with different uses. [KMS key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html), [KMS asymmetric keys](https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html)

KMS key material rotation does not re-encrypt existing data or change database passwords. Keys with AWS_KMS origin retain older key material to decrypt existing ciphertext. Automatic rotation applies to symmetric encryption keys with material generated by AWS KMS. It does not apply to asymmetric keys in the same way. [KMS key rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)

### 6.5 Secrets Manager Envelope Encryption and Read Permissions

More precisely, the KMS key protects a data key, and Secrets Manager uses that data key to encrypt the secret value. This is envelope encryption. Reading a secret encrypted with a customer managed key requires `secretsmanager:GetSecretValue` and `kms:Decrypt` permission on that key. [Secret encryption](https://docs.aws.amazon.com/secretsmanager/latest/userguide/security-encryption.html), [GetSecretValue](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)

CloudTrail records `GetSecretValue` calls but omits the returned `SecretString` and `SecretBinary` values. Application logs must also exclude secret values. Rotating a secret password and rotating KMS key material are different operations. [GetSecretValue logging](https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html)

### 6.6 Configure CloudWatch Collection Separately

Creating EKS does not automatically collect every node memory metric, Pod log, and custom application metric. Configure collectors such as the CloudWatch agent, target metrics/logs, and permissions to send them. The source thresholds are learning examples, not validated Alarm evaluation periods or scaling policies. [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)

### 6.7 CloudTrail Recording Scope

Default Event history shows the last 90 days of management events in a Region. It does not automatically include all APIs or data events such as S3 object access. For ongoing retention and required data events, check the collection scope and retention settings of trails/event data stores separately. [CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)

## Related Topics

- [AWS study scope](index.md)
- [EKS](eks.md)
- [Storage and databases](storage-databases.md)
- [Kafka](../platform-infrastructure/kafka.md)
- [Platform security](../platform-infrastructure/platform-security.md)
