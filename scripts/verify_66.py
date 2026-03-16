"""
セット66: 図形の回転と軌跡 - 解の一意性検証

問1（標準）: 正方形が直線上を1回転するときの頂点の軌跡の長さ
問2（高難度）: 円が正三角形の外側を1周するとき、円の中心の軌跡で囲まれた領域の面積
"""
import math

def verify_q1():
    """
    問1: 一辺2cmの正方形ABCDが直線上を滑らずに1回転する。
    頂点Aの軌跡の長さを求める。

    正方形が直線上を転がるとき、各ステップで頂点が回転の中心から
    どの距離にあるかを計算する。

    正方形ABCD（反時計回り）、辺AB=2。
    初期状態: 辺DAが底辺（Dが左、Aが右）に接地。
    追跡する頂点: A

    Step 1: Aを中心に90°回転 → Aは回転の中心、移動距離 = 0
    Step 2: Bを中心に90°回転 → |AB| = 2、円弧 = 2 × π/2 = π
    Step 3: Cを中心に90°回転 → |AC| = 2√2（対角線）、円弧 = 2√2 × π/2 = π√2
    Step 4: Dを中心に90°回転 → |AD| = 2、円弧 = 2 × π/2 = π

    合計 = 0 + π + π√2 + π = π(2 + √2)
    """
    side = 2

    # 各ステップでの回転中心から頂点Aまでの距離
    # Step 1: Aが中心 → 距離 0
    # Step 2: Bが中心 → 距離 = 辺の長さ = 2
    # Step 3: Cが中心 → 距離 = 対角線 = 2√2
    # Step 4: Dが中心 → 距離 = 辺の長さ = 2
    distances = [0, side, side * math.sqrt(2), side]

    # 各ステップの回転角度 = π/2（90°）
    angle = math.pi / 2

    # 軌跡の長さ = Σ(距離 × 角度)
    total_length = sum(d * angle for d in distances)

    # 正解: π(2 + √2)
    expected = math.pi * (2 + math.sqrt(2))

    print("=" * 60)
    print("問1: 正方形の回転と頂点の軌跡")
    print("=" * 60)
    print(f"辺の長さ: {side} cm")
    print(f"各ステップの回転半径: {distances}")
    print(f"各ステップの円弧長:")
    for i, d in enumerate(distances):
        arc = d * angle
        print(f"  Step {i+1}: 半径{d:.4f} × π/2 = {arc:.6f} cm")
    print(f"合計軌跡長: {total_length:.6f} cm")
    print(f"期待値 π(2+√2): {expected:.6f} cm")
    print(f"一致: {abs(total_length - expected) < 1e-10}")
    print()

    # 選択肢の検証
    choices = {
        1: 2 * math.pi * math.sqrt(2),           # 2π√2
        2: 3 * math.pi,                            # 3π
        3: 2 * math.pi * (1 + math.sqrt(2)),       # 2π(1+√2)
        4: math.pi * (2 + math.sqrt(2)),            # π(2+√2) ← 正解
        5: math.pi * (3 + math.sqrt(2)),            # π(3+√2)
    }

    print("選択肢の値:")
    correct_count = 0
    for num, val in choices.items():
        is_correct = abs(val - expected) < 1e-10
        mark = " ← 正解" if is_correct else ""
        print(f"  ({num}) {val:.6f} cm{mark}")
        if is_correct:
            correct_count += 1

    assert correct_count == 1, f"正解が{correct_count}個存在します"
    print(f"\n正解は唯一: (4) π(2+√2)")

    return True


def verify_q2():
    """
    問2: 半径1cmの円が一辺6cmの正三角形の外側を滑らずに1周する。
    円の中心が描く軌跡で囲まれた領域の面積を求める。

    軌跡で囲まれた領域は以下の3つの部分から成る:
    1. 元の正三角形の面積: (√3/4) × 6² = 9√3
    2. 3つの長方形（各辺に沿った帯状領域）: 3 × 6 × 1 = 18
    3. 3つの扇形（各頂点での円弧部分）: 各120°の扇形、半径1
       → 3 × (120/360) × π × 1² = π

    合計: 9√3 + 18 + π
    """
    r = 1  # 円の半径
    s = 6  # 正三角形の辺の長さ

    # 1. 正三角形の面積
    triangle_area = (math.sqrt(3) / 4) * s**2

    # 2. 3つの長方形（帯状領域）の面積
    # 各辺に沿って幅r=1の帯が3本
    rect_area = 3 * s * r

    # 3. 3つの扇形の面積
    # 正三角形の内角 = 60°、外角 = 120°
    # 各頂点で円の中心が描く弧は120°の扇形
    # 3つの扇形で合計360° → 半径rの完全な円
    interior_angle = 60  # 正三角形の内角（度）
    exterior_angle = 180 - interior_angle  # 外角 = 120°
    sector_angle_rad = math.radians(exterior_angle)
    one_sector_area = 0.5 * r**2 * sector_angle_rad
    total_sector_area = 3 * one_sector_area

    # 検証: 3つの扇形の合計 = π × r²（完全な円）
    assert abs(total_sector_area - math.pi * r**2) < 1e-10, "扇形の合計が円にならない"

    total_area = triangle_area + rect_area + total_sector_area
    expected = 9 * math.sqrt(3) + 18 + math.pi

    print("=" * 60)
    print("問2: 円が正三角形の外側を転がる軌跡の面積")
    print("=" * 60)
    print(f"円の半径: {r} cm")
    print(f"正三角形の辺の長さ: {s} cm")
    print(f"正三角形の面積: 9√3 = {triangle_area:.6f} cm²")
    print(f"3つの長方形の面積: {rect_area:.6f} cm²")
    print(f"3つの扇形の面積: π = {total_sector_area:.6f} cm²")
    print(f"  (外角: {exterior_angle}° × 3 = {exterior_angle * 3}°)")
    print(f"合計面積: {total_area:.6f} cm²")
    print(f"期待値 9√3+18+π: {expected:.6f} cm²")
    print(f"一致: {abs(total_area - expected) < 1e-10}")
    print()

    # 軌跡の長さも検証（解説用）
    # 直線部分: 3 × 6 = 18
    # 円弧部分: 3 × (120/360) × 2π × 1 = 2π
    straight_length = 3 * s
    arc_length = 3 * (exterior_angle / 360) * 2 * math.pi * r
    total_path_length = straight_length + arc_length
    expected_path = 18 + 2 * math.pi

    print(f"軌跡の長さ（参考）:")
    print(f"  直線部分: {straight_length} cm")
    print(f"  円弧部分: 2π = {arc_length:.6f} cm")
    print(f"  合計: 18+2π = {total_path_length:.6f} cm")
    print(f"  期待値: {expected_path:.6f} cm")
    print(f"  一致: {abs(total_path_length - expected_path) < 1e-10}")
    print()

    # 選択肢の検証
    sqrt3 = math.sqrt(3)
    choices = {
        1: 9*sqrt3 + 18,                  # 9√3 + 18（扇形なし）
        2: 9*sqrt3 + 18 + 2*math.pi,      # 9√3 + 18 + 2π（扇形が大きすぎ）
        3: 9*sqrt3 + 24,                   # 9√3 + 24（帯幅が大きすぎ）
        4: 9*sqrt3 + 20 + math.pi,         # 9√3 + 20 + π（帯面積が違う）
        5: 9*sqrt3 + 18 + math.pi,         # 9√3 + 18 + π ← 正解
    }

    print("選択肢の値:")
    correct_count = 0
    for num, val in choices.items():
        is_correct = abs(val - expected) < 1e-10
        mark = " ← 正解" if is_correct else ""
        print(f"  ({num}) {val:.6f} cm²{mark}")
        if is_correct:
            correct_count += 1

    assert correct_count == 1, f"正解が{correct_count}個存在します"
    print(f"\n正解は唯一: (5) 9√3+18+π")

    return True


if __name__ == "__main__":
    print("セット66 検証開始\n")

    q1_ok = verify_q1()
    print()
    q2_ok = verify_q2()

    print("\n" + "=" * 60)
    if q1_ok and q2_ok:
        print("全検証OK: 両問とも解が唯一であることを確認")
    else:
        print("検証NG: エラーがあります")
    print("=" * 60)
