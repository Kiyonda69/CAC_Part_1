"""航大思考172用 アイソメトリックSVG生成器

2x2x2の立方体ブロックから一部を取り除いた立体を、アイソメトリック投影で描画する。
"""

# アイソメトリック投影:
#  +X方向のステップ: ( DX,  DY)  右下
#  +Y方向のステップ: (-DX,  DY)  左下（奥行き）
#  +Z方向のステップ: (  0, -DZ)  上

DX = 17  # 26  -> 17 で少しコンパクトに
DY = 10  # 15  -> 10
DZ = 20  # 30  -> 20


def vertex(i, j, k, ox, oy):
    """格子点 (i,j,k) の画面座標"""
    x = ox + DX * i - DX * j
    y = oy + DY * i + DY * j - DZ * k
    return (x, y)


def poly_str(points):
    return " ".join(f"{x},{y}" for x, y in points)


def render_shape(cubes, ox, oy):
    """cubes: 単位立方体の集合 set of (i,j,k) integers
    アイソメトリック投影のSVG文字列を返す（中身要素のみ）。
    各立方体の3面（top, front, right）のうち、外面のみ描画する。

    色:
      top:  #d0d0d0 （明るい灰）
      right: #909090 （暗い灰）
      front: #b0b0b0 （中間）
    """
    cubes_set = set(cubes)
    elems = []

    # 描画順序: 奥(y大) → 手前(y小), 左(i小) → 右(i大), 下(k小) → 上(k大)
    sorted_cubes = sorted(cubes_set, key=lambda c: (-c[1], c[0], c[2]))

    for (i, j, k) in sorted_cubes:
        # 8頂点を計算
        v000 = vertex(i,   j,   k,   ox, oy)
        v100 = vertex(i+1, j,   k,   ox, oy)
        v110 = vertex(i+1, j+1, k,   ox, oy)
        v010 = vertex(i,   j+1, k,   ox, oy)
        v001 = vertex(i,   j,   k+1, ox, oy)
        v101 = vertex(i+1, j,   k+1, ox, oy)
        v111 = vertex(i+1, j+1, k+1, ox, oy)
        v011 = vertex(i,   j+1, k+1, ox, oy)

        # Top face (z=k+1, +Z方向): 隣に立方体がなければ描画
        if (i, j, k+1) not in cubes_set:
            pts = [v001, v101, v111, v011]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="#d8d8d8" stroke="#222" stroke-width="1" '
                f'stroke-linejoin="round"/>'
            )

        # Front face (y=j, -Y方向): 隣にキューブがなければ描画
        # j方向のマイナス側に立方体がなければ「前」面が見える
        if (i, j-1, k) not in cubes_set:
            pts = [v000, v100, v101, v001]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="#a8a8a8" stroke="#222" stroke-width="1" '
                f'stroke-linejoin="round"/>'
            )

        # Right face (x=i+1, +X方向)
        if (i+1, j, k) not in cubes_set:
            pts = [v100, v110, v111, v101]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="#888888" stroke="#222" stroke-width="1" '
                f'stroke-linejoin="round"/>'
            )

    return "\n".join(elems)


def shape_from_removed(size, removed):
    """size x size x size から removed を取り除いた集合を返す"""
    from itertools import product
    all_cubes = set(product(range(size), repeat=3))
    return all_cubes - set(removed)


if __name__ == "__main__":
    # 問1の5つの選択肢 (順番: position 1..5)
    p1_shapes = {
        1: shape_from_removed(2, [(0, 0, 1), (0, 1, 1)]),       # D: left-top edge
        2: shape_from_removed(2, [(0, 0, 1), (1, 0, 1)]),       # B: front-top edge
        3: shape_from_removed(2, [(0, 1, 1), (1, 1, 1)]),       # A: back-top edge [CORRECT]
        4: shape_from_removed(2, [(1, 0, 1), (1, 1, 1)]),       # C: right-top edge
        5: shape_from_removed(2, [(1, 1, 1)]),                  # E: corner only
    }
    # 問2の5つの選択肢
    p2_shapes = {
        1: shape_from_removed(2, [(0, 1, 1), (1, 0, 1), (1, 1, 1)]),  # B
        2: shape_from_removed(2, [(0, 0, 1), (0, 1, 1), (1, 1, 1)]),  # C
        3: shape_from_removed(2, [(1, 0, 1), (1, 1, 1)]),             # E
        4: shape_from_removed(2, [(0, 0, 1), (1, 0, 1), (1, 1, 1)]),  # A [CORRECT]
        5: shape_from_removed(2, [(0, 0, 1), (1, 0, 1), (0, 1, 1)]),  # D
    }

    # 出力: 各選択肢のSVG内容
    print("==== 問1 ====")
    for pos, cubes in p1_shapes.items():
        # ox=45, oy=70 で描画。SVGサイズ 95x95 を想定。
        svg_body = render_shape(cubes, ox=45, oy=80)
        print(f"--- option {pos} ---")
        print(svg_body)
        print()

    print("==== 問2 ====")
    for pos, cubes in p2_shapes.items():
        svg_body = render_shape(cubes, ox=45, oy=80)
        print(f"--- option {pos} ---")
        print(svg_body)
        print()
