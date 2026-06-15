# -*- coding: utf-8 -*-
"""航大思考229 解の一意性検証
問1: 四半期グループ棒グラフ（国内線/国際線旅客数）→ 国際線比率が最大の四半期
問2: 複合グラフ（棒=就航便数, 折れ線=搭乗率）+表(座席数) → 旅客数最大の月
"""

def verify_q1():
    # (国内線, 国際線)[万人]  Q1..Q4
    data = {
        "Q1": (100, 25),
        "Q2": (120, 48),
        "Q3": (160, 56),
        "Q4": (200, 60),
    }
    ratios = {q: kok / (kok + kn) for q, (kn, kok) in
              ((q, (d[0], d[1])) for q, d in data.items())}
    # 比率 = 国際 / (国内+国際)
    ratios = {q: kok / (kn + kok) for q, (kn, kok) in data.items()}
    best = max(ratios, key=ratios.get)
    # 一意性: 最大値を取る四半期が1つだけか
    mx = max(ratios.values())
    winners = [q for q, r in ratios.items() if abs(r - mx) < 1e-9]
    print("問1 比率:", {q: round(r, 4) for q, r in ratios.items()})
    print("問1 国際線絶対値最大:", max(data, key=lambda q: data[q][1]))
    assert len(winners) == 1, f"解が一意でない: {winners}"
    assert best == "Q2", f"想定位置(2=Q2)と不一致: {best}"
    print("問1 正解:", best, "(option 2)\n")

def verify_q2():
    # 便数, 座席数, 搭乗率(%)  4月..8月
    data = {
        "4月": (260, 210, 80),
        "5月": (320, 170, 78),
        "6月": (300, 180, 76),
        "7月": (220, 220, 85),
        "8月": (280, 190, 79),
    }
    pax = {m: bin_ * seat * rate / 100 for m, (bin_, seat, rate) in data.items()}
    mx = max(pax.values())
    winners = [m for m, p in pax.items() if abs(p - mx) < 1e-9]
    print("問2 旅客数:", {m: int(p) for m, p in pax.items()})
    print("問2 便数最大:", max(data, key=lambda m: data[m][0]))
    print("問2 座席最大:", max(data, key=lambda m: data[m][1]))
    print("問2 搭乗率最大:", max(data, key=lambda m: data[m][2]))
    assert len(winners) == 1, f"解が一意でない: {winners}"
    best = winners[0]
    assert best == "4月", f"想定位置(1=4月)と不一致: {best}"
    print("問2 正解:", best, "(option 1)")

verify_q1()
verify_q2()
print("\n=== 全検証パス ===")
