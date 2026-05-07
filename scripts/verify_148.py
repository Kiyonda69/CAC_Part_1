# -*- coding: utf-8 -*-
"""航大思考148 解の一意性検証"""


def verify_q1():
    """問1: 配送業者選定問題"""
    # 5社の配送業者データ
    companies = {
        'A': {'days': 1, 'price': 2800, 'weight': 30, 'comp': 50000},
        'B': {'days': 2, 'price': 2200, 'weight': 25, 'comp': 100000},
        'C': {'days': 1, 'price': 3200, 'weight': 50, 'comp': 80000},
        'D': {'days': 2, 'price': 1800, 'weight': 20, 'comp': 30000},
        'E': {'days': 2, 'price': 2500, 'weight': 40, 'comp': 60000},
    }

    # 利用条件
    item_weight = 28      # 商品重量
    item_value = 55000    # 商品価値（補償下限）
    max_days = 2          # 翌々日（=2日）まで許容
    max_price = 2700      # 配送料の上限

    valid = []
    for name, c in companies.items():
        if (c['weight'] >= item_weight
                and c['comp'] >= item_value
                and c['days'] <= max_days
                and c['price'] <= max_price):
            valid.append(name)

    print(f"問1 該当業者: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個"
    return valid[0]


def verify_q2():
    """問2: 通信プラン月額料金計算問題"""
    # 利用者情報
    base_plan = 5000        # スタンダードプラン
    family_discount = True  # 家族割 10%
    long_term_months = 18   # 利用期間（24ヶ月以上で5%引き）
    student = False         # 学生でない
    auto_pay = True         # 自動引き落とし -100円

    option_call = 500       # 通話定額オプション

    # 通話状況
    intl_minutes = 8                    # 国際通話 8分
    intl_rate_per_30s = 60              # 30秒あたり60円

    # データ通信
    plan_data_gb = 30
    used_data_gb = 38
    overage_per_gb = 300

    # 計算（資料の規定: パーセント割引 → 定額割引 の順で基本料金に適用）
    fee = base_plan
    if family_discount:
        fee = fee * 0.9
    if long_term_months >= 24:
        fee = fee * 0.95
    if auto_pay:
        fee = fee - 100

    # オプション加算（割引対象外）
    fee += option_call

    # 国際通話料金（8分 = 480秒 = 16単位）
    intl_units = (intl_minutes * 60) / 30
    fee += intl_units * intl_rate_per_30s

    # データ超過料金
    if used_data_gb > plan_data_gb:
        fee += (used_data_gb - plan_data_gb) * overage_per_gb

    fee = int(fee)
    print(f"問2 月額料金: {fee}円")
    return fee


if __name__ == '__main__':
    ans1 = verify_q1()
    ans2 = verify_q2()
    print(f"\n問1 正解: {ans1}社")
    print(f"問2 正解: {ans2}円")
