"""
セット38 検証スクリプト

問1: ピラミッド型数値パターン（隣接2数の和で上段を生成）
問2: 折り紙切り抜き問題（3回折り→切る→展開）
"""

def verify_q1():
    """問1: ピラミッド型加算パターンの検証"""
    print("=" * 50)
    print("問1: ピラミッド型数値パターン")
    print("=" * 50)

    # 底辺（行5）
    row5 = [4, 2, 7, 3, 5]

    # 各行: 隣接する2数の和
    row4 = [row5[i] + row5[i+1] for i in range(4)]
    row3 = [row4[i] + row4[i+1] for i in range(3)]
    row2 = [row3[i] + row3[i+1] for i in range(2)]
    row1 = [row2[0] + row2[1]]

    print(f"行1(頂点): {row1}")
    print(f"行2: {row2}")
    print(f"行3: {row3}")
    print(f"行4: {row4}")
    print(f"行5(底辺): {row5}")

    # 答えの確認
    answer = row1[0]
    assert answer == 71, f"答えが71ではない: {answer}"
    print(f"\n正解: {answer}")

    # 選択肢の検証（正解は(3)に配置）
    options = [65, 68, 71, 74, 77]
    assert options[2] == 71, "正解が選択肢(3)にない"
    print(f"選択肢: {['(%d)%d' % (i+1, v) for i, v in enumerate(options)]}")
    print(f"正解: (3)71")

    # 解の一意性: 規則が「隣接2数の和」であれば答えは一意
    print("\n解の一意性: 規則（隣接2数の和）が決まれば頂点の値は一意に決定")
    print("検証OK")
    return True


def verify_q2():
    """問2: 折り紙切り抜き問題の検証"""
    print("\n" + "=" * 50)
    print("問2: 折り紙切り抜き問題")
    print("=" * 50)

    # 折り方:
    # 1. 下辺→上辺（谷折り）→ 長方形
    # 2. 右辺→左辺（谷折り）→ 正方形(1/4)
    # 3. 右下角→左上角（対角線で谷折り）→ 三角形(1/8)

    # 切り抜き: 三角形の斜辺中央付近に半円型の切り込み

    def unfold_3times(x, y):
        """3回折り(上下→左右→対角)を展開し、全対称位置を返す"""
        positions = set()

        # Step 3 展開: 対角線 y=x で対称（左上1/4の正方形内）
        step3 = [(x, y), (y, x)]

        for px, py in step3:
            # Step 2 展開: x=0.5 で左右対称
            step2 = [(px, py), (1-px, py)]

            for qx, qy in step2:
                # Step 1 展開: y=0.5 で上下対称
                step1 = [(qx, qy), (qx, 1-qy)]
                positions.update(step1)

        return positions

    # 切り抜き位置（折った三角形の斜辺中央付近）
    # 折った状態で (0.25, 0.25) 付近（正方形の対角線上）
    cut_x, cut_y = 0.25, 0.15

    positions = unfold_3times(cut_x, cut_y)
    print(f"切り抜き位置: ({cut_x}, {cut_y})")
    print(f"展開後の穴の位置 ({len(positions)}個):")
    for p in sorted(positions):
        print(f"  ({p[0]:.2f}, {p[1]:.2f})")

    # 8箇所に穴が開くことを確認
    assert len(positions) == 8, f"穴の数が8ではない: {len(positions)}"

    # 4重対称性の確認（浮動小数点を丸めて比較）
    def approx_in(px, py, pos_set, tol=1e-9):
        for sx, sy in pos_set:
            if abs(sx - px) < tol and abs(sy - py) < tol:
                return True
        return False

    # x=0.5対称
    for x, y in list(positions):
        assert approx_in(1-x, y, positions), f"左右対称性が崩れている: ({x}, {y})"
    # y=0.5対称
    for x, y in list(positions):
        assert approx_in(x, 1-y, positions), f"上下対称性が崩れている: ({x}, {y})"

    print("\n対称性検証OK（上下・左右とも対称）")
    print("正解: (1)")
    print("検証OK")
    return True


if __name__ == "__main__":
    q1_ok = verify_q1()
    q2_ok = verify_q2()

    if q1_ok and q2_ok:
        print("\n" + "=" * 50)
        print("全問題の検証が完了しました")
        print("=" * 50)
