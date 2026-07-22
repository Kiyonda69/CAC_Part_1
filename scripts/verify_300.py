#!/usr/bin/env python3
"""セット300検証: 容器への注水と水位変化グラフ（グラフ選択型・新タイプ）

問1: 直方体容器（横6×奥行5×高さ8cm）の底に
     おもり（横3×奥行5×高さ4cm）を置き、毎秒6cm³で注水。
     水位h(t)のグラフを5択から選ぶ。正解=(4)

問2: 直方体容器（横8×奥行5×高さ9cm）に高さ6cmの仕切り板
     （左壁から2cm）。左側Aに毎秒10cm³で注水。
     A側の水位のグラフを5択から選ぶ。正解=(3)
"""


def water_level_q1(t):
    """問1の物理シミュレーション: 時刻tでの水位（幾何から直接計算）"""
    v = 6.0 * t  # 注いだ体積
    # フェーズ1: h in [0,4] 有効底面積 = (6-3)*5 = 15
    if v <= 15 * 4:
        return v / 15
    v -= 60
    # フェーズ2: h in [4,8] 底面積 = 6*5 = 30
    return min(4 + v / 30, 8.0)


def level_a_q2(t):
    """問2: A側の水位（仕切り高6cm・A底面積10・B底面積30・全体40）"""
    v = 10.0 * t
    if v <= 10 * 6:          # フェーズ1: Aが0→6cm (体積60)
        return v / 10
    v -= 60
    if v <= 30 * 6:          # フェーズ2: Bが0→6cm、Aは6のまま (体積180)
        return 6.0
    v -= 180
    return min(6 + v / 40, 9.0)  # フェーズ3: 全体40cm²で6→9cm


def piecewise(points):
    """折れ線グラフの評価関数を返す"""
    def f(t):
        for (t0, h0), (t1, h1) in zip(points, points[1:]):
            if t0 <= t <= t1:
                return h0 + (h1 - h0) * (t - t0) / (t1 - t0) if t1 > t0 else h1
        return points[-1][1]
    return f


def curve_q1_opt5(t):
    """問1選択肢(5): 凹型曲線 h = 8*(t/30)^2"""
    return 8.0 * (t / 30.0) ** 2


def match(sim, opt, t_end, tol=1e-6):
    """シミュレーションと選択肢グラフが全時刻で一致するか"""
    n = 3000
    return all(abs(sim(i * t_end / n) - opt(i * t_end / n)) < tol
               for i in range(n + 1))


def verify_q1():
    options = {
        1: piecewise([(0, 0), (10, 4), (20, 4), (30, 8)]),  # 罠: 停滞あり
        2: piecewise([(0, 0), (20, 4), (30, 8)]),           # 罠: 傾き逆転
        3: piecewise([(0, 0), (30, 8)]),                    # 罠: 直線
        4: piecewise([(0, 0), (10, 4), (30, 8)]),           # 正解
        5: curve_q1_opt5,                                    # 罠: 曲線
    }
    matches = [k for k, f in options.items() if match(water_level_q1, f, 30)]
    assert matches == [4], f"問1: 一致選択肢={matches}（期待:[4]）"
    # 数値確認
    assert abs(water_level_q1(10) - 4) < 1e-9   # 10秒で4cm
    assert abs(water_level_q1(30) - 8) < 1e-9   # 30秒で満水
    assert abs(water_level_q1(5) - 2) < 1e-9    # 前半傾き0.4cm/s
    assert abs(water_level_q1(20) - 6) < 1e-9   # 後半傾き0.2cm/s
    print("問1 OK: 正解(4) (0,0)-(10,4)-(30,8)のみ物理と一致")


def verify_q2():
    options = {
        1: piecewise([(0, 0), (18, 6), (24, 6), (36, 9)]),  # 罠: A/B取り違え
        2: piecewise([(0, 0), (6, 6), (36, 9)]),            # 罠: 停滞なし
        3: piecewise([(0, 0), (6, 6), (24, 6), (36, 9)]),   # 正解
        4: piecewise([(0, 0), (6, 6), (36, 6)]),            # 罠: 6cmのまま
        5: piecewise([(0, 0), (6, 0), (24, 6), (36, 9)]),   # 罠: B側の水位
    }
    matches = [k for k, f in options.items() if match(level_a_q2, f, 36)]
    assert matches == [3], f"問2: 一致選択肢={matches}（期待:[3]）"
    assert abs(level_a_q2(6) - 6) < 1e-9    # 6秒でAが仕切り高6cmに
    assert abs(level_a_q2(15) - 6) < 1e-9   # 停滞中
    assert abs(level_a_q2(24) - 6) < 1e-9   # 24秒でBも6cmに
    assert abs(level_a_q2(36) - 9) < 1e-9   # 36秒で満水
    print("問2 OK: 正解(3) (0,0)-(6,6)-(24,6)-(36,9)のみ物理と一致")


def verify_volumes():
    """体積の整合性チェック"""
    # 問1: 容器240 - おもり60 = 水180cm³ = 6cm³/s × 30s
    assert 6 * 5 * 8 - 3 * 5 * 4 == 6 * 30 == 180
    # 問2: 容器8*5*9=360cm³ = 10cm³/s × 36s
    assert 8 * 5 * 9 == 10 * 36 == 360
    print("体積整合 OK: 問1 水180cm³/30秒、問2 水360cm³/36秒")


if __name__ == "__main__":
    verify_volumes()
    verify_q1()
    verify_q2()
    print("すべての検証に合格（解の一意性確認済み）")
