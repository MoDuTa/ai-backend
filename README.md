# MoDuTa AI Backend

모두타(MoDuTa)의 AI 백엔드 저장소입니다. 현재는 협업에 필요한 설정을 담고 있습니다. 서비스 코드와 로컬 실행·테스트 명령은 첫 구현과 함께 추가할 예정입니다.

## 작업 시작하기

1. WBS의 말단 작업 하나를 골라 이슈 하나를 만듭니다. 작업 목적과 완료 기준을 적습니다. [WBS 작업 이슈 열기](https://github.com/MoDuTa/ai-backend/issues/new?template=task.yml)
2. `develop`에서 작업 브랜치를 만듭니다. 이슈, 브랜치, 커밋, PR에 같은 WBS 번호를 사용합니다.
3. `develop`으로 작업 PR을 열고 본문에 `Closes #이슈번호`와 테스트 결과를 적습니다. 다른 서비스가 사용하는 API나 이벤트 형식이 바뀌면 관련 명세를 갱신하고 담당자에게 공유합니다.
4. 배포할 때는 `develop`에서 `main`으로 PR을 엽니다.

아래는 WBS 번호가 `2.3.1`인 작업의 작성 예시입니다.

| 항목 | 예시 |
| --- | --- |
| 이슈·PR 제목 | `[2.3.1] 모델 입력 형식 문서화` |
| 브랜치 | `docs/2.3.1-model-input` |
| 커밋 첫 줄 | `[Docs]_2.3.1/모델 입력 형식 문서화` |

커밋 첫 줄 다음에는 빈 줄을 두고 변경 내용을 적습니다. 브랜치 종류, 커밋 머리말, 여러 저장소의 이슈를 연결하는 방법은 조직 가이드를 따릅니다. [MoDuTa 협업 가이드](https://github.com/MoDuTa/.github/blob/main/CONTRIBUTING.md)
