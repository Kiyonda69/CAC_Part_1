"""航大思考306 損益算（文章題のみ）の検証

問1: 1個200円で300個仕入れ、200個を1個280円で販売。残り100個を値下げして
      売り切ったところ全体の利益が仕入総額の2割。値下げ後の1個の値段は？
問2: 500個仕入れ、原価の5割増しの定価。300個は定価、150個は定価の□割引、
      50個は売れ残り廃棄。全体の利益は仕入総額の26%（13,000円）。値引き率は？
"""
from fractions import Fraction as F


def verify_q1():
    """問1: 値下げ後の売価を1円刻みで総当たり"""
    COST = 200           # 1個の原価
    TOTAL = 300          # 仕入個数
    AT_LIST = 200        # 280円で売れた個数
    LIST_PRICE = 280     # 値下げ前の売価
    REST = TOTAL - AT_LIST
    PROFIT_RATE = F(2, 10)   # 全体の利益は仕入総額の2割

    buy_total = COST * TOTAL
    target_profit = buy_total * PROFIT_RATE

    solutions = []
    for price in range(0, 1001):   # 0〜1,000円を総当たり
        sales = AT_LIST * LIST_PRICE + REST * price
        if sales - buy_total == target_profit:
            solutions.append(price)
    assert len(solutions) == 1, f"解が{len(solutions)}個存在"
    ans = solutions[0]

    options = [120, 160, 190, 200, 240]
    hits = [p for p in options
            if AT_LIST * LIST_PRICE + REST * p - buy_total == target_profit]
    assert hits == [ans], f"選択肢中の該当が一意でない: {hits}"

    print("=== 問1 ===")
    print(f"仕入総額     : {buy_total}円 / 目標利益: {int(target_profit)}円")
    print(f"売上総額     : {int(buy_total + target_profit)}円")
    print(f"280円販売分  : {AT_LIST * LIST_PRICE}円")
    print(f"値下げ販売分 : {int(buy_total + target_profit - AT_LIST * LIST_PRICE)}円"
          f" ÷ {REST}個 = {ans}円")
    print("-- 各選択肢での全体の利益（仕入総額60,000円に対する割合）--")
    for p in options:
        profit = AT_LIST * LIST_PRICE + REST * p - buy_total
        print(f"  {p:>4}円 -> 利益 {profit:>6}円 ({F(profit, buy_total) * 100}%)")
    print("-- 罠の由来 --")
    print("  120円: 値下げ額(280-160)との取り違え")
    print("  190円: 利益率の基準を売上と誤る 60,000÷0.8=75,000 → 19,000÷100")
    print("  200円: 値下げしても原価は割らないと決めつける")
    print("  240円: 値下げ後も原価の2割の利益があると誤解 200×1.2")
    return ans


def verify_q2():
    """問2: 値引き率を総当たり（1分＝0.05刻み）で特定"""
    TOTAL = 500          # 仕入個数
    AT_LIST = 300        # 定価で売れた個数
    AT_SALE = 150        # 値引きして売れた個数
    DISCARD = 50         # 廃棄した個数
    MARKUP = F(5, 10)    # 原価の5割の利益を見込んだ定価
    PROFIT_RATE = F(26, 100)   # 仕入総額に対する利益率
    PROFIT = 13000       # 利益額
    assert AT_LIST + AT_SALE + DISCARD == TOTAL

    # 仕入総額 = 500c、利益 = 0.26 × 500c = 13,000 より原価が定まる
    cost = PROFIT / (PROFIT_RATE * TOTAL)
    assert cost == 100, cost
    cost = int(cost)
    price = int(cost * (1 + MARKUP))

    solutions = []
    x = F(0)
    while x <= 1:
        sales = AT_LIST * price + AT_SALE * price * (1 - x)
        if sales - TOTAL * cost == PROFIT:
            solutions.append(x)
        x += F(1, 100)   # 1分刻みで総当たり
    assert len(solutions) == 1, f"解が{len(solutions)}個存在"
    ans = solutions[0]

    options = [F(10, 100), F(15, 100), F(20, 100), F(25, 100), F(40, 100)]
    hits = [o for o in options
            if AT_LIST * price + AT_SALE * price * (1 - o) - TOTAL * cost == PROFIT]
    assert hits == [ans], f"選択肢中の該当が一意でない: {hits}"

    print("\n=== 問2 ===")
    print(f"原価         : {cost}円 / 定価: {price}円")
    print(f"値引き率     : {ans} （{int(ans * 100)}%＝{int(ans * 10)}割引）")
    print(f"値引き後売価 : {int(price * (1 - ans))}円")
    print("-- 各選択肢の全体利益（正しく廃棄50個を数えた場合）--")
    for o in options:
        s = AT_LIST * price + AT_SALE * price * (1 - o)
        print(f"  {o*100}%引き(売価{float(price*(1-o)):>6}円) -> 利益 {int(s - TOTAL*cost):>6}円")
    print("-- 最重要罠: 廃棄50個も値引きで売れたと誤ると --")
    for o in options:
        s = AT_LIST * price + (AT_SALE + DISCARD) * price * (1 - o)
        if s - TOTAL * cost == PROFIT:
            print(f"  {int(o*10)}割引 が条件を満たしてしまう（誤答）")
    return ans


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n両問とも解の一意性を確認しました。")
