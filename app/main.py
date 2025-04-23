import os
import re
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from openai import OpenAI

# FastAPI 앱 생성
app = FastAPI()

# 입력 스키마
class CodeRequest(BaseModel):
    code: str

# 모델 경로를 Hugging Face 경로로 설정
model_path = "davin0706/codebert-finetuned-v5"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# ✅ OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ✅ 점수 매핑
score_map = {
    0: {"label": "SQL_Injection", "score": 30, "msg": "⚠️ SQL Injection 취약점 감지"},
    1: {"label": "Hardcoded_Password", "score": 30, "msg": "⚠️ Hardcoded Password 감지"},
    2: {"label": "XSS", "score": 30, "msg": "⚠️ XSS 취약점 감지"},
    3: {"label": "Safe_Code", "score": 100, "msg": "✅ 완전한 방어 코드 (Safe Code)"},
    4: {"label": "Other", "score": 70, "msg": "⚠️ 잠재적 취약점이 있는 코드 (Other)"}
}

# ✅ 보안 분석 함수
def analyze_code(code_snippet: str):
    inputs = tokenizer(code_snippet, return_tensors="pt", truncation=True, padding="max_length", max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)[0]
        predicted = torch.argmax(probs).item()

        # Safe vs Other 후처리
        if predicted == 3:
            if probs[4].item() > 0.3 and probs[3].item() < 0.7:
                predicted = 4

    return {
        "prediction": score_map[predicted]["msg"],
        "label": score_map[predicted]["label"],
        "security_score": score_map[predicted]["score"]
    }

# ✅ GPT 리포트 생성 함수
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
        max_tokens=1200
    )
    return response.choices[0].message.content

# GPT API 결과에서 label 추출
def extract_label_from_report(report: str) -> str:
    # "**SQL_Injection**", "**XSS**" 등 강조된 취약점 명을 추출
    match = re.search(r"발견된 취약점은\s+\*\*(\w+)\*\*", report)
    if match:
        return match.group(1)

    # 대체 케이스: label이 포함된 단어가 있는지 체크
    for item in score_map.values():
        if item["label"] in report:
            return item["label"]
    
    return None

# ✅ API 엔드포인트
@app.post("/analyze")
def analyze(request: CodeRequest):
    result = analyze_code(request.code)  # CodeBERT 기반 예측
    gpt_report = generate_report(request.code, result["label"])  # GPT 기반 리포트 생성
    gpt_label = extract_label_from_report(gpt_report)  # GPT 리포트에서 라벨 추출

    # GPT 라벨이 CodeBERT와 다르면 덮어쓰기
    if gpt_label and gpt_label in [v["label"] for v in score_map.values()] and gpt_label != result["label"]:
        updated = [v for v in score_map.values() if v["label"] == gpt_label][0]
        result["label"] = updated["label"]
        result["prediction"] = updated["msg"]
        result["security_score"] = updated["score"]

    return {
        "prediction": result["prediction"],
        "label": result["label"],
        "security_score": result["security_score"],
        "report": gpt_report
    }