"""航大思考248 検証スクリプト（重量・重心位置の資料読取問題）

資料（共通）:
- モーメント = 重量 × アーム（基準点から後方の距離）
- 重心位置 = 総モーメント ÷ 総重量
- 最大離陸重量: 1,170 kg
- 重心許容範囲: 基準点後方 2.30 m 〜 2.50 m（両端を含む、離陸時・着陸時とも）

アーム表:
- 機体（自重720kg）: 2.45 m
- 前席: 2.00 m / 後席: 3.00 m / 燃料タンク: 2.30 m / 手荷物室: 3.50 m
"""

ARM_EMPTY, W_EMPTY = 2.45, 720
ARM_FRONT, ARM_REAR, ARM_FUEL, ARM_BAG = 2.00, 3.00, 2.30, 3.50
MTOW = 1170
CG_FWD, CG_AFT = 2.30, 2.50


def cg(items):
    """items: [(weight, arm), ...] -> (total_weight, cg)"""
    w = sum(i[0] for i in items)
    m = sum(i[0] * i[1] for i in items)
    return w, m / w


def verify_q1():
    """問1: 前席140kg・後席60kg・燃料60kg・手荷物20kg の重心位置"""
    items = [(W_EMPTY, ARM_EMPTY), (140, ARM_FRONT), (60, ARM_REAR),
             (60, ARM_FUEL), (20, ARM_BAG)]
    w, g = cg(items)
    assert w == 1000, f"総重量が想定と不一致: {w}"
    assert abs(g - 2.432) < 1e-9, f"重心位置が想定と不一致: {g}"
    assert w <= MTOW and CG_FWD <= g <= CG_AFT, "問1の搭載状態が運用限界外"
    rounded = round(g, 2)  # 2.43
    # 距離のある選択肢群の中で正解が一意であることを確認
    options = [2.41, 2.43, 2.45, 2.47, 2.65]  # 正解(2)=2.43
    matches = [o for o in options if abs(o - rounded) < 0.005]
    assert matches == [2.43], f"問1の正解が一意でない: {matches}"
    print(f"問1 OK: 総重量={w}kg 総モーメント={sum(i[0]*i[1] for i in items)}kg・m "
          f"重心={g:.3f}m → 四捨五入 {rounded}m")
    return rounded


def verify_q2():
    """問2: 前席150kg・後席150kg・燃料100kg(着陸時20kg)で搭載できる手荷物の最大重量

    3つの制約（最大離陸重量 / 離陸時後方限界 / 着陸時後方限界）を
    手荷物重量Bを総当たりして検証し、最大値の一意性を確認する。
    """
    fixed = [(W_EMPTY, ARM_EMPTY), (150, ARM_FRONT), (150, ARM_REAR)]
    results = {}
    for b10 in range(0, 1001):  # 0.1kg刻みで0〜100kgを総当たり
        b = b10 / 10
        w_to, g_to = cg(fixed + [(100, ARM_FUEL), (b, ARM_BAG)] if b else fixed + [(100, ARM_FUEL)])
        w_ld, g_ld = cg(fixed + [(20, ARM_FUEL), (b, ARM_BAG)] if b else fixed + [(20, ARM_FUEL)])
        ok = (w_to <= MTOW
              and CG_FWD <= g_to <= CG_AFT
              and CG_FWD <= g_ld <= CG_AFT)
        results[b] = (ok, w_to, g_to, g_ld)
    feasible = [b for b, r in results.items() if r[0]]
    max_b = max(feasible)
    assert abs(max_b - 40.0) < 1e-9, f"最大手荷物重量が想定と不一致: {max_b}"
    # どの制約が支配的かを確認（40kg超で最初に破れるのは着陸時後方限界）
    ok41 = results[40.1]
    assert not ok41[0] and ok41[1] <= MTOW and ok41[2] <= CG_AFT, "着陸時制約が支配的でない"
    # 個別の限界値: MTOW→50kg, 離陸CG→56kg, 着陸CG→40kg
    lim_w = MTOW - (720 + 150 + 150 + 100)
    assert lim_w == 50
    # 離陸CG限界: 2744 + 3.5B <= 2.5(1120+B)
    lim_to = (2.5 * 1120 - 2744) / (3.5 - 2.5)
    assert abs(lim_to - 56) < 1e-9
    # 着陸CG限界: 2560 + 3.5B <= 2.5(1040+B)
    lim_ld = (2.5 * 1040 - 2560) / (3.5 - 2.5)
    assert abs(lim_ld - 40) < 1e-9
    b = 40
    _, g_to = cg(fixed + [(100, ARM_FUEL), (b, ARM_BAG)])
    _, g_ld = cg(fixed + [(20, ARM_FUEL), (b, ARM_BAG)])
    options = [20, 25, 30, 35, 40]  # 正解(5)=40
    matches = [o for o in options if abs(o - max_b) < 0.5]
    assert matches == [40], f"問2の正解が一意でない: {matches}"
    print(f"問2 OK: 最大手荷物={max_b}kg（制約別限界: 重量{lim_w}kg / 離陸CG{lim_to}kg / 着陸CG{lim_ld}kg）")
    print(f"  B=40kg時: 離陸重量={720+150+150+100+40}kg 離陸CG={g_to:.4f}m 着陸CG={g_ld:.4f}m")
    return max_b


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 問1・問2とも解は一意")
