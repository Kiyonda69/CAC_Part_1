"""
航大思考202 検証スクリプト

問1: 3部門×3か月の売上集計表（穴埋め）
問2: 4部門×3か月の売上＋原価率（穴埋め＋利益率）
"""


def verify_q1():
    """問1: 売上集計表の穴埋め検証"""
    # 与えられた情報
    A_april, A_may = 800, 900
    B_may, B_june = 700, 800
    C_april, C_june = 1200, 1400
    A_total = 2700
    B_total = 2100
    total_april = 2600
    total_may = 3000

    # 穴埋め計算
    A_june = A_total - A_april - A_may  # = 1000
    B_april = B_total - B_may - B_june  # = 600
    C_may = total_may - A_may - B_may   # = 1400

    # 4月合計の整合性確認
    assert A_april + B_april + C_april == total_april, \
        f"4月合計不整合: {A_april + B_april + C_april} != {total_april}"

    # C合計
    C_total = C_april + C_may + C_june   # = 4000
    # 6月合計
    total_june = A_june + B_june + C_june  # = 3200
    # 全社四半期合計
    grand_total_by_dept = A_total + B_total + C_total
    grand_total_by_month = total_april + total_may + total_june

    assert grand_total_by_dept == grand_total_by_month, \
        f"集計方向で不一致: 部門{grand_total_by_dept} 月別{grand_total_by_month}"

    print(f"問1 計算結果:")
    print(f"  A 6月 = {A_june}")
    print(f"  B 4月 = {B_april}")
    print(f"  C 5月 = {C_may}")
    print(f"  C 合計 = {C_total}")
    print(f"  6月合計 = {total_june}")
    print(f"  全社四半期合計 = {grand_total_by_dept} 万円")
    return grand_total_by_dept


def verify_q2():
    """問2: 売上＋原価率の穴埋め＋粗利益率"""
    # 与えられた月別売上（一部空欄）
    # A: 4月600, 5月?, 6月700, 合計2000, 原価率55%
    # B: 4月?, 5月500, 6月600, 合計?, 原価率60%, 原価900
    # C: 4月1000, 5月1000, 6月?, 合計3000, 原価率?, 原価1950
    # D: 4月500, 5月?, 6月500, 合計1500, 原価率70%
    A_april, A_june, A_total, A_rate = 600, 700, 2000, 0.55
    B_may, B_june, B_rate, B_cost = 500, 600, 0.60, 900
    C_april, C_may, C_total, C_cost = 1000, 1000, 3000, 1950
    D_april, D_june, D_total, D_rate = 500, 500, 1500, 0.70

    # 計算
    A_may = A_total - A_april - A_june          # 700
    B_total = B_cost / B_rate                   # 1500
    B_april = B_total - B_may - B_june          # 400
    C_june = C_total - C_april - C_may          # 1000
    C_rate = C_cost / C_total                   # 0.65
    D_may = D_total - D_april - D_june          # 500

    # 各部門の原価
    A_cost = A_total * A_rate                   # 1100
    D_cost = D_total * D_rate                   # 1050

    # 全社売上・原価
    total_sales = A_total + B_total + C_total + D_total
    total_cost = A_cost + B_cost + C_cost + D_cost
    gross_profit = total_sales - total_cost
    gross_rate = gross_profit / total_sales * 100

    # 整合性チェック: 月別合計でも検算
    april_total = A_april + B_april + C_april + D_april
    may_total = A_may + B_may + C_may + D_may
    june_total = A_june + B_june + C_june + D_june
    assert april_total + may_total + june_total == total_sales, \
        f"月別合計と部門合計が不一致"

    print(f"\n問2 計算結果:")
    print(f"  A 5月 = {A_may}, 原価 = {A_cost}")
    print(f"  B 4月 = {B_april}, 合計 = {B_total}")
    print(f"  C 6月 = {C_june}, 原価率 = {C_rate*100}%")
    print(f"  D 5月 = {D_may}, 原価 = {D_cost}")
    print(f"  4月合計 = {april_total}, 5月合計 = {may_total}, 6月合計 = {june_total}")
    print(f"  全社売上 = {total_sales}")
    print(f"  全社原価 = {total_cost}")
    print(f"  全社粗利益 = {gross_profit}")
    print(f"  全社粗利益率 = {gross_rate}%")
    return gross_rate


if __name__ == "__main__":
    ans1 = verify_q1()
    ans2 = verify_q2()
    print(f"\n=== 最終解答 ===")
    print(f"問1: 全社四半期総売上 = {ans1} 万円")
    print(f"問2: 全社粗利益率 = {ans2}%")
