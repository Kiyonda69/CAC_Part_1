"""航大思考172 解の一意性検証

問1: 2x2x2立方体から複数のブロックを取り除いた立体の3面図問題
問2: 3x2x2配列のブロック集合から作る立体の3面図問題

3面図 = 平面図(top, +z方向から見下ろし), 正面図(front, -y方向から), 側面図(right side, +x方向から)
各図は silhouette と "internal height transition lines" の両方で表現される。
ここでは「3面図」を、各セルにおけるブロックの「最高z(平面)」または
「最低高さ/最高高さ」のプロファイルで比較する。
"""

from itertools import product


def get_three_views(cubes, size_x, size_y, size_z):
    """立体（cubeの集合）から3面図を計算

    Returns:
        (top, front, side) のタプル
        top: dict[(x,y)] = max_z (-1 ifno cube)  - 平面図の高さプロファイル
        front: set of (x, z) - 正面silhouette
        side: set of (y, z) - 側面silhouette
    """
    # top view: for each (x,y), find max z of present cubes
    top = {}
    for x in range(size_x):
        for y in range(size_y):
            heights = [k for k in range(size_z) if (x, y, k) in cubes]
            top[(x, y)] = max(heights) + 1 if heights else 0  # height(layers)

    # front view: silhouette in (x, z)
    front = set()
    for x in range(size_x):
        for z in range(size_z):
            if any((x, y, z) in cubes for y in range(size_y)):
                front.add((x, z))

    # side view: silhouette in (y, z)
    side = set()
    for y in range(size_y):
        for z in range(size_z):
            if any((x, y, z) in cubes for x in range(size_x)):
                side.add((y, z))

    return top, front, side


def verify_problem_1():
    """問1: 2x2x2 立方体から複数を取り除いた立体の3面図問題

    正解の立体: 2x2x2から(0,1,1)と(1,1,1)を取り除いたもの（背面上部の辺を除去）
    残り6個。
    3面図:
      平面: 全(x,y)がheight>=1なので silhouette = 2x2
             ただし内部線で y=1 側が height=1, y=0 側が height=2 と区別
      正面: x∈{0,1}, z∈{0,1} すべてで何らかのキューブあり → 全2x2
      側面: (y=1,z=1)が空 → L-shape (top-right empty in side view)
    """
    size = 2
    all_cubes = list(product(range(size), repeat=3))

    # 正解の立体
    correct_cubes = set(all_cubes) - {(0, 1, 1), (1, 1, 1)}
    target_top, target_front, target_side = get_three_views(
        correct_cubes, size, size, size
    )

    print("【問1】正解の3面図:")
    print(f"  平面図(height profile): {target_top}")
    print(f"  正面図(filled cells x,z): {sorted(target_front)}")
    print(f"  側面図(filled cells y,z): {sorted(target_side)}")
    print()

    # 5つの選択肢
    candidates = {
        "A: back-top edge missing (0,1,1)(1,1,1) [正解]":
            set(all_cubes) - {(0, 1, 1), (1, 1, 1)},
        "B: front-top edge missing (0,0,1)(1,0,1)":
            set(all_cubes) - {(0, 0, 1), (1, 0, 1)},
        "C: right-top edge missing (1,0,1)(1,1,1)":
            set(all_cubes) - {(1, 0, 1), (1, 1, 1)},
        "D: left-top edge missing (0,0,1)(0,1,1)":
            set(all_cubes) - {(0, 0, 1), (0, 1, 1)},
        "E: only back-right-top corner (1,1,1)":
            set(all_cubes) - {(1, 1, 1)},
    }

    matches = []
    for name, cubes in candidates.items():
        top, front, side = get_three_views(cubes, size, size, size)
        if top == target_top and front == target_front and side == target_side:
            matches.append(name)
            print(f"  ✓ MATCH: {name}")
        else:
            diffs = []
            if top != target_top:
                diffs.append(f"top differs")
            if front != target_front:
                diffs.append(f"front differs")
            if side != target_side:
                diffs.append(f"side differs")
            print(f"    no  : {name}  ({', '.join(diffs)})")

    assert len(matches) == 1, f"問1: 一致する候補が{len(matches)}個（一意でない）"
    print(f"\n  → 一意解確認 ✓\n")


def verify_problem_2():
    """問2: 2x2x2 立方体から3つのキューブを取り除いた立体の3面図問題

    正解の立体: 2x2x2から(0,0,1),(1,0,1),(1,1,1)を取り除いたもの
    残り5個。
    3面図:
      平面:
        (0,0) height=1, (0,1) height=2, (1,0) height=1, (1,1) height=1
        silhouette = 2x2、内部線で (0,1) のみ height=2 と表示
      正面:
        (x=0,z=0)=(0,0,0)✓, (x=0,z=1)=(0,1,1)✓, (x=1,z=0)=(1,0,0)/(1,1,0)✓
        (x=1,z=1)=(1,0,1)❌(1,1,1)❌ → 空
        → L-shape (top-right empty)
      側面:
        (y=0,z=0)=(0,0,0)/(1,0,0)✓
        (y=0,z=1)=(0,0,1)❌(1,0,1)❌ → 空
        (y=1,z=0)=(0,1,0)/(1,1,0)✓
        (y=1,z=1)=(0,1,1)✓ → 埋
        → 凹/L-shape (top-left empty in side view, since y=0 is "left" of side view)
    """
    size = 2
    all_cubes = list(product(range(size), repeat=3))

    correct_removed = {(0, 0, 1), (1, 0, 1), (1, 1, 1)}
    correct_cubes = set(all_cubes) - correct_removed
    target_top, target_front, target_side = get_three_views(
        correct_cubes, size, size, size
    )

    print("【問2】正解の3面図:")
    print(f"  平面図(height profile): {target_top}")
    print(f"  正面図(filled cells x,z): {sorted(target_front)}")
    print(f"  側面図(filled cells y,z): {sorted(target_side)}")
    print()

    candidates = {
        "A: remove (0,0,1)(1,0,1)(1,1,1) [正解]":
            set(all_cubes) - {(0, 0, 1), (1, 0, 1), (1, 1, 1)},
        "B: remove (0,1,1)(1,0,1)(1,1,1) [back-top+right-top-front]":
            set(all_cubes) - {(0, 1, 1), (1, 0, 1), (1, 1, 1)},
        "C: remove (0,0,1)(0,1,1)(1,1,1) [left-top+back-top-right]":
            set(all_cubes) - {(0, 0, 1), (0, 1, 1), (1, 1, 1)},
        "D: remove (0,0,1)(1,0,1)(0,1,1) [front-top+left-top-back]":
            set(all_cubes) - {(0, 0, 1), (1, 0, 1), (0, 1, 1)},
        "E: remove (1,0,1)(1,1,1) only [right-top edge only]":
            set(all_cubes) - {(1, 0, 1), (1, 1, 1)},
    }

    matches = []
    for name, cubes in candidates.items():
        top, front, side = get_three_views(cubes, size, size, size)
        if top == target_top and front == target_front and side == target_side:
            matches.append(name)
            print(f"  ✓ MATCH: {name}")
        else:
            diffs = []
            if top != target_top:
                diffs.append(f"top differs: got {top}")
            if front != target_front:
                diffs.append(f"front differs: got {sorted(front)}")
            if side != target_side:
                diffs.append(f"side differs: got {sorted(side)}")
            print(f"    no  : {name}")
            for d in diffs:
                print(f"        {d}")

    assert len(matches) == 1, f"問2: 一致する候補が{len(matches)}個（一意でない）"
    print(f"\n  → 一意解確認 ✓\n")


if __name__ == "__main__":
    verify_problem_1()
    verify_problem_2()
    print("==== 全問題で解の一意性を確認 ====")
