# 프로젝트(캡스톤 디자인)
2025년 1학기(4학년 1학기) 프로젝트(캡스톤디자인) 과목의 과제물 내용 정리를 위한 레포지토리입니다.<br>
프로젝트 기획서부터 프로젝트 결과물, 주차별 연구일지를 순차적으로 정리할 계획입니다.

## 💡 프로젝트 소개
이 프로젝트는 프로젝트[캡스톤디자인] 과목의 일환으로 진행된 AI 기반 코드 보안 분석기 캡스톤 프로젝트입니다.<br>
fine-tuning한 CodeBERT 모델에 취약점 데이터셋을 학습시켜 입력된 사용자의 코드를 분석하여 취약점 라벨, 점수, 상세 메시지 등을 생성하고<br>
이를 GPT-3.5-API와 결합하여 보기 좋게 보고서 형식으로 정리된 문구를 API 서비스로 받아볼 수 있습니다.

## 📌 프로젝트 기획서
<a href="https://github.com/tealight03/CapstoneDesign/blob/main/%EC%BA%A1%EC%8A%A4%ED%86%A4%EB%94%94%EC%9E%90%EC%9D%B8_%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B8%B0%ED%9A%8D%EC%84%9C_%EA%B9%80%EB%8B%A4%EB%B9%88.pdf" target="_blank">
AI 기반 코드 보안 분석기 개발 프로젝트 기획서</a>

## ✅ 프로젝트 결과물 사용법
### CLI 환경
<a href="https://pypi.org/project/codeanalyze/0.5/" target="_blank">
<img src="https://github.com/user-attachments/assets/d23838c9-3448-465a-aac5-b71b1e041ce6" width="800"></a><br>
패키지 파일 다운로드를 위하여 pip install codeanalyze==0.5 명령어로 최신 버전 패키지를 로컬에 설치합니다.<br>
버전에 무관하게 무조건 최신 버전을 설치하고 싶다면 pip install codeanalyze 명령어로 설치해도 무방합니다.<br><br>

<img src="https://github.com/user-attachments/assets/b81af47c-ad33-4f07-b90c-e2a27a3d2e0f" width="600"><br>
설치 후, 검사할 코드를 .py 파일에 담아 codeanalyze analyze -f vulnerable.py 명령어를 실행하면<br>
그에 해당하는 예측 결과, 라벨, 보안 점수가 출력됩니다.<br>

```
🛡️ 예측 결과: ⚠️ SQL Injection 취약점 감지
🔖 라벨: SQL_Injection
📊 보안 점수: 30
```
<b>출력 예시</b>

### API 웹사이트
<a href="https://tealight03.github.io/CapstoneDesign/" target="_blank">
<img src="https://github.com/user-attachments/assets/bd5f91f9-099d-4227-b8f7-671340919714" width="600"></a><br>
https://tealight03.github.io/CapstoneDesign/ 로 접속하시면 AI 기반 코드 보안 분석기 웹사이트를 확인할 수 있습니다.<br>
상단의 코드 작성란에 코드를 작성한 후, [분석 요청] 버튼을 누르시면 결과 보고서를 받아볼 수 있습니다.<br><br>

<img src="https://github.com/user-attachments/assets/68973be6-c719-4bc9-b523-ecf013bf22fd" width="600"><br>
<b>출력 예시</b><br>

## 📑 주차별 연구일지
- <b>1주차(3/5 ~ 3/11)</b><br>
  ※ 1주차는 프로젝트 계획 정리를 위해 활용. 연구 내용 X
  
- <b>2주차(3/12 ~ 3/18)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/2week" target="_blank">캡스톤디자인 2주차 연구일지(0318)</a>
  
- <b>3주차(3/19 ~ 3/25)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/3week" target="_blank">캡스톤디자인 3주차 연구일지(0325)</a>

- <b>4주차(3/26 ~ 4/1)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/4week" target="_blank">캡스톤디자인 4주차 연구일지(0401)</a>

- <b>5주차(4/2 ~ 4/8)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/5week" target="_blank">캡스톤디자인 5주차 연구일지(0408)</a>

- <b>6주차(4/9 ~ 4/15)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/6week" target="_blank">캡스톤디자인 6주차 연구일지(0415)</a>

- <b>7주차(4/16 ~ 4/22)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/7week" target="_blank">캡스톤디자인 7주차 연구일지(0422)</a>
  
- <b>7주차(4/23 ~ 4/29)</b><br>
  <a href="https://github.com/tealight03/CapstoneDesign/tree/main/8week" target="_blank">캡스톤디자인 8주차 연구일지(0429)</a>
