# -*- coding: utf-8 -*-
"""
航大思考221 検証スクリプト（正投影＝三面図からの立体認識）

座標系:
  x: 幅（右が +x）   0..W-1
  y: 奥行き（奥が +y） 0..D-1
  z: 高さ（上が +z）   0..H-1
立体は単位立方体 (x,y,z) の集合で表す。

三面図:
  正面図 front : 幅x × 高さz   （奥行き方向に投影）
  側面図 side  : 奥行y × 高さz （幅方向に投影）
  平面図 top   : 幅x × 奥行y   （高さ方向に投影）
"""

def front_view(cubes, W, H):
    # (x,z) が埋まるか: いずれかの y に立方体
    return {(x, z) for (x, y, z) in cubes}

def side_view(cubes, D, H):
    # (y,z) が埋まるか: いずれかの x に立方体
    return {(y, z) for (x, y, z) in cubes}

def top_view(cubes, W, D):
    # (x,y) が埋まるか: いずれかの z に立方体
    return {(x, y) for (x, y, z) in cubes}

def render_grid(cells, cols, rows, fill='#', empty='.'):
    """rows を上から下（z降順 / y降順）で文字列化"""
    lines = []
    for r in range(rows - 1, -1, -1):
        line = ''.join(fill if (c, r) in cells else empty for c in range(cols))
        lines.append(line)
    return '\n'.join(lines)


# ====== 立体定義（問1） ======
# W=3, D=2, H=2  正解=3
W1, D1, H1 = 3, 2, 2

def views(cubes, W, D, H):
    return (front_view(cubes, W, H), side_view(cubes, D, H), top_view(cubes, W, D))

# 正解: 底面=幅3奥行2のL字（奥右に欠け）＋ 手前左(0,0)だけ2段の柱
correct1 = {
    (0,0,0),(1,0,0),(2,0,0),(0,1,0),   # 底面L字 (奥y1は左端のみ)
    (0,0,1),                            # 手前左の柱が2段
}

# ダミーa: 柱を右端(2,0)に → 正面図が変わる
d1a = {(0,0,0),(1,0,0),(2,0,0),(0,1,0),(2,0,1)}
# ダミーb: 底面の欠けを奥左に → 平面図が変わる
d1b = {(0,0,0),(1,0,0),(2,0,0),(2,1,0),(0,0,1)}
# ダミーc: 柱を奥(0,1)に → 側面図が変わる（奥行の鏡像）
d1c = {(0,0,0),(1,0,0),(2,0,0),(0,1,0),(0,1,1)}
# ダミーd: 手前2本(0,0)(1,0)が2段 → 正面図が変わる
d1d = {(0,0,0),(1,0,0),(2,0,0),(0,1,0),(0,0,1),(1,0,1)}

# 選択肢の並び（正解=3）
options1 = [d1a, d1c, correct1, d1b, d1d]

def check(name, options, correct, W, D, H):
    target = views(correct, W, D, H)
    matches = [i+1 for i, s in enumerate(options) if views(s, W, D, H) == target]
    print(f'--- {name} 一意性チェック ---')
    print(f'三面図が一致する選択肢: {matches}')
    assert matches == [options.index(correct)+1], f'一意でない: {matches}'
    print(f'OK: 正解は({matches[0]})で一意\n')
    return matches[0]

# ====== 立体定義（問2・高難度） ======
# W=3, D=3, H=3  正解=1  柱状立体（各列は z=0 から積む）
W2, D2, H2 = 3, 3, 3

def solid_from_heightmap(hmap):
    """hmap: {(x,y): 高さ} から立方体集合を生成"""
    cubes = set()
    for (x, y), h in hmap.items():
        for z in range(h):
            cubes.add((x, y, z))
    return cubes

# 正解: 奥(y2)に幅3の壁、中央(x1)が手前へ伸びるT字。中央奥が最も高い塔(3)
hc2 = {(0,2):1,(1,2):3,(2,2):2,(1,1):2,(1,0):1}
correct2 = solid_from_heightmap(hc2)

# ダミーa: (0,1)に高さ1を追加 → 平面図のみ変化（前/側の最大は不変）
d2a = solid_from_heightmap({**hc2, (0,1):1})
# ダミーb: 右奥(2,2)を高さ3に → 正面図のみ変化
d2b = solid_from_heightmap({**hc2, (2,2):3})
# ダミーc: 中央(1,1)を高さ1に → 側面図のみ変化
d2c = solid_from_heightmap({**hc2, (1,1):1})
# ダミーd: 手前左(0,0)に高さ1を追加 → 平面図のみ変化
d2d = solid_from_heightmap({**hc2, (0,0):1})

options2 = [correct2, d2a, d2b, d2c, d2d]

if __name__ == '__main__':
    fv, sv, tv = views(correct1, W1, D1, H1)
    print('=== 問1 正解立体の三面図 ===')
    print('[正面図] 幅3 x 高2 (左=x0)')
    print(render_grid(fv, W1, H1))
    print('[側面図] 奥行2 x 高2 (左=手前y0)')
    print(render_grid(sv, D1, H1))
    print('[平面図] 幅3 x 奥行2 (上=奥y1)')
    print(render_grid(tv, W1, D1))
    print()
    check('問1', options1, correct1, W1, D1, H1)

    fv2, sv2, tv2 = views(correct2, W2, D2, H2)
    print('=== 問2 正解立体の三面図 ===')
    print('[正面図] 幅3 x 高3 (左=x0)')
    print(render_grid(fv2, W2, H2))
    print('[側面図] 奥行3 x 高3 (左=手前y0)')
    print(render_grid(sv2, D2, H2))
    print('[平面図] 幅3 x 奥行3 (上=奥y2)')
    print(render_grid(tv2, W2, D2))
    print()
    check('問2', options2, correct2, W2, D2, H2)
