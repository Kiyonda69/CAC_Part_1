"""
航大思考207 検証スクリプト
文章読解型資料読取問題の数値整合性と選択肢の正誤を確認
"""

def verify_q1():
    """問1: A市観光振興5か年計画"""
    # 本文の数値情報
    past_avg_visitors = 80  # 過去5年平均観光客数（万人）
    target_visitors = 120   # 令和12年度目標（万人）
    total_budget = 12       # 総事業費（億円）
    subsidy_ratio = 0.4     # 国・県補助金比率
    city_ratio = 0.6        # 市一般財源比率
    # 重点施策3つ：歴史文化資源の活用／自然体験型観光の推進／外国人観光客への対応
    # ホテル誘致：含めない（既存宿泊施設の充実支援に切替え）
    # 計画スケジュール：初年度=基盤整備、中期=事業展開、最終年度=成果検証

    # 選択肢検証
    options = {}

    # (1) 過去5年間の年間観光客数は約120万人であった
    # 本文：平均80万人 → 誤
    options[1] = (past_avg_visitors == 120)

    # (2) 計画では新たなホテルの誘致が重点施策の一つとして掲げられている
    # 本文：ホテル誘致は含めず → 誤
    hotel_in_plan = False
    options[2] = hotel_in_plan

    # (3) 5年間の総事業費12億円のうち、約8億円は国・県の補助金で賄われる予定である
    # 本文：補助金は4割 = 12 × 0.4 = 4.8億円 → 8億円ではない → 誤
    subsidy_amount = total_budget * subsidy_ratio
    options[3] = abs(subsidy_amount - 8) < 0.01

    # (4) A市は5年間で観光客数を約1.5倍に増やす目標を掲げている
    # 80万 → 120万 = 1.5倍 → 正
    growth_ratio = target_visitors / past_avg_visitors
    options[4] = abs(growth_ratio - 1.5) < 0.01

    # (5) 計画初年度から事業展開を本格化し、3年目には成果検証を行う予定である
    # 本文：初年度=基盤整備、中期=事業展開、最終(5)年度=成果検証 → 誤
    initial_year_is_expansion = False
    third_year_is_verification = False
    options[5] = initial_year_is_expansion and third_year_is_verification

    # 唯一の正解
    correct_options = [k for k, v in options.items() if v]
    print(f"問1: 選択肢評価={options}")
    print(f"問1: 正しい選択肢={correct_options}")
    assert correct_options == [4], f"問1: 唯一解でない: {correct_options}"
    print(f"問1: 正解(4) ✓")


def verify_q2():
    """問2: D社中期経営計画（令和8〜10年度3か年）"""
    # 令和7年度実績
    sales_7 = 200          # 億円
    op_profit_7 = 16       # 億円
    employees_7 = 800      # 名

    # 計画
    sales_growth = 0.25                          # 25%増加目標
    op_margin_increase_pt = 3                    # 営業利益率3pt引き上げ
    sensor_ratio_10 = 0.45                       # 令和10年度 産業用センサ
    medical_ratio_10 = 0.30                      # 令和10年度 医療機器
    other_ratio_10 = 0.25                        # 令和10年度 その他
    # 令和7年度の産業用センサ売上比率は60%（参考情報）

    capex_total = 60                             # 3年間設備投資総額（億円）
    capex_first_year_ratio = 0.40                # 初年度40%集中投資

    new_hires = 150                              # 計画期間中の新規採用
    natural_decrease = 50                        # 定年退職等による減少
    employees_10 = 900                           # 最終年度従業員数（予想）

    # 計算
    sales_10 = sales_7 * (1 + sales_growth)              # 250億円
    sales_increase = sales_10 - sales_7                  # 50億円
    op_margin_7 = op_profit_7 / sales_7 * 100            # 8%
    op_margin_10_target = op_margin_7 + op_margin_increase_pt  # 11%
    sensor_sales_10 = sales_10 * sensor_ratio_10         # 112.5億
    medical_sales_10 = sales_10 * medical_ratio_10       # 75億
    retire_ratio = natural_decrease / new_hires          # 50/150 = 1/3

    # 整合性検算: 従業員数 800 + 150 - 50 = 900
    assert employees_7 + new_hires - natural_decrease == employees_10

    # 4記述の真偽
    statements = {}
    # ア：令和10年度の売上高目標は、令和7年度比で50億円の増加である
    statements['ア'] = abs(sales_increase - 50) < 0.01

    # イ：令和10年度の営業利益率の目標は、令和7年度実績より3ポイント高い11%である
    statements['イ'] = abs(op_margin_7 - 8) < 0.01 and abs(op_margin_10_target - 11) < 0.01

    # ウ：令和10年度には、医療機器部門の売上が産業用センサ部門の売上を上回る計画となっている
    # 医療75 vs センサ112.5 → センサが上回る → 誤
    statements['ウ'] = medical_sales_10 > sensor_sales_10

    # エ：計画期間中に新規採用される150名のうち、約3分の1が定年退職などで離職する見込み
    # 50/150 = 1/3 → 約3分の1 → 正
    statements['エ'] = abs(retire_ratio - 1/3) < 0.01

    print(f"問2: 記述評価={statements}")
    true_statements = sorted([k for k, v in statements.items() if v])
    print(f"問2: 正しい記述={true_statements}")
    expected = ['ア', 'イ', 'エ']
    assert true_statements == expected, f"問2: 正しい記述が期待と異なる: {true_statements}"

    # 選択肢
    # (1) ア・イ  (2) ア・ウ  (3) イ・ウ  (4) ウ・エ  (5) ア・イ・エ
    options_set = {
        1: ['ア', 'イ'],
        2: ['ア', 'ウ'],
        3: ['イ', 'ウ'],
        4: ['ウ', 'エ'],
        5: ['ア', 'イ', 'エ'],
    }
    matched = [k for k, v in options_set.items() if sorted(v) == true_statements]
    assert matched == [5], f"問2: 唯一解でない: {matched}"
    print(f"問2: 正解(5) ✓")


if __name__ == '__main__':
    verify_q1()
    print()
    verify_q2()
    print()
    print("=" * 40)
    print("全問の検証に成功しました")
