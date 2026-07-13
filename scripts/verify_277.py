#!/usr/bin/env python3
"""航大思考277 検証: 円錐の転がり（頂点を固定して平面上を滑らずに転がす）

原理: 頂点Oを固定して転がすと、底面の円は半径L（母線）の円周上を転がる。
円錐がちょうど1周して元の位置に戻るまでの自転数 n = (2πL)/(2πr) = L/r
"""
import math
from math import isclose


def rotations(L, r):
    """1周あたりの自転数 = 転がった跡の円周 ÷ 底面の円周"""
    return (2 * math.pi * L) / (2 * math.pi * r)


def verify_q1():
    """問1: r=3cm, L=12cm の円錐 → 4回転"""
    L, r = 12, 3
    n = rotations(L, r)
    assert isclose(n, 4), f"回転数が4でない: {n}"
    # 選択肢の値 [2, 3, 4, 6, 8] のうち一致するのは4のみ（解の一意性）
    options = [2, 3, 4, 6, 8]
    matches = [o for o in options if isclose(n, o)]
    assert len(matches) == 1 and matches[0] == 4, f"一意でない: {matches}"
    print(f"問1 OK: L={L}, r={r} → {n:.0f}回転（選択肢中の一致は4のみ）")


def verify_q2():
    """問2: L=18cm, ちょうど3回転 → r=6cm, 中心角120°, 高さ12√2cm"""
    L, n = 18, 3
    # 転がりの条件: 2πL = n × 2πr → r = L/n
    r = L / n
    assert isclose(r, 6), f"半径が6でない: {r}"
    # 一意性: r=1〜17のうち L/r がちょうど3になるのは r=6 のみ
    valid = [rr for rr in range(1, 18) if isclose(rotations(L, rr), 3)]
    assert valid == [6], f"半径の解が一意でない: {valid}"
    # 側面展開図（おうぎ形）の中心角 = 360° × r/L
    angle = 360 * r / L
    assert isclose(angle, 120), f"中心角が120°でない: {angle}"
    # 高さ h = √(L² - r²) = √288 = 12√2
    h_sq = L * L - r * r
    assert h_sq == 288, f"h²が288でない: {h_sq}"
    assert isclose(math.sqrt(h_sq), 12 * math.sqrt(2))
    print(f"問2 OK: r={r:.0f}cm, 中心角={angle:.0f}°, 高さ=12√2cm (√{h_sq:.0f})")

    # 誤答組合せの検証: 正解 (6, 120, 12√2) 以外はいずれかが誤り
    sqrt2, sqrt3 = math.sqrt(2), math.sqrt(3)
    correct = (6, 120, 12 * sqrt2)
    combos = [
        (6, 120, 12 * sqrt2),   # 正解
        (6, 120, 12 * sqrt3),   # ウのみ誤り（√の計算ミス）
        (6, 240, 12 * sqrt2),   # イのみ誤り（中心角の残り側）
        (9, 180, 9 * sqrt3),    # 2回転と誤読した場合の整合的な誤答
        (9, 120, 9 * sqrt3),    # ア・ウ誤り
    ]
    n_correct = sum(
        1 for c in combos
        if isclose(c[0], correct[0]) and isclose(c[1], correct[1])
        and isclose(c[2], correct[2])
    )
    assert n_correct == 1, f"完全一致の組合せが{n_correct}個"
    print("問2 OK: 5つの組合せのうち完全に正しいのは1つのみ")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 両問とも解は一意")
