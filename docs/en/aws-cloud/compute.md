---
id: aws-cloud-compute
status: studied
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids:
  - AWSC-03-01
  - AWSC-03-02
  - AWSC-03-03
  - AWSC-03-04
  - AWSC-03-05
  - AWSC-03-06
---

# Chapter 3. Compute & Load Balancing

The latest compact source keeps its numbering, order, and examples. The unhealthy-target exclusion in 3.4 has a fail-open exception, and the Service diagrams in 3.6 differ from actual paths by target mode. Read the separate supplement below. This is not a record of AWS deployment or performance tests.

<!-- SOURCE CORE START -->

## 3.1 EC2

EC2 = Elastic Compute Cloud.

> An AWS virtual server

Common settings:
- AMI
- Instance Type
- VPC
- Subnet
- Security Group
- Storage
- IAM Role

### AMI
A VM image for creating EC2 instances.

```text
AMI = Full VM image
Docker Image = Container execution image
```

### Instance Type
Hardware specifications such as CPU / memory / GPU.

```text
t = General purpose / low cost
m = General Purpose
c = Compute Optimized
r = Memory Optimized
g / p = GPU
```

### EC2 and subnets
EC2 is created in a specific subnet, so selecting the subnet determines the AZ.

### User Data
An initialization script to run on the first boot.

### Public / Private EC2
Public EC2 can use an IGW/public IP, while private EC2 can access the outside through NAT.

### Elastic IP
Available when a fixed public IPv4 address is needed.

### IAM Role
Access AWS resources through an IAM role rather than storing an Access Key directly in code.

### EKS Node
EKS worker nodes are usually EC2 instances.

---

## 3.2 EBS and EC2

EBS = Elastic Block Store.

> Block storage attached to EC2

```text
EC2
 ↓
EBS
```

EC2 is compute; EBS is storage.

An EBS volume belongs to a specific AZ and attaches to EC2 in the same AZ.

---

## 3.3 Launch Template / Auto Scaling Group

### Launch Template
A blueprint for creating EC2 instances.

Examples of included settings:
- AMI
- Instance Type
- Security Group
- IAM Role
- Storage
- User Data

### ASG
Auto Scaling Group.

```text
Min 2
Desired 3
Max 10
```

```text
Scale Out = Add servers
Scale In = Remove servers
```

If the instance count falls below Desired, new EC2 instances can bring it back to the desired count.

Scaling methods:
- Metric-based
- Target Tracking
- Scheduled Scaling

Keeping the application stateless works well in an Auto Scaling environment.

```text
Persistent Data → RDS
Cache / Session → ElastiCache
Object → S3
```

---

## 3.4 ALB

ALB = Application Load Balancer.

> An L7 load balancer that understands HTTP/HTTPS

Roles:
- Distribute requests
- Health Check
- TLS Termination
- Host Routing
- Path Routing

Example:
```text
/api/* → api-service
/admin/* → admin-service
```

### Listener
Defines the protocol/port that receives requests.

### Target Group
A set of actual backend targets.

### Health Check
Traffic is not sent to unhealthy targets.

ALB can be internet-facing or internal.

---

## 3.5 NLB

NLB = Network Load Balancer.

> An L4 load balancer focused on TCP / UDP / TLS

```text
ALB = L7 / HTTP / HTTPS / Path / Host
NLB = L4 / TCP / UDP / TLS
```

Important:
> ALB is not defined as external-only, nor NLB as internal-only.

Both can be configured for external or internal use.

---

## 3.6 Kubernetes Service and ALB/NLB

A Kubernetes Service also has a protocol and port.

Example:
```yaml
ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

The main role of a Service:
> Group multiple Pod replicas behind a stable endpoint and distribute traffic at L4.

### Internal Pod communication
```text
Pod
 ↓
ClusterIP Service
 ↓
Pod Replicas
```

### External HTTP/HTTPS
```text
Internet
 ↓
ALB
 ↓
Service
 ↓
Pod Replicas
```

### TCP/UDP
```text
Client
 ↓
NLB
 ↓
Service
 ↓
Pod Replicas
```

Final summary:
```text
Service = Group Pod replicas behind a stable endpoint
ALB = L7 HTTP/HTTPS entry point
NLB = L4 TCP/UDP/TLS entry point
```

### ALB/NLB targets
Depending on the configuration:
```text
instance target → EC2 Node
ip target → Pod IP
```

ALB/NLB therefore does not always select only nodes.

---

<!-- SOURCE CORE END -->

## Separate supplement: conditions for use

Official documentation checked: 2026-10-04.

- **3.1:** The `t` family uses CPU credits for burstable performance. It is not always low-cost under every workload. User Data runs on the first boot by default; AMI and launch-agent settings can also enable repeated execution. [CPU credits](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html), [User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
- **3.3–3.4:** ALB health checks and ASG replacement are separate. Enable ELB health checks in the ASG for it to use those results in replacement decisions. [ASG health checks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html)
- **3.4:** The source statement that traffic is not sent to unhealthy targets has an exception. If all registered targets are unhealthy, ALB can **fail open** and send requests to those targets. [ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
- **3.6:** Service in the diagrams is a logical connection. With AWS Load Balancer Controller, instance targets use NodePort, while IP targets receive traffic directly at Pod IPs. Not every request passes through ClusterIP. Check the controller, Service type, CNI, and target type. The YAML shows only the ports section. [ALB target type](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/#target-type), [NLB target mode](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/nlb/)

Reading guide: separate EC2/EBS roles, ASG instance-count management, and ALB/NLB/Service request paths. See [Storage and databases](storage-databases.md) for persistent state choices.

## LLM in Practice

### Situation

A hypothetical case where ALB reports unhealthy targets but requests still arrive. Check the conditions in [3.4–3.6](#34-alb).

### Context to Give the LLM

Provide sanitized Service, target, and controller settings, health reasons, and request logs.

### Example Prompt

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 EKS에서 ALB target이 모두 unhealthy인데 일부 요청은 Pod에 도달한다.
    자료: [target type·Service YAML·health reason·요청 로그]. Controller/CNI 설정은 미확인이다.
    [요청]
    관측과 가정을 나누고 현재 요청 경로와 fail-open 가능성을 검토하라.
    [출력]
    가설 / 필요한 증거 / 다음 읽기 전용 확인 표를 작성하라.
    instance·ip target 경로와 Service port·targetPort를 구분하라.
    [검증]
    공식 문서와 실제 controller·target 설정·시간순 로그를 대조하라.
    원인을 단정하거나 리소스를 변경하지 말고 격리 검증안을 제시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    In hypothetical EKS, all ALB targets are unhealthy, but some requests still reach Pods.
    Material: [target type, Service YAML, health reasons, request logs]. Controller/CNI settings are unknown.
    [Task]
    Separate observations from assumptions; review the current request path and possible fail-open behavior.
    [Output]
    Create a table: hypothesis / required evidence / next read-only check.
    Distinguish instance and IP target paths, Service port, and targetPort.
    [Checks]
    Compare official docs with actual controller/target settings and time-ordered logs.
    Do not assume a cause or change resources; propose an isolated validation plan.
    ```

### Expected Output

A review table linking target-mode paths and the fail-open hypothesis to evidence.

### What the LLM Can Get Wrong

It may treat unhealthy as always blocked or assume every request passes through ClusterIP.

### How to Validate

Compare actual target registration, Service ports, health checks, and request logs. LLM output is a hypothesis. No AWS experiment was run for this page.
