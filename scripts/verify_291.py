#!/usr/bin/env python3
"""航大思考291 損益算（文章題）の解の一意性検証

問1: 定価の1割5分引きで売ると原価の1割9分の利益、
     定価から550円引いて売ると原価の3割の利益。原価はいくらか。

問2: 360個仕入れ、原価の5割増しの定価。定価でn個、
     2割引で(n-30)個売れ、10個廃棄、残りは半額で売り切り。
     全体利益が仕入総額の17.5%のとき、半額で売った個数は。
"""


def verify_q1():
    """問1: 原価x・定価yを100円単位で総当たり"""
    solutions = []
    for x in range(1000, 20001):  # 原価（円）
        # 条件1: 0.85y = 1.19x → y = 1.4x（yが整数になるxのみ）
        y20 = 28 * x  # y = 1.4x → 20y = 28x
        if y20 % 20 != 0:
            continue
        y = y20 // 20
        # 条件2: y - 550 = 1.3x → 10(y-550) = 13x
        if 10 * (y - 550) == 13 * x:
            solutions.append((x, y))
    assert len(solutions) == 1, f"問1: 解が{len(solutions)}個 {solutions}"
    x, y = solutions[0]
    # 検算
    assert 0.85 * y == 1.19 * x
    assert y - 550 == 1.3 * x
    print(f"問1: 原価={x}円, 定価={y}円（唯一解）")
    print(f"  1割5分引き売価={0.85*y:.0f}円 = 原価×1.19={1.19*x:.0f}円")
    print(f"  550円引き売価={y-550}円 = 原価×1.3={1.3*x:.0f}円")
    return x


def verify_q2():
    """問2: 定価で売れた個数nを総当たり"""
    TOTAL = 360
    DISCARD = 10
    solutions = []
    for n in range(1, TOTAL + 1):
        n2 = n - 30            # 2割引で売れた個数
        m = TOTAL - n - n2 - DISCARD  # 半額で売った個数
        if n2 < 0 or m < 0:
            continue
        # 原価を1とした利益: 定価1.5→+0.5, 2割引1.2→+0.2,
        # 半額0.75→-0.25, 廃棄→-1
        profit40 = 20 * n + 8 * n2 - 10 * m - 40 * DISCARD  # 利益×40
        target40 = 7 * TOTAL  # 0.175×360×40 = 7×360
        if profit40 == target40:
            solutions.append((n, n2, m))
    assert len(solutions) == 1, f"問2: 解が{len(solutions)}個 {solutions}"
    n, n2, m = solutions[0]
    profit = 0.5 * n + 0.2 * n2 - 0.25 * m - 1.0 * DISCARD
    print(f"問2: 定価{n}個, 2割引{n2}個, 廃棄{DISCARD}個, 半額{m}個（唯一解）")
    print(f"  合計個数={n+n2+DISCARD+m}個, 利益={profit}x = "
          f"仕入総額の{profit/TOTAL*100:.1f}%")
    return m


if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"\n問1の答え: {a1:,}円 / 問2の答え: {a2}個")
