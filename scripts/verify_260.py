#!/usr/bin/env python3
"""航大思考260: 航法ログ（ナビゲーションログ）穴埋め問題の検証

規則:
1. 磁方位 = 真方位 + 偏差（西偏は加算、東偏は減算）
2. 羅針方位 = 磁方位 + 自差（自差表の磁方位に最も近い行の値を加える）
3. 対地速度 = TAS + 風成分（追い風+、向かい風-）
4. 所要時間(分) = 距離(NM) / GS × 60
5. 燃料 = 30 L/時 × 時間、予備45分、地上滑走5 L、1 L未満切上げ
"""
import math

# 自差表（磁方位30°ごと）
DEV_TABLE = {0: 1, 30: 2, 60: 3, 90: 1, 120: -2, 150: -3,
             180: -1, 210: 2, 240: 3, 270: 1, 300: -2, 330: -1}
VAR_WEST = 7      # 偏差 西偏7°
TAS = 120         # ノット
FUEL_FLOW = 30    # L/時


def angdiff(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


def nearest_dev(mh):
    """磁方位に最も近い自差表の行（タイがないことも確認）"""
    dists = sorted((angdiff(mh, k), k) for k in DEV_TABLE)
    assert dists[0][0] != dists[1][0], f"自差表の行選択がタイ: 磁方位{mh}"
    return DEV_TABLE[dists[0][1]]


def leg(true_course, dist, wind_comp):
    mh = (true_course + VAR_WEST) % 360
    ch = (mh + nearest_dev(mh)) % 360
    gs = TAS + wind_comp
    t = dist / gs * 60
    return mh, ch, gs, t


# ===== 往路（問1） =====
mh1, ch1, gs1, t1 = leg(70, 85, -20)   # 区間1 A→B 向かい風20
mh2, ch2, gs2, t2 = leg(130, 69, +18)  # 区間2 B→C 追い風18

assert (mh1, ch1, gs1) == (77, 78, 100) and t1 == 51.0, (mh1, ch1, gs1, t1)
assert (mh2, ch2, gs2) == (137, 134, 138) and t2 == 30.0, (mh2, ch2, gs2, t2)

# 問1 空欄: (ア)=磁方位1, (イ)=羅針方位2, (ウ)=GS1, (エ)=所要時間2
answer_q1 = (mh1, ch2, gs1, int(t2))
options_q1 = {
    1: (63, 134, 100, 30),   # 偏差を減算する誤り
    2: (77, 140, 100, 30),   # 自差の符号誤り(137+3)
    3: (77, 134, 100, 30),   # 正解
    4: (77, 134, 140, 30),   # 向かい風を加算する誤り
    5: (77, 134, 100, 35),   # TASで時間計算(34.5→35)
}
matches = [k for k, v in options_q1.items() if v == answer_q1]
assert matches == [3], f"問1: 一致選択肢={matches}"
print(f"問1 OK: (ア){answer_q1[0]}° (イ){answer_q1[1]}° "
      f"(ウ){answer_q1[2]}kt (エ){answer_q1[3]}分 → 正解(3)")

# ===== 復路（問2） =====
mh3, ch3, gs3, t3 = leg((130 + 180) % 360, 69, -30)  # C→B 真310 向かい風30
mh4, ch4, gs4, t4 = leg((70 + 180) % 360, 85, +30)   # B→A 真250 追い風30

assert (mh3, ch3, gs3) == (317, 316, 90) and t3 == 46.0, (mh3, ch3, gs3, t3)
assert (mh4, ch4, gs4) == (257, 258, 150) and t4 == 34.0, (mh4, ch4, gs4, t4)

total_min = t3 + t4                                   # 80分
trip_fuel = FUEL_FLOW * total_min / 60                # 40 L
reserve = FUEL_FLOW * 45 / 60                         # 22.5 L
min_fuel = math.ceil(trip_fuel + reserve + 5)         # 67.5 → 68 L

# 問2 空欄: (ア)=C→B羅針方位, (イ)=合計所要時間, (ウ)=必要最小搭載燃料
answer_q2 = (ch3, int(total_min), min_fuel)
options_q2 = {
    1: (316, 80, 68),  # 正解
    2: (301, 80, 68),  # 偏差減算(303→300行-2→301)
    3: (316, 81, 63),  # 往路時間流用+地上滑走忘れ
    4: (315, 80, 68),  # 自差行を300で選ぶ誤り
    5: (316, 80, 63),  # 地上滑走5L忘れ(62.5→63)
}
matches = [k for k, v in options_q2.items() if v == answer_q2]
assert matches == [1], f"問2: 一致選択肢={matches}"
print(f"問2 OK: (ア){answer_q2[0]}° (イ){answer_q2[1]}分 "
      f"(ウ){answer_q2[2]}L → 正解(1)")
print("検証完了: 両問とも解は一意")
