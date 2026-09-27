---
id: platform-infrastructure-linux-containers
status: studied
last_updated: 2026-09-27
last_reviewed: 2026-09-27
knowledge_ids:
  - PIS-01-01
  - PIS-01-02
  - PIS-01-03
  - PIS-01-04
  - PIS-01-05
  - PIS-01-06
  - PIS-01-07
  - PIS-01-08
  - PIS-01-09
  - PIS-01-10
  - PIS-01-11
  - PIS-01-12
---

# Linux, 네트워크와 컨테이너

문서 유형: Learn / Reference. 제공된 Chapter 1의 개념 학습을 정리했다. `studied`는 Linux·Docker·Kubernetes를 실제 구축하거나 장애 실험했다는 뜻이 아니다. 명령, Dockerfile, YAML, IP, PID와 수치는 설명용이며 실행하지 않았다. `<PID>`와 `<pod>`는 실제 대상에 맞춰 바꿀 자리표시자다. 종료 명령은 대상과 권한을 확인한 격리 실습에서만 사용한다.

## 전체 관계

```mermaid
flowchart TD
    K[Kubernetes resource and lifecycle settings] --> R[Container runtime]
    I[Image and filesystem] --> R
    R --> P[Linux application process]
    N[Namespaces: process view and network] --> P
    C[cgroups: CPU and memory control] --> P
    P --> F[Files and sockets via file descriptors]
    P --> S[Signals and exit status]
    S --> O[Observe logs, limits and restart policy]
```

실무에서는 애플리케이션 프로세스, 자원 제어, 네트워크, 저장소를 함께 본다. 소스의 기본 모형을 아래에 보존하되, **원문 보완**은 과도한 일반화를 바로잡는다.

## 1.1 Linux Process

Linux에서 **Process = 실행 중인 프로그램**이다.

예:

```bash
python app.py
```

프로그램이 실행되면 메모리에 올라가고 Linux가 하나의 Process로 관리한다.

### PID

각 Process에는 해당 PID namespace에서 고유한 번호인 **PID(Process ID)** 가 있다.

```bash
ps aux
```

예:

```text
USER    PID   COMMAND
root      1   /sbin/init
user   1523   python app.py
user   1601   nginx
```

PID를 알면 특정 프로세스를 조회하거나 종료할 수 있다.

```bash
kill 1523
```

### Parent / Child Process

대부분의 Process는 다른 Process가 생성한다.

```text
bash
 ↓
python app.py
```

- `bash` = Parent Process
- `python` = Child Process
- 부모의 PID = PPID(Parent Process ID)

```bash
ps -ef
```

예:

```text
UID   PID   PPID   CMD
user  1000  900    bash
user  1200  1000   python app.py
```

이 구조는 이후 **Container의 PID 1**, **Graceful Shutdown**, **Zombie Process**와 연결된다.

### Process State

대표적인 상태:

```text
Running
Sleeping
Stopped
Zombie
```

- **Running**: 실행 중이거나 CPU를 기다리는 상태
- **Sleeping**: I/O나 이벤트를 기다리는 상태
- **Stopped**: 일시 정지
- **Zombie**: 프로세스는 종료됐지만 부모가 종료 결과를 아직 회수하지 않은 상태

Zombie는 살아서 CPU를 쓰는 프로세스가 아니다. 실제 실행은 끝났고 process table에 정보만 일부 남아 있다.

### Exit Code

프로그램은 종료될 때 Linux에 결과값을 반환한다.

보통:

```text
0     → 정상 종료
0이외 → 오류
```

확인:

```bash
ls /tmp
echo $?
```

잘못된 명령 예:

```bash
ls /not-exist
echo $?
```

Docker와 Kubernetes에서도 Container 종료 시 Exit Code를 확인해 정상/비정상 종료를 판단한다.

### /proc

Linux는 `/proc`을 통해 현재 실행 중인 시스템과 프로세스 상태를 보여준다.

PID가 1200이면:

```text
/proc/1200
```

대표 경로:

```text
/proc/1200/status
/proc/1200/cmdline
/proc/1200/fd
```

### 플랫폼 관점 연결

```text
Kubernetes Pod
→ Container
→ 결국 Linux Process
```

예:

```text
Pod
└── Container
     └── vLLM Process
```

프로세스 종료 → Exit Code → Container Runtime 감지 → 재시작 정책에 따른 Kubernetes 재시작 흐름으로 연결된다.

### 핵심 정리

```text
Program이 실행되면 Process가 된다.
Process에는 PID가 있다.
Process는 Parent / Child 관계를 가진다.
Process가 종료되면 Exit Code를 남긴다.
Zombie는 종료됐지만 부모가 회수하지 않은 Process다.
/proc에서 Process 정보를 확인할 수 있다.
```

---

## 1.2 CPU / Memory

플랫폼 엔지니어 관점에서는 CPU와 Memory를 **왜 느려지고, 왜 죽는가** 중심으로 이해하면 된다.

### CPU

CPU는 프로세스의 코드를 실행한다.

CPU 사용률이 높다는 것은 대체로 처리해야 할 계산이 많다는 뜻이다.

대표적인 CPU-bound 작업:

```text
JSON 처리
압축
암호화
대량 연산
LLM inference 일부 연산
```

### CPU-bound vs I/O-bound

**CPU-bound**:

- 계산이 병목

**I/O-bound**:

- DB 응답
- API 응답
- 파일 읽기
- 네트워크/디스크 대기

### CPU Core

예를 들어 8 Core CPU라면 여러 작업을 병렬로 처리할 수 있다.

프로세스가 Core 수보다 많아도 Linux scheduler가 CPU 시간을 나눠준다.

### Memory

프로세스 실행에 필요한 데이터가 RAM에 올라간다.

예:

```text
Application code
Cache
Request data
Model data
```

### Swap

RAM이 부족하면 일부 데이터를 디스크의 Swap으로 옮길 수 있다.

```text
RAM 부족
 ↓
일부 데이터를 Disk의 Swap으로 이동
```

디스크는 RAM보다 훨씬 느리므로 Swap 사용량이 많으면 서버가 매우 느려질 수 있다.

### OOM

OOM = **Out Of Memory**

메모리가 부족해 더 이상 프로세스를 정상적으로 유지할 수 없는 상황.

Linux는 상황에 따라 프로세스를 강제로 종료할 수 있으며, 이를 흔히 **OOM Killer**라고 한다.

### Kubernetes와 연결

예:

```yaml
resources:
  requests:
    memory: "2Gi"
  limits:
    memory: "4Gi"
```

- `request` = 스케줄러가 배치 판단에 사용하는 자원 요청량. 메모리를 즉시 사전 할당하거나 실제 사용을 제한하는 값은 아니다.
- `limit` = 최대 사용 가능량

Memory limit 초과 시 흔히:

```text
OOMKilled
```

흐름:

```text
Application memory 증가
        ↓
Container memory limit에 도달하고 메모리 회수 불가
        ↓
Process 종료 가능
        ↓
Container 상태에서 OOMKilled 확인 가능
```

### CPU Limit

CPU는 Memory와 다르게 limit 초과 시 프로세스를 바로 죽이지 않는다.

보통:

```text
CPU limit 초과
↓
CPU 사용 시간 제한
↓
처리가 느려짐
```

이를 **CPU throttling**이라고 한다.

### 핵심 정리

```text
CPU = 계산을 수행하는 자원
Memory = 프로세스가 데이터를 저장하는 공간

CPU-bound = 계산이 병목
I/O-bound = DB, Network, Disk 등이 병목

Memory가 부족하면 OOM이 발생할 수 있다.

Kubernetes memory limit에서 메모리 회수 불가
→ OOMKilled 가능

Kubernetes CPU limit 초과
→ CPU throttling
```

---

## 1.3 File / File Descriptor

Linux에서는 프로세스가 파일이나 네트워크 연결을 사용할 때 **File Descriptor(FD)** 라는 번호로 관리한다.

### stdin / stdout / stderr

일반적인 프로세스는 관례적으로 다음 표준 FD를 사용한다. 닫거나 다른 대상으로 바꿀 수도 있다:

```text
0 = stdin
1 = stdout
2 = stderr
```

예:

```bash
python app.py > output.log
```

stdout을 파일로 보낸다.

### File Descriptor

프로세스가 파일을 열면 Linux는 번호를 하나 부여한다.

```text
FD 0 → stdin
FD 1 → stdout
FD 2 → stderr
FD 3 → config.yaml
FD 4 → log.txt
```

### Socket도 FD다

네트워크 연결도 FD로 관리된다.

예:

```text
FD 5 → Client A TCP connection
FD 6 → Client B TCP connection
FD 7 → Client C TCP connection
```

즉 Linux는 다음을 비슷한 방식으로 FD로 다룬다.

```text
File
Socket
Pipe
```

### Too many open files

프로세스가 사용할 수 있는 FD 개수에는 제한이 있다.

```bash
ulimit -n
```

예:

```text
1024
```

FD가 계속 쌓여 limit에 도달하면:

```text
Too many open files
```

가 발생할 수 있다.

### Connection Leak

DB나 Network connection을 생성하고 닫지 않으면 FD가 계속 누적될 수 있다.

```text
DB connection 생성
→ 사용
→ close 안 함
→ 계속 누적
→ FD exhaustion
```

서비스는 살아 있는데 새 연결을 못 받는 상황의 원인이 될 수 있다.

### 확인 명령어

```bash
lsof -p <PID>
```

또는:

```bash
ls /proc/<PID>/fd
```

### 플랫폼 관점

API Server는 예를 들어:

```text
API Server
 ├─ Client Socket
 ├─ DB Connection
 ├─ Redis Connection
 └─ Log File
```

등을 모두 FD로 사용한다.

### 핵심 정리

```text
FD = 프로세스가 파일/Socket 등을 다루기 위한 번호

0 = stdin
1 = stdout
2 = stderr

Socket도 FD를 사용한다.
FD에는 제한이 있다.

FD가 계속 쌓이면
→ Too many open files

운영에서는
ulimit / lsof / /proc/<PID>/fd
를 확인한다.
```

---

## 1.4 Linux Networking

플랫폼 엔지니어라면 우선 **IP, Port, Socket, DNS, Routing**을 확실히 알아야 한다.

### IP와 Port

- IP = 어느 장비인지
- Port = 그 장비 안의 어느 프로그램인지

예:

```text
10.0.0.10:8080
```

### Socket

Socket은 네트워크 통신의 끝점이다.

대략:

```text
IP + Port + Protocol
```

조합이라고 보면 된다.

### TCP vs UDP

**TCP**

- 연결 기반
- 신뢰성 있음
- 순서 보장
- 재전송

HTTP, DB 연결 등에 많이 사용.

**UDP**

- 연결 없이 바로 전송
- 연결 설정이 단순함. 항상 더 빠르다는 보장은 없음
- 전송/순서 보장 없음

DNS 등에서 많이 사용.

### TCP Handshake

```text
Client      Server

 SYN   →
       ← SYN-ACK
 ACK   →
```

이후 실제 데이터를 주고받는다.

### 127.0.0.1 vs 0.0.0.0

**127.0.0.1**

- localhost
- 현재 network namespace의 loopback에서 접근 가능

**0.0.0.0**

- 모든 로컬 IPv4 Network Interface에서 요청을 받겠다는 의미

Container에서 App이 127.0.0.1에만 bind하면 Container 밖에서 접근이 안 될 수 있다.

### DNS

DNS는 이름을 IP로 바꾼다.

```text
api.example.com
↓
10.0.0.20
```

확인:

```bash
dig example.com
```

### Routing

Routing은:

> 이 IP로 가려면 어느 방향으로 보내야 하는가?

를 결정한다.

```bash
ip route
```

예:

```text
default via 10.0.0.1
```

### Subnet / CIDR

예:

```text
10.0.0.0/24
```

같은 네트워크 범위를 나타낸다.

Kubernetes에서도 `Pod CIDR`, `Service CIDR` 같은 표현이 나온다.

### NAT

NAT는 IP 주소 또는 Port를 변환하는 기술이다.

```text
Container IP
10.1.0.5
   ↓
NAT
   ↓
Node IP
192.168.0.10
```

### 기본 명령어

```bash
ip addr
ip route
ss -lntp
dig example.com
curl http://server:8080
```

### 기본 장애 분석

```text
1. App이 떠 있는가?
2. Port를 열고 있는가?
3. 올바른 IP에 bind 했는가?
4. DNS가 정상인가?
5. Routing이 정상인가?
6. Firewall / NetworkPolicy 문제인가?
```

### 핵심 정리

```text
IP = 장비
Port = 프로세스
Socket = 통신 endpoint

TCP = 연결 + 신뢰성
UDP = 비연결 방식, 전송과 순서 미보장

127.0.0.1 = 자기 자신만
0.0.0.0 = 모든 interface

DNS = 이름 → IP
Routing = 패킷이 갈 경로
CIDR = 네트워크 범위
NAT = IP/Port 변환
```

---

## 1.5 Signal / Process Lifecycle

프로세스는 시작되고, Signal을 받고, 종료된다.

플랫폼에서는 특히 **SIGTERM / SIGKILL / Graceful Shutdown**이 중요하다.

### Signal

Signal은 운영체제가 프로세스에 보내는 제어 메시지다.

예:

```text
"종료해"
"강제로 죽어"
"인터럽트 발생"
```

### SIGTERM

정상적으로 종료해 달라는 요청.

```bash
kill <PID>
```

기본적으로 SIGTERM을 보낸다.

정상 흐름:

```text
SIGTERM 수신
↓
새 요청 받지 않음
↓
기존 요청 처리
↓
DB connection 정리
↓
파일 flush
↓
종료
```

이런 종료를 **Graceful Shutdown**이라고 한다.

### SIGKILL

즉시 강제 종료.

```bash
kill -9 <PID>
```

정리 작업 기회가 없다.

```text
SIGTERM = 정리하고 종료해
SIGKILL = 즉시 죽어
```

### SIGINT

보통 `Ctrl + C`가 SIGINT를 보낸다.

### Graceful Shutdown

API 서버가 요청 처리 중 바로 죽으면 요청이 실패한다.

Graceful Shutdown은:

```text
종료 요청
↓
새 요청 차단
↓
기존 요청 마무리
↓
connection 정리
↓
프로세스 종료
```

흐름이다.

### Kubernetes와 연결

Pod 종료 시 보통:

```text
Pod 삭제
↓
Container Process에 SIGTERM
↓
Grace Period 동안 대기
↓
아직 안 죽었으면 SIGKILL
```

### PID 1

Container 내부에서 가장 처음 실행되는 프로세스가 보통 PID 1이다.

```text
Container
└── python app.py
    PID 1
```

PID 1이 Signal을 제대로 처리하지 못하면 SIGTERM을 무시하고 결국 SIGKILL될 수 있다.

### 핵심 정리

```text
Signal = 프로세스에 보내는 제어 메시지

SIGTERM
= 정상 종료 요청

SIGKILL
= 즉시 강제 종료

SIGINT
= 보통 Ctrl+C

Graceful Shutdown
= 기존 작업을 정리하고 정상 종료

Kubernetes Pod 종료
= SIGTERM → 대기 → 필요하면 SIGKILL

Container에서는 PID 1의 Signal 처리가 중요
```

---

## 1.6 Linux Namespace

Namespace는:

> 프로세스마다 서로 다른 Linux 환경을 보이게 만드는 기능

이다.

Container 격리의 핵심 기반 기술 중 하나다.

### PID Namespace

Process 목록을 분리한다.

Container 내부:

```text
PID 1  python app.py
PID 20 worker
```

Host:

```text
PID 12345 python app.py
PID 12380 worker
```

Container 내부 PID와 Host PID는 다를 수 있다.

### Network Namespace

독립적인:

```text
IP
Network Interface
Routing Table
Port
```

를 가질 수 있다.

그래서 별도 network namespace를 쓰는 같은 Host 안의 여러 Container가 같은 Port 번호를 각각 사용할 수 있다.

### Mount Namespace

Filesystem mount 상태를 분리한다.

Container마다 독립된 filesystem이 있는 것처럼 보이게 한다.

### UTS Namespace

Hostname 등을 분리한다.

### Container와 연결

```text
Linux Host
 ├─ Container A
 │   ├─ PID Namespace
 │   ├─ Network Namespace
 │   └─ Mount Namespace
 │
 └─ Container B
     ├─ PID Namespace
     ├─ Network Namespace
     └─ Mount Namespace
```

### VM vs Container

```text
VM
→ OS 자체를 분리

Container
→ 같은 Kernel 위에서 프로세스 환경을 격리
```

### 핵심 정리

```text
Namespace = 프로세스가 보는 Linux 환경을 격리

PID Namespace
→ Process 목록 분리

Network Namespace
→ IP / Port / Routing 분리

Mount Namespace
→ Filesystem mount 분리

UTS Namespace
→ Hostname 분리
```

그리고:

```text
Namespace = 무엇을 볼 수 있는가를 격리
cgroup    = 자원을 얼마나 쓸 수 있는가를 제한
```

---

## 1.7 cgroup

cgroup은:

> 프로세스가 사용할 수 있는 CPU, Memory 같은 자원을 제한하고 측정하는 Linux 기능

이다.

### CPU 제한

```text
Container A → 최대 1 CPU
Container B → 최대 2 CPU
```

CPU limit에 걸리면 보통 프로세스 종료가 아니라 **CPU throttling**이 발생한다.

### Memory 제한

예:

```text
Container A
Memory limit = 2GB
```

초과 시:

```text
Memory limit에 도달하고 메모리 회수 불가
↓
OOM 가능
↓
Process 종료 가능
```

### Container와 cgroup

```text
Container A
├─ Namespace → 다른 Container와 분리
└─ cgroup    → CPU 1개, Memory 2GB 제한
```

Container의 핵심은 대략:

```text
Namespace
+
cgroup
+
filesystem
```

### Kubernetes와 연결

```yaml
resources:
  limits:
    cpu: "1"
    memory: "2Gi"
```

흐름:

```text
Kubernetes resource limit
↓
Container runtime
↓
Linux cgroup
↓
실제 CPU / Memory 제한
```

### 핵심 정리

```text
cgroup = CPU / Memory 같은 자원을 제어하는 기능

CPU limit 초과
→ throttling

Memory limit 초과
→ OOM 가능

Namespace
→ 무엇을 볼 수 있는가

cgroup
→ 얼마나 쓸 수 있는가
```

---

## 1.8 Container Fundamentals

Container는:

> 프로세스를 격리된 환경에서 실행하는 방식

이다.

### Container vs VM

VM은 각자 Guest OS를 가진다.

Container는 Host Linux Kernel을 공유한다.

그래서 일반적으로 VM보다 가볍고 시작이 빠르다.

### Container 안에서는 결국 Process가 실행된다

```bash
docker run nginx
```

를 실행해도 결국 Container 안에서 `nginx` 프로세스가 실행된다.

### Docker

사용자가 Container를 쉽게:

```text
build
run
stop
push
pull
```

할 수 있게 해주는 도구.

### containerd

Container lifecycle을 실제로 관리하는 runtime 계층.

Kubernetes에서는 보통:

```text
Kubernetes
   ↓
containerd
   ↓
Container 실행
```

구조로 본다.

### OCI

Container Image 형식과 Runtime 동작 방식을 표준화하는 Container 생태계 공통 표준.

### runc

Linux 기능을 이용해 실제 Container process를 만드는 저수준 runtime.

```text
Kubernetes
   ↓
containerd
   ↓
runc
   ↓
Linux Process
```

### Container Lifecycle

```text
Image
↓
Container 생성
↓
Start
↓
Process 실행
↓
Stop
↓
Container 종료
```

Main process가 끝나면 Container도 종료된다.

### Kubernetes와 연결

```text
Pod
└─ Container
   └─ Application Process
```

CrashLoopBackOff는 반복 종료 후 정책에 따라 재시작을 시도하면서 대기 시간을 늘리는 상태다. 원인 자체가 아니라 재시작 backoff 표시다.

### 핵심 정리

```text
Container
= 격리된 환경에서 실행되는 Linux Process

VM
= OS까지 분리

Container
= Host Kernel 공유

Docker
= Container를 쉽게 사용하는 도구

containerd
= Container lifecycle 관리

runc
= 실제 Container process 실행

OCI
= Container 표준

Container의 main process가 끝나면
Container도 종료
```

---

## 1.9 Container Image / OCI

Container를 실행하려면 먼저 Image가 필요하다.

> Image = Container를 만들기 위한 실행 패키지

### Image 안의 내용

예:

```text
Python runtime
Application code
Library
Config
```

흐름:

```text
Image
↓
Container 생성
↓
Process 실행
```

### Image Layer

Image는 여러 Layer로 구성될 수 있다.

```text
Base Linux
↓
Python 설치
↓
Library 설치
↓
Application code 추가
```

### Dockerfile

Image를 어떻게 만들지 정의하는 파일.

```dockerfile
FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### Build Cache

변경되지 않은 Layer는 다시 만들지 않고 재사용할 수 있다.

### Registry

Image 저장 서버.

대표 예:

```text
Docker Hub
Amazon ECR
Google Artifact Registry
GitHub Container Registry
```

흐름:

```text
Build
↓
Registry에 Push
↓
Server/Kubernetes가 Pull
↓
Container 실행
```

### Tag vs Digest

Tag:

```text
myapp:1.0
myapp:latest
```

- 사람이 보기 쉬움
- 변경 가능

Digest:

```text
myapp@sha256:abc123...
```

- 실제 Image content 식별
- 고정적

### Multi-stage Build

Build에 필요한 도구와 실제 Runtime에 필요한 도구를 분리해 최종 Image를 작게 만든다.

```text
Build Stage
→ compiler 포함
→ binary 생성

Runtime Stage
→ binary만 포함
```

### Kubernetes와 연결

```text
Pod 생성
↓
Node 선택
↓
Image Pull
↓
Container 생성
↓
Process 실행
```

Image Pull 실패 후 재시도 대기 상태:

```text
ImagePullBackOff
```

가능 원인:

```text
Image 이름 오류
Tag 오류
Registry 인증 실패
Network 문제
```

### 핵심 정리

```text
Image
= Container 실행에 필요한 패키지

Dockerfile
= Image 만드는 방법 정의

Layer
= Image를 여러 단계로 나눈 구조

Registry
= Image 저장소

Tag
= 사람이 읽기 쉬운 버전명

Digest
= 실제 Image를 고정적으로 식별

Multi-stage build
= 최종 Image 크기 줄이기
```

---

## 1.10 Container Networking

Container도 네트워크 통신을 해야 하므로 보통 자기만의 Network Namespace와 IP를 가진다.

### Container IP

예:

```text
Container A → 172.18.0.2
Container B → 172.18.0.3
```

### veth pair

Container와 Host 네트워크를 연결하는 가상의 랜선.

```text
Container
   │
veth
   │
Host
```

### Linux Bridge

Host 안에서 여러 Container를 연결할 수 있다.

```text
Container A ─┐
             ├─ Linux Bridge ─ Host Network
Container B ─┘
```

### Port Mapping

예:

```bash
docker run -p 8080:80 nginx
```

의미:

```text
Host 8080
   ↓
Container 80
```

### NAT

외부에서 Host로 들어온 요청을 Container IP/Port로 전달할 때 NAT가 사용될 수 있다.

```text
외부 Client
    ↓
Host IP:8080
    ↓
NAT
    ↓
Container IP:80
```

### Container 간 통신

같은 Network에 있는 Container끼리는 네트워크 정책이 허용하면 통신할 수 있다.

Docker Compose에서는 이름으로 접근하는 경우도 많다.

예:

```text
redis:6379
```

### Kubernetes와 연결

Kubernetes에서는 Pod마다 IP를 가지고 통신하며 CNI가 이를 구현한다.

### 핵심 정리

```text
Container
→ 별도 Network Namespace
→ 별도 IP 가능

veth pair
→ Container와 Host를 연결

Bridge
→ 여러 Container를 연결

Port Mapping
→ Host Port를 Container Port와 연결

NAT
→ 외부와 Container 사이 주소 변환

Kubernetes에서도 이 개념이 Pod Networking의 기반
```

---

## 1.11 Container Storage

Container 내부 filesystem은 기본적으로 **Container 수명에 종속적**이다.

### Ephemeral filesystem

Container 내부에 저장한 파일은 Container 삭제 후 새로 만들어질 때 사라질 수 있다.

```text
Container 생성
↓
파일 생성
↓
Container 삭제
↓
파일도 사라짐
```

### Bind Mount

Host의 특정 디렉터리를 Container에 연결.

```text
Host
/data
  ↓
Container
/app/data
```

예:

```bash
docker run -v /data:/app/data myapp
```

### Volume

Container runtime이 관리하는 별도 저장공간.

```text
Container
   ↓
Volume
   ↓
Persistent Data
```

PostgreSQL, Redis, 파일 저장 서비스 등 지속 데이터에 사용한다.

### Container와 데이터 분리

좋은 구조:

```text
Application Container
→ 언제든 다시 만들 수 있음

Persistent Data
→ 별도 Storage에 저장
```

Application Container는 가능한 stateless하게 만드는 것이 운영에 유리하다.

### Kubernetes와 연결

```text
Pod
 ↓
PVC
 ↓
Persistent Storage
```

Kubernetes에서는 PV / PVC / StorageClass를 사용한다.

### 핵심 정리

```text
Container 내부 filesystem
→ 기본적으로 ephemeral

중요한 데이터
→ Container 외부에 저장

Bind Mount
→ Host 경로를 직접 연결

Volume
→ Container와 분리된 저장공간

Application Container
→ 가능하면 stateless

Kubernetes에서는
PV / PVC를 통해 Persistent Storage 사용
```

---

## 1.12 Linux / Container Troubleshooting

장애 시 무작정 로그부터 보기보다 계층적으로 확인한다.

### CPU 문제

증상:

```text
응답이 느림
처리량 감소
CPU 사용률 높음
```

확인:

```bash
top
ps aux
```

Container/Kubernetes에서는 CPU throttling도 본다.

### Memory 문제

증상:

```text
프로세스가 갑자기 종료됨
Container 재시작
OOMKilled
```

확인:

```bash
free -h
```

Kubernetes:

```bash
kubectl describe pod <pod>
```

### Disk 문제

```bash
df -h
```

Disk 100%는 로그 기록 실패, DB write 실패, Container 이상 동작 등을 유발할 수 있다.

### File Descriptor 문제

증상:

```text
Too many open files
새 connection 생성 실패
```

확인:

```bash
ulimit -n
lsof -p <PID>
```

### Network 문제

단계:

```text
DNS 되는가?
↓
IP까지 갈 수 있는가?
↓
Port가 열려 있는가?
↓
Application이 응답하는가?
```

명령어:

```bash
dig example.com
curl http://server:8080
ss -lntp
ip route
```

### Process Crash

확인:

```text
Exit Code
Application log
OOM 여부
Signal 여부
```

### 기본 장애 분석 Workflow

```text
1. 프로세스가 살아 있는가?
2. CPU / Memory가 정상인가?
3. Disk가 꽉 차지 않았는가?
4. FD가 부족하지 않은가?
5. Port가 열려 있는가?
6. DNS / Network가 정상인가?
7. 로그와 Exit Code 확인
```

Container에서는 추가로:

```text
Image 문제?
Resource limit 문제?
Container가 재시작 중인가?
Volume 문제?
```

### Chapter 1 최종 정리

```text
Linux Process
↓
CPU / Memory
↓
File Descriptor
↓
Networking
↓
Signal
↓
Namespace
↓
cgroup
↓
Container
↓
Image
↓
Container Networking
↓
Container Storage
↓
Troubleshooting
```

Container를 가장 짧게 정리하면:

```text
Container
= Linux Process
+ Namespace
+ cgroup
+ filesystem
```

---

## 원문 보완과 적용 조건

공식 문서 확인일: 2026-09-27. 아래는 개념의 적용 범위를 바로잡는 보완이며, 실행 검증이나 특정 설치 버전의 보장은 아니다. 커널·runtime·네트워크 모드·Kubernetes 설정을 실제 환경에서 확인한다.

### 자원 요청, limit와 종료 원인

원문의 “request = 최소한 확보하고 싶은 자원”은 배치용 요청량으로 이해한다. scheduler가 request를 바탕으로 배치하며 RAM을 미리 할당하지는 않는다. CPU limit는 보통 throttling, memory limit는 반응적 OOM 집행이다. `free -h`의 호스트 여유만으로 컨테이너 메모리 부족을 배제하지 않는다. [Kubernetes 자원 관리](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)

cgroup v2의 `memory.max`에 도달해 회수할 수 없으면 해당 cgroup에서 OOM 처리가 일어날 수 있다. “한 번 초과하면 항상 즉시 전체 Pod가 죽는다”는 뜻이 아니다. 예시 `2GB`와 YAML `2Gi`는 서로 다른 단위다. [Linux cgroup v2](https://cdn.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)

### PID 1과 graceful shutdown

PID는 namespace별 식별자다. PID namespace의 init은 특별한 signal 규칙을 가지며 고아 자식의 종료 결과를 회수하는 역할도 한다. handler 등록과 자식에게 signal 전달 여부를 구분한다. “PID 1이면 모든 SIGTERM을 무시한다”는 일반화는 틀리다. [Linux PID namespaces](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html)

Pod 종료 모형의 SIGTERM은 보통의 stop signal이다. `preStop` hook도 유예 시간 안에서 실행되며 이미지의 `STOPSIGNAL` 또는 지원되는 설정이 signal을 바꿀 수 있다. 시간 안에 끝나지 않으면 강제 종료된다. CrashLoopBackOff는 반복 재시작의 대기 상태이며 원인은 exit code·이전 로그·이벤트로 확인한다. [Kubernetes Pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/)

### 네트워크의 주소·격리·노출 범위

“IP=장비, port=프로그램”은 입문 모형이다. 정확히는 IP는 주소/interface, port는 transport endpoint 식별에 쓰이며 protocol과 namespace도 고려한다. TCP/UDP의 HTTP·DNS 예시는 흔한 용도이지 모든 transport를 제한하는 규칙이 아니다. UDP가 항상 더 빠른 것도 아니다. `127.0.0.1`은 현재 network namespace의 loopback이고 `0.0.0.0` bind는 모든 로컬 IPv4 interface에서 수신한다는 뜻이다.

`docker run -p 8080:80 nginx`는 host 주소를 생략해 모든 host interface에 공개될 수 있다. 로컬 실습의 범위를 줄이는 예시는 아래와 같다. 실제 방화벽·직접 routing·Docker 버전도 확인한다. Docker 28.0.0 이전에는 localhost 게시도 같은 L2 네트워크의 다른 host에서 접근 가능한 문제가 있었다. [Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)

```bash
docker run -p 127.0.0.1:8080:80 nginx
```

별도 network namespace일 때 같은 port 사용이 가능하다. 같은 Pod의 컨테이너는 일반적으로 network namespace를 공유한다. bridge/veth/NAT는 대표 모형이며 host networking 등 모든 모드가 그 경로를 따르지는 않는다. Linux 컨테이너의 kernel 공유는 Linux host 기준이다. VM 위에서 Docker를 쓰는 경우 실제 Linux host와 사용자 OS를 구분한다. containerd→runc도 대표 구현 경로다. [Docker 실행 모드](https://docs.docker.com/engine/containers/run/), [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)

### 이미지·캐시·저장소·명령의 경계

`python:3.12`는 원문의 예시 tag이며 테스트한 버전이 아니다. 축약된 `sha256:abc123...`는 실행 가능한 digest가 아니다. `COPY . .`가 바뀌면 이후 `RUN pip install` 캐시가 무효화될 수 있다. 변경 빈도가 낮은 의존성 입력을 먼저 복사하는 구조를 검토한다. [Docker build cache](https://docs.docker.com/build/cache/invalidation/)

원문의 Image `Config`와 `COPY . .`를 비밀정보 포함 허가로 해석하지 않는다. build context에서 민감 파일을 제외한다. 비밀을 Dockerfile `ARG`/`ENV`에 남기지 말고 build secret mount를 사용한다. [Docker build secrets](https://docs.docker.com/build/building/secrets/)

writable layer의 삭제는 같은 Docker 컨테이너의 단순 stop/start와 다르다. volume의 별도 수명도 백업을 보장하지 않는다. [Docker storage](https://docs.docker.com/engine/storage/)

bind mount의 기본 쓰기 권한은 host 파일에도 영향을 준다. 읽기만 필요한 경로는 read-only 사용을 검토한다. [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)

`ulimit -n`은 현재 shell의 한도이며 다른 서비스 프로세스의 실제 한도와 다를 수 있다. `1024`는 예시이지 고정 기본값이 아니다. `/proc`, `lsof`, `ss`의 세부 정보는 권한과 namespace에 따라 달라진다. `kill`은 관찰 명령이 아니라 상태를 바꾼다. exit code 하나만으로 OOM이나 signal 원인을 확정하지 않는다.

## LLM in Practice

### 상황

가상의 API 컨테이너에서 지연 증가와 재시작이 함께 보인다. CPU throttling, memory OOM, FD 누수, 잘못된 bind를 분리해 첫 조사 순서를 만든다. 실제 장애나 모델 실행 결과가 아닌 작성 예시다.

### LLM에 줄 맥락

익명화한 시간대별 CPU·memory·FD 수, requests/limits, exit reason, 재시작 횟수, listen 주소, DNS 결과, 이전 로그를 준다. 수집하지 못한 값은 빈 값이 아닌 “미확인”으로 표시한다. 비밀·내부 주소·사용자 데이터는 제거한다.

### 예시 프롬프트

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 API 컨테이너의 지연 증가와 재시작을 조사한다.
    관측값: [시간대별 CPU·메모리·FD 수·exit reason·로그].
    설정: [requests/limits·restart policy·listen 주소·DNS 결과].
    미수집 항목은 미확인으로 표시했고 민감정보는 제거했다.
    [요청]
    관측 사실, 가정, 누락 증거를 먼저 분리하라.
    CPU throttling, OOM, FD 누수, bind/DNS 문제를 비교하라.
    원인별 반증 가능한 가설과 읽기 전용 확인 순서를 제안하라.
    [출력]
    가설 / 근거 / 반증 조건 / 다음 명령 / 기대 관측값 표를 작성하라.
    재시작·limit 변경·kill 같은 변경은 실행하지 말고 별도 제안하라.
    [검증]
    실제 namespace·cgroup·권한·버전에서 해석 가능한지 표시하라.
    exit code만으로 원인을 단정하지 말고 공식 문서와 로그로 교차 검증하라.
    사람이 결과를 검토한 뒤 격리 환경의 후속 실험을 결정한다.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    Investigate higher latency and restarts in a hypothetical API container.
    Observations: [CPU, memory, FD count, exit reason, and logs over time].
    Configuration: [requests/limits, restart policy, listen address, DNS results].
    Missing observations are unknown. Sensitive information has been removed.
    [Task]
    Separate observed facts, assumptions, and missing evidence first.
    Compare CPU throttling, OOM, FD leaks, and bind or DNS issues.
    Give falsifiable hypotheses and an ordered set of read-only checks.
    [Output]
    Create a table: hypothesis / evidence / disproof / next command / expected observation.
    Do not run restarts, limit changes, or kill commands. List changes as separate proposals.
    [Checks]
    State whether each check applies to the actual namespace, cgroup, permissions, and version.
    Do not infer a cause from the exit code alone. Cross-check official docs and logs.
    A person reviews the result before choosing follow-up experiments in an isolated environment.
    ```

### 기대 출력

가설과 필요한 관측이 연결된 조사 표, 안전한 읽기 순서, 미확인 조건, 변경 전 승인·실험이 필요한 항목 목록.

### LLM이 틀릴 수 있는 점

exit 137을 모두 OOM으로 단정하거나 CPU 사용률과 throttling을 혼동할 수 있다. host의 loopback·메모리를 컨테이너 상태로 오해하거나 원인 조사 없이 limit만 올리라고 할 수 있다.

### 검증 방법

실제 설정, cgroup 통계, process 상태, listen socket, 시간대가 일치하는 로그·이벤트를 확인한다. 명령의 namespace와 권한을 검토하고 누락 증거를 수집한다. 사람의 검토 뒤 격리 환경에서 가설을 반증한다. 이 문서에서는 명령·모델을 실행하지 않았다.

## 관련 주제

- [플랫폼 인프라 학습 지도](index.md)
- [Kubernetes Core](kubernetes-core.md)
- [Kubernetes 운영과 트러블슈팅](kubernetes-operations.md)
