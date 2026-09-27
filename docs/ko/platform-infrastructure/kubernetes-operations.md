---
id: platform-infrastructure-kubernetes-operations
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - PIS-03-01
  - PIS-03-02
  - PIS-03-03
  - PIS-03-04
  - PIS-03-05
  - PIS-03-06
  - PIS-03-07
  - PIS-03-08
  - PIS-03-09
  - PIS-03-10
---

# Chapter 3. Kubernetes Production Operations

Basic Chapter 3의 개념 학습 기록이다. 실제 클러스터 운영, 장애 훈련, 업그레이드나 명령 실행을 완료했다는 뜻은 아니다. 목표는 Pod 실행에 더해 서버 장애, 트래픽 증가, Node 교체, 업그레이드에서도 서비스를 유지하는 방법을 이해하는 것이다. 선행 내용은 [Kubernetes 핵심](kubernetes-core.md)과 [Linux·컨테이너](linux-containers.md), 전체 범위는 [플랫폼 인프라 학습 안내](index.md)에서 확인한다.

이 페이지의 명령은 실행하지 않은 학습 예제다. 조회 명령도 허가된 환경에서 사용하며, `cordon`, `drain`, 복구·교체는 운영 상태를 바꾼다. 예제 게시는 실제 변경·삭제·복구 실행에 대한 승인이 아니다.


아래 원문 본문은 제공된 학습 자료의 표현과 순서를 그대로 보존했다. 단순화되거나 조건이 빠진 설명은 본문 뒤 **원문 절별 보완과 정정**에서 확인한다. 특히 3.2의 quorum·복구 범위, 3.7의 PDB, 3.8의 drain, 3.10의 Pending·OOM 설명을 실제 적용하기 전에 해당 보완을 함께 읽는다.

**본문 안내:** 아래 원문 구역은 원래 순서와 형태를 보존한 본문이다. 원문의 단순화된 설명에 대한 정정·적용 조건과 추가 설명은 문서 뒤 보완 구역에서 해당 절 번호와 함께 확인한다.

<!-- SOURCE CORE START -->

## 3.1 Cluster Design

Production Kubernetes의 핵심은:

> 서버 한 대가 죽어도 서비스가 계속 살아 있어야 한다

### Control Plane HA

Control Plane이 하나면 Single Point of Failure가 될 수 있다.

Production에서는 여러 Control Plane으로 구성해 HA를 만든다.

관리형 Kubernetes(EKS 등)는 이 부분을 Cloud Provider가 관리해준다.

### Worker Node도 여러 개

```text
Node A → API Pod
Node B → API Pod
Node C → API Pod
```

한 Node가 죽어도 다른 Node의 Pod가 계속 요청을 처리해야 한다.

### Node Pool

용도별 Node 그룹.

예:

```text
General Node Pool
→ 일반 Backend

GPU Node Pool
→ vLLM

Batch Node Pool
→ Batch Job
```

### Failure Domain

한 곳에 모든 Pod를 몰아두지 않는다.

```text
Pod 1 → Node A
Pod 2 → Node B
Pod 3 → Node C
```

### Availability Zone

Cloud에서는 AZ 단위 장애도 고려한다.

```text
AZ-A
├─ Node 1
└─ Pod A

AZ-B
├─ Node 2
└─ Pod B
```

### 플랫폼 설계 예

```text
Kubernetes Cluster

AZ-A
├─ General Node
└─ GPU Node

AZ-B
├─ General Node
└─ GPU Node
```

### 핵심 정리

```text
Control Plane
→ HA 필요

Worker Node
→ 여러 개 운영

Node Pool
→ 용도별 Node 그룹

Failure Domain
→ 장애가 한 곳에 몰리지 않게 분리

Availability Zone
→ Zone 장애까지 고려
```

---

## 3.2 etcd Operations

etcd는 Kubernetes의 **Cluster 상태 저장소**다.

> etcd = Kubernetes의 기억장치

### 저장되는 것

```text
Pod 정보
Deployment 정보
Service 정보
ConfigMap / Secret
Cluster 설정
```

### 중요성

etcd가 망가지면 새 Pod 생성, Deployment 변경, Service 변경 같은 Cluster 관리 작업에 문제가 생길 수 있다.

### Quorum

etcd는 보통 여러 멤버로 구성한다.

예:

```text
etcd 1
etcd 2
etcd 3
```

3개면 2개 이상이 살아 있어야 한다.

> Quorum = 합의를 유지하기 위한 최소 과반수

### 홀수 개 구성

대표적으로 3개, 5개 같은 홀수 개로 구성한다.

### Backup / Restore

```text
정상 Cluster
↓
etcd snapshot 생성
↓
장애 발생
↓
snapshot으로 restore
```

### Managed Kubernetes

EKS 같은 관리형 Kubernetes에서는 etcd와 Control Plane 운영을 Cloud Provider가 관리한다.

### 핵심 정리

```text
etcd
= Kubernetes Cluster 상태 저장소

API Server가 etcd와 통신

Production에서는
→ 여러 etcd 멤버로 HA 구성

Quorum
= 과반수 멤버가 살아 있어야 함

etcd backup
= Cluster 상태 복구를 위해 중요
```

---

## 3.3 CNI

CNI = **Container Network Interface**

> Kubernetes에서 Pod에 IP를 주고, Pod끼리 통신할 수 있게 만드는 네트워크 계층

### 역할

```text
Pod 생성
↓
IP 할당
↓
다른 Pod와 통신
```

### 대표 CNI

```text
Calico
Cilium
```

둘 다 Pod Networking과 Network Policy를 지원한다.

### Calico

대표적인 Kubernetes CNI.

주요 역할:

```text
Pod 네트워크
Routing
NetworkPolicy
```

### Cilium

eBPF를 적극 사용하는 CNI.

```text
Cilium
→ eBPF 기반 네트워크 처리
→ NetworkPolicy
→ Observability 기능도 강함
```

### Overlay vs Routed Network

**Overlay**

```text
Pod
↓
Overlay Network
↓
Host Network
```

가상 네트워크 계층을 한 겹 추가.

**Routed**

```text
Pod IP
↓
Routing
↓
다른 Node의 Pod
```

Routing으로 직접 연결.

### eBPF

Linux Kernel 안에서 네트워크 처리나 관찰을 효율적으로 할 수 있게 해주는 기술.

Cilium은 이를 이용해 Networking, Security, Observability를 구현한다.

### 핵심 정리

```text
CNI
= Pod 네트워크 구현

Calico
= 대표적인 Kubernetes CNI

Cilium
= eBPF 기반 CNI

Overlay
= 가상 네트워크 계층 추가

Routed
= Routing으로 직접 연결
```

---

## 3.4 CSI

CSI = **Container Storage Interface**

> Kubernetes가 다양한 Storage 시스템을 연결하기 위한 표준 인터페이스

### 왜 필요한가

Storage마다 연결 방식이 다르다.

예:

```text
AWS EBS
NFS
Ceph
Google Persistent Disk
Azure Disk
```

Kubernetes는 Storage가 필요하다는 요청만 하고 실제 처리는 CSI Driver가 담당한다.

### 기본 구조

```text
Pod
 ↓
PVC
 ↓
StorageClass
 ↓
CSI Driver
 ↓
실제 Storage
```

AWS 예:

```text
Pod
↓
PVC
↓
EBS CSI Driver
↓
AWS EBS Volume
```

### CSI Driver

Kubernetes와 실제 Storage 사이 연결 역할.

예:

```text
EBS CSI Driver
EFS CSI Driver
Ceph CSI
```

### Volume Attachment

Pod가 특정 Node에서 실행되면 Storage도 그 Node에 연결돼야 할 수 있다.

```text
Pod
→ Node A에 Scheduling
→ EBS Volume을 Node A에 Attach
→ Container에 Mount
```

### Storage 장애

Pod가 `Pending`, `ContainerCreating`에 오래 머무르면:

```text
CSI Driver 문제
Storage 자체 장애
권한 문제
Zone 불일치
Volume attach 실패
```

등을 확인한다.

특히 Cloud Disk는 AZ에 묶일 수 있다.

```text
Volume = AZ-A
Pod = AZ-B Node
→ Attach 불가 가능
```

### 핵심 정리

```text
CSI
= Kubernetes와 Storage를 연결하는 표준

CSI Driver
= 실제 Storage 시스템과 통신

흐름:
Pod
→ PVC
→ StorageClass
→ CSI Driver
→ 실제 Storage
```

---

## 3.5 CoreDNS

CoreDNS는 Kubernetes 내부 DNS 서버다.

> Service 이름을 IP로 바꿔주는 역할

### 기본 흐름

```text
API Pod
↓
redis 라는 이름으로 요청
↓
CoreDNS
↓
Redis Service IP 반환
↓
Redis Service
↓
Redis Pod
```

### Kubernetes DNS 이름

같은 Namespace 안에서는 Service 이름만으로 접근할 수 있다.

예:

```text
redis
postgres
my-api
```

다른 Namespace라면 더 긴 이름을 사용할 수 있다.

예:

```text
redis.cache
```

### CoreDNS 장애

Service가 살아 있어도 이름으로 접근이 안 될 수 있다.

예:

```text
Pod → postgres
```

실패하지만 IP 직접 접근은 성공한다면 DNS 문제 가능성이 있다.

### DNS Troubleshooting

```bash
nslookup postgres
dig postgres
kubectl get pods -n kube-system
```

### DNS Scaling

Pod 수와 DNS 요청이 많아지면 CoreDNS도 부하를 받을 수 있다.

Production에서는 CoreDNS replica 수와 resource 설정도 중요할 수 있다.

### 핵심 정리

```text
CoreDNS
= Kubernetes 내부 DNS

Service 이름
→ CoreDNS
→ Service IP

DNS 장애가 나면
서비스 이름으로 접근 실패 가능
```

---

## 3.6 Autoscaling

핵심:

```text
HPA
VPA
Cluster Autoscaler
KEDA
```

### HPA

Horizontal Pod Autoscaler.

> Pod 개수를 늘리고 줄인다.

예:

```text
API Pod 3개
↓
CPU 사용률 증가
↓
HPA
↓
API Pod 6개
```

대표 기준:

```text
CPU
Memory
Custom Metric
```

### VPA

Vertical Pod Autoscaler.

> Pod 하나가 요청하는 CPU/Memory 크기를 조정

```text
현재
CPU request = 500m
Memory request = 1Gi

↓ VPA

CPU request = 1
Memory request = 2Gi
```

### Cluster Autoscaler

Node 수를 조절한다.

```text
HPA
↓
Pod 10개 필요
↓
Node 공간 부족
↓
Pod Pending
↓
Cluster Autoscaler
↓
Node 증가
```

### HPA + Cluster Autoscaler

```text
트래픽 증가
↓
HPA
↓
Pod 증가
↓
Node 자원 부족
↓
Cluster Autoscaler
↓
Node 증가
↓
새 Pod 배치
```

### KEDA

이벤트 기반 Autoscaling.

예:

```text
Kafka lag 증가
↓
KEDA
↓
Consumer Pod 증가
```

또는 Queue message 수 기반.

### Scaling은 즉시 되지 않는다

```text
트래픽 급증
↓
HPA 감지
↓
새 Pod 생성
↓
Image Pull
↓
App 시작
↓
Readiness 성공
↓
트래픽 처리
```

vLLM은 Model Loading 시간도 추가될 수 있다.

### 핵심 정리

```text
HPA
= Pod 개수 자동 조절

VPA
= Pod CPU / Memory 크기 조절

Cluster Autoscaler
= Node 개수 자동 조절

KEDA
= Queue / Kafka lag 같은 이벤트 기반 scaling
```

---

## 3.7 Reliability

Reliability는 장애나 배포 중에도 서비스를 최대한 유지하는 것이다.

핵심:

```text
PDB
Anti-Affinity
Topology Spread
Graceful Termination
```

### PodDisruptionBudget

유지보수 상황에서 최소 몇 개의 Pod가 살아 있어야 하는지 정하는 규칙.

예:

```text
minAvailable = 2
```

Node drain 중에도 최소 2개를 유지하려고 한다.

### Anti-Affinity

같은 서비스 Pod를 서로 다른 Node에 분산.

```text
Node A → API Pod 1
Node B → API Pod 2
Node C → API Pod 3
```

### Topology Spread

Pod를 Node 또는 AZ에 골고루 분산.

```text
AZ-A → 2개
AZ-B → 2개
AZ-C → 2개
```

### Graceful Termination

Pod를 종료할 때 바로 죽이지 않고 기존 요청을 정리할 시간을 준다.

```text
Pod 종료 시작
↓
새 트래픽 차단
↓
SIGTERM
↓
기존 요청 처리
↓
정상 종료
```

### Reliability 조합

```text
Replica 여러 개
+
Anti-Affinity / Topology Spread
+
PDB
+
Readiness Probe
+
Graceful Shutdown
```

### 핵심 정리

```text
PDB
= 동시에 너무 많은 Pod가 내려가지 않게 보호

Anti-Affinity
= 같은 Pod를 서로 다른 Node에 분산

Topology Spread
= Node / AZ에 골고루 분산

Graceful Termination
= 요청을 정리하고 안전하게 종료
```

---

## 3.8 Node Operations

핵심:

```text
Cordon
Drain
Node Pressure
Replacement
```

### Cordon

> 이 Node에 새 Pod를 더 이상 배치하지 마

```bash
kubectl cordon node-a
```

기존 Pod는 유지되고 신규 Scheduling만 막힌다.

### Drain

> Node에서 Pod를 안전하게 비우는 작업

```bash
kubectl drain node-a
```

```text
Node A
↓
새 Pod 배치 중단
↓
기존 Pod들을 다른 Node로 이동
↓
Node 비움
```

### Cordon vs Drain

```text
Cordon
= 새 Pod만 못 들어옴

Drain
= 기존 Pod도 빼냄
```

### Node Pressure

대표:

```text
MemoryPressure
DiskPressure
PIDPressure
```

#### MemoryPressure

메모리 부족. Pod eviction 가능.

#### DiskPressure

디스크 부족.

원인 예:

```text
Container image 너무 많음
로그 과다
ephemeral storage 부족
```

#### PIDPressure

프로세스 수가 너무 많을 때.

### Eviction

Node 자원이 부족하면 일부 Pod를 제거해 Node를 보호할 수 있다.

```text
Node 자원 부족
↓
Pressure 발생
↓
일부 Pod eviction
↓
다른 Node에 재배치 가능
```

### Node Replacement

Cloud 환경에서는 Node를 수리하기보다 교체하는 방식이 흔하다.

```text
Node 이상
↓
cordon
↓
drain
↓
Node 제거
↓
새 Node 생성
```

### 핵심 정리

```text
Cordon
= 새 Pod 배치 금지

Drain
= 기존 Pod까지 안전하게 비우기

MemoryPressure
= 메모리 부족

DiskPressure
= 디스크 부족

Eviction
= Node 보호를 위해 Pod 제거

Node Replacement
= 문제 Node를 빼고 새 Node로 교체
```

---

## 3.9 Upgrade Strategy

Kubernetes는 버전이 계속 올라가므로 Control Plane과 Worker Node를 안전하게 업그레이드해야 한다.

핵심:

```text
Control Plane Upgrade
Node Upgrade
Version Skew
```

### Control Plane Upgrade

API Server, Scheduler, Controller Manager, etcd 등 관리 영역을 먼저 업그레이드한다.

관리형 Kubernetes는 Cloud Provider가 상당 부분 대신한다.

### Worker Node Upgrade

실제 Pod가 실행되므로 한꺼번에 바꾸면 안 된다.

보통:

```text
Node A
↓
cordon
↓
drain
↓
업그레이드 또는 교체
↓
다시 사용
```

### Rolling Upgrade

Node를 하나씩 또는 일부씩 교체한다.

```text
Node A 업그레이드
↓
정상 확인

Node B 업그레이드
↓
정상 확인

Node C 업그레이드
```

### Version Skew

Control Plane과 Node 버전 차이가 너무 크면 지원되지 않을 수 있다.

즉:

> 구성요소 간 허용 가능한 버전 차이가 존재한다.

### Upgrade 전 확인

```text
1. 현재 Kubernetes 버전
2. 새 버전과의 호환성
3. CNI / CSI 호환성
4. Ingress Controller 호환성
5. 사용 중인 API가 deprecated 되었는지
```

### PDB와 연결

Node drain 중 너무 많은 Pod가 동시에 내려가지 않게 PDB가 가용성을 보호한다.

### 핵심 정리

```text
Control Plane
→ 먼저 안전하게 업그레이드

Worker Node
→ 하나씩 또는 일부씩 Rolling Upgrade

Node Upgrade
→ cordon → drain → upgrade/replace

Version Skew
→ 구성요소 간 허용되는 버전 차이 존재

Upgrade 전
→ CNI / CSI / API 호환성 확인
```

---

## 3.10 Kubernetes Troubleshooting

Production Kubernetes에서는 에러 메시지를 보고 어느 계층 문제인지 빠르게 좁히는 것이 중요하다.

핵심 장애 유형:

```text
Pending
CrashLoopBackOff
OOMKilled
ImagePullBackOff
Network / DNS
Storage
Scheduling
```

### Pending

Pod가 생성됐지만 Node에 올라가지 못한 상태.

대표 원인:

```text
CPU / Memory 부족
GPU 부족
nodeSelector 조건 불일치
taint / toleration 문제
PVC / Storage 문제
```

확인:

```bash
kubectl describe pod <pod>
```

`Events`가 중요하다.

### CrashLoopBackOff

```text
시작
↓
Crash
↓
재시작
↓
Crash
↓
재시작
```

대표 원인:

```text
Application error
잘못된 ConfigMap / Secret
DB 연결 실패
잘못된 실행 명령
Liveness Probe 실패
```

확인:

```bash
kubectl logs <pod>
```

CrashLoopBackOff는 원인이 아니라 “계속 죽고 있음”이라는 결과 상태다.

### OOMKilled

Memory limit 초과로 종료.

```text
Memory 증가
↓
limit 초과
↓
OOMKilled
```

확인:

```bash
kubectl describe pod <pod>
```

해결 방향:

```text
Memory leak 확인
Memory limit 조정
Application memory 사용량 감소
```

### ImagePullBackOff

Image를 Registry에서 가져오지 못한 상태.

대표 원인:

```text
Image 이름 오타
Tag 없음
Registry 인증 실패
Network 문제
```

### Network 문제

단계적으로 확인:

```text
Pod 자체 접근 가능?
↓
Service 접근 가능?
↓
Ingress 접근 가능?
```

확인 대상:

```text
Pod IP
Service
Endpoint
CNI
NetworkPolicy
Port
```

예:

```text
Service는 8080으로 보내는데
App은 8000에서 Listen 중
```

이면 실패한다.

### DNS 문제

증상:

```text
IP로는 연결됨
이름으로는 연결 안 됨
```

예:

```text
10.0.0.10:5432 → 성공
postgres:5432  → 실패
```

이 경우 CoreDNS를 의심한다.

```bash
nslookup postgres
```

### Storage 문제

Stateful Pod가 `Pending` 또는 `ContainerCreating`에 오래 머무를 때:

```text
PVC 상태
PV 상태
CSI Driver
Volume Attach
AZ
```

확인.

### Scheduling 문제

대표 원인:

```text
CPU 부족
Memory 부족
GPU 부족

nodeAffinity
nodeSelector

taint / toleration

Pod anti-affinity
```

이때도 `kubectl describe pod`의 Event가 중요하다.

예:

```text
0/5 nodes are available
```

### 기본 Troubleshooting 순서

```text
1. Pod 상태 확인
      ↓
2. kubectl describe pod
      ↓
3. Events 확인
      ↓
4. kubectl logs 확인
      ↓
5. CPU / Memory 확인
      ↓
6. Scheduling 조건 확인
      ↓
7. Network / DNS 확인
      ↓
8. Storage 확인
```

대표 명령어:

```bash
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
```

### 증상별 빠른 연결

```text
Pending
→ Scheduling / Resource / Storage

CrashLoopBackOff
→ Application / Config / Probe

OOMKilled
→ Memory

ImagePullBackOff
→ Image / Registry

이름으로 연결 실패
→ DNS / CoreDNS

Service 연결 실패
→ Service / Port / CNI / NetworkPolicy

ContainerCreating에서 멈춤
→ Image 또는 Storage 가능성
```

### Chapter 3 최종 정리

```text
Cluster HA
↓
etcd
↓
CNI / CSI / DNS
↓
Autoscaling
↓
Reliability
↓
Node Operations
↓
Upgrade
↓
Troubleshooting
```

Production Kubernetes의 목표:

> Pod를 띄우는 것에서 끝나는 게 아니라, 장애·트래픽 증가·Node 교체·업그레이드 상황에서도 안정적으로 운영하는 것.

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 정정

다음은 원문 본문과 구분한 기존 공식 문서 검토 및 운영 설명이다. 원문의 개념 흐름도는 그대로 두고, 기존 Mermaid 그림은 이 보완 영역에 유지했다. 공식 확인일과 실행하지 않았다는 범위는 기존 기록대로 보존한다.

### 3.1 보완: 클러스터 설계: 한 대의 장애를 견디는 구조

단일 Control Plane은 관리 기능의 Single Point of Failure가 될 수 있다. 여러 Control Plane으로 HA를 구성하고, Worker도 여러 대에 분산한다. 예를 들어 Node A/B/C가 각각 API Pod를 실행하면 한 Node 장애 시 다른 Node의 Pod가 요청을 처리할 수 있다. replica 수만 늘리고 같은 Node에 모아두면 장애 범위를 분리하지 못한다.

Node Pool은 용도별 Node 그룹이다.

| Pool | 학습 예 | 설계 의도 |
| --- | --- | --- |
| General | 일반 Backend | 일반 서비스 용량 |
| GPU | vLLM | GPU가 필요한 추론 |
| Batch | Batch Job | 배치 작업 용량 |

Failure Domain은 함께 실패할 수 있는 범위다. Pod 1/2/3을 Node A/B/C에 나누고, Cloud에서는 AZ 장애도 고려한다. 간단한 예는 AZ-A의 Node 1/Pod A와 AZ-B의 Node 2/Pod B다. 플랫폼 전체로 확장하면 각 AZ에 General·GPU Node를 둘 수 있다. 이는 가상 설계 예이며 특정 제품·노드 수에 대한 실제 운영 결정이 아니다.

```mermaid
flowchart TB
  CP[HA Control Plane] --> GA
  CP --> GB
  subgraph AZA[AZ-A]
    GA[General Node] --> PA[API Pod A]
    GPUA[GPU Node] --> IA[vLLM Pod A]
  end
  subgraph AZB[AZ-B]
    GB[General Node] --> PB[API Pod B]
    GPUB[GPU Node] --> IB[vLLM Pod B]
  end
```

EKS 같은 관리형 Kubernetes에서는 Cloud Provider가 Control Plane과 etcd 운영을 맡는다. 애플리케이션 replica, 배치 정책, Node 용량과 데이터 보호까지 자동 해결됐다고 해석하지 않는다. 관리형 서비스별 책임 범위를 따로 확인한다.

### 3.2 보완: etcd: 클러스터의 기억장치

etcd는 Kubernetes의 클러스터 상태 저장소다. Pod, Deployment, Service, ConfigMap/Secret, 클러스터 설정 같은 API 객체 상태를 저장하며 API Server가 etcd와 통신한다. etcd에 문제가 생기면 새 Pod 생성이나 Deployment·Service 변경 같은 관리 작업이 영향을 받는다. 이미 실행 중인 모든 애플리케이션이 즉시 중단된다는 뜻은 아니다.

Quorum은 합의를 유지하는 과반수다. 멤버가 3개면 최소 2개가 통신하며 정상적으로 참여해야 한다. 단순히 프로세스가 살아 있는 것만으로 충분하지 않다. 흔한 홀수 구성은 3개와 5개이며 각각 과반수 2개와 3개가 필요하다.

```text
정상 클러스터 → etcd snapshot → 장애 → snapshot으로 복구
```

백업은 클러스터 상태 복구에 중요하다. 다만 etcd snapshot은 애플리케이션 Volume 데이터 백업과 다르다. 복구할 시점, snapshot 무결성, 보관 접근 권한, 별도의 Volume 복구 절차를 함께 검토한다. snapshot에는 Secret 등 민감한 상태가 포함될 수 있으므로 외부 공유 자료로 사용하지 않는다.

공식 etcd 3.6 복구 문서에서 snapshot 저장은 `etcdctl snapshot save`, 복구는 `etcdutl snapshot restore`로 구분한다. 복구는 새 논리 클러스터를 만들며 멤버들은 같은 snapshot을 사용한다. Kubernetes에서는 과거 revision으로 되돌아가면 informer cache와 watch에 문제가 생길 수 있어 revision bump와 compaction 처리를 검토해야 한다. 실제 복구는 설치 버전에 맞는 절차와 격리된 복구 검증이 필요하다. 여기서는 실행하지 않았다. [etcd 3.6 복구 문서](https://etcd.io/docs/v3.6/op-guide/recovery/)

### 3.3 보완: CNI: Pod 네트워크

CNI는 Container Network Interface다. Kubernetes 네트워크 플러그인은 CNI를 사용해 Pod에 IP를 할당하고 다른 Pod와 통신할 네트워크를 구성한다. CNI 자체는 인터페이스 규격이며 구체적인 routing·policy 처리는 플러그인과 설정에 따른다.

```text
Pod 생성 → IP 할당 → 다른 Pod와 통신
```

| 구현·방식 | 핵심 |
| --- | --- |
| Calico | Pod 네트워크, routing, NetworkPolicy |
| Cilium | eBPF 기반 네트워크 처리, NetworkPolicy, 네트워크 관측 |
| Overlay | Pod → 추가 가상 네트워크 계층 → Host 네트워크 |
| Routed | Pod IP → routing → 다른 Node의 Pod |

eBPF는 Linux Kernel 안에서 네트워크 처리와 관찰 등에 사용하는 기술이다. Cilium은 이를 networking, security, observability에 사용한다. Calico와 Cilium 모두 네트워크 정책을 지원하지만, 실제 기능과 호환성은 선택한 구성에 달려 있다.

Overlay와 Routed를 제품 이름에 고정해서 대응시키면 안 된다. Calico는 overlay와 non-overlay 방식을 지원하고, Cilium도 encapsulation과 native routing 등 여러 모드를 제공한다. Underlay의 Pod IP 경로 지원, MTU, Cloud 제약을 검토한다. [Calico 네트워크 선택](https://docs.tigera.io/calico/latest/networking/determine-best-networking), [Cilium routing](https://docs.cilium.io/en/stable/network/concepts/routing/)

### 3.4 보완: CSI: Storage 연결과 장애 경계

CSI는 Container Storage Interface다. AWS EBS, NFS, Ceph, Google Persistent Disk, Azure Disk처럼 서로 다른 Storage 시스템을 연결하는 표준 인터페이스다. Kubernetes에서 필요한 저장공간을 선언하면 CSI Driver가 실제 Storage와의 연동을 담당한다. Driver 예는 EBS CSI Driver, EFS CSI Driver, Ceph CSI다.

동적 프로비저닝의 개념 흐름은 다음과 같다. 이미 있는 PV를 사용하는 경우처럼 StorageClass가 모든 경로에 필수인 것은 아니다.

```mermaid
flowchart LR
  P[Pod] --> C[PVC]
  C --> S[StorageClass]
  S --> D[CSI Driver]
  D --> V[Storage and PV]
  V --> M[Attach and mount when required]
  M --> P
```

AWS 예는 `Pod → PVC → EBS CSI Driver → AWS EBS Volume`이다. Pod가 Node A에 배치되면 EBS Volume을 Node A에 attach하고 컨테이너에 mount하는 단계가 필요할 수 있다. 모든 Storage가 같은 attach 방식이나 제약을 갖는 것은 아니다. PVC는 PV에 바인딩되며, StorageClass는 동적 생성의 provisioner와 정책을 나타낸다. [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

Pod가 `Pending`이나 `ContainerCreating`에 오래 머무르면 다음을 나눠 확인한다.

- PVC/PV 상태와 이벤트, StorageClass, CSI Driver 상태
- Storage 자체 장애와 접근 권한
- Volume attach/mount 실패
- Storage와 Node의 Zone 일치 여부

Cloud Disk는 AZ에 묶일 수 있다. 예를 들어 Volume이 AZ-A에 있고 Pod를 AZ-B의 Node에 놓으면 attach가 불가능할 수 있다. Pod 문제처럼 보여도 Storage topology 문제일 수 있다.

### 3.5 보완: CoreDNS: 이름과 연결을 분리해서 본다

CoreDNS는 Kubernetes에서 흔히 사용하는 내부 DNS 서버다. 일반 Service 이름을 Service IP로 해석하는 예를 먼저 이해한다.

```text
API Pod → redis 이름 조회 → CoreDNS → Redis Service IP 반환
API Pod → Redis Service → Redis Pod
```

DNS 조회와 실제 애플리케이션 요청은 다른 단계다. 같은 Namespace에서는 `redis`, `postgres`, `my-api` 같은 Service 이름을 쓸 수 있다. 다른 Namespace의 예는 `redis.cache`다. 일반 Service는 ClusterIP로 해석되지만 headless Service는 Pod 주소를 반환하는 등 규칙이 다르다. [Service·Pod DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

Service가 살아 있어도 DNS 장애 때문에 이름으로 접근하지 못할 수 있다. 예를 들어 `10.0.0.10:5432`는 성공하고 `postgres:5432`는 실패하면 DNS를 의심한다. 이 주소는 원문의 가상 내부 주소 예다. 이름·Namespace·검색 경로·DNS 정책과 CoreDNS를 확인하며, 단서 하나로 CoreDNS 장애를 확정하지 않는다.

```bash
nslookup postgres
dig postgres
kubectl get pods -n kube-system
```

`nslookup`과 `dig`는 도구가 설치되고 문제 Pod와 DNS 조건이 같은 승인된 진단 환경에서 수행하는 예다. Pod와 DNS 요청이 늘면 CoreDNS replica와 CPU/Memory 설정도 중요해진다. 오류·지연·리소스와 요청량을 함께 관찰한다.

### 3.6 보완: Autoscaling: Pod 수·크기·Node 수

| 도구 | 조절 대상 | 원문의 학습 예 |
| --- | --- | --- |
| HPA | Pod replica 수 | CPU 증가에 API Pod 3개 → 6개 |
| VPA | 컨테이너 CPU/Memory requests 권고·조정 | CPU `500m`, Memory `1Gi` → CPU `1`, Memory `2Gi` |
| Cluster Autoscaler | Node 수 | HPA가 Pod 10개 요구 → 자원 부족 Pending → Node 증가 |
| KEDA | 이벤트 기반 workload scaling | Kafka lag 또는 Queue message 수 증가 → Consumer Pod 증가 |

HPA는 CPU, Memory, custom metric 등을 기준으로 desired replicas를 조절한다. CPU utilization 같은 비율은 requests를 기준으로 계산하므로 적절한 requests와 metrics 공급 경로가 필요하다. [HPA](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/)

VPA는 별도 구성요소이며 업데이트 모드에 따라 권고만 하거나 Pod 재생성을 수반할 수 있다. In-place 지원도 Kubernetes·VPA 버전과 설정 조건에 따라 다르다. 따라서 “항상 재시작 없이 메모리를 늘린다”고 이해하면 안 된다. [VPA](https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/)

Cluster Autoscaler 같은 Node autoscaler는 배치할 수 없는 Pod와 Node 조건을 보고 용량을 조정한다. 모든 Pending Pod가 Node 추가로 해결되는 것은 아니다. 잘못된 selector, 맞지 않는 GPU pool, Storage Zone, Cloud quota와 pool 상한은 따로 해결해야 한다. [Node autoscaling](https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/)

KEDA는 이벤트 소스를 연결하고 HPA에 외부 metric을 제공하는 방식으로 함께 동작한다. KEDA가 HPA를 전부 대체하는 별도 Node autoscaler는 아니다. [KEDA 2.18 개념](https://keda.sh/docs/2.18/concepts/)

```mermaid
flowchart TD
  T[Traffic increase] --> H[HPA detects demand]
  H --> P[More Pods required]
  P --> N{Node capacity available}
  N -->|No| C[Cluster Autoscaler adds capacity]
  C --> S[Schedule Pods]
  N -->|Yes| S
  S --> I[Image pull and app start]
  I --> M[Model loading for vLLM]
  M --> R[Readiness succeeds]
  R --> W[Serve traffic]
```

일반 앱은 모델 로딩 단계가 없을 수 있다. 어느 경우든 감지, Pod 생성·배치, image pull, 앱 시작, readiness까지 시간이 걸린다. vLLM은 모델 로딩 시간이 더해질 수 있다. 스케일 요청 시점과 실제 처리 용량 증가 시점을 구분해 급증 대비 여유 용량과 시작 시간을 검토한다.

### 3.7 보완: Reliability: 배치 분산과 종료 처리

Reliability는 장애나 배포 중에도 서비스를 유지하려는 성질이다. 여러 replica에 분산·PDB·readiness·graceful shutdown을 함께 적용해 검토한다.

| 수단 | 학습 예와 경계 |
| --- | --- |
| PodDisruptionBudget | `minAvailable: 2`로 drain 등 Eviction API 기반의 자발적 중단에서 가용 Pod 2개를 유지하도록 제한 |
| Pod anti-affinity | API Pod 1/2/3을 Node A/B/C에 분산 |
| Topology spread | Node 또는 AZ에 분산; AZ-A/B/C에 각각 2개 배치 예 |
| Readiness probe | 요청을 받을 준비가 된 Pod를 구분 |
| Graceful termination | 새 요청 유입을 줄이고 기존 요청을 마무리한 뒤 종료 |

PDB는 Node 고장 같은 비자발적 장애를 막지 못한다. 직접 Pod 삭제나 Deployment 자체의 rolling update가 PDB에 의해 모두 차단되는 것도 아니다. 중단된 Pod는 budget에 영향을 주지만 workload rollout은 해당 workload의 업데이트 전략을 따로 설정한다. `minAvailable: 2`는 어떤 장애에서도 무조건 2개가 살아 있다는 보장이 아니다. [Kubernetes disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

원문의 종료 mental model은 `종료 시작 → 새 트래픽 차단 → SIGTERM → 기존 요청 처리 → 정상 종료`다. 실제로는 endpoint 변경 전파와 프로세스 종료가 완벽한 단일 직렬 순서로 보장되지 않는다. 앱이 종료 신호를 처리하고 유예 시간 안에 요청을 마치도록 설계하며, 라우팅 전파와 기존 연결도 고려한다. [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)

### 3.8 보완: Node 작업: cordon·drain·pressure·교체

`cordon`은 Node를 unschedulable로 표시해 일반적인 신규 scheduling을 막고 기존 Pod는 유지한다. `drain`은 Node를 비우기 위해 Pod eviction 등을 수행한다. 다음은 실행하지 않은 변경 명령 예다.

```bash
kubectl cordon node-a
kubectl drain node-a
```

`drain`을 “살아 있는 Pod를 다른 Node로 그대로 이동한다”로 이해하면 안 된다. 보통 기존 Pod를 종료하고 workload controller가 대체 Pod를 만들어 다른 Node에 배치한다. 대체 용량, controller 유무, PDB, Storage와 데이터 안전성을 먼저 확인해야 한다.

기본 `drain` 명령은 DaemonSet, 관리 controller가 없는 Pod, 로컬 데이터 등의 조건 때문에 멈출 수 있다. DaemonSet을 무시하는 옵션은 해당 Pod를 다른 곳으로 옮겨주는 기능이 아니다. 강제 옵션으로 경고를 일괄 우회하지 않는다. 유지보수 후 기존 Node를 재사용할 때는 정상 상태를 확인하고 `uncordon` 단계가 필요하다. [안전한 Node drain](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/)

| 상태 | 의미·원인 예 | 영향 |
| --- | --- | --- |
| MemoryPressure | Node 메모리 부족 | Pod eviction 가능 |
| DiskPressure | Container image 과다, 로그 과다, ephemeral storage 부족 | 디스크 압박과 eviction 가능 |
| PIDPressure | 프로세스 수 한도에 대한 압박 | 프로세스·Pod 운영 문제 |

Eviction은 자원 부족 시 일부 Pod를 제거해 Node를 보호하는 동작이다. `자원 부족 → Pressure → 일부 Pod eviction → 대체 Pod가 다른 Node에 배치될 가능성`으로 이해한다. 재배치는 controller, 자원, 배치 제약이 충족돼야 하며 자동 성공을 보장하지 않는다.

Cloud에서는 문제 Node를 고치는 대신 교체하는 방식도 사용한다. 원문의 흐름은 `이상 감지 → cordon → drain → Node 제거 → 새 Node 생성`이다. 실제 작업에서는 새 용량을 먼저 확보할지, local data와 연결된 Volume을 어떻게 보호할지, 실패 시 어디서 중단할지 결정한 뒤 수행한다.

### 3.9 보완: 업그레이드: 호환성을 확인하고 순차 변경

Control Plane의 API Server, Scheduler, Controller Manager와 etcd 호환성을 먼저 검토하고, 지원되는 순서대로 관리 영역을 업그레이드한 뒤 Worker를 진행한다. 관리형 Kubernetes는 Provider가 일부 절차를 맡지만 addon과 앱 호환성 확인은 별개다. etcd를 임의로 Kubernetes와 같은 버전 번호로 올린다는 뜻이 아니다.

Worker는 실제 Pod가 실행되므로 전체를 동시에 바꾸지 않는다. 기본 흐름은 `cordon → drain → upgrade 또는 replace → 정상 확인 → 재사용`이다. Node A 완료·정상 확인 후 B, 이어 C처럼 하나씩 또는 일부씩 rolling upgrade한다. drain에서는 PDB와 가용 용량을 함께 확인한다.

업그레이드 전 확인 목록:

1. 현재 Kubernetes 구성요소 버전과 목표 버전
2. 업그레이드 경로와 앱 호환성
3. CNI·CSI 버전 호환성
4. Ingress Controller 호환성
5. 사용하는 API의 deprecated·removed 여부
6. 백업·복구 가능성, PDB, 여유 용량과 단계별 중단 기준

Version skew는 구성요소 사이에 지원되는 버전 차이다. 2026-09-27 확인한 공식 정책에서 HA API Server들은 서로 1 minor 이내여야 한다. kubelet은 API Server보다 새로울 수 없으며 일반적으로 최대 3 minor 오래될 수 있다. kubelet 1.25 미만은 최대 2 minor라는 예외가 있다. 혼합 API Server 버전에서는 허용 범위가 좁아진다. 이것만으로 모든 구성요소의 조합이 지원되는 것은 아니며, 도구·Provider가 더 엄격한 제한을 둘 수 있다. 실제 대상 버전의 전체 정책을 확인한다. [Version skew policy](https://kubernetes.io/releases/version-skew-policy/)

### 3.10 보완: 장애 진단: 결과 상태에서 원인 계층으로

오류 상태는 원인 후보를 좁히는 출발점이다. `Pending`은 scheduling 대기를 포함하지만 image 준비 등 시작 전 단계도 포함하므로 “항상 Node에 못 올라간 상태”로 한정하지 않는다. `CrashLoopBackOff`도 Pod phase 자체가 아니라 반복 재시작에 따른 대기 상태 표시이며 원인 이름이 아니다. [Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)

| 증상 | 원인 후보 | 먼저 확인할 근거 |
| --- | --- | --- |
| Pending | CPU/Memory/GPU 부족, nodeSelector, nodeAffinity, taint/toleration, Pod anti-affinity, PVC/Storage | `describe pod`의 Events, 배치 제약, 자원·PVC |
| CrashLoopBackOff | 앱 오류, ConfigMap/Secret 오류, DB 연결 실패, 실행 명령 오류, liveness 실패 | 컨테이너 상태, 재시작 수, 로그와 이전 인스턴스 로그 |
| OOMKilled | 메모리 limit 초과 또는 Node 메모리 상황과 관련된 OOM | 종료 reason, 메모리 사용 추세, limit, Node 상태 |
| ImagePullBackOff | image 이름 오타, 없는 tag, registry 인증 실패, network | image 경로·tag, 이벤트, 권한과 연결 |
| 이름 연결만 실패 | DNS·Namespace·검색 경로·CoreDNS | IP와 이름 비교, DNS 조회, DNS 서버 상태 |
| Service 연결 실패 | Service/EndpointSlice, port, CNI, NetworkPolicy | Pod부터 Service, Ingress 순서로 연결 경계 |
| ContainerCreating 장기 대기 | image 준비, Storage attach/mount, Pod network 준비 등 | 이벤트와 관련 Driver 상태 |

#### 로그·자원·배치

원문의 반복 crash 흐름은 `시작 → crash → 재시작 → crash → 재시작`이다. 현재 로그만으로 원인을 놓칠 수 있어 이전 인스턴스 로그도 확인한다. 아래 `<pod>`는 실제 승인된 Pod 이름으로 바꿀 자리이며, 다중 컨테이너라면 대상 컨테이너도 구분한다.

```bash
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
kubectl logs <pod> --previous
```

OOM의 학습 예는 `Memory 증가 → limit 초과 → OOMKilled`다. 메모리 누수를 확인하고, 적절한 limit 조정과 앱 메모리 사용량 감소를 검토한다. limit만 무작정 늘리면 Node 압박이나 누수 원인을 해결하지 못한다.

Scheduling에서는 CPU·Memory·GPU뿐 아니라 nodeAffinity, nodeSelector, taint/toleration, Pod anti-affinity를 확인한다. `0/5 nodes are available`은 5개 모두 배치 조건을 만족하지 못했다는 단서다. 상세 이벤트에서 각 이유를 확인한다.

#### 네트워크·DNS·스토리지

네트워크는 `Pod 자체 접근 → Service 접근 → Ingress 접근` 순서로 경계를 좁힌다. Pod IP, Service, Endpoint/EndpointSlice, CNI, NetworkPolicy, port를 확인한다. 예를 들어 Service의 대상 port가 `8080`인데 앱은 `8000`에서 listen하면 연결이 실패할 수 있다.

`10.0.0.10:5432 → 성공`, `postgres:5432 → 실패`는 DNS 진단을 시작할 학습 예다. `nslookup postgres`로 해석 여부를 확인한다. CoreDNS가 가능한 원인이지만 이름과 namespace가 잘못됐을 가능성도 남긴다.

Stateful Pod가 `Pending` 또는 `ContainerCreating`이면 PVC 상태, PV 상태, CSI Driver, Volume attach, AZ를 확인한다. 네트워크와 스토리지는 공통 하부 계층이므로 앱 재시작만 반복하기 전에 이벤트와 실제 연결 경계를 살핀다.

#### 진단 순서와 학습 경계

```text
1. Pod 상태
2. kubectl describe pod
3. Events
4. kubectl logs와 필요한 이전 로그
5. CPU / Memory
6. Scheduling 조건
7. Network / DNS
8. Storage
```

이 순서는 출발점이지 모든 사고에 고정 적용하는 규칙은 아니다. 관찰된 증거에 따라 분기하고 변경 전후를 비교한다. 운영 전체 흐름은 `Cluster HA → etcd → CNI/CSI/DNS → Autoscaling → Reliability → Node 작업 → Upgrade → Troubleshooting`이다. 면접에서는 replica만으로 가용성을 보장하지 못하는 이유와, PDB·Node 용량·Storage topology·종료 처리의 경계를 함께 설명한다.

## LLM in Practice

### Node drain 전 가용성과 막힘 원인 검토

**상황:** 가상의 3-replica API를 운영하는 Node의 유지보수 계획을 검토한다. 아직 drain은 실행하지 않았다.

**LLM에 줄 맥락:** 비식별화한 Pod 배치·Node 여유 자원, PDB 상태, readiness, Storage Zone, 종료 시간, Kubernetes와 addon 버전, 유지보수 허용 범위. Secret 값·인증 정보·실제 내부 주소는 제외한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    API replica는 3개이며 PDB minAvailable은 2다.
    배치·여유 자원·readiness·Storage Zone: [비식별 관측값]
    Kubernetes와 addon 버전: [버전]
    유지보수 범위와 종료 시간: [조건]
    아직 cordon이나 drain은 실행하지 않았다.
    [요청]
    계획을 먼저 검토하고 관측 사실, 가정, 누락 근거를 분리하라.
    PDB와 재배치 용량 때문에 drain이 막힐 조건을 설명하라.
    Node 고장과 Eviction API 기반 중단의 차이를 반영하라.
    [출력]
    원인 가설, 필요한 조회, 진행 조건, 중단 조건 표를 작성하라.
    변경·삭제 명령의 실행 승인을 추정하지 말라.
    [검증]
    실제 Events, PDB 상태, 자원, 버전별 공식 문서로 확인하라.
    실행 전 담당자가 검토할 항목과 남은 불확실성을 제시하라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    The API has 3 replicas and PDB minAvailable is 2.
    Placement, spare resources, readiness, Storage Zone: [sanitized observations]
    Kubernetes and addon versions: [versions]
    Maintenance scope and shutdown time: [constraints]
    No cordon or drain has been run.
    [Task]
    Review the plan first. Separate observations, assumptions, and missing evidence.
    Explain when the PDB or replacement capacity could block drain.
    Distinguish Node failure from disruption through the Eviction API.
    [Output]
    Create a table of hypotheses, read-only checks, go conditions, and stop conditions.
    Do not assume permission to run change or deletion commands.
    [Checks]
    Verify with actual Events, PDB state, resources, and version-specific official docs.
    List remaining uncertainty and checks for the responsible person before execution.
    ```

**예상 결과:** 계획의 가용성 조건, 가능한 막힘 원인, 조회 우선순위, 중단·검토 기준을 구분한 표.

**LLM이 틀릴 수 있는 부분:** PDB가 Node 장애까지 막는다고 단정하거나, drain이 Pod를 그대로 이동한다고 설명하거나, 부족한 GPU·Zone 조건을 Node 수 증가만으로 해결하려 할 수 있다.

**검증 방법:** 실제 상태와 버전별 공식 문서를 사람이 대조한다. 실행이 필요한 검증은 별도로 승인된 테스트 환경과 변경 절차에서 수행한다. 이 프롬프트는 작성한 활용 예이며 모델 응답이나 실제 유지보수 결과를 검증했다는 주장이 아니다.
