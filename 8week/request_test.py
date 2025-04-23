import requests

# Render에 배포된 API URL
url = "https://ai-powered-code-security-analyzer.onrender.com/analyze"

# 테스트할 코드 예시
code_example = """
cursor.execute("SELECT * FROM users WHERE id = " + user_input)
"""

# POST 요청 보낼 데이터
payload = {
    "code": code_example
}

# 요청 보내기
response = requests.post(url, json=payload)

# 결과 출력
if response.status_code == 200:
    result = response.json()
    print("🛡️ 예측 결과:", result["prediction"])
    print("🔖 라벨:", result["label"])
    print("📊 보안 점수:", result["security_score"])
    print("\n📄 리포트:\n", result["report"])
else:
    print("❌ 요청 실패:", response.status_code)
    print(response.text)