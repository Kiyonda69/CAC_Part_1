#!/usr/bin/env python3
"""
セット78 検証スクリプト
問1: 散布図の資料読み取り（国内出荷量と輸出量の合計が前回比で減少した年）
問2: 割合表の資料読み取り（職種別人数の連立方程式＋個別計算の差）
"""


def verify_q1():
    """問1: 散布図 - 合計が前回比で減少した年を特定"""
    print("=" * 60)
    print("問1: 散布図の読み取り検証")
    print("=" * 60)

    # データ: (年, 国内出荷量(万トン), 輸出量(万トン))
    data = [
        (1995, 2200, 600),
        (2000, 2800, 900),
        (2005, 3500, 1400),
        (2010, 3800, 1800),
        (2015, 3200, 2300),
        (2020, 3600, 2800),
    ]

    print("\n各年の合計:")
    totals = []
    for year, domestic, export in data:
        total = domestic + export
        totals.append((year, total))
        print(f"  {year}年: 国内{domestic} + 輸出{export} = 合計{total}万トン")

    print("\n前回比の変化:")
    decreased_years = []
    for i in range(1, len(totals)):
        prev_year, prev_total = totals[i - 1]
        curr_year, curr_total = totals[i]
        diff = curr_total - prev_total
        status = "増加" if diff > 0 else "減少"
        print(f"  {curr_year}年: {curr_total} - {prev_total} = {diff:+d} ({status})")
        if diff < 0:
            decreased_years.append(curr_year)

    assert len(decreased_years) == 1, f"減少した年が{len(decreased_years)}個: {decreased_years}"
    assert decreased_years[0] == 2015, f"減少した年が{decreased_years[0]}年（期待: 2015年）"

    # 選択肢: (1)2000年 (2)2005年 (3)2010年 (4)2015年 (5)2020年
    correct_option = 4  # 2015年
    choices = {1: 2000, 2: 2005, 3: 2010, 4: 2015, 5: 2020}
    assert choices[correct_option] == 2015

    print(f"\n正解: ({correct_option}) {decreased_years[0]}年")
    print("検証OK: 解は唯一")
    return correct_option


def verify_q2():
    """問2: 割合表 - 連立方程式で職種別人数を求め、差を計算"""
    print("\n" + "=" * 60)
    print("問2: 割合表の読み取り検証")
    print("=" * 60)

    total_employees = 3000

    # 表データ（%）
    # 勤務地: 東京, 大阪, 名古屋, 福岡, 札幌
    sales_pct = {"東京": 40.0, "大阪": 25.0, "名古屋": 10.0, "福岡": 15.0, "札幌": 10.0}
    tech_pct = {"東京": 30.0, "大阪": 20.0, "名古屋": 20.0, "福岡": 20.0, "札幌": 10.0}
    total_pct = {"東京": 34.0, "大阪": 22.0, "名古屋": 16.0, "福岡": 18.0, "札幌": 10.0}

    # 各行の合計が100%であることを確認
    assert sum(sales_pct.values()) == 100.0, f"営業の合計: {sum(sales_pct.values())}"
    assert sum(tech_pct.values()) == 100.0, f"技術の合計: {sum(tech_pct.values())}"
    assert sum(total_pct.values()) == 100.0, f"全体の合計: {sum(total_pct.values())}"

    # 連立方程式で営業(S)と技術(T)の人数を求める
    # S + T = 3000
    # 東京について: 0.40*S + 0.30*T = 0.34*3000 = 1020
    # 0.40*S + 0.30*(3000-S) = 1020
    # 0.10*S = 120
    # S = 1200

    tokyo_total = total_pct["東京"] / 100 * total_employees
    # 0.40*S + 0.30*(3000-S) = tokyo_total
    # (0.40-0.30)*S + 0.30*3000 = tokyo_total
    coeff_diff = (sales_pct["東京"] - tech_pct["東京"]) / 100
    S = (tokyo_total - tech_pct["東京"] / 100 * total_employees) / coeff_diff
    T = total_employees - S

    print(f"\n営業職の人数: {S:.0f}人")
    print(f"技術職の人数: {T:.0f}人")

    assert abs(S - 1200) < 0.01, f"営業が{S}人（期待: 1200人）"
    assert abs(T - 1800) < 0.01, f"技術が{T}人（期待: 1800人）"
    S = round(S)
    T = round(T)

    # 全勤務地について整合性を確認
    print("\n各勤務地の整合性確認:")
    for city in sales_pct:
        calculated = sales_pct[city] / 100 * S + tech_pct[city] / 100 * T
        expected = total_pct[city] / 100 * total_employees
        print(f"  {city}: 営業{sales_pct[city]}%×{S:.0f} + 技術{tech_pct[city]}%×{T:.0f} = {calculated:.0f} (期待: {expected:.0f})")
        assert abs(calculated - expected) < 0.01, f"{city}で不整合: {calculated} != {expected}"

    # 問題: 技術職のうち名古屋勤務の人数と営業職のうち福岡勤務の人数の差は何人か
    tech_nagoya = tech_pct["名古屋"] / 100 * T
    sales_fukuoka = sales_pct["福岡"] / 100 * S

    print(f"\n技術職・名古屋勤務: {tech_pct['名古屋']}% × {T:.0f} = {tech_nagoya:.0f}人")
    print(f"営業職・福岡勤務: {sales_pct['福岡']}% × {S:.0f} = {sales_fukuoka:.0f}人")

    difference = tech_nagoya - sales_fukuoka
    print(f"差: {tech_nagoya:.0f} - {sales_fukuoka:.0f} = {difference:.0f}人")

    assert difference == 180, f"差が{difference}人（期待: 180人）"

    # 選択肢: (1)120人 (2)150人 (3)160人 (4)180人 (5)200人
    correct_option = 4  # 180人
    choices = {1: 120, 2: 150, 3: 160, 4: 180, 5: 200}
    assert choices[correct_option] == difference

    # 他の選択肢が誤答として合理的であることを確認
    # (1) 120人: S=T=1500と仮定した場合の誤答など
    # (2) 150人: 計算ミスの可能性
    # (3) 160人: 全体の%をそのまま使った場合の誤答
    # (5) 200人: 概算による誤答

    print(f"\n正解: ({correct_option}) {difference:.0f}人")
    print("検証OK: 解は唯一")
    return correct_option


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()
    print("\n" + "=" * 60)
    print(f"最終結果: 問1正解=({q1_answer}), 問2正解=({q2_answer})")
    print("全検証完了")
    print("=" * 60)
