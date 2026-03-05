"""
航大思考32 検証スクリプト
問1: 透明シートの重ね合わせ（4×4グリッド、90°回転+重ね合わせ）
問2: 立方体の切断面（一辺6の立方体、3辺の中点を通る平面）
"""

import math

def verify_q1():
    """
    問1: 透明シートの重ね合わせ
    シートA を時計回りに90度回転させた後、シートB に重ねる。
    正解番号: 4
    """
    print("=" * 60)
    print("問1: 透明シートの重ね合わせ")
    print("=" * 60)

    # シートA (4×4, 1=黒, 0=白)
    sheet_a = [
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
    ]

    # シートB (4×4)
    sheet_b = [
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
    ]

    def rotate_cw(grid):
        """90度時計回り回転: new(r,c) = old(3-c, r)"""
        n = len(grid)
        return [[grid[n - 1 - c][r] for c in range(n)] for r in range(n)]

    def rotate_ccw(grid):
        """90度反時計回り回転: new(r,c) = old(c, 3-r)"""
        n = len(grid)
        return [[grid[c][n - 1 - r] for c in range(n)] for r in range(n)]

    def rotate_180(grid):
        """180度回転: new(r,c) = old(3-r, 3-c)"""
        n = len(grid)
        return [[grid[n - 1 - r][n - 1 - c] for c in range(n)] for r in range(n)]

    def overlay(g1, g2):
        """OR演算で重ね合わせ"""
        n = len(g1)
        return [[1 if g1[r][c] or g2[r][c] else 0 for c in range(n)] for r in range(n)]

    def print_grid(grid, label=""):
        if label:
            print(f"  {label}:")
        for row in grid:
            print("    " + " ".join("■" if x else "." for x in row))
        print()

    # シートAの各回転を計算
    a_cw = rotate_cw(sheet_a)
    a_ccw = rotate_ccw(sheet_a)
    a_180 = rotate_180(sheet_a)

    print_grid(sheet_a, "シートA（元）")
    print_grid(sheet_b, "シートB")
    print_grid(a_cw, "シートA 90°CW回転")

    # 正解: CW回転 + B
    correct = overlay(a_cw, sheet_b)
    print_grid(correct, "正解（CW + B）")

    # 選択肢を構成
    # (1): 回転なし + B
    opt1 = overlay(sheet_a, sheet_b)
    # (2): CCW + B
    opt2 = overlay(a_ccw, sheet_b)
    # (3): 180° + B
    opt3 = overlay(a_180, sheet_b)
    # (4): 正解（CW + B）
    opt4 = correct
    # (5): CW + B だが1セル異なる
    a_cw_error = [row[:] for row in a_cw]
    # (2,0) を (2,3) に変更
    a_cw_error[2][0] = 0
    a_cw_error[2][3] = 1
    opt5 = overlay(a_cw_error, sheet_b)

    options = [opt1, opt2, opt3, opt4, opt5]

    print("各選択肢:")
    for i, opt in enumerate(options, 1):
        label = "← 正解" if i == 4 else ""
        print_grid(opt, f"選択肢({i}) {label}")

    # 一意性確認: 各選択肢が異なることを確認
    for i in range(5):
        for j in range(i + 1, 5):
            assert options[i] != options[j], f"選択肢({i+1})と({j+1})が同一です！"

    # 正解が(4)であることを確認
    assert options[3] == correct, "正解が(4)ではありません"

    print("問1: 検証OK - 解は唯一、全選択肢が異なる")
    print(f"正解: (4)")
    print()
    return 4


def verify_q2():
    """
    問2: 立方体の切断面
    一辺6の立方体 ABCD-EFGH
    A(0,0,0), B(6,0,0), C(6,6,0), D(0,6,0)
    E(0,0,6), F(6,0,6), G(6,6,6), H(0,6,6)

    P = ABの中点 = (3,0,0)
    Q = CGの中点 = (6,6,3)
    R = EHの中点 = (0,3,6)

    切断面の形状と面積を求める。
    正解番号: 1
    """
    print("=" * 60)
    print("問2: 立方体の切断面")
    print("=" * 60)

    # 頂点定義
    A = (0, 0, 0)
    B = (6, 0, 0)
    C = (6, 6, 0)
    D = (0, 6, 0)
    E = (0, 0, 6)
    F = (6, 0, 6)
    G = (6, 6, 6)
    H = (0, 6, 6)

    # 切断点
    P = (3, 0, 0)   # ABの中点
    Q = (6, 6, 3)   # CGの中点
    R = (0, 3, 6)   # EHの中点

    print(f"P (AB中点) = {P}")
    print(f"Q (CG中点) = {Q}")
    print(f"R (EH中点) = {R}")

    # 平面の方程式: ax + by + cz = d
    # ベクトル PQ, PR
    PQ = tuple(Q[i] - P[i] for i in range(3))
    PR = tuple(R[i] - P[i] for i in range(3))
    print(f"PQ = {PQ}")
    print(f"PR = {PR}")

    # 法線ベクトル = PQ × PR
    n = (
        PQ[1] * PR[2] - PQ[2] * PR[1],
        PQ[2] * PR[0] - PQ[0] * PR[2],
        PQ[0] * PR[1] - PQ[1] * PR[0],
    )
    print(f"法線ベクトル = {n}")

    # 簡約化
    from math import gcd
    g = gcd(gcd(abs(n[0]), abs(n[1])), abs(n[2]))
    n_simplified = (n[0] // g, n[1] // g, n[2] // g)
    print(f"法線ベクトル（簡約） = {n_simplified}")

    # 平面: n_simplified · (point - P) = 0
    # n[0](x-3) + n[1](y) + n[2](z) = 0
    # n[0]x + n[1]y + n[2]z = 3*n[0]
    d_val = n_simplified[0] * P[0] + n_simplified[1] * P[1] + n_simplified[2] * P[2]
    print(f"平面方程式: {n_simplified[0]}x + ({n_simplified[1]})y + {n_simplified[2]}z = {d_val}")

    # 検証: 各点が平面上にあるか
    for name, point in [("P", P), ("Q", Q), ("R", R)]:
        val = sum(n_simplified[i] * point[i] for i in range(3))
        assert val == d_val, f"{name}が平面上にない: {val} != {d_val}"
        print(f"  {name}: {n_simplified[0]}*{point[0]} + ({n_simplified[1]})*{point[1]} + {n_simplified[2]}*{point[2]} = {val} ✓")

    # 立方体の全辺と平面の交点を求める
    edges = [
        ("AB", A, B), ("BC", B, C), ("CD", C, D), ("DA", D, A),
        ("EF", E, F), ("FG", F, G), ("GH", G, H), ("HE", H, E),
        ("AE", A, E), ("BF", B, F), ("CG", C, G), ("DH", D, H),
    ]

    print("\n立方体の辺と平面の交点:")
    intersection_points = []
    intersection_edges = []

    for name, p1, p2 in edges:
        # パラメトリック: point = p1 + t*(p2-p1), 0 <= t <= 1
        # n · point = d_val
        # n · (p1 + t*(p2-p1)) = d_val
        # n·p1 + t*(n·(p2-p1)) = d_val
        np1 = sum(n_simplified[i] * p1[i] for i in range(3))
        direction = tuple(p2[i] - p1[i] for i in range(3))
        n_dir = sum(n_simplified[i] * direction[i] for i in range(3))

        if n_dir == 0:
            # 辺が平面に平行
            continue

        t = (d_val - np1) / n_dir

        if 0 <= t <= 1:
            point = tuple(p1[i] + t * direction[i] for i in range(3))
            intersection_points.append(point)
            intersection_edges.append(name)
            print(f"  辺{name}: t={t:.4f}, 交点 = ({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})")

    print(f"\n交点の数: {len(intersection_points)}")
    assert len(intersection_points) == 6, f"交点が6個ではなく{len(intersection_points)}個"
    print(f"通過する辺: {', '.join(intersection_edges)}")

    # 正しい巡回順序で並べる: AB→BC→CG→GH→HE→AE
    correct_order = ["AB", "BC", "CG", "GH", "HE", "AE"]
    ordered_points = []
    ordered_edges = []
    for edge_name in correct_order:
        idx = intersection_edges.index(edge_name)
        ordered_points.append(intersection_points[idx])
        ordered_edges.append(edge_name)

    print("\n正しい巡回順序:")
    for i, (name, pt) in enumerate(zip(ordered_edges, ordered_points)):
        print(f"  {name}上: ({pt[0]:.1f}, {pt[1]:.1f}, {pt[2]:.1f})")

    # 各辺の長さを計算
    print("\n切断面の辺の長さ:")
    n_pts = len(ordered_points)
    side_lengths = []
    for i in range(n_pts):
        j = (i + 1) % n_pts
        p1 = ordered_points[i]
        p2 = ordered_points[j]
        dist = math.sqrt(sum((p2[k] - p1[k]) ** 2 for k in range(3)))
        side_lengths.append(dist)
        print(f"  {ordered_edges[i]}上の点 → {ordered_edges[j]}上の点: {dist:.6f}")

    # 全辺が等しいか確認
    expected_side = 3 * math.sqrt(2)
    print(f"\n期待される辺の長さ: 3√2 = {expected_side:.6f}")
    for i, length in enumerate(side_lengths):
        assert abs(length - expected_side) < 1e-10, f"辺{i}の長さが3√2と異なる: {length}"
    print("全ての辺が 3√2 → 正六角形 ✓")

    # 面積の計算: 正六角形の面積 = (3√3/2) * s²
    s = expected_side
    area = (3 * math.sqrt(3) / 2) * s ** 2
    expected_area = 27 * math.sqrt(3)
    print(f"\n面積 = (3√3/2) × (3√2)² = (3√3/2) × 18 = 27√3 = {expected_area:.6f}")
    assert abs(area - expected_area) < 1e-10, f"面積が27√3と異なる: {area}"
    print("面積 = 27√3 ✓")

    # 選択肢の検証
    print("\n選択肢:")
    print("(1) 正六角形、面積 27√3  ← 正解")
    print("(2) 正三角形、面積 27√3")
    print("(3) 長方形、面積 36√2")
    print("(4) 正六角形、面積 54√3")
    print("(5) ひし形、面積 36")

    # 誤答の検証
    # (2) 正三角形PQR: P(3,0,0), Q(6,6,3), R(0,3,6)
    pq = math.sqrt(sum((Q[i] - P[i]) ** 2 for i in range(3)))
    qr = math.sqrt(sum((R[i] - Q[i]) ** 2 for i in range(3)))
    rp = math.sqrt(sum((P[i] - R[i]) ** 2 for i in range(3)))
    print(f"\n三角形PQR: PQ={pq:.4f}, QR={qr:.4f}, RP={rp:.4f}")
    print(f"  PQ = √(9+36+9) = √54 = 3√6 = {3*math.sqrt(6):.4f}")
    tri_area = math.sqrt(3) / 4 * pq ** 2  # 正三角形の場合
    print(f"  三角形PQRは切断面ではない（切断面は6つの辺と交わる六角形）")

    print(f"\n問2: 検証OK - 切断面は正六角形、面積は27√3")
    print(f"正解: (1)")
    return 1


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("\n" + "=" * 60)
    print("検証結果まとめ")
    print("=" * 60)
    print(f"問1 正解: ({q1_answer})")
    print(f"問2 正解: ({q2_answer})")
    print("全検証パス ✓")
