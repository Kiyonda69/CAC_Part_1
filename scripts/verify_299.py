#!/usr/bin/env python3
"""
航大思考299 検証コード
空間内の直線と辺の位置関係（平行・交わる・ねじれの位置）

問1: 立方体ABCD−EFGHの辺ABと他の11辺について、
     平行な辺（ア）とねじれの位置にある辺（イ）の本数の組合せ
問2: 正六角柱ABCDEF−GHIJKLの辺ABと他の17辺について、
     交わる辺（ア）とねじれの位置にある辺（イ）の本数の組合せ
     （CD・EFは同一平面上で延長すると交わる＝ねじれではない点が核心）

検証内容:
- ベクトル計算による全辺の位置関係（平行/交わる/ねじれ）の厳密分類
- 本数の検算（合計が残り辺数と一致）
- 選択肢の組合せの中で正解が唯一であることの確認
"""

import math

EPS = 1e-9


def sub(p, q):
    return tuple(p[i] - q[i] for i in range(3))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return sum(u[i] * v[i] for i in range(3))


def norm(u):
    return math.sqrt(dot(u, u))


def classify(line1, line2):
    """2辺（を含む直線）の位置関係: 'parallel' / 'intersect' / 'skew'"""
    p1, p2 = line1
    q1, q2 = line2
    d1, d2 = sub(p2, p1), sub(q2, q1)
    c = cross(d1, d2)
    if norm(c) < EPS:  # 方向が平行（同一直線は辺集合上あり得ない前提）
        return "parallel"
    w = sub(q1, p1)
    # 共面 <=> スカラー三重積が0
    if abs(dot(c, w)) < EPS:
        return "intersect"
    return "skew"


def count_relations(edges, base):
    counts = {"parallel": 0, "intersect": 0, "skew": 0}
    detail = {"parallel": [], "intersect": [], "skew": []}
    for name, e in edges.items():
        if e is base:
            continue
        r = classify(base, e)
        counts[r] += 1
        detail[r].append(name)
    return counts, detail


def verify_q1():
    print("=== 問1: 立方体の辺ABとの位置関係 ===")
    V = {
        "A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0),
        "E": (0, 0, 1), "F": (1, 0, 1), "G": (1, 1, 1), "H": (0, 1, 1),
    }
    edge_names = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE",
                  "AE", "BF", "CG", "DH"]
    edges = {n: (V[n[0]], V[n[1]]) for n in edge_names}
    counts, detail = count_relations(edges, edges["AB"])
    print(f"  平行: {counts['parallel']}本 {detail['parallel']}")
    print(f"  交わる: {counts['intersect']}本 {detail['intersect']}")
    print(f"  ねじれ: {counts['skew']}本 {detail['skew']}")
    assert counts == {"parallel": 3, "intersect": 4, "skew": 4}
    assert sum(counts.values()) == 11
    # 選択肢（ア=平行, イ=ねじれ）: 正解は(4)
    options = {1: (2, 5), 2: (3, 2), 3: (3, 8), 4: (3, 4), 5: (1, 6)}
    answer = (counts["parallel"], counts["skew"])
    matches = [k for k, v in options.items() if v == answer]
    assert matches == [4], f"正解が唯一でない: {matches}"
    print("問1: 正解(4) ア3本・イ4本 が唯一\n")


def verify_q2():
    print("=== 問2: 正六角柱の辺ABとの位置関係 ===")
    s3 = math.sqrt(3)
    # 底面の正六角形（1辺1）: A,Bが手前の辺
    hexagon = {
        "A": (-0.5, -s3 / 2), "B": (0.5, -s3 / 2), "C": (1.0, 0.0),
        "D": (0.5, s3 / 2), "E": (-0.5, s3 / 2), "F": (-1.0, 0.0),
    }
    V = {}
    for k, (x, y) in hexagon.items():
        V[k] = (x, y, 0.0)  # 底面 A〜F
    top = {"A": "G", "B": "H", "C": "I", "D": "J", "E": "K", "F": "L"}
    for k, (x, y) in hexagon.items():
        V[top[k]] = (x, y, 1.0)  # 上面 G〜L（GはAの真上）
    edge_names = (["AB", "BC", "CD", "DE", "EF", "FA"] +
                  ["GH", "HI", "IJ", "JK", "KL", "LG"] +
                  ["AG", "BH", "CI", "DJ", "EK", "FL"])
    edges = {n: (V[n[0]], V[n[1]]) for n in edge_names}
    counts, detail = count_relations(edges, edges["AB"])
    print(f"  平行: {counts['parallel']}本 {detail['parallel']}")
    print(f"  交わる: {counts['intersect']}本 {detail['intersect']}")
    print(f"  ねじれ: {counts['skew']}本 {detail['skew']}")
    assert counts == {"parallel": 3, "intersect": 6, "skew": 8}
    assert sum(counts.values()) == 17
    # CD・EFが「交わる」（延長交差）に分類されることを個別確認
    assert "CD" in detail["intersect"] and "EF" in detail["intersect"]
    # 選択肢（ア=交わる, イ=ねじれ）: 正解は(1)
    options = {1: (6, 8), 2: (4, 10), 3: (6, 4), 4: (8, 6), 5: (4, 12)}
    answer = (counts["intersect"], counts["skew"])
    matches = [k for k, v in options.items() if v == answer]
    assert matches == [1], f"正解が唯一でない: {matches}"
    print("問2: 正解(1) ア6本・イ8本 が唯一（CD・EFは延長すると交わる）\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("すべての検証に合格しました")
