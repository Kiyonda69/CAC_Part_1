#!/usr/bin/env python3
"""航大思考238 検証: 直方体表面の最短経路（展開図による測地線の全列挙）
問1: 4x3x2 コンテナの対角頂点間の表面最短経路 → √41
問2: 30x12x12 格納庫内壁の2点間最短経路（スパイダー&フライ型）→ 40
"""
import math
from itertools import permutations

def sub(p, q): return tuple(p[i]-q[i] for i in range(len(p)))
def add(p, q): return tuple(p[i]+q[i] for i in range(len(p)))
def dot(p, q): return sum(p[i]*q[i] for i in range(len(p)))
def norm(p): return math.sqrt(dot(p, p))
def unit(p):
    n = norm(p); return tuple(x/n for x in p)
def cross2(u, v): return u[0]*v[1] - u[1]*v[0]

def box_faces(a, b, c):
    """面 = (axis, val): axis方向の座標がvalで固定の長方形"""
    return [(0, 0), (0, a), (1, 0), (1, b), (2, 0), (2, c)]

def face_corners(face, dims):
    ax, val = face
    others = [i for i in range(3) if i != ax]
    corners = []
    for s in [0, 1]:
        for t in [0, 1]:
            p = [0.0, 0.0, 0.0]
            p[ax] = val
            p[others[0]] = s * dims[others[0]]
            p[others[1]] = t * dims[others[1]]
            corners.append(tuple(p))
    # 長方形の順序に並べ替え(00,01,11,10)
    return [corners[0], corners[1], corners[3], corners[2]]

def face_center(face, dims):
    cs = face_corners(face, dims)
    return tuple(sum(c[i] for c in cs)/4 for i in range(3))

def shared_edge(f1, f2, dims):
    """2面が共有する辺の端点2つを返す（なければNone）"""
    c1 = set(face_corners(f1, dims))
    c2 = set(face_corners(f2, dims))
    common = c1 & c2
    if len(common) == 2:
        return tuple(sorted(common))
    return None

def on_face(p, face, dims, eps=1e-9):
    ax, val = face
    if abs(p[ax] - val) > eps: return False
    return all(-eps <= p[i] <= dims[i] + eps for i in range(3))

def plane_basis(face, dims):
    """面内の正規直交基底(3D)"""
    ax, _ = face
    others = [i for i in range(3) if i != ax]
    u = [0.0]*3; u[others[0]] = 1.0
    v = [0.0]*3; v[others[1]] = 1.0
    return tuple(u), tuple(v)

def unfold_distance(seq, A, B, dims):
    """面列 seq に沿って展開し、A→B 直線距離を返す。無効な経路は None。"""
    f0 = seq[0]
    u, v = plane_basis(f0, dims)
    def M0(p): return (dot(p, u), dot(p, v))
    maps = [M0]
    prev_center_2d = M0(face_center(f0, dims))
    hinges = []  # 各遷移の辺の2D像
    for i in range(len(seq) - 1):
        e = shared_edge(seq[i], seq[i+1], dims)
        if e is None: return None
        e1, e2 = e
        Mi = maps[-1]
        E1, E2 = Mi(e1), Mi(e2)
        L = norm(sub(e2, e1))
        t3 = unit(sub(e2, e1))
        # 次面の中心から辺への垂直方向(面内・辺から面内部へ)
        cn = face_center(seq[i+1], dims)
        w3 = sub(cn, e1)
        w3 = sub(w3, tuple(dot(w3, t3)*t3[k] for k in range(3)))
        n3 = unit(w3)
        T2 = unit(sub(E2, E1))
        P2a = (-T2[1], T2[0])  # 辺に垂直な2D方向候補
        # 前面の中心と反対側に開く
        side_prev = cross2(sub(E2, E1), sub(prev_center_2d, E1))
        N2 = P2a if cross2(sub(E2, E1), P2a) * side_prev < 0 else (T2[1], -T2[0])
        def Mnext(p, e1=e1, t3=t3, n3=n3, E1=E1, T2=T2, N2=N2):
            d = sub(p, e1)
            s = dot(d, t3); w = dot(d, n3)
            return (E1[0] + s*T2[0] + w*N2[0], E1[1] + s*T2[1] + w*N2[1])
        maps.append(Mnext)
        hinges.append((E1, E2))
        prev_center_2d = Mnext(face_center(seq[i+1], dims))
    A2 = maps[0](A); B2 = maps[-1](B)
    # 妥当性: A→B 直線が各ヒンジ辺をその線分内で昇順に横切ること
    d = sub(B2, A2)
    prev_t = 0.0
    for (E1, E2) in hinges:
        eD = sub(E2, E1)
        denom = cross2(d, eD)
        if abs(denom) < 1e-12: return None
        t = cross2(sub(E1, A2), eD) / denom       # A→B 上のパラメータ
        s = cross2(sub(E1, A2), d) / denom        # 辺上のパラメータ
        if not (-1e-9 <= s <= 1 + 1e-9): return None
        if t < prev_t - 1e-9 or t > 1 + 1e-9: return None
        prev_t = t
    return norm(d)

def surface_min(A, B, dims, max_faces=6):
    faces = box_faces(*dims)
    fA = [f for f in faces if on_face(A, f, dims)]
    fB = [f for f in faces if on_face(B, f, dims)]
    results = []
    def dfs(seq):
        if seq[-1] in fB and len(seq) >= 2:
            dist = unfold_distance(seq, A, B, dims)
            if dist is not None:
                results.append((dist, tuple(seq)))
        if len(seq) >= max_faces: return
        for f in faces:
            if f in seq: continue
            if shared_edge(seq[-1], f, dims):
                dfs(seq + [f])
    for f in fA:
        dfs([f])
    return sorted(results)

def q1():
    dims = (4.0, 3.0, 2.0)
    A = (0.0, 0.0, 0.0)
    B = (4.0, 3.0, 2.0)
    res = surface_min(A, B, dims)
    vals = sorted(set(round(d, 6) for d, _ in res))
    best = vals[0]
    print("問1 経路候補(距離の昇順・上位):", vals[:6])
    assert abs(best - math.sqrt(41)) < 1e-5, best
    # 誤答候補: √45, √53 が実在の劣位経路であること
    assert any(abs(v - math.sqrt(45)) < 1e-6 for v in vals)
    assert any(abs(v - math.sqrt(53)) < 1e-6 for v in vals)
    # 最短値の一意性（2位と明確に離れている）
    assert vals[1] - vals[0] > 0.25
    print(f"問1 OK: 最短 = √41 ≈ {best:.3f} m（内部直線 √29≈{math.sqrt(29):.3f} は不可・辺沿い 9m）")

def q2():
    dims = (12.0, 30.0, 12.0)  # x=幅12, y=奥行30, z=高さ12
    A = (6.0, 0.0, 11.0)   # 手前壁 中央・天井から1m
    B = (6.0, 30.0, 1.0)   # 奥壁 中央・床から1m
    res = surface_min(A, B, dims)
    vals = sorted(set(round(d, 6) for d, _ in res))
    best_d, best_seq = res[0]
    print("問2 経路候補(距離の昇順・上位):", vals[:6])
    print("問2 最短経路の面列:", best_seq, "距離:", best_d)
    assert abs(best_d - 40.0) < 1e-9, best_d
    # 天井直行 42m が劣位経路として存在
    assert any(abs(v - 42.0) < 1e-6 for v in vals)
    # 天井+側壁の4面経由 √1658 ≈ 40.72m
    assert any(abs(v - math.sqrt(1658)) < 1e-6 for v in vals)
    # 側壁経由 √1864 ≈ 43.17m
    assert any(abs(v - math.sqrt(1864)) < 1e-6 for v in vals)
    assert vals[1] - vals[0] > 0.5
    print(f"問2 OK: 最短 = 40 m（5面横断）/ 天井直行 42m / 側壁 √1864≈{math.sqrt(1864):.2f}m / 内部直線 √1000≈{math.sqrt(1000):.2f}m")

if __name__ == "__main__":
    q1()
    q2()
    print("全検証 OK: 両問とも最短値が唯一に定まる")
