"""
航大思考185 検証コード
問1: T字+下3連型展開図の対面特定
問2: 1-4-1型展開図の対面ペア組み合わせ特定
"""
def fold_cube(net):
    """
    展開図(辞書: {label: (col, row)})から、各面の立方体位置をマッピング。
    展開図上の隣接(上下左右)を90度回転で折りたたみ、
    各面の中心の3D法線ベクトルから top/bottom/front/back/left/right を判定する。

    座標系: x=右, y=上, z=手前
    基準面: 最初の面を z+方向(手前=front)に置く
    """
    labels = list(net.keys())
    positions = net
    # 基準面=最初の面、法線=(0,0,1)(手前向き)、up=(0,1,0), right=(1,0,0)
    start = labels[0]
    face_data = {start: {'normal': (0, 0, 1),
                          'up': (0, 1, 0),
                          'right': (1, 0, 0)}}

    # 幅優先で隣接面を折りたたむ
    queue = [start]
    visited = {start}
    while queue:
        cur = queue.pop(0)
        cx, cy = positions[cur]
        cur_n = face_data[cur]['normal']
        cur_u = face_data[cur]['up']
        cur_r = face_data[cur]['right']
        # 隣接候補
        for dx, dy, axis_dir in [(1, 0, 'right'), (-1, 0, 'left'),
                                  (0, 1, 'up'), (0, -1, 'down')]:
            target = None
            for lab, pos in positions.items():
                if pos == (cx + dx, cy + dy) and lab not in visited:
                    target = lab
                    break
            if target is None:
                continue
            # 折りたたみ: 隣接面は90度回転して立方体面になる
            # right方向の隣接 → cur面をrightを軸に-90度回転
            # left方向の隣接 → cur面をrightを軸に+90度回転(反対方向)
            # 軸はそれぞれの方向ベクトル
            neg = lambda v: tuple(-x for x in v)
            if axis_dir == 'right':
                new_n = cur_r
                new_r = neg(cur_n)
                new_u = cur_u
            elif axis_dir == 'left':
                new_n = neg(cur_r)
                new_r = cur_n
                new_u = cur_u
            elif axis_dir == 'up':
                new_n = cur_u
                new_u = neg(cur_n)
                new_r = cur_r
            else:  # down
                new_n = neg(cur_u)
                new_u = cur_n
                new_r = cur_r
            face_data[target] = {'normal': new_n, 'up': new_u, 'right': new_r}
            visited.add(target)
            queue.append(target)

    def normal_to_face(n):
        if n == (0, 0, 1): return 'front'
        if n == (0, 0, -1): return 'back'
        if n == (1, 0, 0): return 'right'
        if n == (-1, 0, 0): return 'left'
        if n == (0, 1, 0): return 'top'
        if n == (0, -1, 0): return 'bottom'
        return 'unknown'

    return {lab: normal_to_face(d['normal']) for lab, d in face_data.items()}


def opposite_pairs(face_map):
    """face_map: {label: cube_face} から対面ペアを抽出"""
    opp = {'top': 'bottom', 'bottom': 'top', 'front': 'back',
           'back': 'front', 'left': 'right', 'right': 'left'}
    pairs = set()
    items = list(face_map.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if opp[items[i][1]] == items[j][1]:
                pairs.add(tuple(sorted([items[i][0], items[j][0]])))
    return pairs


# --- 問1: T字+下3連型 ---
# 配置:
#   [A][B][C]
#      [D]
#      [E]
#      [F]
net1 = {'A': (0, 3), 'B': (1, 3), 'C': (2, 3),
        'D': (1, 2), 'E': (1, 1), 'F': (1, 0)}
fm1 = fold_cube(net1)
pairs1 = opposite_pairs(fm1)
print('問1 各面の立方体位置:', fm1)
print('問1 対面ペア:', pairs1)
# 期待: A-C, B-E, D-F
expected1 = {('A', 'C'), ('B', 'E'), ('D', 'F')}
assert pairs1 == expected1, f'問1の対面が想定と異なる: {pairs1}'
# 面Bの対面=E
print('問1 検証OK: Bの対面=', [p for p in pairs1 if 'B' in p])

# --- 問2: 1-4-1型 ---
# 配置:
#      [A]
#   [B][C][D][E]
#            [F]
net2 = {'A': (1, 2), 'B': (0, 1), 'C': (1, 1), 'D': (2, 1),
        'E': (3, 1), 'F': (3, 0)}
fm2 = fold_cube(net2)
pairs2 = opposite_pairs(fm2)
print('問2 各面の立方体位置:', fm2)
print('問2 対面ペア:', pairs2)
# 期待: A-F, B-D, C-E
expected2 = {('A', 'F'), ('B', 'D'), ('C', 'E')}
assert pairs2 == expected2, f'問2の対面が想定と異なる: {pairs2}'
print('問2 検証OK: 対面ペア=', pairs2)

print('\nすべての検証に合格しました。')
