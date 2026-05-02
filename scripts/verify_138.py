"""
航大思考138 解の一意性検証スクリプト

問1: 3×3矢印グリッドを反時計回り90°回転した後の配置
問2: 立方体の主対角線に垂直な断面形状の検証
"""

import math


# ===== 問1の検証 =====

def verify_q1():
    """
    3×3グリッドの矢印（0=右, 1=上, 2=左, 3=下）を
    反時計回り90°回転したとき、どの配置になるか検証する。
    """
    # 元のグリッド (0-indexed, 0=右→, 1=上↑, 2=左←, 3=下↓)
    # 行1: → ↑ ←
    # 行2: ↑ → ↓
    # 行3: → → ↑
    original = [
        [0, 1, 2],
        [1, 0, 3],
        [0, 0, 1],
    ]

    n = 3

    def rotate_ccw(d):
        """矢印方向を反時計回り90°回転: →↑, ↑←, ←↓, ↓→"""
        return (d + 1) % 4

    # CCW 90°回転: new[r][c] = rotate_ccw(old[c][n-1-r])
    # 根拠: 紙をCCW回転すると、旧右列が新上行になり、矢印方向もCCW回転する
    def ccw_90(grid):
        result = [[None]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                result[r][c] = rotate_ccw(grid[c][n-1-r])
        return result

    def cw_90(grid):
        """時計回り90°: new[r][c] = rotate_cw(old[n-1-c][r])"""
        result = [[None]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                result[r][c] = (grid[n-1-c][r] + 3) % 4
        return result

    def rot_180(grid):
        result = [[None]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                result[r][c] = (grid[n-1-r][n-1-c] + 2) % 4
        return result

    def mirror_lr(grid):
        """左右反転: →↔←, ↑/↓は変わらず"""
        def flip(d):
            if d == 0: return 2  # →→←
            if d == 2: return 0  # ←→→
            return d
        result = [[None]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                result[r][c] = flip(grid[r][n-1-c])
        return result

    def mirror_ud(grid):
        """上下反転: ↑↔↓, →/←は変わらず"""
        def flip(d):
            if d == 1: return 3  # ↑→↓
            if d == 3: return 1  # ↓→↑
            return d
        result = [[None]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                result[r][c] = flip(grid[n-1-r][c])
        return result

    names = {0: '→', 1: '↑', 2: '←', 3: '↓'}

    def show(grid, label):
        print(f"  {label}:")
        for row in grid:
            print("  " + " ".join(names[d] for d in row))

    correct = ccw_90(original)

    print("=== 問1 検証 ===")
    show(original, "元のグリッド")
    show(ccw_90(original), "CCW 90° (選択肢4・正解)")
    show(cw_90(original), "CW 90° (選択肢1)")
    show(rot_180(original), "180° (選択肢2)")
    show(mirror_lr(original), "左右反転 (選択肢3)")
    show(mirror_ud(original), "上下反転 (選択肢5)")

    # 全選択肢が異なることを確認
    candidates = [
        cw_90(original),
        rot_180(original),
        mirror_lr(original),
        correct,
        mirror_ud(original),
    ]
    labels = ["選択肢1(CW90)", "選択肢2(180)", "選択肢3(LR反転)",
              "選択肢4(CCW90=正解)", "選択肢5(UD反転)"]

    for i in range(len(candidates)):
        for j in range(i+1, len(candidates)):
            assert candidates[i] != candidates[j], \
                f"{labels[i]} と {labels[j]} が同じ配置!"
    print("\n  全5選択肢が異なることを確認: OK")
    print("\n  正解: 選択肢(4) - 反時計回り90°回転")
    return True


# ===== 問2の検証 =====

def verify_q2():
    """
    一辺1の立方体を主対角線に垂直な平面で重心を通るように切断。
    断面が正六角形になることを数値的に検証する。
    """
    print("\n=== 問2 検証 ===")
    print("  一辺1の立方体, 主対角線: (0,0,0)→(1,1,1)")
    print("  切断平面: x+y+z=1.5 (重心(0.5,0.5,0.5)を通り, 方向(1,1,1)に垂直)")

    # 切断面と辺の交点を求める
    # 立方体の12辺を列挙
    vertices = [(i, j, k) for i in (0, 1) for j in (0, 1) for k in (0, 1)]
    edges = []
    for v1 in vertices:
        for v2 in vertices:
            diff = sum(abs(v1[i]-v2[i]) for i in range(3))
            if diff == 1 and v1 < v2:
                edges.append((v1, v2))

    intersections = []
    for (x1, y1, z1), (x2, y2, z2) in edges:
        # パラメトリック: P = (x1,y1,z1) + t*((x2,y2,z2)-(x1,y1,z1))
        # x+y+z = 1.5 を解く
        dx, dy, dz = x2-x1, y2-y1, z2-z1
        denom = dx + dy + dz
        if denom == 0:
            continue
        t = (1.5 - (x1+y1+z1)) / denom
        if 0 < t < 1:
            px = x1 + t*dx
            py = y1 + t*dy
            pz = z1 + t*dz
            intersections.append((round(px, 6), round(py, 6), round(pz, 6)))

    print(f"\n  切断平面と辺の交点 ({len(intersections)}個):")
    for p in sorted(intersections):
        print(f"    {p}")

    assert len(intersections) == 6, f"交点が{len(intersections)}個 (6個のはず)"

    # 全辺長を計算して正六角形か確認
    pts = intersections
    # 辺長: 連続する2点間の距離（順序付きが必要）
    # まず重心で平面上に投影し、角度でソート
    cx = sum(p[0] for p in pts) / 6
    cy = sum(p[1] for p in pts) / 6
    cz = sum(p[2] for p in pts) / 6

    # 平面 x+y+z=1.5 の正規直交基底
    n_vec = [1/math.sqrt(3)] * 3
    # 基底ベクトル1: (1,-1,0)/√2
    e1 = [1/math.sqrt(2), -1/math.sqrt(2), 0]
    # 基底ベクトル2: (1,1,-2)/√6
    e2 = [1/math.sqrt(6), 1/math.sqrt(6), -2/math.sqrt(6)]

    def project(p):
        dp = (p[0]-cx, p[1]-cy, p[2]-cz)
        u = sum(dp[i]*e1[i] for i in range(3))
        v = sum(dp[i]*e2[i] for i in range(3))
        return u, v

    projected = [project(p) for p in pts]
    # 角度でソート
    projected_sorted = sorted(projected, key=lambda p: math.atan2(p[1], p[0]))

    print("\n  各頂点間の距離:")
    n = len(projected_sorted)
    side_lengths = []
    for i in range(n):
        p1 = projected_sorted[i]
        p2 = projected_sorted[(i+1) % n]
        d = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        side_lengths.append(d)
        print(f"    辺{i+1}: {d:.6f}")

    tol = 1e-9
    assert all(abs(d - side_lengths[0]) < tol for d in side_lengths), \
        "辺長が等しくない: 正六角形でない"
    print(f"\n  全辺長 = {side_lengths[0]:.6f} (= 1/√2 = {1/math.sqrt(2):.6f})")
    print("  断面は正六角形: OK")
    print("\n  正解: 選択肢(1) - 正六角形")
    return True


if __name__ == "__main__":
    ok1 = verify_q1()
    ok2 = verify_q2()
    if ok1 and ok2:
        print("\n==============================")
        print("全検証合格: 航大思考138")
        print("  問1正解: 選択肢(4)")
        print("  問2正解: 選択肢(1)")
        print("==============================")
