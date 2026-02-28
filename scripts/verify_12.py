#!/usr/bin/env python3
"""
verify_12.py - 航大思考12 解の一意性検証

問1・問2の計器問題（方位・高度偏差計）について、
与えられた4つの表示状態から操作A, B, Cを一意に決定できることを検証する。

計器の読み方:
- 垂直線（方位偏差）:
    左に偏位 = 機体が設定方位より右にいる（左旋回で修正）
    中央     = 設定方位を適正に飛行している
    右に偏位 = 機体が設定方位より左にいる（右旋回で修正）
- 水平線（高度偏差）:
    上に偏位 = 機体が設定高度より低い（上昇で修正）
    中央     = 設定高度を適正に飛行している
    下に偏位 = 機体が設定高度より高い（降下で修正）

座標系:
- V: -1=左(L), 0=中央(C), +1=右(R)
- H: +1=上(U), 0=中央(C), -1=下(D)

操作と計器への影響（操作により機体が動く方向と反対に指示線がシフト）:
- 左旋回: V +1（右にシフト）, H 変化なし
- 右旋回: V -1（左にシフト）, H 変化なし
- 上昇:   V 変化なし, H -1（下にシフト）
- 降下:   V 変化なし, H +1（上にシフト）
- 組み合わせは加算
"""


def apply_operation(state, dv, dh):
    """操作を適用して新しい状態を返す（-1〜+1にクランプ）"""
    v, h = state
    new_v = max(-1, min(1, v + dv))
    new_h = max(-1, min(1, h + dh))
    return (new_v, new_h)


def find_solutions(displays):
    """与えられた4表示から有効な操作の組み合わせをすべて返す"""
    D1, D2, D3, D4 = displays

    # 操作一覧: (名前, ΔV, ΔH)
    operations = [
        ("左旋回", +1, 0),
        ("右旋回", -1, 0),
        ("上昇", 0, -1),
        ("降下", 0, +1),
        ("左旋回しながら上昇", +1, -1),
        ("左旋回しながら降下", +1, +1),
        ("右旋回しながら上昇", -1, -1),
        ("右旋回しながら降下", -1, +1),
    ]

    valid_solutions = []

    for op_A in operations:
        state_after_A = apply_operation(D1, op_A[1], op_A[2])
        if state_after_A != D2:
            continue

        for op_B in operations:
            state_after_B = apply_operation(D2, op_B[1], op_B[2])
            if state_after_B != D3:
                continue

            for op_C in operations:
                state_after_C = apply_operation(D3, op_C[1], op_C[2])
                if state_after_C != D4:
                    continue

                valid_solutions.append((op_A[0], op_B[0], op_C[0]))

    return valid_solutions


def main():
    print("=" * 60)
    print("航大思考12 解の一意性検証")
    print("=" * 60)

    # ===================== 問1 =====================
    # 設計方針: 極端値（±1）にある指示線変数は必ず次の操作で中央へ移動させる
    # → 飽和クランプによる曖昧さを排除
    print("\n【問1】（4表示・3操作）")
    print("表示1: V=左, H=中  （方位右偏・高度正）")
    print("表示2: V=中, H=下  （方位正・高度高い）")
    print("表示3: V=右, H=中  （方位左偏・高度正）")
    print("表示4: V=中, H=上  （方位正・高度低い）")

    # V: -1=L(左), 0=C(中), +1=R(右)
    # H: +1=U(上), 0=C(中), -1=D(下)
    D1_q1 = (-1, 0)   # V=L, H=C
    D2_q1 = (0, -1)   # V=C, H=D
    D3_q1 = (+1, 0)   # V=R, H=C
    D4_q1 = (0, +1)   # V=C, H=U

    solutions_q1 = find_solutions([D1_q1, D2_q1, D3_q1, D4_q1])
    print(f"\n有効解数: {len(solutions_q1)}")
    for sol in solutions_q1:
        print(f"  A={sol[0]}, B={sol[1]}, C={sol[2]}")

    assert len(solutions_q1) == 1, f"問1: 解が{len(solutions_q1)}個 (期待: 1個)"
    print("-> 唯一解確認 OK")

    # ===================== 問2 =====================
    # 問1の派生・高難度版: 5表示・4操作（A, B, C, D）
    # 同じ計器で操作が1つ多いため推論ステップが増加
    print("\n【問2】（5表示・4操作）")
    print("表示1: V=右, H=中  （方位左偏・高度正）")
    print("表示2: V=中, H=下  （方位正・高度高い）")
    print("表示3: V=左, H=中  （方位右偏・高度正）")
    print("表示4: V=中, H=上  （方位正・高度低い）")
    print("表示5: V=中, H=中  （方位正・高度正 = 適正飛行）")

    D1_q2 = (+1, 0)   # V=R, H=C
    D2_q2 = (0, -1)   # V=C, H=D
    D3_q2 = (-1, 0)   # V=L, H=C
    D4_q2 = (0, +1)   # V=C, H=U
    D5_q2 = (0, 0)    # V=C, H=C

    # 問2は4操作なので find_solutions を拡張して使用
    ops = [
        ("左旋回", +1, 0), ("右旋回", -1, 0),
        ("上昇", 0, -1), ("降下", 0, +1),
        ("左旋回しながら上昇", +1, -1), ("左旋回しながら降下", +1, +1),
        ("右旋回しながら上昇", -1, -1), ("右旋回しながら降下", -1, +1),
    ]

    solutions_q2 = []
    displays_q2 = [D1_q2, D2_q2, D3_q2, D4_q2, D5_q2]
    for oA in ops:
        s2 = apply_operation(D1_q2, oA[1], oA[2])
        if s2 != D2_q2:
            continue
        for oB in ops:
            s3 = apply_operation(D2_q2, oB[1], oB[2])
            if s3 != D3_q2:
                continue
            for oC in ops:
                s4 = apply_operation(D3_q2, oC[1], oC[2])
                if s4 != D4_q2:
                    continue
                for oD in ops:
                    s5 = apply_operation(D4_q2, oD[1], oD[2])
                    if s5 != D5_q2:
                        continue
                    solutions_q2.append((oA[0], oB[0], oC[0], oD[0]))

    print(f"\n有効解数: {len(solutions_q2)}")
    for sol in solutions_q2:
        print(f"  A={sol[0]}, B={sol[1]}, C={sol[2]}, D={sol[3]}")

    assert len(solutions_q2) == 1, f"問2: 解が{len(solutions_q2)}個 (期待: 1個)"
    print("-> 唯一解確認 OK")

    print("\n" + "=" * 60)
    print("全検証完了: 問1・問2とも唯一解が確認されました")
    print("=" * 60)

    print("\n【選択肢の正答確認】")
    print(f"問1 正解 -> A={solutions_q1[0][0]}, B={solutions_q1[0][1]}, C={solutions_q1[0][2]}")
    q2sol = solutions_q2[0]
    print(f"問2 正解 -> A={q2sol[0]}, B={q2sol[1]}, C={q2sol[2]}, D={q2sol[3]}")


if __name__ == "__main__":
    main()
