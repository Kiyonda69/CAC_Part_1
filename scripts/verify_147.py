"""
航大思考147 解の一意性検証

問1: 4x3表のパターン認識（標準難度）
  - ルール: 各列で row1 = row4 となる対称性
  - 列内の差分の総和 = 最下行への戻りジャンプ

問2: 8セクター円の2進エンコーディング（高難度）
  - ルール: 各円は8セクター = 8ビット
  - セクターiは 2^i の値を持つ
  - 塗りつぶされたセクターの値の合計が表す数
"""


def verify_q1():
    """問1: 4×3表の空欄を求める。"""
    table = [
        [60, 35, 72],
        [40, 25, 50],
        [20, 15, 30],
        [60, None, 72],
    ]

    # ルール: 各列で row4 = row1（最下行は最上行と同じ）
    # 補助ルール: row3 から row4 へのジャンプ = row1 - row3
    candidates = []
    for guess in range(1, 100):
        # 空欄に値を入れて検証
        col2 = [table[0][1], table[1][1], table[2][1], guess]
        # ルール検証: row4 == row1 in each column
        valid = True
        for col_idx in range(3):
            if col_idx == 1:
                col = [table[0][1], table[1][1], table[2][1], guess]
            else:
                col = [row[col_idx] for row in table]
            if col[3] != col[0]:
                valid = False
                break
            # 補助検証: row1 - row3 == row4 - row3 (自明だが整合性確認)
            decrease_sum = (col[0] - col[1]) + (col[1] - col[2])
            jump_back = col[3] - col[2]
            if decrease_sum != jump_back:
                valid = False
                break
        if valid:
            candidates.append(guess)

    print(f"問1 候補: {candidates}")
    assert len(candidates) == 1, f"解が{len(candidates)}個存在: {candidates}"
    answer = candidates[0]
    print(f"問1 正解: ? = {answer}")
    assert answer == 35
    return answer


def verify_q2():
    """問2: 8セクター円で53を表現する。"""
    # 各セクター位置 i の値 = 2^i
    # セクターは円を8等分（12時方向から時計回り）
    # 1 = bit0 のみ（12時方向）
    # 2 = bit1 のみ（1〜2時方向）
    # 4 = bit2 のみ（3時方向）
    # 8 = bit3 のみ（4〜5時方向）
    # 16 = bit4 のみ（6時方向）
    # 32 = bit5 のみ（7〜8時方向）
    # 64 = bit6 のみ（9時方向）
    # 128 = bit7 のみ（10〜11時方向）

    # 1〜12 までの参照
    for n in range(1, 13):
        bits = [(n >> i) & 1 for i in range(8)]
        filled = [i for i, b in enumerate(bits) if b]
        print(f"  数値 {n:2d} = bits {bits} = sectors {filled}")

    # ターゲット: 53
    target = 53
    bits = [(target >> i) & 1 for i in range(8)]
    correct_sectors = tuple(i for i, b in enumerate(bits) if b)
    print(f"\n問2 ターゲット {target}: bits {bits}")
    print(f"問2 正解セクター: {correct_sectors}")
    # 53 = 32 + 16 + 4 + 1 = sectors 0, 2, 4, 5
    assert correct_sectors == (0, 2, 4, 5), f"想定外: {correct_sectors}"

    # 選択肢の値を計算（5択）
    options = {
        1: (0, 2, 4, 5),  # 53 (正解)
        2: (0, 1, 4, 5),  # 51
        3: (0, 2, 3, 5),  # 45
        4: (0, 2, 4, 6),  # 85
        5: (1, 2, 4, 5),  # 54
    }
    for k, secs in options.items():
        val = sum(2**i for i in secs)
        print(f"  選択肢({k}): sectors {secs} = {val}")

    # 一意性: 53 を表すのは選択肢(1)のみ
    matching = [k for k, secs in options.items() if secs == correct_sectors]
    assert len(matching) == 1, f"複数の選択肢が53を表す: {matching}"
    print(f"問2 正解選択肢: ({matching[0]})")
    return matching[0]


if __name__ == "__main__":
    print("=" * 50)
    print("問1 検証")
    print("=" * 50)
    a1 = verify_q1()
    print()
    print("=" * 50)
    print("問2 検証")
    print("=" * 50)
    a2 = verify_q2()
    print()
    print(f"最終結果: 問1=({a1}が空欄値), 問2=選択肢({a2})")
