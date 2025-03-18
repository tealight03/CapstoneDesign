from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ✅ Fine-tuned CodeBERT 모델 로드 (옵션 없이 실행)
model_path = r"D:\대학교\대학생활\\4학년\\1학기\프로젝트(캡스톤디자인)\codebert_model"

model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

print("✅ Fine-tuned CodeBERT 모델 로드 완료!")