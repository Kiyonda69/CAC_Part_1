# -*- coding: utf-8 -*-
"""セット256: クロック方位（○時の方向）トラフィック位置問題の一意性検証

前提（問題文で提示するルール）:
- クロック方位: 12時=機首方向。1時間 = 30°。時刻kの方向 = 相対方位 k*30° (mod 360)
- 通報は最も近い整数時に丸める（相対方位 ±15° の扇形）
- レーダー図は北を上、自機が中心。各機の真方位は図から読み取る
"""

# 機体配置（自機から見た真方位、度）
AIRCRAFT = {"A": 0, "B": 90, "C": 150, "D": 210, "E": 300}


def clock_of(rel_bearing):
    """相対方位(度) -> クロック方位(1-12時)"""
    k = round((rel_bearing % 360) / 30) % 12
    return 12 if k == 0 else k


def verify_q1():
    """問1: 自機針路060°、管制通報「トラフィック、10時の方向」に該当する機は?"""
    own_heading = 60
    matches = []
    for name, tb in AIRCRAFT.items():
        rel = (tb - own_heading) % 360
        if clock_of(rel) == 10:
            matches.append(name)
    assert len(matches) == 1, f"問1: 解が{len(matches)}個 {matches}"
    assert matches[0] == "A", f"問1: 正解がA機でない: {matches[0]}"
    # 全機のクロック方位が互いに異なることも確認（紛れ防止）
    clocks = [clock_of((tb - own_heading) % 360) for tb in AIRCRAFT.values()]
    assert len(set(clocks)) == 5, f"問1: クロック方位に重複 {clocks}"
    print("問1 OK: 正解 = A機（選択肢(1)）, 各機のクロック方位 =",
          dict(zip(AIRCRAFT, clocks)))


def verify_q2():
    """問2: 自機は針路150°に旋回済み。
    条件1: 自機への通報「トラフィックは2時の方向」→ T機の特定
    条件2: T機への通報「トラフィック（自機）は貴機の7時の方向」→ T機の針路
    (T機, 針路) の組を総当たりで検証する。針路は30°刻みの全方位。
    """
    own_heading = 150
    solutions = []
    for name, tb in AIRCRAFT.items():
        rel_own = (tb - own_heading) % 360
        if clock_of(rel_own) != 2:          # 条件1
            continue
        bearing_from_t = (tb + 180) % 360   # T機から見た自機の真方位
        for h in range(0, 360, 30):
            rel_t = (bearing_from_t - h) % 360
            if clock_of(rel_t) == 7:        # 条件2
                solutions.append((name, h))
    assert len(solutions) == 1, f"問2: 解が{len(solutions)}個 {solutions}"
    assert solutions[0] == ("D", 180), f"問2: 想定解と不一致 {solutions[0]}"
    print("問2 OK: 正解 = D機・針路180°（選択肢(3)）")


def verify_q2_choices():
    """問2の誤答選択肢がいずれも条件を満たさないことを確認"""
    own_heading = 150
    choices = {1: ("C", 120), 2: ("D", 120), 3: ("D", 180),
               4: ("E", 180), 5: ("D", 240)}
    valid = []
    for num, (name, h) in choices.items():
        tb = AIRCRAFT[name]
        cond1 = clock_of((tb - own_heading) % 360) == 2
        cond2 = clock_of(((tb + 180) % 360 - h) % 360) == 7
        if cond1 and cond2:
            valid.append(num)
    assert valid == [3], f"問2選択肢: 成立するのは(3)のみのはず: {valid}"
    print("問2 選択肢 OK: 成立するのは(3)のみ")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    verify_q2_choices()
    print("=== 全検証 OK ===")
