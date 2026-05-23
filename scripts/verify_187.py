"""
航大思考187 検証スクリプト
地形（等高線図）の断面図問題の解の一意性を検証する。

問1: 単一の丘。切断線P-Q上の標高列から断面形状の特徴を導出し、
     5つの選択肢のうち全特徴が一致するものが1つだけであることを確認。
問2: 2つの丘（鞍部を挟む）。同様に特徴照合で一意性を確認。
"""


def features_of_profile(samples):
    """(x, 標高) の列から断面の定性的特徴を抽出する。

    returns dict:
      - peaks: 極大の (x, 標高) リスト
      - valleys: 内部の極小（鞍部）の (x, 標高) リスト
      - peak_count
    """
    elevs = [e for _, e in samples]
    xs = [x for x, _ in samples]
    peaks, valleys = [], []
    for i in range(1, len(samples) - 1):
        if elevs[i] > elevs[i - 1] and elevs[i] >= elevs[i + 1]:
            peaks.append((xs[i], elevs[i]))
        if elevs[i] < elevs[i - 1] and elevs[i] <= elevs[i + 1]:
            valleys.append((xs[i], elevs[i]))
    return {"peaks": peaks, "valleys": valleys, "peak_count": len(peaks)}


def classify_q1(samples):
    """問1: 単峰の (peak_pos, slope) を分類。"""
    f = features_of_profile(samples)
    if f["peak_count"] != 1:
        return ("double_or_valley", None)
    px, _ = f["peaks"][0]
    left_x, right_x = samples[0][0], samples[-1][0]
    mid = (left_x + right_x) / 2
    pos = "left" if px < mid - 15 else ("right" if px > mid + 15 else "center")
    # 左右の傾斜（水平距離が短いほど急）
    left_run = px - left_x
    right_run = right_x - px
    if left_run < right_run * 0.7:
        slope = "steep_left"
    elif right_run < left_run * 0.7:
        slope = "steep_right"
    else:
        slope = "symmetric"
    return (pos, slope)


def classify_q2(samples):
    """問2: 双峰の (左右どちらが高いか, 鞍部の深さ区分) を分類。"""
    f = features_of_profile(samples)
    if f["peak_count"] != 2:
        return ("not_double", None)
    (lx, lh), (rx, rh) = f["peaks"]
    if lh > rh + 3:
        balance = "left_high"
    elif rh > lh + 3:
        balance = "right_high"
    else:
        balance = "equal"
    base = min(samples[0][1], samples[-1][1])
    top = max(lh, rh)
    saddle = min(v for _, v in f["valleys"]) if f["valleys"] else top
    ratio = (saddle - base) / (top - base)
    if ratio < 0.25:
        depth = "deep"      # 谷が裾野まで落ちる
    elif ratio > 0.6:
        depth = "shallow"   # ほとんど下がらない
    else:
        depth = "mid"
    return (balance, depth)


# ===== 問1: 切断線P-Q上の標高（西=左が急、東=右が緩） =====
q1_terrain = [
    (40, 5), (90, 10), (105, 20), (118, 30), (128, 40),
    (150, 45), (185, 40), (230, 30), (275, 20), (320, 10), (340, 5),
]
q1_answer = classify_q1(q1_terrain)
print("問1 正解断面の特徴:", q1_answer)

# 5つの選択肢の特徴（作図と対応）
q1_options = {
    1: ("center", "symmetric"),
    2: ("right", "steep_right"),
    3: ("double_or_valley", None),   # 中央が谷（U字）
    4: ("left", "steep_left"),       # ← 正解
    5: ("double_or_valley", None),   # 二峰（M字）
}
q1_match = [k for k, v in q1_options.items() if v == q1_answer]
print("問1 一致する選択肢:", q1_match)
assert q1_match == [4], f"問1の解が一意でない: {q1_match}"

# ===== 問2: 2つの丘（左40m高 / 右32m低 / 鞍部20m） =====
q2_terrain = [
    (30, 5), (50, 10), (62, 20), (72, 30), (85, 40),
    (98, 30), (120, 20), (150, 30), (165, 32),
    (180, 30), (195, 20), (215, 10), (240, 5),
]
q2_answer = classify_q2(q2_terrain)
print("問2 正解断面の特徴:", q2_answer)

q2_options = {
    1: ("equal", "mid"),
    2: ("right_high", "mid"),
    3: ("left_high", "deep"),
    4: ("left_high", "shallow"),
    5: ("left_high", "mid"),         # ← 正解
}
q2_match = [k for k, v in q2_options.items() if v == q2_answer]
print("問2 一致する選択肢:", q2_match)
assert q2_match == [5], f"問2の解が一意でない: {q2_match}"

print("\n検証成功: 問1=(4), 問2=(5) が唯一解")
