"""
航大思考112 検証スクリプト

問1: 立方体の展開図における向かい合う面の特定
問2: 立方体を指定の順序で転がした後の上面の文字

展開図:
       [A]
    [B][C][D]
       [E]
       [F]
"""


def fold_cube_from_net():
    """
    展開図を折り畳んで立方体を作る。
    展開図のCを前面（基面）として、各面の配置を計算する。

    戻り値: {'top': str, 'bottom': str, 'front': str,
             'back': str, 'right': str, 'left': str}

    折り畳み規則:
    - C (中央): 前面として固定
    - A (Cの上): 上面
    - B (Cの左): 左面
    - D (Cの右): 右面
    - E (Cの下): 下面
    - F (Eの下): Eを下面に折ると、Fはその先で折れて背面になる
    """
    cube = {
        'front':  'C',
        'top':    'A',
        'bottom': 'E',
        'left':   'B',
        'right':  'D',
        'back':   'F',
    }
    return cube


def opposite_pairs(cube):
    """立方体の対面ペアを返す"""
    return [
        tuple(sorted([cube['top'],   cube['bottom']])),
        tuple(sorted([cube['front'], cube['back']])),
        tuple(sorted([cube['left'],  cube['right']])),
    ]


def opposite_of(cube, letter):
    """指定した文字の対面を返す"""
    pairs = {
        cube['top']:    cube['bottom'],
        cube['bottom']: cube['top'],
        cube['front']:  cube['back'],
        cube['back']:   cube['front'],
        cube['left']:   cube['right'],
        cube['right']:  cube['left'],
    }
    return pairs[letter]


def roll_forward(cube):
    """
    立方体を前方（奥方向）に転がす。
    前下辺を軸に回転。
    - 前面 → 下面
    - 下面 → 背面
    - 背面 → 上面
    - 上面 → 前面
    - 左右は不変
    """
    return {
        'front':  cube['top'],
        'bottom': cube['front'],
        'back':   cube['bottom'],
        'top':    cube['back'],
        'left':   cube['left'],
        'right':  cube['right'],
    }


def roll_right(cube):
    """
    立方体を右方向に転がす。
    右下辺を軸に回転。
    - 右面 → 下面
    - 下面 → 左面
    - 左面 → 上面
    - 上面 → 右面
    - 前後は不変
    """
    return {
        'right':  cube['top'],
        'bottom': cube['right'],
        'left':   cube['bottom'],
        'top':    cube['left'],
        'front':  cube['front'],
        'back':   cube['back'],
    }


def verify_q1():
    """問1: Fの対面を求める"""
    cube = fold_cube_from_net()
    print("=== 問1 検証 ===")
    print(f"初期配置: {cube}")
    print(f"対面ペア: {opposite_pairs(cube)}")

    answer = opposite_of(cube, 'F')
    print(f"Fの対面: {answer}")

    # 対面ペア検証: A-E, B-D, C-F
    expected_pairs = [('A', 'E'), ('B', 'D'), ('C', 'F')]
    actual = sorted(opposite_pairs(cube))
    expected = sorted(expected_pairs)
    assert actual == expected, f"対面ペアが不正: {actual} != {expected}"

    assert answer == 'C', f"問1の答えが不正: {answer}"
    print("問1 OK: 正解は C")
    print()
    return answer


def verify_q2():
    """問2: 前方に1回、右に1回転がした後の上面の文字"""
    print("=== 問2 検証 ===")
    cube = fold_cube_from_net()
    print(f"初期配置: 上={cube['top']}, 前={cube['front']}, 右={cube['right']}")
    print(f"          下={cube['bottom']}, 後={cube['back']}, 左={cube['left']}")

    # 1回目: 前方に転がす
    cube = roll_forward(cube)
    print(f"\n前方1回後: 上={cube['top']}, 前={cube['front']}, 右={cube['right']}")
    print(f"            下={cube['bottom']}, 後={cube['back']}, 左={cube['left']}")
    assert cube['top'] == 'F' and cube['front'] == 'A' and cube['bottom'] == 'C'

    # 2回目: 右に転がす
    cube = roll_right(cube)
    print(f"\n右に1回後: 上={cube['top']}, 前={cube['front']}, 右={cube['right']}")
    print(f"            下={cube['bottom']}, 後={cube['back']}, 左={cube['left']}")

    answer = cube['top']
    print(f"\n最終上面: {answer}")

    # 対面ペアが保存されていることを確認
    final_pairs = sorted(opposite_pairs(cube))
    expected_pairs = [('A', 'E'), ('B', 'D'), ('C', 'F')]
    assert final_pairs == sorted(expected_pairs), f"対面ペアが変化: {final_pairs}"

    assert answer == 'B', f"問2の答えが不正: {answer}"
    print("問2 OK: 正解は B")
    print()
    return answer


def verify_uniqueness_q1():
    """問1の解が一意であることを確認 (全候補をチェック)"""
    cube = fold_cube_from_net()
    valid = []
    for candidate in ['A', 'B', 'C', 'D', 'E']:
        if opposite_of(cube, 'F') == candidate:
            valid.append(candidate)
    assert len(valid) == 1, f"問1の解が一意でない: {valid}"
    print(f"問1の解の一意性 OK: {valid[0]}")


def verify_uniqueness_q2():
    """問2の解が一意であることを確認"""
    cube = fold_cube_from_net()
    cube = roll_forward(cube)
    cube = roll_right(cube)
    valid = []
    for candidate in ['A', 'B', 'C', 'D', 'E', 'F']:
        if cube['top'] == candidate:
            valid.append(candidate)
    assert len(valid) == 1, f"問2の解が一意でない: {valid}"
    print(f"問2の解の一意性 OK: {valid[0]}")


if __name__ == '__main__':
    ans1 = verify_q1()
    ans2 = verify_q2()
    verify_uniqueness_q1()
    verify_uniqueness_q2()
    print("\n=== 最終結果 ===")
    print(f"問1 正解: {ans1}")
    print(f"問2 正解: {ans2}")
