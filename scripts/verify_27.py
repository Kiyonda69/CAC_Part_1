"""
航大思考27 - 資料読み取り問題の検証スクリプト

問1: 3社（A社・B社・C社）の売上高と営業利益率の推移
問2: 3社（P社・Q社・R社）の売上高と売上総利益率の推移
"""


def verify_q1():
    """問1 の選択肢検証（正解 = (2)）"""
    print("=" * 50)
    print("問1 検証")
    print("=" * 50)

    # 売上高データ（億円）
    sales = {
        "A": {2020: 180, 2021: 190, 2022: 200, 2023: 195, 2024: 220},
        "B": {2020: 120, 2021: 130, 2022: 125, 2023: 140, 2024: 150},
        "C": {2020: 80,  2021: 90,  2022: 95,  2023: 100, 2024: 110},
    }

    # 営業利益率データ（%）
    op_rate = {
        "A": {2020: 8,  2021: 9,  2022: 10, 2023: 8,  2024: 11},
        "B": {2020: 10, 2021: 9,  2022: 8,  2023: 10, 2024: 11},
        "C": {2020: 6,  2021: 7,  2022: 8,  2023: 6,  2024: 10},
    }

    years = [2020, 2021, 2022, 2023, 2024]

    # 営業利益（億円）= 売上高 × 営業利益率 / 100
    op_profit = {}
    for co in ["A", "B", "C"]:
        op_profit[co] = {y: sales[co][y] * op_rate[co][y] / 100 for y in years}

    print("\n【営業利益（億円）】")
    for co in ["A", "B", "C"]:
        vals = [f"{op_profit[co][y]:.1f}" for y in years]
        print(f"  {co}社: {dict(zip(years, vals))}")

    print("\n【選択肢の検証】")

    # (1) A社の売上高は常にB社+C社の合計を上回っているか
    result1 = all(sales["A"][y] > sales["B"][y] + sales["C"][y] for y in years)
    for y in years:
        bc = sales["B"][y] + sales["C"][y]
        print(f"  (1) {y}: A社={sales['A'][y]} vs B+C={bc} → A>B+C: {sales['A'][y] > bc}")
    print(f"  => 選択肢(1) 全年でA>B+C: {result1} → {'正解' if result1 else '不正解（FALSEなので誤りの選択肢）'}")

    print()
    # (2) B社の売上高が前年より減少した年は2022年の1年だけか
    b_sales = [sales["B"][y] for y in years]
    decreases = [years[i] for i in range(1, len(years)) if b_sales[i] < b_sales[i-1]]
    print(f"  (2) B社売上高: {dict(zip(years, b_sales))}")
    print(f"  (2) 減少した年: {decreases}")
    result2 = (decreases == [2022])
    print(f"  => 選択肢(2) 減少が2022年1回のみ: {result2} → {'正解' if result2 else '不正解'}")

    print()
    # (3) 2024年の3社の売上高合計が500億円を超えるか
    total_2024 = sum(sales[co][2024] for co in ["A", "B", "C"])
    result3 = total_2024 > 500
    print(f"  (3) 2024年3社合計: {total_2024}億円 > 500億円: {result3}")
    print(f"  => 選択肢(3): {result3} → {'正解' if result3 else '不正解（FALSEなので誤りの選択肢）'}")

    print()
    # (4) 2022年に営業利益率が最も高いのはC社か
    rates_2022 = {co: op_rate[co][2022] for co in ["A", "B", "C"]}
    max_co = max(rates_2022, key=rates_2022.get)
    result4 = (max_co == "C")
    print(f"  (4) 2022年営業利益率: A={rates_2022['A']}%, B={rates_2022['B']}%, C={rates_2022['C']}%")
    print(f"  (4) 最高はC社か: {result4} (実際: {max_co}社)")
    print(f"  => 選択肢(4): {result4} → {'正解' if result4 else '不正解（FALSEなので誤りの選択肢）'}")

    print()
    # (5) C社の営業利益が調査期間を通じて毎年増加したか
    c_profits = [op_profit["C"][y] for y in years]
    c_all_increase = all(c_profits[i] > c_profits[i-1] for i in range(1, len(c_profits)))
    print(f"  (5) C社営業利益: {[round(v, 2) for v in c_profits]}")
    print(f"  (5) 毎年増加: {c_all_increase}")
    print(f"  => 選択肢(5): {c_all_increase} → {'正解' if c_all_increase else '不正解（FALSEなので誤りの選択肢）'}")

    # 正解確認
    print("\n【正解確認】")
    results = [result1, result2, result3, result4, c_all_increase]
    true_options = [i+1 for i, r in enumerate(results) if r]
    print(f"  TRUEの選択肢: {true_options}")
    assert true_options == [2], f"唯一の正解が(2)であるべきだが: {true_options}"
    print("  ✓ 唯一の正解: (2) 確認完了")


def verify_q2():
    """問2 の選択肢検証（正解 = (4)）"""
    print("\n" + "=" * 50)
    print("問2 検証")
    print("=" * 50)

    # 売上高データ（百万円）
    sales = {
        "P": {2020: 500, 2021: 520, 2022: 550, 2023: 530, 2024: 580},
        "Q": {2020: 350, 2021: 360, 2022: 340, 2023: 380, 2024: 400},
        "R": {2020: 200, 2021: 220, 2022: 240, 2023: 250, 2024: 260},
    }

    # 売上総利益率データ（%）
    gp_rate = {
        "P": {2020: 30, 2021: 32, 2022: 35, 2023: 26, 2024: 33},
        "Q": {2020: 25, 2021: 24, 2022: 22, 2023: 24, 2024: 30},
        "R": {2020: 20, 2021: 22, 2022: 24, 2023: 20, 2024: 25},
    }

    years = [2020, 2021, 2022, 2023, 2024]

    # 売上総利益（百万円）= 売上高 × 売上総利益率 / 100
    gp = {}
    for co in ["P", "Q", "R"]:
        gp[co] = {y: sales[co][y] * gp_rate[co][y] / 100 for y in years}

    print("\n【売上総利益（百万円）】")
    for co in ["P", "Q", "R"]:
        vals = [f"{gp[co][y]:.1f}" for y in years]
        print(f"  {co}社: {dict(zip(years, vals))}")

    print("\n【選択肢の検証】")

    # (1) 2022年、Q社の売上高が前年より減少したが売上総利益率は前年より上昇したか
    q_sales_dec = sales["Q"][2022] < sales["Q"][2021]
    q_rate_inc = gp_rate["Q"][2022] > gp_rate["Q"][2021]
    result1 = q_sales_dec and q_rate_inc
    print(f"  (1) Q社2022: 売上高減少={q_sales_dec}({sales['Q'][2021]}→{sales['Q'][2022]}), 利益率上昇={q_rate_inc}({gp_rate['Q'][2021]}%→{gp_rate['Q'][2022]}%)")
    print(f"  => 選択肢(1): {result1} → {'正解' if result1 else '不正解（FALSEなので誤りの選択肢）'}")

    print()
    # (2) P社の売上高が前年より減少した年は存在しないか
    p_sales = [sales["P"][y] for y in years]
    p_decreases = [years[i] for i in range(1, len(years)) if p_sales[i] < p_sales[i-1]]
    result2 = (len(p_decreases) == 0)
    print(f"  (2) P社売上高: {dict(zip(years, p_sales))}")
    print(f"  (2) 減少した年: {p_decreases}")
    print(f"  => 選択肢(2): {result2} → {'正解' if result2 else '不正解（FALSEなので誤りの選択肢）'}")

    print()
    # (3) 2024年の3社合計の売上総利益が400百万円を超えるか
    total_gp_2024 = sum(gp[co][2024] for co in ["P", "Q", "R"])
    result3 = total_gp_2024 > 400
    print(f"  (3) 2024年3社合計売上総利益: {total_gp_2024:.1f}百万円 > 400: {result3}")
    for co in ["P", "Q", "R"]:
        print(f"      {co}社: {sales[co][2024]}×{gp_rate[co][2024]}% = {gp[co][2024]:.1f}百万円")
    print(f"  => 選択肢(3): {result3} → {'正解' if result3 else '不正解（FALSEなので誤りの選択肢）'}")

    print()
    # (4) R社の売上高が調査期間を通じて毎年増加したか
    r_sales = [sales["R"][y] for y in years]
    result4 = all(r_sales[i] > r_sales[i-1] for i in range(1, len(r_sales)))
    print(f"  (4) R社売上高: {dict(zip(years, r_sales))}")
    print(f"  (4) 毎年増加: {result4}")
    print(f"  => 選択肢(4): {result4} → {'正解' if result4 else '不正解'}")

    print()
    # (5) 2023年の3社の売上総利益率の平均が2020年の平均より高いか
    avg_2020 = sum(gp_rate[co][2020] for co in ["P", "Q", "R"]) / 3
    avg_2023 = sum(gp_rate[co][2023] for co in ["P", "Q", "R"]) / 3
    result5 = avg_2023 > avg_2020
    print(f"  (5) 2020年平均: ({gp_rate['P'][2020]}+{gp_rate['Q'][2020]}+{gp_rate['R'][2020]})/3 = {avg_2020:.2f}%")
    print(f"  (5) 2023年平均: ({gp_rate['P'][2023]}+{gp_rate['Q'][2023]}+{gp_rate['R'][2023]})/3 = {avg_2023:.2f}%")
    print(f"  (5) 2023年 > 2020年: {result5}")
    print(f"  => 選択肢(5): {result5} → {'正解' if result5 else '不正解（FALSEなので誤りの選択肢）'}")

    # 正解確認
    print("\n【正解確認】")
    results = [result1, result2, result3, result4, result5]
    true_options = [i+1 for i, r in enumerate(results) if r]
    print(f"  TRUEの選択肢: {true_options}")
    assert true_options == [4], f"唯一の正解が(4)であるべきだが: {true_options}"
    print("  ✓ 唯一の正解: (4) 確認完了")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 50)
    print("✓ 全検証完了：問1の正解=(2)、問2の正解=(4)")
    print("=" * 50)
