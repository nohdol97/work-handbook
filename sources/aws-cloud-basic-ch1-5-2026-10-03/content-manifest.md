---
items:
- id: AWS-00-01
  knowledge: AWS Basic 현재 세션1~5장 완료분과 중간 Q&A를 이후 문서화·핸드북·복습의 원본으로 사용한다는 범위. 개념 학습과 실제 운영 실험을 구분한다.
  kind: scope
  source_lines: 1–8
  destination: aws-cloud/index.md
- id: AWS-00-02
  knowledge: '12장 전체 커리큘럼: Region/AZ·Account·IAM, VPC/subnet/routes/IGW/NAT/SG와CIDR/IP/ALB보충, EC2/ASG/LB,
    EBS/S3/EFS, RDS/Aurora/ElastiCache, EKS/nodegroup/ALBcontroller/EBSCSI, MSK/SQS/SNS, IAMRole/IRSA/PodIdentity/KMS/SecretsManager,
    CloudWatch/CloudTrail, Terraform, GPU EC2/EKS/ECR/S3model, 최종 VPC/EKS/ALB/RDS/cache/MSK/S3/GPU/Terraform구조.'
  kind: curriculum
  source_lines: 9–73
  destination: aws-cloud/index.md
- id: AWS-00-03
  knowledge: Region/VPC/IGW와AZ A/B의public ALB/NAT및private EKS/EC2·RDSprimary/standby·cacheprimary/replica
    도식; S3 dataset/model/backup/parquet/iceberg. User→Internet→IGW→ALB→EKS/EC2→DB/cache/S3, private→NAT→IGW→Internet.
    EBSdisk/EFSshared/S3object/RDSpersistent/cachefaststate와 IAM권한/SG허용/route경로/VPCsubnet배치 역할. 도식의S3위치는논리연결이며
    실제VPC내부배치아님을원문밖보완.
  kind: architecture,roles,conditions
  source_lines: 3317–3421
  destination: aws-cloud/index.md
- id: AWS-00-04
  knowledge: 1~5장 Basic개념학습완료; 다음6장 EKS·NodeGroup·ManagedNodeGroup·AWSLoadBalancerController·EBSCSIDriver
    예정. 7Messaging,8Security,9Observability,10IaC,11AIGPU,12최종구조는후속목차.
  kind: study-status
  source_lines: 3422–3451
  destination: aws-cloud/index.md
- id: AWS-01-01
  section: 1.1 Region / Availability Zone
  source_lines: 76-243
  knowledge: Region 지리적 영역과 AZ 독립 장애 영역; 서울 ap-northeast-2와 a/b/c/d 예시, Tokyo/Virginia 비교. 거리·데이터 위치/규제·서비스
    지원·비용 선택 기준. AZ는 하나 이상의 데이터센터이며 Multi-AZ와 Region 장애 대응 구분. 단일 AZ EC2/DB 실패 예와 ALB→다중 AZ EC2→RDS Multi-AZ
    도식, EKS AZ별 Node 및 Single Region+Multi-AZ 개념.
  kind: concept, comparison, architecture, example, failure-boundary, decision-criteria
  destination: aws-cloud/foundations.md
- id: AWS-01-02
  section: 1.2 AWS Account
  source_lines: 244-433
  knowledge: Account는 리소스·권한·비용 관리 경계, Dev/Staging/Prod 분리와 한 Account의 여러 Region. 12자리 123456789012 및
    ARN 예는 placeholder. Root와 IAM/SSO 일상업무 구분, IAM User/Role 비유. Organizations Management/Dev/Prod/Security/Data
    계층, OU Production/NonProduction 그룹, SCP는 최대허용범위 제한이지 권한 부여 아님. 비용 $1,000/$10,000/$5,000/$20,000은 예시;
    Org→Account→Region→AZ→Resource 도식.
  kind: concept, architecture, identity, policy-boundary, cost-example
  destination: aws-cloud/foundations.md
- id: AWS-01-03
  section: 1.3 IAM 기본
  source_lines: 434-679
  knowledge: IAM User/Role/Policy와 사람 SSO/IdentityCenter+Role. s3:GetObject 특정 bucket ARN statement 예제와
    Effect/Action/Resource/Condition. AssumeRole·EC2 저장 AccessKey 나쁜예와 Role 기반 SDK 임시credential, AccessKey/SecretKey/SessionToken/Expiration.
    Pod IRSA/PodIdentity, permission policy 대 trust policy, leastprivilege s3:* Resource:* 대비 특정객체. 기본deny·명시deny
    우선. 사람/EC2/Pod 접근흐름과 Kubernetes RBAC 대 AWS IAM 경계.
  kind: concept, policy-example, security, workflow, comparison, misconception
  destination: aws-cloud/foundations.md
- id: AWS-02-01
  section: 2.1 VPC
  source_lines: 682-855
  knowledge: VPC는 Region 단위 논리 사설망, Subnet은 한 AZ에만 속하는 범위. 10.0.0.0/16과 10.0.1/2/3.0/24 예시, VPC생성만으로 인터넷
    연결 없음. private app10.0.1.10→DB10.0.2.20, Internet→ALB→App→RDS. VPC peering와 Dev10.10/Stage10.20/Prod10.30.0.0/16
    비중복 계획. VPC→Subnet→EKSNode→Pod. Subnet은 Node가 아니라 네트워크 공간, 여러Node포함, 땅/서버 비유.
  kind: concept, architecture, address-example, network-condition, question-answer
  destination: aws-cloud/networking.md
- id: AWS-02-02
  section: 2.2 Public / Private Subnet
  source_lines: 856-949
  knowledge: Public/private는 특수유형 아닌 route구성. Public default0.0.0.0/0→IGW와 publicIP/SG조건, 자동노출아님. Private
    local10.0.0.0/16 또는 defaultNAT, private→NAT→IGW→Internet outbound와 인터넷직접 inbound 구분. Public ALB/NAT/Bastion
    대 PrivateEKS/EC2/RDS/ElastiCache/MSK. AZA/B/C별 public/private subnet 도식.
  kind: concept, comparison, routing-example, deployment-pattern, security-condition
  destination: aws-cloud/networking.md
- id: AWS-02-03
  section: 2.3 Route Table
  source_lines: 950-1019
  knowledge: Destination/Target, local·IGW·NAT 라우트. 0.0.0.0/0 모든IPv4와 더구체경로우선. 10.0.0.0/16 local,10.10.0.0/16
    peering,defaultIGW longestprefixmatch. Route는 목적지경로,SG는 통신허용이라는 역할구분.
  kind: concept, routing-rule, example, comparison
  destination: aws-cloud/networking.md
- id: AWS-02-04
  section: CIDR 상세 보충 (원문 2.3 다음)
  source_lines: 1020-1165
  knowledge: IPv4 32bit, /24 fixed24 remaining8→2^8=256과10.0.0.0~255; /16 remaining16→2^16=65,536과10.0.0.0~10.0.255.255.
    /16,/20,/24,/28,/32,/0 표 65,536/4,096/256/16/1/all. 203.0.113.10/32 관리자예시. VPC내public1/2 private11/12
    subnet 포함·비중복과1.0/24 vs1.128/25 overlap. masks255.255.0.0,/24,/32. AWS5예약주소, VPC CNI Pod21~24 IP사용과subnet고갈.
  kind: supplement, calculation, table, address-example, constraint, capacity-risk
  destination: aws-cloud/networking.md
- id: AWS-02-05
  section: Public IP / Private IP 보충 (원문 2.4 앞)
  source_lines: 1166-1210
  knowledge: Public은 인터넷라우팅 가능 3.34.100.20/8.8.8.8 설명예시, Private은 인터넷직접라우팅불가. RFC1918 10/8,172.16/12,192.168/16
    정확범위표. EC2private10.0.1.10→IGW또는NAT→PublicIP→Internet 흐름과 내부/외부통신구분.
  kind: supplement, concept, address-table, architecture
  destination: aws-cloud/networking.md
- id: AWS-02-06
  section: 2.4 Internet Gateway
  source_lines: 1211-1305
  knowledge: IGW는 VPC단위 attach, attach만으로인터넷완성아님. publicEC2 route0.0.0.0/0→IGW/publicIP/SG조건과 privateIP
    mapping. Private보통defaultNAT. User→Internet→IGW→PublicALB→Private→EKSPod. IGW는 AZ별 생성대신 한VPC에하나 attach공유.
  kind: concept, prerequisite, workflow, architecture, scope
  destination: aws-cloud/networking.md
- id: AWS-02-07
  section: 2.5 NAT Gateway
  source_lines: 1306-1415
  knowledge: Private outbound→NAT→IGW→Internet. NAT변환10.0.11.20→PublicIP, 외부직접시작불가. PublicSubnet위치/EIP/defaultNAT/localroute.
    AZA/B별NAT와privateSubnet availability패턴. PrivateEKS API/package/image egress, AWS서비스 S3/ECR VPCendpoint를
    통한NAT우회가능.
  kind: concept, address-translation, direction-boundary, architecture, availability, alternative
  destination: aws-cloud/networking.md
- id: AWS-02-08
  section: 2.6 Security Group
  source_lines: 1416-1547
  knowledge: SG resource/ENI virtualfirewall protocol/port/source/dest. TCP443 allIPv4, inbound/outbound,
    stateful응답자동허용. HTTP80/HTTPS443 공개예와SSH22 203.0.113.10/32제한. ALB-SG443→APP-SG8080→DB-SG5432 referencedSG
    패턴/EKS→RDS 흐름. Allow-only 명시deny없음. SG resource/ENI stateful 대비 NACL subnet stateless allow/deny 표.
  kind: concept, rule-example, security, architecture, comparison-table
  destination: aws-cloud/networking.md
- id: AWS-02-09
  section: ALB 보충 설명 (원문 2.6 다음)
  source_lines: 1548-1686
  knowledge: ALB L7분산/장애제외/MultiAZ/HTTPS/pathhost라우팅. /api/*,/web/*,api.example.com/www.example.com. Listener80/443와
    targetgroupEC2A/B/C, GET/health200정상 및unhealthy제외 원문주장. PublicIGW→ALB→PrivateApp vsInternal서비스→InternalALB.
    TLStermination HTTPS→ALB→HTTP/HTTPS +ACM. EKSIngress→AWSLBController→ALB→Service→Pod도식. ALBL7/NLBL4
    HTTP/path/host/TCPUDP 비교표.
  kind: supplement, concept, routing-example, health-condition, architecture, comparison-table
  destination: aws-cloud/networking.md
- id: AWS-03-01
  knowledge: "## 3.1 EC2; EC2 = **Elastic Compute Cloud**; > AWS에서 빌려 쓰는 가상 서버; ### EC2 구성 시 선택; - AMI\n\
    - Instance Type\n- VPC\n- Subnet\n- Security Group\n- Storage\n- IAM Role; ### AMI; Amazon Machine\
    \ Image.; EC2 생성을 위한 서버 이미지.; ```text\nAMI\n ↓\nEC2 생성\n ↓\n운영체제가 설치된 서버\n```; AMI와 Docker Image의\
    \ 차이:; ```text\nAMI\n= VM 전체 이미지\n\nDocker Image\n= Container 실행 이미지\n```; ### Instance Type; CPU,\
    \ Memory, GPU 등의 서버 사양.; 대표 계열:; ```text\nt = 범용/저비용\nm = General Purpose\nc = Compute Optimized\n\
    r = Memory Optimized\ng / p = GPU\n```; ### EC2는 특정 Subnet에 배치; ```text\nVPC\n└─ Subnet\n   └─ EC2\n\
    ```; Subnet 선택으로 AZ도 결정된다.; ### Public EC2 / Private EC2; Public:; ```text\nInternet\n ↓\nIGW\n ↓\n\
    Public Subnet\n ↓\nEC2\n```; Private:; ```text\nPrivate Subnet\n└─ EC2\n```; Private EC2의 외부 접속:;\
    \ ```text\nEC2\n ↓\nNAT Gateway\n ↓\nIGW\n ↓\nInternet\n```; ### Security Group; EC2 앞의 접근 제어.; ###\
    \ EBS; EC2 저장공간으로 보통 EBS를 사용.; ```text\nEC2\n ↓\nEBS Volume\n```; ### IAM Role; ```text\nEC2\n ↓\n\
    IAM Role\n ↓\nS3\n```; 고정 Access Key 저장을 피할 수 있다.; ### User Data; EC2 최초 부팅 시 실행할 초기화 Script.; ###\
    \ Stop / Start / Terminate; - Stop = 전원 끄기\n- Start = 다시 켜기\n- Terminate = 인스턴스 제거; ### Public IP\
    \ / Elastic IP; Public IP는 변할 수 있다.; 고정 Public IPv4가 필요하면 Elastic IP 사용 가능.; 현대적인 웹 서비스에서는 EC2 Public\
    \ IP에 직접 의존하기보다:; ```text\nDNS\n ↓\nALB\n ↓\nEC2 여러 대\n```; 구조를 많이 사용한다.; ### 단일 EC2 문제; Single Point\
    \ of Failure.; Production에서는 여러 AZ에 여러 EC2를 두는 구성이 일반적.; ### EKS Node와 EC2; Managed Node Group을 쓰면\
    \ EKS Worker Node의 실체가 EC2인 경우가 많다.; ```text\nEKS Cluster\n   ↓\nNode Group\n   ↓\nEC2\n   ↓\nPod\n\
    ```; ### AI/GPU; GPU EC2 위에 vLLM 등을 실행할 수 있다."
  kind: 개념·규칙·조건
  source_lines: 1689–1862
  destination: aws-cloud/compute.md
- id: AWS-03-02
  knowledge: "## 3.2 Auto Scaling; Auto Scaling:; > 트래픽이나 상태에 따라 EC2 개수를 자동으로 늘리거나 줄이는 기능; ### Scale Out\
    \ / Scale In; ```text\nScale Out\n= 서버 추가\n\nScale In\n= 서버 제거\n```; Horizontal Scaling.; Vertical\
    \ Scaling은 서버 한 대의 사양을 키우는 것.; ### Auto Scaling Group(ASG); ```text\nMin     = 2\nDesired = 3\nMax\
    \     = 10\n```; - Min = 최소 인스턴스 수\n- Desired = 유지하려는 인스턴스 수\n- Max = 최대 수; ### Self Healing; Desired\
    \ 3인데 한 대가 죽으면 새 EC2를 만들어 3대를 유지한다.; ### Launch Template; EC2 생성 설계도.; ```text\nLaunch Template\n\
    ├─ AMI\n├─ Instance Type\n├─ Security Group\n├─ IAM Role\n├─ Storage\n└─ User Data\n```; ### ALB와\
    \ 결합; ```text\nALB\n ↓\nTarget Group\n ↓\nASG\n├─ EC2 A\n├─ EC2 B\n└─ EC2 C\n```; Scale Out된 인스턴스도\
    \ Target Group에 등록된다.; ### Health Check; 불량 인스턴스를 트래픽 대상에서 제외하거나 교체할 수 있다.; ### Dynamic Scaling; CloudWatch\
    \ Metric 기반.; 예:; ```text\nCPU > 70%\n→ EC2 증가\n```; ### Target Tracking; 예:; ```text\n평균 CPU 50%\
    \ 유지\n```; 목표에 맞게 자동 증감.; ### Scheduled Scaling; 정해진 시간에 증감.; ### Multi-AZ; ASG를 여러 AZ에 걸쳐 구성해 장애\
    \ 대응.; ### EKS와 연결; EKS에서는 Node 수를 조절하기 위해:; - Managed Node Group\n- Auto Scaling Group\n- Cluster\
    \ Autoscaler\n- Karpenter; 등이 연결될 수 있다.; ### Stateless Application; Auto Scaling에서는 EC2가 언제든 생성/삭제되므로\
    \ 애플리케이션은 Stateless가 유리하다.; ```text\nApplication\n= Stateless\n\nState\n= RDS / ElastiCache / S3\n\
    ```"
  kind: 개념·규칙·조건
  source_lines: 1866–1985
  destination: aws-cloud/compute.md
- id: AWS-03-03
  knowledge: "## 3.3 Load Balancer; Load Balancer:; > 들어오는 요청을 여러 Backend 서버로 분산; ### 핵심 역할; 1. 요청 분산\n\
    2. Health Check\n3. 단일 진입점 제공; ### ALB vs NLB; ALB:\n- L7\n- HTTP/HTTPS\n- Path/Host 기반 Routing; NLB:\n\
    - L4\n- TCP/UDP/TLS\n- 고성능 네트워크; ### Listener; 어떤 Protocol/Port로 요청을 받을지 정의.; ### Listener Rule; ```text\n\
    /api/*   → API Target Group\n/admin/* → Admin Target Group\n그 외    → Web Target Group\n```; ### Target\
    \ Group; Backend 서버 그룹.; ### Auto Scaling 연동; 새 EC2가 생기면 Target Group에 등록되어 ALB가 트래픽을 분산한다.; ### HTTPS\
    \ / ACM; ALB Listener에서 TLS Termination 가능.; ### Public / Internal ALB; 둘 다 존재 가능.; ### 전체 Compute\
    \ 구조; ```text\nInternet\n   ↓\n  IGW\n   ↓\n  ALB\n   ↓\nTarget Group\n   ↓\nAuto Scaling Group\n\
    ├─ EC2 - AZ A\n├─ EC2 - AZ A\n├─ EC2 - AZ B\n└─ EC2 - AZ B\n```; 정리:; ```text\nEC2\n= 실제 서버\n\nASG\n\
    = 서버 개수 관리\n\nALB\n= 요청 분산\n\nTarget Group\n= Backend 묶음\n\nListener\n= 요청 받을 Port/Protocol\n```"
  kind: 개념·규칙·조건
  source_lines: 1989–2076
  destination: aws-cloud/compute.md
- id: AWS-04-01
  knowledge: "## 4.1 EBS; EBS = **Elastic Block Store**; > EC2에 붙여 사용하는 가상 디스크; ```text\nEC2\n ↓\nEBS\
    \ Volume\n```; 비유:; ```text\nEC2 = 컴퓨터 본체\nEBS = SSD/HDD\n```; ### EBS와 EC2는 별도 리소스; EBS는 EC2와 분리\
    \ 가능한 저장장치다.; ### Block Storage; 운영체제에서는 일반 디스크 장치처럼 보인다.; 예:; ```text\n/dev/xvda\n/dev/nvme0n1\n\
    ```; 위에 ext4/xfs 같은 파일시스템을 구성.; ### EBS vs S3; ```text\nEBS\n= 서버 디스크\n\nS3\n= Object Storage\n```;\
    \ ### EBS는 AZ 단위; EC2와 EBS를 연결하려면 기본적으로 같은 AZ여야 한다.; ```text\nEC2: AZ A\nEBS: AZ A\n→ Attach 가능\n\n\
    EC2: AZ A\nEBS: AZ B\n→ 직접 Attach 불가\n```; ### Root Volume; EC2 운영체제가 설치된 기본 디스크.; 추가 데이터 EBS도 연결\
    \ 가능.; ### Volume Type; 대표:; - gp3 = 일반적인 SSD\n- io2 = 높은 IOPS 요구\n- st/sc = HDD 계열; ### IOPS vs Throughput;\
    \ ```text\nIOPS\n= 초당 I/O 작업 횟수\n\nThroughput\n= 초당 전송 데이터 양\n```; ### Snapshot; EBS Volume의 시점 기반\
    \ 백업.; ```text\nEBS\n ↓\nSnapshot\n ↓\nNew EBS\n```; 다른 AZ에 복원도 가능.; ### EC2 Terminate와 EBS; Root\
    \ Volume은 `Delete on Termination` 설정에 따라 EC2와 같이 삭제될 수 있다.; ### Instance Store; 호스트 로컬 임시 스토리지.; ```text\n\
    중요한 지속 데이터\n→ EBS\n\n잃어도 되는 임시 데이터\n→ Instance Store\n```; ### EKS에서 EBS; ```text\nPod\n ↓\nPVC\n\
    \ ↓\nPV\n ↓\nEBS\n```; AWS EBS CSI Driver가 중간에서 EBS를 관리.; ### AZ 제약; EBS는 특정 AZ에 있으므로 Pod가 다른 AZ Node로\
    \ 이동할 때 제약이 생길 수 있다.; ### RDS; RDS는 내부 스토리지를 Managed 형태로 제공하므로 사용자가 EBS를 직접 attach/detach하지 않는다."
  kind: 개념·규칙·조건
  source_lines: 2082–2216
  destination: aws-cloud/storage.md
- id: AWS-04-02
  knowledge: "## 4.2 S3; S3 = **Simple Storage Service**; > AWS의 Object Storage; ```text\nApplication\n\
    \   ↓\nS3 API\n   ↓\nBucket\n   ↓\nObjects\n```; ### Bucket / Object; - Bucket = Object를 담는 컨테이너\n\
    - Object = 실제 데이터; 예:; ```text\nmy-data-bucket\n├─ images/logo.png\n├─ models/model-v1.bin\n└─ logs/2026/10/03/app.log\n\
    ```; ### 폴더처럼 보이는 구조; 실제로는 폴더가 아니라 Object Key.; ```text\nlogs/2026/10/03/app.log\n```; 이 전체가 Key다.;\
    \ ### EBS와 차이; EBS:; ```text\nEC2\n ↓\nFile System\n ↓\nEBS\n```; S3:; ```text\nApplication\n ↓\n\
    HTTP/API\n ↓\nS3\n```; ### 여러 서비스가 공동 사용; ```text\n        S3\n      /  |  \\\n    EC2 EKS Lambda\n\
    ```; ### 대표 저장 데이터; - 이미지 / 영상\n- 로그\n- 백업\n- CSV / Parquet\n- AI Model\n- Dataset\n- 정적 웹 파일\n- Data\
    \ Lake; ### Data Platform; ```text\nRaw Data\n   ↓\nS3\n   ↓\nParquet / Iceberg\n   ↓\nAnalytics /\
    \ AI\n```; ### S3는 Region 기반 서비스; Bucket 생성 시 Region을 선택한다.; EBS처럼 특정 AZ에 붙이는 개념으로 쓰지 않는다.; ### Versioning;\
    \ 같은 Key의 이전 버전을 보존할 수 있다.; ### Lifecycle; 오래된 Object를 저렴한 Storage Class로 이동하거나 삭제할 수 있다.; ### Storage\
    \ Class; - Standard\n- Infrequent Access 계열\n- Glacier 계열; ### Access Control; 보통 Private으로 사용.; ```text\n\
    Application\n ↓\nIAM Role\n ↓\nS3\n```; ### Bucket Policy; Bucket 자체에 적용하는 Resource-based Policy.;\
    \ ```text\nIAM Policy\n= User/Role 쪽 권한\n\nBucket Policy\n= Bucket 쪽 권한\n```; ### VPC Endpoint; Private\
    \ Subnet에서 S3 접근 시 NAT 대신 VPC Endpoint를 사용할 수 있다.; ```text\nPrivate Subnet\n ↓\nVPC Endpoint\n ↓\n\
    S3\n```; ### AI / LLM; ```text\nS3\n└─ Model Files\n     ↓\nGPU Node\n     ↓\nvLLM\n```; ### S3는 NAS가\
    \ 아니다; S3는 일반 파일시스템이 아니다.; 기본 접근은:; - GetObject\n- PutObject; 같은 API 방식.; ### 보충 Q&A: Object Storage를\
    \ Bucket으로 나누는 이유; 정책/권한 분리가 큰 이유 중 하나다.; Bucket은 **큰 관리 경계**로 볼 수 있다.; ```text\nBucket\n├─ Access\
    \ Policy\n├─ Lifecycle\n├─ Versioning\n├─ Encryption\n├─ Logging\n└─ Objects\n```; 예:; ```text\ncompany-raw-data\n\
    company-model-artifacts\ncompany-public-assets\n```; 권한 분리 예:; ```text\nraw-data bucket\n→ Data Engineer만\
    \ write 가능\n\nmodel bucket\n→ AI Serving Role은 read만 가능\n\npublic-assets bucket\n→ 외부 공개 허용\n```;\
    \ 그 외 Bucket 분리 이유:; - 보안 경계\n- Lifecycle 정책 분리\n- Versioning/Replication 설정 분리\n- 비용/운영 관리\n- 환경\
    \ 분리(dev/stage/prod); 다만 데이터 종류마다 무조건 Bucket을 나눌 필요는 없다.; 하나의 Bucket 내부 Prefix로 논리적 구분도 가능.; ```text\n\
    data-platform-prod/\n├─ raw/\n├─ processed/\n└─ curated/\n```; 정리:; > Bucket = 큰 관리/보안 경계  \n> Prefix\
    \ = Bucket 내부 논리적 분류"
  kind: 개념·규칙·조건
  source_lines: 2220–2450
  destination: aws-cloud/storage.md
- id: AWS-04-03
  knowledge: "## 4.3 EFS; EFS = **Elastic File System**; > 여러 EC2/EKS 인스턴스가 동시에 마운트해서 쓸 수 있는 공유 파일시스템;\
    \ ```text\n        EFS\n      /  |  \\\n    EC2 EC2 EKS\n```; ### EBS와 차이; ```text\nEBS\n= 서버 디스크\n\
    \nEFS\n= 공유 네트워크 파일시스템\n```; ### S3와 차이; S3는 API 기반 Object Storage.; EFS는 POSIX 스타일 파일시스템처럼 Mount해서\
    \ 사용할 수 있다.; ```text\n/mnt/shared/file.txt\n```; ### NFS 기반; EFS는 네트워크 파일시스템이며 일반적으로 NFS 프로토콜을 사용한다.;\
    \ ### 공유가 필요한 이유; 여러 EC2가 같은 파일을 봐야 할 때.; ```text\n        EFS\n         │\n    ┌────┼────┐\n    ↓\
    \    ↓    ↓\n  EC2A EC2B EC2C\n```; ### Multi-AZ; 여러 AZ의 인스턴스에서 접근 가능하도록 설계할 수 있다.; ### Mount Target;\
    \ VPC에서 EFS에 접근하기 위한 네트워크 접점.; ### Security Group; NFS는 일반적으로 TCP 2049를 사용.; 예:; ```text\nEFS-SG\n\
    Inbound\n2049 ← APP-SG\n```; ### EKS + EFS; ```text\nPod\n ↓\nPVC\n ↓\nEFS CSI Driver\n ↓\nEFS\n```;\
    \ 여러 Pod가 하나의 공유 파일시스템을 함께 사용할 때 적합.; ### EBS vs EFS in Kubernetes; ```text\nEBS\n→ 단일 Workload용 Block\
    \ Storage\n\nEFS\n→ 여러 Workload가 공유하는 File Storage\n```; ### S3 vs EFS; ```text\nObject 형태로 저장/전송\n\
    → S3\n\nPOSIX 파일시스템 공유\n→ EFS\n```; ### AI Platform 예; S3 방식:; ```text\nS3\n ↓\nGPU Node A 다운로드\n\
    GPU Node B 다운로드\nGPU Node C 다운로드\n```; EFS 방식:; ```text\n        EFS\n      /  |  \\\n   GPUA GPUB\
    \ GPUC\n```; ### Data Platform; Data Lake는 보통 EFS보다 S3가 자연스럽다.; ```text\nRaw Data\n ↓\nS3\n ↓\nParquet\
    \ / Iceberg\n```; EFS는 Shared Config, Workspace, Legacy App Files 등 파일시스템 공유가 필요할 때 적합.; ### Storage\
    \ 3종 비교; | 항목 | EBS | EFS | S3 |\n|---|---|---|---|\n| Storage Type | Block | File | Object |\n| 접근\
    \ | Attach | Mount | API |\n| 공유 | 제한적 | 여러 서버 공유 | 여러 서비스 공유 |\n| 범위 | AZ | Multi-AZ 접근 가능 | Region\
    \ 기반 |\n| 대표 용도 | OS, DB Disk | Shared File System | Dataset, Backup, Model |\n| EKS | PVC + EBS CSI\
    \ | PVC + EFS CSI | SDK/API |; 선택 기준:; ```text\n서버 디스크가 필요\n→ EBS\n\n여러 서버가 같은 파일시스템을 봐야 함\n→ EFS\n\
    \n대규모 파일/데이터를 객체 형태로 저장\n→ S3\n```; ### 보충 Q&A: PostgreSQL 여러 Pod면 EFS를 공유하는가?; 아니다.; 여러 PostgreSQL\
    \ Pod가 하나의 EFS에 동일한 `PGDATA`를 동시에 쓰는 구조는 일반적으로 사용하면 안 된다.; ```text\n        EFS\n       /   \\\nPostgres\
    \ A  Postgres B\n   ↓            ↓\n동일 DB 파일 동시 수정 ❌\n```; 데이터 손상 위험이 있다.; 일반적으로 각 PostgreSQL Pod가\
    \ 자기 전용 Volume을 가진다.; ```text\nPostgres Primary\n      ↓\n    PVC A\n      ↓\n    EBS A\n\nPostgres\
    \ Replica\n      ↓\n    PVC B\n      ↓\n    EBS B\n```; 데이터 복제는 파일시스템 공유가 아니라 PostgreSQL Replication으로\
    \ 한다.; ```text\nPrimary\n  │\n  │ WAL Replication\n  ▼\nReplica\n```; Kubernetes에서는 StatefulSet을 사용해:;\
    \ ```text\npostgres-0 → PVC-0 → EBS-0\npostgres-1 → PVC-1 → EBS-1\npostgres-2 → PVC-2 → EBS-2\n```;\
    \ 형태로 구성할 수 있다.; EFS는 DB 데이터 디렉터리보다는 백업/공유 Dump 같은 용도에 더 적합하다.; ```text\nPostgreSQL\n ↓\npg_dump\n\
    \ ↓\nEFS 또는 S3\n```; 특히 백업은 S3가 더 흔하다.; AWS에서는 특별한 이유가 없다면 EKS 내부 직접 PostgreSQL 운영보다 RDS PostgreSQL\
    \ / Aurora PostgreSQL도 강하게 고려한다."
  kind: 개념·규칙·조건
  source_lines: 2454–2678
  destination: aws-cloud/storage.md
- id: AWS-05-01
  source_lines: 2684–2918
  knowledge: RDS는Managed관계형DB서비스이며PostgreSQL/MySQL/MariaDB/Oracle/SQLServer예시를제공. EC2직접운영의OS·설치·disk·backup·patch·monitoring·failover·replication과비교해사용자는schema/query/index/application
    connection/DBparameter관리. Private subnet·DBSubnetGroup AZ A/B/C·APP-SG에서TCP5432·가상RDS endpoint및장애조치관계.
    MultiAZprimary/standby는HA,readreplica는읽기분산이라는원문구분;backup/PITR/manualsnapshot,storage size/type/IOPS는직접EBSattach아님;instanceclass수직확장.100Pods×20connections=2000DBconnections·pool/RDSProxy.
    ALB→EKS→RDS,statelessapp와영구transactiondata. EKS직접Postgres운영의StatefulSet/PVC/EBS/replication/backup/failover/upgrade/operator부담과RDS에서도slowquery/index/schema/pool/transaction/lock/vacuum/capacity책임.
  kind: concept, comparison, architecture, example, operations, constraint
  destination: aws-cloud/databases-cache.md
- id: AWS-05-02
  source_lines: 2920–3075
  knowledge: Aurora는RDS에서제공하는AWS자체PostgreSQL/MySQL호환관계형엔진. RDS서비스/엔진계층도,compute/shared distributed storage분리와DB1/2/3도식.
    Writer INSERT/UPDATE/DELETE,readers SELECT/readscaling;clusterendpoint쓰기와readerendpoint읽기;reader→writer승격과clusterendpoint유지.
    MultiAZ분산storage·자동storagecapacity확장·provisioned고정크기대serverless탄력compute. 비용/기능차이/PostgreSQL버전·extension호환/AWS종속/복잡도;작은서비스RDS충분가능,HA/readscaling시Aurora검토.
    App→pool→optionalRDSProxy→Aurora로연결관리필요. RDSvsAurora비교표7행엔진/storage/HA/readscaling/failover/storage확장/비용구조.
  kind: concept, architecture, comparison, tradeoff, operations, constraint
  destination: aws-cloud/databases-cache.md
- id: AWS-05-03
  source_lines: 3077–3316
  knowledge: ElastiCache는Managedin-memorycache,DB부하감소. cacheaside hit반환/miss RDS조회→Redis저장→반환;RDSsourceoftruth/임시cache구분.
    cache/session/ratelimit/counter/leaderboard/temporarystate;EKS직접Redis StatefulSet/PVC/replication/failover/backup/upgrade대Managed.
    PrivateVPC ALB/EKS/RDS/cache도식,6379←APP-SG. primary/replica HA/readscaling·MultiAZ승격,shard당primary/replica;replica동일데이터대shard분할capacity/write확장.
    user:123 TTL600초·token/session/ratelimit;DB변경후cachedelete/update또는TTL stale조건. PodA/B/C외부공유session으로stateless.
    appstateless/cacheElastiCache/persistentRDS/objectS3. RDS/cache비교disk-memory/영구임시/속도/사용자주문설정vsCacheSession/sourceoftruth.
    Redis필수아니며초기RDS충분시생략,추가cachepolicy/TTL/invalidation/memory/failover복잡성을실제DB부하/latency근거로평가.
  kind: concept, workflow, architecture, comparison, example, failure, tradeoff
  destination: aws-cloud/databases-cache.md
---

# AWS 1~5장 지식 추출

장별 상세 개념·예시·수치·조건과 전체 과정·통합구조·진도를25개ID로 추적한다. 번호 없는CIDR·IP·ALB보충도 별도ID이며 버리지 않는다. 부모의manifest집계 전에 각담당이 상세추출을 먼저 수행했다.
