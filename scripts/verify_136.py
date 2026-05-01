"""
航大思考136 解の一意性検証

問1: 数表の規則性
  各行で A→B→C の変換規則 (×2+1) を適用した数表の空欄を求める

問2: 二次元数列の規則性
  行方向と列方向に異なる規則が存在する4×4数表の空欄を求める
"""

def verify_q1():
    """問1: 数表パターン ×2+1 の規則"""
    # 既知の表
    # A  B   C
    # 2  5  11
    # 3  7  15
    # 4  9   ?
    # 規則: B = 2A+1, C = 2B+1

    table = [
        [2, 5, 11],
        [3, 7, 15],
        [4, 9, None],
    ]

    # 規則の検証
    for row in table[:2]:
        a, b, c = row
        assert b == 2*a + 1, f"規則違反: {a}→{b} ≠ {2*a+1}"
        assert c == 2*b + 1, f"規則違反: {b}→{c} ≠ {2*b+1}"

    # 空欄候補の探索
    solutions = []
    for candidate in range(1, 200):
        a, b = table[2][0], table[2][1]
        if b == 2*a + 1 and candidate == 2*b + 1:
            solutions.append(candidate)

    assert len(solutions) == 1, f"解が{len(solutions)}個: {solutions}"
    print(f"問1 唯一解: {solutions[0]}")
    print(f"  検証: {table[2][0]} → {table[2][1]} (×2+1) → {solutions[0]} (×2+1)")
    return solutions[0]


def verify_q2():
    """問2: 二次元数列 (行方向×2、列A値は2^n-1系列)"""
    # 既知の表
    #      A    B    C    D
    # 行1   1    2    4    8
    # 行2   3    6   12   24
    # 行3   7   14   28   56
    # 行4  15   30    ?  120
    # 列方向規則: 右に行くにつれ×2
    # 行A列の規則: 1→3→7→15 (差分: 2,4,8 = 2^n)

    table = [
        [ 1,  2,  4,   8],
        [ 3,  6, 12,  24],
        [ 7, 14, 28,  56],
        [15, 30, None, 120],
    ]

    # 列方向規則の検証 (各行でA→B→C→Dが×2)
    for i, row in enumerate(table):
        known = [v for v in row if v is not None]
        # row 3は?を除く
        for j in range(len(known)-1):
            if table[i][j] is not None and table[i][j+1] is not None:
                assert table[i][j+1] == 2 * table[i][j], \
                    f"行{i+1}の列規則違反: {table[i][j]}→{table[i][j+1]}"

    # 行A列の規則検証: 差分が 2,4,8,...
    col_a = [row[0] for row in table]
    diffs = [col_a[i+1] - col_a[i] for i in range(len(col_a)-1)]
    print(f"行A列の差分: {diffs}")
    assert diffs == [2, 4, 8], f"差分規則違反: {diffs}"

    # 空欄の探索
    # 行4 A=15 なら C = A × 4 = 60
    solutions = []
    for candidate in range(1, 300):
        row4_a = table[3][0]
        row4_b = table[3][1]
        row4_d = table[3][3]
        # 列規則: B=2A, C=2B=4A, D=2C=8A
        if (row4_b == 2*row4_a and
            candidate == 2*row4_b and
            row4_d == 2*candidate):
            solutions.append(candidate)

    assert len(solutions) == 1, f"解が{len(solutions)}個: {solutions}"
    print(f"問2 唯一解: {solutions[0]}")
    print(f"  検証: A=15 → B=30 → C={solutions[0]} → D=120 (×2ずつ)")
    return solutions[0]


if __name__ == "__main__":
    q1_ans = verify_q1()
    q2_ans = verify_q2()
    print(f"\n=== 正解番号 ===")
    print(f"問1: {q1_ans} → 選択肢(2)")
    print(f"問2: {q2_ans} → 選択肢(2)")
