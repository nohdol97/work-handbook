---
id: aws-cloud-foundations
status: studied
last_updated: 2026-10-03
last_reviewed: 2026-10-03
knowledge_ids:
  - AWS-01-01
  - AWS-01-02
  - AWS-01-03
---

# Chapter 1. AWS 기본 구조

제공된 AWS Cloud Basic의 학습 원문이다. 번호·순서·예시와 중간 보충 절을 보존했다. 실제 AWS 리소스를 생성하거나 정책·라우팅을 적용한 기록이 아니다. **본문 안내:** 뒤의 **원문 절별 보완과 정정**에서 AZ 식별, SCP 적용 범위와 IAM 정책·임시 자격 증명 조건을 확인한다.

<!-- SOURCE CORE START -->

## 1.1 Region / Availability Zone

AWS를 이해할 때 가장 먼저 잡아야 하는 개념은 Region과 Availability Zone(AZ)이다.

- **Region**: AWS가 운영하는 큰 지리적 영역
- **AZ**: Region 안에 있는 서로 분리된 장애 영역

서울 Region 예:

```text
Region
ap-northeast-2
```

그 안에는 여러 AZ가 있다.

```text
ap-northeast-2a
ap-northeast-2b
ap-northeast-2c
ap-northeast-2d
```

구조:

```text
AWS
│
├─ Seoul Region (ap-northeast-2)
│   ├─ AZ A
│   ├─ AZ B
│   ├─ AZ C
│   └─ AZ D
│
├─ Tokyo Region
└─ Virginia Region
```

### Region은 왜 필요한가?

사용자와 서버 사이의 거리, 데이터 규제, 서비스 지원 여부, 비용 등을 고려해 Region을 선택한다.

예를 들어 한국 사용자를 대상으로 서비스한다면 일반적으로 서울 Region을 고려한다.

```text
Seoul Region
ap-northeast-2
```

Region 선택 시 주요 기준:

- 사용자와의 거리
- 데이터 저장 위치 / 규제
- 서비스 지원 여부
- 비용

### AZ는 왜 필요한가?

한 데이터센터에 모든 서비스를 몰아넣으면 해당 데이터센터 장애 시 전체 서비스가 중단될 수 있다.

그래서 AWS는 Region 내부를 여러 AZ로 나눠 장애 영역을 분리한다.

```text
Seoul Region
│
├─ AZ A
│   └─ Server A
├─ AZ B
│   └─ Server B
└─ AZ C
    └─ Server C
```

하나의 AZ에 장애가 나더라도 다른 AZ에서 계속 서비스를 제공할 수 있다.

이를 **Multi-AZ Architecture**라고 한다.

### Region과 AZ 차이

| 개념 | 의미 |
|---|---|
| Region | 큰 지리적 AWS 운영 영역 |
| AZ | Region 내부의 독립된 장애 영역 |
| 예시 Region | `ap-northeast-2` |
| 예시 AZ | `ap-northeast-2a` |
| 주 목적 | 지역 선택 |
| AZ 주 목적 | 고가용성 |

중요:

```text
Region 장애 대응
≠
AZ 장애 대응
```

Multi-AZ는 Region 내부의 AZ 장애 대응이다.

### 실무 배치

좋지 않은 구조:

```text
AZ A

EC2
 ↓
EC2
 ↓
Database
```

AZ A 장애 시 전체 서비스 장애.

일반적인 구조:

```text
              Internet
                 │
                ALB
              /     \
           AZ A      AZ B
            │          │
          EC2        EC2
             \        /
              \      /
               RDS
            Multi-AZ
```

### Kubernetes와 연결

```text
EKS Cluster

AZ A
 └ Node

AZ B
 └ Node

AZ C
 └ Node
```

즉 Kubernetes의 고가용성을 AWS의 Multi-AZ 기반 위에서 구현할 수 있다.

### AZ = 데이터센터 하나인가?

정확히는 아니다.

AZ는 하나 이상의 물리적 데이터센터로 구성될 수 있는 **독립된 장애 영역**으로 이해하면 된다.

핵심:

```text
Region
= 큰 지리적 영역

AZ
= Region 내부의 독립된 장애 영역

실무 기본
= Single Region + Multi-AZ
```

---

## 1.2 AWS Account

AWS Account는 단순 로그인 계정이 아니라 **리소스, 비용, 권한을 나누는 큰 관리 경계**다.

```text
AWS Account
│
├─ EC2
├─ S3
├─ RDS
├─ EKS
└─ IAM
```

### 환경을 Account로 분리

하나의 Account에 Dev/Prod를 모두 넣을 수도 있지만 운영 실수 위험이 커질 수 있다.

```text
AWS Organization
│
├─ Dev Account
├─ Staging Account
└─ Production Account
```

즉:

> Account separation = 큰 단위의 격리

### Account와 Region의 차이

하나의 AWS Account에서 여러 Region을 사용할 수 있다.

```text
AWS Account
│
├─ Seoul Region
├─ Tokyo Region
└─ Virginia Region
```

정리:

```text
Account
= 관리 / 권한 / 비용 경계

Region
= 지리적 배치 영역
```

### Account ID

AWS Account에는 12자리 고유 Account ID가 있다.

예:

```text
123456789012
```

ARN 예:

```text
arn:aws:iam::123456789012:role/MyRole
```

### Root User

Root User는 Account의 최상위 사용자다.

```text
AWS Account
   │
 Root User
```

실무에서는 평소 운영에 Root User를 쓰지 않는 것이 기본이다.

```text
Root User
→ 초기 설정 / 매우 제한된 작업

IAM / SSO
→ 평소 운영
```

### IAM User와 Account

```text
AWS Account
│
├─ IAM User A
├─ IAM User B
└─ IAM Role
```

비유:

```text
회사 = AWS Account
직원 계정 = IAM User
직책 / 임시 권한 = IAM Role
```

### AWS Organizations

여러 Account를 중앙에서 관리할 수 있다.

```text
AWS Organizations
│
├─ Management Account
├─ Dev Account
├─ Prod Account
├─ Security Account
└─ Data Account
```

### OU

Organizational Unit.

Account들의 그룹/폴더.

```text
AWS Organization
│
├─ Production OU
│   ├─ AI Platform Prod
│   └─ Data Platform Prod
│
└─ Non-Production OU
    ├─ Dev
    └─ Test
```

### SCP

Service Control Policy.

조직 차원에서 Account/OU가 가질 수 있는 권한의 **최대 범위**를 제한한다.

```text
IAM Policy
= 실제 권한 부여

SCP
= 조직 차원의 최대 허용 범위 제한
```

SCP 자체가 권한을 부여하는 것은 아니다.

### 비용 분리

Account별로 비용을 보기 쉬워진다.

```text
Dev Account       $1,000
Prod Account      $10,000
Data Account      $5,000
AI Account        $20,000
```

### 정리

```text
AWS Organization
        │
      Account
        │
      Region
        │
        AZ
        │
     Resources
```

정확히는 Account 하나가 여러 Region을 사용할 수 있다.

핵심:

- AWS Account = 리소스 / 비용 / 권한의 큰 관리 경계
- Root User = Account의 최상위 사용자
- AWS Organizations = 여러 Account 중앙 관리
- 실무에서는 Dev / Prod 등을 Account 단위로 분리하는 경우가 많다

---

## 1.3 IAM 기본

IAM = **Identity and Access Management**

> 누가, 어떤 AWS 리소스에, 무엇을 할 수 있는가를 관리하는 시스템

핵심 요소:

```text
IAM User
IAM Role
IAM Policy
```

의미:

```text
User
= 사람 또는 고정 사용자

Role
= 필요할 때 맡는 권한

Policy
= 어떤 행동을 허용/거부할지 정의
```

### IAM User

AWS Account 내부의 사용자.

기업 환경에서는 사람에게 장기 Access Key를 주는 방식보다 SSO / IAM Identity Center + Role을 더 많이 고려한다.

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

의미:

- Effect = Allow
- Action = S3 객체 읽기
- Resource = 특정 Bucket 내부 객체

핵심 필드:

```text
Effect
Action
Resource
Condition
```

### IAM Role

Role은 특정 사용자에 고정된 계정이 아니라 **권한 묶음**이다.

```text
User
  ↓
Assume Role
  ↓
AdminRole
  ↓
관리자 권한
```

### 왜 Role이 필요한가?

나쁜 구조:

```text
EC2
└─ Access Key 저장
```

좋은 구조:

```text
EC2
 ↓
IAM Role
 ↓
S3
```

고정 Access Key를 애플리케이션에 저장하지 않아도 된다.

### Temporary Credential

Role을 사용하면 임시 자격 증명을 받을 수 있다.

```text
Application
    ↓
IAM Role
    ↓
Temporary Credential
    ↓
AWS API
```

일반적으로 포함:

- Access Key
- Secret Key
- Session Token
- Expiration

### EC2 + IAM Role

```text
EC2
 │
 └─ IAM Role
      │
      └─ Policy
           └─ s3:GetObject
```

애플리케이션은 AWS SDK를 통해 Role 기반 임시 Credential을 사용할 수 있다.

### EKS에서는?

Pod가 S3에 접근한다면:

```text
Pod
 ↓
IAM Role
 ↓
S3
```

이를 위해 IRSA 또는 EKS Pod Identity를 사용할 수 있다.

### Trust Policy

Role에는 두 종류의 관점이 있다.

```text
Role
│
├─ Permission Policy
│    └─ 이 Role이 무엇을 할 수 있는가
│
└─ Trust Policy
     └─ 누가 이 Role을 맡을 수 있는가
```

### Least Privilege

필요한 최소 권한만 부여한다.

나쁜 예:

```text
s3:*
Resource: *
```

좋은 예:

```text
s3:GetObject
Resource: my-bucket/*
```

### Allow와 Deny

기본적으로 권한이 없으면 Deny.

명시적인 Deny가 있으면 Allow보다 우선한다.

```text
Explicit Deny
> Allow
```

### 사람 / 서비스 권한 구조

사람:

```text
Developer
    ↓
SSO / Identity Center
    ↓
IAM Role
    ↓
AWS Resource
```

EC2:

```text
EC2
 ↓
IAM Role
 ↓
S3 / DynamoDB / etc
```

EKS Pod:

```text
Pod
 ↓
Pod Identity / IRSA
 ↓
IAM Role
 ↓
AWS Resource
```

### IAM과 Kubernetes RBAC

```text
Pod → Kubernetes API 접근
= Kubernetes RBAC

Pod → S3 접근
= AWS IAM
```

즉:

```text
Kubernetes 내부 권한
= RBAC

AWS 리소스 권한
= IAM
```

---

<!-- SOURCE CORE END -->

## 원문 절별 보완과 정정

공식 문서 확인일: 2026-10-03. 아래는 원문을 적용할 때 확인할 조건이며 실제 계정 생성·권한 부여·장애 시험 결과가 아니다.

### 1.1: AZ 이름과 가용성의 범위

AZ 이름의 문자만으로 서로 다른 Account의 물리적 위치를 비교하지 않는다. 일부 기존 Region·계정에는 이름과 물리적 AZ의 매핑 차이가 남아 있으므로 교차 계정 비교는 AZ ID로 확인한다. 모든 Region에서 이름이 다르게 매핑된다고 일반화해서도 안 된다. [AWS AZ IDs](https://docs.aws.amazon.com/global-infrastructure/latest/regions/az-ids.html)

원문의 Multi-AZ 도식은 설계 예시다. 다른 AZ에 자원을 두는 것만으로 애플리케이션의 복제·라우팅·데이터 failover·잔여 용량까지 자동 검증되지는 않는다. Single Region + Multi-AZ는 Region 전체 장애에 대한 복구 전략과 구분한다. 이는 원문의 장애 영역 구분에 따른 설계 검토 기준이다.

### 1.2: Root와 SCP의 실제 적용 범위

일상 업무에는 federation·임시 자격 증명을 사용하고 root 접근은 제한하며 MFA로 보호한다. “초기 설정”을 모든 구축 작업의 root 실행으로 해석하지 않는다. [AWS IAM 보안 권장 사항](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

SCP는 권한을 부여하지 않는다. Member account의 root도 제한하지만 management account의 사용자·role과 service-linked role에는 적용되지 않는다. Organizations의 all features가 필요하다. 원문의 계층 그림이 모든 리소스가 AZ에 속한다는 뜻도 아니다. IAM처럼 전역 범위의 서비스가 있으므로 리소스별 범위를 따로 확인한다. [AWS SCP](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)

### 1.3: 정책 예제와 Role 자격 증명

원문의 JSON은 `Effect`·`Action`·`Resource`를 설명하는 **Statement 조각**이며 완전한 정책 문서가 아니다. 실제 정책은 `Statement`에 넣고 적절한 정책 언어 `Version` 등을 확인한다. `Condition`은 선택 사항이다. `my-bucket/*`은 객체 범위의 예시이며 bucket 자체 작업의 ARN과 구분한다. [IAM JSON 정책 요소](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html)

Role은 policy 자체가 아니라 assume할 수 있는 IAM identity다. Trust policy와 permission policy를 함께 검토하고 EC2 instance profile, Pod Identity/IRSA 및 SDK credential provider 설정을 확인해야 한다. 임시 자격 증명도 비밀값이며 만료·갱신 처리가 필요하다. 장기 키를 없애는 것만으로 최소 권한이 완성되지 않는다. [AWS IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

Account ID `123456789012`, ARN·bucket 이름, 비용은 설명용 예다. 실제 계정·청구서·측정 결과가 아니다. IAM이 허용해도 [네트워크 경로](networking.md)가 없으면 API 통신은 실패할 수 있으며, 네트워크 연결 성공만으로 IAM 허용을 뜻하지도 않는다.

## LLM 실무 활용

### 계정·장애 영역·권한을 나눠 설계 검토하기

**상황:** 가상 Dev/Prod 서비스가 EC2에서 S3 객체를 읽는다. [플랫폼 보안](../platform-infrastructure/platform-security.md)과 연결해 현재 설계의 경계를 먼저 검토한다.

**LLM에 줄 맥락:** 비식별 Account/Region/AZ ID 배치, 서비스별 장애 요구, role의 trust·permission policy 요약, SDK 자격 증명 방식. 실제 계정 식별자·키·토큰은 제외한다.

**예시 프롬프트:**

=== "한국어"

    ```text {.prompt}
    [맥락]
    가상 Dev/Prod 서비스는 EC2에서 지정 S3 객체를 읽는다.
    배치와 장애 요구: [비식별 Account·Region·AZ ID·복구 조건]
    Role trust/permission policy와 SDK 자격 증명 방식: [비식별 요약]
    [요청]
    현재 구성을 먼저 검토하고 관측·가정·가설·누락 증거를 구분하라.
    계정 격리, AZ 장애, Region 장애, IAM 권한을 각각 평가하라.
    [출력]
    경계 / 현재 근거 / 실패 가능성 / 다음 확인 표를 작성하라.
    Trust와 permission policy를 구분하고 최소 권한 후보를 설명하라.
    [검증]
    Multi-AZ나 Role 사용만으로 복구·접근 성공을 단정하지 말라.
    공식 문서와 실제 비식별 구성으로 사람이 검증할 항목을 제시하라.
    키·토큰을 요구하거나 정책·계정을 변경하지 말라.
    ```

=== "English"

    ```text {.prompt}
    [Context]
    A hypothetical Dev/Prod service reads specified S3 objects from EC2.
    Placement and failure requirements: [sanitized accounts, Regions, AZ IDs, recovery conditions]
    Role trust/permission policies and SDK credential handling: [sanitized summary]
    [Task]
    Review the current design first; separate observations, assumptions, hypotheses, and missing evidence.
    Assess account isolation, AZ failure, Region failure, and IAM permissions separately.
    [Output]
    Create a table: boundary / current evidence / possible failure / next check.
    Distinguish trust from permission policies and explain least-privilege candidates.
    [Checks]
    Do not infer successful recovery or access from Multi-AZ or role use alone.
    List checks for a person to make against official docs and actual sanitized configuration.
    Do not request keys or tokens or change policies or accounts.
    ```

**기대 출력:** 장애 영역과 권한 경계를 분리한 검토표, 실제 동작을 확인할 증거와 미확인 조건.

**LLM이 틀릴 수 있는 부분:** Multi-AZ를 Region 장애 복구로 해석하거나, SCP를 권한 부여로 보거나, trust policy만으로 S3 읽기가 허용된다고 판단할 수 있다.

**검증 방법:** 사람이 AZ ID, 정책 평가, 실제 credential provider와 네트워크 구성을 대조한다. 필요 시험은 승인된 격리 환경에서 별도로 수행한다. 이는 작성한 시나리오이며 실제 모델 응답·AWS 운영 경험의 기록이 아니다.
