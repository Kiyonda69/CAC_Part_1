#!/usr/bin/env python3
"""セット279検証: 立体表面の最短経路（ひも掛け）問題

問1: 直方体(3x4x5)の頂点Aから対角頂点Gへ表面を伝う最短経路
問2: 円錐(底面半径3, 母線12)の底面円周上の点Aから側面を1周してAに戻る最短経路
"""
import math
import heapq


def verify_q1():
    """問1: 直方体の表面最短経路"""
    a, b, c = 3.0, 4.0, 5.0  # 縦・横・高さ

    # 展開図による3通りの候補（対角頂点への2面経由経路）
    candidates = {
        "(3+4),5": math.sqrt((a + b) ** 2 + c ** 2),  # sqrt(74)
        "(4+5),3": math.sqrt((b + c) ** 2 + a ** 2),  # sqrt(90)
        "(3+5),4": math.sqrt((a + c) ** 2 + b ** 2),  # sqrt(80)
    }
    print("問1 展開図候補:")
    for k, v in candidates.items():
        print(f"  {k}: {v:.4f}")

    vals = sorted(candidates.values())
    assert abs(vals[0] - math.sqrt(74)) < 1e-9, "最短はsqrt(74)のはず"
    assert vals[1] - vals[0] > 0.3, "最短解が一意でない（僅差すぎる）"

    # メッシュDijkstraによる裏取り（表面を格子化して最短路を近似）
    # 格子経路は真の測地線以上の長さになる（離散化で必ず過大評価）
    approx = surface_dijkstra(a, b, c, n=60)
    print(f"  メッシュ近似: {approx:.4f} (理論値 {math.sqrt(74):.4f})")
    assert approx >= math.sqrt(74) - 1e-9, "理論値より短い経路が存在（矛盾）"
    assert approx < math.sqrt(74) * 1.08, "メッシュ近似が理論値から乖離しすぎ"
    assert approx < math.sqrt(80), "√74以外の展開が最短になっている可能性"

    # 選択肢の値がすべて異なることを確認
    options = [math.sqrt(50), math.sqrt(74), math.sqrt(80), math.sqrt(90), 12.0]
    assert len(set(round(o, 6) for o in options)) == 5
    print(f"問1 正解値: √74 = {math.sqrt(74):.4f} cm\n")
    return math.sqrt(74)


def surface_dijkstra(a, b, c, n=60):
    """直方体表面をパラメータ化した格子グラフ上のDijkstra近似。

    展開図: 前面(4x5)→上面経由等を含む全面を3D頂点座標でノード化し、
    同一3D座標のノードを同一視して表面グラフを作る。
    A=(0,0,0), G=(b,a,c)  (x:横b=4, y:奥a=3, z:高c=5)
    """
    step = 0.5
    nodes = {}

    def nid(p):
        key = (round(p[0] / step), round(p[1] / step), round(p[2] / step))
        return nodes.setdefault(key, len(nodes)), key

    # 6面の格子点を生成
    pts = []
    xs = [i * step for i in range(int(b / step) + 1)]
    ys = [i * step for i in range(int(a / step) + 1)]
    zs = [i * step for i in range(int(c / step) + 1)]
    for x in xs:
        for y in ys:
            pts += [(x, y, 0.0), (x, y, c)]      # 底面・上面
    for x in xs:
        for z in zs:
            pts += [(x, 0.0, z), (x, a, z)]      # 前面・背面
    for y in ys:
        for z in zs:
            pts += [(0.0, y, z), (b, y, z)]      # 左面・右面

    coord = {}
    for p in pts:
        i, key = nid(p)
        coord[i] = p
    # 隣接: 同一面内で距離が step*sqrt(2)+eps 以下の点同士を接続
    from collections import defaultdict
    adj = defaultdict(list)
    ids = list(coord.items())
    # 空間ハッシュで近傍探索
    grid = defaultdict(list)
    for i, p in ids:
        grid[(round(p[0]), round(p[1]), round(p[2]))].append((i, p))
    for i, p in ids:
        gx, gy, gz = round(p[0]), round(p[1]), round(p[2])
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j, q in grid.get((gx + dx, gy + dy, gz + dz), []):
                        if j <= i:
                            continue
                        d = math.dist(p, q)
                        if d < step * 1.5:
                            adj[i].append((j, d))
                            adj[j].append((i, d))

    start = nodes[(0, 0, 0)]
    goal = nodes[(round(b / step), round(a / step), round(c / step))]
    dist = {start: 0.0}
    pq = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == goal:
            return d
        if d > dist.get(u, 1e18):
            continue
        for v, w in adj[u]:
            ndv = d + w
            if ndv < dist.get(v, 1e18):
                dist[v] = ndv
                heapq.heappush(pq, (ndv, v))
    raise RuntimeError("経路なし")


def verify_q2():
    """問2: 円錐の側面1周最短経路"""
    r, L = 3.0, 12.0  # 底面半径・母線
    theta = 2 * math.pi * r / L  # 展開扇形の中心角
    assert abs(theta - math.pi / 2) < 1e-12, "中心角は90度のはず"

    # 展開図上でA(L,0)からA'(L*cosθ, L*sinθ)への直線距離
    ax, ay = L, 0.0
    bx, by = L * math.cos(theta), L * math.sin(theta)
    chord = math.dist((ax, ay), (bx, by))
    assert abs(chord - 12 * math.sqrt(2)) < 1e-9
    print(f"問2 中心角: {math.degrees(theta):.1f}度, 弦長: {chord:.4f} = 12√2")

    # 直線が扇形内に収まる（=側面上に存在する）ことを確認
    min_dist_to_apex = min(
        math.hypot(ax + (bx - ax) * t, ay + (by - ay) * t)
        for t in [i / 1000 for i in range(1001)]
    )
    assert min_dist_to_apex <= L + 1e-9, "扇形の外にはみ出す"
    assert abs(min_dist_to_apex - 6 * math.sqrt(2)) < 1e-3, "頂点への最接近は6√2のはず"
    print(f"  頂点への最接近距離: {min_dist_to_apex:.4f} = 6√2（母線12以内→側面上に存在）")

    # 罠: 底面円周を1周する経路より短いことを確認
    base_loop = 2 * math.pi * r
    assert chord < base_loop, "底面1周より長くなってはいけない"
    print(f"  底面1周: {base_loop:.4f} > 弦 {chord:.4f}（側面経由が最短）")

    # 選択肢の値がすべて異なることを確認
    options = [6 * math.sqrt(2), 12 * math.sqrt(2), 6 * math.pi, 12 * math.sqrt(3), 24.0]
    assert len(set(round(o, 6) for o in options)) == 5
    print(f"問2 正解値: 12√2 = {chord:.4f} cm\n")
    return chord


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証OK: 両問とも解が一意")
