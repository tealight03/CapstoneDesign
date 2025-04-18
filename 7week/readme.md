# 📑 캡스톤디자인 6주차 연구일지(0422)
### 1) 계획
- GitHub, Hugging Face 파일 업로드
- Render로 API 서비스 배포
- API 서비스 환경 점검 / 테스트

### 2) 진행 상황

<img src="https://github.com/user-attachments/assets/35afef81-adff-409e-bb1c-5dfe556b32c6" width="1000"><br>
지난 주차에 이어서 GitHub, Hugging Face에 모델, 배포 파일 업로드 작업을 진행했다.<br>
모델 파일 중 model.safetensors 파일의 용량이 거의 500MB 정도여서 대용량 파일의 업로드가 안 되는 문제 때문에<br>
.gitattributes 파일에 LFS 설정을 해두고, CLI 대신 웹 환경으로 모델 파일을 모두 Hugging Face에 업로드했다.<br>

<img src="https://github.com/user-attachments/assets/a46c8a07-0578-4615-83af-f5a300861f48" width="1000"><br>
현재 Hugging Face에 접속하면 이렇게 codebert-finetuned-v5 모델 폴더에서 내용을 확인해볼 수 있다.<br>
API 배포 웹호스팅은 Render를 이용할 계획이라 내 GitHub와 Hugging Face의 콘텐츠를 바로 결합해서<br>
결과물을 만들어낼 수 있어서 나중에 추가 학습한 모델을 업로드할 때도 이런식으로 업로드하고 연동해서 작업하면 될 것 같다.<br>

<img src="https://github.com/user-attachments/assets/19ec1dc0-a405-44fe-ab0f-009784efe941" width="800"><br>
서비스 정식 배포 이전까지는 Hobby(무료) 요금제로 사용하고, 정식 배포 이후에는 Professional 요금제를 사용할 계획이다.<br>

<img src="https://github.com/user-attachments/assets/92f6f306-d6c5-4970-af6c-7b9457b90a4a" width="1000"><br>
Render에서 웹서비스 프로젝트를 새로 생성하고, 연동할 GitHub와 Hugging Face를 가져와서<br>
서비스를 배포해주면 된다.

<img src="https://github.com/user-attachments/assets/b2671c7f-586f-4dda-a4f4-8fd15747fbcd" width="800"><br>
"Live" 표시가 보이면 이제 정상적으로 서비스가 배포되었다는 의미이다.<br>

### 3) 비고
