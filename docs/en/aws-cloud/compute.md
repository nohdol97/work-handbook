---
id: aws-cloud-compute
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-03-01
  - AWS-03-02
  - AWS-03-03
---

# Chapter 3. Compute

The supplied section numbers, order, diagrams, and examples are preserved. See the separate supplement for User Data and instance-family details in 3.1 and ASG replacement and ALB health-check conditions in 3.2–3.3. Numbers are study examples, not results from running AWS resources.

<!-- SOURCE CORE START -->

## 3.1 EC2

EC2 = **Elastic Compute Cloud**

> A virtual server rented from AWS

### Choices when configuring EC2

- AMI
- Instance Type
- VPC
- Subnet
- Security Group
- Storage
- IAM Role

### AMI

Amazon Machine Image.

A server image used to create an EC2 instance.

```text
AMI
 ↓
Create EC2
 ↓
A server with an operating system installed
```

The difference between an AMI and a Docker Image:

```text
AMI
= An image of a full VM

Docker Image
= An image for running a container
```

### Instance Type

Server specifications such as CPU, memory, and GPU.

Common families:

```text
t = General purpose / low cost
m = General Purpose
c = Compute Optimized
r = Memory Optimized
g / p = GPU
```

### EC2 is placed in a specific subnet

```text
VPC
└─ Subnet
   └─ EC2
```

Selecting a subnet also determines the AZ.

### Public EC2 / Private EC2

Public:

```text
Internet
 ↓
IGW
 ↓
Public Subnet
 ↓
EC2
```

Private:

```text
Private Subnet
└─ EC2
```

Outbound internet access from private EC2:

```text
EC2
 ↓
NAT Gateway
 ↓
IGW
 ↓
Internet
```

### Security Group

Access control in front of EC2.

### EBS

EC2 commonly uses EBS for storage.

```text
EC2
 ↓
EBS Volume
```

### IAM Role

```text
EC2
 ↓
IAM Role
 ↓
S3
```

This avoids storing a fixed Access Key.

### User Data

An initialization script run when EC2 first boots.

### Stop / Start / Terminate

- Stop = Power off
- Start = Power on again
- Terminate = Remove the instance

### Public IP / Elastic IP

A public IP can change.

An Elastic IP can provide a fixed public IPv4 address.

Modern web services often use this structure instead of depending directly on an EC2 public IP:

```text
DNS
 ↓
ALB
 ↓
Multiple EC2 instances
```

This is a common setup.

### The problem with a single EC2 instance

Single Point of Failure.

Production commonly uses multiple EC2 instances across multiple AZs.

### EKS nodes and EC2

With a Managed Node Group, EKS worker nodes are often EC2 instances.

```text
EKS Cluster
   ↓
Node Group
   ↓
EC2
   ↓
Pod
```

### AI/GPU

You can run vLLM and similar software on GPU EC2 instances.

---

## 3.2 Auto Scaling

Auto Scaling:

> Automatically increases or decreases the number of EC2 instances based on traffic or health

### Scale Out / Scale In

```text
Scale Out
= Add servers

Scale In
= Remove servers
```

Horizontal Scaling.

Vertical Scaling increases the specifications of a single server.

### Auto Scaling Group (ASG)

```text
Min     = 2
Desired = 3
Max     = 10
```

- Min = Minimum number of instances
- Desired = Number of instances to maintain
- Max = Maximum number

### Self Healing

If Desired is 3 and one instance fails, a new EC2 instance is created to maintain 3 instances.

### Launch Template

A blueprint for creating EC2 instances.

```text
Launch Template
├─ AMI
├─ Instance Type
├─ Security Group
├─ IAM Role
├─ Storage
└─ User Data
```

### Combining with ALB

```text
ALB
 ↓
Target Group
 ↓
ASG
├─ EC2 A
├─ EC2 B
└─ EC2 C
```

Instances added through scale out are also registered with the Target Group.

### Health Check

Unhealthy instances can be excluded from traffic or replaced.

### Dynamic Scaling

Based on CloudWatch metrics.

Example:

```text
CPU > 70%
→ Add EC2 instances
```

### Target Tracking

Example:

```text
Maintain average CPU at 50%
```

Automatically scales up or down to meet the target.

### Scheduled Scaling

Scales up or down at scheduled times.

### Multi-AZ

Configure an ASG across multiple AZs to handle failures.

### Connection to EKS

To adjust the number of nodes, EKS can use:

- Managed Node Group
- Auto Scaling Group
- Cluster Autoscaler
- Karpenter

These components may be involved.

### Stateless Application

A stateless application works well with Auto Scaling because EC2 instances can be created or deleted at any time.

```text
Application
= Stateless

State
= RDS / ElastiCache / S3
```

---

## 3.3 Load Balancer

Load Balancer:

> Distributes incoming requests across multiple backend servers

### Main roles

1. Distribute requests
2. Health Check
3. Provide a single entry point

### ALB vs NLB

ALB:
- L7
- HTTP/HTTPS
- Path/Host-based routing

NLB:
- L4
- TCP/UDP/TLS
- High-performance networking

### Listener

Defines the protocol and port that receive requests.

### Listener Rule

```text
/api/*   → API Target Group
/admin/* → Admin Target Group
Other    → Web Target Group
```

### Target Group

A group of backend servers.

### Auto Scaling integration

When a new EC2 instance is created, it is registered with the Target Group so ALB can distribute traffic to it.

### HTTPS / ACM

TLS termination can take place at an ALB listener.

### Public / Internal ALB

Both types are available.

### Overall compute structure

```text
Internet
   ↓
  IGW
   ↓
  ALB
   ↓
Target Group
   ↓
Auto Scaling Group
├─ EC2 - AZ A
├─ EC2 - AZ A
├─ EC2 - AZ B
└─ EC2 - AZ B
```

Summary:

```text
EC2
= The actual server

ASG
= Manages the server count

ALB
= Distributes requests

Target Group
= A set of backends

Listener
= The port/protocol that receives requests
```

---

<!-- SOURCE CORE END -->

## Separate supplement: placement, replacement, and request flow

Official documentation checked: 2026-10-03. These conditions supplement the source without changing it.

### 3.1 Instance selection and boot

“Low cost” for the `t` family does not guarantee low cost for every workload. Burstable instances use a CPU baseline and credits. Check Standard/Unlimited mode behavior and additional charges. [AWS Burstable performance instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html)

Running User Data on the first boot is the usual default. Depending on the supported AMI's cloud-init or Windows launch agent and its settings, it can also run on later boots. Do not assume the application is ready before initialization finishes. [AWS EC2 User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

### 3.1 / 3.3 Public/private placement and the actual request path

A public subnet name alone does not expose EC2 to the internet. Direct IPv4 internet communication needs an IGW route and a public IPv4 or Elastic IP address. The source's NAT flow illustrates outbound communication initiated by private EC2. [AWS Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)

EC2 behind an internet-facing ALB can receive requests through its private IP without a public IP. In the overall diagram in 3.3, the ASG manages the instance count; it is not a device that packets pass through. ALB sends the request to a target in the target group selected by the listener rule. [AWS ELB request routing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html)

### 3.2 / 3.3 Registration, health checks, and replacement

Automatic target registration for new instances requires the relevant load balancer/target group to be attached to the ASG. ALB does not automatically discover every EC2 instance. [AWS Auto Scaling and ELB](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html)

By default, an ASG does not use ELB health check results for replacement decisions. Check whether this is enabled. ALB marking a target unhealthy and ASG replacing an instance are separate actions. [AWS Auto Scaling health checks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html)

If all registered ALB targets are unhealthy, **fail-open** behavior can send requests to those targets. A failed health check does not always block traffic. Check target health reasons, the health check path, port, and success codes, alongside actual request errors. [AWS ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

Reading guide: use 3.1 for instance placement and boot, 3.2 for instance-count management, and 3.3 for request delivery. `2/3/10`, `70%`, and `50%` are separate configuration examples. They do not prove that a service has enough capacity. See [Storage](storage.md) when choosing where to keep external state.

## LLM in Practice

### Situation

In a hypothetical ASG, 3 EC2 instances are running, but one ALB target is unhealthy. Use [the concepts in 3.2–3.3](#32-auto-scaling) to review why it has not been replaced. This is not an actual incident record.

### Context to Give the LLM

Provide sanitized ASG health check types and activity history, target group attachment state, target health reasons, User Data completion status, and application logs. Do not provide account IDs or credentials.

### Example Prompt

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 ASG: Min=2, Desired=3, Max=10, 실행 중 EC2는 3대다.
    ALB target 1개는 unhealthy이고 아직 교체되지 않았다. 원인은 미확인이다.
    자료: [target health reason·ASG health check type·activity·연결 상태·부팅 로그].
    [요청]
    관측과 가정을 분리하고 ALB의 요청 제외와 ASG의 교체 판단을 설명하라.
    기존 구성을 먼저 평가하고 원인별 필요한 증거를 제시하라.
    [출력]
    가설 / 지지·반박 증거 / 다음 읽기 전용 확인 / 판단 조건 표를 작성하라.
    초기화 실패, health check 설정, ASG 연결·교체 설정의 차이를 포함하라.
    [검증]
    공식 AWS 문서와 실제 설정·시간순 로그를 대조하고 미확인은 미확인으로 남겨라.
    모든 target이 unhealthy일 때 fail-open 가능성을 검토하라.
    인스턴스 종료나 health check 변경은 실행하지 말고 격리 검증안을 제시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Hypothetical ASG: Min=2, Desired=3, Max=10; 3 EC2 instances are running.
    One ALB target is unhealthy and has not been replaced. The cause is unknown.
    Material: [target health reason, ASG health check type, activities, attachment state, boot logs].
    [Task]
    Separate observations from assumptions; explain ALB traffic exclusion and ASG replacement decisions.
    Assess the existing setup first and identify the evidence needed for each possible cause.
    [Output]
    Create a table: hypothesis / supporting or conflicting evidence / next read-only check / decision conditions.
    Include initialization failures, health check settings, and ASG attachment and replacement settings.
    [Checks]
    Compare official AWS docs with actual settings and time-ordered logs; keep unknowns explicit.
    Consider fail-open behavior if all targets become unhealthy.
    Do not terminate instances or change health checks; propose an isolated validation plan.
    ```

### Expected Output

A table that separates ALB health decisions from ASG replacement behavior and links each hypothesis to evidence that would support or reject it.

### What the LLM Can Get Wrong

It may assume an unhealthy instance is replaced immediately or that a running EC2 instance means the application is ready. It may also infer enough request capacity from the Desired value alone.

### How to Validate

Compare the actual target group attachment, health check settings, ASG activities, boot logs, and application logs over the same time window. LLM output is a hypothesis. This page did not create AWS resources or run failure or replacement experiments.
