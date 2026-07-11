#!/usr/bin/env python3
"""セット275の検証: 方眼の対角線が通るマスの数

問1: 縦6×横9の方眼に対角線1本 → 通るマスの数
問2: 縦9×横15の方眼に両対角線 → 少なくとも一方が通るマスの数

総当たり: 各マスについて対角線がマスの内部を通過するかを幾何的に判定する。
線分がマスの内部を通る ⇔ マスのx範囲と線分のy値範囲がマス内部で重なる。
"""

from fractions import Fraction
from math import gcd


def cells_crossed_by_segment(n, m, x0, y0, x1, y1):
    """横nマス×縦mマスの方眼で、線分(x0,y0)-(x1,y1)が内部を通るマスの集合。

    厳密判定: マス(i,j) = [i,i+1]×[j,j+1] の内部と線分が交わるか。
    垂直でない線分を仮定し、x区間 [max(i,min(x0,x1)), min(i+1,max(x0,x1))]
    上でのyの範囲が (j, j+1) と開区間で交わるかを分数演算で判定する。
    """
    cells = set()
    x_lo, x_hi = min(x0, x1), max(x0, x1)
    slope = Fraction(y1 - y0, x1 - x0)
    for i in range(n):
        a = max(Fraction(i), Fraction(x_lo))
        b = min(Fraction(i + 1), Fraction(x_hi))
        if a >= b:
            continue
        ya = y0 + slope * (a - x0)
        yb = y0 + slope * (b - x0)
        y_min, y_max = min(ya, yb), max(ya, yb)
        for j in range(m):
            # 開区間 (j, j+1) と [y_min, y_max] が交わる ⇔ y_max > j かつ y_min < j+1
            if y_max > j and y_min < j + 1:
                cells.add((i, j))
    return cells


def q1():
    """問1: 縦6×横9・対角線1本"""
    m, n = 6, 9
    cells = cells_crossed_by_segment(n, m, 0, 0, n, m)
    formula = m + n - gcd(m, n)
    print(f"問1: 縦{m}×横{n} 対角線が通るマス = {len(cells)} (公式値 {formula})")
    assert len(cells) == formula == 12
    # 図中の例の検証
    for (em, en, exp) in [(2, 3, 4), (3, 4, 6)]:
        c = cells_crossed_by_segment(en, em, 0, 0, en, em)
        print(f"  例: 縦{em}×横{en} → {len(c)}マス (期待 {exp})")
        assert len(c) == exp
    # 選択肢: (1)9 (2)10 (3)11 (4)12 (5)14 → 正解は(4)
    options = [9, 10, 11, 12, 14]
    assert options.count(12) == 1 and 12 in options
    return len(cells)


def q2():
    """問2: 縦9×横15・両対角線"""
    m, n = 9, 15
    d1 = cells_crossed_by_segment(n, m, 0, 0, n, m)
    d2 = cells_crossed_by_segment(n, m, 0, m, n, 0)
    union = d1 | d2
    overlap = d1 & d2
    each = m + n - gcd(m, n)
    print(f"問2: 縦{m}×横{n} 対角線1本あたり = {len(d1)} (公式値 {each})")
    print(f"  重複マス = {sorted(overlap)} ({len(overlap)}個)")
    print(f"  少なくとも一方が通るマス = {len(union)}")
    assert len(d1) == len(d2) == each == 21
    # 両対角線は中央行（下から5行目, j=4）の同じ3マスを通る
    # 対角線の傾きは3/5なので中央行の通過区間は x∈(20/3, 25/3) → 列6,7,8
    assert overlap == {(6, 4), (7, 4), (8, 4)}
    assert len(union) == 2 * each - 3 == 39
    # 選択肢: (1)36 (2)39 (3)41 (4)42 (5)45 → 正解は(2)
    options = [36, 39, 41, 42, 45]
    assert options.count(39) == 1 and 39 in options
    return len(union)


if __name__ == "__main__":
    a1 = q1()
    a2 = q2()
    print(f"\n検証OK: 問1={a1}, 問2={a2} （いずれも唯一解）")
