# -*- coding: utf-8 -*-
"""航大思考192 検証スクリプト
問1: 5社ECサイト単一表（購入率・客単価・返品率）正しい記述を1つ選ぶ
問2: 6店舗カフェ2表クロスリファレンス（売上・原価・営業利益・利益率・1日あたり来客）
"""


def verify_q1():
    # 企業: (アクセス数(千件), 購入件数(件), 売上(千円), 返品件数(件))
    data = {
        "A": (200, 4000, 8000, 120),
        "B": (150, 3600, 7200, 72),
        "C": (250, 5000, 9000, 200),
        "D": (120, 3000, 6600, 60),
        "E": (180, 3600, 7920, 144),
    }
    cvr, price, ret = {}, {}, {}
    for k, (acc, buy, sales, r) in data.items():
        cvr[k] = buy / (acc * 1000) * 100          # 購入率(%)
        price[k] = sales * 1000 / buy              # 客単価(円)
        ret[k] = r / buy * 100                      # 返品率(%)
    print("Q1 購入率(%):", {k: round(v, 2) for k, v in cvr.items()})
    print("Q1 客単価(円):", price)
    print("Q1 返品率(%):", {k: round(v, 2) for k, v in ret.items()})

    def uniq_max(d):
        m = max(d.values())
        return [k for k, v in d.items() if abs(v - m) < 1e-9]

    def uniq_min(d):
        m = min(d.values())
        return [k for k, v in d.items() if abs(v - m) < 1e-9]

    # 各記述の真偽
    s = {}
    s["購入率最高=D"] = uniq_max(cvr) == ["D"]
    s["客単価最高=Dのみ"] = uniq_max(price) == ["D"]
    s["返品率最高=C"] = uniq_max(ret) == ["C"]
    s["客単価最低=B"] = uniq_min(price) == ["B"]
    s["返品率最低=A"] = uniq_min(ret) == ["A"]
    print("Q1 記述真偽:", s)
    trues = [k for k, v in s.items() if v]
    assert trues == ["購入率最高=D"], f"Q1 唯一の正は購入率最高=D のはず: {trues}"
    print("Q1 OK: 唯一の正しい記述 =", trues[0], "→ 正解(3)に配置\n")


def verify_q2():
    # 店舗: 表1(来客数(千人), 客単価(円), 営業日数(日)), 表2(総費用(千円), 原価率(%))
    t1 = {
        "A": (40, 800, 25), "B": (30, 1000, 30), "C": (50, 600, 25),
        "D": (25, 1200, 20), "E": (60, 500, 24), "F": (36, 900, 24),
    }
    t2 = {
        "A": (10000, 60), "B": (9000, 55), "C": (12000, 50),
        "D": (7500, 65), "E": (9600, 58), "F": (8000, 62),
    }
    sales, profit, margin, per_day = {}, {}, {}, {}
    for k in t1:
        guests, unit, days = t1[k]
        cost_fix, cost_rate = t2[k]
        sales[k] = guests * unit                         # 売上(千円)
        cogs = sales[k] * cost_rate / 100                # 原価(千円)
        profit[k] = sales[k] - cogs - cost_fix           # 営業利益(千円)
        margin[k] = profit[k] / sales[k] * 100           # 利益率(%)
        per_day[k] = guests * 1000 / days                # 1日あたり来客(人)
    print("Q2 売上(千円):", sales)
    print("Q2 営業利益(千円):", {k: round(v, 1) for k, v in profit.items()})
    print("Q2 利益率(%):", {k: round(v, 2) for k, v in margin.items()})
    print("Q2 1日あたり来客(人):", {k: round(v) for k, v in per_day.items()})

    def amax(d):
        m = max(d.values()); return [k for k, v in d.items() if abs(v - m) < 1e-6]

    def amin(d):
        m = min(d.values()); return [k for k, v in d.items() if abs(v - m) < 1e-6]

    a = amax(sales) == amax(profit)                     # ア
    i = amax(margin) == amin(per_day)                   # イ
    u = amin(profit) == amin(margin)                    # ウ
    e = amax(per_day) == amax(sales)                    # エ
    o = amax(profit) == amax(margin)                    # オ
    print("Q2 ア:", a, " イ:", i, " ウ:", u, " エ:", e, " オ:", o)
    correct = set(x for x, ok in [("ア", a), ("イ", i), ("ウ", u), ("エ", e), ("オ", o)] if ok)
    assert correct == {"イ", "ウ", "オ"}, f"Q2 正しい記述は イ・ウ・オ のはず: {correct}"
    # HTMLに記載する最終的な選択肢（全て相異・(5)のみ一致）
    options = {1: {"ア", "イ"}, 2: {"ア", "エ"}, 3: {"イ", "ウ"},
               4: {"ウ", "エ", "オ"}, 5: {"イ", "ウ", "オ"}}
    assert len({frozenset(v) for v in options.values()}) == 5, "選択肢に重複あり"
    match = [n for n, st in options.items() if st == correct]
    assert match == [5], f"唯一一致する選択肢は(5)のはず: {match}"
    print("Q2 OK: 正しい記述 イ・ウ・オ → 選択肢(5)\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("=== 全検証パス ===")
