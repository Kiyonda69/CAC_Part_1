"""
航大思考149 検証スクリプト
================================
立方体の断面図問題（解答者が自ら作図する必要のある問題）

座標系:
A=(0,0,1), B=(1,0,1), C=(1,1,1), D=(0,1,1)  ← 上面
E=(0,0,0), F=(1,0,0), G=(1,1,0), H=(0,1,0)  ← 下面
（AE, BF, CG, DH が垂直辺）

問1: 頂点 A, C と 辺 FG の中点 M の3点を通る平面で切断
問2: 辺 AB, CG, HE の中点 P, Q, R の3点を通る平面で切断
"""

import math

# 立方体の頂点
V = {
    'A': (0, 0, 1), 'B': (1, 0, 1), 'C': (1, 1, 1), 'D': (0, 1, 1),
    'E': (0, 0, 0), 'F': (1, 0, 0), 'G': (1, 1, 0), 'H': (0, 1, 0),
}

# 立方体の辺（12本）
EDGES = [
    ('A','B'), ('B','C'), ('C','D'), ('D','A'),  # 上面
    ('E','F'), ('F','G'), ('G','H'), ('H','E'),  # 下面
    ('A','E'), ('B','F'), ('C','G'), ('D','H'),  # 垂直辺
]


def sub(a, b):
    return tuple(a[i]-b[i] for i in range(3))

def add(a, b):
    return tuple(a[i]+b[i] for i in range(3))

def scale(a, s):
    return tuple(a[i]*s for i in range(3))

def dot(a, b):
    return sum(a[i]*b[i] for i in range(3))

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def norm(a):
    return math.sqrt(dot(a, a))


def plane_from_3points(p1, p2, p3):
    """3点を通る平面 n·x = d を返す"""
    n = cross(sub(p2, p1), sub(p3, p1))
    d = dot(n, p1)
    return n, d


def edge_intersect(p_start, p_end, n, d, eps=1e-9):
    """辺 p_start→p_end と平面 n·x=d の交点を返す。なければ None"""
    direction = sub(p_end, p_start)
    denom = dot(n, direction)
    val_start = dot(n, p_start) - d
    if abs(denom) < eps:
        # 平面と平行
        return None
    t = -val_start / denom
    if -eps <= t <= 1 + eps:
        return tuple(p_start[i] + t*direction[i] for i in range(3))
    return None


def find_cross_section(n, d, eps=1e-7):
    """平面で立方体を切ったときの断面の頂点を求める（重複除去）"""
    points = []
    for a, b in EDGES:
        p = edge_intersect(V[a], V[b], n, d)
        if p is None:
            continue
        # 重複チェック
        dup = False
        for q in points:
            if all(abs(p[i]-q[i]) < eps for i in range(3)):
                dup = True
                break
        if not dup:
            points.append(p)
    return points


def order_points_on_plane(points, n):
    """平面上の点を凸多角形の順に並べ替える"""
    # 平面の重心
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    cz = sum(p[2] for p in points) / len(points)
    center = (cx, cy, cz)

    # 平面上の基底ベクトル u, v を構築
    # 任意の方向で n と直交するベクトル
    if abs(n[0]) < 0.9:
        ref = (1, 0, 0)
    else:
        ref = (0, 1, 0)
    u = cross(n, ref)
    u_len = norm(u)
    u = tuple(u[i]/u_len for i in range(3))
    v = cross(n, u)
    v_len = norm(v)
    v = tuple(v[i]/v_len for i in range(3))

    # 各点を (u, v) 座標に投影し、角度でソート
    angles = []
    for p in points:
        rel = sub(p, center)
        pu = dot(rel, u)
        pv = dot(rel, v)
        angles.append((math.atan2(pv, pu), p))
    angles.sort()
    return [p for _, p in angles]


def side_lengths(ordered):
    """順序付き多角形の各辺の長さ"""
    n = len(ordered)
    return [norm(sub(ordered[(i+1) % n], ordered[i])) for i in range(n)]


def interior_angles(ordered):
    """順序付き多角形の各内角（度）"""
    n = len(ordered)
    angles = []
    for i in range(n):
        prev = ordered[(i-1) % n]
        curr = ordered[i]
        nxt = ordered[(i+1) % n]
        v1 = sub(prev, curr)
        v2 = sub(nxt, curr)
        cos_a = dot(v1, v2) / (norm(v1) * norm(v2))
        cos_a = max(-1, min(1, cos_a))
        angles.append(math.degrees(math.acos(cos_a)))
    return angles


def parallel_pairs(ordered):
    """順序付き多角形で平行な辺のペアを返す"""
    n = len(ordered)
    edges = [sub(ordered[(i+1) % n], ordered[i]) for i in range(n)]
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            c = cross(edges[i], edges[j])
            if norm(c) < 1e-7:
                pairs.append((i, j))
    return pairs


def midpoint(a, b):
    return tuple((a[i]+b[i])/2 for i in range(3))


print("="*60)
print("問1: 頂点 A, C と 辺 FG の中点 M を通る平面")
print("="*60)
A_pt = V['A']
C_pt = V['C']
M = midpoint(V['F'], V['G'])
print(f"A = {A_pt}")
print(f"C = {C_pt}")
print(f"M (FG中点) = {M}")

n1, d1 = plane_from_3points(A_pt, C_pt, M)
print(f"平面方程式: {n1[0]}x + {n1[1]}y + {n1[2]}z = {d1}")

points1 = find_cross_section(n1, d1)
ordered1 = order_points_on_plane(points1, n1)
print(f"\n断面の頂点数: {len(ordered1)}")
for p in ordered1:
    print(f"  {tuple(round(c, 4) for c in p)}")

sides1 = side_lengths(ordered1)
angles1 = interior_angles(ordered1)
print(f"\n辺の長さ: {[round(s, 4) for s in sides1]}")
print(f"内角(度): {[round(a, 2) for a in angles1]}")

pairs1 = parallel_pairs(ordered1)
print(f"平行な辺のペア: {pairs1}")

# 形状の判定
n_sides = len(ordered1)
if n_sides == 4:
    # 4辺の中で平行ペアの数
    n_parallel = len(pairs1)
    s_round = [round(s, 6) for s in sides1]
    if n_parallel == 2:
        print("→ 平行四辺形")
    elif n_parallel == 1:
        # 台形
        i, j = pairs1[0]
        # 平行でない2辺（脚）
        legs = [s_round[k] for k in range(4) if k != i and k != j]
        if abs(legs[0] - legs[1]) < 1e-6:
            print("→ 等脚台形")
        else:
            print("→ 一般の台形")
    else:
        print("→ 一般の四角形")

print()
print("="*60)
print("問2: 辺 AB, CG, HE の中点 P, Q, R を通る平面")
print("="*60)
P = midpoint(V['A'], V['B'])
Q = midpoint(V['C'], V['G'])
R = midpoint(V['H'], V['E'])
print(f"P (AB中点) = {P}")
print(f"Q (CG中点) = {Q}")
print(f"R (HE中点) = {R}")

n2, d2 = plane_from_3points(P, Q, R)
print(f"平面方程式: {n2[0]}x + {n2[1]}y + {n2[2]}z = {d2}")

points2 = find_cross_section(n2, d2)
ordered2 = order_points_on_plane(points2, n2)
print(f"\n断面の頂点数: {len(ordered2)}")
for p in ordered2:
    print(f"  {tuple(round(c, 4) for c in p)}")

sides2 = side_lengths(ordered2)
angles2 = interior_angles(ordered2)
print(f"\n辺の長さ: {[round(s, 4) for s in sides2]}")
print(f"内角(度): {[round(a, 2) for a in angles2]}")

# 正六角形か判定
if len(ordered2) == 6:
    all_sides_equal = all(abs(sides2[0] - s) < 1e-6 for s in sides2)
    all_angles_equal = all(abs(120 - a) < 1e-3 for a in angles2)
    if all_sides_equal and all_angles_equal:
        print("→ 正六角形")
    else:
        print("→ 一般の六角形")
