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

DX = 26
DY = 18
DZ = 30

# 色設定: 3面で明度差を出し、立体感を強調
TOP_FILL = "#e8e8e8"    # 上面: 明るい
FRONT_FILL = "#b4b4b4"  # 前面: 中間
RIGHT_FILL = "#787878"  # 右面: 暗め
INTERNAL_STROKE = "#222"
INTERNAL_WIDTH = "0.7"   # 内部立方体境界: 細め
SILHOUETTE_STROKE = "#000"
SILHOUETTE_WIDTH = "2.4"  # 外形シルエット: 太め


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


def geom_to_polygons(geom, fill, stroke="#111", stroke_width="1.2"):
    """Polygon/MultiPolygon を SVG polygon 要素群に変換"""
    if geom is None or geom.is_empty:
        return []
    geoms = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    results = []
    for g in geoms:
        pts = list(g.exterior.coords)
        pts_str = " ".join(f"{round(x, 2)},{round(y, 2)}" for x, y in pts)
        results.append(
            f'<polygon points="{pts_str}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linejoin="miter"/>'
        )
    return results


def render_shape(cubes, ox, oy):
    """
    描画戦略:
    1. 立体全体のシルエットを塗りつぶしで描画 (背景となるソリッド)
    2. 個々の見える面を方向別の色で塗りつぶし (3D 陰影)
    3. 各立方体の内部境界線を薄く描画 (立方体カウント補助)
    4. 立体外形シルエットを太線で描画 (3D 物体感を強調)
    """
    cubes_set = set(cubes)
    elems = []

    sorted_cubes = sorted(cubes_set, key=lambda c: (c[0] - c[1] + c[2], -c[1], c[0], c[2]))

    # 各立方体の見える面を個別に描画 (個別立方体を視認可能にする)
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
                f'fill="{TOP_FILL}" stroke="{INTERNAL_STROKE}" '
                f'stroke-width="{INTERNAL_WIDTH}" stroke-linejoin="miter"/>'
            )
        if (i, j-1, k) not in cubes_set:
            pts = [v000, v100, v101, v001]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="{FRONT_FILL}" stroke="{INTERNAL_STROKE}" '
                f'stroke-width="{INTERNAL_WIDTH}" stroke-linejoin="miter"/>'
            )
        if (i+1, j, k) not in cubes_set:
            pts = [v100, v110, v111, v101]
            elems.append(
                f'<polygon points="{poly_str(pts)}" '
                f'fill="{RIGHT_FILL}" stroke="{INTERNAL_STROKE}" '
                f'stroke-width="{INTERNAL_WIDTH}" stroke-linejoin="miter"/>'
            )

    # 立体全体のシルエット外形を太線で描画 → 3D ソリッド物体感を強調
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
                f'stroke="{SILHOUETTE_STROKE}" stroke-width="{SILHOUETTE_WIDTH}" '
                f'stroke-linejoin="miter" stroke-linecap="round"/>'
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
