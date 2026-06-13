#!/usr/bin/env python3
"""航大思考216 検証コード: 立体表面の最短経路（展開図で直線化）

問1: 直方体（縦4cm・横3cm・高さ2cm）の頂点Aから対角頂点Gまで、
     表面を伝う最短経路の長さを求める。
問2: 正四角柱（底面1辺3cm・高さ8cm）の下底頂点Aから真上の上底頂点A'まで、
     側面をちょうど2周巻き付けるひもの最短の長さを求める。
"""
import math


def verify_q1():
    """問1: 直方体 4x3x2 の対角頂点間の表面最短経路。

    展開の仕方は3通り（どの2辺を「合算」するか）。
    さらに数値的に経路を離散化して、展開図の最良値と一致することを確認する。
    """
    a, b, c = 4, 3, 2
    candidates = {
        "(a+b)とc": math.sqrt((a + b) ** 2 + c ** 2),  # √53
        "(a+c)とb": math.sqrt((a + c) ** 2 + b ** 2),  # √45
        "(b+c)とa": math.sqrt((b + c) ** 2 + a ** 2),  # √41
    }
    best_name = min(candidates, key=candidates.get)
    best = candidates[best_name]

    # 数値検証: 2面をまたぐ経路を、共有辺上の通過点 t で離散化して最小化
    # 展開すると幅 w1+w2・高さ h の長方形上の直線 → √((w1+w2)^2+h^2)
    def two_face_min(w1, w2, h):
        best_num = float("inf")
        for i in range(100001):
            t = h * i / 100000
            d = math.sqrt(w1 ** 2 + t ** 2) + math.sqrt(w2 ** 2 + (h - t) ** 2)
            best_num = min(best_num, d)
        return best_num

    num_results = [
        two_face_min(b, c, a),  # 共有辺 a をまたぐ
        two_face_min(a, c, b),  # 共有辺 b をまたぐ
        two_face_min(a, b, c),  # 共有辺 c をまたぐ
    ]
    num_best = min(num_results)
    assert abs(num_best - best) < 1e-4, f"数値検証不一致: {num_best} vs {best}"

    traps = {
        "√53 (4+3を合算)": math.sqrt(53),
        "√45 (4+2を合算)": math.sqrt(45),
        "9 (辺伝い 4+3+2)": a + b + c,
        "√29 (内部の対角線)": math.sqrt(a * a + b * b + c * c),
    }
    for name, v in traps.items():
        assert abs(v - best) > 0.1, f"罠 {name} が正解に近すぎる"

    print(f"問1 正解: √41 = {best:.4f} cm（展開 {best_name}）")
    print(f"  数値最小化との一致確認 OK ({num_best:.4f})")
    for name, v in sorted(traps.items(), key=lambda kv: kv[1]):
        print(f"  罠: {name} = {v:.4f}")
    return best


def verify_q2():
    """問2: 正四角柱（底面1辺3・高さ8）の側面をちょうど2周するひもの最短長。

    側面を2周分展開すると 幅24×高さ8 の長方形 → 直線 √(24²+8²) = 8√10。
    数値検証: 経路は8枚の面を順に通過し、7本の縦の辺を横切る。
    各辺上の通過高さを変数として総延長を座標降下法で最小化する。
    """
    s, h = 3, 8
    n_faces = 8  # 2周 = 4面 × 2
    exact = math.sqrt((n_faces * s) ** 2 + h ** 2)  # 8√10

    xs = [i * s for i in range(n_faces + 1)]
    ys = [0.0] * (n_faces + 1)
    ys[n_faces] = float(h)  # 始点(0,0)・終点(24,8)、中間は0から最適化

    def total(ys_):
        return sum(
            math.hypot(xs[i + 1] - xs[i], ys_[i + 1] - ys_[i])
            for i in range(n_faces)
        )

    for _ in range(200):  # 座標降下法 + 三分探索
        for i in range(1, n_faces):
            lo, hi = 0.0, float(h)
            for _ in range(60):
                m1 = lo + (hi - lo) / 3
                m2 = hi - (hi - lo) / 3
                y1, y2 = list(ys), list(ys)
                y1[i], y2[i] = m1, m2
                if total(y1) < total(y2):
                    hi = m2
                else:
                    lo = m1
            ys[i] = (lo + hi) / 2
    num_best = total(ys)
    assert abs(num_best - exact) < 1e-4, f"数値検証不一致: {num_best} vs {exact}"

    traps = {
        "20 (1周で高さ2倍と誤計算 √(12²+16²))": math.sqrt(12 ** 2 + 16 ** 2),
        "4√13 (1周のみ √(12²+8²))": math.sqrt(12 ** 2 + 8 ** 2),
        "8√13 (1周√208を2倍)": 2 * math.sqrt(12 ** 2 + 8 ** 2),
        "32 (辺伝い 24+8)": 24 + 8,
    }
    for name, v in traps.items():
        assert abs(v - exact) > 0.1, f"罠 {name} が正解に近すぎる"

    print(f"問2 正解: 8√10 = {exact:.4f} cm")
    print(f"  数値最小化との一致確認 OK ({num_best:.4f})")
    for name, v in sorted(traps.items(), key=lambda kv: kv[1]):
        print(f"  罠: {name} = {v:.4f}")
    return exact


if __name__ == "__main__":
    verify_q1()
    print()
    verify_q2()
    print("\n検証完了: 両問とも展開図による厳密解と数値最小化が一致（唯一解）")
