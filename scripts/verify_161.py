"""
航大思考161: 折り紙穴あけ問題の検証

問1: 2回折り（縦→横）、1穴
問2: 2回折り（縦→横）、2穴
"""


def fold_unfold_one_hole(fold_pos, fold_lines):
    """
    折った紙に穴を開けたときの、開いた紙の穴位置を計算する

    fold_pos: (x, y) 折った紙上での穴位置
    fold_lines: 折り線のリスト [('v', x_line), ('h', y_line), ...] の順
                折る順序の逆順で適用してアンフォールドする

    Returns: 元の紙に開いた全ての穴位置の集合
    """
    holes = {fold_pos}
    # 折った逆順で展開
    for axis, line in reversed(fold_lines):
        new_holes = set()
        for hx, hy in holes:
            new_holes.add((hx, hy))
            if axis == 'v':
                # 縦折り線で対称
                new_holes.add((2 * line - hx, hy))
            elif axis == 'h':
                # 横折り線で対称
                new_holes.add((hx, 2 * line - hy))
        holes = new_holes
    return holes


def main():
    # 折りシーケンス: 縦に半分（x=2で右→左）、横に半分（y=2で下→上）
    fold_lines = [('v', 2.0), ('h', 2.0)]

    # 問1: 折った紙の (1.5, 0.5) 位置に穴
    print("=" * 50)
    print("問1: 折った紙の (1.5, 0.5) に穴")
    print("=" * 50)
    q1_holes = fold_unfold_one_hole((1.5, 0.5), fold_lines)
    print(f"穴の数: {len(q1_holes)}")
    print(f"穴の位置: {sorted(q1_holes)}")

    # 期待値: (1.5, 0.5), (2.5, 0.5), (1.5, 3.5), (2.5, 3.5)
    expected_q1 = {(1.5, 0.5), (2.5, 0.5), (1.5, 3.5), (2.5, 3.5)}
    assert q1_holes == expected_q1, f"問1の穴位置が想定と異なります: {q1_holes} vs {expected_q1}"
    print("問1: 検証OK\n")

    # 問2: 2つの穴
    print("=" * 50)
    print("問2: 折った紙の (0.5, 0.5) と (1.5, 1.5) に穴")
    print("=" * 50)
    q2_hole_a = fold_unfold_one_hole((0.5, 0.5), fold_lines)
    q2_hole_b = fold_unfold_one_hole((1.5, 1.5), fold_lines)
    q2_holes = q2_hole_a | q2_hole_b
    print(f"穴Aから: {sorted(q2_hole_a)}")
    print(f"穴Bから: {sorted(q2_hole_b)}")
    print(f"合計穴の数: {len(q2_holes)}")
    print(f"全穴位置: {sorted(q2_holes)}")

    expected_q2_a = {(0.5, 0.5), (3.5, 0.5), (0.5, 3.5), (3.5, 3.5)}
    expected_q2_b = {(1.5, 1.5), (2.5, 1.5), (1.5, 2.5), (2.5, 2.5)}
    expected_q2 = expected_q2_a | expected_q2_b
    assert q2_holes == expected_q2, f"問2の穴位置が想定と異なります"
    print("問2: 検証OK\n")

    # 各選択肢の比較（問1）
    print("=" * 50)
    print("問1: 5つの選択肢")
    print("=" * 50)
    choices_q1 = {
        1: {(0.5, 0.5), (3.5, 0.5), (0.5, 3.5), (3.5, 3.5)},  # 4隅
        2: {(0.5, 1.5), (0.5, 2.5), (3.5, 1.5), (3.5, 2.5)},  # 左右辺中央
        3: {(1.5, 0.5), (2.5, 0.5), (1.5, 3.5), (2.5, 3.5)},  # 上下辺中央 [正解]
        4: {(1.5, 1.5), (2.5, 1.5), (1.5, 2.5), (2.5, 2.5)},  # 中央クラスタ
        5: {(1.5, 0.5), (2.5, 0.5), (0.5, 3.5), (3.5, 3.5)},  # 非対称（誤り）
    }
    for i, choice in choices_q1.items():
        match = (choice == q1_holes)
        marker = " ★正解" if match else ""
        print(f"  ({i}): {len(choice)}穴 {sorted(choice)}{marker}")

    correct_count = sum(1 for c in choices_q1.values() if c == q1_holes)
    assert correct_count == 1, f"問1の正解が{correct_count}個あります"
    assert choices_q1[3] == q1_holes, "問1の正解は (3) であるべき"
    print("問1: 唯一解確認OK\n")

    # 各選択肢の比較（問2）
    print("=" * 50)
    print("問2: 5つの選択肢")
    print("=" * 50)
    choices_q2 = {
        1: expected_q2_a | expected_q2_b,  # 4隅+中央クラスタ [正解]
        2: expected_q2_a,  # 4隅のみ
        3: expected_q2_b,  # 中央クラスタのみ
        4: expected_q2_a | {(1.5, 0.5), (2.5, 0.5), (0.5, 1.5), (3.5, 1.5)},  # 4隅+異なる位置
        5: {(0.5, 0.5), (1.5, 0.5), (2.5, 0.5), (3.5, 0.5),
            (0.5, 3.5), (1.5, 3.5), (2.5, 3.5), (3.5, 3.5)},  # 上下行
    }
    for i, choice in choices_q2.items():
        match = (choice == q2_holes)
        marker = " ★正解" if match else ""
        print(f"  ({i}): {len(choice)}穴 {sorted(choice)}{marker}")

    correct_count = sum(1 for c in choices_q2.values() if c == q2_holes)
    assert correct_count == 1, f"問2の正解が{correct_count}個あります"
    assert choices_q2[1] == q2_holes, "問2の正解は (1) であるべき"
    print("問2: 唯一解確認OK\n")

    print("全ての検証が完了しました。")


if __name__ == "__main__":
    main()
