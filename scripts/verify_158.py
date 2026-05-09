#!/usr/bin/env python3
"""
航大思考158 解の一意性検証

問1: 6色で塗られたサイコロの3視点から「赤の裏側」を推理する
問2: 同じサイコロを2回転がした後の上面・前面の色を求める

サイコロの面: 上(top), 下(bottom), 前(front), 後(back), 左(left), 右(right)
6色: 赤(R), 青(B), 黄(Y), 緑(G), 白(W), 黒(K)
"""

from itertools import permutations

COLORS = ['R', 'B', 'Y', 'G', 'W', 'K']  # 赤,青,黄,緑,白,黒

# サイコロの隣接関係: 各面と隣接する4面
# 標準的なサイコロでは、(top,bottom), (front,back), (left,right) が対面
# 隣接 = 対面でない
def is_opposite(face1, face2):
    pairs = [('top', 'bottom'), ('front', 'back'), ('left', 'right')]
    for a, b in pairs:
        if {face1, face2} == {a, b}:
            return True
    return False

def get_adjacents(face):
    all_faces = ['top', 'bottom', 'front', 'back', 'left', 'right']
    return [f for f in all_faces if f != face and not is_opposite(f, face)]


def verify_problem_1():
    """
    問1: 3視点から赤の裏側を推理する

    視点1: 上=赤, 前=白, 右=黄
    視点2: 上=青, 前=白, 右=緑
    視点3: 上=黒, 前=黄, 右=青

    各視点は同じサイコロを別の角度から見たもの。
    赤の対面の色を一意に決定できるか検証する。
    """
    # サイコロは6色を6面に塗り分ける順列で表現
    # face_color[face] = color, face ∈ {top, bottom, front, back, left, right}
    valid_solutions = []
    faces = ['top', 'bottom', 'front', 'back', 'left', 'right']

    for perm in permutations(COLORS):
        coloring = dict(zip(faces, perm))

        # 各視点が、サイコロのある回転位置で実現可能かチェック
        # 視点i = (top_color, front_color, right_color)
        view1 = ('R', 'W', 'Y')
        view2 = ('B', 'W', 'G')
        view3 = ('K', 'Y', 'B')

        if not all(view_realizable(coloring, v) for v in [view1, view2, view3]):
            continue

        valid_solutions.append(coloring)

    # 全ての有効な塗り分けについて、赤の対面が唯一かチェック
    red_opposite_set = set()
    for sol in valid_solutions:
        # 赤の面を見つける
        red_face = [f for f, c in sol.items() if c == 'R'][0]
        # 赤の対面の色
        opposites = {'top': 'bottom', 'bottom': 'top',
                     'front': 'back', 'back': 'front',
                     'left': 'right', 'right': 'left'}
        red_opp_face = opposites[red_face]
        red_opposite_set.add(sol[red_opp_face])

    print(f"問1: 有効な塗り分け数 = {len(valid_solutions)}")
    print(f"問1: 赤の対面の色（候補）= {red_opposite_set}")
    assert len(red_opposite_set) == 1, f"赤の対面が一意でない: {red_opposite_set}"
    answer = list(red_opposite_set)[0]
    color_jp = {'R': '赤', 'B': '青', 'Y': '黄', 'G': '緑', 'W': '白', 'K': '黒'}
    print(f"問1: 正解 = 赤の裏側は{color_jp[answer]}")
    return valid_solutions[0]  # 任意の有効解を返す


def view_realizable(coloring, view):
    """
    与えられた塗り分けで、ある視点(top_color, front_color, right_color)が実現可能か判定。
    サイコロを24通りの向きに回転させて、いずれかが視点と一致するかを確認。
    """
    top_c, front_c, right_c = view

    # 全24通りの回転を列挙
    # (top, front, right) の組み合わせとして
    # 各面の色が view と一致するかチェック
    for orientation in get_24_orientations():
        t, f, r = orientation  # それぞれ元の面名
        if (coloring[t] == top_c and
            coloring[f] == front_c and
            coloring[r] == right_c):
            return True
    return False


def get_24_orientations():
    """
    サイコロの24通りの回転位置。
    各位置について(top面, front面, right面)が元のどの面に対応するかを返す。
    """
    # 原始: top=top, front=front, right=right
    # 6つの面を上にする × 4回転 = 24通り

    base_states = [
        # (top, front, right) - 元の面名
        ('top', 'front', 'right'),
        ('top', 'right', 'back'),
        ('top', 'back', 'left'),
        ('top', 'left', 'front'),

        ('bottom', 'front', 'left'),
        ('bottom', 'left', 'back'),
        ('bottom', 'back', 'right'),
        ('bottom', 'right', 'front'),

        ('front', 'top', 'left'),
        ('front', 'left', 'bottom'),
        ('front', 'bottom', 'right'),
        ('front', 'right', 'top'),

        ('back', 'top', 'right'),
        ('back', 'right', 'bottom'),
        ('back', 'bottom', 'left'),
        ('back', 'left', 'top'),

        ('left', 'top', 'front'),
        ('left', 'front', 'bottom'),
        ('left', 'bottom', 'back'),
        ('left', 'back', 'top'),

        ('right', 'top', 'back'),
        ('right', 'back', 'bottom'),
        ('right', 'bottom', 'front'),
        ('right', 'front', 'top'),
    ]
    return base_states


def verify_problem_2():
    """
    問2: 問1の塗り分けに従うサイコロを以下の操作で転がす。
    初期状態: 上=赤, 前=白, 右=黄
    操作①: 東方向に転がす（右側に倒す: top→right, right→bottom, bottom→left, left→top）
    操作②: 北方向に転がす（後ろ側に倒す: top→back, back→bottom, bottom→front, front→top）

    最終的な上面と前面の色を求める。
    """
    # 問1から決定された塗り分け
    # 視点1から: top=赤, front=白, right=黄
    # 対面ペア: 赤-青, 白-黒, 黄-緑（問1の解）
    # よって、初期状態: top=R, front=W, right=Y, bottom=B, back=K, left=G

    state = {'top': 'R', 'front': 'W', 'right': 'Y',
             'bottom': 'B', 'back': 'K', 'left': 'G'}

    # 操作①: 東に転がす
    # top→right, right→bottom, bottom→left, left→top
    new_state = {
        'top': state['left'],
        'right': state['top'],
        'bottom': state['right'],
        'left': state['bottom'],
        'front': state['front'],
        'back': state['back']
    }
    state = new_state
    print(f"操作①後: {state}")

    # 操作②: 北に転がす
    # top→back, back→bottom, bottom→front, front→top
    new_state = {
        'top': state['front'],
        'back': state['top'],
        'bottom': state['back'],
        'front': state['bottom'],
        'right': state['right'],
        'left': state['left']
    }
    state = new_state
    print(f"操作②後: {state}")

    color_jp = {'R': '赤', 'B': '青', 'Y': '黄', 'G': '緑', 'W': '白', 'K': '黒'}
    print(f"問2: 上面={color_jp[state['top']]}, 前面={color_jp[state['front']]}")
    return state['top'], state['front']


if __name__ == "__main__":
    print("=" * 50)
    print("問1の検証")
    print("=" * 50)
    sol = verify_problem_1()
    print(f"塗り分けの一例: {sol}")

    print()
    print("=" * 50)
    print("問2の検証")
    print("=" * 50)
    top, front = verify_problem_2()
    print(f"問2の答え: 上面={top}, 前面={front}")
