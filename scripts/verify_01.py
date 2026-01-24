#!/usr/bin/env python3
"""
航大思考1.html の検証コード

問1: パターン認識（図形と点の系列）
問2: グリッド演算（XOR操作）
"""


def verify_q1():
    """
    問1: 図形パターンの検証

    規則1: 外周の多角形の辺が1ずつ増加（3→4→5→6→7）
    規則2: 内部の点が2ずつ増加（1→3→5→7→9）
    """
    print("="*60)
    print("問1: 図形パターンの検証")
    print("="*60)

    # 観察データ
    data = [
        ('A', 3, 1),   # 三角形, 1点
        ('B', 4, 3),   # 四角形, 3点
        ('C', 5, 5),   # 五角形, 5点
        ('D', 6, 7),   # 六角形, 7点
    ]

    # 規則の検証
    print("\n【規則1: 多角形の辺の数】")
    sides = [d[1] for d in data]
    print(f"  {sides}")
    print(f"  差分: {[sides[i+1] - sides[i] for i in range(len(sides)-1)]}")
    next_sides = sides[-1] + 1
    print(f"  → 次の値: {next_sides} (七角形)")

    print("\n【規則2: 点の数】")
    points = [d[2] for d in data]
    print(f"  {points}")
    print(f"  差分: {[points[i+1] - points[i] for i in range(len(points)-1)]}")
    next_points = points[-1] + 2
    print(f"  → 次の値: {next_points}点")

    # 選択肢の検証
    print("\n【選択肢の検証】")
    options = [
        (1, 7, 7),   # 七角形, 7点
        (2, 6, 9),   # 六角形, 9点
        (3, 7, 9),   # 七角形, 9点 ← 正解
        (4, 8, 9),   # 八角形, 9点
        (5, 7, 11),  # 七角形, 11点
    ]

    correct = None
    for opt_num, s, p in options:
        rule1_ok = (s == next_sides)
        rule2_ok = (p == next_points)
        status = "正解" if (rule1_ok and rule2_ok) else "不正解"

        reason = []
        if not rule1_ok:
            reason.append(f"規則1違反(辺={s})")
        if not rule2_ok:
            reason.append(f"規則2違反(点={p})")

        print(f"  ({opt_num}) {s}角形・{p}点 → {status} {', '.join(reason)}")

        if rule1_ok and rule2_ok:
            correct = opt_num

    print(f"\n正解: ({correct})")
    assert correct == 3, f"正解が(3)ではありません"
    return correct


def verify_q2():
    """
    問2: XOR演算の検証

    演算★の規則:
    - 同じ色（黒と黒、白と白）→ 白
    - 異なる色（黒と白、白と黒）→ 黒
    """
    print("\n" + "="*60)
    print("問2: XOR演算の検証")
    print("="*60)

    # 0=白, 1=黒
    def xor_grids(g1, g2):
        """XOR演算（異なる色→黒、同じ色→白）"""
        return [[g1[i][j] ^ g2[i][j] for j in range(3)] for i in range(3)]

    def print_grid(name, g):
        print(f"\n{name}:")
        for row in g:
            print("  " + " ".join(['黒' if c else '白' for c in row]))

    # 例1の検証: A★B
    A = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    B = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]
    expected_AB = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]

    result_AB = xor_grids(A, B)
    print_grid("A", A)
    print_grid("B", B)
    print_grid("A★B (計算結果)", result_AB)
    assert result_AB == expected_AB, "例1の検証失敗"
    print("  → 例1: 検証OK")

    # 問題: E★F
    E = [
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 0]
    ]
    F = [
        [1, 1, 0],
        [0, 0, 1],
        [0, 0, 0]
    ]

    result_EF = xor_grids(E, F)
    print_grid("E", E)
    print_grid("F", F)
    print_grid("E★F (正解)", result_EF)

    # 選択肢の検証
    print("\n【選択肢との照合】")
    options = {
        1: [[0, 1, 0], [0, 0, 0], [0, 0, 0]],  # AND
        2: [[1, 1, 1], [1, 0, 1], [0, 1, 0]],  # OR
        3: [[1, 0, 1], [1, 0, 1], [0, 1, 0]],  # XOR (正解)
        4: [[0, 0, 1], [1, 0, 1], [0, 1, 1]],  # 計算ミス
        5: [[1, 0, 1], [1, 0, 1], [1, 0, 0]],  # 一部異なる
    }

    correct = None
    for opt_num, grid in options.items():
        if grid == result_EF:
            print(f"  ({opt_num}) → 一致 (正解)")
            correct = opt_num
        else:
            print(f"  ({opt_num}) → 不一致")

    print(f"\n正解: ({correct})")
    assert correct == 3, f"正解が(3)ではありません"
    return correct


if __name__ == '__main__':
    verify_q1()
    verify_q2()
    print("\n" + "="*60)
    print("全ての検証が完了しました")
    print("="*60)
