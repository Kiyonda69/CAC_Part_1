"""
航大思考113 検証スクリプト
問1: 立方体展開図の対面特定（標準）
問2: 立方体の鏡像問題（高難度）
"""

# ===== 問1の検証 =====
# 展開図 (T字形 + 下方向に延長):
#       [P]
#    [Q][R][S]
#       [T]
#       [U]
#
# 折り畳み:
# - R = 前面 (基面)
# - P = 上面 (Rの上に折る)
# - Q = 左面 (Rの左に折る)
# - S = 右面 (Rの右に折る)
# - T = 下面 (Rの下に折る)
# - U = Tからさらに下に連結 → Tを下面として折ると、Uは更に折れて背面に回り込む

def verify_q1():
    # 立方体の各面 → 展開図のラベル
    cube = {
        '前面': 'R',
        '上面': 'P',
        '左面': 'Q',
        '右面': 'S',
        '下面': 'T',
        '背面': 'U',
    }
    # 対面ペア
    pairs = [('前面', '背面'), ('上面', '下面'), ('左面', '右面')]
    opposite = {}
    for a, b in pairs:
        opposite[cube[a]] = cube[b]
        opposite[cube[b]] = cube[a]

    # 質問: 面Uと向かい合う面は?
    target = 'U'
    answer = opposite[target]
    print(f"問1: 面{target}の対面は {answer}")
    assert answer == 'R', f"Expected R, got {answer}"

    # 選択肢: (1)Q (2)T (3)S (4)P (5)R
    options = {1: 'Q', 2: 'T', 3: 'S', 4: 'P', 5: 'R'}
    correct = [k for k, v in options.items() if v == answer]
    assert len(correct) == 1, f"複数正解: {correct}"
    print(f"問1 正解: ({correct[0]})")
    return correct[0]


# ===== 問2の検証 =====
# 展開図:
#       [S]
#    [H][P][R]
#       [W]
#       [Y]
#
# 折り畳み:
# - P = 前面 (基面)
# - S = 上面
# - H = 左面
# - R = 右面
# - W = 下面 (Pの直下)
# - Y = 背面 (Wの直下に連結 → 折ると背面)

def verify_q2():
    cube = {
        '前面': 'P',
        '上面': 'S',
        '左面': 'H',
        '右面': 'R',
        '下面': 'W',
        '背面': 'Y',
    }
    pairs = [('前面', '背面'), ('上面', '下面'), ('左面', '右面')]
    opposite = {}
    for a, b in pairs:
        opposite[cube[a]] = cube[b]
        opposite[cube[b]] = cube[a]
    print(f"問2 立方体: {cube}")
    print(f"問2 対面: {opposite}")

    # 鏡は立方体の左側に置かれ、目は右側にある
    # 鏡に映る立方体の像:
    # - 上面 (S) が反転して見える
    # - 前面 (P) が反転して見える
    # - 鏡が左に面しているため、左面 (H) が反転して見える (右面Rではない)
    expected_top = cube['上面']    # S
    expected_front = cube['前面']  # P
    expected_side = cube['左面']   # H (鏡が左にあるため左面が映る)
    print(f"鏡像で見える面: 上={expected_top}反転, 前={expected_front}反転, 横={expected_side}反転")

    # 選択肢:
    # (1) S反転, P反転, H反転 ← 正解
    # (2) S反転, P反転, R反転 (右面表示は誤り)
    # (3) S反転, P正,   H反転 (前面が反転されていない)
    # (4) S正,   P反転, H反転 (上面が反転されていない)
    # (5) S正,   P正,   H正   (反転なし)
    options = [
        {'top': ('S', True), 'front': ('P', True), 'side': ('H', True)},  # (1)
        {'top': ('S', True), 'front': ('P', True), 'side': ('R', True)},  # (2)
        {'top': ('S', True), 'front': ('P', False), 'side': ('H', True)},  # (3)
        {'top': ('S', False), 'front': ('P', True), 'side': ('H', True)},  # (4)
        {'top': ('S', False), 'front': ('P', False), 'side': ('H', False)},  # (5)
    ]
    correct_pattern = {
        'top': (expected_top, True),
        'front': (expected_front, True),
        'side': (expected_side, True),
    }
    matches = [i+1 for i, opt in enumerate(options) if opt == correct_pattern]
    assert len(matches) == 1, f"複数正解または0個: {matches}"
    print(f"問2 正解: ({matches[0]})")
    return matches[0]


if __name__ == '__main__':
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"\n=== 最終結果 ===")
    print(f"問1正解: ({a1})")
    print(f"問2正解: ({a2})")
    assert a1 == 5, f"問1正解は(5)を想定: 実際は({a1})"
    assert a2 == 1, f"問2正解は(1)を想定: 実際は({a2})"
    print("検証成功: 想定通り")
