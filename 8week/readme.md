# 📑 캡스톤디자인 8주차 연구일지(0429)
### 1) 계획
- 보고서 출력 오류 수정
- Swagger UI 수정
- 취약점 분석 보고서 파일 다운로드 기능 구현

### 2) 진행 상황
<img src="https://github.com/user-attachments/assets/5a38ee9f-18da-44c3-b820-81af864c9ec0" width="450"><br>
코드를 계속 이리저리 수정해봐도 라벨과 내용이 일치하지 않는 문제가 해결되지 않아서 뭐가 문제인지 코드를 샅샅이 살펴보았다.<br>
GPT 보고서를 받아와서 보고서 내용 중 취약점 명칭을 잘라낼 때 뭔가 문제가 있는 것 같아서<br>
보고서 내용을 분석하고, 다시 라벨링하는 부분을 일부 수정하였다.<br>

```
def extract_label_from_report(report: str) -> str:
    try:
        # 정규식으로 취약점 라벨 추출 시도
        match = re.search(r"취약점(?:은|이)?[^가-힣]{0,5}\*\*['\"]?(.+?)['\"]?\*\*", report)
        if match:
            candidate = match.group(1).strip().replace(" ", "_")
            print(f"🔍 [정규식 매칭] 추출된 candidate: '{candidate}'")

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
```
<b>extract_label_from_report() function</b><br>
위와 같이 extract_label_from_report() 함수를 수정하면...!<br>

<img src="https://github.com/user-attachments/assets/c1369985-0f00-4fc1-a08e-8773483d3d50" width="450"><br>
이렇게 결과가 서로 매치된다ㅠㅠ 이거 하나 고친다고 너무 애먹었다..<br>
이어서 사용자에게 API 사용법을 알려주기 위한 Swagger UI, 분석 보고서 파일 다운로드 기능을 만들어보자.<br>


<a href="https://ai-powered-code-security-analyzer.onrender.com/docs" target="_blank">
<img src="https://github.com/user-attachments/assets/b2e8424e-c4cd-463b-9aa1-e93ed42d3bc1" width="800"></a><br>

<a href="https://ai-powered-code-security-analyzer.onrender.com/docs" target="_blank">https://ai-powered-code-security-analyzer.onrender.com/docs</a>로 접속하면<br>
위와 같이 기본 설정된 Swagger UI 화면이 보인다. 기본 제공된 화면에서는 사용자가 API를 사용하기에 충분한 정보를 얻기 어려워 보인다.<br>
이 화면을 개발자가 이해하기 수월하도록 이 API 서비스를 활용하는 방법을 상세히 작성해 화면을 수정해보자.<br>

```
# FastAPI 앱 생성(Swagger 문서 정보 포함함)
app = FastAPI(
    title = 'AI 기반 코드 보안 분석기 API',
    description = "CodeBERT와 GPT API를 활용해 코드의 보안 취약점을 자동 탐지하고, 보안 리포트를 생성하는 API입니다.",
    version = "1.0.0",
    contact = {
        "email": "davin0706@gmail.com",
        "url": "https://github.com/tealight03/CapstoneDesign"
    }
)

# 입력 스키마
class CodeRequest(BaseModel):
    code: str = Field(
        ...,
        description = "보안 분석할 소스 코드 (Python)",
        example = "user_input = input('Enter ID: ')\nsql = 'SELECT * FROM users WHERE id = ' + user_input"
    )
    
# 응답 스키마
class AnalyzeResponse(BaseModel):
    prediction: str = Field(..., description="분석 결과 메시지")
    label: str = Field(..., description="예측된 보안 취약점 라벨 (예: SQL_Injection, Safe_Code 등)")
    security_score: int = Field(..., description="0~100 사이의 보안 점수 (낮을수록 취약함)")
    report: str = Field(..., description="GPT API가 작성한 보안 분석 보고서")
    model_reference: dict = Field(..., description="CodeBERT 모델의 원래 예측 결과")
```
<b>수정된 main.py(일부)</b><br>
main.py 내용을 수정하면 docs의 API 서비스 설명에 관한 화면도 변경된다.<br>
보다 상세한 설명을 위해 서비스 소개, API 입력/출력 및 개발자 연락처에 대한 내용을 담았다.<br>

<img src="https://github.com/user-attachments/assets/ce717dca-7e5e-45f7-b002-dbf8a5b6986d" width="1000"><br>
이렇게 내용을 수정해주면 위 화면처럼 변경된 Swagger UI를 확인할 수 있다.<br>

<img src="https://github.com/user-attachments/assets/33ee1eaa-337b-4698-acef-2f873bba5571" width="450"><br>
Schema를 누르면 실제 이 코드의 스키마, 설명문을 읽을 수 있어 어떤 내용이 리턴되는지 확인하여<br>
이를 기반으로 보고서 작성, 결과물 출력 등에 유용하게 활용할 수도 있다.<br>

```
# API 분석 보고서 docx 다운로드
@app.post("/report/docx", 
            summary="DOCX 형식의 취약점 보고서 다운로드", 
            description="""
            입력된 소스 코드를 기반으로 CodeBERT와 GPT API를 활용해 보안 취약점을 분석하여
            취약점 종류, 점수, 설명, 공격 시나리오, 보완 방안이 포함된 분석 보고서를
            Word 파일 형식으로 다운로드할 수 있습니다.
            """
)
def download_docx(request: CodeRequest):
    # 1. 모델 예측 및 리포트 생성
    bert_result = analyze_code(request.code)
    gpt_report = generate_report(request.code, bert_result["label"])
    gpt_label = extract_label_from_report(gpt_report)

    final_label = gpt_label or bert_result["label"]
    final_score = bert_result["security_score"]
    final_msg = bert_result["prediction"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 2. 문서 객체 생성
    doc = Document()
    doc.add_heading("AI 기반 보안 분석 리포트", 0)
    doc.add_paragraph(f"분석 일시: {timestamp}")
    doc.add_paragraph(f"예측된 취약점 라벨: {final_label}")
    doc.add_paragraph(f"보안 점수: {final_score}")
    doc.add_paragraph(f"분석 요약 메시지: {final_msg}")
    doc.add_paragraph("상세 보안 리포트:")
    doc.add_paragraph(gpt_report)

    # 3. 파일 저장
    filename = f"report_{uuid.uuid4().hex[:8]}.docx"
    doc.save(filename)

    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename="Security_Report.docx")
```
<b></b><br>
또한 위 코드를 추가해서 /report/docx 엔드포인트에서 pdf로 정리된 보고서 문서를 다운로드하는 기능을 구현하였다.<br>

<img src="https://github.com/user-attachments/assets/470a64cb-c57c-41ab-a4b6-be469bb69bb4" width="800"><br>
그리고 각 엔드포인트 별로 동작 방식 및 상세 설명을 기입하여 처음 서비스를 이용하는 사용자도 쉽게 이용할 수 있도록 하였다.

### 3) 비고
최종 결과물 발표 시 활용할 CLI 패키지, 웹사이트, VScode 플러그인 개발 후 깃허브 readme.md 파일 내용 다듬고 마무리!
