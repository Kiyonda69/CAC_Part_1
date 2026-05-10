"""
航大思考169 検証スクリプト
資料穴埋め問題（売上データ表からの欠損値復元）
"""


def verify_q1():
    """
    問1: 4店舗 × 3ヶ月の売上表
    各店合計、各月計、総合計が与えられる。
    B店の5月の売上を求める。
    """
    # 与えられた表（万円）
    # 店 | 4月 | 5月 | 6月 | 合計
    # A  | 120 | 135 | 150 | 405
    # B  |  95 |  ?  | 130 | 340
    # C  | 110 | 125 | 145 | 380
    # D  | 105 | 130 | 155 | 390
    # 月計| 430 |  ?  | 580 | 1515

    # B店の5月を逆算
    b_total = 340
    b_apr = 95
    b_jun = 130
    b_may = b_total - b_apr - b_jun
    assert b_may == 115, f"B店の5月={b_may}が期待値115と一致しない"

    # 全体の整合性確認
    a_total = 120 + 135 + 150
    assert a_total == 405

    c_total = 110 + 125 + 145
    assert c_total == 380

    d_total = 105 + 130 + 155
    assert d_total == 390

    # 月計の確認
    apr_total = 120 + 95 + 110 + 105
    assert apr_total == 430

    jun_total = 150 + 130 + 145 + 155
    assert jun_total == 580

    may_total = 135 + b_may + 125 + 130
    assert may_total == 505

    grand_total = a_total + b_total + c_total + d_total
    assert grand_total == 1515

    # 月計の合計確認
    assert apr_total + may_total + jun_total == grand_total

    # 選択肢から一意解であることを確認（候補は5つ）
    candidates = [105, 115, 120, 125, 130]
    valid = [c for c in candidates if c == b_may]
    assert len(valid) == 1, f"解が一意でない: {valid}"

    print(f"問1 答え: B店の5月 = {b_may}万円")
    print(f"問1 選択肢: {candidates}")
    print(f"問1 正解番号: (2)")
    return b_may


def verify_q2():
    """
    問2: 4店舗 × 3ヶ月の売上表（複数空欄）
    複数の空欄が存在し、追加条件を用いて連立で解く。
    A店の6月の売上を求める。

    店 | 4月 | 5月 | 6月 | 合計
    A  |  80 |  ?  |  ?  | 305
    B  |  ?  |  80 |  90 | 240
    C  |  ?  |  85 | 105 | 280
    D  |  75 |  95 |  ?  | 290
    月計| 315 |  ?  |  ?  | 1115

    追加条件:
    - A店の5月の売上は、A店の4月の売上より20多い
    """
    # 既知値の代入
    a_apr = 80
    b_may = 80
    b_jun = 90
    c_may = 85
    c_jun = 105
    d_apr = 75
    d_may = 95

    # 各店合計
    a_total = 305
    b_total = 240
    c_total = 280
    d_total = 290

    # 月計と全体合計
    apr_total_given = 315
    grand_total_given = 1115

    # B店4月の逆算
    b_apr = b_total - b_may - b_jun
    assert b_apr == 70, f"B店4月={b_apr}"

    # C店4月の逆算
    c_apr = c_total - c_may - c_jun
    assert c_apr == 90, f"C店4月={c_apr}"

    # D店6月の逆算
    d_jun = d_total - d_apr - d_may
    assert d_jun == 120, f"D店6月={d_jun}"

    # 4月計の検証
    apr_total = a_apr + b_apr + c_apr + d_apr
    assert apr_total == apr_total_given, f"4月計不整合: {apr_total} vs {apr_total_given}"

    # 全体合計の検証
    sum_totals = a_total + b_total + c_total + d_total
    assert sum_totals == grand_total_given, f"全体合計不整合: {sum_totals}"

    # 追加条件: A店5月 = A店4月 + 20
    a_may = a_apr + 20
    assert a_may == 100

    # A店6月の逆算
    a_jun = a_total - a_apr - a_may
    assert a_jun == 125, f"A店6月={a_jun}"

    # 月計の整合性
    may_total = a_may + b_may + c_may + d_may
    jun_total = a_jun + b_jun + c_jun + d_jun
    assert apr_total + may_total + jun_total == grand_total_given

    # 一意解の確認
    candidates = [100, 105, 115, 120, 125]
    valid = [c for c in candidates if c == a_jun]
    assert len(valid) == 1, f"解が一意でない: {valid}"

    print(f"問2 答え: A店の6月 = {a_jun}万円")
    print(f"問2 選択肢: {candidates}")
    print(f"問2 正解番号: (5)")
    return a_jun


if __name__ == "__main__":
    print("=" * 50)
    print("航大思考169 検証")
    print("=" * 50)
    q1 = verify_q1()
    print()
    q2 = verify_q2()
    print()
    print("=" * 50)
    print("検証完了：解は一意に定まる")
    print("=" * 50)
