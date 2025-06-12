### Quick Environment Setup
- 키 얻기
  - https://aistudio.google.com 방문 
  - `Get AP Key` > `+ Create API Key` > GCP 프로젝트 선택 > 생성된 키 복사

- 프로젝트 초기화
  - install uv
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
  - 새 프로젝트 생성
    ```bash
    mkdir agent; cd agent; uv init; uv venv; source .venv/bin/activate
    ```
  - 패키지 설치
    ```bash
    uv add google-adk python-dotenv
    ```
  - .env 파일 생성 및 환경 변수 설정
    ```bash
    echo "GOOGLE_API_KEY=your_key_here" > .env
    ```

- Agent Development Kit Web 맛 보기
  - IDE에서 생성한 프로젝트 열기
    - ![image](https://github.com/user-attachments/assets/e6580bf6-e529-4d05-82db-ed01e604406d)
  - 터미널 창 열기
  - adk web 실행
    - ![image](https://github.com/user-attachments/assets/ec8a69ab-78b6-42c4-b9ce-2bdca5aed4e4)

- 참고 자료 확인 
  - [Google ADK - Quickstart](https://google.github.io/adk-docs/get-started/quickstart)
  - [Google ADK - Tutorials](https://google.github.io/adk-docs/tutorials/agent-team/#step-1-your-first-agent-basic-weather-lookup)
  - [adk-samples](https://github.com/google/adk-samples)
