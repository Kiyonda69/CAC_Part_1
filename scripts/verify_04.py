"""
セット4 解の一意性検証スクリプト

問1: 通信費データの読み取り（部署別スマートフォン料金）
問2: 電力料金データの読み取り（段階料金制）
"""


def verify_q1():
    """
    問1: 通信費データの読み取り

    通話料金（円）= 通話時間（分）× 通話単価（円/分）
    データ料金（円）= データ通信量（GB）× データ単価（円/GB）
    合計（円）= 通話料金 + データ料金 + 基本料金

    既知データから単価を導出し、企画部のデータ通信量（ア）を求める
    """
    data = [
        {"部署": "営業部", "通話時間": 300, "データ通信量": 10,
         "通話料金": 6000, "データ料金": 2500, "基本料金": 1500, "合計": 10000},
        {"部署": "総務部", "通話時間": 150, "データ通信量": 5,
         "通話料金": 3000, "データ料金": 1250, "基本料金": 1500, "合計": 5750},
        {"部署": "技術部", "通話時間": 200, "データ通信量": 15,
         "通話料金": 4000, "データ料金": 3750, "基本料金": 1500, "合計": 9250},
    ]

    # 単価の一貫性を検証
    call_rate = None
    data_rate = None
    base_fee = 1500

    for row in data:
        r = row["通話料金"] / row["通話時間"]
        d = row["データ料金"] / row["データ通信量"]

        assert row["合計"] == row["通話料金"] + row["データ料金"] + base_fee, \
            f"合計の計算が合わない: {row['部署']}"

        if call_rate is None:
            call_rate = r
        assert r == call_rate, f"通話単価が不一致: {row['部署']}: {r} vs {call_rate}"

        if data_rate is None:
            data_rate = d
        assert d == data_rate, f"データ単価が不一致: {row['部署']}: {d} vs {data_rate}"

    print(f"通話単価: {call_rate} 円/分")
    print(f"データ単価: {data_rate} 円/GB")

    # 企画部の（ア）を求める
    kikabu = {"通話時間": 250, "合計": 10250, "基本料金": 1500}
    call_fee = kikabu["通話時間"] * call_rate
    assert call_fee == 5000, f"通話料金の計算エラー: {call_fee}"

    data_fee = kikabu["合計"] - call_fee - kikabu["基本料金"]
    assert data_fee == 3750, f"データ料金の計算エラー: {data_fee}"

    data_volume = data_fee / data_rate
    assert data_volume == 15, f"データ通信量の計算エラー: {data_volume}"

    print(f"\n問1 正解: （ア）= {data_volume} GB")
    print("選択肢: (1)15  (2)10  (3)12  (4)18  (5)20")
    print("正解番号: (1)")
    return data_volume


def verify_q2():
    """
    問2: 電力料金データの読み取り（段階料金制）

    合計料金（円）= 基本料金 + 使用料金
    使用料金は段階料金制（各段階の境界値と単価を表から導出）:
      第1段階: 0〜100 kWh: 25 円/kWh
      第2段階: 101〜200 kWh: 35 円/kWh
      第3段階: 201 kWh以上: 45 円/kWh
    """
    def calc_usage_fee(kwh):
        if kwh <= 100:
            return kwh * 25
        elif kwh <= 200:
            return 100 * 25 + (kwh - 100) * 35
        else:
            return 100 * 25 + 100 * 35 + (kwh - 200) * 45

    base_fee = 1000

    data = [
        {"月": "1月", "使用量": 80,  "使用料金": 2000, "合計": 3000},
        {"月": "2月", "使用量": 150, "使用料金": 4250, "合計": 5250},
        {"月": "3月", "使用量": 250, "使用料金": 8250, "合計": 9250},
    ]

    # 段階料金の検証
    for row in data:
        fee = calc_usage_fee(row["使用量"])
        assert fee == row["使用料金"], \
            f"使用料金の計算エラー: {row['月']}: {fee} vs {row['使用料金']}"
        assert row["合計"] == base_fee + row["使用料金"], \
            f"合計料金の計算エラー: {row['月']}"

    print("段階料金の検証完了:")
    print("  第1段階 (0-100 kWh): 25 円/kWh")
    print("  第2段階 (101-200 kWh): 35 円/kWh")
    print("  第3段階 (201+ kWh): 45 円/kWh")

    # 4月の（ア）を求める（使用料金=5,300円の場合の使用量）
    target_usage_fee = 5300
    target_total = 6300

    assert target_total == base_fee + target_usage_fee, "合計料金の整合性エラー"

    # 第1段階の最大: 100 × 25 = 2,500 < 5,300 → 第2段階に突入
    tier1_max = 100 * 25  # = 2,500
    assert tier1_max < target_usage_fee, "第1段階のみでは不足"

    # 第2段階での追加使用量を計算
    remaining = target_usage_fee - tier1_max  # = 2,800
    tier2_kwh = remaining / 35  # = 80 kWh
    assert tier2_kwh == 80, f"第2段階使用量計算エラー: {tier2_kwh}"

    usage = 100 + tier2_kwh  # = 180 kWh
    assert usage == 180, f"使用量計算エラー: {usage}"
    assert usage <= 200, "第2段階の範囲内であること"

    # 第3段階が必要かチェック（不要なことを確認）
    tier2_check = 100 * 25 + 100 * 35  # 第2段階満杯 = 6,000
    assert target_usage_fee < tier2_check, "第3段階は不要"

    # 逆向き検証: calc_usage_fee(180) = 5,300
    assert calc_usage_fee(180) == target_usage_fee, "逆検証失敗"

    print(f"\n問2 正解: （ア）= {int(usage)} kWh")
    print("選択肢: (1)180  (2)80  (3)150  (4)160  (5)200")
    print("正解番号: (1)")
    return int(usage)


def verify_uniqueness_q1():
    """問1の解の一意性: 全ての整数値GB(1-30)を試して唯一解を確認"""
    call_rate = 20   # 円/分
    data_rate = 250  # 円/GB
    base_fee = 1500

    # 企画部の条件
    call_time = 250  # 分
    total = 10250    # 円

    valid_solutions = []
    for data_volume in range(1, 100):
        call_fee = call_time * call_rate
        data_fee = data_volume * data_rate
        calc_total = call_fee + data_fee + base_fee
        if calc_total == total:
            valid_solutions.append(data_volume)

    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在: {valid_solutions}"
    print(f"\n問1 一意性検証: 解は {valid_solutions[0]} GB のみ ✓")
    return valid_solutions[0]


def verify_uniqueness_q2():
    """問2の解の一意性: 使用量 1-300kWh を総当たりして唯一解を確認"""
    def calc_usage_fee(kwh):
        if kwh <= 100:
            return kwh * 25
        elif kwh <= 200:
            return 100 * 25 + (kwh - 100) * 35
        else:
            return 100 * 25 + 100 * 35 + (kwh - 200) * 45

    target = 5300
    valid_solutions = []
    for kwh in range(1, 301):
        if calc_usage_fee(kwh) == target:
            valid_solutions.append(kwh)

    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在: {valid_solutions}"
    print(f"問2 一意性検証: 解は {valid_solutions[0]} kWh のみ ✓")
    return valid_solutions[0]


if __name__ == "__main__":
    print("=" * 50)
    print("セット4 問1 検証")
    print("=" * 50)
    verify_q1()
    verify_uniqueness_q1()

    print()
    print("=" * 50)
    print("セット4 問2 検証")
    print("=" * 50)
    verify_q2()
    verify_uniqueness_q2()

    print()
    print("全検証完了 ✓")
