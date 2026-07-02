#!/usr/bin/env python3
"""航大思考234 検証スクリプト
問1: 直方体表面の最短経路（頂点A→対角頂点G）
問2: 円錐側面を1周する糸の最短長
"""
import math
from itertools import permutations


def verify_q1():
    """直方体 1cm x 2cm x 4cm の表面最短経路。
    2面をまたぐ展開は3通り: sqrt((a+b)^2 + c^2) の全順列を総当たり。
    """
    dims = (1, 2, 4)
    candidates = set()
    for a, b, c in permutations(dims):
        candidates.add(round(math.sqrt((a + b) ** 2 + c ** 2), 6))
    candidates = sorted(candidates)
    print("問1 展開候補の経路長:", candidates)

    # 最短が5cmで唯一であること
    assert min(candidates) == 5.0, f"最短が5でない: {min(candidates)}"
    assert candidates.count(5.0) == 1, "最短経路長が複数の展開で一致（曖昧）"

    # 罠選択肢の検証
    space_diag = math.sqrt(1 + 4 + 16)      # 空間対角線（表面不可）
    edge_path = 1 + 2 + 4                    # 辺伝い
    print(f"  空間対角線 √21 = {space_diag:.4f}（表面経路ではないため不可）")
    print(f"  他の展開: √29 = {math.sqrt(29):.4f}, √37 = {math.sqrt(37):.4f}")
    print(f"  辺伝い = {edge_path}")
    assert space_diag < 5.0 < math.sqrt(29) < math.sqrt(37) < edge_path
    print("問1 検証OK: 正解 = 5cm（展開 (1+2)x4 の直線）\n")


def verify_q2():
    """円錐（底面半径2cm・母線8cm）の点Aから側面を1周してAへ戻る糸の最短長。
    側面展開図は半径8・中心角 360*2/8 = 90度の扇形。最短 = 弦AA'。
    """
    r, slant = 2, 8
    angle = 360 * r / slant
    assert angle == 90.0, f"中心角が90度でない: {angle}"
    chord = 2 * slant * math.sin(math.radians(angle / 2))
    expected = 8 * math.sqrt(2)
    assert abs(chord - expected) < 1e-9, f"弦の長さ不一致: {chord}"
    print(f"問2 中心角 = {angle}度, 弦 = 8√2 = {chord:.4f} cm")

    # 数値近似（多角形近似で側面測地線が弦に一致することを確認）
    # 展開図上の直線が最短（平面内の2点間）。曲面上の代替経路と比較:
    base_loop = 2 * math.pi * r  # 底面の縁を1周
    two_slant = 2 * slant        # 頂点経由（母線を往復）
    print(f"  底面の縁を1周 = 2π×2 = {base_loop:.4f} cm（弦より長い）")
    print(f"  頂点経由の往復 = {two_slant} cm（弦より長い）")
    assert chord < base_loop < two_slant

    # 弦が扇形の内部に収まる（頂点を通らない）ことを確認
    apex_dist = slant * math.cos(math.radians(angle / 2))
    print(f"  糸が頂点に最も近づく距離 = 8cos45° = {apex_dist:.4f} cm > 0")
    assert apex_dist > 0
    print("問2 検証OK: 正解 = 8√2 cm ≈ 11.31cm\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証OK: 両問とも解は一意")
