#!/usr/bin/env python3
"""航大思考305 損益算（文章のみ・2商品構成）の解の一意性検証

問1: 商品A・Bを合わせて6,000円で仕入れ、Aは原価の2割の利益を見込んだ価格で、
     Bは原価の1割引の価格で売ったところ、全体で660円の利益となった。
     Aの原価はいくらか。
問2: 商品A・Bを合わせて500個仕入れた。仕入値はA:1個300円、B:1個200円、
     仕入総額128,000円。Aは原価の3割増しの定価で全部売れた。
     Bは原価の4割増しの定価で仕入個数の6割だけ売れ、残りは定価の25％引きで
     すべて売り切った。全体の利益はいくらか。
"""


def verify_q1():
    """問1: Aの原価を10円刻みで総当たりし唯一解を確認

    10倍して整数化: 2a - (6000 - a) = 6600 (0.2a - 0.1b = 660, a + b = 6000)
    """
    valid_solutions = []
    for a in range(0, 6001, 10):        # Aの原価
        b = 6000 - a                    # Bの原価
        # 利益: Aは+0.2a, Bは-0.1b → 10倍して整数判定
        if 2 * a - b == 6600:
            valid_solutions.append((a, b))
    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在: {valid_solutions}"
    a, b = valid_solutions[0]
    profit = (12 * a // 10 - a) - (b - 9 * b // 10)
    print(f"問1: Aの原価={a}円, Bの原価={b}円")
    print(f"  検算: Aの利益={a // 5}円, Bの損失={b // 10}円, 全体={profit}円")
    assert profit == 660
    return a


def verify_q2():
    """問2: 個数の組を総当たりで確定し、利益を計算"""
    valid_counts = []
    for na in range(0, 501):            # Aの個数
        nb = 500 - na                   # Bの個数
        if 300 * na + 200 * nb == 128000:
            valid_counts.append((na, nb))
    assert len(valid_counts) == 1, f"個数の解が{len(valid_counts)}個存在: {valid_counts}"
    na, nb = valid_counts[0]
    print(f"問2: A={na}個, B={nb}個")

    # A: 原価300円 → 定価 300×1.3 = 390円ですべて売れた
    profit_a = (390 - 300) * na
    # B: 原価200円 → 定価 200×1.4 = 280円で6割、残りは定価の25%引き 210円
    nb_full = nb * 6 // 10
    assert nb * 6 % 10 == 0, "Bの6割が整数にならない"
    nb_disc = nb - nb_full
    price_disc = 280 * 75 // 100
    assert 280 * 75 % 100 == 0, "25%引きの売価が整数にならない"
    profit_b = (280 - 200) * nb_full + (price_disc - 200) * nb_disc
    total = profit_a + profit_b
    print(f"  A: 定価390円×{na}個 → 利益{profit_a}円")
    print(f"  B: 定価280円×{nb_full}個 → 利益{(280 - 200) * nb_full}円, "
          f"割引{price_disc}円×{nb_disc}個 → 利益{(price_disc - 200) * nb_disc}円")
    print(f"  全体の利益 = {total}円")
    # 売上ベースの検算
    revenue = 390 * na + 280 * nb_full + price_disc * nb_disc
    assert revenue - 128000 == total, "売上ベースの検算が不一致"
    print(f"  検算: 総売上{revenue}円 − 仕入総額128,000円 = {revenue - 128000}円")
    return total


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    print(f"\n問1の正解: {q1}円 / 問2の正解: {q2}円 — いずれも唯一解")
