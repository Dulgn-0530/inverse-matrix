"""
역행렬 계산 프로그램
 1. 행렬 입력 (n x n, 2차원 리스트)
 2. 행렬식(수반행렬) 방식 역행렬
 3. 가우스-조던 소거법 역행렬
 4. 결과 출력 및 비교
 + 추가기능: 분수(정확한 계산) 사용, A x A^-1 = I 검증, 소수/분수 출력 선택, 반복 실행
"""
from fractions import Fraction


# ---------------------------------------------------------------
# 1. 행렬 입력 기능
# ---------------------------------------------------------------
def input_matrix():
    """정수 n을 입력받고 n x n 행렬을 행 단위로 입력받아 2차원 리스트로 반환"""
    while True:
        try:
            n = int(input("행렬의 크기 n을 입력하세요 (n x n): "))
            if n >= 1:
                break
            print("  n은 1 이상의 정수여야 합니다.")
        except ValueError:
            print("  정수를 입력하세요.")

    print(f"{n}개의 행을 한 줄씩 입력하세요 (숫자 {n}개를 공백으로 구분).")
    matrix = []
    i = 0
    while i < n:
        try:
            row = [Fraction(x) for x in input(f"  {i + 1}행: ").split()]
            if len(row) != n:
                print(f"  숫자를 정확히 {n}개 입력하세요.")
                continue
            matrix.append(row)
            i += 1
        except (ValueError, ZeroDivisionError):
            print("  올바른 숫자(정수, 소수, 분수)를 입력하세요.")
    return matrix


# ---------------------------------------------------------------
# 2. 행렬식을 이용한 역행렬
# ---------------------------------------------------------------
def minor(m, i, j):
    """i행 j열을 제거한 소행렬"""
    return [row[:j] + row[j + 1:] for k, row in enumerate(m) if k != i]


def determinant(m):
    """여인수 전개(첫 번째 행 기준)로 행렬식 계산"""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0
    for j in range(n):
        det += ((-1) ** j) * m[0][j] * determinant(minor(m, 0, j))
    return det


def inverse_by_determinant(m):
    """A^-1 = (1/det A) * adj(A). det = 0 이면 ValueError"""
    n = len(m)
    det = determinant(m)
    if det == 0:
        raise ValueError("행렬식이 0이므로 역행렬이 존재하지 않습니다.")
    if n == 1:
        return [[1 / det]]

    # 여인수 행렬을 구한 뒤 전치(= 수반행렬)
    cofactor = [[((-1) ** (i + j)) * determinant(minor(m, i, j))
                 for j in range(n)] for i in range(n)]
    adjugate = [[cofactor[j][i] for j in range(n)] for i in range(n)]
    return [[adjugate[i][j] / det for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------
# 3. 가우스-조던 소거법을 이용한 역행렬
# ---------------------------------------------------------------
def inverse_by_gauss_jordan(m):
    """[A | I] -> [I | A^-1]. 피벗을 못 찾으면 ValueError"""
    n = len(m)
    # 첨가행렬 [A | I]
    aug = [list(m[i]) + [Fraction(int(i == j)) for j in range(n)]
           for i in range(n)]

    for col in range(n):
        # 피벗 선택: 현재 열에서 0이 아닌 행 찾기 (절댓값 최대)
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if aug[pivot][col] == 0:
            raise ValueError("피벗이 0이므로 역행렬이 존재하지 않습니다.")
        aug[col], aug[pivot] = aug[pivot], aug[col]

        # 피벗 행을 피벗 값으로 나누어 피벗을 1로
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]

        # 다른 모든 행의 해당 열을 0으로
        for r in range(n):
            if r != col and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [a - f * b for a, b in zip(aug[r], aug[col])]

    return [row[n:] for row in aug]


# ---------------------------------------------------------------
# 4. 출력 및 비교
# ---------------------------------------------------------------
def fmt(x, as_fraction):
    if as_fraction:
        return str(x)
    return f"{float(x):.4f}"


def print_matrix(m, title, as_fraction=False):
    print(f"[{title}]")
    cells = [[fmt(x, as_fraction) for x in row] for row in m]
    w = max(len(c) for row in cells for c in row)
    for row in cells:
        print("  " + "  ".join(c.rjust(w) for c in row))
    print()


def multiply(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def is_identity(m):
    n = len(m)
    return all(m[i][j] == (1 if i == j else 0)
               for i in range(n) for j in range(n))


def main():
    print("=" * 50)
    print("        역행렬 계산 프로그램")
    print("=" * 50)

    while True:
        A = input_matrix()
        mode = input("출력 형식 선택 (1: 소수, 2: 분수) [기본 1]: ").strip()
        as_fraction = (mode == "2")
        print()
        print_matrix(A, "입력 행렬 A", as_fraction)

        det = determinant(A)
        print(f"행렬식 det(A) = {fmt(det, as_fraction)}\n")

        inv1 = inv2 = None

        # 방법 1: 행렬식
        print("--- 방법 1: 행렬식(수반행렬) 이용 ---")
        try:
            inv1 = inverse_by_determinant(A)
            print_matrix(inv1, "역행렬 (행렬식)", as_fraction)
        except ValueError as e:
            print("오류:", e, "\n")

        # 방법 2: 가우스-조던
        print("--- 방법 2: 가우스-조던 소거법 이용 ---")
        try:
            inv2 = inverse_by_gauss_jordan(A)
            print_matrix(inv2, "역행렬 (가우스-조던)", as_fraction)
        except ValueError as e:
            print("오류:", e, "\n")

        # 비교
        print("--- 결과 비교 ---")
        if inv1 is not None and inv2 is not None:
            if inv1 == inv2:
                print("두 방법으로 계산한 역행렬이 동일합니다.")
            else:
                print("두 방법의 결과가 서로 다릅니다.")
            # 추가기능: A x A^-1 = I 검증
            print("검증 A x A^-1 = I :",
                  "성공" if is_identity(multiply(A, inv1)) else "실패")
        else:
            print("역행렬이 존재하지 않아 비교할 수 없습니다.")

        print()
        if input("다시 실행하시겠습니까? (y/n): ").strip().lower() != "y":
            print("프로그램을 종료합니다.")
            break
        print()


if __name__ == "__main__":
    main()
