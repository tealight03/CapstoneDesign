# 📑 캡스톤디자인 5주차 연구일지(0408)

### 1) 계획
- 점수 체계 세분화
- GPT 3.5 API 보고서 출력 결과 다듬기
- Fast API로 REST API 구현(1차 작업)

### 2) 진행상황
<img src="https://github.com/user-attachments/assets/12436cb0-2145-45ae-8ed6-2e00eff99e75" width="650"><br>
점수 체계 조정 작업을 하고 있는데 계속 예상하는 결과값과 출력이 다르게 나와서<br>
데이터 추가 학습도 시켜보고, 점수 체계도 바꿔봤지만 결과값이 계속 출력되는 것이 이상해서<br>
3번과 4번의 매핑 순서를 바꾸고 다시 실행해보았다.<br>

<img src="https://github.com/user-attachments/assets/32602fdc-7ec4-4852-bdb5-6ce97ee3fcaf" width="550"><br>
<b>레이블 순서 조정 전</b><br>

<img src="https://github.com/user-attachments/assets/c1e0fd4a-8af6-4b0a-b6a3-c96a794ab794" width="550"><br>
<b>레이블 순서 조정 후</b><br>

그랬더니 이렇게 점수가 확 다르게 나오는 것을 확인할 수 있었다.<br>
예제 1, 2, 3번은 각각 해당하는 레이블이 존재하기에 결과가 알맞게 출력되었지만<br>
4번과 5번은 이에 해당하는 명확한 레이블이 없어서 그전 레이블에 해당하지 않으면<br>
if-else 구문에서 그 다음 레이블로 처리해버리는 것처럼 레이블 매핑 순서에 따라 결과가 바뀌는 것을 확인할 수 있었다.<br>

```
import torch
import torch.nn.functional as F

# ✅ 라벨 및 점수 매핑 딕셔너리
score_map = {
    0: {"label": "SQL_Injection", "score": 30, "msg": "⚠️ SQL Injection 취약점 감지"},
    1: {"label": "Hardcoded_Password", "score": 30, "msg": "⚠️ Hardcoded Password 감지"},
    2: {"label": "XSS", "score": 30, "msg": "⚠️ XSS 취약점 감지"},
    3: {"label": "Safe_Code", "score": 100, "msg": "✅ 완전한 방어 코드 (Safe Code)"}, 
    4: {"label": "Other", "score": 70, "msg": "⚠️ 잠재적 취약점이 있는 코드 (Other)"}
}

def analyze_code(code_snippet):
    inputs = tokenizer(code_snippet, return_tensors="pt", truncation=True, padding="max_length", max_length=128)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)[0]  # 확률로 변환
        predicted = torch.argmax(probs).item()

        # 후처리 로직: Safe_Code vs Other 세분화
        if predicted == 3:  # Safe_Code로 예측됐을 때만 검사
            safe_prob = probs[3].item()
            other_prob = probs[4].item()
            if other_prob > 0.3 and safe_prob < 0.7:
                predicted = 4  # 확신이 부족하면 Other로 판단

    return {
        "prediction": score_map[predicted]["msg"],
        "label": score_map[predicted]["label"],
        "security_score": score_map[predicted]["score"]
    }
```
<b>analyze_code() function</b><br>
위 코드와 같이 모델이 출력한 로짓 값(logits)을 분석하여 더 세밀하게 판단하기 위해<br>
로짓 점수 기반 후처리(logit-based postprocessing) 방식을 이용해<br>
안전한 코드(safe-code)와 또다른 취약점이 내재된 코드(others)를 명확하게 구분하도록 코드를 수정했다.<br>

<b>[참고]</b><br>
<a href="https://i-am-eden.tistory.com/21" target="_blank">Logit이 무엇일까? what is a Logit?[Eden 블로그]</a>

<img src="https://github.com/user-attachments/assets/61ed1b3d-8059-4d4d-bcbe-0c673aad5044" width="550"><br>
코드 수정 후 다시 예제 코드를 실행해보니 이번에는 제대로 결과가 출력되는 것을 확인할 수 있었다.<br>
우선 지금까지 상황으로는 이 점수 체계를 활용하면 올바른 결과가 출력될 것 같다.<br>
이어서 GPT-3.5 API를 활용한 분석 보고서 출력 내용을 다듬어보자.<br><br>

```
def generate_report(code_snippet: str, label: str) -> str:
    prompt = f"""
당신은 보안 분석 전문가입니다.
아래의 소스 코드에서 감지된 취약점은 **'{label}'** 입니다.

[취약 코드]
{code_snippet.rstrip()}


📌 **1. 취약점 설명**  
해당 취약점이 발생한 이유와 코드 구조상 문제점을 설명해주세요.

💣 **2. 공격 시나리오**  
공격자가 해당 코드를 어떻게 악용할 수 있는지 설명해주세요.

🛠 **3. 보완 방법 및 개선된 코드 예시**  
보완 방법을 설명하고, 보완된 코드 예시를 포함해주세요.

✅ **4. 요약된 보안 권고사항**  
요약된 권고사항을 **리스트 형식**으로 정리해주세요.

---

아래 형식으로 리포트를 작성해주세요:

📄 **보안 분석 리포트**

---
"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for code security analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1200  # 최대 출력 길이 여유 있게 확보
    )

    return response.choices[0].message.content
```
<b>generate_report() function</b>
이전에 보고서 출력 양식을 만들었었지만 조금 다급하게 만든 티가 나서<br>
좀 더 예쁘게 출력하게끔 내용을 살짝 다듬었다.<br>

---

### 📄 **보안 분석 리포트**

📌 **1. 취약점 설명**  
해당 코드는 사용자로부터 입력받은 `username` 값을 그대로 쿼리에 삽입하는 방식으로 SQL 쿼리를 구성하고 있습니다. 이는 SQL Injection 공격에 취약한 상황을 만들 수 있습니다. 공격자가 악의적인 SQL 코드를 입력하여 데이터베이스를 조작하거나 민감한 정보를 노출시킬 수 있습니다.

💣 **2. 공격 시나리오**  
공격자는 `username` 파라미터에 `' OR '1'='1' --`와 같은 SQL Injection 페이로드를 전달하여, 원래의 쿼리를 조작하고 모든 사용자의 정보를 반환하는 쿼리로 변조할 수 있습니다. 이를 통해 공격자는 데이터베이스에 저장된 모든 사용자 정보를 열람할 수 있게 됩니다.

🛠 **3. 보완 방법 및 개선된 코드 예시**  
SQL Injection 공격을 방지하기 위해서는 사용자 입력을 안전하게 처리해야 합니다. 이를 위해 파라미터화된 쿼리를 사용하거나 ORM(Object-Relational Mapping)을 활용하는 것이 좋습니다. 아래는 파라미터화된 쿼리를 사용한 개선된 코드 예시입니다.

```python
user_input = request.args.get('username')
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```

위 코드에서 `%s`는 파라미터로 사용자 입력을 전달하는 방식으로, 사용자 입력이 쿼리에 직접 삽입되지 않아 SQL Injection 공격을 방지할 수 있습니다.

✅ **4. 요약된 보안 권고사항**  
- 사용자 입력을 쿼리에 직접 삽입하지 말고, 파라미터화된 쿼리를 사용하거나 ORM을 활용해야 합니다.
- 입력값을 검증하고 필요한 경우 이스케이프 처리를 해야 합니다.
- 데이터베이스 접근 권한을 최소화하고, 보안 패치를 정기적으로 적용해야 합니다.

---

```
# 예제 코드 & 레이블
code = """
user_input = request.args.get('username')
query = "SELECT * FROM users WHERE name = '" + user_input + "'"
"""

label = "SQL_Injection"
```
<b>예제 코드</b><br>
위 코드로 출력 결과를 테스트해보았는데 코드에 알맞게 잘 분석해주고 보고서 내용도 깔끔하게 나와서 보기 좋은 것 같다.<br>

### 3) 비고
특별히 없음. 다음 주차 진행 계획대로 이어서 진행하면 될 것 같다.
