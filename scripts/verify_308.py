#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""航大思考308 検証スクリプト（図を伴う損益算）

問1: 3商品の原価棒グラフ＋値引き販売条件から利益合計を求める
問2: 3商品の原価棒グラフ＋一部個数未知、全体の利益率から未知の個数を求める
"""

from fractions import Fraction as F


# ---------------------------------------------------------------
# 問1: 原価（棒グラフから読み取る値）と販売条件
# ---------------------------------------------------------------
Q1_ITEMS = [
    # (商品名, 1個の原価, 仕入個数, 定価の値引き率)
    ("A", 200, 40, F(0)),      # 定価のまま
    ("B", 300, 30, F(2, 10)),  # 定価の2割引
    ("C", 400, 25, F(4, 10)),  # 定価の4割引
]
Q1_MARKUP = F(5, 10)  # 原価の5割増しの定価


def q1_profit():
    """商品ごとの利益と合計利益を返す"""
    detail, total = [], 0
    for name, cost, n, off in Q1_ITEMS:
        price = cost * (1 + Q1_MARKUP)          # 定価
        sell = price * (1 - off)                # 実際の売値
        profit = (sell - cost) * n              # その商品の利益（損失は負）
        assert price == int(price) and sell == int(sell), f"{name}: 金額が整数でない"
        detail.append((name, int(price), int(sell), int(profit)))
        total += profit
    return detail, int(total)


def q1_check():
    detail, total = q1_profit()
    print("【問1】")
    for name, price, sell, profit in detail:
        print(f"  商品{name}: 定価{price}円 → 売値{sell}円 / 利益 {profit:+,}円")
    # 別解（売上総額 − 仕入総額）による検算
    sales = sum(int(c * (1 + Q1_MARKUP) * (1 - off)) * n for _, c, n, off in Q1_ITEMS)
    buy = sum(c * n for _, c, n, _ in Q1_ITEMS)
    print(f"  売上総額 {sales:,}円 − 仕入総額 {buy:,}円 = {sales - buy:,}円")
    assert sales - buy == total, "商品別の合計と売上−仕入が一致しない"
    assert total == 4800, f"想定解と不一致: {total}"

    # --- 誤答（罠）が各誤解から導かれることを確認 ---
    # (a) 商品Cの「4割引」を「定価の4割の値段」と読み違える
    a = 4000 + 1800 + (int(600 * F(4, 10)) - 400) * 25
    # (b) 商品BとCの値引き率を取り違える
    b = 4000 + (int(450 * F(6, 10)) - 300) * 30 + (int(600 * F(8, 10)) - 400) * 25
    # (c) 商品Cの損失を無視して0とみなす
    c = 4000 + 1800 + 0
    # (d) 商品Cの損失を利益として加える
    d = 4000 + 1800 + 1000
    traps = {"4割の値段と誤読": a, "値引き率の取り違え": b,
             "損失の無視": c, "損失を利益に加算": d}
    for label, v in traps.items():
        print(f"  罠[{label}] = {v:,}円")
    options = [1800, 5100, 5800, 6800, 4800]   # (1)〜(5)
    assert sorted(traps.values()) == sorted(options[:4]), "罠と選択肢が不一致"
    assert len(set(options)) == 5, "選択肢に重複あり"
    assert options.index(total) == 4, "正解は選択肢(5)のはず"
    print(f"  → 合計利益 {total:,}円 ＝ 選択肢(5) / 一意性OK\n")
    return total


# ---------------------------------------------------------------
# 問2: 未知の個数アを全体の利益率から求める
# ---------------------------------------------------------------
Q2_MARKUP = F(6, 10)         # 原価の6割増しの定価
Q2_RATE = F(4, 10)           # 全体の利益は仕入総額の4割
# (商品名, 原価, 仕入個数)
Q2_ITEMS = {"P": (250, 80), "Q": (300, 100), "R": (500, 60)}


def q2_sales(a):
    """アを与えたときの売上総額（円）"""
    def tanka(name):
        return Q2_ITEMS[name][0] * (1 + Q2_MARKUP)

    p = tanka("P") * 80                                   # 全て定価
    q = tanka("Q") * 60 + tanka("Q") * F(75, 100) * 40    # 60個定価＋40個を2割5分引き
    r = tanka("R") * a + tanka("R") * F(1, 2) * (60 - a)  # ア個定価＋残りを半額
    return p + q + r


def q2_check():
    buy = sum(c * n for c, n in Q2_ITEMS.values())
    target = buy * (1 + Q2_RATE)
    print("【問2】")
    print(f"  仕入総額 {buy:,}円 / 目標売上総額 {int(target):,}円（利益 {int(buy * Q2_RATE):,}円）")

    # 0〜60個の総当たりで唯一解を確認
    sols = [a for a in range(61) if q2_sales(a) == target]
    assert len(sols) == 1, f"解が{len(sols)}個存在: {sols}"
    ans = sols[0]
    print(f"  ア = {ans}個（0〜60個の総当たりで唯一解）")

    # --- 誤答（罠）が各誤解から導かれることを確認 ---
    # (a) 商品Qの値引きを見落とし、100個すべて定価で売れたとする
    a1 = [a for a in range(61)
          if 400 * 80 + 480 * 100 + 800 * a + 400 * (60 - a) == target]
    # (b) 半額を「定価の4割引」と読み違える
    a2 = [a for a in range(61)
          if 400 * 80 + (480 * 60 + 360 * 40) + 800 * a + 480 * (60 - a) == target]
    # (c) 商品Rの定価販売分と半額販売分を取り違える
    a3 = [a for a in range(61)
          if 400 * 80 + (480 * 60 + 360 * 40) + 400 * a + 800 * (60 - a) == target]
    # (d) 売れ残り（半額販売分）の売上を0円としてしまう
    a4 = [a for a in range(61)
          if 400 * 80 + (480 * 60 + 360 * 40) + 800 * a == target]
    traps = {"Qの値引き見落とし": a1, "半額を4割引と誤読": a2,
             "定価分と半額分の取り違え": a3, "売れ残りを0円と誤る": a4}
    vals = []
    for label, s in traps.items():
        assert len(s) == 1, f"罠[{label}]が整数解を持たない: {s}"
        print(f"  罠[{label}] = {s[0]}個")
        vals.append(s[0])

    options = [20, 32, 25, 28, 46]   # (1)〜(5)
    assert sorted(vals) == sorted([o for o in options if o != ans]), "罠と選択肢が不一致"
    assert len(set(options)) == 5, "選択肢に重複あり"
    assert options.index(ans) == 1, "正解は選択肢(2)のはず"

    # 内訳の検算
    print(f"  内訳: P {400 * 80:,}円 / Q {480 * 60 + 360 * 40:,}円 "
          f"/ R {800 * ans + 400 * (60 - ans):,}円 = {int(q2_sales(ans)):,}円")
    print(f"  → ア＝{ans}個 ＝ 選択肢(2) / 一意性OK\n")
    return ans


if __name__ == "__main__":
    q1_check()
    q2_check()
    print("すべての検証に成功しました。")
