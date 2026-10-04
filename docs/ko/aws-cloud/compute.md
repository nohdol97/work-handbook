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

최신 compact 원문의 번호·순서·예시를 보존했다. 3.4의 unhealthy target 제외에는 fail-open 예외가 있고, 3.6의 Service 도식은 target 모드별 실제 경로와 구분한다. 뒤의 별도 보완을 함께 읽는다. 실제 AWS 배포·성능 시험 기록이 아니다.

<!-- SOURCE CORE START -->

## 3.1 EC2

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

---

<!-- SOURCE CORE END -->

## 별도 보완: 실제 적용 조건

공식 문서 확인일: 2026-10-04.

- **3.1:** `t` 계열은 CPU credit을 사용하는 burstable 인스턴스이므로 모든 부하에서 저비용을 보장하지 않는다. User Data의 최초 부팅 실행은 기본 동작이며 AMI·launch agent 설정으로 반복 실행도 가능하다. [CPU credit](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html), [User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
- **3.3–3.4:** ALB 상태 확인과 ASG 교체는 별도다. ASG가 ELB health check 결과를 교체 판단에 쓰려면 해당 검사를 활성화해야 한다. [ASG health checks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html)
- **3.4:** 원문의 “Unhealthy Target에는 트래픽을 보내지 않는다”에는 예외가 있다. 등록된 target들이 모두 unhealthy이면 ALB는 **fail-open**으로 해당 target들에 요청을 보낼 수 있다. [ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
- **3.6:** 도식의 Service는 논리적 연결이다. AWS Load Balancer Controller의 instance target은 NodePort를 경유하고 ip target은 Pod IP로 직접 전달하므로, 모든 요청이 ClusterIP를 경유하는 것은 아니다. 실제 controller·Service type·CNI·target type 조건을 확인한다. YAML은 ports 부분만 보여주는 예시다. [ALB target type](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/ingress/annotations/#target-type), [NLB target mode](https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/nlb/)

읽기 순서: EC2·EBS의 역할, ASG의 개수 관리, ALB/NLB와 Service의 요청 경로를 나누어 읽는다. 영속 상태의 선택은 [스토리지·DB](storage-databases.md)를 참고한다.

## LLM in Practice

### 상황

ALB의 unhealthy 상태와 실제 요청 도달이 달라 보이는 가상 사례다. [3.4–3.6](#34-alb)의 조건을 점검한다.

### LLM에 제공할 맥락

비식별 Service·target·controller 설정과 health reason·요청 로그를 제공한다.

### 예시 프롬프트

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

### 기대 출력

Target 모드별 경로와 fail-open 가설을 증거에 연결한 검토표.

### LLM이 틀릴 수 있는 점

Unhealthy를 항상 차단으로 해석하거나 모든 요청이 ClusterIP를 지난다고 가정할 수 있다.

### 검증 방법

실제 target 등록과 Service port, health check·요청 로그를 대조한다. LLM 출력은 가설이며 이 페이지에서는 AWS 실험을 실행하지 않았다.
