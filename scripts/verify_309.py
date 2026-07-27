"""航大思考309 検証コード

問1: 損益分岐点グラフ（売上高・総費用の2直線）から目標利益となる販売個数を求める
問2: 利益グラフ（折れ線）から原価と値引き率を逆算する

すべて Fraction で厳密計算し、正解の一意性と各誤答の由来を確認する。
"""
from fractions import Fraction as F


# =====================================================================
# 問1: 売上高と総費用のグラフ
# =====================================================================
def verify_q1():
    # グラフから読み取る値
    PRICE = F(210000, 300)   # 売上高直線の傾き = 700円/個（定価）
    FIXED = F(30000)         # 総費用直線の切片 = 固定費 30,000円
    COST = (F(150000) - FIXED) / 300  # 総費用直線の傾き = 400円/個（1個あたり原価）

    assert PRICE == 700, PRICE
    assert COST == 400, COST

    TARGET = F(15000)        # 求める利益

    def profit(x):
        """x個売ったときの利益 = 売上高 - 総費用"""
        return PRICE * x - (FIXED + COST * x)

    # 総当たりで利益15,000円となる個数を探索
    answers = [x for x in range(0, 1001) if profit(x) == TARGET]
    assert len(answers) == 1, f"解が{len(answers)}個: {answers}"
    correct = answers[0]
    assert correct == 150, correct

    # 検算: 売上高105,000円 - 総費用90,000円 = 15,000円
    assert PRICE * correct == 105000
    assert FIXED + COST * correct == 90000

    # 損益分岐点（利益0）
    breakeven = [x for x in range(0, 1001) if profit(x) == 0]
    assert breakeven == [100], breakeven

    # ---- 各誤答が特定の誤解から整数として現れることを確認 ----
    traps = {}
    # (a) 固定費を無視した: 15,000 ÷ (700-400)
    traps["固定費を無視"] = TARGET / (PRICE - COST)
    # (b) 損益分岐点（利益0）の個数を答えた
    traps["損益分岐点と混同"] = FIXED / (PRICE - COST)
    # (c) 固定費を二重に引いた: 300x - 30,000 - 30,000 = 15,000
    traps["固定費の二重減算"] = (TARGET + 2 * FIXED) / (PRICE - COST)
    # (d) 総費用の傾きを平均費用150,000÷300=500円と誤読
    avg_cost = F(150000, 300)
    traps["平均費用と誤読"] = (TARGET + FIXED) / (PRICE - avg_cost)

    for name, v in traps.items():
        assert v.denominator == 1, f"{name} が整数でない: {v}"

    options = [50, 100, 225, 250, 150]  # (1)〜(5)
    assert options[4] == correct, "正解は(5)"
    assert len(set(options)) == 5, "選択肢に重複"
    for name, v in traps.items():
        assert int(v) in options, f"{name}={v} が選択肢にない"

    print("問1 OK: 正解 =", correct, "個  正解番号 = (5)")
    print("   単価700円 / 原価400円 / 固定費30,000円 / 損益分岐点100個")
    for name, v in traps.items():
        print(f"   罠 {name}: {int(v)}個")


# =====================================================================
# 問2: 利益グラフ（折れ線）から原価と値引き率を逆算
# =====================================================================
def verify_q2():
    # グラフから読み取る3点
    P0 = F(-20000)   # 0個のときの利益（= -固定費）
    P100 = F(10000)  # 100個のときの利益
    P200 = F(22000)  # 200個のときの利益

    FIXED = -P0
    assert FIXED == 20000

    slope1 = (P100 - P0) / 100    # 定価 - 原価
    slope2 = (P200 - P100) / 100  # 値引き後の売値 - 原価
    assert slope1 == 300, slope1
    assert slope2 == 120, slope2

    # 定価は原価の5割増し → 定価 - 原価 = 0.5 × 原価 = slope1
    cost = slope1 / F(1, 2)
    price = cost * F(3, 2)
    assert cost == 600 and price == 900, (cost, price)

    # 値引き後の売値と値引き率
    sale = cost + slope2
    assert sale == 720, sale
    rate = 1 - sale / price
    assert rate == F(1, 5), rate  # 2割引

    # ---- グラフの3点が矛盾なく再現されることを確認（順方向の検算） ----
    def profit(x):
        if x <= 100:
            return price * x - (FIXED + cost * x)
        return price * 100 + sale * (x - 100) - (FIXED + cost * x)

    assert profit(0) == P0 and profit(100) == P100 and profit(200) == P200

    # ---- 誤答の由来 ----
    # (1) 傾き300円をそのまま原価と誤認
    assert slope1 == 300
    # (3) 傾きの比を値引き率と誤認: 120 ÷ 300 = 0.4 → 4割引
    assert slope2 / slope1 == F(2, 5)
    # (4) 売値÷定価 = 0.8 を「8割引」と取り違え
    assert sale / price == F(4, 5)
    # (5) 定価900円を原価と取り違え
    assert price == 900

    options = [(300, "2割引"), (600, "2割引"), (600, "4割引"),
               (600, "8割引"), (900, "2割引")]
    assert len(set(options)) == 5, "選択肢に重複"
    assert options[1] == (600, "2割引"), "正解は(2)"

    print("問2 OK: 原価 =", cost, "円 / 定価 =", price,
          "円 / 値引き後 =", sale, "円 → 2割引  正解番号 = (2)")
    print("   固定費20,000円 / 傾き300円・120円 / 損益分岐点 =",
          [x for x in range(0, 501) if profit(x) == 0])


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\nすべての検証に成功しました。")
