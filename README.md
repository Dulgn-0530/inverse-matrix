# 역행렬 계산 프로그램 (Python)

n × n 정방행렬의 역행렬을 두 가지 방법으로 계산하고 결과를 비교합니다.

- 행렬식(수반행렬) 방법: A^-1 = adj(A) / det(A)
- 가우스-조던 소거법: [A | I] -> [I | A^-1]
- 추가기능: Fraction 정확 계산, 소수/분수 출력 선택, A x A^-1 = I 검증, 입력 예외 처리, 반복 실행

## 실행 방법
Python 3 IDLE에서 `inverse_matrix.py`를 열고 F5(Run Module)를 누릅니다.
별도 설치 없이 표준 라이브러리(fractions)만 사용합니다.
