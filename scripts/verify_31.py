#!/usr/bin/env python3
"""
航大思考31 解の一意性検証スクリプト
テーマ: スポーツセンター料金計算（資料読み取り）
"""

# ==================== 料金表 ====================
# 施設: 水泳プール, アリーナ, トレーニング室
# 区分: 一般, 学生, シニア(65歳以上)
FEES = {
    '水泳プール': {'一般': 600, '学生': 400, 'シニア': 300},
    'アリーナ':   {'一般': 500, '学生': 300, 'シニア': 250},
    'トレーニング室': {'一般': 400, '学生': 250, 'シニア': 200},
}


def calc_multi_facility(category, facilities):
    """
    2種類以上の施設利用時の料金計算
    ルール: 定価の高い施設が1種類目(定価), 2種類目以降は20%引き(切り捨て)
    """
    prices = [(FEES[f][category], f) for f in facilities]
    prices.sort(reverse=True)  # 高い順に並べ替え

    total = 0
    for i, (price, facility) in enumerate(prices):
        if i == 0:
            total += price          # 1種類目: 定価
        else:
            total += int(price * 0.8)  # 2種類目以降: 20%引き(切り捨て)
    return total


# ==================== 問1 検証 ====================
def verify_q1():
    """
    問1: Aさん(一般)は水泳プール+トレーニング室、Bさん(学生)はアリーナ+水泳プールを利用
    正解: 1,560円
    """
    print("=" * 50)
    print("問1 検証")
    print("=" * 50)

    # Aさん（一般）: 水泳プール(600) + トレーニング室(400)
    a_facilities = ['水泳プール', 'トレーニング室']
    a_fee = calc_multi_facility('一般', a_facilities)
    # 水泳プール(600) > トレーニング室(400) → プール定価, トレーニング20%引き
    # 600 + int(400 * 0.8) = 600 + 320 = 920
    print(f"Aさん（一般）: {a_fee}円")
    assert a_fee == 920, f"Aさんの計算が違う: {a_fee} != 920"

    # Bさん（学生）: アリーナ(300) + 水泳プール(400)
    b_facilities = ['アリーナ', '水泳プール']
    b_fee = calc_multi_facility('学生', b_facilities)
    # 水泳プール(400) > アリーナ(300) → プール定価, アリーナ20%引き
    # 400 + int(300 * 0.8) = 400 + 240 = 640
    print(f"Bさん（学生）: {b_fee}円")
    assert b_fee == 640, f"Bさんの計算が違う: {b_fee} != 640"

    total = a_fee + b_fee
    print(f"合計: {total}円")
    assert total == 1560, f"合計が違う: {total} != 1560"

    print(">>> 問1 正解: 1,560円 (確認済)")
    print()

    # 選択肢の検証（誤答候補）
    print("選択肢の検証:")
    # (1)全施設に20%引き誤り: A:480+320=800, B:320+240=560 → 1,360
    wrong1 = int(600*0.8) + int(400*0.8) + int(400*0.8) + int(300*0.8)
    print(f"  (1) 全施設20%引き誤り: {wrong1}円")
    assert wrong1 == 1360

    # (2)高い方を20%引きにした誤り: A:480+400=880, B:320+300=620 → 1,500
    wrong2 = int(600*0.8)+400 + int(400*0.8)+300
    print(f"  (2) 高い方を20%引き誤り: {wrong2}円")
    assert wrong2 == 1500

    # (3)20%→10%誤り: A:600+360=960, B:400+270=670 → 1,630
    wrong3 = 600 + int(400*0.9) + 400 + int(300*0.9)
    print(f"  (3) 20%→10%誤り: {wrong3}円")
    assert wrong3 == 1630

    # (4)割引なし: 600+400+400+300=1,700
    wrong4 = 600 + 400 + 400 + 300
    print(f"  (5) 割引なし: {wrong4}円")
    assert wrong4 == 1700

    return total


# ==================== 問2 検証 ====================
def calc_q2():
    """
    問2: 5名がアリーナ+追加施設を利用（団体割引あり）
    アリーナ利用5名 → 団体割引(10%引き)
    Cさん(一般): アリーナ+トレーニング室
    Dさん(一般): アリーナのみ
    Eさん(シニア): アリーナのみ
    Fさん(学生): アリーナのみ
    Gさん(一般): アリーナのみ
    正解: 2,165円
    """
    print("=" * 50)
    print("問2 検証")
    print("=" * 50)

    TEAM_DISCOUNT = 0.10  # 団体割引率10%
    MULTI_DISCOUNT = 0.20  # 2種類以上割引率20%

    # アリーナ利用人数: C, D, E, F, G = 5名 → 団体割引適用
    arena_users = 5
    has_team_discount = arena_users >= 5
    print(f"アリーナ利用人数: {arena_users}名 → 団体割引: {'適用' if has_team_discount else '不適用'}")
    print()

    # Cさん（一般）: アリーナ + トレーニング室
    # アリーナ(500) > トレーニング室(400)なのでアリーナが1種類目
    # 1種類目(アリーナ): 団体割引10%引き vs 定価 → 団体割引適用
    # 2種類目(トレーニング室): 2種類割引20%引き vs 団体割引10%引き → 20%引きが有利
    c_arena = int(FEES['アリーナ']['一般'] * (1 - TEAM_DISCOUNT))      # 500*0.9=450
    c_training = int(FEES['トレーニング室']['一般'] * (1 - MULTI_DISCOUNT))  # 400*0.8=320
    c_fee = c_arena + c_training
    print(f"Cさん（一般）:")
    print(f"  アリーナ（1種類目、団体割引）: {c_arena}円")
    print(f"  トレーニング室（2種類目、20%引き）: {c_training}円")
    print(f"  小計: {c_fee}円")
    assert c_fee == 770

    # Dさん（一般）: アリーナのみ（団体割引）
    d_fee = int(FEES['アリーナ']['一般'] * (1 - TEAM_DISCOUNT))  # 500*0.9=450
    print(f"Dさん（一般）: アリーナ（団体割引）: {d_fee}円")
    assert d_fee == 450

    # Eさん（シニア）: アリーナのみ（団体割引）
    e_fee = int(FEES['アリーナ']['シニア'] * (1 - TEAM_DISCOUNT))  # 250*0.9=225
    print(f"Eさん（シニア）: アリーナ（団体割引）: {e_fee}円")
    assert e_fee == 225

    # Fさん（学生）: アリーナのみ（団体割引）
    f_fee = int(FEES['アリーナ']['学生'] * (1 - TEAM_DISCOUNT))  # 300*0.9=270
    print(f"Fさん（学生）: アリーナ（団体割引）: {f_fee}円")
    assert f_fee == 270

    # Gさん（一般）: アリーナのみ（団体割引）
    g_fee = int(FEES['アリーナ']['一般'] * (1 - TEAM_DISCOUNT))  # 500*0.9=450
    print(f"Gさん（一般）: アリーナ（団体割引）: {g_fee}円")
    assert g_fee == 450

    total = c_fee + d_fee + e_fee + f_fee + g_fee
    print(f"\n合計: {total}円")
    assert total == 2165, f"合計が違う: {total} != 2165"

    print(">>> 問2 正解: 2,165円 (確認済)")
    print()

    # 選択肢の検証（誤答候補）
    print("問2 選択肢の検証:")

    # Cさんのアリーナを団体割引せず(500), 他は団体割引ありのミス
    wrong_c2 = (500 + 320) + 450 + 225 + 270 + 450
    print(f"  Cのアリーナに団体割引未適用: {wrong_c2}円")  # 820+1395=2215
    assert wrong_c2 == 2215

    # Cさんのトレーニング室を10%引きで計算（20%の代わり）
    wrong_c3 = (450 + int(400*0.9)) + 450 + 225 + 270 + 450
    print(f"  Cのトレーニング室を10%引き（誤）: {wrong_c3}円")  # 810+1395=2205
    assert wrong_c3 == 2205

    # 団体割引なし
    wrong_nodiscount = (500+int(400*0.8)) + 500 + 250 + 300 + 500
    print(f"  団体割引なし: {wrong_nodiscount}円")  # 820+1550=2370
    assert wrong_nodiscount == 2370

    return total


if __name__ == '__main__':
    q1_answer = verify_q1()
    q2_answer = calc_q2()

    print("=" * 50)
    print(f"問1 正解: {q1_answer:,}円")
    print(f"問2 正解: {q2_answer:,}円")
    print("=" * 50)
    print("全検証完了: 解は一意")
