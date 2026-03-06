"""
航大思考45 - 解の一意性検証スクリプト

問1: 製造・販売部門の非正規雇用者割合の変化（資料読み取り）
問2: 3地域の店舗数と平均売上から加重平均を計算（資料読み取り）
"""

def verify_q1():
    """問1: 製造部門と販売部門を合わせた非正規雇用割合の変化"""
    print("=" * 60)
    print("問1: 非正規雇用割合の変化（2016年→2017年）")
    print("=" * 60)

    # データ: (製造正規, 製造非正規, 販売正規, 販売非正規)
    data = {
        2012: (420, 130, 280, 190),
        2013: (380, 170, 310, 160),
        2014: (450, 150, 260, 220),
        2015: (350, 200, 330, 180),
        2016: (400, 160, 290, 210),
        2017: (300, 240, 250, 270),
        2018: (370, 190, 320, 200),
        2019: (340, 220, 270, 250),
    }

    # 各年の非正規割合を検証
    print("\n各年の部門別・合計非正規割合:")
    for year, (mr, mn, sr, sn) in sorted(data.items()):
        m_total = mr + mn
        s_total = sr + sn
        m_ratio = mn / m_total * 100
        s_ratio = sn / s_total * 100
        combined_non = mn + sn
        combined_total = m_total + s_total
        combined_ratio = combined_non / combined_total * 100
        print(f"  {year}年: 製造={m_ratio:.1f}%, 販売={s_ratio:.1f}%, "
              f"合計={combined_non}/{combined_total}={combined_ratio:.2f}%")

    # 2016年と2017年の合計非正規割合
    mr16, mn16, sr16, sn16 = data[2016]
    ratio_2016 = (mn16 + sn16) / (mr16 + mn16 + sr16 + sn16) * 100

    mr17, mn17, sr17, sn17 = data[2017]
    ratio_2017 = (mn17 + sn17) / (mr17 + mn17 + sr17 + sn17) * 100

    change = ratio_2017 - ratio_2016

    print(f"\n2016年合計非正規割合: {ratio_2016:.2f}%")
    print(f"2017年合計非正規割合: {ratio_2017:.2f}%")
    print(f"増加ポイント: {change:.1f}ポイント")

    # 正解: 13.2ポイント → 選択肢(4)
    assert abs(change - 13.2) < 0.1, f"期待値13.2に対して{change:.1f}"
    print(f"\n正解: (4) 13.2ポイント")
    print("検証OK")


def verify_q2():
    """問2: 3地域の加重平均売上高の変化"""
    print("\n" + "=" * 60)
    print("問2: 全地域の1店舗あたり平均売上高の変化（2019年→2020年）")
    print("=" * 60)

    # データ: (東部店舗, 東部平均, 中部店舗, 中部平均, 西部店舗, 西部平均)
    data = {
        2016: (24, 85, 18, 72, 15, 68),
        2017: (28, 78, 20, 75, 18, 70),
        2018: (30, 82, 22, 68, 20, 74),
        2019: (35, 90, 25, 80, 22, 76),
        2020: (40, 72, 28, 65, 30, 60),
        2021: (38, 76, 26, 70, 28, 64),
        2022: (42, 80, 30, 74, 25, 72),
        2023: (45, 84, 32, 78, 27, 68),
    }

    print("\n各年の加重平均売上高:")
    for year, (es, ea, cs, ca, ws, wa) in sorted(data.items()):
        total_rev = es * ea + cs * ca + ws * wa
        total_stores = es + cs + ws
        weighted_avg = total_rev / total_stores
        simple_avg = (ea + ca + wa) / 3
        print(f"  {year}年: 総売上={total_rev}, 総店舗={total_stores}, "
              f"加重平均={weighted_avg:.2f}, 単純平均={simple_avg:.2f}")

    # 2019年と2020年
    es19, ea19, cs19, ca19, ws19, wa19 = data[2019]
    rev_2019 = es19 * ea19 + cs19 * ca19 + ws19 * wa19
    stores_2019 = es19 + cs19 + ws19
    avg_2019 = rev_2019 / stores_2019

    es20, ea20, cs20, ca20, ws20, wa20 = data[2020]
    rev_2020 = es20 * ea20 + cs20 * ca20 + ws20 * wa20
    stores_2020 = es20 + cs20 + ws20
    avg_2020 = rev_2020 / stores_2020

    decrease = avg_2019 - avg_2020

    print(f"\n2019年: 総売上={rev_2019}, 総店舗={stores_2019}, 加重平均={avg_2019:.2f}百万円")
    print(f"2020年: 総売上={rev_2020}, 総店舗={stores_2020}, 加重平均={avg_2020:.2f}百万円")
    print(f"減少額: {decrease:.1f}百万円")

    # トラップ: 単純平均の差
    simple_2019 = (ea19 + ca19 + wa19) / 3
    simple_2020 = (ea20 + ca20 + wa20) / 3
    simple_diff = simple_2019 - simple_2020
    print(f"\n【トラップ】単純平均の差: {simple_diff:.1f}百万円（選択肢(2)に配置）")

    # 正解: 16.9百万円 → 選択肢(3)
    assert abs(decrease - 16.9) < 0.1, f"期待値16.9に対して{decrease:.1f}"
    print(f"\n正解: (3) 16.9百万円")
    print("検証OK")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 60)
    print("全問題の検証が完了しました")
    print("=" * 60)
