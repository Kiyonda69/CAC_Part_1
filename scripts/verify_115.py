"""
航大思考115 解の一意性検証
資料読取・穴埋め問題
"""


def verify_q1():
    """問1: 図書館の蔵書・貸出統計"""
    # 資料データ
    data = {
        "一般書":       {"蔵書": 48000, "貸出": 72000},
        "児童書":       {"蔵書": 18000, "貸出": 85000},
        "専門書":       {"蔵書": 22000, "貸出":  9000},
        "雑誌・新聞":   {"蔵書":  8000, "貸出": 14000},
    }

    # 正しい値を計算
    total_books = sum(v["蔵書"] for v in data.values())  # 96,000
    max_category = max(data.items(), key=lambda x: x[1]["蔵書"])[0]  # 一般書
    max_loan_value = max(v["貸出"] for v in data.values())  # 85,000（児童書）
    max_loan_category = max(data.items(), key=lambda x: x[1]["貸出"])[0]  # 児童書

    # 選択肢を評価
    options = [
        {"ア": 180000, "イ": "一般書", "ウ": 72000},   # (1)
        {"ア":  96000, "イ": "一般書", "ウ": 85000},   # (2) 正解
        {"ア":  96000, "イ": "児童書", "ウ": 85000},   # (3)
        {"ア":  96000, "イ": "一般書", "ウ": 72000},   # (4)
        {"ア":  88000, "イ": "一般書", "ウ": 85000},   # (5)
    ]

    correct_tuple = (total_books, max_category, max_loan_value)
    assert max_loan_category == "児童書", "貸出最多は児童書である必要"

    valid = []
    for i, opt in enumerate(options, 1):
        if (opt["ア"], opt["イ"], opt["ウ"]) == correct_tuple:
            valid.append(i)

    assert len(valid) == 1, f"問1 解が{len(valid)}個: {valid}"
    assert valid[0] == 2, f"問1 正解は(2)のはず、得られた値: {valid[0]}"
    print(f"問1: 唯一解 = ({valid[0]})")
    print(f"  ア={total_books:,}冊, イ={max_category}, ウ={max_loan_value:,}冊")


def verify_q2():
    """問2: 企業部門別業績と生産性"""
    # 資料データ
    data = {
        "製造":     {"2024売上": 300, "2024人員": 500, "2025売上": 360, "2025人員": 500},
        "販売":     {"2024売上": 200, "2024人員": 200, "2025売上": 250, "2025人員": 250},
        "サービス": {"2024売上": 200, "2024人員": 400, "2025売上": 220, "2025人員": 400},
    }
    total_2024 = sum(v["2024売上"] for v in data.values())  # 700
    total_2025 = sum(v["2025売上"] for v in data.values())  # 830

    increase = total_2025 - total_2024  # 130
    growth_rate = increase / total_2024 * 100  # 18.57...

    # 2025年度の生産性（万円/人）: 億円 → 万円 は ×10,000
    productivity = {k: v["2025売上"] * 10000 / v["2025人員"] for k, v in data.items()}
    # 製造: 360*10000/500 = 7200
    # 販売: 250*10000/250 = 10000
    # サービス: 220*10000/400 = 5500
    top_dept = max(productivity, key=productivity.get)  # 販売
    top_value = productivity[top_dept]  # 10,000

    print(f"  全社売上増加: {increase}億円")
    print(f"  成長率: {growth_rate:.1f}%")
    print(f"  生産性: {productivity}")
    print(f"  最高生産性: {top_dept} = {top_value:.0f}万円")

    options = [
        {"ア": 130, "イ": 18.6, "ウ": "販売",     "エ": 10000},  # (1) 正解
        {"ア": 130, "イ": 15.7, "ウ": "販売",     "エ": 10000},  # (2)
        {"ア": 130, "イ": 18.6, "ウ": "製造",     "エ":  7200},  # (3)
        {"ア": 140, "イ": 20.0, "ウ": "販売",     "エ": 10000},  # (4)
        {"ア": 130, "イ": 18.6, "ウ": "販売",     "エ":  7200},  # (5)
    ]

    correct = (130, 18.6, "販売", 10000)
    # 成長率は四捨五入で18.6
    assert round(growth_rate, 1) == 18.6, f"成長率は18.6%のはず: {growth_rate}"
    assert top_dept == "販売"
    assert int(top_value) == 10000

    valid = []
    for i, opt in enumerate(options, 1):
        if (opt["ア"], opt["イ"], opt["ウ"], opt["エ"]) == correct:
            valid.append(i)

    assert len(valid) == 1, f"問2 解が{len(valid)}個: {valid}"
    assert valid[0] == 1, f"問2 正解は(1)のはず、得られた値: {valid[0]}"
    print(f"問2: 唯一解 = ({valid[0]})")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n✔ 両問題とも解の一意性を確認")
