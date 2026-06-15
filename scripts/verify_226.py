# -*- coding: utf-8 -*-
"""
航大思考226 検証スクリプト
タイプ: 立方体の転がり（格子の上を1マスずつ転がる立方体の面追跡）
220〜225（旋回方位・三面図・展開図・地図方位・紙折り・立方体切断）とは異なるタイプ。

立方体の面: top, bottom, north, south, east, west
真上から見て 北=上, 東=右。1マスずつ指定方向へ「転がる」。
"""


def roll(cube, direction):
    """cube を direction（E/W/N/S）に1マス転がした後の面配置を返す"""
    t, b = cube['top'], cube['bottom']
    n, s = cube['north'], cube['south']
    e, w = cube['east'], cube['west']
    if direction == 'E':   # 東へ転がる（東の辺を軸に倒れる）
        return {'top': w, 'bottom': e, 'east': t, 'west': b,
                'north': n, 'south': s}
    if direction == 'W':   # 西へ
        return {'top': e, 'bottom': w, 'west': t, 'east': b,
                'north': n, 'south': s}
    if direction == 'N':   # 北へ
        return {'top': s, 'bottom': n, 'north': t, 'south': b,
                'east': e, 'west': w}
    if direction == 'S':   # 南へ
        return {'top': n, 'bottom': s, 'south': t, 'north': b,
                'east': e, 'west': w}
    raise ValueError(direction)


def simulate(initial, path):
    cube = dict(initial)
    pos = (0, 0)
    move = {'E': (1, 0), 'W': (-1, 0), 'N': (0, 1), 'S': (0, -1)}
    for d in path:
        cube = roll(cube, d)
        dx, dy = move[d]
        pos = (pos[0] + dx, pos[1] + dy)
    return cube, pos


# ---- 初期配置（問1・問2 共通） ----
initial = {'top': 'A', 'bottom': 'B', 'north': 'C',
           'south': 'D', 'east': 'E', 'west': 'F'}

print("=== 問1: 東→北→東 と転がした後、上面の文字 ===")
path1 = ['E', 'N', 'E']
cube1, pos1 = simulate(initial, path1)
print("最終面配置:", cube1, "位置:", pos1)
print("上面 =", cube1['top'])

print("\n=== 問2: 閉ループ 東→北→北→西→南→南 を転がした後 ===")
# 出発(0,0)→E(1,0)→N(1,1)→N(1,2)→W(0,2)→S(0,1)→S(0,0) 出発点に戻る
path2 = ['E', 'N', 'N', 'W', 'S', 'S']
cube2, pos2 = simulate(initial, path2)
print("最終面配置:", cube2, "位置:", pos2)
assert pos2 == (0, 0), "閉ループになっていない"
print("出発点に戻ったが向きは変化。南を向く面 =", cube2['south'])
print("（参考）上面 =", cube2['top'], " 北面 =", cube2['north'])
