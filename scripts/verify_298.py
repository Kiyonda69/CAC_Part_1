#!/usr/bin/env python3
"""航大思考298: 直方体の対角線が貫く小立方体の個数の検証

直方体 a×b×c を1cm角の小立方体に分割し、対角線(0,0,0)-(a,b,c)が
内部を通る（＝線分と小立方体の開内部が交わる）小立方体の個数を
厳密に数える。Fractionで交差時刻を求め、区間の中点がどの小立方体に
属するかで数える総当たり検証。
"""
from fractions import Fraction
from math import gcd


def pierced_cubes(a, b, c):
    """対角線が内部を通る小立方体の個数（厳密計算）"""
    times = {Fraction(0), Fraction(1)}
    for n, k in ((a, 'x'), (b, 'y'), (c, 'z')):
        for i in range(1, n):
            times.add(Fraction(i, n))
    ts = sorted(times)
    cubes = set()
    for t0, t1 in zip(ts, ts[1:]):
        tm = (t0 + t1) / 2  # 区間中点は必ず小立方体の内部
        cube = (int(tm * a), int(tm * b), int(tm * c))
        cubes.add(cube)
    return len(cubes), len(ts) - 2  # (個数, 内部境界イベント数)


def formula(a, b, c):
    """公式: a+b+c - gcd(a,b) - gcd(b,c) - gcd(c,a) + gcd(a,b,c)"""
    return a + b + c - gcd(a, b) - gcd(b, c) - gcd(c, a) + gcd(a, b, c)


def simultaneous_crossings(a, b, c):
    """2方向以上の境界面を同時に通過する回数（辺・頂点の通過）"""
    naive = (a - 1) + (b - 1) + (c - 1)
    _, distinct = pierced_cubes(a, b, c)
    return naive - distinct


def main():
    # ---- 問1: 4×3×5 ----
    n1, ev1 = pierced_cubes(4, 3, 5)
    assert n1 == formula(4, 3, 5) == 10, n1
    assert simultaneous_crossings(4, 3, 5) == 0  # 同時通過なし(互いに素)
    assert ev1 == 9  # 境界面の通過は 3+2+4=9 回
    options1 = [9, 10, 11, 12, 13]
    assert options1.count(10) == 1 and options1[1] == 10  # 正解(2)
    print(f"問1: 4×3×5 → 貫く小立方体 {n1} 個（境界通過 {ev1} 回・同時通過なし）")
    print(f"問1: 正解 (2) 10個 / 選択肢 {options1} で唯一")

    # ---- 問2: 6×4×3 ----
    n2, ev2 = pierced_cubes(6, 4, 3)
    assert n2 == formula(6, 4, 3) == 8, n2
    sim = simultaneous_crossings(6, 4, 3)
    assert sim == 3  # t=1/3,1/2,2/3 の3回、辺を通過
    assert ev2 == 7  # 異なる通過イベントは 10-3=7 回
    options2 = [6, 7, 8, 10, 11]
    assert options2.count(8) == 1 and options2[2] == 8  # 正解(3)
    print(f"問2: 6×4×3 → 貫く小立方体 {n2} 個（単純合計10回中、同時通過 {sim} 回）")
    print(f"問2: 正解 (3) 8個 / 選択肢 {options2} で唯一")

    # 辺通過点の確認（頂点通過でないこと）
    for t in (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3)):
        p = (6 * t, 4 * t, 3 * t)
        ints = sum(1 for v in p if v.denominator == 1)
        assert ints == 2, (t, p)  # ちょうど2座標が整数=辺の通過
    print("問2: t=1/3, 1/2, 2/3 はいずれも辺の通過（頂点通過なし）を確認")

    # 罠の値の根拠確認
    assert 6 + 3 - gcd(6, 3) == 6  # 問2罠(1): 6×3の側面に2次元公式を適用
    assert ev2 == 7                # 問2罠(2): イベント数7を個数と取り違え
    assert 1 + 10 - 1 == 10        # 問2罠(4): 同時通過を1回しか引かない
    assert 1 + 10 == 11            # 問2罠(5): 同時通過の見落とし(最重要罠)
    print("すべての検証に合格: 両問とも解は一意")


if __name__ == "__main__":
    main()
