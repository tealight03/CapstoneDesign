# 📑 캡스톤디자인 6주차 연구일지(0415)
### 1) 계획
- FastAPI를 활용한 REST API 구현
- Render를 통해 API 서비스 배포

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
명령어를 실행해주면 ngrok으로 서비스를 테스트할 수 있다.<br>

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



### 3) 비고
