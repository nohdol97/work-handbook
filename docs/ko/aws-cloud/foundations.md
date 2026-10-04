---
id: aws-cloud-foundations
status: studied
last_updated: 2026-10-04
last_reviewed: 2026-10-04
knowledge_ids:
  - AWSC-01-01
  - AWSC-01-02
  - AWSC-01-03
  - AWSC-01-04
---

# Chapter 1. AWS Foundation

제공된 compact 원문의 순서와 예시를 보존한 학습 기록이다. 실제 AWS 운영 결과가 아니다. **본문 안내:** 뒤의 보완에서 Multi-AZ·SCP 범위와 IAM 정책 예제의 조건을 확인한다.

<!-- SOURCE CORE START -->

## 1.1 Region / Availability Zone

### Region
AWS의 큰 지리적 운영 영역이다.

예:
```text
Seoul Region
ap-northeast-2
```

Region 선택 시 주요 고려 요소:
- 사용자와의 거리 / Latency
- 데이터 저장 위치와 규제
- 해당 Region의 AWS 서비스 지원 여부
- 비용

### Availability Zone
AZ는 하나의 Region 안에 존재하는 독립된 장애 영역이다.

```text
Seoul Region
├─ AZ A
├─ AZ B
├─ AZ C
└─ AZ D
```

AZ는 데이터센터 하나라고 단정하기보다 하나 이상의 데이터센터로 구성될 수 있는 독립 장애 영역으로 이해한다.

### Multi-AZ
한 AZ에만 서비스를 배치하면 해당 AZ 장애가 전체 서비스 장애로 이어질 수 있다.

```text
ALB
├─ AZ A → Application
└─ AZ B → Application
```

따라서 Production에서는 하나의 Region 안에서 여러 AZ에 리소스를 분산하는 구성이 기본이다.

핵심:
```text
Region = 큰 지리적 영역
AZ = Region 내부의 독립 장애 영역
기본 운영 패턴 = Single Region + Multi-AZ
```

---

## 1.2 AWS Account / Organizations

AWS Account는 단순 로그인 계정이 아니라 리소스, 비용, 권한의 큰 관리 경계다.

```text
AWS Account
├─ EC2
├─ S3
├─ RDS
├─ EKS
└─ IAM
```

하나의 Account 안에서 여러 Region을 사용할 수 있다.

```text
Account = 관리 / 권한 / 비용 경계
Region = 지리적 배치 영역
```

실무에서는 환경이나 조직에 따라 Account를 분리하기도 한다.

```text
AWS Organization
├─ Dev Account
├─ Staging Account
├─ Prod Account
├─ Security Account
└─ Data Account
```

장점:
- 운영 실수 격리
- 권한 분리
- 비용 분리
- 보안 경계 강화

### Root User
Account의 최상위 사용자다. 평소 운영에는 사용하지 않고 초기 설정이나 매우 제한된 작업에만 사용하는 것이 기본이다.

### AWS Organizations
여러 AWS Account를 중앙에서 관리한다.

### OU
Organizational Unit. Account들을 묶는 논리적 그룹이다.

### SCP
Service Control Policy. 조직/OU/Account 수준에서 최대 허용 권한 범위를 제한한다.

```text
IAM Policy = 실제 권한 부여
SCP = 조직 수준의 최대 허용 범위 제한
```

SCP 자체가 권한을 주는 것은 아니다.

---

## 1.3 IAM User / Role / Policy

IAM = Identity and Access Management.

> 누가 어떤 AWS Resource에 무엇을 할 수 있는가를 관리한다.

핵심:
```text
IAM User
IAM Role
IAM Policy
```

### IAM User
AWS Account 내부의 고정 사용자 Identity.

기업 환경에서는 사람에게 장기 Access Key를 직접 주기보다 SSO / IAM Identity Center + Role 방식을 많이 고려한다.

### IAM Policy
권한 규칙.

예:
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-bucket/*"
}
```

핵심 요소:
```text
Effect
Action
Resource
Condition
```

### IAM Role
필요할 때 맡는 권한 묶음.

```text
Identity
 ↓
AssumeRole
 ↓
IAM Role
 ↓
AWS Resource
```

Role 기반 인증에서는 만료 시간이 있는 Temporary Credential을 사용할 수 있다.

일반적으로:
- Access Key
- Secret Key
- Session Token
- Expiration

### Trust Policy vs Permission Policy
```text
Trust Policy = 누가 이 Role을 맡을 수 있는가
Permission Policy = Role을 맡았을 때 무엇을 할 수 있는가
```

### Least Privilege
필요한 최소 권한만 부여한다.

```text
나쁜 예
s3:* / Resource: *

좋은 예
s3:GetObject / 특정 bucket/*
```

### IAM과 Kubernetes RBAC
```text
Pod → Kubernetes API = Kubernetes RBAC
Pod → S3 / SQS / Secrets Manager = AWS IAM
```

---

## 1.4 AWS Resource / ARN

AWS Resource 예:
- EC2 Instance
- S3 Bucket
- IAM Role
- RDS Instance
- EKS Cluster

많은 AWS Resource는 ARN(Amazon Resource Name)으로 식별한다.

예:
```text
arn:aws:iam::123456789012:role/MyRole
```

---

<!-- SOURCE CORE END -->

## 보완: 1.1~1.4의 적용 조건

공식 문서 확인일: 2026-10-04.

**1.1 Multi-AZ:** 여러 AZ에 배치해도 애플리케이션·데이터 복제·장애 시 라우팅·잔여 용량을 검증해야 한다. Multi-AZ 자체가 Region 전체 장애에 대한 복구를 보장하지는 않는다.

**1.2 계정과 SCP:** SCP는 Organizations의 모든 기능을 활성화한 조직에서 사용하며, 멤버 계정의 root에도 적용된다. 관리 계정의 사용자·역할과 서비스 연결 역할에는 적용되지 않는다. 사람의 일상 접근은 연동 로그인과 임시 자격 증명을 우선하고 MFA를 적용한다. [AWS SCP 문서](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html), [IAM 보안 권장 사항](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html).

**1.3~1.4 정책 예제:** 원문의 JSON은 정책 전체가 아니라 하나의 statement이다. 실제 정책 문서는 `Statement`로 감싸고 정책 언어 버전 `Version`을 지정한다. `Condition`은 선택 사항이다. Trust Policy가 역할 수임 주체를 허용해도 Permission Policy의 서비스 권한을 대신하지 않는다. 임시 자격 증명도 비밀이며 만료 전에 안전하게 갱신해야 한다. ARN의 `123456789012`는 설명용 계정 번호이다. [IAM 정책 요소](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html), [IAM 역할](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

## LLM 실습: S3 읽기 역할의 권한 경계 검토

- **상황:** 개발 앱에 필요한 S3 읽기 권한과 역할 수임 권한을 혼동하지 않는다.
- **LLM에 제공할 맥락:** 가상 멤버 계정의 앱 역할이 `example-study-bucket/reports/*`만 읽어야 한다. SCP와 Trust Policy의 실제 내용은 제공되지 않았다.
- **기대 출력:** 최소 권한 statement 초안, 수임·SCP 확인 항목, 미확인 전제를 구분한 표.
- **검증 방법:** `s3:GetObject`와 객체 ARN을 사용하고, Trust Policy나 SCP가 서비스 권한을 자동 부여한다고 주장하지 않는다.
- **주의점:** 실제 계정 ID·키·토큰은 넣지 않는다. 생성된 정책은 배포 전에 사람이 확인한다.
- **LLM이 틀릴 수 있는 점:** SCP가 S3 권한을 부여한다고 하거나 Trust Policy만으로 객체 접근이 가능하다고 할 수 있다.
- **예시 프롬프트:** 아래 두 언어 탭을 사용한다.
- **출처 연결:** 1.2~1.4, AWSC-01-02~04.

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 AWS 멤버 계정의 앱 역할이 example-study-bucket/reports/* 객체만 읽어야 한다. SCP와 Trust Policy는 미제공이다.
    [요청]
    최소 권한 IAM statement를 작성하고 역할 수임, 서비스 접근, SCP 제한을 구분해 검토하라.
    [출력]
    statement JSON과 확인 항목/근거/미확인 전제 표를 작성하라.
    [검증]
    s3:GetObject와 객체 ARN을 사용하라. SCP나 Trust Policy를 권한 부여의 충분조건으로 보지 말고 실제 계정 정보나 자격 증명을 요구하지 마라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    An app role in a fictional AWS member account must read only objects under example-study-bucket/reports/*. The SCP and Trust Policy are unavailable.
    [Task]
    Draft a least-privilege IAM statement and distinguish role assumption, service access, and SCP restrictions.
    [Output]
    Provide statement JSON and a table of checks, rationale, and unknown assumptions.
    [Checks]
    Use s3:GetObject and an object ARN. Do not treat an SCP or Trust Policy as sufficient to grant access, and do not request real account information or credentials.
    ```
