#!/usr/bin/env python3
"""
セット64 検証コード
問1: 立方体の全頂点切断 → 切頂立体の面・辺・頂点
問2: 立方体の3点を通る平面による切断面の形状
"""
import math

print("=" * 60)
print("問1: 立方体の全頂点を各辺の中点で切り落とした立体の性質")
print("=" * 60)

# 立方体の12辺の中点 → 新しい立体の12頂点
# 元の立方体の各面(6面) → 正方形の面 (各面に4つの中点)
# 元の立方体の各頂点(8頂点) → 三角形の面 (各頂点に3つの中点)

V = 12  # 12辺 → 12中点 → 12頂点
# 辺: 三角形面8つ × 3辺 = 24辺(だが各辺は正方形面と三角形面で共有)
# 正方形面6つ × 4辺 = 24辺(各辺は三角形面と共有)
# 各辺は正確に2面で共有されるので: (8*3)/1 は合わない
# 正しくは: 各辺は隣接する2つの面に属する
# 三角形面の辺数: 8 × 3 = 24 (延べ)
# 正方形面の辺数: 6 × 4 = 24 (延べ)
# 全面の辺数合計: 24 + 24 = 48 (各辺は2面で共有) → E = 48/2 = 24
E = 24
F = 2 - V + E  # オイラーの公式
print(f"頂点 V = {V}")
print(f"辺   E = {E}")
print(f"面   F = {F}")
print(f"  内訳: 正方形面 6 + 三角形面 8 = 14")
print(f"V - E + F = {V} - {E} + {F} = {V - E + F}")
assert V == 12 and E == 24 and F == 14
assert V - E + F == 2
print("問1 検証OK\n")

print("=" * 60)
print("問2: 立方体の3辺上の点を通る切断面の形状")
print("=" * 60)

# 一辺4cmの立方体 ABCD-EFGH
# A(0,0,0) B(4,0,0) C(4,4,0) D(0,4,0)
# E(0,0,4) F(4,0,4) G(4,4,4) H(0,4,4)

# 3つの点:
M = (0, 0, 2)   # 辺AEの中点
P = (4, 0, 1)   # 辺BF上, BP=1
Q = (0, 4, 3)   # 辺DH上, DQ=3

print(f"M = {M} (辺AEの中点)")
print(f"P = {P} (辺BF上, BP=1)")
print(f"Q = {Q} (辺DH上, DQ=3)")

# 法線ベクトル = MP × MQ
MP = (P[0]-M[0], P[1]-M[1], P[2]-M[2])  # (4, 0, -1)
MQ = (Q[0]-M[0], Q[1]-M[1], Q[2]-M[2])  # (0, 4, 1)
print(f"MP = {MP}")
print(f"MQ = {MQ}")

# 外積
normal = (
    MP[1]*MQ[2] - MP[2]*MQ[1],
    MP[2]*MQ[0] - MP[0]*MQ[2],
    MP[0]*MQ[1] - MP[1]*MQ[0]
)
print(f"法線 = {normal}")  # (4, -4, 16) → (1, -1, 4)

# 平面: 1(x) -1(y) + 4(z) = 8
# 検証: M → 0-0+8=8 ✓, P → 4-0+4=8 ✓, Q → 0-4+12=8 ✓
for name, pt in [("M", M), ("P", P), ("Q", Q)]:
    val = pt[0] - pt[1] + 4*pt[2]
    print(f"  {name}: x-y+4z = {val}")
    assert val == 8

# 立方体の12辺との交点を求める
vertices = {
    'A': (0,0,0), 'B': (4,0,0), 'C': (4,4,0), 'D': (0,4,0),
    'E': (0,0,4), 'F': (4,0,4), 'G': (4,4,4), 'H': (0,4,4)
}

edges = [
    ('A','B'), ('B','C'), ('C','D'), ('D','A'),
    ('E','F'), ('F','G'), ('G','H'), ('H','E'),
    ('A','E'), ('B','F'), ('C','G'), ('D','H')
]

intersections = []
for v1n, v2n in edges:
    v1, v2 = vertices[v1n], vertices[v2n]
    # f(v) = x - y + 4z - 8
    f1 = v1[0] - v1[1] + 4*v1[2] - 8
    f2 = v2[0] - v2[1] + 4*v2[2] - 8
    if f1 == f2:
        continue
    t = -f1 / (f2 - f1)
    if 0 <= t <= 1:
        pt = (v1[0] + t*(v2[0]-v1[0]), v1[1] + t*(v2[1]-v1[1]), v1[2] + t*(v2[2]-v1[2]))
        intersections.append((v1n+v2n, pt))
        print(f"辺{v1n}{v2n}: t={t:.4f}, 交点={pt}")

print(f"\n交点数: {len(intersections)}")
assert len(intersections) == 4, f"交点が4つでない: {len(intersections)}"

# 交点を順序付け: M→P→R→Q (M on AE, P on BF, R on CG, Q on DH)
pts = {}
for name, pt in intersections:
    pts[name] = pt

print(f"\nM on AE = {pts['AE']}")
print(f"P on BF = {pts['BF']}")
print(f"R on CG = {pts['CG']}")
print(f"Q on DH = {pts['DH']}")

def dist(a, b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

def dot(a, b):
    return sum(a[i]*b[i] for i in range(3))

def vec(a, b):
    return tuple(b[i]-a[i] for i in range(3))

# 辺の長さ
m, p, r, q = pts['AE'], pts['BF'], pts['CG'], pts['DH']
side_mp = dist(m, p)
side_pr = dist(p, r)
side_rq = dist(r, q)
side_qm = dist(q, m)

print(f"\n辺の長さ:")
print(f"  MP = {side_mp:.6f} = sqrt({int(side_mp**2+0.5)})")
print(f"  PR = {side_pr:.6f} = sqrt({int(side_pr**2+0.5)})")
print(f"  RQ = {side_rq:.6f} = sqrt({int(side_rq**2+0.5)})")
print(f"  QM = {side_qm:.6f} = sqrt({int(side_qm**2+0.5)})")

all_equal = abs(side_mp - side_pr) < 0.001 and abs(side_pr - side_rq) < 0.001 and abs(side_rq - side_qm) < 0.001
print(f"全辺等しい: {all_equal}")

# 平行四辺形チェック
v_mp = vec(m, p)  # (4, 0, -1)
v_qr = vec(q, r)  # (4, 0, -1)
is_parallel1 = v_mp == v_qr
v_pq_check = vec(p, r)  # (0, 4, 1)
v_mq = vec(m, q)        # (0, 4, 1)
is_parallel2 = v_pq_check == v_mq
print(f"\nMP = {v_mp}, QR = {v_qr}, 平行: {is_parallel1}")
print(f"PR = {v_pq_check}, MQ = {v_mq}, 平行: {is_parallel2}")
print(f"平行四辺形: {is_parallel1 and is_parallel2}")

# 直角チェック
dot_val = dot(vec(m, p), vec(m, q))
print(f"\nMP · MQ = {dot_val}")
is_right = dot_val == 0
print(f"直角: {is_right}")

if all_equal and is_right:
    shape = "正方形"
elif all_equal and not is_right:
    shape = "ひし形（正方形でない）"
elif is_parallel1 and is_parallel2:
    shape = "平行四辺形"
else:
    shape = "一般の四角形"

print(f"\n結論: 切断面は「{shape}」")

# 対角線の長さ
diag_mr = dist(m, r)
diag_pq = dist(p, q)
print(f"対角線: MR = {diag_mr:.6f}, PQ = {diag_pq:.6f}")

print("\n問2 検証OK: 切断面はひし形（正方形でない）")
print(f"4辺の長さ = sqrt(17) ≈ {side_mp:.4f}")
print(f"MP·MQ = {dot_val} ≠ 0 なので正方形ではない")

