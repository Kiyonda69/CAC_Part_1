"""
航大思考92 - サイコロ転がし問題の検証
問1: 標準難度（8回転がし）
問2: 高難度（13回転がし + 底面を問う）
"""

def roll_die(state, direction):
    """
    サイコロを指定方向に転がす
    state: (top, bottom, front, back, right, left)
    front = 北(奥)方向, right = 東(右)方向
    """
    top, bottom, front, back, right, left = state

    if direction == 'E':  # 東（右）に転がす
        return (left, right, front, back, top, bottom)
    elif direction == 'W':  # 西（左）に転がす
        return (right, left, front, back, bottom, top)
    elif direction == 'N':  # 北（奥）に転がす
        return (back, front, top, bottom, right, left)
    elif direction == 'S':  # 南（手前）に転がす
        return (front, back, bottom, top, right, left)
    else:
        raise ValueError(f"Unknown direction: {direction}")


def simulate_path(initial_state, directions):
    """パスに沿ってサイコロを転がし、各ステップの状態を返す"""
    states = [initial_state]
    state = initial_state
    for d in directions:
        state = roll_die(state, d)
        states.append(state)
    return states


def verify_problem1():
    """
    問1: 標準難度サイコロ転がし

    初期状態: 上面=1, 正面(北)=2, 右面(東)=3
    → bottom=6, back=5, left=4

    経路: S(0,0) → N → E → E → N → N → W → W → N → G
    8回転がし
    """
    # 初期状態: (top, bottom, front, back, right, left)
    # top=1, bottom=6, front(N)=2, back(S)=5, right(E)=3, left(W)=4
    initial = (1, 6, 2, 5, 3, 4)

    # 経路の定義
    # グリッド座標での経路:
    # S(0,0) → (0,1)N → (1,1)E → (2,1)E → (2,2)N → (1,2)W → (1,3)N → (0,3)W → (0,4)N = G
    path = ['N', 'E', 'E', 'N', 'W', 'N', 'W', 'N']

    states = simulate_path(initial, path)

    print("=" * 50)
    print("問1: サイコロ転がし（標準）")
    print("=" * 50)
    print(f"初期状態: top={initial[0]}, bottom={initial[1]}, front={initial[2]}, back={initial[3]}, right={initial[4]}, left={initial[5]}")
    print(f"経路: {' → '.join(path)}")
    print()

    # 各ステップの座標と状態
    positions = [(0,0)]
    x, y = 0, 0
    for d in path:
        if d == 'N': y += 1
        elif d == 'S': y -= 1
        elif d == 'E': x += 1
        elif d == 'W': x -= 1
        positions.append((x, y))

    for i, (state, pos) in enumerate(zip(states, positions)):
        top, bottom, front, back, right, left = state
        if i == 0:
            label = "Start(S)"
        elif i == len(states) - 1:
            label = "Goal(G)"
        else:
            label = f"Step {i}"
        print(f"  {label} {pos}: top={top}, bottom={bottom}, front={front}, back={back}, right={right}, left={left}")

    final_top = states[-1][0]
    print(f"\n最終上面: {final_top}")

    # 検証: 対面の和が常に7
    for i, state in enumerate(states):
        top, bottom, front, back, right, left = state
        assert top + bottom == 7, f"Step {i}: top+bottom={top+bottom}"
        assert front + back == 7, f"Step {i}: front+back={front+back}"
        assert right + left == 7, f"Step {i}: right+left={right+left}"
    print("検証OK: 全ステップで対面の和=7")

    return final_top


def verify_problem2():
    """
    問2: 高難度サイコロ転がし

    初期状態: 上面=3, 正面(北)=1, 右面(東)=2
    → bottom=4, back=6, left=5

    経路: より複雑な蛇行パス（13回転がし）
    S(0,0) → E → E → E → N → W → W → N → N → E → E → N → W → W → G

    問い: ゴール地点での底面の数
    """
    # 初期状態: (top, bottom, front, back, right, left)
    # top=3, bottom=4, front(N)=1, back(S)=6, right(E)=2, left(W)=5
    initial = (3, 4, 1, 6, 2, 5)

    # 検証: 有効な標準サイコロ配置か
    top, bottom, front, back, right, left = initial
    assert top + bottom == 7
    assert front + back == 7
    assert right + left == 7

    # 経路の定義 (蛇行パス)
    # S(0,0) → (1,0)E → (2,0)E → (3,0)E → (3,1)N → (2,1)W → (1,1)W → (1,2)N → (1,3)N → (2,3)E → (3,3)E → (3,4)N → (2,4)W → (1,4)W = G
    path = ['E', 'E', 'E', 'N', 'W', 'W', 'N', 'N', 'E', 'E', 'N', 'W', 'W']

    states = simulate_path(initial, path)

    print("\n" + "=" * 50)
    print("問2: サイコロ転がし（高難度）")
    print("=" * 50)
    print(f"初期状態: top={initial[0]}, bottom={initial[1]}, front={initial[2]}, back={initial[3]}, right={initial[4]}, left={initial[5]}")
    print(f"経路: {' → '.join(path)}")
    print()

    positions = [(0,0)]
    x, y = 0, 0
    for d in path:
        if d == 'N': y += 1
        elif d == 'S': y -= 1
        elif d == 'E': x += 1
        elif d == 'W': x -= 1
        positions.append((x, y))

    for i, (state, pos) in enumerate(zip(states, positions)):
        top, bottom, front, back, right, left = state
        if i == 0:
            label = "Start(S)"
        elif i == len(states) - 1:
            label = "Goal(G)"
        else:
            label = f"Step {i:2d}"
        print(f"  {label} {pos}: top={top}, bottom={bottom}, front={front}, back={back}, right={right}, left={left}")

    final_bottom = states[-1][1]
    print(f"\n最終底面: {final_bottom}")

    # 検証
    for i, state in enumerate(states):
        top, bottom, front, back, right, left = state
        assert top + bottom == 7, f"Step {i}: top+bottom={top+bottom}"
        assert front + back == 7, f"Step {i}: front+back={front+back}"
        assert right + left == 7, f"Step {i}: right+left={right+left}"
    print("検証OK: 全ステップで対面の和=7")

    return final_bottom


if __name__ == "__main__":
    answer1 = verify_problem1()
    answer2 = verify_problem2()

    print("\n" + "=" * 50)
    print("最終結果")
    print("=" * 50)
    print(f"問1の正解（上面）: {answer1}")
    print(f"問2の正解（底面）: {answer2}")

    # 正解番号の割り当て
    # 問1: 正解を選択肢(5)に配置 → answer1の値を(5)に
    # 問2: 正解を選択肢(1)に配置 → answer2の値を(1)に
    print(f"\n問1: 選択肢(5)が正解 = {answer1}")
    print(f"問2: 選択肢(1)が正解 = {answer2}")

    # 選択肢の設計
    print("\n--- 選択肢設計 ---")
    all_faces = [1, 2, 3, 4, 5, 6]

    # 問1の選択肢（上面の値、5つから選ぶ）
    q1_wrong = [x for x in all_faces if x != answer1]
    import random
    random.shuffle(q1_wrong)
    q1_options = q1_wrong[:4]  # 4つの不正解
    q1_options.insert(4, answer1)  # 5番目（index 4）に正解を挿入
    print(f"問1選択肢: {['({}) {}'.format(i+1, v) for i, v in enumerate(q1_options)]}")

    # 問2の選択肢（底面の値、5つから選ぶ）
    q2_wrong = [x for x in all_faces if x != answer2]
    random.shuffle(q2_wrong)
    q2_options = [answer2] + q2_wrong[:4]  # 1番目に正解
    print(f"問2選択肢: {['({}) {}'.format(i+1, v) for i, v in enumerate(q2_options)]}")
