"""
verify_150.py - 航大思考150 解の一意性検証

問題内容: 飛行機の方位面・高度面表示計器
- 垂直線: 方位面（基準方位の鉛直断面）
- 水平線: 高度面（基準高度の水平断面）
- 中央の小さな四角: 飛行機（自機）

操作と表示の関係:
- 機首上げ: 飛行機が高度面より上昇 → 高度面（水平線）が下に移動
- 機首下げ: 飛行機が高度面より下降 → 高度面（水平線）が上に移動
- 右旋回: 飛行機が方位面より右へ → 方位面（垂直線）が左に移動
- 左旋回: 飛行機が方位面より左へ → 方位面（垂直線）が右に移動
"""


# 操作による線の移動方向 (delta_v, delta_h)
# delta_v > 0: 垂直線が右へ
# delta_h > 0: 水平線が下へ
OPERATIONS = {
    "機首上げ": (0, +1),  # 水平線が下に移動
    "機首下げ": (0, -1),  # 水平線が上に移動
    "右旋回": (-1, 0),    # 垂直線が左に移動
    "左旋回": (+1, 0),    # 垂直線が右に移動
}


def apply(state, op):
    dv, dh = OPERATIONS[op]
    return (state[0] + dv, state[1] + dh)


def verify_q1():
    """問1: 4表示・3操作"""
    # 観測された表示の位置 (V, H)
    # V: -1=左, 0=中央, 1=右
    # H: -1=上, 0=中央, 1=下
    displays = [
        (-1, -1),  # D1: V左, H上
        (-1,  0),  # D2: V左, H中央
        ( 0,  0),  # D3: V中央, H中央（適正）
        ( 0,  1),  # D4: V中央, H下
    ]

    # 全ての操作の組み合わせを試す
    valid = []
    ops = list(OPERATIONS.keys())
    for a in ops:
        for b in ops:
            for c in ops:
                state = displays[0]
                state = apply(state, a)
                if state != displays[1]:
                    continue
                state = apply(state, b)
                if state != displays[2]:
                    continue
                state = apply(state, c)
                if state != displays[3]:
                    continue
                valid.append((a, b, c))

    print("【問1】")
    print(f"  表示遷移: {displays}")
    print(f"  有効な操作列: {valid}")
    assert len(valid) == 1, f"問1: 解が{len(valid)}個存在"
    print(f"  正解: A={valid[0][0]}, B={valid[0][1]}, C={valid[0][2]}")
    print(f"  → 解は唯一に定まる ✓\n")
    return valid[0]


def verify_q2():
    """問2: 5表示・4操作"""
    # 5段階の位置を使用 (-2, -1, 0, +1, +2)
    displays = [
        (-1,  0),  # D1: V やや左, H 中央
        ( 0,  0),  # D2: V 中央, H 中央
        ( 0, -1),  # D3: V 中央, H やや上
        (-1, -1),  # D4: V やや左, H やや上
        (-1,  0),  # D5: V やや左, H 中央（D1と同じ）
    ]

    valid = []
    ops = list(OPERATIONS.keys())
    for a in ops:
        for b in ops:
            for c in ops:
                for d in ops:
                    state = displays[0]
                    state = apply(state, a)
                    if state != displays[1]:
                        continue
                    state = apply(state, b)
                    if state != displays[2]:
                        continue
                    state = apply(state, c)
                    if state != displays[3]:
                        continue
                    state = apply(state, d)
                    if state != displays[4]:
                        continue
                    valid.append((a, b, c, d))

    print("【問2】")
    print(f"  表示遷移: {displays}")
    print(f"  有効な操作列: {valid}")
    assert len(valid) == 1, f"問2: 解が{len(valid)}個存在"
    print(f"  正解: A={valid[0][0]}, B={valid[0][1]}, C={valid[0][2]}, D={valid[0][3]}")
    print(f"  → 解は唯一に定まる ✓\n")
    return valid[0]


def verify_options_unique(question_label, displays, options):
    """選択肢のうち1つだけが観測表示を再現することを確認"""
    correct = []
    for idx, ops_seq in enumerate(options, start=1):
        state = displays[0]
        ok = True
        for i, op in enumerate(ops_seq):
            state = apply(state, op)
            if state != displays[i + 1]:
                ok = False
                break
        if ok:
            correct.append(idx)
    print(f"【{question_label} 選択肢検証】")
    print(f"  観測表示を再現する選択肢: {correct}")
    assert len(correct) == 1, f"{question_label}: {len(correct)}個の選択肢が一致"
    print(f"  → 正解番号: ({correct[0]}) のみが一致 ✓\n")
    return correct[0]


if __name__ == "__main__":
    q1_answer = verify_q1()
    q2_answer = verify_q2()

    # 問1選択肢
    q1_displays = [(-1, -1), (-1, 0), (0, 0), (0, 1)]
    q1_options = [
        ("機首下げ", "左旋回", "機首上げ"),
        ("機首上げ", "左旋回", "機首上げ"),  # 正解
        ("機首上げ", "右旋回", "機首上げ"),
        ("機首上げ", "左旋回", "機首下げ"),
        ("機首下げ", "右旋回", "機首下げ"),
    ]
    q1_correct = verify_options_unique("問1", q1_displays, q1_options)
    assert q1_correct == 2

    # 問2選択肢
    q2_displays = [(-1, 0), (0, 0), (0, -1), (-1, -1), (-1, 0)]
    q2_options = [
        ("右旋回", "機首下げ", "左旋回", "機首上げ"),
        ("左旋回", "機首上げ", "右旋回", "機首下げ"),
        ("左旋回", "機首下げ", "右旋回", "機首上げ"),  # 正解
        ("右旋回", "機首上げ", "左旋回", "機首下げ"),
        ("左旋回", "機首下げ", "左旋回", "機首上げ"),
    ]
    q2_correct = verify_options_unique("問2", q2_displays, q2_options)
    assert q2_correct == 3

    print("=" * 50)
    print("すべての検証に合格")
    print(f"問1正解: ({q1_correct})  問2正解: ({q2_correct})")
