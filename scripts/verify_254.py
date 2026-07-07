#!/usr/bin/env python3
"""航大思考254: 低温時の高度計補正問題の検証"""

# 資料2: 低温補正表（加算する補正量 ft）
# 列: 高度計規正値提供地点からの高さ(ft)
HEIGHTS = [500, 1000, 1500, 2000, 3000, 4000, 5000]
# 行: 飛行場気温(℃)
TABLE = {
    0:   [30,  60,  90,  120, 170, 230, 280],
    -10: [50, 100, 150, 200, 290, 390, 490],
    -20: [70, 140, 210, 280, 420, 570, 710],
    -30: [100, 190, 280, 380, 570, 760, 950],
}


def lookup(temp, height):
    """表の値をそのまま参照（問1用: 温度・高さとも表の値に一致）"""
    return TABLE[temp][HEIGHTS.index(height)]


def interp(temp, height):
    """温度・高さの双方向直線補間（問2用）"""
    temps = sorted(TABLE.keys())  # [-30, -20, -10, 0]
    # 温度方向の補間
    if temp in TABLE:
        row = TABLE[temp]
    else:
        lo = max(t for t in temps if t <= temp)
        hi = min(t for t in temps if t >= temp)
        f = (temp - lo) / (hi - lo)
        row = [a + f * (b - a) for a, b in zip(TABLE[lo], TABLE[hi])]
    # 高さ方向の補間
    if height in HEIGHTS:
        return row[HEIGHTS.index(height)]
    lo_i = max(i for i, h in enumerate(HEIGHTS) if h <= height)
    hi_i = lo_i + 1
    f = (height - HEIGHTS[lo_i]) / (HEIGHTS[hi_i] - HEIGHTS[lo_i])
    return row[lo_i] + f * (row[hi_i] - row[lo_i])


def roundup100(x):
    import math
    return int(math.ceil(x / 100.0)) * 100


def q1():
    """問1: C空港 標高1,000ft, 気温-20℃
    IF 4,000ft / FAF 3,000ft / DA 1,500ft の補正後高度"""
    elev, temp = 1000, -20
    published = {"IF": 4000, "FAF": 3000, "DA": 1500}
    corrected = {}
    for k, alt in published.items():
        h = alt - elev
        assert h in HEIGHTS, f"{k}: 高さ{h}が表にない"
        corrected[k] = alt + lookup(temp, h)
    assert corrected == {"IF": 4420, "FAF": 3280, "DA": 1570}, corrected
    # 選択肢（FAF, DA の組合せ）と誤答パターンの検証
    correct = (corrected["FAF"], corrected["DA"])
    wrong_no_elev = (3000 + lookup(temp, 3000), 1500 + lookup(temp, 1500))  # 標高を引き忘れ
    wrong_row10 = (3000 + lookup(-10, 2000), 1500 + lookup(-10, 500))       # -10℃行を誤用
    wrong_row30 = (3000 + lookup(-30, 2000), 1500 + lookup(-30, 500))       # -30℃行を誤用
    wrong_minus = (3000 - lookup(temp, 2000), 1500 - lookup(temp, 500))     # 減算の誤り
    options = [correct, wrong_no_elev, wrong_row10, wrong_row30, wrong_minus]
    assert len(set(options)) == 5, f"選択肢が重複: {options}"
    print("問1 正解: FAF", correct[0], "ft / DA", correct[1], "ft")
    print("  誤答: 標高引き忘れ", wrong_no_elev, "/ -10℃行", wrong_row10,
          "/ -30℃行", wrong_row30, "/ 減算", wrong_minus)
    return correct


def q2():
    """問2: G飛行場(標高750ft)のQNH・気温-25℃で山岳区間を巡航
    区間1 MEA 4,300ft / 区間2 MEA 5,750ft, 双方向補間+100ft切り上げ"""
    elev, temp = 750, -25
    res = {}
    for name, mea in [("区間1", 4300), ("区間2", 5750)]:
        h = mea - elev
        c = interp(temp, h)
        res[name] = roundup100(mea + c)
    # 手計算での期待値:
    # 区間1: h=3550, -25℃行 col3000=(420+570)/2=495, col4000=(570+760)/2=665
    #        495+0.55*170=588.5 → 4888.5 → 4900
    # 区間2: h=5000, -25℃行 col5000=(710+950)/2=830 → 6580 → 6600
    assert res == {"区間1": 4900, "区間2": 6600}, res
    correct = (res["区間1"], res["区間2"])
    # 誤答パターン
    w20 = tuple(roundup100(m + interp(-20, m - elev)) for m in (4300, 5750))   # -20℃行のみ
    w30 = tuple(roundup100(m + interp(-30, m - elev)) for m in (4300, 5750))   # -30℃行のみ
    def floor_col(m):  # 高さ方向を補間せず低い方の列を使用
        h = m - elev
        h_lo = max(x for x in HEIGHTS if x <= h)
        return roundup100(m + interp(temp, h_lo))
    wfl = tuple(floor_col(m) for m in (4300, 5750))
    import math
    wdn = tuple(int(math.floor((m + interp(temp, m - elev)) / 100)) * 100
                for m in (4300, 5750))                                          # 切り捨て
    options = [correct, w20, w30, wfl, wdn]
    assert len(set(options)) == 5, f"選択肢が重複: {options}"
    print("問2 正解: 区間1", correct[0], "ft / 区間2", correct[1], "ft")
    print("  誤答: -20℃行", w20, "/ -30℃行", w30, "/ 補間なし", wfl, "/ 切り捨て", wdn)
    return correct


if __name__ == "__main__":
    q1()
    q2()
    print("検証OK: 問1・問2とも解は一意")
