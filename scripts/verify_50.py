"""
セット50 解の一意性検証
問1: 数のピラミッドパターン
問2: 紙折り・穴あけ問題
"""

def verify_problem1():
    """問1: 数のピラミッド
    ルール:
    - 左辺: 行番号 n (1, 2, 3, 4, ...)
    - 右辺: 2n-1 (1, 3, 5, 7, ...)
    - 内部の数: 直上2つの数の和
    問い: 7行目の左から4番目の数は？
    """
    rows = []
    for n in range(1, 9):
        row = [0] * n
        row[0] = n           # 左辺
        row[-1] = 2 * n - 1  # 右辺
        for j in range(1, n - 1):
            row[j] = rows[n - 2][j - 1] + rows[n - 2][j]
        rows.append(row)

    print("=== 問1: 数のピラミッド ===")
    for i, row in enumerate(rows, 1):
        indent = "  " * (8 - i)
        print(f"{indent}Row {i}: {row}")

    answer = rows[6][3]  # 7行目、4番目 (0-indexed: [6][3])
    print(f"\n7行目の左から4番目 = {answer}")
    assert answer == 65, f"期待値65, 実際値{answer}"

    # 選択肢（正解は(2)に配置）
    choices = [47, 65, 56, 61, 72]
    print(f"選択肢: {['({}) {}'.format(i+1, c) for i, c in enumerate(choices)]}")
    print(f"正解: (2) {choices[1]}")

    # 解の一意性: ルールから計算が一意に定まることを確認
    print("解の一意性: ルールが確定的であるため、解は唯一。 ✓")
    return answer


def verify_problem2():
    """問2: 紙折り・穴あけ
    4×4グリッドの正方形の紙を3回折り、穴を開ける。
    折り方:
    1. 右半分を左に折る（垂直中心線）
    2. 下半分を上に折る（水平中心線）
    3. 対角線に沿って折る
    穴の位置: 折り後の(2,1)（三角形の頂点付近）
    展開後: 8つの穴
    """
    print("\n=== 問2: 紙折り・穴あけ ===")

    # 折りの逆変換を追跡
    # 折り1: 右→左（c=3→c=2, c=4→c=1）
    # 折り後: c=1 → {c=1, c=4}, c=2 → {c=2, c=3}
    # 折り2: 下→上（r=3→r=2, r=4→r=1）
    # 折り後: r=1 → {r=1, r=4}, r=2 → {r=2, r=3}

    # 2×2の各セルが対応する元のセル
    quarter_map = {
        (1, 1): [(1,1), (1,4), (4,1), (4,4)],
        (1, 2): [(1,2), (1,3), (4,2), (4,3)],
        (2, 1): [(2,1), (2,4), (3,1), (3,4)],
        (2, 2): [(2,2), (2,3), (3,2), (3,3)],
    }

    # 折り3: 対角線折り（(1,2)が(2,1)に折り重なる）
    # 折り後の見える位置: (1,1), (2,1), (2,2)（三角形）
    # (2,1)の下には元の(2,1)と(1,2)の8層がある
    triangle_map = {
        (1, 1): quarter_map[(1,1)],  # 4層
        (2, 1): quarter_map[(2,1)] + quarter_map[(1,2)],  # 8層
        (2, 2): quarter_map[(2,2)],  # 4層
    }

    print("折り後の三角形の各位置と対応するセル:")
    for pos, cells in triangle_map.items():
        print(f"  位置{pos}: {cells} ({len(cells)}層)")

    # 穴を(2,1)に開ける → 8つの穴
    hole_pos = (2, 1)
    holes = triangle_map[hole_pos]
    print(f"\n穴の位置 {hole_pos} → 展開後の穴: {sorted(holes)}")

    # グリッド表示
    grid = [['.' for _ in range(4)] for _ in range(4)]
    for r, c in holes:
        grid[r-1][c-1] = 'O'

    print("\n展開後のパターン（正解）:")
    for row in grid:
        print("  " + " ".join(row))

    # 正解パターンの確認
    expected = {(1,2), (1,3), (2,1), (2,4), (3,1), (3,4), (4,2), (4,3)}
    assert set(holes) == expected, f"期待値と不一致"
    assert len(holes) == 8, f"穴の数が8でない: {len(holes)}"

    print(f"\n穴の数: {len(holes)} ✓")
    print("解の一意性: 折り方と穴の位置から展開パターンが一意に決まる。 ✓")

    # 誤答パターンの表示
    wrong_patterns = {
        "誤答A（反転）": [(1,1), (1,4), (2,2), (2,3), (3,2), (3,3), (4,1), (4,4)],
        "誤答B（上下辺のみ）": [(1,2), (1,3), (4,2), (4,3)],
        "誤答C（左右辺のみ）": [(2,1), (2,4), (3,1), (3,4)],
        "誤答D（中央4穴）": [(2,2), (2,3), (3,2), (3,3)],
    }

    for name, pattern in wrong_patterns.items():
        grid_w = [['.' for _ in range(4)] for _ in range(4)]
        for r, c in pattern:
            grid_w[r-1][c-1] = 'O'
        print(f"\n{name}:")
        for row in grid_w:
            print("  " + " ".join(row))

    return holes


if __name__ == "__main__":
    verify_problem1()
    verify_problem2()
    print("\n=== 全検証完了 ===")
