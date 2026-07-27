#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
航大思考307 検証コード（文章のみの損益算・金額が与えられない割合型）

問1: 原価の3割の利益を見込んだ定価 → 定価の2割引 → さらにその値段の1割5分引き
     最後に売った分は原価の何%の損失か
問2: 定価に対して2割5分の利益が出るように定価を設定。300個のうち
     定価で売った分と定価の4割引で売った分があり売れ残りなし。
     全体の利益が仕入総額の2割となるとき、4割引で売ったのは何個か
"""
from fractions import Fraction as F


def verify_q1():
    """問1: 連続値下げ後の損益率（原価を1として厳密計算）"""
    cost = F(1)
    price = cost * (1 + F(3, 10))          # 定価 = 原価の3割増し
    sale1 = price * (1 - F(2, 10))         # 定価の2割引
    sale2 = sale1 * (1 - F(15, 100))       # さらにその値段の1割5分引き

    assert price == F(13, 10), price
    assert sale1 == F(104, 100), sale1     # 1.04（この時点では4%の利益）
    assert sale2 == F(884, 1000), sale2    # 0.884

    loss_rate = cost - sale2               # 損失率
    assert loss_rate == F(116, 1000), loss_rate

    # 原価を実額に置いても整合することを確認（例: 原価1,000円 → 116円の損失）
    for c in range(100, 10001, 100):
        assert c * 0.884 == c - c * 0.116

    print(f"[問1] 定価={float(price)}倍 / 2割引後={float(sale1)}倍 / "
          f"1割5分引き後={float(sale2)}倍")
    print(f"[問1] 正解: 原価の {float(loss_rate)*100:.1f}% の損失")
    return loss_rate


def verify_q1_options():
    """問1の誤答選択肢が全て別値であることを確認"""
    opts = {
        "4%の利益（1割5分引きを忘れ1.04で止める）": F(4, 100),
        "5%の損失（3割-2割-1割5分=-5分と足し引き）": F(-5, 100),
        "11%の損失（1.04から0.15を引く額の誤り）": F(-11, 100),
        "11.6%の損失（正解）": F(-116, 1000),
        "15.5%の損失（2割引と1割5分引きをまとめて定価から引く）": F(-155, 1000),
    }
    # 罠の再現確認
    assert F(13, 10) * (1 - F(2, 10) - F(15, 100)) == F(845, 1000)   # → 15.5%の損失
    assert F(104, 100) - F(15, 100) == F(89, 100)                    # → 11%の損失
    vals = list(opts.values())
    assert len(set(vals)) == len(vals), "選択肢に重複がある"
    print(f"[問1] 選択肢5個すべて異なる値: OK")


def verify_q2():
    """問2: 4割引で売った個数（定価dを文字のまま総当たり検証）"""
    total = 300
    answers = []
    for k in range(0, total + 1):
        # 定価を分数dとして扱うため、d=1 で計算（比較式は両辺dで割れる）
        d = F(1)
        cost_each = d * F(3, 4)            # 定価に対して2割5分の利益 → 原価=定価の75%
        buy_total = cost_each * total
        sales = (total - k) * d + k * d * F(6, 10)
        profit = sales - buy_total
        if profit == buy_total * F(2, 10):
            answers.append(k)
    assert len(answers) == 1, f"解が{len(answers)}個: {answers}"
    k = answers[0]
    assert k == 75, k

    # 実額での検算（定価400円 → 原価300円）
    d, c = 400, 300
    sales = (300 - k) * d + k * int(d * 0.6)
    buy = 300 * c
    assert buy == 90000 and sales == 108000, (buy, sales)
    assert sales - buy == 18000 == int(buy * 0.2)
    print(f"[問2] 正解: 定価の4割引で売ったのは {k} 個")
    print(f"[問2] 検算(定価400円/原価300円): 仕入{buy:,}円 売上{sales:,}円 "
          f"利益{sales-buy:,}円 = 仕入総額の{(sales-buy)/buy:.0%}")
    return k


def verify_q2_options():
    """問2の各誤答が『特定の誤解の帰結』として整数で現れることを確認"""
    total, d = 300, F(1)

    # (a) 利益率の基準を原価と誤解: 定価=原価の1.25倍
    c = d / F(5, 4)
    buy = c * total
    for k in range(total + 1):
        if (total - k) * d + k * d * F(6, 10) - buy == buy * F(2, 10):
            trap_a = k
            break
    assert trap_a == 30, trap_a

    # (b) 「4割引」を「定価の4割で売る」と誤解: 売価=0.4d
    c = d * F(3, 4)
    buy = c * total
    for k in range(total + 1):
        if (total - k) * d + k * d * F(4, 10) - buy == buy * F(2, 10):
            trap_b = k
            break
    assert trap_b == 50, trap_b

    # (c) 割引率を2割5分と取り違え: 売価=0.75d
    for k in range(total + 1):
        if (total - k) * d + k * d * F(75, 100) - buy == buy * F(2, 10):
            trap_c = k
            break
    assert trap_c == 120, trap_c

    # (d) 定価で売った個数を答える
    trap_d = total - 75
    assert trap_d == 225

    opts = sorted([30, 50, 75, 120, 225])
    assert len(set(opts)) == 5, "選択肢に重複がある"
    print(f"[問2] 罠: 原価基準の誤解→{trap_a}個 / 0.4d誤解→{trap_b}個 / "
          f"2割5分引き誤解→{trap_c}個 / 定価販売分→{trap_d}個")
    print(f"[問2] 選択肢5個すべて異なる値: OK {opts}")


if __name__ == "__main__":
    verify_q1()
    verify_q1_options()
    print("-" * 60)
    verify_q2()
    verify_q2_options()
    print("-" * 60)
    print("すべての検証に成功しました。")
