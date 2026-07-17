from fractions import Fraction as F

def verify_q1():
    """問1: 原価xに3割の利益で定価、定価の2割引で売り利益120円 -> 原価は?"""
    solutions = []
    for x in range(1, 20001):  # 原価を1円単位で総当たり
        teika = F(x) * F(13, 10)
        baika = teika * F(8, 10)
        profit = baika - x
        if profit == 120:
            solutions.append(x)
    assert len(solutions) == 1, f"解が{len(solutions)}個: {solutions}"
    x = solutions[0]
    print("問1 原価 =", x)
    print("  定価 =", F(x)*F(13,10), " 売価 =", F(x)*F(13,10)*F(8,10), " 利益 =", F(x)*F(13,10)*F(8,10)-x)
    # 罠の検算
    print("  罠: 3割-2割=1割 ->", 120*10)          # 1200
    print("  罠: 0.05x=120 ->", 120*20)             # 2400
    print("  罠: 0.03x=120 ->", 120*100//3)         # 4000
    print("  罠: 0.02x=120 ->", 120*50)             # 6000
    return x

def verify_q2():
    """問2: 240個仕入れ、原価の2割5分増しの定価。n個定価で売れ、
    残りは定価の2割引で完売。総利益=仕入総額の15% -> nは?"""
    solutions = []
    for n in range(0, 241):  # 定価で売れた個数を総当たり(原価xは任意で消える)
        # 原価を x=1 として比率計算(xは両辺に共通なので一意性に影響しない)
        teika = F(5, 4)          # 1.25x
        waribiki = teika * F(4, 5)  # 1.00x = 原価と同額
        profit = n * (teika - 1) + (240 - n) * (waribiki - 1)
        if profit == F(15, 100) * 240:
            solutions.append(n)
    assert len(solutions) == 1, f"解が{len(solutions)}個: {solutions}"
    n = solutions[0]
    print("問2 定価で売れた個数 =", n, " 売れ残り =", 240-n)
    # 原価が任意の値でも成立することを確認(比率問題であることの検証)
    for x in [100, 800, 1234]:
        t = F(x)*F(5,4); w = t*F(4,5)
        p = n*(t-x) + (240-n)*(w-x)
        assert p == F(15,100)*240*x, x
    print("  任意原価で成立を確認")
    # 罠の検算
    # 罠A: 割引分も0.05xの利益と誤る 0.25n+0.05(240-n)=36 -> n
    nA = (F(36) - F(5,100)*240) / F(20,100)
    print("  罠A(割引分に5%利益):", nA)             # 120
    # 罠B: 売れ残り個数と取り違え -> 96
    # 罠C: 利益率を定価売上に対して取る 0.25n = 0.15*1.25*240 -> n
    nC = F(15,100)*F(5,4)*240 / F(25,100)
    print("  罠C(定価売上基準の15%):", nC)          # 180
    return n

q1 = verify_q1()
q2 = verify_q2()
print("OK: 問1 =", q1, "円 / 問2 =", q2, "個")
