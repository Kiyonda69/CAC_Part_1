"""航大思考172用 アイソメトリックSVG生成器 v2 - 改善版

立方体を大きく、ストロークを濃く、視認性を向上させる
"""

DX = 25
DY = 18
DZ = 26


def vertex(i, j, k, ox, oy):
    return (ox + DX * i - DX * j, oy + DY * i + DY * j - DZ * k)


def poly_str(points):
    return " ".join(f"{x},{y}" for x, y in points)


def render_shape(cubes, ox, oy):
    cubes_set = set(cubes)
    elems = []
    # 描画順: 奥(viewer から遠い順) → 手前。深さ = x - y + z 昇順
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
            elems.append(
                f'<polygon points="{poly_str([v001, v101, v111, v011])}" '
                f'fill="#dcdcdc" stroke="#111" stroke-width="1.5" stroke-linejoin="miter"/>'
            )
        if (i, j-1, k) not in cubes_set:
            elems.append(
                f'<polygon points="{poly_str([v000, v100, v101, v001])}" '
                f'fill="#a8a8a8" stroke="#111" stroke-width="1.5" stroke-linejoin="miter"/>'
            )
        if (i+1, j, k) not in cubes_set:
            elems.append(
                f'<polygon points="{poly_str([v100, v110, v111, v101])}" '
                f'fill="#787878" stroke="#111" stroke-width="1.5" stroke-linejoin="miter"/>'
            )
    return "\n".join(elems)


def shape_from_removed(size, removed):
    from itertools import product
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

    # ox=65, oy=95 → 描画範囲: x∈[15, 115], y∈[35, 155]
    # viewBox: "0 0 130 170"
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
