#!/usr/bin/env python3
"""航大思考238 検証: 円筒（機体胴体）の曲面展開（計算不要の純粋空間認識）

設定: 胴体を円筒とみなし、真下の母線に沿って切り開き、外側から見た展開図
（左=機首側）を選ぶ。展開図の縦座標 y∈[0,1]: 0=下端(切り口・真下),
0.25=右舷, 0.5=真上, 0.75=左舷, 1=上端(切り口・真下)。

問1: 機首端の真上から右舷側を通ってちょうど1周巻くストライプの展開図
問2: 同ストライプ + 右舷の窓列4個 + 尾部寄り真下の点検口の複合展開図
"""

EPS = 1e-9

def stripe_true_segments():
    """ストライプの展開像（正解）: y(t) = (0.5 - t) mod 1, t∈[0,1]
    → 継ぎ目 t=0.5 で分割された右下がりの平行2線分"""
    return [(0.0, 0.5, 0.5, 0.0), (0.5, 1.0, 1.0, 0.5)]

def sample_stripe(n=2001):
    pts = []
    for i in range(n):
        t = i / (n - 1)
        y = (0.5 - t) % 1.0
        pts.append((t, y))
    return pts

def on_segments(p, segs, tol=1e-6):
    x, y = p
    for (x1, y1, x2, y2) in segs:
        if min(x1, x2) - tol <= x <= max(x1, x2) + tol:
            dx = x2 - x1
            if abs(dx) < EPS:
                if abs(x - x1) < tol and min(y1, y2) - tol <= y <= max(y1, y2) + tol:
                    return True
                continue
            yy = y1 + (y2 - y1) * (x - x1) / dx
            if abs(yy - y) < tol:
                return True
    return False

def stripe_matches(segs):
    """継ぎ目上の点(y=0/1は同一点)を考慮してストライプ像と線分集合を照合"""
    for (t, y) in sample_stripe():
        ok = on_segments((t, y), segs) or \
             (abs(y) < 1e-9 and on_segments((t, 1.0), segs)) or \
             (abs(y - 1.0) < 1e-9 and on_segments((t, 0.0), segs))
        if not ok:
            return False
    # 逆向き照合: 各線分の中点がストライプ像上にあること
    for (x1, y1, x2, y2) in segs:
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        yt = (0.5 - xm) % 1.0
        if not (abs(ym - yt) < 1e-6 or (abs(yt) < 1e-9 and abs(ym - 1.0) < 1e-6)):
            return False
    return True

# ---- 問1: 選択肢のストライプ線分（展開図上, x:0→1 左=機首側） ----
Q1_OPTIONS = {
    "A_correct":   [(0.0, 0.5, 0.5, 0.0), (0.5, 1.0, 1.0, 0.5)],   # 右下がり2分割・継ぎ目一致
    "B_reversed":  [(0.0, 0.5, 0.5, 1.0), (0.5, 0.0, 1.0, 0.5)],   # 巻き方向逆(右上がり)
    "C_diagonal":  [(0.0, 1.0, 1.0, 0.0)],                          # 1本対角線(分割なし)
    "D_misalign":  [(0.0, 0.5, 0.35, 0.0), (0.65, 1.0, 1.0, 0.5)],  # 分割位置がずれ不連続
    "E_vshape":    [(0.0, 0.5, 0.5, 0.0), (0.5, 0.0, 1.0, 0.5)],    # V字(折り返し)
}

# ---- 問2: (ストライプ線分, 窓列のy, 点検口のy位置リスト) ----
WIN_XS = [0.2, 0.4, 0.6, 0.8]
Q2_OPTIONS = {
    "A_correct":    (Q1_OPTIONS["A_correct"],  0.25, [0.0, 1.0]),  # 全部正しい
    "B_reversed":   (Q1_OPTIONS["B_reversed"], 0.25, [0.0, 1.0]),  # 巻き方向逆
    "C_portside":   (Q1_OPTIONS["A_correct"],  0.75, [0.0, 1.0]),  # 窓が左舷の帯
    "D_diagonal":   (Q1_OPTIONS["C_diagonal"], 0.25, [0.0]),       # 対角線1本+点検口下のみ
    "E_misalign":   (Q1_OPTIONS["D_misalign"], 0.25, [0.0, 1.0]),  # 継ぎ目不連続
}

def q1():
    matches = [k for k, segs in Q1_OPTIONS.items() if stripe_matches(segs)]
    assert matches == ["A_correct"], matches
    print("問1 OK: ストライプ展開像に一致する選択肢は A_correct のみ")

def q2():
    true_win_y, true_hatch = 0.25, [0.0, 1.0]
    matches = []
    for k, (segs, win_y, hatch) in Q2_OPTIONS.items():
        ok = stripe_matches(segs) and abs(win_y - true_win_y) < 1e-9 \
             and sorted(hatch) == true_hatch
        if ok:
            matches.append(k)
    assert matches == ["A_correct"], matches
    # 各要素の検証: 窓列の横断位置(ストライプが y=0.25 を横切るのは t=0.25)
    t_cross = 0.25
    assert WIN_XS[0] < t_cross < WIN_XS[1]  # 窓1と窓2の間 ✓
    print("問2 OK: ストライプ・窓列(右舷=下側1/4の帯)・点検口(切り口上→上下両端に2つ)の")
    print("        3要素すべて正しい選択肢は A_correct のみ / ストライプは窓1と窓2の間を横断")

if __name__ == "__main__":
    q1()
    q2()
    print("全検証 OK: 両問とも正解選択肢が唯一に定まる")
