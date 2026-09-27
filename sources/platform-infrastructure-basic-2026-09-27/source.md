<!-- 반입 기록
범위: 업로드 Markdown 전체 1~4132행, Chapters 1~3 및 후속 학습 목차.
읽기: 원문 전체를 장별 담당자가 읽고 개인정보·한영 의미를 검토했다. 접근하지 못한 본문과 발견된 실제 민감정보 없음.
한계: Basic 개념 학습 자료. 실제 Linux·Docker·Kubernetes 실행이나 AI serving 구축을 증명하지 않음.
원본 bytes: 55197; SHA-256: 9c5236418f74d28e84794d8a98e66742afbb000835354e2039a2212a953ae536
정규화: ledger의 행 끝 space/tab만 제거하며 원문 내용·행 순서를 보존한다.
whitespace_restoration: [{"line": 3, "removed": "  "}, {"line": 4, "removed": "  "}]
-->
<!-- ORIGINAL SOURCE START -->
# Platform / Infrastructure / AI Serving — Basic Study Notes

> 범위: 이 세션에서 학습 완료한 Chapter 1~3
> 수준: Basic — 플랫폼 엔지니어가 반드시 알아야 할 핵심 개념 중심
> 다음 추출 요청부터는 Chapter 4부터 이어서 정리

---

# Chapter 1. Linux, Networking, Containers

## 1.1 Linux Process

Linux에서 **Process = 실행 중인 프로그램**이다.

예:

```bash
python app.py
```

프로그램이 실행되면 메모리에 올라가고 Linux가 하나의 Process로 관리한다.

### PID

각 Process에는 고유한 번호인 **PID(Process ID)** 가 있다.

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

프로세스 종료 → Exit Code → Container Runtime 감지 → Kubernetes 재시작 흐름으로 연결된다.

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

- `request` = 최소한 확보하고 싶은 자원
- `limit` = 최대 사용 가능량

Memory limit 초과 시 흔히:

```text
OOMKilled
```

흐름:

```text
Application memory 증가
        ↓
Container memory limit 초과
        ↓
Process 종료
        ↓
Pod에서 OOMKilled 확인
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

Kubernetes memory limit 초과
→ OOMKilled

Kubernetes CPU limit 초과
→ CPU throttling
```

---

## 1.3 File / File Descriptor

Linux에서는 프로세스가 파일이나 네트워크 연결을 사용할 때 **File Descriptor(FD)** 라는 번호로 관리한다.

### stdin / stdout / stderr

모든 프로세스는 기본적으로:

```text
0 = stdin
1 = stdout
2 = stderr
```

를 가진다.

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
- 빠름
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
- 현재 장비 자기 자신에서만 접근 가능

**0.0.0.0**
- 모든 Network Interface에서 요청을 받겠다는 의미

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
UDP = 빠르고 단순

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

그래서 같은 Host 안의 여러 Container가 같은 Port 번호를 각각 사용할 수 있다.

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
Memory limit 초과
↓
OOM
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

CrashLoopBackOff는 결국 애플리케이션 프로세스가 계속 종료되고 Container가 재시작되는 상황이다.

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

Image Pull 실패 시:

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

같은 Network에 있는 Container끼리는 통신할 수 있다.

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

# Chapter 2. Kubernetes Core

## 2.1 Kubernetes Architecture

Kubernetes는:

> 여러 서버에서 Container를 원하는 상태로 계속 유지해주는 시스템

이다.

예:

```text
"nginx 3개를 항상 실행해"
```

```text
3개 실행 중 → 정상
2개만 실행 중 → 하나 다시 생성
```

### 큰 구조

```text
Kubernetes Cluster
├─ Control Plane
└─ Worker Node
```

### Control Plane

핵심 구성요소:

```text
API Server
Scheduler
Controller Manager
etcd
```

#### API Server

Kubernetes의 중앙 입구.

```bash
kubectl get pods
```

대략:

```text
kubectl
↓
API Server
↓
Cluster 정보 반환
```

#### Scheduler

새 Pod를 어느 Worker Node에 실행할지 결정.

#### Controller Manager

현재 상태를 원하는 상태로 맞춘다.

```text
Desired State = Pod 3개
Current State = Pod 2개
↓
Pod 하나 더 생성
```

#### etcd

Cluster 상태 데이터를 저장하는 DB.

### Worker Node

실제 Container가 실행되는 서버.

대표 구성:

```text
kubelet
container runtime
kube-proxy
```

#### kubelet

각 Node의 agent.

```text
API Server
↓
kubelet
↓
containerd
↓
Container 실행
```

#### Container Runtime

실제로 Container 실행.

대표적으로 containerd.

#### kube-proxy

Service 트래픽 전달을 위한 네트워크 구성을 담당.

### 전체 흐름

```text
kubectl apply
↓
API Server
↓
etcd에 상태 저장
↓
Scheduler가 Node 선택
↓
해당 Node의 kubelet
↓
container runtime
↓
Container 실행
```

Controller는 계속 Desired State를 확인한다.

### 핵심 정리

```text
Control Plane
= Cluster 관리

Worker Node
= 실제 Container 실행
```

Control Plane:

```text
API Server
→ 모든 요청의 중심

Scheduler
→ Pod를 어느 Node에 둘지 결정

Controller Manager
→ Desired State 유지

etcd
→ Cluster 상태 저장
```

Worker:

```text
kubelet
→ Node에서 Pod 관리

container runtime
→ Container 실행

kube-proxy
→ Service Network 처리
```

---

## 2.2 Kubernetes API / Declarative Model

Kubernetes는 보통 원하는 상태를 YAML로 선언하고 Kubernetes가 맞추도록 한다.

### Declarative Model

예:

```yaml
replicas: 3
```

의미:

```text
Pod 3개를 유지해
```

Kubernetes가 계속 Current State를 맞춘다.

### Resource

Kubernetes 관리 대상.

예:

```text
Pod
Deployment
Service
ConfigMap
Secret
```

### Object

Resource를 실제로 하나 생성하면 Kubernetes Object가 된다.

예:

```text
Deployment라는 Resource 종류
↓
my-api라는 실제 Deployment Object
```

### YAML 기본 구조

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-api

spec:
  replicas: 3
```

핵심:

```text
apiVersion
kind
metadata
spec
```

### spec vs status

**spec**
- 원하는 상태
- Desired State

**status**
- 현재 상태
- Current State

Kubernetes는 둘을 계속 비교한다.

```text
spec != status
→ Kubernetes가 다시 맞춘다
```

### 실제 흐름

```bash
kubectl apply -f deployment.yaml
```

```text
YAML
↓
API Server
↓
Kubernetes Object 생성
↓
etcd에 저장
↓
Controller가 spec 확인
↓
실제 상태를 맞춤
```

---

## 2.3 Pod

Pod는 Kubernetes에서 Container를 실행하는 가장 작은 단위다.

> Pod = 하나 이상의 Container를 감싸는 실행 단위

### 보통 Container 1개

```text
Pod
└─ Container
   └─ App
```

### Multi-container Pod

```text
Pod
├─ App Container
└─ Sidecar Container
```

같은 Pod 안의 Container는 네트워크와 일부 리소스를 공유한다.

`localhost`로 서로 통신할 수 있다.

### Pod IP

Pod는 보통 자기 IP를 가진다.

예:

```text
Pod A → 10.244.1.10
Pod B → 10.244.2.15
```

Pod는 재생성될 수 있어 IP가 바뀔 수 있으므로 직접 Pod IP를 의존하지 않고 Service를 사용한다.

### Pod Lifecycle

```text
Pending
↓
Running
↓
Succeeded / Failed
```

Pod는 disposable한 실행 단위다.

### Restart Policy

```text
Always
OnFailure
Never
```

### Init Container

Main Container보다 먼저 실행.

```text
Init Container
↓
설정 파일 준비
↓
Main Container 실행
```

### Sidecar

Main App을 보조하는 Container.

예:

```text
Pod
├─ App
└─ Log collector
```

또는 Proxy.

### 핵심 정리

```text
Pod
= Kubernetes의 최소 실행 단위

Pod 안에는
하나 이상의 Container가 들어감

Pod는 자기 IP를 가질 수 있음

Pod는 영구적이지 않음
→ 언제든 다시 생성 가능

Init Container
→ Main App 전에 준비 작업

Sidecar
→ Main App 보조
```

---

## 2.4 ReplicaSet / Deployment

### ReplicaSet

역할:

```text
Pod를 N개 유지
```

예:

```text
replicas = 3
```

- 2개면 1개 생성
- 4개면 1개 제거

### Deployment

ReplicaSet을 관리하면서 배포/업데이트/롤백을 제공한다.

```text
Deployment
   ↓
ReplicaSet
   ↓
Pod
```

보통 직접 ReplicaSet을 만들기보다 Deployment를 사용한다.

### Rolling Update

예:

```text
v1 v1 v1
↓
v2 v1 v1
↓
v2 v2 v1
↓
v2 v2 v2
```

### Rollback

새 버전 문제 시 이전 버전으로 복구.

### Revision

배포 변경마다 이력이 생긴다.

```text
Revision 1 → image v1
Revision 2 → image v2
Revision 3 → image v3
```

### 핵심 정리

```text
ReplicaSet
= Pod 개수 유지

Deployment
= ReplicaSet을 관리하면서
  배포/업데이트/롤백 제공

Rolling Update
= Pod를 점진적으로 새 버전으로 교체

Rollback
= 이전 버전으로 복구
```

---

## 2.5 StatefulSet

StatefulSet은:

> 각 Pod의 고유한 정체성과 저장공간을 유지해야 하는 경우

에 사용한다.

### Deployment와 차이

Deployment의 Pod는 서로 대체 가능하다.

StatefulSet은:

```text
postgres-0
postgres-1
postgres-2
```

처럼 각 Pod identity가 중요할 수 있다.

### Stable Identity

`db-1`이 죽어도 다시 `db-1`로 만들어지는 식으로 이름과 정체성이 유지된다.

### Persistent Storage

각 Pod별 저장공간을 유지할 수 있다.

```text
db-0 → Volume 0
db-1 → Volume 1
db-2 → Volume 2
```

### Ordered Startup

필요하면 순서대로 시작/종료할 수 있다.

```text
db-0
↓
db-1
↓
db-2
```

### 대표 사용 예

```text
PostgreSQL
Kafka
Redis Cluster
ZooKeeper 계열
```

실제 운영에서는 Operator와 함께 쓰는 경우도 많다.

### 핵심 정리

```text
Deployment
= Pod가 서로 대체 가능
= Stateless 앱에 적합

StatefulSet
= Pod identity 유지
= 각 Pod별 storage 유지
= 순서가 중요한 workload 지원
```

---

## 2.6 DaemonSet / Job / CronJob

### DaemonSet

> 각 Node마다 Pod를 하나씩 실행하고 싶을 때

사용.

대표 용도:
- 로그 수집 agent
- 모니터링 agent
- 네트워크 agent

### Job

> 한 번 실행하고 끝나는 작업

예:

```text
데이터 마이그레이션
배치 처리
일회성 파일 변환
DB 초기화
```

### CronJob

> Job을 정해진 시간마다 반복 실행

예:

```text
매일 새벽 2시 → 백업
매시간 → 통계 집계
```

### 핵심 정리

```text
DaemonSet
= 각 Node에 Pod 실행

Job
= 일회성 작업

CronJob
= 주기적인 Job
```

---

## 2.7 Service

Pod는 재생성 시 IP가 바뀔 수 있다.

Service는:

> 여러 Pod 앞에 고정된 접근 지점을 만들어주는 Kubernetes 리소스

### 기본 구조

```text
Client
  ↓
Service
  ↓
Pod A / Pod B / Pod C
```

### Label Selector

Service는 보통 label selector로 대상 Pod를 찾는다.

예:

```text
Pod A: app=my-api
Pod B: app=my-api
Pod C: app=my-api
```

Service selector:

```text
app=my-api
```

### ClusterIP

Cluster 내부에서만 접근 가능.

### NodePort

Node의 특정 Port를 열어 외부에서 접근.

```text
NodeIP:30080
      ↓
   Service
      ↓
     Pod
```

### LoadBalancer

Cloud Load Balancer와 연결.

```text
Internet
   ↓
Cloud Load Balancer
   ↓
Kubernetes Service
   ↓
Pods
```

### Headless Service

하나의 가상 IP를 주지 않고 개별 Pod 주소를 찾을 수 있게 한다.

주로 StatefulSet, DB Cluster, Kafka 등.

### 핵심 정리

```text
Pod IP는 바뀔 수 있다.

Service
= Pod 앞의 안정적인 접근 지점

ClusterIP
= Cluster 내부용

NodePort
= Node Port를 통해 접근

LoadBalancer
= 외부 Load Balancer 연결

Headless Service
= 개별 Pod 접근이 필요한 경우
```

---

## 2.8 Ingress / Gateway API

Ingress는:

> 외부 HTTP/HTTPS 트래픽을 어떤 Service로 보낼지 결정하는 라우팅 계층

### Host Routing

```text
api.example.com → API Service
web.example.com → Web Service
```

### Path Routing

```text
example.com/api → API Service
example.com/web → Web Service
```

### Ingress Controller

Ingress Resource만으로 실제 트래픽 처리가 되는 것은 아니다.

실제 요청을 처리하는 구현체가 필요하다.

```text
Ingress Resource
↓
Ingress Controller
↓
Service
↓
Pod
```

### TLS Termination

Ingress에서 HTTPS 인증서 처리를 끝낼 수 있다.

```text
Client
  ↓ HTTPS
Ingress
  ↓ HTTP 또는 HTTPS
Service
  ↓
Pod
```

### Gateway API

Ingress보다 더 확장된 최신 Kubernetes Network API.

대략:

```text
Gateway
↓
HTTPRoute
↓
Service
```

### Service와 Ingress 차이

```text
Service
= Pod들을 하나의 안정적인 주소로 묶음

Ingress
= 외부 HTTP 요청을 어떤 Service로 보낼지 결정
```

---

## 2.9 ConfigMap / Secret

애플리케이션 설정값을 Image 안에 직접 넣기보다 Kubernetes에서 분리해 관리할 수 있다.

### ConfigMap

민감하지 않은 일반 설정값.

예:

```text
APP_ENV=production
LOG_LEVEL=info
API_URL=http://backend
```

### Secret

민감한 설정값.

예:

```text
DB_PASSWORD
API_KEY
TOKEN
```

Kubernetes Secret 자체가 완벽한 보안 저장소라는 뜻은 아니다. Production에서는 Vault, External Secrets 같은 도구와 함께 사용할 수 있다.

### Pod에 전달하는 방식

**Environment Variable**

```text
DB_HOST=postgres
DB_PASSWORD=***
```

**File Mount**

```text
ConfigMap
↓
/app/config.yaml
```

### Image와 설정 분리

```text
Container Image
= 애플리케이션 코드

ConfigMap / Secret
= 환경별 설정
```

같은 Image를 dev / staging / production에 재사용할 수 있다.

---

## 2.10 Storage

핵심:

```text
Volume
PV
PVC
StorageClass
```

### Volume

Pod에 붙이는 저장공간.

### PV

PersistentVolume.

> Kubernetes Cluster에서 사용할 수 있는 실제 저장공간

예:

```text
AWS EBS
NFS
Cloud Disk
```

### PVC

PersistentVolumeClaim.

Pod가 필요한 Storage를 요청하는 리소스.

```text
Pod
 ↓
PVC
 ↓
PV
 ↓
Disk
```

```text
PV  = 실제 Storage
PVC = Storage 요청
```

### StorageClass

어떤 종류의 Storage를 만들지 정의.

예:

```text
fast-ssd
standard
high-iops
```

### Dynamic Provisioning

PVC 요청 시 StorageClass를 보고 실제 Disk와 PV를 자동 생성.

```text
PVC 생성
↓
StorageClass 확인
↓
실제 Disk 자동 생성
↓
PV 생성
↓
PVC와 연결
```

### StatefulSet 연결

```text
postgres-0
↓
PVC-0
↓
Disk-0

postgres-1
↓
PVC-1
↓
Disk-1
```

---

## 2.11 Scheduling

Scheduler는 새 Pod를 어느 Node에 배치할지 결정한다.

### Node Selector

특정 label을 가진 Node에만 배치.

```yaml
nodeSelector:
  gpu: "true"
```

### Node Affinity

Node Selector보다 더 유연한 조건.

- `required` = 반드시 만족
- `preferred` = 가능하면 만족

### Pod Affinity

특정 Pod와 가까이 배치.

### Pod Anti-Affinity

특정 Pod끼리 떨어뜨린다.

예:

```text
Pod A → Node 1
Pod B → Node 2
Pod C → Node 3
```

### Taint / Toleration

**Taint**
- Node가 “일반 Pod는 오지 마”라고 제한

**Toleration**
- Pod가 “그 Taint가 있어도 들어갈 수 있어”라고 허용

GPU Node에서 자주 사용.

### Topology Spread

Pod를 여러 Node나 AZ에 골고루 분산.

### 핵심 차이

```text
Node Selector / Node Affinity
→ 이 Pod가 어디로 가야 하는가

Taint / Toleration
→ 이 Node에 누가 들어올 수 있는가

Pod Anti-Affinity
→ 비슷한 Pod를 서로 떨어뜨림
```

---

## 2.12 Resource Management

핵심:

```text
request
limit
```

### Request

> 이 Pod가 최소한 필요로 하는 자원

예:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "1Gi"
```

Scheduler는 이 값을 보고 배치 가능 여부를 판단한다.

### Limit

> Pod가 사용할 수 있는 최대 자원

```yaml
resources:
  limits:
    cpu: "1"
    memory: "2Gi"
```

### CPU

```text
request = 0.5 CPU
limit   = 1 CPU
```

CPU limit 초과:

```text
CPU throttling
```

### Memory

Memory limit 초과:

```text
OOM
↓
Container 종료
↓
OOMKilled
```

### Scheduler는 Request를 본다

Node에 2 CPU가 남았는데 Pod request가 3 CPU라면 그 Node에는 배치할 수 없다.

### QoS Class

대표:

```text
Guaranteed
Burstable
BestEffort
```

Basic 수준 이해:

```text
Guaranteed
→ request와 limit을 명확하게 설정

Burstable
→ 일부 자원만 설정하거나 request < limit

BestEffort
→ request / limit 없음
```

### 핵심 정리

```text
Request
= Scheduler가 보는 최소 필요 자원

Limit
= 실제 사용할 수 있는 최대 자원

CPU limit 초과
→ throttling

Memory limit 초과
→ OOMKilled 가능

QoS
= request / limit 설정에 따른 자원 보호 수준
```

---

## 2.13 Health Checks

핵심:

```text
Liveness Probe
Readiness Probe
Startup Probe
```

### Liveness Probe

> 이 애플리케이션이 살아 있는가?

계속 실패하면 Container를 재시작할 수 있다.

```text
Liveness 실패
→ Container restart 가능
```

### Readiness Probe

> 지금 요청을 받을 준비가 되었는가?

실패하면 Pod를 죽이지 않고 Service 트래픽 대상에서 제외한다.

```text
Readiness 실패
→ Pod는 살아 있음
→ 하지만 요청은 보내지 않음
```

### Startup Probe

시작이 오래 걸리는 앱에서 사용.

예:

```text
vLLM
↓
Model Load
↓
GPU Memory 준비
↓
몇 분 후 Ready
```

Startup 완료 전에는 Liveness 판단을 기다릴 수 있다.

### 핵심 구분

```text
Startup Probe
= 시작은 끝났는가?

Readiness Probe
= 요청 받을 준비가 됐는가?

Liveness Probe
= 앱이 정상적으로 살아 있는가?
```

---

## 2.14 Kubernetes Networking Basics

핵심:

```text
Pod ↔ Pod
Pod ↔ Service
Pod ↔ DNS
```

### Pod-to-Pod

각 Pod가 자기 IP를 가질 수 있다.

```text
Pod A → 10.244.1.10
Pod B → 10.244.2.20
```

CNI가 실제 네트워크 연결을 구현한다.

### CNI

Container Network Interface.

> Pod에 IP를 주고 Pod 간 네트워크를 연결하는 역할

대표:

```text
Calico
Cilium
```

### Pod-to-Service

Pod IP는 바뀔 수 있어 Service를 통해 통신한다.

```text
Client Pod
   ↓
Service
   ↓
Pod A
Pod B
Pod C
```

### Kubernetes DNS

Service에는 DNS 이름이 생긴다.

예:

```text
http://my-api:8080
```

CoreDNS가 Service 이름을 주소로 바꾼다.

### kube-proxy

Service → Pod 트래픽 전달을 위한 네트워크 구성을 담당해온 구성요소.

### 외부 요청까지 연결

```text
Internet
   ↓
Ingress
   ↓
Service
   ↓
Pod
   ↓
Container
   ↓
Process
```

### 핵심 정리

```text
Pod마다 IP를 가질 수 있다.

CNI
= Pod 네트워크와 IP 담당

Service
= 변경되는 Pod들을 고정된 주소로 묶음

CoreDNS
= Service 이름을 주소로 찾음

kube-proxy
= Service → Pod 트래픽 전달 구현
```

---

# Chapter 3. Kubernetes Production Operations

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

# 현재까지 학습 완료 상태

```text
1. Linux, Networking, Containers ✅
2. Kubernetes Core ✅
3. Kubernetes Production Operations ✅
4. Redis for Platform Systems ← 다음
5. PostgreSQL for Platform Systems
6. Kafka for Platform Systems
7. vLLM
8. LiteLLM
9. GPU Infrastructure & Scheduling
10. Platform Security
11. CI/CD, Helm, Argo CD & GitOps
12. Terraform & Infrastructure as Code
13. Multi-tenancy, Quotas & Cost Control
14. Internal Developer Platform / Self-Service
15. End-to-End AI Platform Architecture
```

> 다음 source markdown 추출 요청부터는 **Chapter 4부터 이어서 생성**한다.
