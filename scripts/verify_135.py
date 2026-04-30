"""
セット135 検証スクリプト
問1: 立方体断面（菱形）
  切断点: A, M=mid(BF), N=mid(DH) → 断面は菱形 A-M-G-N
問2: 立方体断面（正六角形）
  切断点: P=mid(BC), Q=mid(DH), R=mid(EF) → 断面は正六角形

立方体 ABCD-EFGH の座標:
  A(0,0,0), B(1,0,0), C(1,1,0), D(0,1,0)
  E(0,0,1), F(1,0,1), G(1,1,1), H(0,1,1)
"""
import math

vertices = {
    'A': (0,0,0), 'B': (1,0,0), 'C': (1,1,0), 'D': (0,1,0),
    'E': (0,0,1), 'F': (1,0,1), 'G': (1,1,1), 'H': (0,1,1),
}

edges = [
    ('A','B'),('B','C'),('C','D'),('D','A'),
    ('E','F'),('F','G'),('G','H'),('H','E'),
    ('A','E'),('B','F'),('C','G'),('D','H'),
]

def midpoint(p, q):
    return tuple((a+b)/2 for a,b in zip(p,q))

def plane_normal_and_d(p1, p2, p3):
    v1 = [p2[i]-p1[i] for i in range(3)]
    v2 = [p3[i]-p1[i] for i in range(3)]
    n = [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0],
    ]
    d = sum(n[i]*p1[i] for i in range(3))
    return n, d

def intersect_plane_edge(n, d, p, q):
    vp = sum(n[i]*p[i] for i in range(3))
    vq = sum(n[i]*q[i] for i in range(3))
    if abs(vq - vp) < 1e-9:
        return None
    t = (d - vp) / (vq - vp)
    if -1e-9 <= t <= 1+1e-9:
        t = max(0, min(1, t))
        return tuple(p[i] + t*(q[i]-p[i]) for i in range(3))
    return None

def get_cross_section(n, d):
    pts = []
    for e1, e2 in edges:
        pt = intersect_plane_edge(n, d, vertices[e1], vertices[e2])
        if pt is not None:
            if not any(all(abs(pt[i]-p[i])<1e-9 for i in range(3)) for p in pts):
                pts.append(pt)
    return pts

def sort_polygon(pts, normal):
    """断面多角形の頂点を順序付けする（法線方向基準）"""
    center = [sum(p[i] for p in pts)/len(pts) for i in range(3)]
    # 法線に垂直な2つの基底ベクトルを作成
    n_len = math.sqrt(sum(x**2 for x in normal))
    n = [x/n_len for x in normal]
    # 最初の点からのベクトルを基底に
    v0 = [pts[0][i]-center[i] for i in range(3)]
    def angle(p):
        v = [p[i]-center[i] for i in range(3)]
        cos_t = sum(v[i]*v0[i] for i in range(3))
        cross = [
            v0[1]*v[2]-v0[2]*v[1],
            v0[2]*v[0]-v0[0]*v[2],
            v0[0]*v[1]-v0[1]*v[0],
        ]
        sin_t = sum(cross[i]*n[i] for i in range(3))
        return math.atan2(sin_t, cos_t)
    return sorted(pts, key=angle)

def dist(a, b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(3)))

def verify_q1():
    print("=== 問1: A, M=mid(BF), N=mid(DH) を通る平面 ===")
    A = vertices['A']
    M = midpoint(vertices['B'], vertices['F'])
    N = midpoint(vertices['D'], vertices['H'])
    print(f"  A={A}, M={M}, N={N}")

    n, d = plane_normal_and_d(A, M, N)
    pts_raw = get_cross_section(n, d)
    pts = sort_polygon(pts_raw, n)

    print(f"  断面頂点数: {len(pts)}")
    for p in pts:
        print(f"    {tuple(round(x,4) for x in p)}")

    sides = [dist(pts[i], pts[(i+1)%len(pts)]) for i in range(len(pts))]
    print(f"  辺の長さ: {[round(s,4) for s in sides]}")
    all_equal = max(sides) - min(sides) < 1e-9
    print(f"  全辺等長: {all_equal}")

    if len(pts) == 4:
        d1 = dist(pts[0], pts[2])
        d2 = dist(pts[1], pts[3])
        print(f"  対角線: d1={round(d1,4)}, d2={round(d2,4)}")
        print(f"  正方形か（対角線等長）: {abs(d1-d2)<1e-9}")
        is_rhombus = all_equal and abs(d1-d2)>1e-9
        print(f"  菱形（非正方形）: {is_rhombus}")
    print()

def verify_q2():
    print("=== 問2: P=mid(BC), Q=mid(DH), R=mid(EF) を通る平面 ===")
    P = midpoint(vertices['B'], vertices['C'])
    Q = midpoint(vertices['D'], vertices['H'])
    R = midpoint(vertices['E'], vertices['F'])
    print(f"  P={P}, Q={Q}, R={R}")
    print(f"  平面の方程式検証: x+y+z=?  P:{sum(P)}, Q:{sum(Q)}, R:{sum(R)}")

    n, d = plane_normal_and_d(P, Q, R)
    pts_raw = get_cross_section(n, d)
    pts = sort_polygon(pts_raw, n)

    print(f"  断面頂点数: {len(pts)}")
    for p in pts:
        print(f"    {tuple(round(x,4) for x in p)}")

    sides = [dist(pts[i], pts[(i+1)%len(pts)]) for i in range(len(pts))]
    print(f"  辺の長さ: {[round(s,4) for s in sides]}")
    all_equal = max(sides) - min(sides) < 1e-9
    print(f"  全辺等長: {all_equal}")

    is_regular_hex = (len(pts) == 6 and all_equal)
    print(f"  正六角形: {is_regular_hex}")

if __name__ == '__main__':
    verify_q1()
    verify_q2()
