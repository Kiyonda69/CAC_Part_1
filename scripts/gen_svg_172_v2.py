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

        # 見える3面（top/front/right）は塗りつぶし＋ストローク
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

    # シルエット境界の補完: 立体の境界エッジで、上記の見える面が描かない部分を線で描く
    # 各エッジ位置で「周囲4セル中、立方体である数」を数え、0 < count < 4 ならエッジ描画
    # ただし、すでに見える面が描いている可視エッジは省略（重複防止）
    edge_lines = compute_boundary_edges(cubes_set, ox, oy)
    for (p1, p2) in edge_lines:
        elems.append(
            f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" '
            f'stroke="#111" stroke-width="1.5" stroke-linecap="round"/>'
        )
    return "\n".join(elems)


def compute_boundary_edges(cubes_set, ox, oy):
    """立体の表面上にあるエッジを返す。

    各単位エッジは周囲の4セル（垂直方向にエッジを取り囲む4つの単位立方体位置）
    に接する。立方体である数が 1,2,3 ならエッジは立体表面上にある。
    0 → 完全に空中
    4 → 完全に内部
    1,2,3 → 表面上のエッジ

    アイソメトリック視点 (1,-1,1) で、表面エッジのうち
    奥(背面側) の隠れたものは「不可視」だが、可視シルエットを完成させる
    ため、表面エッジはすべて描画する（通常の3面図と同様の表現）。
    """
    lines = []
    drawn = set()

    def add_line(p1, p2):
        key = tuple(sorted([p1, p2]))
        if key in drawn:
            return
        drawn.add(key)
        lines.append((p1, p2))

    # 2x2x2 のグリッド範囲を想定: i,j,k ∈ {0..size}
    # bounding box を立体から決定
    if not cubes_set:
        return lines
    max_i = max(c[0] for c in cubes_set) + 2
    max_j = max(c[1] for c in cubes_set) + 2
    max_k = max(c[2] for c in cubes_set) + 2

    # X方向エッジ: (i,j,k) - (i+1,j,k) を共有する 4 セル: (i, j-1, k-1), (i, j, k-1), (i, j-1, k), (i, j, k)
    for i in range(max_i):
        for j in range(max_j + 1):
            for k in range(max_k + 1):
                cells = [(i, j-1, k-1), (i, j, k-1), (i, j-1, k), (i, j, k)]
                cnt = sum(1 for c in cells if c in cubes_set)
                if 0 < cnt < 4:
                    add_line(vertex(i, j, k, ox, oy), vertex(i+1, j, k, ox, oy))

    # Y方向エッジ: (i,j,k) - (i,j+1,k) を共有する 4 セル: (i-1, j, k-1), (i, j, k-1), (i-1, j, k), (i, j, k)
    for i in range(max_i + 1):
        for j in range(max_j):
            for k in range(max_k + 1):
                cells = [(i-1, j, k-1), (i, j, k-1), (i-1, j, k), (i, j, k)]
                cnt = sum(1 for c in cells if c in cubes_set)
                if 0 < cnt < 4:
                    add_line(vertex(i, j, k, ox, oy), vertex(i, j+1, k, ox, oy))

    # Z方向エッジ: (i,j,k) - (i,j,k+1) を共有する 4 セル: (i-1, j-1, k), (i, j-1, k), (i-1, j, k), (i, j, k)
    for i in range(max_i + 1):
        for j in range(max_j + 1):
            for k in range(max_k):
                cells = [(i-1, j-1, k), (i, j-1, k), (i-1, j, k), (i, j, k)]
                cnt = sum(1 for c in cells if c in cubes_set)
                if 0 < cnt < 4:
                    add_line(vertex(i, j, k, ox, oy), vertex(i, j, k+1, ox, oy))

    return lines


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
