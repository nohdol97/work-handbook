---
items:
- id: AWSC-00-01
  knowledge: 현재세션 압축형AWS과정,중복제거·핵심중심·보충질문·오개념교정 반영. 원문은Terraform/IaC를 다른Platform/Infrastructure세션에서학습했다고밝혀AWS별도장제외.
    이파일은Terraform본문을제공하지않으므로기존핸드북본문범위를자동확대하지않음.
  kind: scope,source-claim
  source_lines: 1–8
  destination: aws-cloud/index.md
- id: AWSC-00-02
  knowledge: 7장압축커리큘럼:AWSFoundation,Networking,ComputeLoadBalancing,StorageDatabase,EKS,AWSManagedServices,AIGPUEndToEnd.
    이자료는1~5장학습내용.
  kind: curriculum
  source_lines: 9–22
  destination: aws-cloud/index.md
- id: AWSC-00-03
  knowledge: 최종요약의Region/AZ·Account/Organizations·IAM/Role/Policy·ARN, VPC→Subnet→Route→IGW/NAT→SG, AMI→LaunchTemplate→ASG→EC2
    및 ALB/NLB→TargetGroup→Application, EBSBlock/EFSShared/S3Object/RDSAuroraDB/ElastiCache, EKSmanagedcontrolplane/nodegroup/VPC
    CNI/LBcontroller/CSI/ECR/PodIdentityIAM 역할연결.
  kind: summary,roles
  source_lines: 1415–1480
  destination: aws-cloud/index.md
- id: AWSC-00-04
  knowledge: 1~5장완료:Foundation/Networking/ComputeLoadBalancing/StorageDatabase/EKS. 다음6장ManagedServices는SQS/SNS/MSK/KMS/SecretsManager/CloudWatch/CloudTrail,
    다음7장AIGPU와최종구조. 후속본문은미제공.
  kind: study-status
  source_lines: 1481–1503
  destination: aws-cloud/index.md
- id: AWSC-01-01
  section: 1.1 Region / Availability Zone
  source_lines: 25-74
  knowledge: Region지리적영역·서울ap-northeast-2 예시와 거리/latency·데이터위치규제·서비스지원·비용 선택기준. AZ독립장애영역/하나이상데이터센터, SeoulA~D도식.
    SingleAZ실패영향과ALB→AZA/B App, SingleRegion+MultiAZ운영패턴.
  kind: concept, comparison, architecture, failure boundary, decision criteria
  destination: aws-cloud/foundations.md
- id: AWSC-01-02
  section: 1.2 AWS Account / Organizations
  source_lines: 75-132
  knowledge: Account는리소스·비용·권한관리경계이며다중Region사용. Org Dev/Staging/Prod/Security/Data계정분리와운영실수격리/권한/비용/보안장점.
    Root일상사용제한,Organizations중앙관리,OU논리그룹,SCP최대허용범위제한과IAM권한부여구분.
  kind: concept, identity, architecture, policy boundary
  destination: aws-cloud/foundations.md
- id: AWSC-01-03
  section: 1.3 IAM User / Role / Policy
  source_lines: 133-216
  knowledge: IAM누가무엇을할수있는가. 고정User,사람SSO/IdentityCenter+Role. s3:GetObject arn:aws:s3:::my-bucket/* JSON
    statement예와Effect/Action/Resource/Condition. Identity→AssumeRole→Role→AWSResource,만료temporarycredentials
    AccessKey/SecretKey/SessionToken/Expiration. Trust주체와Permission행동구분,leastprivilege s3:*Resource:*
    대비특정bucket읽기. PodKubernetesAPI=RBAC 대 S3/SQS/SecretsManager=IAM.
  kind: concept, policy example, credential lifecycle, comparison
  destination: aws-cloud/foundations.md
- id: AWSC-01-04
  section: 1.4 AWS Resource / ARN
  source_lines: 217-234
  knowledge: EC2Instance/S3Bucket/IAMRole/RDSInstance/EKSCluster리소스목록과많은리소스ARN식별,arn:aws:iam::123456789012:role/MyRole
    설명placeholder예.
  kind: concept, identifier, example
  destination: aws-cloud/foundations.md
- id: AWSC-02-01
  section: 2.1 VPC
  source_lines: 237-295
  knowledge: VPC사설네트워크·Region범위,Account→Region→VPC→Subnet→EC2/EKS/RDS.10.0.0.0/16과1/2/3.0/24 subnet. Subnet한AZ,Node와다른네트워크공간,Subnet→Node→Pod
    및여러Node포함,땅/서버비유.
  kind: concept, address example, architecture, misconception
  destination: aws-cloud/networking.md
- id: AWSC-02-02
  section: 2.2 CIDR
  source_lines: 296-344
  knowledge: CIDR주소범위와IPv4 32bit /24앞24고정. /16=65,536,/20=4,096,/24=256,/28=16,/32=1,/0allIPv4,작은prefix넓은범위.
    AWS예약으로 /24실사용251; Node/Pod/ENI/기타AWS주소소비로Node+Pod256계산금지.
  kind: concept, calculation, capacity condition, misconception
  destination: aws-cloud/networking.md
- id: AWSC-02-03
  section: 2.3 Public IP / Private IP
  source_lines: 345-363
  knowledge: Private범위표10.0.0.0~10.255.255.255/8,172.16.0.0~172.31.255.255/12,192.168.0.0~192.168.255.255/16.
    private내부통신/public인터넷통신,private인터넷직접라우팅불가.
  kind: concept, address table, routing boundary
  destination: aws-cloud/networking.md
- id: AWSC-02-04
  section: 2.4 Public / Private Subnet
  source_lines: 364-399
  knowledge: Public/private route구성으로구분. PublicdefaultIGW,직접인터넷 IGWroute/publicIPorEIP/SG조건. Private직접IGW없고필요시defaultNAT.
    PublicALB/NAT 대 PrivateEKSNode/EC2App/RDS/ElastiCache/MSK배치.
  kind: concept, prerequisite, route example, placement
  destination: aws-cloud/networking.md
- id: AWSC-02-05
  section: 2.5 Route Table
  source_lines: 400-433
  knowledge: Destination/Target,10.0.0.0/16local과0.0.0.0/0igw예. local내부/defaultIGWpublic/defaultNATprivateoutbound.
    LongestPrefixMatch구체CIDR우선,route경로대SG허용구분.
  kind: routing rule, example, comparison
  destination: aws-cloud/networking.md
- id: AWSC-02-06
  section: 2.6 Internet Gateway
  source_lines: 434-464
  knowledge: IGW Internet→IGW→VPC,subnet아닌VPCattach. publicdefaultIGW,직접EC2인터넷조건 VPCIGW/RouteTable/PublicIP/SG.
    AZ별이아닌VPC여러publicsubnet공유.
  kind: concept, scope, prerequisite, workflow
  destination: aws-cloud/networking.md
- id: AWSC-02-07
  section: 2.7 NAT Gateway
  source_lines: 465-491
  knowledge: Private→NAT→IGW→Internet outbound가능,인터넷에서private직접시작불가. 일반publicsubnet배치·productionAZ별NAT고려,
    S3/ECR등VPCendpoint NAT우회가능경우.
  kind: concept, direction boundary, placement, alternative
  destination: aws-cloud/networking.md
- id: AWSC-02-08
  section: 2.8 Security Group
  source_lines: 492-533
  knowledge: Resource/ENIstateful방화벽 protocol/port/source·destination, TCP443allIPv4예,허용요청응답자동허용. SGsource참조ALB443Internet→APP8080ALBSG→DB5432APPSG.
    SG대NACL범위ResourceENI/subnet,statefulO/X,allowO/O,explicitdenyX/O표.
  kind: concept, security rule, reference example, comparison table
  destination: aws-cloud/networking.md
- id: AWSC-02-09
  section: 2.9 Multi-AZ VPC 기본 구조
  source_lines: 534-553
  knowledge: VPC AZA/B각publicsubnet ALB/NAT와privatesubnetApplication/EKSNode전체배치도. NAT A/B구분 및 public/private부하진입·outbound·compute위치관계.
  kind: architecture, placement, availability example
  destination: aws-cloud/networking.md
- id: AWSC-03-01
  knowledge: '## 3.1 EC2; EC2 = Elastic Compute Cloud.; > AWS의 가상 서버; 대표 설정:

    - AMI

    - Instance Type

    - VPC

    - Subnet

    - Security Group

    - Storage

    - IAM Role; ### AMI; EC2 생성용 VM 이미지.; ```text

    AMI = VM 전체 이미지

    Docker Image = Container 실행 이미지

    ```; ### Instance Type; CPU / Memory / GPU 등의 하드웨어 사양.; ```text

    t = 범용 / 저비용

    m = General Purpose

    c = Compute Optimized

    r = Memory Optimized

    g / p = GPU

    ```; ### EC2와 Subnet; EC2는 특정 Subnet에 생성되며 Subnet 선택으로 AZ가 결정된다.; ### User Data; 최초 부팅 시 실행할 초기화 Script.;
    ### Public / Private EC2; Public EC2는 IGW/Public IP와 연결될 수 있고, Private EC2는 NAT를 통해 외부로 나갈 수 있다.;
    ### Elastic IP; 고정 Public IPv4가 필요한 경우 사용 가능.; ### IAM Role; Access Key를 코드에 직접 저장하기보다 IAM Role을 통해
    AWS Resource에 접근한다.; ### EKS Node; EKS Worker Node의 실체는 보통 EC2다.'
  kind: 개념·예시·조건
  source_lines: 556–606
  destination: aws-cloud/compute.md
- id: AWSC-03-02
  knowledge: "## 3.2 EBS와 EC2; EBS = Elastic Block Store.; > EC2에 붙이는 Block Storage; ```text\nEC2\n ↓\n\
    EBS\n```; EC2는 Compute, EBS는 Storage다.; EBS는 특정 AZ에 속하므로 EC2와 같은 AZ에서 Attach한다."
  kind: 개념·예시·조건
  source_lines: 610–624
  destination: aws-cloud/compute.md
- id: AWSC-03-03
  knowledge: '## 3.3 Launch Template / Auto Scaling Group; ### Launch Template; EC2 생성 설계도.; 포함 예:

    - AMI

    - Instance Type

    - Security Group

    - IAM Role

    - Storage

    - User Data; ### ASG; Auto Scaling Group.; ```text

    Min 2

    Desired 3

    Max 10

    ```; ```text

    Scale Out = 서버 추가

    Scale In = 서버 제거

    ```; Desired보다 인스턴스가 줄면 새 EC2를 만들어 수를 맞출 수 있다.; Scaling 방식:

    - Metric 기반

    - Target Tracking

    - Scheduled Scaling; Auto Scaling 환경에서는 Application을 Stateless하게 두는 것이 유리하다.; ```text

    Persistent Data → RDS

    Cache / Session → ElastiCache

    Object → S3

    ```'
  kind: 개념·예시·조건
  source_lines: 628–668
  destination: aws-cloud/compute.md
- id: AWSC-03-04
  knowledge: '## 3.4 ALB; ALB = Application Load Balancer.; > HTTP/HTTPS를 이해하는 L7 Load Balancer; 역할:

    - 요청 분산

    - Health Check

    - TLS Termination

    - Host Routing

    - Path Routing; 예:; ```text

    /api/* → api-service

    /admin/* → admin-service

    ```; ### Listener; 어떤 Protocol/Port로 요청을 받을지 정의.; ### Target Group; 실제 Backend Target 묶음.; ### Health
    Check; Unhealthy Target에는 트래픽을 보내지 않는다.; ALB는 Internet-facing 또는 Internal로 사용할 수 있다.'
  kind: 개념·예시·조건
  source_lines: 672–700
  destination: aws-cloud/compute.md
- id: AWSC-03-05
  knowledge: '## 3.5 NLB; NLB = Network Load Balancer.; > TCP / UDP / TLS 중심의 L4 Load Balancer; ```text

    ALB = L7 / HTTP / HTTPS / Path / Host

    NLB = L4 / TCP / UDP / TLS

    ```; 중요:

    > ALB = 외부용, NLB = 내부용으로 구분하는 것이 아니다.; 둘 다 외부/내부 구성 가능하다.'
  kind: 개념·예시·조건
  source_lines: 704–718
  destination: aws-cloud/compute.md
- id: AWSC-03-06
  knowledge: "## 3.6 Kubernetes Service와 ALB/NLB; Kubernetes Service도 Protocol과 Port를 가진다.; 예:; ```yaml\n\
    ports:\n  - port: 80\n    targetPort: 8080\n    protocol: TCP\n```; Service의 핵심 역할:\n> 여러 Pod Replica를\
    \ 하나의 안정적인 Endpoint로 묶고 L4 수준에서 분산한다.; ### 내부 Pod 통신; ```text\nPod\n ↓\nClusterIP Service\n ↓\nPod\
    \ Replicas\n```; ### 외부 HTTP/HTTPS; ```text\nInternet\n ↓\nALB\n ↓\nService\n ↓\nPod Replicas\n```;\
    \ ### TCP/UDP; ```text\nClient\n ↓\nNLB\n ↓\nService\n ↓\nPod Replicas\n```; 최종 정리:; ```text\nService\
    \ = Pod Replica를 안정적인 Endpoint로 묶음\nALB = L7 HTTP/HTTPS 진입점\nNLB = L4 TCP/UDP/TLS 진입점\n```; ### ALB/NLB\
    \ Target; 구성에 따라:; ```text\ninstance target → EC2 Node\nip target → Pod IP\n```; 즉 ALB/NLB가 항상 Node만\
    \ 선택하는 것은 아니다."
  kind: 개념·예시·조건
  source_lines: 722–782
  destination: aws-cloud/compute.md
- id: AWSC-04-01
  knowledge: '## 4.1 EBS; Block Storage.; 대표 용도:

    - EC2 OS Disk

    - Application Disk

    - DB Disk

    - EKS Persistent Volume; 특징:

    - AZ 단위

    - Snapshot 지원

    - IOPS / Throughput 고려; ```text

    IOPS = 초당 I/O 작업 횟수

    Throughput = 초당 전송 데이터 양

    ```'
  kind: 개념·예시·조건
  source_lines: 788–806
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-02
  knowledge: '## 4.2 S3; S3 = Simple Storage Service.; > AWS Object Storage; ```text

    Bucket

    └─ Object

    ```; Object는 Key로 식별한다.; 대표 용도:

    - Dataset

    - Model Artifact

    - CSV / Parquet

    - Logs

    - Backup

    - Image / Video

    - Data Lake; ### Versioning; 같은 Key의 이전 버전을 보존할 수 있다.; ### Lifecycle; 오래된 Object를 다른 Storage Class로
    이동하거나 삭제.; ### Bucket Policy; Bucket 자체에 적용하는 Resource-based Policy.; ```text

    IAM Policy = User / Role 쪽 권한

    Bucket Policy = Bucket 쪽 권한

    ```; ### Bucket 분리 이유; Bucket은 큰 관리/보안 경계다.; - Access Policy

    - Lifecycle

    - Versioning / Replication

    - Encryption

    - 환경 분리

    - 비용/운영 관리; Prefix는 Bucket 내부의 논리적 분류다.; ```text

    Bucket = 큰 관리 / 보안 경계

    Prefix = Bucket 내부 논리적 분류

    ```; ### S3는 파일시스템이 아니다; 기본적으로 API(GetObject / PutObject)로 접근한다.; ### VPC Endpoint; Private Subnet에서
    NAT 없이 S3 접근에 사용할 수 있다.'
  kind: 개념·예시·조건
  source_lines: 810–867
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-03
  knowledge: '## 4.3 EFS; EFS = Elastic File System.; > 여러 EC2/EKS Workload가 동시에 Mount할 수 있는 공유 파일시스템;
    특징:

    - File Storage

    - NFS 기반

    - 여러 AZ Client 접근

    - Mount Target

    - NFS 기본 TCP 2049; 비교:; ```text

    EBS = Block / 서버 디스크

    EFS = Shared File

    S3 = Object / API

    ```; Kubernetes:; ```text

    Pod 전용 Persistent Disk → EBS

    여러 Pod 공유 File System → EFS

    Dataset / Model / Object → S3

    ```'
  kind: 개념·예시·조건
  source_lines: 871–896
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-04
  knowledge: "## 4.4 PostgreSQL 여러 Pod와 EFS; 여러 PostgreSQL Pod가 하나의 EFS `PGDATA`를 공유하면 안 된다.; 잘못된 구조:;\
    \ ```text\n        EFS\n       /   \\\nPostgres A  Postgres B\n```; 일반적 구조:; ```text\nPrimary → PVC\
    \ A → EBS A\nReplica → PVC B → EBS B\n```; 데이터는 PostgreSQL Replication으로 복제한다.; ```text\nPrimary\n\
    \ ↓ WAL Replication\nReplica\n```; EFS는 DB 실시간 데이터 디렉터리보다 Shared File / Dump / Export에 더 적합하고, 백업은\
    \ S3를 많이 고려한다."
  kind: 개념·예시·조건
  source_lines: 900–925
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-05
  knowledge: '## 4.5 RDS; RDS = Relational Database Service.; > AWS Managed 관계형 DB 서비스; 지원 예:

    - PostgreSQL

    - MySQL

    - MariaDB

    - Oracle

    - SQL Server

    - Aurora; RDS는 하나의 DB 엔진이 아니라 여러 엔진을 Managed 형태로 제공하는 서비스다.; ### 직접 PostgreSQL vs RDS; RDS는 OS, DB
    설치, Backup, Patch, Failover, Replication, Storage 운영 부담을 상당 부분 줄인다.; ### DB Subnet Group; RDS가 배치될
    수 있는 Private Subnet 집합.; ### Security Group; 예:; ```text

    5432 ← APP-SG

    ```; ### Endpoint; Application은 DB IP가 아니라 Endpoint를 사용한다.; ### Multi-AZ; ```text

    Multi-AZ = High Availability

    ```; ### Read Replica; ```text

    Read Replica = Read Scaling

    ```; ### Backup; - Automated Backup

    - Point-in-Time Recovery

    - Snapshot; ### Connection Pool; Pod 수가 늘면 DB Connection도 증가하므로 Connection Pool 관리가 중요하다.

    필요 시 RDS Proxy를 고려할 수 있다.'
  kind: 개념·예시·조건
  source_lines: 929–977
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-06
  knowledge: '## 4.6 Aurora; Aurora는 AWS가 만든 PostgreSQL/MySQL-compatible DB Engine이다.; 핵심:; ```text

    Writer ─┐

    Reader ─┼→ Shared Distributed Storage

    Reader ─┘

    ```; ### Writer / Reader; ```text

    Writer = Write

    Reader = Read Scaling

    ```; ### Endpoint; ```text

    Cluster Endpoint → Writer

    Reader Endpoint → Readers

    ```; ### Failover; Writer 장애 시 Reader를 새 Writer로 승격할 수 있다.; ### Aurora Serverless; 수요에 따라 DB Compute
    Capacity를 탄력적으로 조절하는 방식.; Aurora가 항상 더 좋은 것은 아니다.

    비용, AWS Lock-in, PostgreSQL Extension/Version 호환성 등을 고려한다.'
  kind: 개념·예시·조건
  source_lines: 981–1011
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-07
  knowledge: "## 4.7 ElastiCache; > AWS Managed In-Memory Cache; 대표 용도:\n- Cache\n- Session\n- Rate Limit\n\
    - Counter\n- Temporary State; ### Cache Aside; ```text\nApplication\n ↓\nElastiCache\n ↓ Cache Miss\n\
    RDS\n```; ### RDS와 역할; ```text\nRDS = Source of Truth\nElastiCache = 빠른 임시 / 캐시 데이터\n```; ### Replica\
    \ / Shard; ```text\nReplica = 같은 데이터 복제\nShard = 데이터 분할\n```; ### TTL / Invalidation; Cache는 stale\
    \ data 문제가 있으므로 TTL, Delete, Update 정책이 필요하다.; Redis는 무조건 도입하는 것이 아니라 실제 DB 부하나 Latency 문제가 있을 때 도입하는\
    \ 것이 좋다."
  kind: 개념·예시·조건
  source_lines: 1015–1050
  destination: aws-cloud/storage-databases.md
- id: AWSC-04-08
  knowledge: '## Chapter 4 통합 비교; | 종류 | AWS 서비스 | 대표 용도 |

    |---|---|---|

    | Block Storage | EBS | OS / DB Disk |

    | File Storage | EFS | Shared File System |

    | Object Storage | S3 | Dataset / Model / Backup |

    | Relational DB | RDS / Aurora | Transactional Data |

    | In-Memory Cache | ElastiCache | Cache / Session |'
  kind: 개념·예시·조건
  source_lines: 1054–1062
  destination: aws-cloud/storage-databases.md
- id: AWSC-05-01
  source_lines: 1068–1099
  knowledge: EKS=Elastic Kubernetes Service. AWS가 API Server/Scheduler/Controller Manager/etcd control
    plane 관리, worker node에Pod실행. control/data plane분리도와 VPC→PrivateSubnet→EC2Node→Pod경로.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-02
  source_lines: 1100–1150
  knowledge: NodeGroup은같은특성worker묶음;General/GPU예시,instance type/AMI/subnet/scaling범위/OnDemandSpot설정. ManagedNodeGroup→EC2AutoScalingGroup→EC2Nodes
    lifecycle관리. Min/Desired/Max,PodPending→ClusterAutoscaler/Karpenter→NodeGroupScaleOut원문도식. NodePool종류와증감시점역할구분.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-03
  source_lines: 1151–1195
  knowledge: AmazonVPCCNI는Pod에VPCIP직접할당.10.0.1.0/24,node.10,PodA.21/PodB.22예시. Pod증가→subnetIP소비→고갈. /24총256/사용가능251,NodePodENI공유.
    더큰/추가private subnet,여러AZ분산. /20=4096. 기존subnet /24→/20직접확장불가.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-04
  source_lines: 1196–1227
  knowledge: AWSLoadBalancerController가Kubernetes리소스감시하고AWSAPI로ALB/NLB/listener/targetgroup생성수정. Ingress→ALB,ServiceLoadBalancer→NLB.
    instance target→EC2Node/ip target→PodIP. Service안정endpoint+L4,ALBHTTPHTTPSL7,NLB TCPUDPTLSL4 구분.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-05
  source_lines: 1228–1271
  knowledge: CSI=ContainerStorageInterface. EBS/EFS driver서비스연결,Pod→PVC→EBSCSI→EBS와Pods→PVC→EFSCSI→EFS도식.
    EBSAZ와Podscheduling조건. EFS공유filesystem. 전용diskEBS/공유fileEFS/objectdatasetmodelS3역할.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-06
  source_lines: 1272–1306
  knowledge: ECR=ElasticContainerRegistry Managedimage registry. SourceCode→dockerbuild→image→ECR→EKSNodePull→Pod실행.
    repository별image/tag버전. Node또는관련identity에pull권한. AI코드imageECR대modelweight/dataset/artifactS3.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-07
  source_lines: 1307–1359
  knowledge: Pod가AWS접근시직접accesskey저장대신IAMrole. NodeRole공유의과도권한위험. Pod→SA→PodIdentity→IAMRole→AWSResource.
    model-loader S3Read/api SecretsManagerRead/worker SQSConsume예시. IRSA확장명과Pod단위role연결개념,PodK8sAPIRBAC대AWSIAM구분.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
- id: AWSC-05-08
  source_lines: 1360–1414
  knowledge: Chapter5전체구조도Internet→ALB→EKS→General/GPUNodeGroup→Pods/vLLMPods→PodIdentity→IAMRole→S3/SQS/SecretsManager.
    별도storagePVC EBS/EFS,containerECR→node→Pod,networkVPC→privateSubnet→EC2Node→VPCCNI→PodIP,trafficHTTPHTTPSALB/TCPUDPNLB/내부PodreplicaService도식전부.
  kind: concept/architecture/operations/conditions/examples
  destination: aws-cloud/eks.md
---

# 압축형 AWS 1~5장 지식 추출

장별 상세 개념·예시·수치·조건과 전체 과정·통합구조·진도를39개ID로 추적한다. 새로운1.4 ARN·2.2 CIDR·2.3 IP와4장통합비교·5장전체구조까지추적한다. 부모의manifest집계 전에 각담당이 상세추출을 먼저 수행했다.
