"""
verify_26.py - 問題セット26の解の一意性検証
資料読み取り問題：離陸性能図を用いた離陸可能便数の判定
"""

# ============================================================
# 性能図データ（海面高度・無風・標準大気における離陸滑走距離）
# 機体重量ごとの線形モデル: baseline(T) = 定数 + 傾き × (T + 20)
# ============================================================

def get_baseline(weight_lbs, temp_c):
    """機体重量と外気温から海面高度における基準離陸滑走距離を返す（ft）"""
    if weight_lbs == 2000:
        return 660 + 8 * (temp_c + 20)
    elif weight_lbs == 2100:
        return 780 + 10 * (temp_c + 20)
    elif weight_lbs == 2200:
        return 920 + 13 * (temp_c + 20)
    elif weight_lbs == 2300:
        return 1080 + 16 * (temp_c + 20)
    else:
        raise ValueError(f"未対応の機体重量: {weight_lbs}")

# 標高補正係数テーブル
ALTITUDE_CORRECTION = {
    0:     1.00,
    2000:  1.10,
    4000:  1.20,
    6000:  1.30,
    8000:  1.40,
    10000: 1.50,
}

# 風補正係数テーブル（問2用）
WIND_CORRECTION = {
    "HW20": 0.75,   # 向かい風20kt
    "HW10": 0.85,   # 向かい風10kt
    "calm": 1.00,   # 無風
    "TW10": 1.15,   # 追い風10kt
    "TW20": 1.30,   # 追い風20kt
}

# ============================================================
# 問1の検証
# 条件: 滑走路長1,200ft、標高6,000ft（補正係数1.30）
# ============================================================
print("=" * 60)
print("問1の検証")
print("条件: 滑走路長1,200ft、標高6,000ft（補正係数1.30）")
print("=" * 60)

RUNWAY_Q1 = 1200
ELEVATION_Q1 = 6000
ALT_FACTOR_Q1 = ALTITUDE_CORRECTION[ELEVATION_Q1]

flights_q1 = [
    ("ALPHA",   2000,  0),
    ("BRAVO",   2100, 20),
    ("CHARLIE", 2000, 20),
    ("DELTA",   2000, -20),
    ("ECHO",    2100, -10),
    ("FOXTROT", 2300,  0),
    ("GOLF",    2100, -20),
    ("HOTEL",   2100,  0),
    ("INDIA",   2200,  0),
    ("JULIETT", 2000, 30),
]

can_depart_q1 = []
print(f"\n{'便名':<10} {'重量':>8} {'気温':>6} {'基準(ft)':>10} {'補正後(ft)':>12} {'離陸'}")
print("-" * 60)
for name, weight, temp in flights_q1:
    baseline = get_baseline(weight, temp)
    corrected = baseline * ALT_FACTOR_Q1
    can_depart = corrected <= RUNWAY_Q1
    if can_depart:
        can_depart_q1.append(name)
    result = "可能" if can_depart else "不可"
    print(f"{name:<10} {weight:>8} {temp:>6}°C {baseline:>10.0f} {corrected:>12.1f} {result}")

print(f"\n離陸可能便: {can_depart_q1}")
print(f"離陸可能便数: {len(can_depart_q1)}便")
print(f"選択肢(3)の答え: (3) 4便")
assert len(can_depart_q1) == 4, f"想定外の解: {len(can_depart_q1)}便"
assert set(can_depart_q1) == {"ALPHA", "DELTA", "ECHO", "GOLF"}, \
    f"想定外の便: {can_depart_q1}"
print("問1: 解が一意に確認されました (4便)")

# ============================================================
# 問2の検証
# 条件: 滑走路長1,400ft、標高4,000ft（補正係数1.20）＋風補正
# ============================================================
print("\n" + "=" * 60)
print("問2の検証")
print("条件: 滑走路長1,400ft、標高4,000ft（補正係数1.20）＋風補正")
print("=" * 60)

RUNWAY_Q2 = 1400
ELEVATION_Q2 = 4000
ALT_FACTOR_Q2 = ALTITUDE_CORRECTION[ELEVATION_Q2]

flights_q2 = [
    ("ALPHA",   2000,  0, "calm"),
    ("BRAVO",   2200, 10, "calm"),
    ("CHARLIE", 2100,  0, "HW10"),
    ("DELTA",   2300, -20, "TW10"),
    ("ECHO",    2100, -20, "HW10"),
    ("FOXTROT", 2000, 30, "TW20"),
    ("GOLF",    2200, -20, "HW20"),
    ("HOTEL",   2300,  0, "calm"),
    ("INDIA",   2000, 20, "HW10"),
    ("JULIETT", 2100, 20, "TW10"),
]

WIND_LABELS = {
    "HW20": "向かい風20kt",
    "HW10": "向かい風10kt",
    "calm": "無風",
    "TW10": "追い風10kt",
    "TW20": "追い風20kt",
}

can_depart_q2 = []
print(f"\n{'便名':<10} {'重量':>8} {'気温':>6} {'風':>12} {'基準':>8} {'×標高':>8} {'×風':>8} {'離陸'}")
print("-" * 70)
for name, weight, temp, wind in flights_q2:
    baseline = get_baseline(weight, temp)
    after_alt = baseline * ALT_FACTOR_Q2
    wind_factor = WIND_CORRECTION[wind]
    required = after_alt * wind_factor
    can_depart = required <= RUNWAY_Q2
    if can_depart:
        can_depart_q2.append(name)
    result = "可能" if can_depart else "不可"
    wind_label = WIND_LABELS[wind]
    print(f"{name:<10} {weight:>8} {temp:>6}°C {wind_label:>12} {baseline:>8.0f} {after_alt:>8.1f} {required:>8.1f} {result}")

print(f"\n離陸可能便: {can_depart_q2}")
print(f"離陸可能便数: {len(can_depart_q2)}便")
print(f"選択肢(4)の答え: (4) 5便")
assert len(can_depart_q2) == 5, f"想定外の解: {len(can_depart_q2)}便"
assert set(can_depart_q2) == {"ALPHA", "CHARLIE", "ECHO", "GOLF", "INDIA"}, \
    f"想定外の便: {can_depart_q2}"
print("問2: 解が一意に確認されました (5便)")

# ============================================================
# グラフデータ確認（座標計算検証）
# ============================================================
print("\n" + "=" * 60)
print("グラフ座標データ（SVG用）")
print("SVG: 540×390, viewBox 0 0 540 390")
print("チャート領域: x=75(T=-20)〜450(T=30), y=15(2000ft)〜320(400ft)")
print("=" * 60)

def x_coord(T):
    """温度→X座標: x = 75 + 7.5*(T+20)"""
    return 75 + 7.5 * (T + 20)

def y_coord(ft):
    """離陸距離(ft)→Y座標: y = 15 + 305*(2000-ft)/1600"""
    return 15 + 305 * (2000 - ft) / 1600

temps = [-20, -10, 0, 10, 20, 30]
weights = [2000, 2100, 2200, 2300]

for w in weights:
    points = []
    for T in temps:
        b = get_baseline(w, T)
        x = x_coord(T)
        y = y_coord(b)
        points.append(f"({x:.0f},{y:.0f})")
    print(f"{w} lbs: {' '.join(points)}")

print("\n検証完了: 問1=4便[選択肢(3)], 問2=5便[選択肢(4)]")
