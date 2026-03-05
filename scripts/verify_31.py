#!/usr/bin/env python3
"""
航大思考31 解の一意性検証スクリプト
問1: スポーツセンター料金計算（2種類施設割引）
問2: スマートフォン利用料金計算（学割・家族割引と超過料金）
"""

# ==================== 問1 ====================
# 料金表（1人1回あたり）
SPORTS_FEES = {
    '水泳プール': {'一般': 600, '学生': 400, 'シニア': 300},
    'アリーナ':   {'一般': 500, '学生': 300, 'シニア': 250},
    'トレーニング室': {'一般': 400, '学生': 250, 'シニア': 200},
}


def calc_sports_fee(category, facilities):
    """
    スポーツセンター料金計算
    ルール: 定価の高い施設が1種類目(定価), 2種類目以降は20%引き(切り捨て)
    """
    prices = sorted(
        [SPORTS_FEES[f][category] for f in facilities], reverse=True
    )
    total = prices[0]
    for price in prices[1:]:
        total += int(price * 0.8)
    return total


def verify_q1():
    print("=" * 50)
    print("問1 検証（スポーツセンター料金計算）")
    print("=" * 50)

    # Aさん（一般）: 水泳プール(600) + トレーニング室(400)
    a_fee = calc_sports_fee('一般', ['水泳プール', 'トレーニング室'])
    # 600 + int(400*0.8) = 600 + 320 = 920
    print(f"Aさん（一般）: {a_fee}円")
    assert a_fee == 920

    # Bさん（学生）: アリーナ(300) + 水泳プール(400)
    b_fee = calc_sports_fee('学生', ['アリーナ', '水泳プール'])
    # 400 + int(300*0.8) = 400 + 240 = 640
    print(f"Bさん（学生）: {b_fee}円")
    assert b_fee == 640

    total = a_fee + b_fee
    print(f"合計: {total}円")
    assert total == 1560
    print(">>> 問1 正解: 1,560円（位置4）確認済")
    print()

    # 誤答候補の検証
    print("問1 選択肢検証:")
    print(f"  (1) 全施設20%引き誤り: {int(600*0.8)+int(400*0.8)+int(400*0.8)+int(300*0.8)}円")
    assert int(600*0.8)+int(400*0.8)+int(400*0.8)+int(300*0.8) == 1360
    print(f"  (2) 高い方を20%引き誤り: {int(600*0.8)+400+int(400*0.8)+300}円")
    assert int(600*0.8)+400+int(400*0.8)+300 == 1500
    print(f"  (3) 20%→10%誤り: {600+int(400*0.9)+400+int(300*0.9)}円")
    assert 600+int(400*0.9)+400+int(300*0.9) == 1630
    print(f"  (5) 割引なし: {600+400+400+300}円")
    assert 600+400+400+300 == 1700
    print()
    return total


# ==================== 問2 ====================
# スマートフォンプラン料金表
PHONE_PLANS = {
    'ライト':       {'base': 2000, 'data_gb': 3,  'overage': 500},
    'スタンダード': {'base': 4500, 'data_gb': 15, 'overage': 400},
    'プレミアム':   {'base': 7000, 'data_gb': None, 'overage': 0},  # 無制限
}

STUDENT_DISCOUNT = 1000   # 学割: 基本料から1,000円引き（25歳以下）
FAMILY_DISCOUNT = 0.20    # 家族割引: 基本料20%引き（2回線目以降）


def calc_phone_fee(plan_name, usage_gb, is_student=False, is_family_2nd=False):
    """
    スマートフォン月額料金計算
    - 学割と家族割引は重複不可、有利な方を適用
    - 超過料金は割引対象外
    """
    plan = PHONE_PLANS[plan_name]
    base = plan['base']

    # 割引計算（基本料のみ）
    discounted_base = base
    if is_student and is_family_2nd:
        # 有利な方を適用
        student_base = base - STUDENT_DISCOUNT
        family_base = int(base * (1 - FAMILY_DISCOUNT))
        discounted_base = min(student_base, family_base)
    elif is_student:
        discounted_base = base - STUDENT_DISCOUNT
    elif is_family_2nd:
        discounted_base = int(base * (1 - FAMILY_DISCOUNT))

    # 超過料金計算
    overage_fee = 0
    if plan['data_gb'] is not None and usage_gb > plan['data_gb']:
        overage_gb = usage_gb - plan['data_gb']
        overage_fee = overage_gb * plan['overage']

    return discounted_base + overage_fee


def verify_q2():
    print("=" * 50)
    print("問2 検証（スマートフォン料金計算）")
    print("=" * 50)

    # Aさん（一般、スタンダード、1回線目、18GB使用）
    a_fee = calc_phone_fee('スタンダード', 18, is_student=False, is_family_2nd=False)
    # 基本料4,500円 + 超過(18-15)×400=1,200 = 5,700
    print(f"Aさん（一般、スタンダード、18GB）: {a_fee}円")
    assert a_fee == 5700

    # Bさん（20歳、ライト、2回線目、5GB使用）
    # 学割: 2,000-1,000=1,000円 vs 家族割引: 2,000×0.8=1,600円 → 学割が有利
    b_fee = calc_phone_fee('ライト', 5, is_student=True, is_family_2nd=True)
    # 基本料1,000円 + 超過(5-3)×500=1,000 = 2,000
    print(f"Bさん（20歳、ライト、5GB、学割vs家族割引）: {b_fee}円")
    student_base = PHONE_PLANS['ライト']['base'] - STUDENT_DISCOUNT
    family_base = int(PHONE_PLANS['ライト']['base'] * (1 - FAMILY_DISCOUNT))
    print(f"  学割適用後基本料: {student_base}円, 家族割引後基本料: {family_base}円")
    print(f"  → 有利な方（学割）を適用")
    assert b_fee == 2000

    # Cさん（一般、ライト、家族割引なし、2GB使用）
    c_fee = calc_phone_fee('ライト', 2, is_student=False, is_family_2nd=False)
    # 基本料2,000円 + 超過なし(2GB < 3GB) = 2,000
    print(f"Cさん（一般、ライト、2GB、割引なし）: {c_fee}円")
    assert c_fee == 2000

    total = a_fee + b_fee + c_fee
    print(f"合計: {total}円")
    assert total == 9700
    print(">>> 問2 正解: 9,700円（位置5）確認済")
    print()

    # 誤答候補の検証
    print("問2 選択肢検証:")

    # (1) 9,200円: Bさんの超過を1GBのみで計算した誤り
    b_wrong1 = 1000 + 1 * 500  # 超過1GBのみ
    w1 = a_fee + b_wrong1 + c_fee
    print(f"  (1) Bさん超過1GBのみの誤り: {w1}円")
    assert w1 == 9200

    # (2) 10,000円: Aさんの超過レートを500円/GBと誤算
    a_wrong2 = 4500 + 3 * 500  # 400→500に誤算
    w2 = a_wrong2 + b_fee + c_fee
    print(f"  (2) Aさん超過レート500円/GB誤り: {w2}円")
    assert w2 == 10000

    # (3) 10,300円: Bさんに家族割引を適用した誤り（学割より高い方を選んだ）
    b_wrong3 = family_base + 2 * 500  # 家族割引1,600円 + 超過1,000円
    w3 = a_fee + b_wrong3 + c_fee
    print(f"  (3) Bさんに家族割引適用の誤り: {w3}円")
    assert w3 == 10300

    # (4) 10,700円: Bさんに割引なし
    b_wrong4 = 2000 + 2 * 500  # 割引なし2,000円 + 超過1,000円
    w4 = a_fee + b_wrong4 + c_fee
    print(f"  (4) Bさんに割引なしの誤り: {w4}円")
    assert w4 == 10700

    return total


if __name__ == '__main__':
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    print("=" * 50)
    print(f"問1 正解: {q1_answer:,}円（位置4）")
    print(f"問2 正解: {q2_answer:,}円（位置5）")
    print("=" * 50)
    print("全検証完了: 解は一意")
