#!/usr/bin/env python3
"""航大思考274 検証: マッチ棒の規則性問題

問1: 正六角形を横一列にn個連ねた図形のマッチ棒本数(5n+1)を
     座標ベースの辺集合で総当たり検証し、100本で作れる最大個数を確認。
問2: 一辺nの大正三角形を一辺1の小三角形に分割した図形の
     マッチ棒本数(3n(n+1)/2)と上向き小三角形の個数(n(n+1)/2)を検証。
"""
from fractions import Fraction


def hexagon_chain_edges(n):
    """正六角形をn個横一列に連ねたときの辺集合を構築して数える。
    隣り合う六角形は1辺を共有する。"""
    import math
    edges = set()
    for i in range(n):
        # 中心を横に√3ずつずらす(共有辺=縦の辺)
        cx = Fraction(i)  # 正規化した中心x(共有判定は頂点キーで行う)
        # 頂点を30°開始の60°刻みで定義(有理数キー化のため角度indexで表現)
        # 一辺1・平頂(pointy-top)六角形: 頂点角度 30,90,150,210,270,330度
        verts = []
        for k in range(6):
            ang = math.radians(30 + 60 * k)
            x = round(i * math.sqrt(3) + math.cos(ang), 6)
            y = round(math.sin(ang), 6)
            verts.append((x, y))
        for k in range(6):
            a, b = verts[k], verts[(k + 1) % 6]
            edges.add(tuple(sorted([a, b])))
    return len(edges)


def verify_q1():
    # 規則の検証: 図nの本数 = 5n+1
    for n in range(1, 25):
        cnt = hexagon_chain_edges(n)
        assert cnt == 5 * n + 1, f"n={n}: {cnt} != {5*n+1}"
    # 100本で作れる最大個数
    valid = [n for n in range(1, 100) if 5 * n + 1 <= 100 < 5 * (n + 1) + 1]
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    assert valid[0] == 19
    # 図19=96本, 図20=101本
    assert 5 * 19 + 1 == 96 and 5 * 20 + 1 == 101
    print(f"問1 OK: 図nの本数=5n+1, 100本で最大 {valid[0]} 個 (図19=96本, 図20=101本)")
    return valid[0]


def triangle_lattice(n):
    """一辺nの大正三角形を一辺1の小三角形に分割。
    (辺の本数, 上向き小三角形数, 下向き小三角形数) を返す。"""
    edges = set()
    up = down = 0
    # 格子点: 行r(0=頂上)にr+1個。点(r, c)
    for r in range(n):
        for c in range(r + 1):
            # 上向き小三角形: (r,c),(r+1,c),(r+1,c+1)
            a, b, d = (r, c), (r + 1, c), (r + 1, c + 1)
            for e in [(a, b), (a, d), (b, d)]:
                edges.add(tuple(sorted(e)))
            up += 1
            # 下向き小三角形: (r+1,c+1),(r,c),(r,c+1) ← r行にc+1が存在する場合
            if c + 1 <= r:
                down += 1
    return len(edges), up, down


def verify_q2():
    # 規則の検証: 図nの本数 = 3n(n+1)/2
    for n in range(1, 20):
        cnt, up, down = triangle_lattice(n)
        assert cnt == 3 * n * (n + 1) // 2, f"n={n}: {cnt}"
        assert up == n * (n + 1) // 2, f"n={n}: up={up}"
        assert down == n * (n - 1) // 2, f"n={n}: down={down}"
    # 135本ちょうどになるnの一意性
    valid = [n for n in range(1, 100) if 3 * n * (n + 1) // 2 == 135]
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    n = valid[0]
    assert n == 9
    cnt, up, down = triangle_lattice(n)
    print(f"問2 OK: 135本 → n={n} (一意), 上向き={up}個, 下向き={down}個, 計={up+down}個")
    assert up == 45 and down == 36 and up + down == 81
    return up


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証OK: 両問とも唯一解")
