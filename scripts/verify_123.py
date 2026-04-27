#!/usr/bin/env python3
"""
航大思考123 - 飛行機計器の類題検証スクリプト
問1：3つの操作シーケンスから正しい組み合わせを推測
問2：4つの操作シーケンスから正しい組み合わせを推測
"""

def apply_op(state, op_vec):
    """操作を状態に適用（-1～1の範囲でクリップ）"""
    v, h = state
    dv, dh = op_vec
    new_v = max(-1, min(1, v + dv))
    new_h = max(-1, min(1, h + dh))
    return (new_v, new_h)


def verify_q1():
    """問1の検証：3つの操作シーケンスから正しい組み合わせを推測"""
    # 操作による状態変化ベクトル
    # 左旋回: V+1, 右旋回: V-1, 上昇: H+1, 降下: H-1
    operations = {
        "右旋回しながら上昇": (-1, 1),
        "左旋回しながら上昇": (1, 1),
        "右旋回しながら降下": (-1, -1),
        "左旋回しながら降下": (1, -1),
        "上昇": (0, 1),
        "降下": (0, -1),
    }

    # 問1の表示シーケンス：
    # 表示1 -- [A] --> 表示2 -- [B] --> 表示3 -- [C] --> 表示4
    displays_q1 = [
        (1, 0),     # 表示1：V=R, H=C
        (0, 1),     # 表示2：V=C, H=D
        (-1, 0),    # 表示3：V=L, H=C
        (0, -1),    # 表示4：V=C, H=U
    ]

    # 各操作パターンを総当たり検証
    valid_combinations = []

    for op_a in operations:
        state_after_a = apply_op(displays_q1[0], operations[op_a])
        if state_after_a != displays_q1[1]:
            continue

        for op_b in operations:
            state_after_b = apply_op(state_after_a, operations[op_b])
            if state_after_b != displays_q1[2]:
                continue

            for op_c in operations:
                state_after_c = apply_op(state_after_b, operations[op_c])
                if state_after_c != displays_q1[3]:
                    continue

                valid_combinations.append((op_a, op_b, op_c))

    assert len(valid_combinations) == 1, f"問1の解が{len(valid_combinations)}個存在"
    print(f"問1正解：A: {valid_combinations[0][0]} / B: {valid_combinations[0][1]} / C: {valid_combinations[0][2]}")
    return valid_combinations[0]


def verify_q2():
    """問2の検証：4つの操作シーケンスから正しい組み合わせを推測（高難度版）"""

    operations = {
        "右旋回しながら上昇": (-1, 1),
        "左旋回しながら上昇": (1, 1),
        "右旋回しながら降下": (-1, -1),
        "左旋回しながら降下": (1, -1),
        "上昇": (0, 1),
        "降下": (0, -1),
    }

    # 問2の表示シーケンス：
    # 表示1 -- [A] --> 表示2 -- [B] --> 表示3 -- [C] --> 表示4 -- [D] --> 表示5
    displays_q2 = [
        (0, 1),     # 表示1：V=C, H=D
        (1, 1),     # 表示2：V=R, H=D
        (0, 0),     # 表示3：V=C, H=C
        (-1, -1),   # 表示4：V=L, H=U
        (0, 0),     # 表示5：V=C, H=C
    ]

    valid_combinations = []

    for op_a in operations:
        state_after_a = apply_op(displays_q2[0], operations[op_a])
        if state_after_a != displays_q2[1]:
            continue

        for op_b in operations:
            state_after_b = apply_op(state_after_a, operations[op_b])
            if state_after_b != displays_q2[2]:
                continue

            for op_c in operations:
                state_after_c = apply_op(state_after_b, operations[op_c])
                if state_after_c != displays_q2[3]:
                    continue

                for op_d in operations:
                    state_after_d = apply_op(state_after_c, operations[op_d])
                    if state_after_d != displays_q2[4]:
                        continue

                    valid_combinations.append((op_a, op_b, op_c, op_d))

    assert len(valid_combinations) == 1, f"問2の解が{len(valid_combinations)}個存在"
    print(f"問2正解：A: {valid_combinations[0][0]} / B: {valid_combinations[0][1]} / C: {valid_combinations[0][2]} / D: {valid_combinations[0][3]}")
    return valid_combinations[0]


if __name__ == "__main__":
    print("=== 航大思考123 検証開始 ===\n")

    print("【問1】")
    sol_q1 = verify_q1()

    print("\n【問2】")
    sol_q2 = verify_q2()

    print("\n=== 検証完了：両問とも唯一解あり ===")
