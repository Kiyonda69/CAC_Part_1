"""
航大思考94 検証スクリプト
問1: 倉庫の保管量特定（制約充足）
問2: プロジェクトスケジューリング（論理推論）
"""
from itertools import permutations

def verify_q1():
    """問1: 5つの倉庫の保管量を特定"""
    print("=== 問1: 倉庫の保管量 ===")
    values = [10, 20, 30, 40, 50]
    solutions = []

    for perm in permutations(values):
        A, B, C, D, E = perm
        if A + B != C + D:          # [ア]
            continue
        if B != C - 20:             # [イ]
            continue
        if A >= E:                  # [ウ]
            continue
        if D >= B:                  # [エ]
            continue
        if E not in [20, 50]:       # [オ]
            continue
        solutions.append((A, B, C, D, E))

    assert len(solutions) == 1, f"解が{len(solutions)}個存在"
    A, B, C, D, E = solutions[0]
    print(f"  唯一解: A={A}, B={B}, C={C}, D={D}, E={E}")
    print(f"  正解: C={C}トン → 選択肢(3)")
    assert C == 40
    return True

def verify_q2():
    """問2: プロジェクトスケジューリング"""
    print("\n=== 問2: プロジェクトスケジューリング ===")
    weeks = [1, 2, 3, 4, 5]
    solutions = []

    for perm in permutations(weeks):
        A, B, C, D, E = perm
        if not (A < C and C - A >= 3):  # [ア]
            continue
        if abs(B - E) != 1:             # [イ]
            continue
        if D in [1, 5]:                 # [ウ]
            continue
        if C <= E:                      # [エ]
            continue
        if A not in [1, 2]:             # [オ]
            continue
        if B % 2 == 0:                  # [カ]
            continue
        if D <= E:                      # [キ]
            continue
        solutions.append((A, B, C, D, E))

    assert len(solutions) == 1, f"解が{len(solutions)}個存在"
    A, B, C, D, E = solutions[0]
    print(f"  唯一解: A=第{A}週, B=第{B}週, C=第{C}週, D=第{D}週, E=第{E}週")
    print(f"  正解: E=第{E}週 → 選択肢(2)")
    assert E == 2
    return True

if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n全問題の検証に成功しました。")
