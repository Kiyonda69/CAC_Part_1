#!/usr/bin/env python3
"""セット294の検証: 資料読取（人口統計の比率計算）

問1: 5市の面積・人口（2015/2025）の実数表から「確実にいえる」記述を判定
問2: 同じ5市の世帯数を加えた表から「確実にいえる」記述を判定（高難度）

各選択肢の真偽を厳密な分数計算（Fraction）で判定し、
真である記述がちょうど1つ（＝正解肢）であることを確認する。
"""
from fractions import Fraction as F

# ---------- データ定義 ----------
# 市: (面積km², 人口2015千人, 人口2025千人, 世帯2015千世帯, 世帯2025千世帯)
DATA = {
    'A': (120, 216, 238, 80, 96),
    'B': (85, 187, 204, 68, 80),
    'C': (240, 456, 480, 160, 200),
    'D': (64, 144, 160, 48, 64),
    'E': (150, 330, 315, 120, 140),
}
CITIES = list(DATA.keys())

area = {c: DATA[c][0] for c in CITIES}
p15 = {c: DATA[c][1] for c in CITIES}
p25 = {c: DATA[c][2] for c in CITIES}
h15 = {c: DATA[c][3] for c in CITIES}
h25 = {c: DATA[c][4] for c in CITIES}


def verify_q1():
    """問1: 各選択肢の真偽を判定（正解: (1)のみ真）"""
    results = {}

    # (1) 2015→2025の5市合計人口の増加数は60千人を上回る【真であるべき】
    total15 = sum(p15.values())
    total25 = sum(p25.values())
    results[1] = (total25 - total15) > 60
    print(f"(1) 合計人口: {total15}→{total25} 増加数={total25 - total15}千人 "
          f"(>60? {results[1]})")

    # (2) 2025年の人口密度が最も高いのはB市【偽であるべき: 最高はD】
    dens25 = {c: F(p25[c], area[c]) for c in CITIES}
    top_d = max(CITIES, key=lambda c: dens25[c])
    results[2] = (top_d == 'B')
    print(f"(2) 2025密度(千人/km²): "
          f"{[f'{c}:{float(dens25[c]):.3f}' for c in CITIES]} 最高={top_d}")

    # (3) 人口増加率が最も大きいのはA市【偽であるべき: 最大はD】
    rate = {c: F(p25[c] - p15[c], p15[c]) for c in CITIES}
    top_r = max(CITIES, key=lambda c: rate[c])
    results[3] = (top_r == 'A')
    print(f"(3) 増加率: {[f'{c}:{float(rate[c]) * 100:.2f}%' for c in CITIES]} "
          f"最大={top_r}")

    # (4) 2025年のC市の構成比は35%を超える【偽であるべき: 約34.4%】
    share_c = F(p25['C'], total25)
    results[4] = share_c > F(35, 100)
    print(f"(4) C市構成比: {float(share_c) * 100:.2f}% (>35%? {results[4]})")

    # (5) 2015年の人口密度が2千人/km²未満の市は3つ【偽であるべき: 2つ(A,C)】
    dens15 = {c: F(p15[c], area[c]) for c in CITIES}
    under = [c for c in CITIES if dens15[c] < 2]
    results[5] = (len(under) == 3)
    print(f"(5) 2015密度2未満: {under} ({len(under)}市)")

    return results


def verify_q2():
    """問2: 各選択肢の真偽を判定（正解: (5)のみ真）"""
    results = {}

    # (1) 2015年の1世帯当たり人員が最も多いのはC市【偽: 最多はD(3.00)】
    pph15 = {c: F(p15[c], h15[c]) for c in CITIES}
    top15 = max(CITIES, key=lambda c: pph15[c])
    results[1] = (top15 == 'C')
    print(f"(1) 2015世帯人員: {[f'{c}:{float(pph15[c]):.3f}' for c in CITIES]} "
          f"最多={top15}")

    # (2) 世帯数の増加率が最も大きいのはC市【偽: 最大はD(+33.3%)】
    hrate = {c: F(h25[c] - h15[c], h15[c]) for c in CITIES}
    top_h = max(CITIES, key=lambda c: hrate[c])
    results[2] = (top_h == 'C')
    print(f"(2) 世帯増加率: {[f'{c}:{float(hrate[c]) * 100:.2f}%' for c in CITIES]} "
          f"最大={top_h}")

    # (3) 5市合計世帯数の増加率は25%を超える【偽: 約21.8%】
    ht15, ht25 = sum(h15.values()), sum(h25.values())
    tot_rate = F(ht25 - ht15, ht15)
    results[3] = tot_rate > F(25, 100)
    print(f"(3) 合計世帯: {ht15}→{ht25} 増加率={float(tot_rate) * 100:.2f}% "
          f"(>25%? {results[3]})")

    # (4) E市の1世帯当たり人員の減少率は15%を下回る【偽: 約18.2%】
    e15 = F(p15['E'], h15['E'])
    e25 = F(p25['E'], h25['E'])
    drop = (e15 - e25) / e15
    results[4] = drop < F(15, 100)
    print(f"(4) E市世帯人員: {float(e15):.3f}→{float(e25):.3f} "
          f"減少率={float(drop) * 100:.2f}% (<15%? {results[4]})")

    # (5) 2025年に1世帯当たり人員が2.5人を上回るのはB市のみ【真であるべき】
    pph25 = {c: F(p25[c], h25[c]) for c in CITIES}
    above = [c for c in CITIES if pph25[c] > F(5, 2)]
    results[5] = (above == ['B'])
    print(f"(5) 2025世帯人員: {[f'{c}:{float(pph25[c]):.3f}' for c in CITIES]} "
          f"2.5超={above}")
    # 境界チェック: D市はちょうど2.50（「上回る」に含まれない）であることを明示
    assert pph25['D'] == F(5, 2), "D市は正確に2.50であるべき"

    return results


def main():
    print("=" * 60)
    print("問1の検証（正解: (1)）")
    print("=" * 60)
    r1 = verify_q1()
    true1 = [k for k, v in r1.items() if v]
    print(f"→ 真の選択肢: {true1}")
    assert true1 == [1], f"問1: 真が{true1}（(1)のみ真であるべき）"

    print()
    print("=" * 60)
    print("問2の検証（正解: (5)）")
    print("=" * 60)
    r2 = verify_q2()
    true2 = [k for k, v in r2.items() if v]
    print(f"→ 真の選択肢: {true2}")
    assert true2 == [5], f"問2: 真が{true2}（(5)のみ真であるべき）"

    print()
    print("検証OK: 問1は(1)のみ、問2は(5)のみが真（唯一解）")


if __name__ == '__main__':
    main()
