#!/usr/bin/env python3
"""航大思考253: SID上昇勾配要件の検証

資料:
- 換算式: 必要上昇率[ft/min] = 必要上昇勾配[ft/NM] × 対地速度GS[kt] ÷ 60
- GS = TAS + 追い風成分（向かい風は減算）
- 上昇性能表（上昇率 ft/min）
    重量\OAT   10°C  20°C  30°C
    2,200 lb    980   900   820
    2,400 lb    880   800   720
    2,600 lb    780   700   620
"""

PERF = {  # (weight, oat) -> rate of climb ft/min
    (2200, 10): 980, (2200, 20): 900, (2200, 30): 820,
    (2400, 10): 880, (2400, 20): 800, (2400, 30): 720,
    (2600, 10): 780, (2600, 20): 700, (2600, 30): 620,
}


def roc(weight, oat):
    """重量方向に線形補間（OATは表の値のみ使用）"""
    lo, hi = 2200, 2400
    if weight > 2400:
        lo, hi = 2400, 2600
    r_lo, r_hi = PERF[(lo, oat)], PERF[(hi, oat)]
    return r_lo + (r_hi - r_lo) * (weight - lo) / (hi - lo)


def q1():
    """問1: 勾配330ft/NM, OAT30°C, 重量2400lb, TAS120kt, 追い風10kt"""
    grad, tas, tail = 330, 120, 10
    gs = tas + tail
    required = grad * gs / 60
    available = roc(2400, 30)
    ok = available >= required
    print(f"問1: GS={gs}kt 必要上昇率={required}ft/min 性能={available}ft/min 可否={ok}")
    assert required == 715 and available == 720 and ok
    # 選択肢の一意性: (必要上昇率, 可否) の正しい組は1つだけ（正解は(3)）
    options = [(605, True), (660, True), (715, True), (715, False), (660, False)]
    correct = [i + 1 for i, o in enumerate(options) if o == (required, ok)]
    assert correct == [3], f"問1の正解位置が{correct}"
    # 誤答の由来: 660=風無視(GS120), 605=風を減算(GS110)
    assert grad * tas / 60 == 660 and grad * (tas - tail) / 60 == 605


def q2():
    """問2: 障害物2つ, DER標高650ft, 余裕100ft, OAT20°C, 無風GS120kt"""
    der_elev, margin, gs, oat = 650, 100, 120, 20
    obstacles = [(4.0, 1750), (2.5, 1500)]  # (距離NM, 標高ft)
    grads = [(elev + margin - der_elev) / d for d, elev in obstacles]
    print(f"問2: 必要勾配 A={grads[0]}ft/NM B={grads[1]}ft/NM")
    assert grads == [300.0, 380.0]
    governing = max(grads)
    required = governing * gs / 60
    assert required == 760
    # 最大重量: 総当たり（1lb刻み）で条件を満たす最大値
    max_w = max(w for w in range(2200, 2601) if roc(w, oat) >= required)
    print(f"問2: 必要上昇率={required}ft/min 最大重量={max_w}lb")
    assert max_w == 2480
    # 選択肢の一意性: 要件を満たすのは選択肢中1つだけ（正解は(1)）
    options = [2480, 2520, 2560, 2600, 2640]
    feasible = [i + 1 for i, w in enumerate(options) if roc(w, oat) >= required]
    assert feasible == [1], f"問2の正解位置が{feasible}"
    # 誤答の由来: 2640 = 余裕100ftを忘れた場合の最大重量
    grad_no_margin = max((elev - der_elev) / d for d, elev in obstacles)
    w_no_margin = max(w for w in range(2200, 2601 + 100)
                      if 900 - 0.5 * (w - 2200) >= grad_no_margin * gs / 60)
    print(f"問2: 選択肢の可否 = {[(w, roc(w, oat) >= required) for w in options]}")
    print(f"問2: 余裕忘れの誤答 = {w_no_margin}lb")
    assert w_no_margin == 2640


if __name__ == "__main__":
    q1()
    q2()
    print("検証OK: 両問とも解は一意")
