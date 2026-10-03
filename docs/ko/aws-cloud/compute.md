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

제공된 원문의 번호·순서·도식·예시를 보존했다. 3.1의 User Data·인스턴스 계열, 3.2–3.3의 ASG 교체·ALB health check 조건은 뒤의 별도 보완에서 확인한다. 수치는 학습 예시이며 실제 AWS 실행 결과가 아니다.

<!-- SOURCE CORE START -->

## 3.1 EC2

EC2 = **Elastic Compute Cloud**

> AWS에서 빌려 쓰는 가상 서버

### EC2 구성 시 선택

- AMI
- Instance Type
- VPC
- Subnet
- Security Group
- Storage
- IAM Role

### AMI

Amazon Machine Image.

EC2 생성을 위한 서버 이미지.

```text
AMI
 ↓
EC2 생성
 ↓
운영체제가 설치된 서버
```

AMI와 Docker Image의 차이:

```text
AMI
= VM 전체 이미지

Docker Image
= Container 실행 이미지
```

### Instance Type

CPU, Memory, GPU 등의 서버 사양.

대표 계열:

```text
t = 범용/저비용
m = General Purpose
c = Compute Optimized
r = Memory Optimized
g / p = GPU
```

### EC2는 특정 Subnet에 배치

```text
VPC
└─ Subnet
   └─ EC2
```

Subnet 선택으로 AZ도 결정된다.

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

Private EC2의 외부 접속:

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

EC2 앞의 접근 제어.

### EBS

EC2 저장공간으로 보통 EBS를 사용.

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

고정 Access Key 저장을 피할 수 있다.

### User Data

EC2 최초 부팅 시 실행할 초기화 Script.

### Stop / Start / Terminate

- Stop = 전원 끄기
- Start = 다시 켜기
- Terminate = 인스턴스 제거

### Public IP / Elastic IP

Public IP는 변할 수 있다.

고정 Public IPv4가 필요하면 Elastic IP 사용 가능.

현대적인 웹 서비스에서는 EC2 Public IP에 직접 의존하기보다:

```text
DNS
 ↓
ALB
 ↓
EC2 여러 대
```

구조를 많이 사용한다.

### 단일 EC2 문제

Single Point of Failure.

Production에서는 여러 AZ에 여러 EC2를 두는 구성이 일반적.

### EKS Node와 EC2

Managed Node Group을 쓰면 EKS Worker Node의 실체가 EC2인 경우가 많다.

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

GPU EC2 위에 vLLM 등을 실행할 수 있다.

---

## 3.2 Auto Scaling

Auto Scaling:

> 트래픽이나 상태에 따라 EC2 개수를 자동으로 늘리거나 줄이는 기능

### Scale Out / Scale In

```text
Scale Out
= 서버 추가

Scale In
= 서버 제거
```

Horizontal Scaling.

Vertical Scaling은 서버 한 대의 사양을 키우는 것.

### Auto Scaling Group(ASG)

```text
Min     = 2
Desired = 3
Max     = 10
```

- Min = 최소 인스턴스 수
- Desired = 유지하려는 인스턴스 수
- Max = 최대 수

### Self Healing

Desired 3인데 한 대가 죽으면 새 EC2를 만들어 3대를 유지한다.

### Launch Template

EC2 생성 설계도.

```text
Launch Template
├─ AMI
├─ Instance Type
├─ Security Group
├─ IAM Role
├─ Storage
└─ User Data
```

### ALB와 결합

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

Scale Out된 인스턴스도 Target Group에 등록된다.

### Health Check

불량 인스턴스를 트래픽 대상에서 제외하거나 교체할 수 있다.

### Dynamic Scaling

CloudWatch Metric 기반.

예:

```text
CPU > 70%
→ EC2 증가
```

### Target Tracking

예:

```text
평균 CPU 50% 유지
```

목표에 맞게 자동 증감.

### Scheduled Scaling

정해진 시간에 증감.

### Multi-AZ

ASG를 여러 AZ에 걸쳐 구성해 장애 대응.

### EKS와 연결

EKS에서는 Node 수를 조절하기 위해:

- Managed Node Group
- Auto Scaling Group
- Cluster Autoscaler
- Karpenter

등이 연결될 수 있다.

### Stateless Application

Auto Scaling에서는 EC2가 언제든 생성/삭제되므로 애플리케이션은 Stateless가 유리하다.

```text
Application
= Stateless

State
= RDS / ElastiCache / S3
```

---

## 3.3 Load Balancer

Load Balancer:

> 들어오는 요청을 여러 Backend 서버로 분산

### 핵심 역할

1. 요청 분산
2. Health Check
3. 단일 진입점 제공

### ALB vs NLB

ALB:
- L7
- HTTP/HTTPS
- Path/Host 기반 Routing

NLB:
- L4
- TCP/UDP/TLS
- 고성능 네트워크

### Listener

어떤 Protocol/Port로 요청을 받을지 정의.

### Listener Rule

```text
/api/*   → API Target Group
/admin/* → Admin Target Group
그 외    → Web Target Group
```

### Target Group

Backend 서버 그룹.

### Auto Scaling 연동

새 EC2가 생기면 Target Group에 등록되어 ALB가 트래픽을 분산한다.

### HTTPS / ACM

ALB Listener에서 TLS Termination 가능.

### Public / Internal ALB

둘 다 존재 가능.

### 전체 Compute 구조

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

정리:

```text
EC2
= 실제 서버

ASG
= 서버 개수 관리

ALB
= 요청 분산

Target Group
= Backend 묶음

Listener
= 요청 받을 Port/Protocol
```

---

<!-- SOURCE CORE END -->

## 별도 보완: 배치·교체·요청 흐름의 조건

공식 문서 확인일: 2026-10-03. 아래는 원문을 수정하지 않고 적용 조건을 덧붙인 내용이다.

### 3.1 인스턴스 선택과 부팅

`t` 계열의 “저비용”은 모든 부하에서의 비용 보장이 아니다. Burstable 인스턴스는 CPU baseline과 credit을 사용하며 Standard/Unlimited 모드의 동작과 추가 요금을 확인해야 한다. [AWS Burstable performance instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html)

User Data의 최초 부팅 실행은 일반적인 기본 동작이다. 지원되는 AMI의 cloud-init·Windows launch agent와 설정에 따라 재부팅 시 반복 실행도 구성할 수 있다. 초기화 완료 전에 애플리케이션이 준비되었다고 가정하지 않는다. [AWS EC2 User Data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)

### 3.1 / 3.3 Public·Private와 실제 요청 경로

Public Subnet이라는 이름만으로 EC2가 인터넷에 노출되지는 않는다. 직접 IPv4 인터넷 통신에는 IGW 경로와 public IPv4 또는 Elastic IP가 필요하다. 원문의 NAT 흐름은 private EC2가 시작한 외부 통신을 설명하는 예시다. [AWS Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)

인터넷 공개 ALB 뒤의 EC2는 public IP 없이도 private IP로 요청을 받을 수 있다. 3.3의 전체 도식에서 ASG는 패킷이 통과하는 장치가 아니라 인스턴스 수를 관리하는 구성이다. 실제 요청은 ALB가 listener rule로 선택한 target group의 target으로 전달한다. [AWS ELB request routing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html)

### 3.2 / 3.3 등록·상태 확인·교체

새 인스턴스의 자동 target 등록은 ASG에 해당 load balancer/target group을 연결한 구성을 전제로 한다. ALB가 모든 EC2를 자동 발견하는 것은 아니다. [AWS Auto Scaling and ELB](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html)

ASG는 기본적으로 ELB health check 결과를 교체 판단에 사용하지 않는다. 이를 활성화했는지 확인해야 한다. ALB의 unhealthy 판정과 ASG의 인스턴스 교체는 별도 동작이다. [AWS Auto Scaling health checks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/health-checks-overview.html)

ALB에서 등록된 target이 모두 unhealthy이면 **fail-open**으로 해당 target들에 요청을 보낼 수 있다. 따라서 “health check 실패 = 항상 트래픽 차단”으로 해석하지 않는다. Target health reason, 검사 path·port·성공 코드와 실제 요청 오류를 함께 확인한다. [AWS ALB health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)

읽기 순서: 3.1에서 인스턴스의 위치와 부팅을 확인하고, 3.2에서 개수 관리, 3.3에서 요청 전달을 나누어 읽는다. `2/3/10`, `70%`, `50%`는 서로 다른 설정 예시이며 서비스의 적정 용량을 증명하지 않는다. 상태를 외부에 둘 때의 저장소 선택은 [Storage](storage.md)와 함께 본다.

## LLM in Practice

### 상황

가상의 ASG에서 EC2 3대는 실행 중이지만 ALB target 하나가 unhealthy다. [3.2–3.3의 개념](#32-auto-scaling)을 이용해 교체가 일어나지 않은 이유를 검토한다. 실제 장애 기록이 아니다.

### LLM에 제공할 맥락

비식별 ASG health check type·activity history, target group 연결 상태, target health reason, User Data 완료 여부와 애플리케이션 로그를 제공한다. 계정 ID·인증정보는 제공하지 않는다.

### 예시 프롬프트

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

### 기대 출력

ALB 상태 판정과 ASG 교체 동작을 구분하고, 각 가설을 확인하거나 기각할 증거를 연결한 표.

### LLM이 틀릴 수 있는 점

Unhealthy면 즉시 교체된다고 단정하거나 EC2가 running이면 애플리케이션도 준비되었다고 생각할 수 있다. Desired 값만 보고 실제 요청 용량이 충분하다고 결론낼 수도 있다.

### 검증 방법

실제 target group 연결·health check 설정·ASG activity와 부팅·애플리케이션 로그를 같은 시간대로 대조한다. LLM 출력은 가설이다. 이 페이지에서는 AWS 리소스를 생성하거나 장애·교체 실험을 실행하지 않았다.
