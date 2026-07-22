#!/usr/bin/env python3
"""航大思考296 解の一意性検証スクリプト

問1: 年齢3区分別人口の空欄穴埋め（構成比・増減率）
問2: ごみ排出量の空欄穴埋め（対前年増減率の連鎖計算）
"""


def verify_q1():
    """問1: ある市の年齢3区分別人口"""
    total_2020 = 240000
    ratio_young, ratio_work, ratio_old = 0.125, 0.60, 0.275

    # 構成比の合計が100%であること
    assert abs(ratio_young + ratio_work + ratio_old - 1.0) < 1e-9

    young = total_2020 * ratio_young   # 30,000
    work = total_2020 * ratio_work     # ア = 144,000
    old = total_2020 * ratio_old       # 66,000
    assert young == 30000 and work == 144000 and old == 66000
    assert young + work + old == total_2020

    # 2025年: 総人口4%減、高齢人口8%増
    total_2025 = total_2020 * 0.96     # 230,400
    old_2025 = old * 1.08              # 71,280
    assert total_2025 == 230400 and old_2025 == 71280

    # イ = 2025年の高齢人口の構成比（%・小数第1位）
    b = round(old_2025 / total_2025 * 100, 1)
    assert b == 30.9, b

    # 選択肢（ア, イ）: 正解は (144000, 30.9)
    options = [(144000, 30.9), (144000, 29.7), (132000, 30.9),
               (144000, 28.6), (150000, 31.5)]
    valid = [o for o in options if o == (144000, b)]
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    print("問1 OK: ア=144,000人, イ=30.9%（唯一解）")


def verify_q2():
    """問2: ごみ排出量の連鎖増減率計算"""
    # 可燃ごみ: 2021年48,000トン、増減率 -5%, -2.5%, +5%
    k = [48000]
    for r in (-5.0, -2.5, 5.0):
        k.append(k[-1] * (1 + r / 100))
    assert k == [48000, 45600, 44460, 46683], k
    assert all(v == int(v) for v in k), "非整数が発生"

    # 資源ごみ: 2021年12,800トン、増減率 +12.5%, -10%, +25%
    s = [12800]
    for r in (12.5, -10.0, 25.0):
        s.append(s[-1] * (1 + r / 100))
    assert s == [12800, 14400, 12960, 16200], s
    assert all(v == int(v) for v in s), "非整数が発生"

    a = int(k[3])                                  # ア = 46,683
    b = int(k[3] - s[3])                           # イ = 30,483
    c = round((s[3] / s[0] - 1) * 100, 1)          # ウ = 26.6
    assert (a, b, c) == (46683, 30483, 26.6), (a, b, c)

    # 選択肢（ア, イ, ウ）: 正解の組合せが唯一存在すること
    options = [(46683, 30483, 26.6), (46800, 30600, 27.5),
               (46683, 30483, 27.5), (46683, 30600, 26.6),
               (45486, 29286, 26.6)]
    valid = [o for o in options if o == (a, b, c)]
    assert len(valid) == 1, f"解が{len(valid)}個存在"

    # 罠の検算: 増減率を足し算で処理した場合の誤答
    assert 48000 * (1 - 0.025) == 46800            # ア の加法誤り
    assert round((12.5 - 10 + 25), 1) == 27.5      # ウ の加法誤り
    print("問2 OK: ア=46,683トン, イ=30,483トン, ウ=26.6%（唯一解）")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証 PASS")
