# slides-generator 템플릿 출처와 검토 기록

- 원본: <https://github.com/bmad-labs/skills/tree/69c605f769b9db991e25fc171aa2265ef16dec50/skills/slides-generator/assets/template>
- 저장소: `bmad-labs/skills`
- 고정 리비전: `69c605f769b9db991e25fc171aa2265ef16dec50`
- 검토일: 2026-10-18
- 라이선스: MIT (`LICENSE`, 원본 저장소 루트에서 복사)
- 도입 유형: 사용자가 요청한 템플릿 코드의 수동 선별 도입. Codex Skill 설치가 아니며 `skills.lock.json`의 installed 항목이 아니다.

## 도입 파일

아래 파일은 고정 리비전의 같은 상대 경로에서 내용 변경 없이 복사했다.

| 파일 | 재사용 목적 |
| --- | --- |
| `src/components/Background.jsx` | 슬라이드 배경 표현 |
| `src/components/Navigation.jsx` | 이동, 진행률, 목차 UI |
| `src/components/SlideTransition.jsx` | 전환 및 단계적 공개 애니메이션 |
| `src/index.css` | 반응형 슬라이드 스타일과 레이아웃 유틸리티 |
| `postcss.config.js` | Tailwind/PostCSS 구성 |
| `tailwind.config.js` | 디자인 토큰과 Tailwind 구성 |
| `vite.config.js` | React 개발 빌드 구성 |
| `vite.standalone.config.js` | JS·CSS 인라인 단일 HTML 빌드 구성 |

## 실행 및 외부 동작 검토

원본 템플릿의 전체 실행 파일과 `package.json`을 검토했다. 도입 파일에는 자격 증명 조회, 외부 게시, 원격 데이터 전송, 파일 삭제 명령이 없다. React 구성 요소는 로컬 UI 상태를 처리하며 `Background.jsx`의 SVG 노이즈는 `data:` URL이다. 도입한 빌드 구성은 Vite/React/Tailwind 및 `vite-plugin-singlefile`을 사용한다. `vite.standalone.config.js`의 `vite-plugin-webfont-dl`은 Google Fonts 참조가 있을 경우 빌드 시 폰트를 내려받아 포함할 수 있으므로 빌드의 네트워크 동작과 최종 HTML의 오프라인 동작을 별도로 검증해야 한다.

원본 `package.json`은 React 18, React DOM 18, Framer Motion 11, Lucide React, Vite 6, Tailwind 3, `vite-plugin-singlefile` 등 버전 범위(`^`)를 사용하며 lockfile이 없다. 2026-10-18에 원본 범위로 임시 lockfile을 생성하여 실행한 `npm audit --package-lock-only` 결과는 총 17건(critical 1, high 13, moderate 3)이었다. 이 의존성 명세는 도입하지 않았다. 실제 통합에서 필요한 패키지는 별도 lockfile로 고정하고 감사한다.

## 제외 및 사용 경계

- `App.jsx`는 포함하지 않았다. 빈 슬라이드 목록과 아래의 `ExportModal`에 의존한다.
- `ExportModal.jsx`는 포함하지 않았다. 이미지 캡처 HTML 내보내기는 상호작용을 제거하고, 제목을 HTML에 그대로 삽입하며, 현재 URL을 `fetch`하여 `file://`에서 실패할 수 있다.
- 원본 `index.html`은 Google Fonts CDN 링크와 존재하지 않는 `/vite.svg`를 포함하므로 제외했다.
- 원본 `package.json`의 `export:*` 명령은 템플릿 안에 없는 `export-slides.js`를 가리키므로 포함하지 않았다.
- PDF/PNG 내보내기, 원본 Skill의 설치 지침, 외부 browser Skill 설치 및 GitHub Pages 게시 지침은 도입하지 않았다.

이 디렉터리는 독립적으로 실행하는 애플리케이션이 아니다. Handbook 렌더러가 필요한 구성 요소만 가져와 사용하고, 원본 문서의 내용 검증과 실제 인터랙션 검증은 별도로 수행한다.
