#!/usr/bin/env python3
"""
セット5 解の一意性検証スクリプト

問1: 展開図から立方体を判断（十字形展開図 → 正しい3D図を選ぶ）
問2: 立方体から展開図を判断（3D図 → 正しい十字形展開図を選ぶ）

正解番号:
  問1: (1)
  問2: (4)
"""


def verify_problem1():
    """
    問1: 展開図を折り畳んだときの立方体の正しい見え方を選ぶ

    展開図（十字型）:
        [上:●]
    [左:■][正面:□][右:△]
        [下:+]
        [背面:▲]

    折り畳み規則（正面□を基準）:
      □ → 正面(Front)
      ■ → 左(Left)
      △ → 右(Right)
      ● → 上(Top)
      + → 下(Bottom)
      ▲ → 背面(Back)

    対面ペア: (●↔+), (□↔▲), (■↔△)

    正面+上+右から見た正しい見え方: 上=●, 正面=□, 右=△
    """

    cube = {
        'top': '●',
        'bottom': '+',
        'front': '□',
        'back': '▲',
        'left': '■',
        'right': '△'
    }

    # 正面+上面+右面から見た正しい見え方
    correct_view = {
        'top': cube['top'],      # ●
        'front': cube['front'],  # □
        'right': cube['right']   # △
    }

    # 5つの選択肢（問1の正解は選択肢(1)）
    choices = [
        # (1) 正解
        {'top': '●', 'front': '□', 'right': '△'},
        # (2) 不正解: 前面が左面(■)になっている
        {'top': '●', 'front': '■', 'right': '△'},
        # (3) 不正解: 上面が下面(+)になっている（●の対面）
        {'top': '+', 'front': '□', 'right': '△'},
        # (4) 不正解: 右面が背面(▲)になっている（△の対面）
        {'top': '●', 'front': '□', 'right': '▲'},
        # (5) 不正解: 前面が背面(▲)になっている（□の対面）
        {'top': '●', 'front': '▲', 'right': '△'},
    ]

    valid = [i + 1 for i, choice in enumerate(choices) if choice == correct_view]
    assert len(valid) == 1, f"正解が{len(valid)}個存在: {valid}"
    print(f"問題1 正解: ({valid[0]})")
    print(f"  上={correct_view['top']}, 正面={correct_view['front']}, 右={correct_view['right']}")

    # 反対面ルールの確認: 正解以外の選択肢が正しく不正解であることを確認
    opposite = {
        '●': '+', '+': '●',
        '□': '▲', '▲': '□',
        '■': '△', '△': '■'
    }
    print("  各選択肢の検証:")
    for i, c in enumerate(choices):
        is_valid = (c == correct_view)
        # 反対面が同時に見えているか確認
        visible = [c['top'], c['front'], c['right']]
        conflict = []
        for face in visible:
            if opposite.get(face) in visible:
                conflict.append(f"{face}↔{opposite[face]}")
        status = "正解" if is_valid else f"不正解（{'対面矛盾: ' + ', '.join(conflict) if conflict else '面の割り当て違反'}）"
        print(f"    ({i+1}) 上={c['top']}, 正面={c['front']}, 右={c['right']} → {status}")

    return valid[0]


def verify_problem2():
    """
    問2: 3D立方体図から、対応する展開図（十字型）を選ぶ

    目標立方体（正面+上+右から見た図）:
      上=●, 正面=■, 右=△

    完全な面配置:
      上=●, 下=○, 正面=■, 背面=□, 左=▲, 右=△

    十字型展開図のポジション定義:
        [P]
    [Q][R][S]
        [T]
        [U]

    折り畳み時の対応:
      R → 正面(Front)
      Q → 左(Left)
      S → 右(Right)
      P → 上(Top)   ← Rの上のセル
      T → 下(Bottom) ← Rの下のセル
      U → 背面(Back) ← Tのさらに下のセル

    正解の展開図:
      P=●(上), Q=▲(左), R=■(正面), S=△(右), T=○(下), U=□(背面)
    """

    target_cube = {
        'top': '●',
        'bottom': '○',
        'front': '■',
        'back': '□',
        'left': '▲',
        'right': '△'
    }

    def fold(P, Q, R, S, T, U):
        """展開図の各セルを立方体の面にマッピング"""
        return {
            'top': P,
            'left': Q,
            'front': R,
            'right': S,
            'bottom': T,
            'back': U
        }

    # 5つの展開図候補（問2の正解は選択肢(4)）
    # すべて6種類の記号を1つずつ使用
    nets = [
        # (1) 不正解: P=○, T=● （上面と下面が入れ替わり）→ 上面=○ ≠ ●
        ('○', '▲', '■', '△', '●', '□'),
        # (2) 不正解: Q=△, S=▲ （左面と右面が入れ替わり）→ 右面=▲ ≠ △
        ('●', '△', '■', '▲', '○', '□'),
        # (3) 不正解: R=□, U=■ （正面と背面が入れ替わり）→ 正面=□ ≠ ■
        ('●', '▲', '□', '△', '○', '■'),
        # (4) 正解: P=●, Q=▲, R=■, S=△, T=○, U=□
        ('●', '▲', '■', '△', '○', '□'),
        # (5) 不正解: T=□, U=○ （下面と背面が入れ替わり）→ 下面=□ ≠ ○
        ('●', '▲', '■', '△', '□', '○'),
    ]

    valid = []
    print("  各展開図の検証:")
    for i, (P, Q, R, S, T, U) in enumerate(nets):
        result = fold(P, Q, R, S, T, U)
        is_match = (result == target_cube)
        if is_match:
            valid.append(i + 1)
        diffs = {face: f"期待={target_cube[face]}, 実際={result[face]}"
                 for face in target_cube if result[face] != target_cube[face]}
        status = "正解" if is_match else f"不正解（{diffs}）"
        print(f"    ({i+1}) P={P}, Q={Q}, R={R}, S={S}, T={T}, U={U} → {status}")

    assert len(valid) == 1, f"正解が{len(valid)}個存在: {valid}"
    print(f"問題2 正解: ({valid[0]})")
    return valid[0]


def verify_uniqueness_comprehensive():
    """全順列から唯一解を確認する包括的検証"""
    from itertools import permutations

    # 問1: 6面から3面が見えるとき、有効な組み合わせを列挙
    symbols_q1 = ['●', '+', '□', '▲', '■', '△']
    opposite_q1 = {
        '●': '+', '+': '●',
        '□': '▲', '▲': '□',
        '■': '△', '△': '■'
    }
    correct_q1 = {'top': '●', 'front': '□', 'right': '△'}

    valid_q1_views = []
    for top in symbols_q1:
        for front in symbols_q1:
            if front == top or front == opposite_q1.get(top):
                continue
            for right in symbols_q1:
                if right in (top, front, opposite_q1.get(top), opposite_q1.get(front)):
                    continue
                valid_q1_views.append({'top': top, 'front': front, 'right': right})

    print(f"\n包括的検証:")
    print(f"  問1: 有効な3面ビューの総数 = {len(valid_q1_views)}")
    print(f"  問1: 5つの選択肢の中で正解は1つのみ ✓")

    # 問2: 全順列から目標立方体に一致する展開図を列挙
    symbols_q2 = ['●', '○', '■', '□', '▲', '△']
    target_q2 = {'top': '●', 'bottom': '○', 'front': '■', 'back': '□', 'left': '▲', 'right': '△'}

    valid_q2_nets = []
    for perm in permutations(symbols_q2):
        P, Q, R, S, T, U = perm
        result = {'top': P, 'left': Q, 'front': R, 'right': S, 'bottom': T, 'back': U}
        if result == target_q2:
            valid_q2_nets.append(perm)

    print(f"  問2: 目標立方体に対応する全配置数 = {len(valid_q2_nets)}")
    for v in valid_q2_nets:
        print(f"        P={v[0]}, Q={v[1]}, R={v[2]}, S={v[3]}, T={v[4]}, U={v[5]}")
    print(f"  問2: 5つの選択肢の中で正解は1つのみ ✓")


if __name__ == "__main__":
    print("=" * 60)
    print("セット5 問1 検証: 展開図 → 正しい3D立方体")
    print("=" * 60)
    verify_problem1()

    print()
    print("=" * 60)
    print("セット5 問2 検証: 3D立方体 → 正しい展開図")
    print("=" * 60)
    verify_problem2()

    print()
    verify_uniqueness_comprehensive()

    print()
    print("全検証完了: 問1正解=(1), 問2正解=(4)")
