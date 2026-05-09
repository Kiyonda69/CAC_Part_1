"""
航大思考163 検証スクリプト

Net layout (cross):
       [F1]
  [F2][F3][F4][F5]
       [F6]

When folded with F3 = front, F1 = top:
- top=F1, bottom=F6, front=F3, back=F5, left=F2, right=F4
- Opposite pairs: F1-F6, F2-F4, F3-F5
"""

# 6 symbols (用記号)
F1 = '●'   # filled circle  - top
F2 = '○'   # open circle    - left
F3 = '■'   # filled square  - front
F4 = '□'   # open square    - right
F5 = '▲'   # filled triangle - back
F6 = '△'   # open triangle  - bottom


def all_valid_orientations():
    """24通りの向き全列挙: (top, front, right)"""
    # 6 faces in 3 opposite pairs
    pairs = [(F1, F6), (F2, F4), (F3, F5)]
    valid = set()
    for tp_pair in range(3):
        for tp_side in range(2):
            top = pairs[tp_pair][tp_side]
            bottom = pairs[tp_pair][1 - tp_side]
            for ft_pair in range(3):
                if ft_pair == tp_pair:
                    continue
                for ft_side in range(2):
                    front = pairs[ft_pair][ft_side]
                    back = pairs[ft_pair][1 - ft_side]
                    for rt_pair in range(3):
                        if rt_pair == tp_pair or rt_pair == ft_pair:
                            continue
                        for rt_side in range(2):
                            right = pairs[rt_pair][rt_side]
                            left = pairs[rt_pair][1 - rt_side]
                            # 標準: top=F1,front=F3,right=F4 で右手系
                            # ハンドedness 検証: (top, front, right) が正しい
                            # 標準展開図: top=F1,front=F3 なら right=F4
                            # その他は標準からの回転で検証
                            if is_consistent(top, front, right):
                                valid.add((top, front, right))
    return valid


def is_consistent(top, front, right):
    """与えられた展開図と整合する向きか判定。
    標準: top=F1, front=F3, right=F4 から24通りの回転を生成して照合。"""
    # 立方体の標準状態
    state = {'top': F1, 'bottom': F6, 'front': F3, 'back': F5, 'left': F2, 'right': F4}

    def roll_forward(s):
        return {'top': s['back'], 'front': s['top'], 'bottom': s['front'],
                'back': s['bottom'], 'left': s['left'], 'right': s['right']}

    def roll_right(s):
        return {'top': s['left'], 'right': s['top'], 'bottom': s['right'],
                'left': s['bottom'], 'front': s['front'], 'back': s['back']}

    def rotate_z(s):  # 上から見て時計回り
        return {'top': s['top'], 'bottom': s['bottom'], 'front': s['left'],
                'right': s['front'], 'back': s['right'], 'left': s['back']}

    seen = set()
    stack = [state]
    while stack:
        s = stack.pop()
        key = (s['top'], s['front'], s['right'])
        if key in seen:
            continue
        seen.add(key)
        stack.append(roll_forward(s))
        stack.append(roll_right(s))
        stack.append(rotate_z(s))
    return (top, front, right) in seen


def check_problem1():
    """問1: 5つの (top, front, right) の中から、正しい組立を選ぶ"""
    choices = [
        (F1, F3, F2),   # (1) front=■, right=○ → 左右逆
        (F1, F4, F3),   # (2) front=□, right=■ → 左右逆 (front=□のとき right=▲のはず)
        (F1, F3, F5),   # (3) F3↔F5 は対面なので両方見えるのは不可
        (F1, F6, F4),   # (4) F1↔F6 は対面なので両方見えるのは不可
        (F1, F3, F4),   # (5) 標準向きで正解 ★
    ]
    valid_set = all_valid_orientations()
    print('=== 問1検証 ===')
    print(f'有効な向きの総数: {len(valid_set)} (期待: 24)')
    correct = []
    for i, c in enumerate(choices, 1):
        ok = c in valid_set
        print(f'  選択肢({i}) {c}: {"✓ 有効" if ok else "✗ 無効"}')
        if ok:
            correct.append(i)
    assert len(correct) == 1, f'唯一解でない: {correct}'
    assert correct[0] == 5, f'正解位置が5でない: {correct[0]}'
    print(f'問1 正解: ({correct[0]})')


def check_problem2():
    """問2: 立方体を 前→右→前 と転がしたとき、上面はどれか"""
    state = {'top': F1, 'bottom': F6, 'front': F3, 'back': F5, 'left': F2, 'right': F4}

    def roll_forward(s):
        return {'top': s['back'], 'front': s['top'], 'bottom': s['front'],
                'back': s['bottom'], 'left': s['left'], 'right': s['right']}

    def roll_right(s):
        return {'top': s['left'], 'right': s['top'], 'bottom': s['right'],
                'left': s['bottom'], 'front': s['front'], 'back': s['back']}

    print('=== 問2検証 ===')
    print(f'初期: {state}')
    s1 = roll_forward(state); print(f'前へ転がし後: {s1}')
    s2 = roll_right(s1);      print(f'右へ転がし後: {s2}')
    s3 = roll_forward(s2);    print(f'前へ転がし後: {s3}')
    answer_top = s3['top']
    print(f'最終的な上面: {answer_top}')

    choices = [F1, F2, F3, F6, F5]   # (1)● (2)○ (3)■ (4)△ (5)▲
    print(f'選択肢: {choices}')
    pos = choices.index(answer_top) + 1 if answer_top in choices else None
    print(f'正解位置: ({pos})')
    assert answer_top == F6, f'上面は△ではなく {answer_top}'
    assert pos == 4, f'正解位置が4でない: {pos}'


if __name__ == '__main__':
    check_problem1()
    print()
    check_problem2()
    print('\n全検証パス')
