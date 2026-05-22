"""
航大思考180 検証スクリプト（v3: 各選択肢を視覚的に大きく異ならせた版）

問1（標準難度・3分）: 対称な家型五角柱の展開図
  正面図: 五角形 (0,0),(4,0),(4,3),(2,4),(0,3)  ← 対称な「家」型
  上面図: 4×2 の長方形を x=2 で縦に2分割
  奥行 D = 2

  選択肢ペンタゴン（各々顕著に異なる形状）:
    (1) 屋根が極端に高い: (0,0),(4,0),(4,3),(2,6),(0,3)  高さ6（正解の1.5倍）
    (2) 正解:             (0,0),(4,0),(4,3),(2,4),(0,3)  高さ4
    (3) 頂点が極端に左:   (0,0),(4,0),(4,3),(0.5,4),(0,3)  apex x=0.5
    (4) 底辺が極端に広い: (0,0),(6,0),(6,3),(3,4),(0,3)  底6（正解の1.5倍）
    (5) 屋根が極端に平ら: (0,0),(4,0),(4,2),(2,2.5),(0,2)  高さ2.5・壁2
  正解: (2)

問2（高難度・5分）: 非対称な家型五角柱の展開図
  正面図: 五角形 (0,0),(6,0),(6,2),(2,4),(0,4)  ← 左が高い非対称
  上面図: 6×3 の長方形を x=2 で縦に2分割
  奥行 D = 3

  選択肢ペンタゴン（各々顕著に異なる形状）:
    (1) 極端に低い: (0,0),(6,0),(6,1),(2,2),(0,2)  高さ2（正解の半分）
    (2) 右壁が極端に高い: (0,0),(6,0),(6,4),(2,5),(0,5)  右壁4（正解の2倍）
    (3) 正解: (0,0),(6,0),(6,2),(2,4),(0,4)
    (4) 頂点が極端に右: (0,0),(6,0),(6,2),(5,4),(0,4)  apex x=5（端寄り）
    (5) 左右反転: (0,0),(6,0),(6,4),(4,4),(0,2)
  正解: (3)
"""

import math


def pentagon_edges(verts):
    n = len(verts)
    edges = []
    for i in range(n):
        a, b = verts[i], verts[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        edges.append((a, b, L))
    return edges


def verify_q1():
    print("=" * 60)
    print("問1: 対称な家型五角柱（正解=(2)）")
    print("=" * 60)

    target_lengths = [4.0, 3.0, math.sqrt(5), math.sqrt(5), 3.0]

    options = {
        1: [(0, 0), (4, 0), (4, 3), (2, 6), (0, 3)],
        2: [(0, 0), (4, 0), (4, 3), (2, 4), (0, 3)],
        3: [(0, 0), (4, 0), (4, 3), (0.5, 4), (0, 3)],
        4: [(0, 0), (6, 0), (6, 3), (3, 4), (0, 3)],
        5: [(0, 0), (4, 0), (4, 2), (2, 2.5), (0, 2)],
    }
    descriptions = {
        1: "屋根が極端に高い（高さ6）",
        2: "正解（対称・高さ4）",
        3: "頂点が極端に左（apex x=0.5）",
        4: "底辺が極端に広い（底6）",
        5: "屋根が極端に平ら（高さ2.5・壁2）",
    }
    valid = []
    for k, pent in options.items():
        edges = pentagon_edges(pent)
        lengths = [round(L, 4) for _, _, L in edges]
        target = [round(L, 4) for L in target_lengths]
        length_ok = lengths == target
        apex_ok = pent[3][0] == 2
        ok = length_ok and apex_ok
        print(f"  ({k}) {descriptions[k]} 辺長={lengths} apex_x={pent[3][0]} → {'正解' if ok else '不正解'}")
        if ok:
            valid.append(k)
    assert valid == [2], f"一意解でない: {valid}"
    print(f"\n問1 一意解: ({valid[0]})  [想定: (2)] OK\n")


def verify_q2():
    print("=" * 60)
    print("問2: 非対称な家型五角柱（正解=(3)）")
    print("=" * 60)

    target_lengths = [6.0, 2.0, math.sqrt(20), 2.0, 4.0]
    target_apex_x = 2

    options = {
        1: [(0, 0), (6, 0), (6, 1), (2, 2), (0, 2)],
        2: [(0, 0), (6, 0), (6, 4), (2, 5), (0, 5)],
        3: [(0, 0), (6, 0), (6, 2), (2, 4), (0, 4)],
        4: [(0, 0), (6, 0), (6, 2), (5, 4), (0, 4)],
        5: [(0, 0), (6, 0), (6, 4), (4, 4), (0, 2)],
    }
    descriptions = {
        1: "極端に低い（高さ2）",
        2: "右壁が極端に高い（右壁4・apex y=5）",
        3: "正解",
        4: "頂点が極端に右（apex x=5）",
        5: "左右反転（右壁4・左壁2・apex右側）",
    }
    valid = []
    for k, pent in options.items():
        edges = pentagon_edges(pent)
        lengths = [round(L, 4) for _, _, L in edges]
        target = [round(L, 4) for L in target_lengths]
        length_ok = lengths == target
        apex_ok = pent[3][0] == target_apex_x
        ok = length_ok and apex_ok
        print(f"  ({k}) {descriptions[k]} 辺長={lengths} apex_x={pent[3][0]} → {'正解' if ok else '不正解'}")
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
