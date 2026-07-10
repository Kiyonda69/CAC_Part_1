#!/usr/bin/env python3
"""航大思考270 検証: 直方体水槽を傾けたときの水面（体積保存・断面把握）

容器: 底面 横6cm × 奥行き4cm、高さ8cm。
奥行き方向（長さ4cm）の底の辺を床につけたまま傾ける。
断面（傾け軸に垂直）: 幅W=6, 高さH=8 の長方形。奥行きD=4。
"""

W, D, H = 6.0, 4.0, 8.0
BASE = W * D  # 24 cm^2


def verify_q1():
    """問1: 水深5.5cmの水を傾け、水面がちょうど注ぎ口側の上端の辺に達した。
    反対側の側面と水面が交わる位置の底面からの高さ h を求める。
    水の断面 = 台形（低い側 H, 高い側 h）: (H+h)/2 * W * D = W * D * 5.5
    """
    volume = BASE * 5.5  # 132 cm^3
    solutions = []
    for i in range(0, int(H * 100) + 1):  # h を 0.01 刻みで総当たり
        h = i / 100.0
        if abs((H + h) / 2.0 * W * D - volume) < 1e-9:
            solutions.append(h)
    assert len(solutions) == 1, f"問1: 解が{len(solutions)}個"
    h = solutions[0]
    assert 0 < h < H, "台形（水面が底面・上面と交わらない）が成立すること"
    assert abs(h - 3.0) < 1e-9
    print(f"問1: h = {h} cm（正解 3cm・台形の平均性質 (8+h)/2 = 5.5）")
    return h


def verify_q2():
    """問2: 満水(192cm^3)から傾けて水を捨て、底面のちょうど半分(3cm)が
    露出したところで止め、水平に戻したときの水深を求める。
    水の断面 = 三角形（底辺 W/2=3, 高さ H=8）→ V = 1/2*3*8*4 = 48
    """
    wet_base = W / 2.0
    remaining = 0.5 * wet_base * H * D
    depth = remaining / BASE
    assert abs(remaining - 48.0) < 1e-9
    assert abs(depth - 2.0) < 1e-9
    # 物理整合: 底面が露出し始める瞬間(断面=直角三角形W×H)の残量より少ない
    at_exposure = 0.5 * W * H * D  # 96
    assert remaining < at_exposure < BASE * H  # 48 < 96 < 192 単調減少
    # 罠: 「半分露出=半分残る」→ 96/24 = 4cm ／ 露出開始時と混同 → 4cm
    trap_half = (BASE * H / 2.0) / BASE
    print(f"問2: 残量 = {remaining} cm^3, 戻した水深 = {depth} cm（正解 2cm）")
    print(f"  罠: 半分残る誤解 → {trap_half} cm（正解と異なることを確認）")
    assert trap_half != depth
    return depth


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証OK: 問1・問2とも唯一解")
