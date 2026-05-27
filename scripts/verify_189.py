# -*- coding: utf-8 -*-
"""航大思考189 解の一意性検証

問1: 5図書館の年間統計表（蔵書・貸出・登録者・開館日数）から
     導出指標（1人あたり貸出/1日あたり貸出/蔵書回転率）を計算し
     正しい記述を1つ特定する（資料読み取り・標準）。
問2: 6工場の月間生産データ表（生産数・不良品数・稼働時間・作業員数・電力）
     から4種の導出指標を計算し、ア〜オの正誤を判定して
     正しい組み合わせを特定する（資料読み取り・高難度）。
"""


def verify_q1():
    # (蔵書千冊, 貸出千冊, 登録者千人, 開館日数)
    lib = {
        "A": (150, 240, 40, 300),
        "B": (120, 198, 36, 300),
        "C": (200, 280, 56, 280),
        "D": (90, 168, 24, 280),
        "E": (125, 225, 50, 250),
    }
    per_person = {k: v[1] / v[2] for k, v in lib.items()}          # 冊/人
    per_day = {k: v[1] * 1000 / v[3] for k, v in lib.items()}       # 冊/日
    turnover = {k: v[1] / v[0] for k, v in lib.items()}            # 回転率

    # 導出値が一意に順位付けできること（同値がないこと）を確認
    for name, d in [("1人あたり", per_person), ("1日あたり", per_day),
                    ("回転率", turnover)]:
        assert len(set(d.values())) == len(d), f"{name}に同値あり"

    def argmax(d):
        return max(d, key=d.get)

    def argmin(d):
        return min(d, key=d.get)

    statements = {
        1: argmax(per_person) == "A",                  # 1人あたり最多=A?
        2: argmax(turnover) == "E",                    # 回転率最高=E?
        3: argmax(per_day) == "C",                     # 1日あたり最多=C?
        4: per_person["C"] > per_person["B"],          # C>B?
        5: argmin(per_day) == "E",                     # 1日あたり最少=E?
    }
    correct = [k for k, v in statements.items() if v]
    assert correct == [3], f"問1: 正しい記述が{correct}（1つでない）"
    print("問1 OK 正解:(3)")
    print("  1人あたり貸出(冊/人):", {k: round(v, 2) for k, v in per_person.items()})
    print("  1日あたり貸出(冊/日):", {k: round(v) for k, v in per_day.items()})
    print("  蔵書回転率:", {k: round(v, 3) for k, v in turnover.items()})


def verify_q2():
    # (生産数, 不良品数, 稼働時間, 作業員数, 電力kWh)
    fac = {
        "P": (8000, 160, 200, 40, 2400),
        "Q": (9000, 270, 250, 50, 3150),
        "R": (7200, 108, 160, 45, 2880),
        "S": (10000, 250, 200, 40, 2500),
        "T": (6000, 210, 200, 40, 2700),
        "U": (8400, 84, 240, 35, 1680),
    }
    defect = {k: v[1] / v[0] * 100 for k, v in fac.items()}        # 不良品率%
    per_hour = {k: v[0] / v[2] for k, v in fac.items()}           # 個/時
    per_worker = {k: v[0] / v[3] for k, v in fac.items()}        # 個/人
    power_unit = {k: v[4] / v[0] for k, v in fac.items()}        # kWh/個

    for name, d in [("不良品率", defect), ("時間あたり", per_hour),
                    ("1人あたり", per_worker), ("電力単価", power_unit)]:
        assert len(set(d.values())) == len(d), f"{name}に同値あり"

    def argmax(d):
        return max(d, key=d.get)

    def argmin(d):
        return min(d, key=d.get)

    props = {
        "ア": argmax(defect) == argmin(per_hour),           # 不良率最高=時間生産最少
        "イ": argmax(per_worker) == argmax(defect),         # 1人最多=不良率最高
        "ウ": argmin(power_unit) == argmin(defect),         # 電力最少=不良率最低
        "エ": argmax(per_hour) == argmax(per_worker),       # 時間最多=1人最多
        "オ": argmax(power_unit) == argmax(per_worker),     # 電力最多=1人最多
    }
    true_set = {k for k, v in props.items() if v}
    assert true_set == {"ア", "ウ", "エ"}, f"問2: 真の記述が{true_set}"

    options = {
        1: {"ア", "イ"},
        2: {"ア", "ウ", "エ"},
        3: {"イ", "エ"},
        4: {"ウ", "オ"},
        5: {"ア", "エ", "オ"},
    }
    matched = [k for k, s in options.items() if s == true_set]
    assert matched == [2], f"問2: 正解の選択肢が{matched}（一意でない）"
    print("問2 OK 正解:(2) ア・ウ・エ")
    print("  不良品率(%):", {k: round(v, 1) for k, v in defect.items()})
    print("  時間あたり生産(個/h):", {k: round(v) for k, v in per_hour.items()})
    print("  1人あたり生産(個/人):", {k: round(v) for k, v in per_worker.items()})
    print("  1個あたり電力(kWh):", {k: round(v, 2) for k, v in power_unit.items()})
    print("  各記述真偽:", props)


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n全検証パス: 解は一意に確定")
