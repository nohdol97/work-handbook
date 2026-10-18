# 설명 중심 학습 모드와 공개 배포 검토

## 범위와 권한

기준 커밋은 `972e927de586e95022762619b8026b4f7a4dee6c`다. 최초 재현·수정 기록은 [이전 검토](2026-10-18-explanation-review.md)에 보존했다. 이후 사용자가 “웹에서 학습모드일때는 설명을 위해서 한 페이지에 내용이 많이 들어가도 괜찮아. 잘 이해하는게 우선”, “스킬 자체도 이런 방식을 지키도록 수정하고, 배포까지 진행”을 지시했다. 이 후속 지시는 이전 커밋·배포 금지와 학습 모드 세로 스크롤 금지를 해당 범위에서 대체한다.

정규 한영 Markdown은 변경하지 않는다. 기존 Pages 배포 경로를 사용하며 비공개 설정·권한·자격 증명은 변경하지 않는다. 저장소의 기존 공개 배포 상태는 기준 SHA의 Actions run `39081064145` validate/deploy 성공이었다.

## 최종 동작과 직접 검토

기본 웹 학습 모드는 같은 원문 절의 설명 단위를 한 페이지에서 이어 읽는다. 정의→관계→예제→조건·한계의 맥락을 보존하고 페이지 세로 스크롤을 허용한다. 가로 넘침·내부 스크롤·필수 내용 잘림·작은 글씨로 억지 축소는 허용하지 않는다. 발표 모드는 현재 화면에 맞춘 의미 단위 분할을 유지한다. 두 모드 모두 배경 좌우 클릭/탭·방향키·목차로 이동하며, 본문 선택·링크·입력·드래그는 이동과 분리된다. Page Up/Down·Home/End는 학습 문서의 기본 스크롤 의미를 유지한다.

자동 퀴즈·채점·카드 뒤집기·필수 편집은 제거했다. 문서 발견과 설명 설계를 분리하고 정적 원문을 정상 결과로 둔다. 원문 변경 시 검토된 설계의 fingerprint가 맞지 않으면 정적 원문으로 돌아간다. 이때에도 절 ID가 유지되도록 대표 기술 절의 ID를 원문 레지스트리에 고정했다. 검토 비활성화 시 ID가 달라지는 실패를 단위 테스트로 재현한 뒤 한영8개 등록값을 수정했다. QLoRA는 후반부 설명을 근거로 삼으므로 전체 문서 fingerprint도 검증한다.

| 대표 절 | 무엇/왜/어떻게/예제 결과 이유의 화면 검토 | 한영 대응과 제한 |
|---|---|---|
| Watermark | 이벤트 시각·도착 순서·진행 기준의 차이, 10:01:10/5초/약10:01:05 시간축, 이후 도착10:01:03의 late 분류와 처리 정책 분리 | 같은 설명 ID와 수치·가정. 실제 Flink 공식을 재현한 시뮬레이터가 아니며 window 결과를 단정하지 않음 |
| SG/NACL | 두 기술을 동일 기준 열로 비교, 같은 요청·응답 방향, stateful 차이와 경로 확인 이유 | 머리글·셀 관계 유지. 규칙 허용만으로 통신 성공을 보장하지 않음 |
| Schema Break | BIGINT→STRING 계약 변경, Producer→CDC/Event→Flink/Spark→Silver→dbt→Dashboard 가능 경로, 격리·수정·backfill·검증 이유 | 실제 운영 장애나 모든 단계의 필연적 실패로 표현하지 않음 |
| 영어 check | 뜻·용법·업무 문맥과 예문을 기본 본문에 표시 | 번호 암기나 정오답 선택 없음 |
| Flink 실무 프롬프트 | 용도·입력·의도·기대 출력, 원문 한영 요청과 주의사항, 가정한10:00:20 입력의 interval 소속→count+1 | 요청의 안전 조건 보존. 실제 실행 결과와 구분, 최종 결과는 watermark/정책 의존 |
| QLoRA 전체 흐름 | 원문의10단계·9방향 관계, 준비 이유, frozen base/adapter 갱신, 저장과 평가의 구분, Redis/Kafka 입력→token 예측→loss→adapter 갱신 | 동일4개 단위 ID. loss를 문장 비교 점수로 오해하지 않도록 labels/mask 명시. 개선·승격 보장 없음 |
| Foundations Statistics | min100/max500에서 `>300`은 읽을 가능성, `>500`·`>1000`은 건너뛰기, 초기화1000 | 가능성을 실제 데이터 존재로 단정하지 않음 |

기술 의미는 대표 한영 원문과 근거 절을 직접 대조했다. 디자인은 흰 배경·진한 본문·한 강조색, 본문 폭·정렬·제목 위계·간격을 검토한다. 학습 모드에서 더 긴 페이지 자체를 결함으로 취급하지 않으며, 정보 밀도나 클릭 수를 이해도 향상의 측정값으로 사용하지 않는다.

## 회귀와 확장 정책

기본 모드 부재를 실패로 재현한 뒤 학습 모드를 추가했다. 화면 회전 때 숫자 분할 위치가 달라져 Statistics 결과 패널이 사라지는 실패도 독립적으로 재현했으며, 설명 도구의 의미상 위치와 입력 결과 보존을 회귀 기준으로 삼았다. 전체 학습 절 검사에서 코드 글자 크기가 중첩 스타일로13.536px이 되는 결함을 발견해14.4px로 수정했다. 표를 모바일에서 나눌 때 행/열 머리글·링크·caption을 유지하며 병합 셀·다단 머리글은 임의 평탄화하지 않는다. 검토되지 않은 공간 도식은 원문 표기임을 밝히며 작은 화면 줄바꿈의 공간 배치 한계를 숨기지 않는다.

새 유형의 확대에는 원문 양언어 읽기, 설명상 이점, 필수 내용의 기본 본문 존재, 독립 기대 결과, 실제 화면 검토가 필요하다. 전체 발견·로딩·텍스트 보존·배치 자동 검사는 전 문서의 기술 전문 검토와 구분한다. 초기 구조 기반 한영 절 ID 등록은 번역 의미 승인으로 간주하지 않는다.

스킬과 아키텍처 가이드에도 학습/발표 모드 구분, 정적 설명 기본값, 화면에 드러나는 의미, 독립적인 결과 검증, 검토 경계와 측정 한계를 반영했다.

## 검증·배포 증거

`make finalize`는 exit 0으로 완료됐다. 로그는 로컬 `_workspace/slide-qa/study-finalize.log`다. 절 ID 등록 보강 후 전체 재생성한 HTML167개(덱166개+색인1개)는 브라우저 검사를 통과한 파일과 SHA-256이 모두 동일했다. 따라서 현재 공개 화면에 대한 기존 브라우저 증거가 그대로 적용된다. 추가한 검토 무효화/절 ID 회귀를 포함한 전체 단위 테스트는 별도 최신 실행 `_workspace/slide-qa/study-unittest-final.log`에서 155개 통과했다.

| 명령/표면 | 관찰 결과 | 증명 범위 |
|---|---|---|
| 전체 unittest | 155개 통과 | 생성·원문·설계·레지스트리와 기존 하네스 회귀 |
| source preservation / handbook / English study | 오류0 | 원본 한영 Markdown과 등록 보존 계약 |
| Mermaid / strict MkDocs / check_site / prompts | 통과, 사이트 오류0, 145개 한영 실무 예시 오류0 | 구문·공개 파일/링크·원문 프롬프트 계약 |
| 전체 슬라이드 생성·오프라인 로딩 | 166개 통과 | 발견·빌드·독립 실행; 설명 품질과 구분 |
| 전체 학습 절 순회 | 166문서·4,762절을320/1280px에서 순회, 9,524회 절 방문 | 렌더링 텍스트 누락·가로 넘침·내부 스크롤·잘림·작은 글씨 검사 |
| 학습 모드 전체 관찰 | 9,619개, 실패0·실행 오류0 | 위 순회 + 대표6유형 한영5화면 + Statistics +200%글자/회전 +모드/언어/히스토리 |
| 발표 모드 화면 감사 | 294개 화면 상태, 오류0; 의미 텍스트 기록60개 별도 | 한영 대표 절 전체 분할·최장 결과·목차/노트·확대·회전·키보드·배경 조작 |
| vault byte 검사 | unchanged=283, pending=0 | 검사 시점 first-party Markdown mirror 동일성 |
| skill validator / check_harness / diff check | 통과 | 스킬 형식·운영 계약·공백 오류 |

발표 관찰 JSON의354개 항목을354개 화면 검사로 부풀리지 않는다.60개는 가시 텍스트 기록이다. 전체 로딩과 배치 검사는 전 문서의 전문 의미 승인이나 사용자 이해도 향상 측정이 아니다.

| 입력/상황 | 독립 기대 | 실제 |
|---|---|---|
| min100/max500, `>300` | 읽을 가능성, 존재 미확정 | 한영 학습·발표 화면에서 일치 |
| 같은 범위 `>500`·`>1000` | 건너뛰기 | 일치 |
| 초기화 | 1000 | 일치 |
| 300 입력 후390×844→320×568→844×390→390×844 | 도구·입력300·가능성 결과 유지 | 일치, 숫자 분할 위치 대신 패널 ID로 유지 |
| 학습 PageDown/Home/End | 문서 스크롤, 절 유지 | 일치 |
| 언어/모드·reload·Back/Forward | 같은 의미 절/단위 유지 | 대표 한영 실제 이동에서 일치 |
| 원문 변경으로 검토 무효화 | 정적 원문 복귀, 절 ID 유지 | 한영 대표 기술4절8등록값 회귀 통과 |

배포는 검증된 변경을 두 커밋으로 나누어 기존 `main`의 Pages workflow로 수행한다. 실제 배포 SHA·Actions run·공개 HTTP/브라우저 결과는 최종 응답과 로컬 `_workspace/slide-qa/live/` 증거로 보고한다. 공개 URL은 [슬라이드 목록](https://nohdol97.github.io/work-handbook/slides/)과 [Watermark 학습 페이지](https://nohdol97.github.io/work-handbook/slides/ko/data-platform/flink/#section=watermark&mode=study)다.

## 미검증 범위

브라우저 접근성 트리·키보드·포커스 검사는 실제 VoiceOver 음성 출력을 검증한 것이 아니다. 물리적 iOS/Android 기기와 실제 사용자 이해도 실험은 수행하지 않았다. 모든 공개 문서의 원문 텍스트·구조·배치를 검사하더라도, 대표 절 밖의 모든 기술 설명을 새로 전문 검토했다는 의미는 아니다. 발표 모드의 미검토 대형 블록은 원문 링크와 명시적인 준비 중 상태를 유지할 수 있다. 학습 모드에는 화면 크기를 이유로 본문을 준비 중 문구로 대체하지 않는다.

## 화면 증거 안내

수정 전 이미지는 기준 커밋의 실제 렌더링이다. 학습 모드 수정 후 이미지는 의도한 문서 세로 읽기를 보이도록 전체 페이지로 캡처하며 발표 모드 이미지는 지정 viewport로 캡처한다. 긴 이미지의 높이를 발표 화면의 overflow와 혼동하지 않는다. 대표 비교는 Watermark 모바일, SG/NACL 데스크톱과 모바일, QLoRA 흐름이며 Statistics300의 가장 긴 결과도 따로 보관한다. 최종 선택 이미지는 `screenshots/`에, 전체 크기·언어 조합과 감사 JSON은 로컬 `_workspace/slide-qa/study/`에 보관한다.

| 화면 | 수정 전 | 수정 후 |
|---|---|---|
| Watermark 모바일390×844 | [카드·좁은 본문](screenshots/before-watermark-mobile.png) | [학습 페이지](screenshots/study-watermark-ko-390x844.png) |
| Watermark 데스크톱1280×720 | [기존 화면](screenshots/before-watermark-desktop.png) | [학습 페이지](screenshots/study-watermark-ko-1280x720.png) |
| SG/NACL 모바일390×844 | [기존 비교](screenshots/before-sg-nacl-mobile.png) | [머리글·요청·응답 설명](screenshots/study-sg-nacl-ko-390x844.png) |
| SG/NACL 데스크톱1280×720 | [기존 비교](screenshots/before-sg-nacl-desktop.png) | [학습 페이지](screenshots/study-sg-nacl-ko-1280x720.png) |
| QLoRA 모바일390×844 | [노드 버튼 격자](screenshots/before-qlora-mobile.png) | [방향 관계·원인·예시](screenshots/study-qlora-flow-ko-390x844.png) |
| QLoRA 영어 데스크톱 | — | [동일 설명·한계](screenshots/study-qlora-flow-en-1280x720.png) |
| Statistics 긴 결과300 | — | [모바일](screenshots/statistics-study-ko-390x844.png), [데스크톱](screenshots/statistics-study-ko-1280x720.png) |

나머지 대표 화면: [Schema Break](screenshots/study-schema-break-en-390x844.png), [영어 check](screenshots/study-vocab-check-en-390x844.png), [실무 프롬프트](screenshots/study-flink-01-ko-390x844.png).

발표 모드의 화면 내 구성: [Watermark 모바일](screenshots/presentation-watermark-ko-390x844.png), [Watermark 데스크톱](screenshots/presentation-watermark-ko-1280x720.png), [SG/NACL 영어](screenshots/presentation-sg-nacl-en-390x844.png), [QLoRA 320px](screenshots/presentation-qlora-ko-320x568.png). 이전 검토의 QLoRA 대표 흐름 준비 중 상태는 이번에 설명 단위를 검토하여 해소했다.

발표 모드의 긴 Statistics300 결과: [모바일](screenshots/presentation-statistics-300-390x844.png), [데스크톱](screenshots/presentation-statistics-300-1280x720.png).
