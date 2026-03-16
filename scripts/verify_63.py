"""
セット63 検証スクリプト
問1: 積み木の投影図（最大個数）
問2: 立方体の切断面の形状
"""
import itertools
import math


def verify_q1():
    """
    問1: 3×3マス目上の積み木の最大個数

    正面図（左からx=1,2,3の最大高さ）: 2, 3, 1
    右側面図（手前からy=1,2,3の最大高さ）: 3, 1, 2

    最大個数 = sum of min(front[x], right[y]) for all (x,y)
    理由: 各セルの高さは front[x] と right[y] の両方以下でなければならない
    """
    front = [2, 3, 1]  # x=1,2,3 の最大高さ
    right = [3, 1, 2]  # y=1,2,3 の最大高さ

    # 最大構成: h(x,y) = min(front[x], right[y])
    max_config = {}
    total = 0
    for x in range(3):
        for y in range(3):
            h = min(front[x], right[y])
            max_config[(x+1, y+1)] = h
            total += h

    print("=== 問1: 積み木の最大個数 ===")
    print(f"正面図の高さ: {front}")
    print(f"右側面図の高さ: {right}")
    print()
    print("最大構成のグリッド (h(x,y) = min(front[x], right[y])):")
    for y in range(1, 4):
        row = [max_config[(x, y)] for x in range(1, 4)]
        print(f"  y={y}: {row}")

    # 検証: 正面図チェック
    for x in range(3):
        max_h = max(max_config[(x+1, y+1)] for y in range(3))
        assert max_h == front[x], f"正面図の列{x+1}が不一致: {max_h} != {front[x]}"

    # 検証: 右側面図チェック
    for y in range(3):
        max_h = max(max_config[(x+1, y+1)] for x in range(3))
        assert max_h == right[y], f"右側面図の列{y+1}が不一致: {max_h} != {right[y]}"

    print(f"\n最大個数: {total}")

    # 全探索で最大解を確認
    max_height = max(max(front), max(right))
    max_total_brute = 0

    for heights in itertools.product(range(max_height + 1), repeat=9):
        grid = {}
        for i, h in enumerate(heights):
            x = i % 3 + 1
            y = i // 3 + 1
            grid[(x, y)] = h

        # 正面図チェック
        valid = True
        for x in range(1, 4):
            if max(grid[(x, yy)] for yy in range(1, 4)) != front[x-1]:
                valid = False
                break
        if not valid:
            continue

        # 右側面図チェック
        for y in range(1, 4):
            if max(grid[(xx, y)] for xx in range(1, 4)) != right[y-1]:
                valid = False
                break

        if valid:
            t = sum(heights)
            if t > max_total_brute:
                max_total_brute = t

    print(f"全探索による最大個数: {max_total_brute}")
    assert total == max_total_brute, f"最大個数が不一致: {total} != {max_total_brute}"
    print("問1 検証OK\n")
    return total


def verify_q2():
    """
    問2: 立方体の切断面

    立方体ABCD-EFGH（辺の長さ6）
    A=(0,0,0), B=(6,0,0), C=(6,6,0), D=(0,6,0)
    E=(0,0,6), F=(6,0,6), G=(6,6,6), H=(0,6,6)

    P: 辺AB上、Aから2の点 → (2,0,0)
    Q: 辺BF上、Bから4の点 → (6,0,4)
    R: 辺GH上、Hから4の点 → (2,6,6)

    切断面の平面方程式: x + y - z = 2
    """
    print("=== 問2: 立方体の切断面 ===")

    # 立方体の頂点
    vertices = {
        'A': (0, 0, 0), 'B': (6, 0, 0), 'C': (6, 6, 0), 'D': (0, 6, 0),
        'E': (0, 0, 6), 'F': (6, 0, 6), 'G': (6, 6, 6), 'H': (0, 6, 6)
    }

    # 与えられた3点
    P = (2, 0, 0)  # 辺AB上、Aから2
    Q = (6, 0, 4)  # 辺BF上、Bから4
    R = (2, 6, 6)  # 辺GH上、Hから4

    # 平面の法線ベクトルを計算
    PQ = (Q[0]-P[0], Q[1]-P[1], Q[2]-P[2])
    PR = (R[0]-P[0], R[1]-P[1], R[2]-P[2])

    normal = (
        PQ[1]*PR[2] - PQ[2]*PR[1],
        PQ[2]*PR[0] - PQ[0]*PR[2],
        PQ[0]*PR[1] - PQ[1]*PR[0]
    )
    print(f"PQ = {PQ}")
    print(f"PR = {PR}")
    print(f"法線ベクトル: {normal}")

    def on_plane(point):
        return abs(point[0] + point[1] - point[2] - 2) < 1e-9

    assert on_plane(P), "P is not on plane"
    assert on_plane(Q), "Q is not on plane"
    assert on_plane(R), "R is not on plane"
    print("平面方程式: x + y - z = 2")

    # 立方体の12辺との交点を求める
    edges = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'),
        ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'E'),
        ('A', 'E'), ('B', 'F'), ('C', 'G'), ('D', 'H')
    ]

    intersection_points = []
    for v1_name, v2_name in edges:
        v1 = vertices[v1_name]
        v2 = vertices[v2_name]
        dx = v2[0] - v1[0]
        dy = v2[1] - v1[1]
        dz = v2[2] - v1[2]

        denom = dx + dy - dz
        if abs(denom) < 1e-9:
            continue

        t = (2 - v1[0] - v1[1] + v1[2]) / denom

        if -1e-9 <= t <= 1 + 1e-9:
            t = max(0, min(1, t))
            point = (
                round(v1[0] + t * dx, 6),
                round(v1[1] + t * dy, 6),
                round(v1[2] + t * dz, 6)
            )
            # 重複チェック
            is_dup = False
            for existing in intersection_points:
                if all(abs(a-b) < 1e-6 for a, b in zip(existing['point'], point)):
                    is_dup = True
                    break
            if not is_dup:
                intersection_points.append({
                    'edge': f"{v1_name}{v2_name}",
                    'point': point,
                    't': t
                })

    print(f"\n交点の数: {len(intersection_points)}")
    for ip in intersection_points:
        p = ip['point']
        print(f"  辺{ip['edge']}: ({p[0]}, {p[1]}, {p[2]}) [t={ip['t']:.4f}]")

    n_sides = len(intersection_points)
    print(f"\n切断面は {n_sides}角形")
    assert n_sides == 6, f"切断面が六角形でない: {n_sides}角形"

    # 辺の長さを計算（順序付け）
    points = [ip['point'] for ip in intersection_points]
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    cz = sum(p[2] for p in points) / len(points)

    def angle_from_center(p):
        dx, dy, dz = p[0]-cx, p[1]-cy, p[2]-cz
        u = (dx - dy) / math.sqrt(2)
        v = (dx + dy + 2*dz) / math.sqrt(6)
        return math.atan2(v, u)

    sorted_points = sorted(points, key=angle_from_center)

    print("\n頂点（順序付き）:")
    for i, p in enumerate(sorted_points):
        print(f"  {i+1}: ({p[0]}, {p[1]}, {p[2]})")

    print("\n辺の長さ:")
    side_lengths = []
    for i in range(len(sorted_points)):
        p1 = sorted_points[i]
        p2 = sorted_points[(i+1) % len(sorted_points)]
        d = math.sqrt(sum((a-b)**2 for a, b in zip(p1, p2)))
        side_lengths.append(round(d, 6))
        print(f"  辺{i+1}-{(i+1)%6+1}: {d:.4f}")

    is_regular = all(abs(s - side_lengths[0]) < 1e-4 for s in side_lengths)
    print(f"\n正六角形: {'Yes' if is_regular else 'No'}")
    unique_lengths = sorted(set(round(s, 2) for s in side_lengths))
    print(f"辺の長さの種類: {unique_lengths}")

    print("問2 検証OK")
    return n_sides


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("\n" + "=" * 50)
    print("検証結果サマリー")
    print("=" * 50)
    print(f"問1 正解: {q1_answer}個 → 選択肢(2)")
    print(f"問2 正解: {q2_answer}角形（六角形）→ 選択肢(2)")
