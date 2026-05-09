"""
航大思考160: 立方体の切断面検証

問1: 3点の中点を通る平面で切ったときの切り口
  - P1: 前底辺の中点 (0.5, 0, 0)
  - P2: 後右垂直辺の中点 (1, 1, 0.5)
  - P3: 上左辺の中点 (0, 0.5, 1)
  → 正六角形

問2: 3点を通る平面で切ったときの切り口
  - P1: 前底辺3/4の点 (0.75, 0, 0)
  - P2: 後左垂直辺の中点 (0, 1, 0.5)
  - P3: 前上辺1/4の点 (0.25, 0, 1)
  → 五角形
"""

import math


def vsub(a, b):
    return tuple(a[i] - b[i] for i in range(3))


def vadd(a, b):
    return tuple(a[i] + b[i] for i in range(3))


def vmul(a, k):
    return tuple(a[i] * k for i in range(3))


def vdot(a, b):
    return sum(a[i] * b[i] for i in range(3))


def vcross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vnorm(a):
    return math.sqrt(vdot(a, a))


def cube_edges():
    """立方体の12辺をリストで返す（端点座標のペア）"""
    vertices = [
        (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0),  # 底面 V1-V4
        (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),  # 上面 V5-V8
    ]
    edges_idx = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # 底面の辺
        (4, 5), (5, 6), (6, 7), (7, 4),  # 上面の辺
        (0, 4), (1, 5), (2, 6), (3, 7),  # 垂直辺
    ]
    return [(vertices[a], vertices[b]) for a, b in edges_idx]


def plane_edge_intersect(p1, p2, normal, d):
    """辺p1-p2と平面 n·x = d の交点を求める。なければNone"""
    direction = vsub(p2, p1)
    denom = vdot(normal, direction)
    if abs(denom) < 1e-9:
        return None
    t = (d - vdot(normal, p1)) / denom
    if -1e-9 <= t <= 1 + 1e-9:
        return vadd(p1, vmul(direction, t))
    return None


def points_close(a, b, tol=1e-6):
    return all(abs(a[i] - b[i]) < tol for i in range(3))


def cross_section(normal, d):
    """平面 n·x = d による立方体の切り口の頂点を返す（重複除去）"""
    points = []
    for p1, p2 in cube_edges():
        ip = plane_edge_intersect(p1, p2, normal, d)
        if ip is not None:
            if not any(points_close(ip, q) for q in points):
                points.append(ip)
    return points


def shape_name(n):
    return {3: "三角形", 4: "四角形", 5: "五角形", 6: "六角形"}.get(n, f"{n}角形")


def order_points(pts, normal):
    """凸包順に並べる"""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    cz = sum(p[2] for p in pts) / len(pts)
    center = (cx, cy, cz)

    nlen = vnorm(normal)
    nu = tuple(normal[i] / nlen for i in range(3))

    u = vsub(pts[0], center)
    ulen = vnorm(u)
    u = tuple(u[i] / ulen for i in range(3))
    v = vcross(nu, u)

    angles = []
    for p in pts:
        r = vsub(p, center)
        angles.append((math.atan2(vdot(r, v), vdot(r, u)), p))
    angles.sort(key=lambda x: x[0])
    return [p for _, p in angles]


def verify_problem1():
    """問1: 3つの中点を通る平面 → 正六角形"""
    P1 = (0.5, 0, 0)
    P2 = (1, 1, 0.5)
    P3 = (0, 0.5, 1)

    v1 = vsub(P2, P1)
    v2 = vsub(P3, P1)
    n = vcross(v1, v2)
    d = vdot(n, P1)

    print(f"問1: 法線={n}, d={d}")
    pts = cross_section(n, d)
    print(f"  交点数: {len(pts)} ({shape_name(len(pts))})")
    for p in pts:
        print(f"    {p}")

    if len(pts) == 6:
        ordered = order_points(pts, n)
        print("  辺の長さ:")
        for i in range(len(ordered)):
            e = vsub(ordered[(i + 1) % len(ordered)], ordered[i])
            print(f"    辺{i + 1}: {vnorm(e):.4f}")

    assert len(pts) == 6, f"問1: 期待は6角形、実際は{len(pts)}角形"
    print("  ✓ 問1: 正六角形を確認")
    return len(pts)


def verify_problem2():
    """問2: 3点を通る平面 → 五角形"""
    P1 = (0.75, 0, 0)
    P2 = (0, 1, 0.5)
    P3 = (0.25, 0, 1)

    v1 = vsub(P2, P1)
    v2 = vsub(P3, P1)
    n = vcross(v1, v2)
    d = vdot(n, P1)

    print(f"\n問2: 法線={n}, d={d}")
    pts = cross_section(n, d)
    print(f"  交点数: {len(pts)} ({shape_name(len(pts))})")
    for p in pts:
        print(f"    {p}")

    if len(pts) == 5:
        ordered = order_points(pts, n)
        print("  順序付き頂点（凸包順）:")
        for i, p in enumerate(ordered):
            print(f"    V{i + 1}: {p}")
        print("  辺の長さ:")
        for i in range(len(ordered)):
            e = vsub(ordered[(i + 1) % len(ordered)], ordered[i])
            print(f"    辺{i + 1}: {vnorm(e):.4f}")

    assert len(pts) == 5, f"問2: 期待は5角形、実際は{len(pts)}角形"
    print("  ✓ 問2: 五角形を確認")
    return len(pts)


if __name__ == "__main__":
    verify_problem1()
    verify_problem2()
    print("\n=== 全ての検証に成功 ===")
