"""航大思考188 検証スクリプト: 立方体の断面図

立方体ABCD-EFGH（一辺2）の座標:
  上面 z=2: A(0,0,2) B(2,0,2) C(2,2,2) D(0,2,2)
  下面 z=0: E(0,0,0) F(2,0,0) G(2,2,0) H(0,2,0)

問1: 頂点Bに集まる3辺の端点 A,C,F を通る平面 → 切り口の形
問2: 辺ABの中点・辺ADの中点・頂点G を通る平面 → 切り口の角数
"""
import itertools
import math

V = {
    'A': (0, 0, 2), 'B': (2, 0, 2), 'C': (2, 2, 2), 'D': (0, 2, 2),
    'E': (0, 0, 0), 'F': (2, 0, 0), 'G': (2, 2, 0), 'H': (0, 2, 0),
}
EDGES = ['AB', 'BC', 'CD', 'DA', 'EF', 'FG', 'GH', 'HE',
         'AE', 'BF', 'CG', 'DH']


def sub(p, q):
    return (p[0]-q[0], p[1]-q[1], p[2]-q[2])


def cross(u, w):
    return (u[1]*w[2]-u[2]*w[1], u[2]*w[0]-u[0]*w[2], u[0]*w[1]-u[1]*w[0])


def dot(u, w):
    return u[0]*w[0]+u[1]*w[1]+u[2]*w[2]


def dist(p, q):
    return math.sqrt(sum(d*d for d in sub(p, q)))


def plane_from_points(p1, p2, p3):
    """平面 a*x+b*y+c*z = d を返す"""
    n = cross(sub(p2, p1), sub(p3, p1))
    d = dot(n, p1)
    return (n, d)


def cross_section(plane):
    """立方体と平面の交わりとなる多角形の頂点を順序付けて返す"""
    n, d = plane
    pts = []
    for e in EDGES:
        p, q = V[e[0]], V[e[1]]
        fp, fq = dot(n, p)-d, dot(n, q)-d
        if abs(fp) < 1e-9:        # 端点が平面上
            pts.append(p)
        if abs(fq) < 1e-9:
            pts.append(q)
        elif abs(fp) >= 1e-9 and fp*fq < 0:   # 辺の内部で交差
            t = fp/(fp-fq)
            pts.append(tuple(p[i]+t*(q[i]-p[i]) for i in range(3)))
    # 重複除去
    uniq = []
    for pt in pts:
        if not any(dist(pt, u) < 1e-6 for u in uniq):
            uniq.append(pt)
    return order_polygon(uniq, n)


def order_polygon(pts, n):
    """法線nの平面上で頂点を角度順に並べる"""
    cx = sum(p[0] for p in pts)/len(pts)
    cy = sum(p[1] for p in pts)/len(pts)
    cz = sum(p[2] for p in pts)/len(pts)
    c = (cx, cy, cz)
    u = sub(pts[0], c)
    ulen = math.sqrt(dot(u, u))
    u = tuple(x/ulen for x in u)
    w = cross(n, u)
    wlen = math.sqrt(dot(w, w))
    w = tuple(x/wlen for x in w)

    def ang(p):
        r = sub(p, c)
        return math.atan2(dot(r, w), dot(r, u))
    return sorted(pts, key=ang)


def angles(poly):
    """多角形の内角(度)のリスト"""
    res = []
    m = len(poly)
    for i in range(m):
        a = poly[(i-1) % m]
        b = poly[i]
        cc = poly[(i+1) % m]
        u, w = sub(a, b), sub(cc, b)
        cosv = dot(u, w)/(math.sqrt(dot(u, u))*math.sqrt(dot(w, w)))
        res.append(round(math.degrees(math.acos(max(-1, min(1, cosv)))), 1))
    return res


def sides(poly):
    m = len(poly)
    return [round(dist(poly[i], poly[(i+1) % m]), 4) for i in range(m)]


print("=" * 50)
print("問1: 平面 through A, C, F")
p1 = plane_from_points(V['A'], V['C'], V['F'])
poly1 = cross_section(p1)
s1 = sides(poly1)
print(f"  頂点数 = {len(poly1)} 辺の長さ = {s1}")
print(f"  内角 = {angles(poly1)}")
assert len(poly1) == 3, "三角形でない"
assert max(s1)-min(s1) < 1e-6, "辺長が不揃い"
print("  → 正三角形 (equilateral triangle) で確定")

print("=" * 50)
print("問2: 平面 through midAB, midAD, G")
midAB = tuple((V['A'][i]+V['B'][i])/2 for i in range(3))
midAD = tuple((V['A'][i]+V['D'][i])/2 for i in range(3))
p2 = plane_from_points(midAB, midAD, V['G'])
poly2 = cross_section(p2)
print(f"  平面: {p2[0]} = {p2[1]}")
print(f"  頂点数 = {len(poly2)} 辺の長さ = {sides(poly2)}")
print(f"  内角 = {angles(poly2)}")
print(f"  頂点座標 = {[tuple(round(x,3) for x in p) for p in poly2]}")
assert len(poly2) == 5, "五角形でない"
print("  → 五角形 (pentagon) で確定")
print("=" * 50)
print("検証完了: 問1=正三角形, 問2=五角形")
