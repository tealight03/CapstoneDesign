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
    try:
        # 정규식으로 취약점 라벨 추출 시도
        match = re.search(r"취약점(?:은|이)?[^가-힣]{0,5}\*\*['\"]?(.+?)['\"]?\*\*", report)
        if match:
            candidate = match.group(1).strip().replace(" ", "_")
            print(f"🔍 [정규식 매칭] 추출된 candidate: '{candidate}'")

            # 안전한 코드로 판명되었을 경우
            if candidate == "Safe_Code":
                for item in score_map.values():
                    if item["label"] != "Safe_Code" and item["label"] in report:
                        print(f"⚠️ Safe_Code 오탐 감지, 대체 라벨 사용: '{item['label']}'")
                        return item["label"]
            print(f"✅ 최종 선택된 라벨 (정규식 기준): '{candidate}'")
            return candidate

        # fallback: 정규식 실패 시, 본문 내에서 수동 탐색
        for item in score_map.values():
            if item["label"] in report:
                print(f"🔁 [본문 탐색] '{item['label']}' 라벨이 보고서에 직접 포함되어 있음")
                return item["label"]

    except Exception as e:
        print(f"⚠️ extract_label_from_report 예외 발생: {e}")
    
    print("❌ 라벨 추출 실패: None 반환")
    return None

# ✅ API 엔드포인트
@app.post("/analyze")
def analyze(request: CodeRequest):
    # 1. CodeBERT 결과
    bert_result = analyze_code(request.code)

    # 2. GPT 보고서 생성
    gpt_report = generate_report(request.code, label=bert_result["label"])

    # 3. GPT 보고서에서 라벨 추출
    gpt_label = extract_label_from_report(gpt_report)

    # 4. GPT 라벨이 존재하고, CodeBERT 라벨과 다르다면 GPT 결과를 반영
    if gpt_label and gpt_label != bert_result["label"]:
        matched_entry = None

        # 라벨 중 GPT 보고서의 라벨과 일치하는 것이 있는지 확인
        for entry in score_map.values():
            label_key = entry["label"].lower()
            if label_key == gpt_label.lower():
                matched_entry = entry
                break
        # 일치하는 라벨이 있다면 GPT 보고서로 수정
        if matched_entry:
            final = matched_entry
        else:
            # fallback: CodeBERT 결과 사용
            final = {
                "label": bert_result["label"],
                "score": bert_result["security_score"],
                "msg": bert_result["prediction"]
            }
    else:
        # GPT 결과가 없거나 같을 경우, CodeBERT 그대로 사용
        final = {
            "label": bert_result["label"],
            "score": bert_result["security_score"],
            "msg": bert_result["prediction"]
        }

    return {
        "prediction": final["msg"],
        "label": final["label"],
        "security_score": final["score"],
        "report": gpt_report,
        "model_reference": bert_result
    }