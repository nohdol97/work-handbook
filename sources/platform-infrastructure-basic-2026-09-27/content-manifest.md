---
items:
- id: PIS-00-01
  knowledge: 'Basic 학습 자료의 범위와 깊이: Chapter 1~3만 완료'
  kind: constraint
- id: PIS-01-01
  knowledge: Linux Process
  kind: concept
- id: PIS-01-02
  knowledge: CPU / Memory
  kind: concept
- id: PIS-01-03
  knowledge: File / File Descriptor
  kind: concept
- id: PIS-01-04
  knowledge: Linux Networking
  kind: concept
- id: PIS-01-05
  knowledge: Signal / Process Lifecycle
  kind: concept
- id: PIS-01-06
  knowledge: Linux Namespace
  kind: concept
- id: PIS-01-07
  knowledge: cgroup
  kind: concept
- id: PIS-01-08
  knowledge: Container Fundamentals
  kind: concept
- id: PIS-01-09
  knowledge: Container Image / OCI
  kind: concept
- id: PIS-01-10
  knowledge: Container Networking
  kind: concept
- id: PIS-01-11
  knowledge: Container Storage
  kind: concept
- id: PIS-01-12
  knowledge: Linux / Container Troubleshooting
  kind: troubleshooting
- id: PIS-02-01
  knowledge: '아키텍처: API Server·Scheduler·Controller Manager·etcd와 kubelet·runtime·kube-proxy 및 desired state 흐름'
  kind: concept/example/constraint
- id: PIS-02-02
  knowledge: '선언형 API: Resource와 Object, YAML 네 필드 및 spec/status 비교'
  kind: concept/example/constraint
- id: PIS-02-03
  knowledge: 'Pod: 공유 네트워크·IP·lifecycle·restartPolicy·init·sidecar'
  kind: concept/example/constraint
- id: PIS-02-04
  knowledge: 'ReplicaSet·Deployment: 개수 유지·점진 업데이트·rollback·revision'
  kind: concept/example/constraint
- id: PIS-02-05
  knowledge: 'StatefulSet: stable identity·Pod별 저장소·시작 순서와 운영 예시'
  kind: concept/example/constraint
- id: PIS-02-06
  knowledge: 'DaemonSet·Job·CronJob: 노드 agent·일회성 작업·예약 실행'
  kind: concept/example/constraint
- id: PIS-02-07
  knowledge: 'Service: selector·ClusterIP·NodePort·LoadBalancer·Headless'
  kind: concept/example/constraint
- id: PIS-02-08
  knowledge: 'Ingress·Gateway API: host/path routing·controller·TLS termination'
  kind: concept/example/constraint
- id: PIS-02-09
  knowledge: 'ConfigMap·Secret: 비민감/민감 설정·환경변수·파일 마운트·image 분리'
  kind: concept/example/constraint
- id: PIS-02-10
  knowledge: 'Storage: Volume·PV·PVC·StorageClass·dynamic provisioning'
  kind: concept/example/constraint
- id: PIS-02-11
  knowledge: 'Scheduling: nodeSelector·affinity·taint/toleration·topology spread'
  kind: concept/example/constraint
- id: PIS-02-12
  knowledge: 'Resource management: request·limit·CPU throttling·OOM·QoS'
  kind: concept/example/constraint
- id: PIS-02-13
  knowledge: 'Health checks: liveness/readiness/startup 및 모델 로딩 사례'
  kind: concept/example/constraint
- id: PIS-02-14
  knowledge: 'Networking: Pod·Service·DNS·CNI·kube-proxy 및 외부→process 흐름'
  kind: concept/example/constraint
- id: PIS-03-01
  knowledge: HA·Node Pool·Failure Domain·AZ 분산
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-02
  knowledge: etcd 상태·과반수·백업 복구
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-03
  knowledge: CNI·Calico·Cilium·Overlay·Routing·eBPF
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-04
  knowledge: CSI·StorageClass·Volume Attach·AZ 제약
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-05
  knowledge: CoreDNS 이름해석·진단·스케일
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-06
  knowledge: HPA·VPA·Cluster Autoscaler·KEDA·스케일 지연
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-07
  knowledge: PDB·Anti-Affinity·Topology Spread·Graceful Termination
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-08
  knowledge: Cordon·Drain·Node Pressure·Eviction·교체
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-09
  knowledge: Control Plane·Worker 순차 업그레이드·Version Skew
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-03-10
  knowledge: Pod·리소스·네트워크·DNS·스토리지 계층별 장애 진단
  kind: 개념·흐름·예시·운영·장애·제약
- id: PIS-04-01
  knowledge: 현재 완료 상태와 Chapter4~15 후속 커리큘럼
  kind: curriculum
---

# 추출 목록

원문 행 번호는 source.md의 ORIGINAL SOURCE START 경계 다음부터 센다. 각 절의 예시·명령·숫자·제약을 함께 추적한다.

| ID | 원문 행 | 의미·세부 범위 | 정규 목적지 |
|---|---|---|---|
| PIS-00-01 | 1–8 | Basic 학습 자료의 범위와 깊이: Chapter 1~3만 완료; 플랫폼 엔지니어 핵심개념 중심; 구축경험이나후속AI serving학습완료를뜻하지않음 | platform-infrastructure/index.md |
| PIS-01-01 | 11–167 | Linux Process; Process는 실행중인 프로그램; python app.py; PID, ps aux의 root 1/init,user1523/python,user1601/nginx, kill1523; bash부모/python자식과PPID,ps-ef의1000/900,1200/1000; Running CPU대기포함,Sleeping I/O,Stopped,Zombie 종료결과미회수 및CPU미사용; exit0/비0,ls /tmp와/not-exist echo$?; /proc/1200/status,cmdline,fd; Pod→Container→vLLM process 종료/exit/runtime/Kubernetes재시작과 정책조건. | platform-infrastructure/linux-containers.md |
| PIS-01-02 | 168–306 | CPU / Memory; CPU 코드실행,JSON/압축/암호화/대량연산/LLMinference일부 CPU-bound; I/O-bound DB/API/file/network/disk대기;8cores와scheduler시분할;RAM code/cache/request/modeldata;Swap RAM부족시disk와성능저하;OOM과LinuxOOMkiller;YAML request memory2Gi limit4Gi;request는배치기준자원량이지메모리사전확보보장아님교정;memory증가→limit→OOMKilled단순흐름 및반응적강제;CPUlimitthrottling,CPU초과즉시kill아님. | platform-infrastructure/linux-containers.md |
| PIS-01-03 | 307–446 | File / File Descriptor; FD는프로세스별파일/socket/pipe번호;0stdin1stdout2stderr기본관례; python app.py > output.log;FD3config.yaml4log.txt5/6/7clientTCP;ulimit-n예1024;FDlimit와Too many open files;DB/networkclose누락→누수→FD고갈→살아도신규연결실패;lsof-p<PID>,ls/proc/<PID>/fd;APIclient/DB/Redis/log모두FD. | platform-infrastructure/linux-containers.md |
| PIS-01-04 | 447–615 | Linux Networking; IP어느장비/port어느프로그램기초모형10.0.0.10:8080;socketendpoint IP+port+protocol;TCP연결신뢰순서재전송HTTP/DB,UDP비연결순서전송미보장DNS,UDP빠름보장아님;SYN/SYN-ACK/ACK;127.0.0.1현재namespace loopback과0.0.0.0모든IPv4interface;containerloopbackbind외부접근불가;DNSapi.example.com→10.0.0.20,dig;route질문iproute defaultvia10.0.0.1;CIDR10.0.0.0/24 PodCIDR ServiceCIDR;NATcontainer10.1.0.5→node192.168.0.10;ipaddr,iproute,ss-lntp,dig,curlhttp://server:8080;앱/port/bind/DNS/route/firewallNetworkPolicy검사. | platform-infrastructure/linux-containers.md |
| PIS-01-05 | 616–751 | Signal / Process Lifecycle; Signal제어메시지;kill<PID>기본SIGTERM정상종료요청;새요청중단/기존요청처리/DB정리/fileflush/exit;kill-9SIGKILL정리불가;Ctrl+C SIGINT;API처리중즉시종료요청실패;K8s삭제→TERM→graceperiod→필요KILL 일반모형preStop/STOPSIGNAL예외교정;container첫processPID1과handler/signalforward/reaping중요,PIDnamespaceinit특수규칙. | platform-infrastructure/linux-containers.md |
| PIS-01-06 | 752–858 | Linux Namespace; namespace는process가보는Linux환경격리;PIDcontainer1python20worker/host12345python12380worker;networkIP/interface/routes/port격리→동일host동일port가능(별도namespace전제);mountmount상태,UTShostname;A/Bcontainers각PID/network/mount;VMguestOSvscontainerhostkernel공유;namespace무엇을봄/cgroup얼마나사용. | platform-infrastructure/linux-containers.md |
| PIS-01-07 | 859–953 | cgroup; CPU/memory자원제어측정;A최대1CPU B2CPU;CPUthrottling;A memory2GB초과OOM종료가능;cgroup1CPU2GB+namespace+filesystem;YAML cpu1 memory2Gi;K8slimit→runtime→Linuxcgroup실제집행;GB와GiB동일아님;memory.max회수실패조건/즉시항상OOM아님. | platform-infrastructure/linux-containers.md |
| PIS-01-08 | 954–1083 | Container Fundamentals; Container격리환경process실행;VMguestOS/ContainerhostLinuxkernel공유보통가벼움시작빠름;docker run nginx→nginxprocess;Docker build/run/stop/push/pull;containerdlifecycle,Kubernetes→containerd→runc→LinuxProcess대표경로OCIimage/runtime공통표준;runc저수준runtime;Image→create→start→process→stop→exit;mainexitcontainerexit;Podcontainerapp;CrashLoopBackOff반복종료후재시작backoff상태/정책조건. | platform-infrastructure/linux-containers.md |
| PIS-01-09 | 1084–1259 | Container Image / OCI; Image실행package Pythonruntime/app/libraries/config;BaseLinux→Python→libraries→appLayers;Dockerfile FROMpython3.12 WORKDIR/app COPY.. RUNpipinstall-rrequirements.txt CMDpythonapp.py;unchangedlayercache조건;registryDockerHub/ECR/ArtifactRegistry/GHCR;buildpushpullrun;tagsmyapp1.0/latest mutable/digestsha256abc123content固定예시유효digest아님;multistagecompilerbinarybuild/runtimebinary분리크기감소;Pod생성node선택imagepullcreateprocess;ImagePullBackOff이름/tag/auth/network실패backoff. | platform-infrastructure/linux-containers.md |
| PIS-01-10 | 1260–1364 | Container Networking; Networknamespace별IP가능 A172.18.0.2 B172.18.0.3;veth가상랜선pair host연결;LinuxbridgeA/Bhost;docker run-p8080:80nginx host8080→container80;external→host8080→NAT→container80조건;같은network통신정책조건 Compose redis6379 name;K8sPodIP+CNI공유namespace모델;publish모든interface외부노출주의와localhost범위제한예시. | platform-infrastructure/linux-containers.md |
| PIS-01-11 | 1365–1464 | Container Storage; writablelayer컨테이너삭제재생성시손실가능단순stop/start와구분;bindmountHost/data→container/app/data docker run-v/data:/app/data myapp;runtimevolume별도persistentdata PostgreSQL/Redis/file;앱재생성가능persistentdata분리stateless권장;Pod→PVC→persistentstorage PV/PVC/StorageClass;mountwritehost영향및backup별도. | platform-infrastructure/linux-containers.md |
| PIS-01-12 | 1465–1628 | Linux / Container Troubleshooting; CPU느림처리량감소고사용률 top/psaux/throttling;memory갑작종료재시작OOMKilled free-h kubectldescribepod;df-h disk100%log/DBwrite/container실패;FD Too manyopenfiles 신규연결실패ulimit-n/lsof;DNS→IP→port→application dig/curl/ss/iproute;crashExitCode/log/OOM/signal;전체alive CPUmemory disk FD port DNSnetwork logexit순서;container image/resource/restart/volume추가;전체Process CPUmemoryFDnetworksignalnamespacecgroupcontainerimagestorage순서와LinuxProcess+namespace+cgroup+filesystem요약. | platform-infrastructure/linux-containers.md |
| PIS-02-01 | 1631–1802 | 아키텍처: API Server·Scheduler·Controller Manager·etcd와 kubelet·runtime·kube-proxy 및 desired state 흐름; Kubernetes는 여러 서버 컨테이너 desired state 유지; nginx 3개 예시와 현재2→1개보충; cluster=Control Plane+Worker; API Server 중앙입구와 kubectl get pods 요청/응답; Scheduler Node선택; Controller Manager 상태조정; etcd cluster상태저장; worker kubelet agent→containerd runtime→container실행; kube-proxy Service 네트워크; kubectl apply→API→etcd→Scheduler→kubelet→runtime→container 흐름 및 지속조정. | platform-infrastructure/kubernetes-core.md |
| PIS-02-02 | 1803–1909 | 선언형 API: Resource와 Object, YAML 네 필드 및 spec/status 비교; 선언형 YAML replicas:3; Resource 종류 Pod/Deployment/Service/ConfigMap/Secret; my-api Deployment Object; apiVersion apps/v1, kind Deployment, metadata.name my-api, spec.replicas3 조각; spec desired vs status current; kubectl apply -f deployment.yaml→API Object→etcd→controller spec확인→상태조정. | platform-infrastructure/kubernetes-core.md |
| PIS-02-03 | 1910–2017 | Pod: 공유 네트워크·IP·lifecycle·restartPolicy·init·sidecar; Pod는 하나이상container 최소실행단위; 보통 app1개 또는 app+sidecar; 네트워크와일부자원공유/localhost; Pod A10.244.1.10 B10.244.2.15; 재생성IP변경으로Service사용; Pending→Running→Succeeded/Failed; disposable; restart Always/OnFailure/Never; Init가main전설정파일준비; sidecar로그수집/proxy. | platform-infrastructure/kubernetes-core.md |
| PIS-02-04 | 2018–2097 | ReplicaSet·Deployment: 개수 유지·점진 업데이트·rollback·revision; ReplicaSet N유지,3목표에2면1생성4면1제거; Deployment→ReplicaSet→Pod; 직접RS보다Deployment; 배포/업데이트/롤백; v1v1v1→v2v1v1→v2v2v1→v2v2v2 rolling예시; 문제시이전version rollback; Revision1imagev1/2v2/3v3. 원문배포변경마다revision표현은canonical에서Podtemplate변경조건으로보완. | platform-infrastructure/kubernetes-core.md |
| PIS-02-05 | 2098–2171 | StatefulSet: stable identity·Pod별 저장소·시작 순서와 운영 예시; StatefulSet Pod고유정체성/저장소; Deployment상호대체가능stateless; postgres-0/1/2 및 db-1재생성같은이름; db-0→Volume0 db-1→Volume1 db-2→Volume2; orderedstartup db0→db1→db2; PostgreSQL/Kafka/RedisCluster/ZooKeeper계열; Operator함께사용가능. | platform-infrastructure/kubernetes-core.md |
| PIS-02-06 | 2172–2223 | DaemonSet·Job·CronJob: 노드 agent·일회성 작업·예약 실행; DaemonSet각Node Pod,로그수집/모니터링/networkagent; Job완료작업 데이터마이그레이션/배치/일회성파일변환/DB초기화; CronJob정기Job 매일새벽2시백업/매시간통계집계. | platform-infrastructure/kubernetes-core.md |
| PIS-02-07 | 2224–2318 | Service: selector·ClusterIP·NodePort·LoadBalancer·Headless; PodIP변경문제와Service안정접점 Client→Service→A/B/C; labelselector app=my-api; ClusterIP내부,NodePort NodeIP:30080→Service→Pod,LoadBalancer Internet→CloudLB→Service→Pods; Headless가상IP없이개별Pod발견 StatefulSet/DBcluster/Kafka. | platform-infrastructure/kubernetes-core.md |
| PIS-02-08 | 2319–2394 | Ingress·Gateway API: host/path routing·controller·TLS termination; Ingress외부HTTP/HTTPS 목적Service라우팅; host api.example.com→API/web.example.com→Web, path example.com/api→API /web→Web; resource만으로처리불가controller필요; resource→controller→Service→Pod; TLStermination ClientHTTPS→Ingress→HTTP또는HTTPS→Service→Pod; Gateway→HTTPRoute→Service; Service접점vsIngress목적지. | platform-infrastructure/kubernetes-core.md |
| PIS-02-09 | 2395–2455 | ConfigMap·Secret: 비민감/민감 설정·환경변수·파일 마운트·image 분리; Image와설정분리; ConfigMap비민감 APP_ENV=production LOG_LEVEL=info API_URL=http://backend; Secret민감key DB_PASSWORD/API_KEY/TOKEN; Secret완벽한보안저장소아님 Vault/ExternalSecrets조합가능; env DB_HOST=postgres DB_PASSWORD=*** 예시/filemount ConfigMap→/app/config.yaml; image코드 vs config환경설정; 같은image dev/staging/production재사용. | platform-infrastructure/kubernetes-core.md |
| PIS-02-10 | 2456–2551 | Storage: Volume·PV·PVC·StorageClass·dynamic provisioning; Volume Pod저장소; PV PersistentVolume 실제storage표현 EBS/NFS/cloudDisk; PVC PersistentVolumeClaim 요청; Pod→PVC→PV→Disk; StorageClass종류 fast-ssd/standard/high-iops; dynamic PVC생성→SC→disk자동생성→PV→binding; postgres0→PVC0→Disk0 및 postgres1→PVC1→Disk1. | platform-infrastructure/kubernetes-core.md |
| PIS-02-11 | 2552–2616 | Scheduling: nodeSelector·affinity·taint/toleration·topology spread; Scheduler신규PodNode선택; nodeSelector gpu:true YAML; nodeAffinity required필수/preferred선호; PodAffinity근접/AntiAffinity분리 A→Node1 B→Node2 C→Node3; taintNode제한/tolerationPod허용 GPUNode사용; topologySpread Node/AZ분산; selector/affinity 어디갈지 vs taint/toleration 누가올지. | platform-infrastructure/kubernetes-core.md |
| PIS-02-12 | 2617–2724 | Resource management: request·limit·CPU throttling·OOM·QoS; request예약배치기준 cpu500m memory1Gi; limit cpu1 memory2Gi; CPUrequest0.5 limit1; CPUlimit초과throttling; memory초과OOM→종료→OOMKilled가능; Node가용2CPU Podrequest3불가; QoS Guaranteed/Burstable/BestEffort; 원문Guaranteed단순표현은canonical에서모든containerCPUmemory양수request=limit로보완; request<limit/일부만설정Burstable,없음BestEffort. | platform-infrastructure/kubernetes-core.md |
| PIS-02-13 | 2725–2790 | Health checks: liveness/readiness/startup 및 모델 로딩 사례; Liveness살아있는가 실패시containerrestart가능; Readiness요청준비 실패시Pod살아있되Service대상제외; Startup느린앱초기화 vLLM→ModelLoad→GPUMemory준비→몇분뒤Ready; startup완료전liveness대기; 시작완료/요청준비/생존구분. | platform-infrastructure/kubernetes-core.md |
| PIS-02-14 | 2791–2890 | Networking: Pod·Service·DNS·CNI·kube-proxy 및 외부→process 흐름; Pod↔Pod/Service/DNS; A10.244.1.10 B10.244.2.20 예시; CNI(ContainerNetworkInterface)IP/Pod간연결 Calico/Cilium; ClientPod→Service→A/B/C; Service DNS http://my-api:8080/CoreDNS주소변환; kube-proxy Service→Pod네트워크구성; Internet→Ingress→Service→Pod→Container→Process; 역할분리. | platform-infrastructure/kubernetes-core.md |
| PIS-03-01 | 2893–2992 | HA·Node Pool·Failure Domain·AZ 분산; 서버 1대 장애에도 서비스 지속 목표; 단일 Control Plane SPOF와 다중 HA; EKS 등 관리형 운영 분담; Worker A/B/C 각각 API Pod; General=Backend/GPU=vLLM/Batch=Job Node Pool; Failure Domain 분산; AZ-A Node1/PodA·AZ-B Node2/PodB; 각 AZ에 General·GPU Node 설계 예 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-02 | 2993–3068 | etcd 상태·과반수·백업 복구; 클러스터 기억장치; Pod·Deployment·Service·ConfigMap·Secret·클러스터 설정 저장; API Server가 etcd 통신; 장애시 새 Pod/Deployment/Service 변경 영향; 3멤버 중2 quorum; 3/5 홀수멤버; 정상→snapshot→장애→restore; EKS 관리형 책임 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-03 | 3069–3169 | CNI·Calico·Cilium·Overlay·Routing·eBPF; CNI Container Network Interface; Pod생성→IP할당→Pod통신; Calico 네트워크/routing/NetworkPolicy; Cilium eBPF networking/security/observability; Overlay가상계층→Host와 Routed PodIP→routing→다른NodePod 비교; eBPF Linux kernel 처리·관측 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-04 | 3170–3281 | CSI·StorageClass·Volume Attach·AZ 제약; CSI Container Storage Interface; AWS EBS/NFS/Ceph/Google Persistent Disk/Azure Disk; Pod→PVC→StorageClass→CSI Driver→Storage; EBS/EFS/Ceph driver; NodeA scheduling→EBSattach→containermount; Pending/ContainerCreating시 driver/storage/권한/AZ/attach; Volume AZ-A·Pod AZ-B 부착 불가 가능 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-05 | 3282–3365 | CoreDNS 이름해석·진단·스케일; CoreDNS Service이름→IP; APIPod→redis이름→CoreDNS→RedisServiceIP→Service→Pod; 같은namespace redis/postgres/my-api·다른namespace redis.cache; IP성공·이름실패DNS가설; nslookup postgres/dig postgres/kubectl get pods -n kube-system; Pod/요청증가에replica/resource고려 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-06 | 3366–3509 | HPA·VPA·Cluster Autoscaler·KEDA·스케일 지연; HPA Pod수 CPU/Memory/custommetric 예API3→6; VPA CPUrequest500m/Memory1Gi→1/2Gi; ClusterAutoscaler Node수 예HPA10Pod→자원부족Pending→Node추가; traffic→HPA→Pod→Node자원부족→CA→Node→배치; KEDA Kafkalag/queue량→consumerPod; 감지/생성/imagepull/start/readiness까지지연·vLLMmodelload추가 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-07 | 3510–3602 | PDB·Anti-Affinity·Topology Spread·Graceful Termination; Reliability 장애·배포시유지; PDBminAvailable2/drain; AntiAffinity NodeA/B/C에API1/2/3; TopologySpread AZ-A/B/C각2; graceful종료 신규traffic차단→SIGTERM→기존요청→종료; replica+분산+PDB+readiness+graceful조합 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-08 | 3603–3735 | Cordon·Drain·Node Pressure·Eviction·교체; kubectl cordon node-a 신규배치금지/기존유지; kubectl drain node-a 기존도비움; MemoryPressure/DiskPressure/PIDPressure; image/log/ephemeralstorage디스크원인; 자원부족→pressure→eviction→다른Node재배치가능; cloud cordon→drain→제거→생성 교체 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-09 | 3736–3830 | Control Plane·Worker 순차 업그레이드·Version Skew; ControlPlane API Server/Scheduler/ControllerManager/etcd 먼저; 관리형provider역할; Worker하나씩일부씩 cordon→drain→upgrade/replace→재사용; NodeA정상후B정상후C rolling; version skew 허용차이; 현재/목표버전,CNI,CSI,IngressController,deprecatedAPI확인; drain PDB 연결 | platform-infrastructure/kubernetes-operations.md |
| PIS-03-10 | 3831–4111 | Pod·리소스·네트워크·DNS·스토리지 계층별 장애 진단; Pending CPU/Memory/GPU/nodeSelector/taint-toleration/PVC; CrashLoop app/config/secret/DB/명령/liveness·원인아닌결과; OOMKilled limit/leak/사용감소; ImagePull image오타/tag/auth/network; Pod→Service→Ingress; PodIP/Service/Endpoint/CNI/NetworkPolicy/Port; Service8080-App8000예; 10.0.0.10:5432성공/postgres:5432실패; PVC/PV/CSI/attach/AZ; affinity/selector/taint/anti-affinity; 0/5nodes; getpods→describe→Events→logs→자원→scheduling→networkDNS→storage; ContainerCreating image/storage 가능; HA→etcd→CNI/CSI/DNS→scaling→reliability→node→upgrade→troubleshoot 전체 흐름 | platform-infrastructure/kubernetes-operations.md |
| PIS-04-01 | 4112–4132 | 현재 완료 상태와 Chapter4~15 후속 커리큘럼; 1Linux/network/container,2Kubernetes core,3production개념완료;Redis→PostgreSQL→Kafka→vLLM→LiteLLM→GPU→security→CI/CD/Helm/Argo/GitOps→Terraform/IaC→multitenancy/quota/cost→IDP→end-to-end AI미학습 | platform-infrastructure/index.md |
