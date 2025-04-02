# 📑 캡스톤디자인 4주차 연구일지(0401)

### 1) 계획
- 모델 데이터셋 추가 학습
- 점수 체계 세분화
- GPT-4 API 연동/보고서 생성 작업

### 2) 진행상황

<b>GPT-4 API 연동</b><br>
<img src="https://github.com/user-attachments/assets/f5d1dfb4-5f9b-45a9-8af3-51fcf236e378" width="800"><br>
OpenAI 공식 웹사이트에 접속해서 로그인을 한 후,<br>

<img src="https://github.com/user-attachments/assets/6edf1f66-6a26-46ba-946d-46a855c6fa67" width="800"><br>
상단 검색창으로 API-KEYS를 검색해서 API key를 받을 수 있는 페이지로 이동한다.<br>

<img src="https://github.com/user-attachments/assets/d2e50e2a-93ea-4ba8-8197-f1448187fcd8" width="800"><br>
여기서 "Create new secret Key"를 눌러 생성한다.<br>

<img src="https://github.com/user-attachments/assets/34c5294d-81d7-4de1-8f59-8f44f771b45d" width="450"><br>
키 이름을 설정해주고 "Create secret key" 버튼을 누르면 키가 생성된다.<br>

<img src="https://github.com/user-attachments/assets/691287c2-7220-4708-b025-a63fba05f5d5" width="450"><br>
생성된 키는 한 번밖에 볼 수 없으므로 반드시 복사해서 키를 저장해두어야한다.<br>
깃허브 등에 올릴 경우에는 .env 파일에 저장해 키를 숨겨야한다.<br>

<img src="https://github.com/user-attachments/assets/b3aaef78-8d9d-444d-bad0-bca8431ae804" width="800"><br>
이후 GPT-4 API를 사용하려고 했는데.. 지금 사용 권한이 없어서 바로 GPT-4 API를 사용할 수가 없다.<br>
우선 GPT-3.5 API를 이용해 만들고, 추후 GPT-4 API로 변경하는 것으로 계획을 수정했다.<br>

<img src="" width="800"><br>

<img src="" width="800"><br>

<img src="" width="800"><br>

### 3) 비고
<img src="https://github.com/user-attachments/assets/b3aaef78-8d9d-444d-bad0-bca8431ae804" width="800"><br>
GPT-4 API를 바로 이용하려니 현재 권한이 없는 상태라 바로 이용이 불가능했다.<br>
따라서, 우선 GPT-3.5 API로 서비스를 만들고, 추후에 GPT-4 API로 다시 업데이트하는 것으로 계획을 수정해야할 것 같다.
