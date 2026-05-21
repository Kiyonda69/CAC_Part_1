"""
航大思考180 検証スクリプト

問1（標準難度・3分）: 対称な家型五角柱の展開図
  正面図: 五角形 (0,0),(4,0),(4,3),(2,4),(0,3)  ← 対称な「家」型
  上面図: 4×2 の長方形を x=2 で縦に2分割
  奥行 D = 2
  面構成: 五角形 ×2 + 長方形 ×5(底4×2, 右3×2, 右斜√5×2, 左斜√5×2, 左3×2)
  正解: (2)

問2（高難度・5分）: 非対称な家型五角柱の展開図
  正面図: 五角形 (0,0),(6,0),(6,2),(2,4),(0,4)  ← 左が高い非対称な「家」型
  上面図: 6×3 の長方形を x=2 で縦に2分割（左の屋根高側と右の斜面側）
  奥行 D = 3
  面構成: 五角形 ×2 + 長方形 ×5(底6×3, 右2×3, 斜2√5×3, 上2×3, 左4×3)
  正解: (3)
"""

import math


def pentagon_edges(verts):
    """頂点列から辺(始点,終点,長さ)を順に取得（多角形は閉じている）"""
    n = len(verts)
    edges = []
    for i in range(n):
        a, b = verts[i], verts[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        edges.append((a, b, L))
    return edges


def polygon_area(verts):
    """符号付き多角形面積（シューレース公式）"""
    n = len(verts)
    s = 0.0
    for i in range(n):
        x1, y1 = verts[i]
        x2, y2 = verts[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def verify_q1():
    """問1: 対称な家型五角柱の検証"""
    print("=" * 60)
    print("問1: 対称な家型五角柱")
    print("=" * 60)

    pent = [(0, 0), (4, 0), (4, 3), (2, 4), (0, 3)]
    D = 2
    edges = pentagon_edges(pent)
    print(f"五角形頂点: {pent}")
    print(f"奥行: {D}")
    print("辺長:")
    expected_lengths = [4.0, 3.0, math.sqrt(5), math.sqrt(5), 3.0]
    labels = ["底", "右", "右斜", "左斜", "左"]
    for (a, b, L), exp, lab in zip(edges, expected_lengths, labels):
        ok = abs(L - exp) < 1e-9
        print(f"  {lab}: {a}→{b}  長さ={L:.4f}  期待={exp:.4f}  {'OK' if ok else 'NG'}")
        assert ok

    # 対称性確認
    assert abs(edges[1][2] - edges[4][2]) < 1e-9, "左右の壁の高さが対称でない"
    assert abs(edges[2][2] - edges[3][2]) < 1e-9, "屋根の左右斜辺が対称でない"
    print("対称性: OK（左右の壁・屋根が対称）")

    # 上面図の分割線
    # 屋根の頂点 (2,4) が x=2 で分割
    apex_x = pent[3][0]
    assert apex_x == 2, "頂点位置が中央でない"
    print(f"上面図の分割: x={apex_x} で2等分（4×{D} → 2×{D} + 2×{D}）")

    # 表面積
    pent_area = polygon_area(pent)
    side_area = sum(L * D for _, _, L in edges)
    total = 2 * pent_area + side_area
    print(f"五角形面積: {pent_area}")
    print(f"側面合計: {side_area:.4f}")
    print(f"表面積: {total:.4f}")

    # 選択肢: 正解は (2)
    options = {
        1: {"問題": "屋根の斜辺長を sqrt(3) と短く描画", "斜辺": math.sqrt(3), "対称": True,  "底辺": 4, "壁": 3, "誤り": "斜辺長"},
        2: {"問題": "正しい展開図",                   "斜辺": math.sqrt(5), "対称": True,  "底辺": 4, "壁": 3, "誤り": None},
        3: {"問題": "五角形端面が非対称（頂点が左ずれ）","斜辺": math.sqrt(5), "対称": False, "底辺": 4, "壁": 3, "誤り": "端面の対称性"},
        4: {"問題": "底辺が 5 と長い",                "斜辺": math.sqrt(5), "対称": True,  "底辺": 5, "壁": 3, "誤り": "底辺長"},
        5: {"問題": "壁が 2 と低い",                  "斜辺": math.sqrt(5), "対称": True,  "底辺": 4, "壁": 2, "誤り": "壁高"},
    }
    valid = []
    for k, v in options.items():
        ok = (
            abs(v["斜辺"] - math.sqrt(5)) < 1e-9 and
            v["対称"] is True and
            v["底辺"] == 4 and
            v["壁"] == 3
        )
        print(f"  ({k}) {v['問題']} → {'正解' if ok else '不正解(' + v['誤り'] + ')'}")
        if ok:
            valid.append(k)
    assert valid == [2], f"一意解でない: {valid}"
    print(f"\n問1 一意解: ({valid[0]})  [想定: (2)] OK\n")


def verify_q2():
    """問2: 非対称な家型五角柱の検証"""
    print("=" * 60)
    print("問2: 非対称な家型五角柱")
    print("=" * 60)

    pent = [(0, 0), (6, 0), (6, 2), (2, 4), (0, 4)]
    D = 3
    edges = pentagon_edges(pent)
    print(f"五角形頂点: {pent}")
    print(f"奥行: {D}")
    print("辺長:")
    expected_lengths = [6.0, 2.0, math.sqrt(20), 2.0, 4.0]
    labels = ["底", "右壁", "屋根斜辺", "屋根上辺", "左壁"]
    for (a, b, L), exp, lab in zip(edges, expected_lengths, labels):
        ok = abs(L - exp) < 1e-9
        print(f"  {lab}: {a}→{b}  長さ={L:.4f}  期待={exp:.4f}  {'OK' if ok else 'NG'}")
        assert ok

    # 上面図の分割線
    # 屋根の頂点 (2,4) で屋根上辺と屋根斜辺が分かれる → 上面図の分割は x=2
    apex_x = pent[3][0]
    print(f"上面図の分割: x={apex_x}（上面長6を 2 と 4 に分割）")

    pent_area = polygon_area(pent)
    side_area = sum(L * D for _, _, L in edges)
    total = 2 * pent_area + side_area
    print(f"五角形面積: {pent_area}")
    print(f"側面合計: {side_area:.4f}")
    print(f"表面積: {total:.4f}")

    # 選択肢: 正解は (3)
    options = {
        1: {"問題": "屋根斜辺が短い(sqrt(10))",                "斜辺": math.sqrt(10), "屋根上辺": 2, "右壁": 2, "左壁": 4, "底辺": 6, "頂点x": 2, "向き": "正", "誤り": "斜辺長"},
        2: {"問題": "右壁が3と長い",                          "斜辺": math.sqrt(20), "屋根上辺": 2, "右壁": 3, "左壁": 4, "底辺": 6, "頂点x": 2, "向き": "正", "誤り": "右壁長"},
        3: {"問題": "正しい展開図",                            "斜辺": math.sqrt(20), "屋根上辺": 2, "右壁": 2, "左壁": 4, "底辺": 6, "頂点x": 2, "向き": "正", "誤り": None},
        4: {"問題": "端面の屋根頂点が x=4 にずれている",        "斜辺": math.sqrt(20), "屋根上辺": 2, "右壁": 2, "左壁": 4, "底辺": 6, "頂点x": 4, "向き": "正", "誤り": "端面の頂点位置"},
        5: {"問題": "端面が左右反転(頂点が右側にある)",         "斜辺": math.sqrt(20), "屋根上辺": 2, "右壁": 2, "左壁": 4, "底辺": 6, "頂点x": 2, "向き": "反転", "誤り": "端面の向き"},
    }
    valid = []
    for k, v in options.items():
        ok = (
            abs(v["斜辺"] - math.sqrt(20)) < 1e-9 and
            v["屋根上辺"] == 2 and
            v["右壁"] == 2 and
            v["左壁"] == 4 and
            v["底辺"] == 6 and
            v["頂点x"] == 2 and
            v["向き"] == "正"
        )
        print(f"  ({k}) {v['問題']} → {'正解' if ok else '不正解(' + v['誤り'] + ')'}")
        if ok:
            valid.append(k)
    assert valid == [3], f"一意解でない: {valid}"
    print(f"\n問2 一意解: ({valid[0]})  [想定: (3)] OK\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("=" * 60)
    print("全検証 PASS")
    print("=" * 60)
