# 📑 캡스톤디자인 2주차 연구일지(0318)

### 1) 계획
- 취약점 데이터셋 수집(CVE, CWE, OWASP, CodeXGLUE...)
- 데이터셋 전처리
- CodeBert 모델 불러와서 파인 튜닝하기
- 모델 학습

### 2) 진행상황
취약점 데이터셋 수집은 다행히 공개된 데이터셋들이 많아서<br>
이 데이터들을 모델에 학습시키면 원하는 결과가 잘 도출될 것 같다.<br>
아래의 CWE, CVE, CodeXGLUE, OWASP의 데이터셋을 활용할 계획이다.<br><br>

<b>CWE 공식 데이터셋</b><br>
<img src="https://github.com/user-attachments/assets/f1bd2f55-caaf-4f4c-ac1a-04c1e97f9438" width="600"><br>
url = <a href="https://cwe.mitre.org/data/index.html" target="_blank">https://cwe.mitre.org/data/index.html</a>

<b>CVE 공식 데이터셋(JSON)</b><br>
<img src="https://github.com/user-attachments/assets/9b2655cd-95f7-4532-a418-aca851360a30" width="600"><br>
url = <a href="https://nvd.nist.gov/vuln/data-feeds" target="_blank">https://nvd.nist.gov/vuln/data-feeds</a>

<b>CodeXGLUE GitHub</b><br>
<img src="https://github.com/user-attachments/assets/db54dcf2-3964-4b38-bf3a-42db75743d1c" width="600"><br>
url = <a href="https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans" target="_blank">https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans</a>

<b>OWASP Cheat Sheet</b><br>
<img src="https://github.com/user-attachments/assets/0a383d85-740d-4091-8f5c-3fcc33c25e81" width="600"><br>
url = <a href="https://cheatsheetseries.owasp.org/" target="_blank">https://cheatsheetseries.owasp.org/</a>

CodeBERT 모델을 파인튜닝해서 데이터를 모델 학습시킬 계획이라,<br>
Google Colab에서 CodeBERT 모델을 HuggingPace에서 불러와서 파인튜닝하고,<br>
파인튜닝한 모델을 로컬에 다운받아 로컬에서 실행하려고 했지만<br>
로컬에 다운로드하는 과정에서 오류가 발생해서 Google Colab 에서<br>
모델을 다시 불러와 데이터셋을 학습시키는 방식으로 변경하여 진행할 계획이다.<br>

### 3) 비고
<img src="https://github.com/user-attachments/assets/5d06f6e5-05c4-4302-a898-35dd80a37ac3" width="800"><br>
Google Colab 에서 모델 파인튜닝 작업을 정리하고 다운받아서 로컬에서 모델을 학습시키려고 했는데,<br>
모델 가중치, 토크나이저 등등 자꾸 모델 작동시키는데 필요한 요소가 하나씩 누락된 채 다운되어서<br>
몇 번 시도해봤지만 정상적으로 모델을 불러오는데 실패했다.<br>
로컬이 아니라 Google Colab에서 모델을 그대로 불러와 학습시켜야할 것 같다.
