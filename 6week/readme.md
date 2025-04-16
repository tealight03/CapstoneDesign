# 📑 캡스톤디자인 6주차 연구일지(0415)
### 1) 계획
- ngrok으로 API 서비스 상태 확인
- FastAPI를 활용한 REST API 구현
- GitHub, Hugging Face, Render를 활용한 API 서비스 배포 준비

### 2) 진행 상황
<img src="https://github.com/user-attachments/assets/b0a4ae5f-9fd0-48ef-a8a1-3f692c3cae75" width="650"><br>
API 서버에 배포하기 이전에 먼저 Colab에서 API가 정상적으로 동작되는지 ngrok로 확인부터 해보았다.<br>
ngrok은 로컬에서 제공하는 서비스를 외부에서 접근할 수 있게끔 해주는 서비스인데,<br>
이걸 이용하면 당장 API서버로 서비스를 배포한 상태가 아니더라도 임시적으로 서비스 동작을 점검할 수 있다.<br>

<img src="https://github.com/user-attachments/assets/834aa6c5-ddea-4206-8b5e-e314335e9567" width="800"><br>
ngrok을 이용하기 위해서는 ngrok 인증토큰이 필요해서 ngrok 웹사이트에 로그인한 후,

<img src="https://github.com/user-attachments/assets/8be26f45-947c-4622-903b-5a1a37207d4d" width="800"><br>
[Getting Started] - [Your AuthToken] 에 들어가서 상단의 토큰값을 복사해서

```
!ngrok config add-authtoken <My ngrok AuthToken>
```
명령어를 실행해주면 ngrok으로 서비스를 테스트할 수 있다.<br><br>

<b>[참고]</b><br>
<a href="https://velog.io/@ejaman/%EB%A1%9C%EC%BB%AC-%ED%98%B8%EC%8A%A4%ED%8A%B8-%EC%99%B8%EB%B6%80%EC%97%90%EC%84%9C-%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0-Ngrok" target="_blank">[Velog]로컬 호스트 외부에서 실행하기 Ngrok!</a><br>

```
import requests

#  FastAPI 서버 URL (ngrok 주소 + /analyze)
url = "https://e480-34-125-130-216.ngrok-free.app/analyze"

# ✅ 테스트 코드
code_snippet = '''
user_input = request.args.get("username")
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
'''

# ✅ POST 요청 데이터
payload = {
    "code": code_snippet
}

# ✅ 요청 보내기
response = requests.post(url, json=payload)

# ✅ 응답 출력
print("✅ 상태 코드:", response.status_code)
print("✅ 결과:\n", response.json())
```
<b>test.py</b>
로컬에서 VScode로 위의 테스트 코드를 실행해보았다.

<img src="https://github.com/user-attachments/assets/48ec41bc-44cf-4e30-ac48-a0441f0b2401" width="800"><br>
테스트 코드에 대해 올바른 분석 보고서가 출력된 것으로 보아, API 동작에 문제가 없는 것으로 보인다.<br>
이어서 API 서버 배포 작업을 진행해도 될 것 같다.<br>

원래 계획은 GitHub에 모델과 서비스 배포 파일을 모두 업로드하고 Render로 배포하는 것이었는데,<br>
AI 모델 내의 model.safetensors 파일 용량이 너무 커서 계속 파일 업로드에 실패해서<br>
GitHub에는 서비스 배포 파일만 업로드하고, 모델 파일은 Hugging Face에 업로드해서<br>
Render로 배포하는 방식으로 변경해서 진행할 계획이다.<br>

<img src="https://github.com/user-attachments/assets/991d21b8-24e9-47f0-88c2-750db73f5fe7" width="800"><br>
Hugging Face CLI환경에서 로그인하기 위해서는 인증 토큰이 필요하기 때문에 웹사이트에 접속해서 토큰을 생성해준다.<br>

<img src="https://github.com/user-attachments/assets/fce896dd-fcf6-473d-904f-85f930f6a1ea" width="600"><br>
다른 웹사이트들과 마찬가지로 토큰값은 초기 생성 시밖에 확인할 수 없기 때문에<br>
이 토큰값은 별도로 잘 보관해두어야한다. 절대 다시 확인할 수 없다!<br>

<img src="https://github.com/user-attachments/assets/b5588a0c-cd93-49d5-a37d-d746437e29be" width="800"><br>
토큰값으로 Hugging Face CLI에 로그인해두면 다음에 연동할 때도 자동 인증이 된다.<br>

### 3) 비고
<img src="https://github.com/user-attachments/assets/7ed447f2-6554-4d04-9bf4-a6ca389a0b79" width="600"><br>
토큰 인증 후 Hugging Face CLI 환경으로 모델을 업로드하려고 했는데<br>
파일 용량 때문인지 Hugging Face에도 업로드가 안 된다... 어떻게 하면 해결할 수 있을까<br>
이것저것 시도해봐도 해결이 안 되어서 일단 다음 주차로 넘기고 이어서 진행해야할 것 같다.
