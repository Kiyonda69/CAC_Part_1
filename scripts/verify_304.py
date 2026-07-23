#!/usr/bin/env python3
"""航大思考304: n角柱の対角線の本数の規則性の検証
問1: 空間対角線（どの面上にもない対角線）の本数 → 十角柱で70本
問2: 対角線の総数（面の対角線＋空間対角線）が初めて200を超える → 十二角柱
実座標でn角柱を構成し、全頂点対を辺/面の対角線/空間対角線に分類して総当たり検証する。
"""
import math
from itertools import combinations


def build_prism(n):
    """n角柱の頂点座標・辺・面（頂点インデックス集合）を返す"""
    bottom = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n), 0.0)
              for k in range(n)]
    top = [(x, y, 1.0) for (x, y, _) in bottom]
    verts = bottom + top
    edges = set()
    for k in range(n):
        edges.add(frozenset({k, (k + 1) % n}))            # 底面の辺
        edges.add(frozenset({n + k, n + (k + 1) % n}))    # 上面の辺
        edges.add(frozenset({k, n + k}))                  # 側面の縦の辺
    faces = [frozenset(range(n)), frozenset(range(n, 2 * n))]  # 底面・上面
    for k in range(n):
        faces.append(frozenset({k, (k + 1) % n, n + (k + 1) % n, n + k}))  # 側面
    return verts, edges, faces


def classify(n):
    """(空間対角線の本数, 面の対角線の本数, 対角線の総数) を数え上げで返す"""
    verts, edges, faces = build_prism(n)
    space = face_diag = 0
    for i, j in combinations(range(2 * n), 2):
        pair = frozenset({i, j})
        if pair in edges:
            continue
        if any(i in f and j in f for f in faces):
            face_diag += 1
        else:
            space += 1
    return space, face_diag, space + face_diag


def verify_q1():
    """問1: 空間対角線の本数が n(n-3) に従い、十角柱で70本（選択肢中唯一）"""
    seq = []
    for n in range(3, 13):
        space, _, _ = classify(n)
        assert space == n * (n - 3), f"n={n}: {space} != n(n-3)"
        seq.append(space)
    # 図で提示する 三角柱0・四角柱4・五角柱10（と六角柱18）
    assert seq[:4] == [0, 4, 10, 18], seq[:4]
    # 階差 4,6,8,... の公差2の等差数列であること
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    assert diffs == [4 + 2 * k for k in range(len(diffs))], diffs
    ans = classify(10)[0]
    assert ans == 70, ans
    # 選択肢の検証: 70のみが十角柱の空間対角線数
    choices = [35, 54, 70, 80, 140]
    assert [c for c in choices if c == ans] == [70]
    print(f"問1 OK: 空間対角線 数列(3〜12角柱) = {seq}, 十角柱 = {ans}本")


def verify_q2():
    """問2: 対角線の総数 2n(n-2) が初めて200を超えるのは十二角柱（唯一解）"""
    totals = {}
    for n in range(3, 20):
        space, face_d, total = classify(n)
        # 面の対角線: 底面・上面 n(n-3)/2 ×2 ＋ 側面の長方形 2本×n
        assert face_d == n * (n - 3) + 2 * n, f"n={n}"
        assert total == 2 * n * (n - 2), f"n={n}: {total} != 2n(n-2)"
        totals[n] = total
    # 図の値: 三角柱6・四角柱16・五角柱30（階差10,14,18,...の公差4）
    assert [totals[n] for n in (3, 4, 5, 6, 7)] == [6, 16, 30, 48, 70]
    # 初めて200を超えるnの一意性（十一角柱は198でちょうど超えない）
    first = min(n for n in totals if totals[n] > 200)
    assert first == 12 and totals[11] == 198 and totals[12] == 240
    print(f"問2 OK: 総数 n=10..13 -> {[totals[n] for n in (10, 11, 12, 13)]}, "
          f"初めて200超は {first}角柱")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証OK: 解は一意")
