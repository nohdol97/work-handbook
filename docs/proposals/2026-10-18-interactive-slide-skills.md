# 외부 인터랙티브 슬라이드 Skill 검토

- 날짜: 2026-10-18
- 대상: 사용자가 지정한 두 오픈소스 Skill
- 결론: bmad의 검토된 템플릿 일부를 고정 리비전으로 수동 선별 도입하고, sylvial928의 교육 활동 설계는 참고한다.

## 조사 결과

| 항목 | slides-generator | interactive-slides |
|---|---|---|
| 저장소·리비전 | [bmad-labs/skills](https://github.com/bmad-labs/skills/tree/69c605f769b9db991e25fc171aa2265ef16dec50/skills/slides-generator) `69c605f769b9db991e25fc171aa2265ef16dec50` | [sylvial928/interactive-slides](https://github.com/sylvial928/interactive-slides/tree/7bb26d4873ea085c3fbe98ec92843d6ed4924831) `7bb26d4873ea085c3fbe98ec92843d6ed4924831` |
| 라이선스 | MIT, 원본 LICENSE 확인 | MIT, 원본 LICENSE 확인 |
| 실행 방식 | React/Vite/Tailwind/Framer Motion, 단일 HTML Vite 빌드 | 지침 중심; 기본 HTML은 GSAP·Chart.js·폰트 CDN 사용 |
| 재사용 가능 | React 전환·디자인·내비게이션·standalone 구성 | 퀴즈·분기·계산기·필터의 학습 활동 구상 |
| Handbook 차이 | 문서별 JSX 수작업 전제; 대량 발견·스키마·원문 추적 없음 | 실행 가능한 공통 렌더러 없음; 오프라인 보장 안 됨 |

## 도입 판단

사용자의 명시적 도입 요청에 따라 bmad 템플릿에서 8개 파일을 원본 byte 그대로 `third_party/slides-generator-template`에 수동 도입하고 MIT LICENSE와 [출처·실행 감사](../../third_party/slides-generator-template/PROVENANCE.md)를 남겼다. 실제 앱은 `SlideTransition`을 import하며 나머지는 이후 검토된 확장용이다. 원본 ExportModal의 이미지 캡처 HTML은 상호작용을 잃고, 파일 URL fetch와 제목 escaping 문제가 있어 사용하지 않는다. 원본 Google Fonts CDN HTML과 존재하지 않는 export 스크립트도 사용하지 않는다.

원본 패키지 범위에 lockfile이 없고 임시 감사에서 취약점 17건(critical 1, high 13, moderate 3)을 확인하여 패키지 명세를 도입하지 않았다. Handbook의 필요한 React·Framer Motion·esbuild·Playwright만 별도 exact 버전과 lockfile로 고정한다. 두 외부 Skill은 자동 설치 허용목록·감사 3종 기록을 충족하지 않으므로 `skills.lock.json`의 자동 설치 항목으로 등록하지 않는다. 이는 사용자가 지시한 수동 선별 도입과 구분한다.

## 적용 경계

공개 문서 발견, Slide Schema, 원문 줄 매핑, 교육 상호작용 선택, 한영 연계, 증분 빌드와 사이트 감사는 Handbook 전용 확장이다. 새 문서별 JSX를 복사해 만들지 않는다. 외부 디자인·전환 패턴을 재사용하되, 내용과 조작의 기술적 정확성은 원문과 실제 브라우저로 따로 검증한다.
