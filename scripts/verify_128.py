"""
verify_128.py - 航大思考128 解の検証

問1: 三面図問題（立体の投影図）
問2: 直方体の断面問題
"""


def verify_q1():
    """
    問1: 三面図問題
    立体の構成:
      Block A: x:[2-4], z:[0-2], y:[0-3]  (右前・高い、幅2×奥行2×高さ3)
      Block B: x:[0-2], z:[0-4], y:[0-1]  (左全域・低い、幅2×奥行4×高さ1)
    """
    print("=" * 55)
    print("問1 検証: 三面図問題")
    print("=" * 55)

    # 立体の定義 (各ブロックを (x_min, x_max, z_min, z_max, y_max) で表現)
    block_A = {"x": (2, 4), "z": (0, 2), "y": (0, 3)}
    block_B = {"x": (0, 2), "z": (0, 4), "y": (0, 1)}
    blocks = [block_A, block_B]

    # --- 上面図: x-z平面への投影 (y方向から見下ろす) ---
    print("\n[上面図 (真上から)] - x-z平面")
    print("各グリッドに材料があるかチェック:")
    top_view = {}
    for xi in range(4):
        for zi in range(4):
            has_material = False
            for b in blocks:
                if b["x"][0] <= xi < b["x"][1] and b["z"][0] <= zi < b["z"][1]:
                    has_material = True
            top_view[(xi, zi)] = has_material

    # L字形かチェック
    l_shape_expected = set()
    for xi in range(4):
        for zi in range(4):
            # Block Aの足跡: x:2-4, z:0-2
            # Block Bの足跡: x:0-2, z:0-4
            if (2 <= xi < 4 and 0 <= zi < 2) or (0 <= xi < 2 and 0 <= zi < 4):
                l_shape_expected.add((xi, zi))

    actual = {k for k, v in top_view.items() if v}
    assert actual == l_shape_expected, f"上面図不一致: {actual} != {l_shape_expected}"
    print("=> L字形 (x:[0-4]×z:[0-2] + x:[0-2]×z:[2-4]) ✓")

    # --- 正面図: x-y平面への投影 (z方向=アから見る) ---
    print("\n[正面図 (ア方向: z=0側から見る)] - x-y平面")
    for xi in range(4):
        max_height = 0
        for b in blocks:
            if b["x"][0] <= xi < b["x"][1]:
                max_height = max(max_height, b["y"][1])
        print(f"  x={xi}: 高さ = {max_height}")

    # 正面図: x:0-1,1 → 高さ1, x:2-3 → 高さ3
    assert all(
        max(b["y"][1] for b in blocks if b["x"][0] <= xi < b["x"][1]) == 1
        for xi in range(2)
    ), "正面図左半分の高さが1でない"
    assert all(
        max(b["y"][1] for b in blocks if b["x"][0] <= xi < b["x"][1]) == 3
        for xi in range(2, 4)
    ), "正面図右半分の高さが3でない"
    print("=> 左低(高さ1)・右高(高さ3) の階段形状 ✓")

    # --- 右側面図: z-y平面への投影 (x=+∞側から見る) ---
    print("\n[右側面図 (イ方向: x=+∞側から見る)] - z-y平面")
    for zi in range(4):
        max_height = 0
        for b in blocks:
            if b["z"][0] <= zi < b["z"][1]:
                max_height = max(max_height, b["y"][1])
        print(f"  z={zi}: 高さ = {max_height}")

    # 右側面図: z:0-1 → 高さ3, z:2-3 → 高さ1
    h_z0 = max(b["y"][1] for b in blocks if b["z"][0] <= 0 < b["z"][1])
    h_z2 = max(b["y"][1] for b in blocks if b["z"][0] <= 2 < b["z"][1])
    assert h_z0 == 3, f"前部(z=0)の高さが3でない: {h_z0}"
    assert h_z2 == 1, f"後部(z=2)の高さが1でない: {h_z2}"
    print("=> 前部(z:0-2)高さ3・後部(z:2-4)高さ1 の階段形状 ✓")

    print("\n[選択肢の確認]")
    print("(1) 4×3 全体の長方形              → 誤（高さが一定）")
    print("(2) 4×1 全体の長方形              → 誤（高さが一定）")
    print("(3) 後部が高い階段形状            → 誤（前後逆）")
    print("(4) 前部が高い階段形状 ← 正解     → ✓ (z:0-2高さ3, z:2-4高さ1)")
    print("(5) 前部1/4だけ高い階段形状       → 誤（比率が違う）")
    print("\n正解: 選択肢 (4) ✓")


def verify_q2():
    """
    問2: 直方体の断面問題
    直方体 ABCD-EFGH: AB=4, BC=3, AE=3
    P = 辺DH の中点, Q = 辺BF の中点
    3点 A, P, Q を含む平面で切断 → 断面形状は？
    """
    print("\n" + "=" * 55)
    print("問2 検証: 直方体の断面問題")
    print("=" * 55)

    # 頂点座標
    A = (0, 0, 0)
    B = (4, 0, 0)
    C = (4, 3, 0)
    D = (0, 3, 0)
    E = (0, 0, 3)
    F = (4, 0, 3)
    G = (4, 3, 3)
    H = (0, 3, 3)

    # 中点
    P = tuple((D[i] + H[i]) / 2 for i in range(3))  # DH中点 = (0, 3, 1.5)
    Q = tuple((B[i] + F[i]) / 2 for i in range(3))  # BF中点 = (4, 0, 1.5)

    print(f"P (辺DH の中点) = {P}")
    print(f"Q (辺BF の中点) = {Q}")

    # 平面の法線ベクトル AP × AQ
    AP = tuple(P[i] - A[i] for i in range(3))
    AQ = tuple(Q[i] - A[i] for i in range(3))

    normal = (
        AP[1] * AQ[2] - AP[2] * AQ[1],
        AP[2] * AQ[0] - AP[0] * AQ[2],
        AP[0] * AQ[1] - AP[1] * AQ[0],
    )
    print(f"\n法線ベクトル AP × AQ = {normal}")

    # すべての頂点と特殊点が平面上にあるか確認
    print("\n各点の平面方程式値 (0ならば平面上):")
    key_points = [("A", A), ("P", P), ("Q", Q), ("G", G)]
    for name, pt in key_points:
        val = sum(normal[i] * (pt[i] - A[i]) for i in range(3))
        status = "✓ (平面上)" if abs(val) < 1e-9 else "✗"
        print(f"  {name}{pt}: {val:.4f} {status}")

    # 断面が四角形 A-Q-G-P であることを確認
    print("\n断面の頂点: A → Q → G → P → A")

    # 平行四辺形チェック
    AQ_v = tuple(Q[i] - A[i] for i in range(3))
    PG_v = tuple(G[i] - P[i] for i in range(3))
    AP_v = tuple(P[i] - A[i] for i in range(3))
    QG_v = tuple(G[i] - Q[i] for i in range(3))

    print(f"\nAQ = {AQ_v}")
    print(f"PG = {PG_v}")
    aq_eq_pg = all(abs(AQ_v[i] - PG_v[i]) < 1e-9 for i in range(3))
    print(f"AQ = PG: {aq_eq_pg} => {'対辺平行・等長 ✓' if aq_eq_pg else '✗'}")

    print(f"\nAP = {AP_v}")
    print(f"QG = {QG_v}")
    ap_eq_qg = all(abs(AP_v[i] - QG_v[i]) < 1e-9 for i in range(3))
    print(f"AP = QG: {ap_eq_qg} => {'対辺平行・等長 ✓' if ap_eq_qg else '✗'}")

    assert aq_eq_pg and ap_eq_qg, "平行四辺形の条件を満たさない"

    # 長方形チェック (内積=0なら長方形)
    dot_product = sum(AQ_v[i] * AP_v[i] for i in range(3))
    print(f"\nAQ · AP = {dot_product:.4f}")
    print(f"長方形チェック: {'長方形' if abs(dot_product) < 1e-9 else '長方形ではない (一般の平行四辺形)'}")

    # 辺の長さ
    len_AQ = sum(x**2 for x in AQ_v) ** 0.5
    len_AP = sum(x**2 for x in AP_v) ** 0.5
    print(f"\n|AQ| = |PG| = {len_AQ:.4f}")
    print(f"|AP| = |QG| = {len_AP:.4f}")

    print("\n断面形状: 平行四辺形（parallelogram）= 選択肢(3)")

    print("\n[選択肢の確認]")
    print("(1) 三角形   → 誤（断面は4頂点A,Q,G,Pを持つ四角形）")
    print("(2) 台形     → 誤（対辺が両方とも平行なので台形ではない）")
    print("(3) 平行四辺形 ← 正解  → ✓ AQ//PG かつ AP//QG")
    print("(4) 長方形   → 誤（AQ·AP≠0 なので直角ではない）")
    print("(5) 六角形   → 誤（断面は四角形）")
    print("\n正解: 選択肢 (3) ✓")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 55)
    print("全検証完了: 問1=(4), 問2=(3)")
    print("=" * 55)
