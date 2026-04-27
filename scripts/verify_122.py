"""航大思考122 解の一意性検証スクリプト"""

from itertools import product


def verify_q1():
    """問1: 3x3ラテン方陣（形・塗り・点の数）

    マトリクス:
         列1          列2          列3
    行1: △斜1       □黒2        ○空3
    行2: ○黒3       △空1        □斜2
    行3: □空2       ○斜3        ?
    """
    matrix = [
        [('triangle', 'stripe', 1), ('square', 'black', 2), ('circle', 'white', 3)],
        [('circle', 'black', 3), ('triangle', 'white', 1), ('square', 'stripe', 2)],
        [('square', 'white', 2), ('circle', 'stripe', 3), None],
    ]

    shapes = ['circle', 'triangle', 'square']
    fills = ['white', 'stripe', 'black']
    dots = [1, 2, 3]

    valid = []
    for s, f, d in product(shapes, fills, dots):
        candidate = (s, f, d)
        rows = []
        cols = []
        for r in range(3):
            row = [matrix[r][c] if (r, c) != (2, 2) else candidate for c in range(3)]
            rows.append(row)
        for c in range(3):
            col = [matrix[r][c] if (r, c) != (2, 2) else candidate for r in range(3)]
            cols.append(col)

        ok = True
        for line in rows + cols:
            for attr_idx in range(3):
                vals = [item[attr_idx] for item in line]
                if len(set(vals)) != 3:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            valid.append(candidate)

    print(f"問1 候補数: {len(valid)}")
    for v in valid:
        print(f"  解: {v}")
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    assert valid[0] == ('triangle', 'black', 1), f"想定解と不一致: {valid[0]}"
    print("問1 OK: 解は (triangle, black, 1)")


def xor_pattern(p, q):
    return [[p[r][c] ^ q[r][c] for c in range(3)] for r in range(3)]


def verify_q2():
    """問2: 3x3パターンXOR則

    A XOR B = C, D XOR E = F, A XOR D = G, B XOR E = H
    G XOR H = C XOR F = ?
    """
    A = [[1,0,1],[1,1,0],[0,1,0]]
    B = [[1,1,0],[0,1,1],[1,1,1]]
    D = [[0,1,0],[1,0,1],[1,1,1]]
    E = [[1,0,1],[0,1,0],[1,0,0]]

    C = xor_pattern(A, B)
    F = xor_pattern(D, E)
    G = xor_pattern(A, D)
    H = xor_pattern(B, E)

    ans_row = xor_pattern(G, H)
    ans_col = xor_pattern(C, F)
    ans_diag = xor_pattern(xor_pattern(A, E), xor_pattern(B, D))

    assert ans_row == ans_col, f"行/列で結果不一致: {ans_row} vs {ans_col}"

    print(f"  A = {A}")
    print(f"  B = {B}")
    print(f"  C = {C}")
    print(f"  D = {D}")
    print(f"  E = {E}")
    print(f"  F = {F}")
    print(f"  G = {G}")
    print(f"  H = {H}")
    print(f"  ?  = {ans_row}")

    expected = [[1,0,0],[0,1,0],[1,1,0]]
    assert ans_row == expected, f"想定解と不一致: {ans_row}"

    options = [
        [[0,1,1],[1,0,1],[0,0,1]],
        [[1,0,0],[0,1,0],[1,1,1]],
        [[1,1,0],[0,1,0],[1,1,0]],
        [[1,0,0],[0,1,0],[1,1,0]],
        [[0,0,1],[0,1,0],[0,1,1]],
    ]
    matches = [i+1 for i, o in enumerate(options) if o == expected]
    print(f"  選択肢中の一致: {matches}")
    assert matches == [4], f"正解は選択肢4のみであるべき: {matches}"
    print("問2 OK: 解は選択肢(4)")


if __name__ == "__main__":
    print("=== 問1検証 ===")
    verify_q1()
    print()
    print("=== 問2検証 ===")
    verify_q2()
    print()
    print("✓ 全検証通過")
