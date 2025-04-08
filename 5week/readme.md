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



### 3) 비고
