# 🚀 Remote Code Bridge 배포 가이드

회사 컴퓨터에서 집 컴퓨터로 텍스트/코드를 보내기 위해, 이 앱을 웹에 배포해야 합니다. (Streamlit Cloud 사용 - 무료)

## 0. 준비물
- GitHub 계정
- Streamlit Cloud 계정 (GitHub으로 로그인)

## 1. GitHub에 코드 올리기 (공개/Public)
이 폴더의 코드를 GitHub에 올려야 합니다. **공개(Public)** 저장소로 만드세요.
(`.gitignore` 파일이 중요한 비밀번호 파일은 자동으로 제외해주므로 안심하셔도 됩니다.)

1.  **GitHub 접속**: [새 저장소 만들기](https://github.com/new)
2.  **저장소 이름**: `remote-code-bridge` (또는 원하는 이름)
3.  **공개 범위**: 반드시 **Public** 선택 (회사 컴퓨터에서 접근하기 위해)
4.  **Create repository** 클릭.
5.  **코드 푸시** (터미널에 입력):
    *아래 명령어는 예시입니다. GitHub 화면에 나오는 명령어를 참고하세요.*
    ```bash
    git init
    git add .
    git commit -m "첫 배포"
    git branch -M main
    # 아래 주소는 본인의 저장소 주소로 바꿔야 합니다!
    git remote add origin https://github.com/사용자명/remote-code-bridge.git
    git push -u origin main
    ```

## 2. Streamlit Cloud에 배포하기
1.  [Streamlit Cloud](https://streamlit.io/cloud) 접속 및 로그인.
2.  우측 상단 **New app** 클릭.
3.  **Repository**: 방금 만든 `remote-code-bridge` 선택.
4.  **Branch**: `main`.
5.  **Main file path**: `app.py`.
6.  **Deploy!** 클릭. (앱이 실행되다가 에러가 날 겁니다. 정상입니다.)

## 3. 비밀번호 설정 (제일 중요!)
앱이 프라이빗(Private) Google Drive에 접근하려면 아까 만든 **Google 토큰**과 새로 추가된 **앱 접속 비밀번호**가 필요합니다.

1.  앱 화면 오른쪽 하단의 **Manage app** 또는 점 3개 메뉴(**⋮**) > **Settings** 클릭.
2.  **Secrets** 탭 클릭.
3.  내 컴퓨터의 `.streamlit/secrets.toml` 파일을 메모장으로 엽니다.
    - 파일 안에 `app_password = "..."` 부분이 있는지 확인하세요!
4.  내용 **전체**를 복사해서, Streamlit Cloud의 Secrets 입력창에 붙여넣습니다.
5.  **Save** 클릭.

## 4. 사용하기
앱이 자동으로 재시작됩니다. 이제 주소창의 링크만 있으면 어디서든(회사에서도) 접속 가능합니다!
- 회사에서 링크 접속 -> 코드 붙여넣기 -> **Send to Home**
- 집 컴퓨터의 Google Drive 폴더(`1QMU...`)에 파일이 짠! 하고 나타납니다.
