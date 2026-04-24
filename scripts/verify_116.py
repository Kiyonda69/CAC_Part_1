"""
verify_116.py - 航大思考116 の解の一意性検証

問1: 5つの市立図書館の月次運営報告書（長文読解）
  5つの記述のうち、資料の内容と数値的に整合するものを1つ選ぶ

問2: 食品工場の月次品質管理報告書（長文読解 + 複数条件判定）
  4条件すべてを満たす「優良品」の組合せを特定する
"""


def verify_q1():
    """問1: 図書館運営報告書の記述判定（唯一解の確認）"""
    libraries = {
        "中央館": {"open_days": 28, "visitors": 14000, "loans": 21000},
        "北支館": {"open_days": 25, "visitors": 4500, "loans": 8500},
        "南支館": {"open_days": 24, "visitors": 6000, "loans": 7200},
        "東支館": {"open_days": 26, "visitors": 5200, "loans": 10400},
        "西支館": {"open_days": 27, "visitors": 8100, "loans": 13500},
    }

    # 派生量
    per_day_visitors = {k: v["visitors"] / v["open_days"] for k, v in libraries.items()}
    per_day_loans = {k: v["loans"] / v["open_days"] for k, v in libraries.items()}
    per_visitor_loans = {k: v["loans"] / v["visitors"] for k, v in libraries.items()}
    total_loans = sum(v["loans"] for v in libraries.values())

    print("==== 問1 基礎データ ====")
    for k, v in libraries.items():
        print(f"  {k}: 開館{v['open_days']}日, 来館{v['visitors']}人, 貸出{v['loans']}冊")
        print(f"     1日あたり来館 {per_day_visitors[k]:.2f}人, 1日あたり貸出 {per_day_loans[k]:.2f}冊, 1人あたり貸出 {per_visitor_loans[k]:.3f}冊")
    print(f"  合計貸出: {total_loans}冊（半分={total_loans/2}冊）")

    # 各記述の判定
    statements = []

    # 記述ア: 1日あたり平均来館者数が最も多いのは西支館
    max_visitors_per_day = max(per_day_visitors, key=per_day_visitors.get)
    statements.append(("ア", max_visitors_per_day == "西支館",
                       f"1日あたり来館最多 = {max_visitors_per_day}（{per_day_visitors[max_visitors_per_day]:.1f}人）"))

    # 記述イ: 貸出冊数が最も多いのは中央館であり、5館合計の半分以上を占める
    max_loans_lib = max(libraries, key=lambda k: libraries[k]["loans"])
    central_loans = libraries["中央館"]["loans"]
    statements.append(("イ", max_loans_lib == "中央館" and central_loans >= total_loans / 2,
                       f"最多貸出 = {max_loans_lib}（{libraries[max_loans_lib]['loans']}冊）、中央館占有率={central_loans/total_loans*100:.1f}%"))

    # 記述ウ: 来館者1人あたり貸出冊数が最大の図書館は東支館で、ちょうど2.0冊である
    max_per_visitor_lib = max(per_visitor_loans, key=per_visitor_loans.get)
    east_ratio = per_visitor_loans["東支館"]
    statements.append(("ウ", max_per_visitor_lib == "東支館" and abs(east_ratio - 2.0) < 1e-9,
                       f"1人あたり貸出最大 = {max_per_visitor_lib}（{per_visitor_loans[max_per_visitor_lib]:.3f}冊）、東支館={east_ratio:.3f}"))

    # 記述エ: 1日あたり平均貸出冊数が最も少ないのは北支館
    min_loans_per_day = min(per_day_loans, key=per_day_loans.get)
    statements.append(("エ", min_loans_per_day == "北支館",
                       f"1日あたり貸出最少 = {min_loans_per_day}（{per_day_loans[min_loans_per_day]:.1f}冊）"))

    # 記述オ: 開館日数が最も多いのは西支館で27日間開館した
    max_days_lib = max(libraries, key=lambda k: libraries[k]["open_days"])
    statements.append(("オ", max_days_lib == "西支館" and libraries["西支館"]["open_days"] == 27,
                       f"開館日数最多 = {max_days_lib}（{libraries[max_days_lib]['open_days']}日）"))

    print("\n==== 問1 記述判定 ====")
    correct_statements = []
    for label, result, detail in statements:
        mark = "○" if result else "×"
        print(f"  ({label}) {mark}  {detail}")
        if result:
            correct_statements.append(label)

    print(f"\n正しい記述: {correct_statements}")
    assert len(correct_statements) == 1, f"正しい記述が{len(correct_statements)}個（一意でない）"
    print("✓ 問1: 正しい記述は唯一（ウ）")


def verify_q2():
    """問2: 食品工場 出荷基準 4条件を全て満たす製品の組合せ"""
    products = {
        "P1": {"produced": 12000, "defective": 100, "returned": 40, "lead_time": 2.5},
        "P2": {"produced": 15000, "defective": 120, "returned": 50, "lead_time": 3.2},
        "P3": {"produced": 8000, "defective": 40, "returned": 20, "lead_time": 2.0},
        "P4": {"produced": 11000, "defective": 110, "returned": 30, "lead_time": 2.8},
        "P5": {"produced": 14000, "defective": 140, "returned": 80, "lead_time": 2.7},
    }

    # 出荷基準
    # ① 月間生産数 ≧ 10,000 個
    # ② 不良品率 ≦ 1.0%
    # ③ 返品率 ≦ 0.5%
    # ④ 平均リードタイム ≦ 3.0 日

    print("\n==== 問2 基礎データ ====")
    for k, v in products.items():
        defect_rate = v["defective"] / v["produced"] * 100
        return_rate = v["returned"] / v["produced"] * 100
        print(f"  {k}: 生産{v['produced']}個, 不良{v['defective']}個（{defect_rate:.3f}%）, 返品{v['returned']}個（{return_rate:.3f}%）, リード{v['lead_time']}日")

    excellent = []
    reasons = {}
    for k, v in products.items():
        cond1 = v["produced"] >= 10000
        defect_rate = v["defective"] / v["produced"]
        cond2 = defect_rate <= 0.01 + 1e-9
        return_rate = v["returned"] / v["produced"]
        cond3 = return_rate <= 0.005 + 1e-9
        cond4 = v["lead_time"] <= 3.0 + 1e-9
        if cond1 and cond2 and cond3 and cond4:
            excellent.append(k)
            reasons[k] = "全条件充足"
        else:
            failed = []
            if not cond1: failed.append(f"①生産数{v['produced']}<10000")
            if not cond2: failed.append(f"②不良率{defect_rate*100:.3f}%>1.0%")
            if not cond3: failed.append(f"③返品率{return_rate*100:.3f}%>0.5%")
            if not cond4: failed.append(f"④リード{v['lead_time']}>3.0")
            reasons[k] = "不適（" + ", ".join(failed) + "）"

    print("\n==== 問2 製品別判定 ====")
    for k in products:
        mark = "◎優良品" if k in excellent else "×"
        print(f"  {k}: {mark}  {reasons[k]}")

    print(f"\n優良品の組合せ: {sorted(excellent)}")

    # 選択肢
    options = {
        1: ["P1", "P2"],
        2: ["P1", "P4"],
        3: ["P2", "P4"],
        4: ["P1", "P3", "P5"],
        5: ["P2", "P4", "P5"],
    }
    correct = None
    for n, combo in options.items():
        if sorted(combo) == sorted(excellent):
            correct = n
    assert correct is not None, "いずれの選択肢も正解と一致しない"
    assert correct == 2, f"期待した正解番号(2)と異なる: {correct}"
    print(f"✓ 問2: 正解は選択肢({correct}) — {options[correct]}")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n===== すべての検証を通過 =====")
