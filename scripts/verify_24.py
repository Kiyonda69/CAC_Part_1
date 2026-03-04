#!/usr/bin/env python3
"""
セット24: 飛行計器偏差計の類題 - 検証スクリプト

計器の読み方:
- 垂直線(V): L=機体が右偏, C=方位正, R=機体が左偏
- 水平線(H): U=機体が低い, C=高度正, D=機体が高い

操作と偏差線の変化:
- 左旋回: V が L→C→R 方向に移動
- 右旋回: V が R→C→L 方向に移動
- 上昇: H が U→C→D 方向に移動
- 降下: H が D→C→U 方向に移動
"""

def get_operation(v_from, v_to, h_from, h_to):
    """2つの表示間の操作を推定する"""
    # 垂直線の変化から旋回方向を判定
    v_moves = {
        ('L', 'C'): '左旋回',  # 右偏解消 → 左旋回
        ('C', 'R'): '左旋回',  # 左偏発生 → 左旋回
        ('R', 'C'): '右旋回',  # 左偏解消 → 右旋回
        ('C', 'L'): '右旋回',  # 右偏発生 → 右旋回
        ('C', 'C'): None,      # 方位変化なし
        ('L', 'L'): None,
        ('R', 'R'): None,
    }

    # 水平線の変化から高度操作を判定
    h_moves = {
        ('U', 'C'): '上昇',    # 低い → 正常 → 上昇した
        ('C', 'D'): '上昇',    # 正常 → 高い → 上昇した
        ('D', 'C'): '降下',    # 高い → 正常 → 降下した
        ('C', 'U'): '降下',    # 正常 → 低い → 降下した
        ('C', 'C'): None,      # 高度変化なし
        ('U', 'U'): None,
        ('D', 'D'): None,
    }

    turn = v_moves.get((v_from, v_to))
    altitude = h_moves.get((h_from, h_to))

    if turn and altitude:
        return f"{turn}しながら{altitude}"
    elif turn:
        return turn
    elif altitude:
        return altitude
    else:
        return "変化なし"


def verify_q1():
    """問1の検証: 4つの表示、3つの操作"""
    print("=" * 60)
    print("問1 検証")
    print("=" * 60)

    # 表示列: D1=(V=R,H=C), D2=(V=C,H=U), D3=(V=L,H=C), D4=(V=C,H=D)
    displays = [
        ('R', 'C'),  # 表示1
        ('C', 'U'),  # 表示2
        ('L', 'C'),  # 表示3
        ('C', 'D'),  # 表示4
    ]

    print("\n表示列:")
    for i, (v, h) in enumerate(displays):
        print(f"  表示{i+1}: V={v}, H={h}")

    # 各操作を導出
    operations = []
    labels = ['A', 'B', 'C']
    for i in range(len(displays) - 1):
        v_from, h_from = displays[i]
        v_to, h_to = displays[i + 1]
        op = get_operation(v_from, v_to, h_from, h_to)
        operations.append(op)
        print(f"\n操作{labels[i]}（表示{i+1}→表示{i+2}）:")
        print(f"  V: {v_from}→{v_to}, H: {h_from}→{h_to}")
        print(f"  → {op}")

    # 正解の確認
    expected = ["右旋回しながら降下", "右旋回しながら上昇", "左旋回しながら上昇"]
    for i, (op, exp) in enumerate(zip(operations, expected)):
        assert op == exp, f"操作{labels[i]}: 期待={exp}, 実際={op}"

    print("\n✓ 問1 全操作が正しいことを確認")
    return operations


def verify_q2():
    """問2の検証: 5つの表示、4つの操作"""
    print("\n" + "=" * 60)
    print("問2 検証")
    print("=" * 60)

    # 表示列: D1=(V=R,H=C), D2=(V=C,H=D), D3=(V=L,H=C), D4=(V=C,H=U), D5=(V=C,H=C)
    displays = [
        ('R', 'C'),  # 表示1
        ('C', 'D'),  # 表示2
        ('L', 'C'),  # 表示3
        ('C', 'U'),  # 表示4
        ('C', 'C'),  # 表示5
    ]

    print("\n表示列:")
    for i, (v, h) in enumerate(displays):
        print(f"  表示{i+1}: V={v}, H={h}")

    # 各操作を導出
    operations = []
    labels = ['A', 'B', 'C', 'D']
    for i in range(len(displays) - 1):
        v_from, h_from = displays[i]
        v_to, h_to = displays[i + 1]
        op = get_operation(v_from, v_to, h_from, h_to)
        operations.append(op)
        print(f"\n操作{labels[i]}（表示{i+1}→表示{i+2}）:")
        print(f"  V: {v_from}→{v_to}, H: {h_from}→{h_to}")
        print(f"  → {op}")

    # 正解の確認
    expected = ["右旋回しながら上昇", "右旋回しながら降下", "左旋回しながら降下", "上昇"]
    for i, (op, exp) in enumerate(zip(operations, expected)):
        assert op == exp, f"操作{labels[i]}: 期待={exp}, 実際={op}"

    print("\n✓ 問2 全操作が正しいことを確認")
    return operations


def verify_uniqueness():
    """各操作が一意に決まることを検証"""
    print("\n" + "=" * 60)
    print("解の一意性検証")
    print("=" * 60)

    # 問1の表示列
    q1_displays = [('R', 'C'), ('C', 'U'), ('L', 'C'), ('C', 'D')]
    # 問2の表示列
    q2_displays = [('R', 'C'), ('C', 'D'), ('L', 'C'), ('C', 'U'), ('C', 'C')]

    # 各遷移について、可能な操作は一意であることを確認
    for q_name, displays in [("問1", q1_displays), ("問2", q2_displays)]:
        print(f"\n{q_name}:")
        for i in range(len(displays) - 1):
            v_from, h_from = displays[i]
            v_to, h_to = displays[i + 1]
            op = get_operation(v_from, v_to, h_from, h_to)

            # V変化とH変化がそれぞれ一意の操作を示すことを確認
            v_key = (v_from, v_to)
            h_key = (h_from, h_to)

            # 不正な遷移（2ステップ）がないことを確認
            valid_v = [('L','C'),('C','R'),('R','C'),('C','L'),('C','C'),('L','L'),('R','R')]
            valid_h = [('U','C'),('C','D'),('D','C'),('C','U'),('C','C'),('U','U'),('D','D')]

            assert v_key in valid_v, f"不正なV遷移: {v_key}"
            assert h_key in valid_h, f"不正なH遷移: {h_key}"

            print(f"  遷移{i+1}→{i+2}: V({v_from}→{v_to}), H({h_from}→{h_to}) → {op} ✓")

    print("\n✓ 全遷移が有効であり、解は一意に決まる")


def verify_wrong_answers():
    """誤答選択肢が正解と異なることを検証"""
    print("\n" + "=" * 60)
    print("誤答選択肢の検証")
    print("=" * 60)

    # 問1 正解と選択肢
    q1_correct = ("右旋回しながら降下", "右旋回しながら上昇", "左旋回しながら上昇")
    q1_options = [
        ("左旋回しながら上昇", "左旋回しながら降下", "右旋回しながら降下"),       # (1) 全反転
        ("右旋回しながら上昇", "右旋回しながら降下", "左旋回しながら降下"),       # (2) 高度反転
        ("左旋回しながら降下", "左旋回しながら上昇", "右旋回しながら上昇"),       # (3) 旋回反転
        ("右旋回しながら降下", "左旋回しながら上昇", "右旋回しながら降下"),       # (4) 一部入替
    ]

    print("\n問1:")
    print(f"  正解: {q1_correct}")
    for i, opt in enumerate(q1_options):
        assert opt != q1_correct, f"選択肢({i+1})が正解と一致している"
        print(f"  ({i+1}): {opt} ≠ 正解 ✓")

    # 問2 正解と選択肢
    q2_correct = ("右旋回しながら上昇", "右旋回しながら降下", "左旋回しながら降下", "上昇")
    q2_options = [
        ("左旋回しながら降下", "左旋回しながら上昇", "右旋回しながら上昇", "降下"),       # (1) 全反転
        ("右旋回しながら降下", "右旋回しながら上昇", "左旋回しながら上昇", "降下"),       # (2) 高度反転
        ("左旋回しながら上昇", "左旋回しながら降下", "右旋回しながら降下", "上昇"),       # (3) 旋回反転
        ("右旋回しながら上昇", "左旋回しながら降下", "右旋回しながら降下", "降下"),       # (4) 一部入替
    ]

    print("\n問2:")
    print(f"  正解: {q2_correct}")
    for i, opt in enumerate(q2_options):
        assert opt != q2_correct, f"選択肢({i+1})が正解と一致している"
        print(f"  ({i+1}): {opt} ≠ 正解 ✓")

    print("\n✓ 全誤答選択肢が正解と異なることを確認")


if __name__ == "__main__":
    q1_ops = verify_q1()
    q2_ops = verify_q2()
    verify_uniqueness()
    verify_wrong_answers()
    print("\n" + "=" * 60)
    print("全検証完了 - セット24は正しく設計されています")
    print("=" * 60)
