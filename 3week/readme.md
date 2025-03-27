# 📑 캡스톤디자인 3주차 연구일지(0325)

### 1) 계획
- 전처리한 데이터셋으로 모델 학습
- 추가 데이터셋 수집/전처리/학습
- 모델 학습 결과 확인 및 추가 학습

### 2) 진행 상황
<img src="https://github.com/user-attachments/assets/73e9bb54-5d7b-4952-bb88-235f6c37200f" width="800"><br>
지난 주에 이어, 이번 주에는 파인튜닝한 모델을 불러와 Google Colab에서 모델을 학습시킬 계획이다.<br>
원래는 모델 파일을 다운로드받아서 로컬에서 학습시킬 계획이었지만 로컬에 모델 파일이 하나씩 누락되는 문제로 인해<br>
계획을 변경하여 Colab에서 모델을 학습시키고, 추후에 REST API 서비스 배포를 준비할 때 이어서 처리하는 것으로 계획을 변경했다.<br><br>

<img src="https://github.com/user-attachments/assets/a0131f0b-ae60-415e-b5b7-12a261024efd" width="700"><br>
파이토치로 모델 학습 코드를 짜서 취약점을 분석하고, 취약정도에 따라 점수를 출력하도록 했는데<br>
분명히 잠재적인 SQL Injection이 있는 코드임에도 불구하고 취약점이 없다고 결과가 출력되었다.<br>
채점 기준이 너무 단순한 탓인가 싶어 기준을 좀 더 세분화해서 데이터를 판별하게끔 코드를 수정해서 다시 예제를 실행해보았다.<br><br>

<img src="https://github.com/user-attachments/assets/5f29b163-188e-4759-a05c-59a72484eccf" width="700"><br>
이번에는 코드의 잠재적인 SQL Injection 위험성을 감지해냈다!<br>
그런데 점수가 0, 50, 100으로만 나오니까 너무 모 아니면 도처럼 결과가 출력되는 것 같아서 점수 체계는 좀 더 세분화할 필요가 있을 것 같다.<br>
우선 이어서 다른 취약점들도 잘 캐치하는지 확인하기 위해 추가로 테스트했다.<br>

```
# SQL Injection(취약점 O)
code_1 = """
user_input = request.args.get('username')
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
"""

# Hardcoded Password(취약점 O)
code_2 = """
password = "admin123"
login(user, password)
"""

# XSS(취약점 O)
code_3 = """
@app.route('/search')
def search():
    keyword = request.args.get('q')
    return "<p>" + keyword + "</p>"
"""

# SQL Injection 방지 코드(취약점 X)
code_4 = """
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
"""

# XSS 방지 코드(취약점 X)
code_5 = """
@app.route('/search')
def search():
    keyword = escape(request.args.get('q'))
    return f"<p>{keyword}</p>"
"""

test_cases = [code_1, code_2, code_3, code_4, code_5]

for idx, code in enumerate(test_cases, start=1):
    result = analyze_code(code)
    print(f"[Test Case {idx}] 🔍 결과: {result['prediction']} | 🔐 점수: {result['security_score']}\n")
```
<b>취약점 확인 예제 코드</b><br>

이렇게 취약점 탐지 성능 테스트를 하기 위해서 위 코드를 실행해보았다.<br><br>

<img src="https://github.com/user-attachments/assets/512ec65f-7045-4e70-903c-c3a09ef2e5d1" width="700"><br>
Test Case 2, 4에 대해서 잘못된 결과가 출력되는 것으로 보아,<br>
현재 Hardcoded Password 취약점과 SQL Injection 코드에 대해 학습이 부족해서 잘못된 결과가 출력되는 것 같다.<br>
우선 다른 취약점에 대한 데이터셋을 더 많이 찾아야할 것 같다.<br>

### 3) 비고
당장 모든 취약점에 대한 모든 예제를 충분히 구하기에는 시간적인 무리가 있어서<br>
우선 SQL Injection, Hardcoded Credential, Cross-Site Scripting (XSS) 등 대표적인 취약점만 학습시키고,<br>
그 외의 취약점들은 순차적으로 데이터셋을 더 찾는대로 학습시켜서 모델 성능을 향상시키는 방향으로 수정해야할 것 같다.<br>
