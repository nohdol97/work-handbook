---
id: aws-cloud-compute
status: studied
last_updated: 2026-10-18
last_reviewed: 2026-10-18
knowledge_ids:
  - AWSC-03-01
  - AWSC-03-02
  - AWSC-03-03
  - AWSC-03-04
  - AWSC-03-05
  - AWSC-03-06
---

# Chapter 3. Compute & Load Balancing

예시 구성은 학습용이며 실제 AWS 환경에서 실행한 결과가 아니다.

<!-- SOURCE CORE START -->

## 3.1 EC2

EC2는 작업을 실행하는 서버이고 로드 밸런서는 손님을 적절한 창구로 안내하는 접수대와 비슷하다. 서버 수를 늘리는 일과 요청을 어디로 보내는 일은 따로 확인한다.

EC2 = Elastic Compute Cloud.

> AWS의 가상 서버

대표 설정:
- AMI
- Instance Type
- VPC
- Subnet
- Security Group
- Storage
- IAM Role

### AMI
EC2 생성용 VM 이미지.

```text
AMI = VM 전체 이미지
Docker Image = Container 실행 이미지
```

### Instance Type
CPU / Memory / GPU 등의 하드웨어 사양.

```text
t = 범용 / 저비용
m = General Purpose
c = Compute Optimized
r = Memory Optimized
g / p = GPU
```

### EC2와 Subnet
EC2는 특정 Subnet에 생성되며 Subnet 선택으로 AZ가 결정된다.

### User Data
최초 부팅 시 실행할 초기화 Script.

### Public / Private EC2
Public EC2는 IGW/Public IP와 연결될 수 있고, Private EC2는 NAT를 통해 외부로 나갈 수 있다.

### Elastic IP
고정 Public IPv4가 필요한 경우 사용 가능.

### IAM Role
Access Key를 코드에 직접 저장하기보다 IAM Role을 통해 AWS Resource에 접근한다.

### EKS Node
EKS Worker Node의 실체는 보통 EC2다.


`t` 계열은 CPU credit을 사용하는 burstable 인스턴스이므로 모든 부하에서 저비용을 보장하지 않는다. User Data의 최초 부팅 실행은 기본 동작이며 AMI·launch agent 설정으로 반복 실행도 가능하다. [CPU credit](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html), [User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

---

## 3.2 EBS와 EC2

EBS = Elastic Block Store.

> EC2에 붙이는 Block Storage

```text
EC2
 ↓
EBS
```

EC2는 Compute, EBS는 Storage다.

EBS는 특정 AZ에 속하므로 EC2와 같은 AZ에서 Attach한다.

---

## 3.3 Launch Template / Auto Scaling Group

### Launch Template
EC2 생성 설계도.

포함 예:
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
Scale Out = 서버 추가
Scale In = 서버 제거
```

Desired보다 인스턴스가 줄면 새 EC2를 만들어 수를 맞출 수 있다.

Scaling 방식:
- Metric 기반
- Target Tracking
- Scheduled Scaling

Auto Scaling 환경에서는 Application을 Stateless하게 두는 것이 유리하다.

```text
Persistent Data → RDS
Cache / Session → ElastiCache
Object → S3
```


ALB 상태 확인과 ASG 교체는 별도다. ASG가 ELB health check 결과를 교체 판단에 쓰려면 해당 검사를 활성화해야 한다. [ASG health checks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html)

---

## 3.4 ALB

ALB = Application Load Balancer.

> HTTP/HTTPS를 이해하는 L7 Load Balancer

역할:
- 요청 분산
- Health Check
- TLS Termination
- Host Routing
- Path Routing

예:
```text
/api/* → api-service
/admin/* → admin-service
```

### Listener
어떤 Protocol/Port로 요청을 받을지 정의.

### Target Group
실제 Backend Target 묶음.

### Health Check
Unhealthy Target에는 트래픽을 보내지 않는다.

ALB는 Internet-facing 또는 Internal로 사용할 수 있다.


원문의 “Unhealthy Target에는 트래픽을 보내지 않는다”에는 예외가 있다. 등록된 target들이 모두 unhealthy이면 ALB는 **fail-open**으로 해당 target들에 요청을 보낼 수 있다. [ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

---

## 3.5 NLB

NLB = Network Load Balancer.

> TCP / UDP / TLS 중심의 L4 Load Balancer

```text
ALB = L7 / HTTP / HTTPS / Path / Host
NLB = L4 / TCP / UDP / TLS
```

중요:
> ALB = 외부용, NLB = 내부용으로 구분하는 것이 아니다.

둘 다 외부/내부 구성 가능하다.

---

## 3.6 Kubernetes Service와 ALB/NLB

Kubernetes Service도 Protocol과 Port를 가진다.

예:
```yaml
ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
```

Service의 핵심 역할:
> 여러 Pod Replica를 하나의 안정적인 Endpoint로 묶고 L4 수준에서 분산한다.

### 내부 Pod 통신
```text
Pod
 ↓
ClusterIP Service
 ↓
Pod Replicas
```

### 외부 HTTP/HTTPS
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

최종 정리:
```text
Service = Pod Replica를 안정적인 Endpoint로 묶음
ALB = L7 HTTP/HTTPS 진입점
NLB = L4 TCP/UDP/TLS 진입점
```

### ALB/NLB Target
구성에 따라:
```text
instance target → EC2 Node
ip target → Pod IP
```

즉 ALB/NLB가 항상 Node만 선택하는 것은 아니다.


도식의 Service는 논리적 연결이다. AWS Load Balancer Controller의 instance target은 NodePort를 경유하고 ip target은 Pod IP로 직접 전달하므로, 모든 요청이 ClusterIP를 경유하는 것은 아니다. 실제 controller·Service type·CNI·target type 조건을 확인한다. YAML은 ports 부분만 보여주는 예시다. [ALB target type](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/#target-type), [NLB target mode](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/nlb/)

---

<!-- SOURCE CORE END -->

## 핵심 정리

EC2와 로드 밸런서는 실행과 트래픽 분산을 맡는다. 연결 경로와 장애 범위를 확인해 실제 서비스에 맞게 선택한다.

영속 상태를 어디에 둘지는 [스토리지·DB](storage-databases.md)에서 이어서 살펴본다.

## LLM in Practice

**프롬프트:**

=== "한국어"

    ```text {.prompt}
    ALB target이 unhealthy인데 요청이 일부 도달하고 있어. target type, Service port, health check와 요청 로그를 보고 실제 경로와 fail-open 가능성을 설명해 줘. ALB 상태와 ASG 교체 판단은 구분하고 설정은 변경하지 마.
    ```

=== "English"

    ```text {.prompt}
    ALB targets are unhealthy, yet some requests still arrive. Use the target type, Service ports, health checks, and request logs to explain the actual path and possible fail-open behavior. Keep ALB health separate from ASG replacement decisions, and do not change settings.
    ```

**핵심 사항:** 실제 target type·Service port를 따른 요청 경로, fail-open/health check 가설과 최소 설정 변경 검토 의견. unhealthy를 항상 차단으로 보거나 모든 요청이 ClusterIP·controller를 통과한다고 가정할 수 있다. target 등록·health reason·요청 로그 시각이 경로 설명과 맞는지 확인한다. instance와 ip 모드를 섞거나 ALB health를 ASG 자동 교체로 간주한 결론은 다시 검토한다. 관련: [3.4–3.6](#34-alb)
