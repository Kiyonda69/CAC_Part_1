#!/usr/bin/env python3
"""航大思考271 検証: 立方体の切断面の形状

座標系: 一辺1の立方体
A(0,0,1) B(1,0,1) C(1,1,1) D(0,1,1) 上面
E(0,0,0) F(1,0,0) G(1,1,0) H(0,1,0) 下面
"""
from fractions import Fraction as Fr
from itertools import combinations

V = {
    'A': (0, 0, 1), 'B': (1, 0, 1), 'C': (1, 1, 1), 'D': (0, 1, 1),
    'E': (0, 0, 0), 'F': (1, 0, 0), 'G': (1, 1, 0), 'H': (0, 1, 0),
}
EDGES = [('A','B'),('B','C'),('C','D'),('D','A'),
         ('E','F'),('F','G'),('G','H'),('H','E'),
         ('A','E'),('B','F'),('C','G'),('D','H')]

def mid(p, q):
    return tuple(Fr(V[p][i] + V[q][i], 2) for i in range(3))

def sub(a, b): return tuple(a[i]-b[i] for i in range(3))
def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return sum(a[i]*b[i] for i in range(3))

def plane_from_points(p1, p2, p3):
    n = cross(sub(p2, p1), sub(p3, p1))
    assert n != (0, 0, 0), "3点が一直線上"
    return n, dot(n, p1)

def cross_section(n, d):
    """平面 n・x = d と立方体の交線多角形の頂点を返す"""
    pts = set()
    for p, q in EDGES:
        vp, vq = dot(n, V[p]) - d, dot(n, V[q]) - d
        if vp == 0: pts.add(tuple(map(Fr, V[p])))
        if vq == 0: pts.add(tuple(map(Fr, V[q])))
        if vp * vq < 0:
            t = Fr(vp, vp - vq)
            pts.add(tuple(Fr(V[p][i]) + t*(V[q][i]-V[p][i]) for i in range(3)))
    return sorted(pts)

def dist2(a, b): return sum((a[i]-b[i])**2 for i in range(3))

def order_polygon(pts, n):
    """凸多角形の頂点を周順に並べる"""
    c = tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))
    ref = sub(pts[0], c)
    def key(p):
        v = sub(p, c)
        cr = cross(ref, v)
        s = dot(cr, n)
        co = dot(ref, v)
        import math
        return math.atan2(float(s), float(co) * math.sqrt(float(dot(v,v)*dot(ref,ref))) ** 0)
    import math
    def angle(p):
        v = sub(p, c)
        x = float(dot(ref, v))
        y = float(dot(cross(ref, v), n))
        return math.atan2(y, x)
    return sorted(pts, key=angle)

def analyze(label, p1, p2, p3):
    n, d = plane_from_points(p1, p2, p3)
    pts = cross_section(n, d)
    poly = order_polygon(pts, n)
    k = len(poly)
    sides = [dist2(poly[i], poly[(i+1) % k]) for i in range(k)]
    print(f"--- {label} ---")
    print(f"平面法線: {n}, d={d}")
    print(f"断面の頂点数: {k}")
    for p in poly:
        print(f"  {tuple(str(x) for x in p)}")
    print(f"辺の長さ^2: {[str(s) for s in sides]}")
    # 正多角形か（全辺等長 + 全対角線パターン）
    equilateral = len(set(sides)) == 1
    print(f"全辺等長: {equilateral}")
    return k, sides, poly, n

# ============ 問1: 辺AB, 辺FG, 辺DH の中点を通る平面 ============
k1, s1, poly1, n1 = analyze("問1", mid('A','B'), mid('F','G'), mid('D','H'))
assert k1 == 6, f"問1: 六角形でない ({k1}角形)"
assert len(set(s1)) == 1, "問1: 辺が等長でない"
# 正六角形: 等辺かつ全ての内角が等しい（対角線 = 2*辺 の関係で確認）
diags = [dist2(poly1[i], poly1[(i+3) % 6]) for i in range(3)]
assert all(d == s1[0]*4 for d in diags), "問1: 正六角形でない（長対角線≠2辺長）"
print("問1: 正六角形 => OK\n")

# ============ 問2: 辺AB, 辺AD, 辺CG の中点を通る平面 ============
k2, s2, poly2, n2 = analyze("問2", mid('A','B'), mid('A','D'), mid('C','G'))
assert k2 == 5, f"問2: 五角形でない ({k2}角形)"
print("問2: 五角形 => OK\n")

# ============ 選択肢の排他性チェック（問1） ============
# 他の選択肢（正三角形・正方形・長方形・ひし形）は頂点数6と矛盾 => 一意
# 問2 選択肢（正三角形・等脚台形・ひし形・正六角形）は頂点数5と矛盾 => 一意
print("選択肢排他性: 問1は6角形のみ、問2は5角形のみが該当 => 解は一意")
