#!/usr/bin/env python3
"""セット301: 正四面体の切断（断面図・新タイプ）の検証

問1: 一辺6cmの正四面体ABCDを、辺AC・AD・BC・BDの中点P・Q・R・Sを
     通る平面で切断 → 切り口は一辺3cmの正方形になることを検証。
問2: 辺AC上にAP:PC=1:2の点P、辺AD上にAQ:QD=1:2の点Q、
     辺BC上にBR:RC=1:2の点R、辺BD上にBS:SD=1:2の点Sをとり、
     4点を通る平面で切断 → 切り口は2cm×4cmの長方形（面積8cm²）を検証。
"""
from fractions import Fraction as F
import math

# 正四面体: 立方体の交互頂点を利用（辺 = s*sqrt(2)）
# 一辺6cm → s = 6/sqrt(2) = 3*sqrt(2)。長さ² は有理数で扱える。
# s=1 の座標で計算し、辺長² = 2 を単位として実寸に換算する。
A = (F(0), F(0), F(0))
B = (F(1), F(1), F(0))
C = (F(1), F(0), F(1))
D = (F(0), F(1), F(1))
EDGE2_UNIT = F(2)          # s=1 のときの辺長²
SCALE2 = F(36) / EDGE2_UNIT  # 実寸cm² = 単位長² × SCALE2 (辺6cm)

def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def cross(u, v):
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])

def lerp(p, q, t):
    return tuple(a + (b - a) * t for a, b in zip(p, q))

def len2_cm2(u):
    return dot(u, u) * SCALE2  # cm²

def check_all_edges_regular():
    verts = [A, B, C, D]
    for i in range(4):
        for j in range(i+1, 4):
            assert dot(sub(verts[i], verts[j]), sub(verts[i], verts[j])) == EDGE2_UNIT
    # 対辺 AB⊥CD, AC⊥BD, AD⊥BC（正四面体の性質）
    assert dot(sub(B, A), sub(D, C)) == 0
    assert dot(sub(C, A), sub(D, B)) == 0
    assert dot(sub(D, A), sub(C, B)) == 0

def section_points(t):
    """辺AC・AD上はAからt、辺BC・BD上はBからtの位置の4点 P,Q,R,S"""
    P = lerp(A, C, t)
    Q = lerp(A, D, t)
    R = lerp(B, C, t)
    S = lerp(B, D, t)
    return P, Q, R, S

def analyze(t):
    P, Q, R, S = section_points(t)
    # 共面性: 法線 n = PQ×PR に対し PS·n = 0
    n = cross(sub(Q, P), sub(R, P))
    assert dot(sub(S, P), n) == 0, "4点が同一平面上にない"
    # 平面が他の辺 AB・CD と正四面体内部で交わらないこと
    d0 = dot(sub(A, P), n)
    for U, V in [(A, B), (C, D)]:
        du, dv = dot(sub(U, P), n), dot(sub(V, P), n)
        assert du * dv > 0, f"平面が辺{U}{V}と交わる"
    # 四角形 P→Q→S→R の辺ベクトル
    e1, e2, e3, e4 = sub(Q, P), sub(S, Q), sub(R, S), sub(P, R)
    # 対辺の平行性（平行四辺形）: PQ = -SR, QS = -RP
    assert e1 == tuple(-x for x in e3) and e2 == tuple(-x for x in e4)
    # 辺の向き: PQ∥CD, QS∥AB
    assert cross(e1, sub(D, C)) == (0, 0, 0)
    assert cross(e2, sub(B, A)) == (0, 0, 0)
    # 直角（AB⊥CD より）
    assert dot(e1, e2) == 0, "隣り合う辺が直交しない"
    side_pq = math.sqrt(float(len2_cm2(e1)))  # CD方向の辺(cm)
    side_qs = math.sqrt(float(len2_cm2(e2)))  # AB方向の辺(cm)
    area = side_pq * side_qs
    return side_pq, side_qs, area

def verify_q1():
    a, b, area = analyze(F(1, 2))
    assert abs(a - 3.0) < 1e-12 and abs(b - 3.0) < 1e-12, "正方形の辺が3cmでない"
    # 全辺等しい＋直角 → 正方形。5択のうち成立は「正方形」のみ
    shapes = {
        "正三角形": False,            # 頂点は4つ
        "長方形（正方形ではない）": not (a == b),
        "正方形": a == b,
        "ひし形（正方形ではない）": False,  # 直角があるので正方形
        "等脚台形": False,            # 両組の対辺が平行
    }
    assert sum(shapes.values()) == 1 and shapes["正方形"]
    print(f"問1: 切り口は一辺{a:.0f}cmの正方形（面積{area:.0f}cm²）→ 唯一解OK")

def verify_q2():
    a, b, area = analyze(F(1, 3))
    assert abs(a - 2.0) < 1e-12 and abs(b - 4.0) < 1e-12, "長方形が2×4でない"
    assert abs(area - 8.0) < 1e-12
    # 選択肢（ア: 形, イ: 面積）の検証: 正解の組合せのみ成立
    cands = [
        ("正方形", 9.0), ("長方形", 9.0), ("長方形", 8.0),
        ("平行四辺形(直角なし)", 4 * math.sqrt(3)), ("等脚台形", 9.0),
    ]
    ok = [(s, v) for s, v in cands
          if s == "長方形" and a != b and abs(v - area) < 1e-9]
    assert len(ok) == 1, f"成立する選択肢が{len(ok)}個"
    print(f"問2: 切り口は{a:.0f}cm×{b:.0f}cmの長方形（面積{area:.0f}cm²）→ 唯一解OK")

if __name__ == "__main__":
    check_all_edges_regular()
    verify_q1()
    verify_q2()
    # 参考: t を動かすと辺は (1-t)*6 と t*6 の長方形（t=1/2のみ正方形）
    for t in [F(1, 4), F(1, 3), F(1, 2), F(2, 3)]:
        a, b, area = analyze(t)
        print(f"  t={t}: {a:.2f}cm × {b:.2f}cm, 面積{area:.2f}cm²")
    print("すべての検証に合格しました。")
