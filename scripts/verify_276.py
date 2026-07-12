#!/usr/bin/env python3
"""航大思考276: 円を直線で分割したときの領域数の検証。

実座標で弦の配置を構成し、オイラーの公式 V-E+F=2 から面数を数えて
組合せ論的な公式（増分規則）と一致することを確認する。
"""
import math

R = 10.0
EPS = 1e-9


def line_from_point_angle(px, py, deg):
    """点(px,py)を通り角度degの直線 -> (dx,dy,px,py)"""
    t = math.radians(deg)
    return (math.cos(t), math.sin(t), px, py)


def chord_endpoints(line):
    """直線と円 x^2+y^2=R^2 の2交点"""
    dx, dy, px, py = line
    b = px * dx + py * dy
    c = px * px + py * py - R * R
    disc = b * b - c
    assert disc > EPS, "直線が円と交わらない"
    s = math.sqrt(disc)
    return [(px + (-b - s) * dx, py + (-b - s) * dy),
            (px + (-b + s) * dx, py + (-b + s) * dy)]


def intersect(l1, l2):
    """2直線の交点（平行ならNone）"""
    d1x, d1y, p1x, p1y = l1
    d2x, d2y, p2x, p2y = l2
    det = d1x * d2y - d1y * d2x
    if abs(det) < EPS:
        return None
    t = ((p2x - p1x) * d2y - (p2y - p1y) * d2x) / det
    return (p1x + t * d1x, p1y + t * d1y)


def count_regions(lines):
    """円内の領域数をオイラーの公式で数える"""
    n = len(lines)
    # 円内の交点（重複統合）
    pts = []  # [(x, y, set(line_ids))]
    for i in range(n):
        for j in range(i + 1, n):
            p = intersect(lines[i], lines[j])
            if p is None:
                continue
            assert math.hypot(*p) < R - 1e-6, f"交点が円外: 直線{i},{j}"
            for q in pts:
                if math.hypot(p[0] - q[0], p[1] - q[1]) < 1e-6:
                    q[2].update({i, j})
                    break
            else:
                pts.append([p[0], p[1], {i, j}])
    interior = len(pts)
    # 頂点: 円周上の端点2n + 円内交点
    V = 2 * n + interior
    # 辺: 円弧2n + 各弦の分割数(弦上の交点数+1)
    seg = sum(sum(1 for q in pts if i in q[2]) + 1 for i in range(n))
    E = 2 * n + seg
    F = E - V + 2  # オイラーの公式
    regions = F - 1  # 外側の面を除く
    multi = [q for q in pts if len(q[2]) > 2]
    return regions, interior, multi


# ===== 問1: 一般位置（どの2本も円内で交わり、3本が1点で交わらない）=====
def general_lines(n):
    return [line_from_point_angle(0.9 * math.cos(2.39996 * i),
                                  0.9 * math.sin(2.39996 * i),
                                  180.0 * i / n + 7.0) for i in range(n)]


print("=== 問1: 一般位置の直線 n 本 ===")
seq = {}
for n in range(1, 9):
    regions, inter, multi = count_regions(general_lines(n))
    assert not multi, f"n={n}: 意図しない3本共点"
    formula = 1 + n + n * (n - 1) // 2
    assert regions == formula, f"n={n}: 実測{regions} != 公式{formula}"
    assert inter == n * (n - 1) // 2
    seq[n] = regions
    print(f"  n={n}: 領域数={regions} (増分+{n})")
assert (seq[1], seq[2], seq[3]) == (2, 4, 7), "例示図(1,2,3本)の値"
assert seq[7] == 29, "問1の正解"
assert seq[5] == 16 and seq[6] == 22 and seq[8] == 37, "誤答選択肢の根拠値"

# ===== 問2: 8本（3本平行 + 3本共点P + 自由2本）=====
print("=== 問2: 8本（a,b,c平行 / f,g,hが点Pで共点）===")
P = (0.8, -0.5)
lines2 = [
    line_from_point_angle(-1.5 * math.sin(math.radians(78)),
                          1.5 * math.cos(math.radians(78)), 78),   # a
    line_from_point_angle(0.0, 0.0, 78),                            # b
    line_from_point_angle(1.5 * math.sin(math.radians(78)),
                          -1.5 * math.cos(math.radians(78)), 78),  # c
    line_from_point_angle(-0.5, 0.9, 5),                            # d
    line_from_point_angle(0.4, 1.2, 130),                           # e
    line_from_point_angle(P[0], P[1], 20),                          # f
    line_from_point_angle(P[0], P[1], 55),                          # g
    line_from_point_angle(P[0], P[1], 160),                         # h
]
regions2, inter2, multi2 = count_regions(lines2)
print(f"  領域数={regions2}, 円内交点={inter2}個, 3本以上の共点={len(multi2)}個")
assert len(multi2) == 1 and len(multi2[0][2]) == 3, "共点はPの1か所・3本のみ"
assert inter2 == 23, f"交点数23のはず: {inter2}"  # 25組-3組+1点
assert regions2 == 33, f"問2の正解33のはず: {regions2}"

# 増分規則による検算: 領域増 = その直線上の交点数 + 1
inc = [1, 1, 1, 4, 5, 6, 7, 7]  # a,b,c,d,e,f,g,h
assert 1 + sum(inc) == 33, "増分規則の検算"
# 誤答の根拠値: 37(条件無視) / 32(共点で2減) / 31(共点で3減) / 29(7本扱い)
assert 1 + 8 + 28 == 37 and 37 - 3 - 2 == 32 and 37 - 3 - 3 == 31
assert 1 + 7 + 21 == 29

print("\nすべての検証に合格: 問1=29(正解(4)) / 問2=33(正解(4))")
