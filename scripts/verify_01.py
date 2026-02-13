#!/usr/bin/env python3
"""
航大思考1 検証コード
問1: 数表の規則性（C=A+B, D=A×B+C）
問2: 二重規則性の数表（cell(i,j) = i² × (2j-1)）
"""

def verify_q1():
    """問1の検証: 表の規則性を確認"""
    print("=" * 50)
    print("問1: 数表の規則性")
    print("=" * 50)
    
    # 表データ
    table = [
        # A, B, C, D
        [1, 3, 4, 7],
        [2, 5, 7, 17],
        [3, 7, 10, None],  # ?を求める
    ]
    
    # 規則1: C = A + B
    print("\n【規則1】C = A + B の検証:")
    for i, row in enumerate(table):
        A, B, C, D = row
        expected_C = A + B
        if C is not None:
            match = "OK" if C == expected_C else "NG"
            print(f"  行{i+1}: {A} + {B} = {expected_C} (実際: {C}) [{match}]")
            assert C == expected_C, f"行{i+1}でC = A + Bが成立しない"
    
    # 規則2: D = A × B + C
    print("\n【規則2】D = A × B + C の検証:")
    for i, row in enumerate(table):
        A, B, C, D = row
        expected_D = A * B + C
        if D is not None:
            match = "OK" if D == expected_D else "NG"
            print(f"  行{i+1}: {A} × {B} + {C} = {expected_D} (実際: {D}) [{match}]")
            assert D == expected_D, f"行{i+1}でD = A×B + Cが成立しない"
    
    # 答えの計算
    A, B, C, _ = table[2]
    answer = A * B + C
    print(f"\n【答え】行3: D = {A} × {B} + {C} = {answer}")
    
    # 列方向の規則性も検証
    print("\n【列方向の検証】")
    col_A = [1, 2, 3]  # +1
    col_B = [3, 5, 7]  # +2
    col_C = [4, 7, 10]  # +3
    col_D = [7, 17, answer]  # +10, +14
    
    print(f"  列A: {col_A} → 差分: {[col_A[i+1]-col_A[i] for i in range(len(col_A)-1)]}")
    print(f"  列B: {col_B} → 差分: {[col_B[i+1]-col_B[i] for i in range(len(col_B)-1)]}")
    print(f"  列C: {col_C} → 差分: {[col_C[i+1]-col_C[i] for i in range(len(col_C)-1)]}")
    print(f"  列D: {col_D} → 差分: {[col_D[i+1]-col_D[i] for i in range(len(col_D)-1)]}")
    
    # 列Dの差分の差分が一定か確認
    d_diff = [col_D[i+1]-col_D[i] for i in range(len(col_D)-1)]
    dd_diff = [d_diff[i+1]-d_diff[i] for i in range(len(d_diff)-1)]
    print(f"  列D差分の差分: {dd_diff} → {'一定' if len(set(dd_diff)) == 1 else '不定'}")
    
    # 唯一解の確認
    print("\n【唯一解の確認】")
    choices = [25, 27, 29, 31, 35]
    valid = []
    for c in choices:
        # 行の規則で検証
        if c == A * B + C:
            valid.append(c)
    assert len(valid) == 1, f"解が{len(valid)}個: {valid}"
    print(f"  選択肢 {choices} のうち、規則を満たすのは {valid[0]} のみ")
    
    return answer


def verify_q2():
    """問2の検証: 二重規則性の数表"""
    print("\n" + "=" * 50)
    print("問2: 二重規則性の数表")
    print("=" * 50)
    
    # 表データ (Noneは空欄)
    #        列1  列2   列3   列4   列5
    table = [
        [1,   3,    5,    7,    9],     # 行1
        [4,   12,   20,   28,   36],    # 行2
        [9,   None, 45,   63,   None],  # 行3 (A, B)
        [16,  48,   None, 112,  144],   # 行4 (C)
    ]
    
    # 規則: cell(i,j) = i² × (2j-1)  (i=1,2,3,4; j=1,2,3,4,5)
    print("\n【規則】cell(i,j) = i² × (2j-1) の検証:")
    for i in range(4):
        row_vals = []
        for j in range(5):
            expected = (i+1)**2 * (2*(j+1)-1)
            actual = table[i][j]
            row_vals.append(expected)
            if actual is not None:
                match = "OK" if actual == expected else "NG"
                print(f"  cell({i+1},{j+1}): {(i+1)}² × {2*(j+1)-1} = {expected} (実際: {actual}) [{match}]")
                assert actual == expected, f"cell({i+1},{j+1})が規則に合わない"
            else:
                print(f"  cell({i+1},{j+1}): {(i+1)}² × {2*(j+1)-1} = {expected} (空欄)")
        print(f"  行{i+1}: {row_vals}")
    
    # 空欄の値を計算
    A = 3**2 * 3  # cell(3,2) = 9 × 3 = 27
    B = 3**2 * 9  # cell(3,5) = 9 × 9 = 81
    C = 4**2 * 5  # cell(4,3) = 16 × 5 = 80
    
    print(f"\n【空欄の値】")
    print(f"  A = cell(3,2) = 3² × 3 = {A}")
    print(f"  B = cell(3,5) = 3² × 9 = {B}")
    print(f"  C = cell(4,3) = 4² × 5 = {C}")
    print(f"  A + B + C = {A} + {B} + {C} = {A + B + C}")
    
    answer = A + B + C
    
    # 行方向の検証
    print("\n【行方向の規則性検証】")
    for i in range(4):
        row = [(i+1)**2 * (2*(j+1)-1) for j in range(5)]
        factor = (i+1)**2
        print(f"  行{i+1}: {row} → {factor} × (1,3,5,7,9)")
    
    # 列方向の検証
    print("\n【列方向の規則性検証】")
    for j in range(5):
        col = [(i+1)**2 * (2*(j+1)-1) for i in range(4)]
        factor = 2*(j+1)-1
        print(f"  列{j+1}: {col} → (1,4,9,16) × {factor}")
    
    # 唯一解の確認
    print("\n【唯一解の確認】")
    choices = [178, 183, 188, 193, 198]
    valid = [c for c in choices if c == answer]
    assert len(valid) == 1, f"解が{len(valid)}個: {valid}"
    print(f"  選択肢 {choices} のうち、正しいのは {valid[0]} のみ")
    
    return answer


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()
    
    print("\n" + "=" * 50)
    print("検証結果サマリー")
    print("=" * 50)
    print(f"問1の答え: {q1_answer}")
    print(f"問2の答え: {q2_answer}")
    print("全検証パス!")
