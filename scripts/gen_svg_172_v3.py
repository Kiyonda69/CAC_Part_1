"""航大思考172 SVG生成 v5 - シンプル版

方針:
1. 「見える面」(top/front/right) を塗りつぶしで描画 → 立体感
2. 見える面の境界が立体の格子線・シルエットの大部分を担う
3. 不足するシルエット外形は、shapely で全可視面の和集合の外周を計算して追加
4. 見えない内部エッジは描画しない → 線数を抑制
"""

from itertools import product
from shapely.geometry import Polygon
from shapely.ops import unary_union

DX = 25
DY = 18
DZ = 26


def vertex(i, j, k, ox, oy):
    return (ox + DX * i - DX * j, oy + DY * i + DY * j - DZ * k)


def poly_str(points):
    return " ".join(f"{x},{y}" for x, y in points)


def cube_silhouette_polygon(i, j, k, ox, oy):
    """単位立方体の2D投影 = 6頂点ヘキサゴン"""
    # 8頂点のうち、isometric投影で外周ヘキサゴンを形成する6頂点
    # 順番: 上 → 右上 → 右下 → 下 → 左下 → 左上 → 上
    v002 = vertex(i,   j,   k+1, ox, oy)   # top-front-left
    v102 = vertex(i+1, j,   k+1, ox, oy)   # top-front-right
    v100 = vertex(i+1, j,   k,   ox, oy)   # bottom-front-right
    v110 = vertex(i+1, j+1, k,   ox, oy)   # bottom-back-right
    v010 = vertex(i,   j+1, k,   ox, oy)   # bottom-back-left
    v012 = vertex(i,   j+1, k+1, ox, oy)   # top-back-left
    return [v002, v102, v100, v110, v010, v012]


def render_shape(cubes, ox, oy):
    cubes_set = set(cubes)
    elems = []

    # 1. 見える面の polygon を描画 (top/front/right)
    sorted_cubes = sorted(cubes_set, key=lambda c: (c[0] - c[1] + c[2], -c[1], c[0], c[2]))
    for (i, j, k) in sorted_cubes:
        v000 = vertex(i,   j,   k,   ox, oy)
        v100 = vertex(i+1, j,   k,   ox, oy)
        v110 = vertex(i+1, j+1, k,   ox, oy)
        v010 = vertex(i,   j+1, k,   ox, oy)
        v001 = vertex(i,   j,   k+1, ox, oy)
        v101 = vertex(i+1, j,   k+1, ox, oy)
        v111 = vertex(i+1, j+1, k+1, ox, oy)
        v011 = vertex(i,   j+1, k+1, ox, oy)

        if (i, j, k+1) not in cubes_set:
            pts = [v001, v101, v111, v011]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="#dcdcdc" stroke="#111" stroke-width="1.2" stroke-linejoin="miter"/>'
            )
        if (i, j-1, k) not in cubes_set:
            pts = [v000, v100, v101, v001]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="#a8a8a8" stroke="#111" stroke-width="1.2" stroke-linejoin="miter"/>'
            )
        if (i+1, j, k) not in cubes_set:
            pts = [v100, v110, v111, v101]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="#787878" stroke="#111" stroke-width="1.2" stroke-linejoin="miter"/>'
            )

    # 2. 全立方体の2D投影の和集合の外周 = 立体のシルエット
    cube_silhouettes = [
        Polygon(cube_silhouette_polygon(i, j, k, ox, oy))
        for (i, j, k) in cubes_set
    ]
    if cube_silhouettes:
        union = unary_union(cube_silhouettes)

        def extract_outline_paths(geom):
            paths = []
            if geom.geom_type == "Polygon":
                paths.append(list(geom.exterior.coords))
                for interior in geom.interiors:
                    paths.append(list(interior.coords))
            elif geom.geom_type == "MultiPolygon":
                for poly in geom.geoms:
                    paths.extend(extract_outline_paths(poly))
            return paths

        for path in extract_outline_paths(union):
            pts_str = " ".join(f"{round(x, 2)},{round(y, 2)}" for x, y in path)
            elems.append(
                f'<polyline points="{pts_str}" fill="none" '
                f'stroke="#111" stroke-width="1.8" stroke-linejoin="miter" stroke-linecap="round"/>'
            )

    return "\n".join(elems)


def shape_from_removed(size, removed):
    all_cubes = set(product(range(size), repeat=3))
    return all_cubes - set(removed)


if __name__ == "__main__":
    p1_shapes = {
        1: shape_from_removed(2, [(0, 0, 1), (0, 1, 1)]),       # D
        2: shape_from_removed(2, [(0, 0, 1), (1, 0, 1)]),       # B
        3: shape_from_removed(2, [(0, 1, 1), (1, 1, 1)]),       # A [CORRECT]
        4: shape_from_removed(2, [(1, 0, 1), (1, 1, 1)]),       # C
        5: shape_from_removed(2, [(1, 1, 1)]),                  # E
    }
    p2_shapes = {
        1: shape_from_removed(2, [(0, 1, 1), (1, 0, 1), (1, 1, 1)]),  # B
        2: shape_from_removed(2, [(0, 0, 1), (0, 1, 1), (1, 1, 1)]),  # C
        3: shape_from_removed(2, [(1, 0, 1), (1, 1, 1)]),             # E
        4: shape_from_removed(2, [(0, 0, 1), (1, 0, 1), (1, 1, 1)]),  # A [CORRECT]
        5: shape_from_removed(2, [(0, 0, 1), (1, 0, 1), (0, 1, 1)]),  # D
    }

    print("==== 問1 ====")
    for pos, cubes in p1_shapes.items():
        svg_body = render_shape(cubes, ox=65, oy=95)
        print(f"--- option {pos} ---")
        print(svg_body)
        print()

    print("==== 問2 ====")
    for pos, cubes in p2_shapes.items():
        svg_body = render_shape(cubes, ox=65, oy=95)
        print(f"--- option {pos} ---")
        print(svg_body)
        print()
