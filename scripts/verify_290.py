#!/usr/bin/env python3
"""航大思考290 検証スクリプト（損益算・文章のみ）

問1: ある商品に原価の何割かの利益を見込んで定価をつけた。
     定価の1割引で売ると560円の利益があり、
     定価の2割5分引で売ると280円の損失が出る。原価はいくらか。

問2: ある商品を300個仕入れ、原価の5割の利益を見込んで定価をつけた。
     何個かを定価で売り、その後、定価の2割引にして定価で売れた個数の
     ちょうど半分の個数を売り、残りは定価の半額で売り切った。
     全体の利益は仕入総額のちょうど27%であった。
     定価の半額で売った個数は何個か。
"""


def verify_q1():
    """問1: 総当たりで原価・定価の組を探索"""
    solutions = []
    # 原価・定価を10円単位で総当たり
    for cost in range(100, 20001, 10):
        for price in range(cost, 30001, 10):
            # 定価の1割引で560円の利益
            if price * 0.9 - cost != 560:
                continue
            # 定価の2割5分引で280円の損失
            if price * 0.75 - cost != -280:
                continue
            solutions.append((cost, price))
    assert len(solutions) == 1, f"問1: 解が{len(solutions)}個存在: {solutions}"
    cost, price = solutions[0]
    # 検算
    assert price * 0.9 - cost == 560
    assert cost - price * 0.75 == 280
    print(f"問1 唯一解: 原価={cost}円, 定価={price}円")
    print(f"  検算: 1割引 {price*0.9:.0f}円 → 利益 {price*0.9-cost:.0f}円")
    print(f"  検算: 2割5分引 {price*0.75:.0f}円 → 損失 {cost-price*0.75:.0f}円")
    return cost


def verify_q2():
    """問2: 定価で売れた個数xを総当たり"""
    total = 300
    solutions = []
    # 原価を1とおく（利益率の条件なので原価の値に依存しない）
    # 定価1.5, 2割引1.2, 半額0.75
    for x in range(0, total + 1):  # 定価で売れた個数
        if x % 2 != 0:
            continue  # 2割引の個数 x/2 が整数
        disc = x // 2
        half = total - x - disc
        if half < 0:
            continue
        # 「その後2割引で売り」「残りは半額で売り切った」→ 各段階1個以上
        if x == 0 or disc == 0 or half == 0:
            continue
        revenue = 1.5 * x + 1.2 * disc + 0.75 * half
        profit = revenue - total
        # 利益は仕入総額の27%
        if abs(profit - 0.27 * total) < 1e-9:
            solutions.append((x, disc, half))
    assert len(solutions) == 1, f"問2: 解が{len(solutions)}個存在: {solutions}"
    x, disc, half = solutions[0]
    print(f"問2 唯一解: 定価={x}個, 2割引={disc}個, 半額={half}個")
    revenue = 1.5 * x + 1.2 * disc + 0.75 * half
    print(f"  検算: 売上={revenue}（原価1あたり）, 利益={revenue-300}, "
          f"利益率={(revenue-300)/300*100:.1f}%")
    return half


if __name__ == "__main__":
    q1 = verify_q1()
    q2 = verify_q2()
    print(f"\n問1の答え: {q1}円 / 問2の答え: {q2}個")
