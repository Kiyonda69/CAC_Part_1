"""
航大思考173用 SVG生成ヘルパー
等角投影（isometric projection）で立体図形を描画する
"""

import math

def make_renderer(S):
    """指定の立方体サイズSで描画器を生成"""
    COS30 = S * math.sqrt(3) / 2
    SIN30 = S / 2

    def project(x, y, z, ox=0, oy=0):
        X = ox + (x - y) * COS30
        Y = oy + (x + y) * SIN30 - z * S
        return (round(X, 2), round(Y, 2))

    def visible_faces(cubes):
        faces = []
        for (x, y, z) in cubes:
            if (x, y, z + 1) not in cubes:
                faces.append(('top', x, y, z))
            if (x + 1, y, z) not in cubes:
                faces.append(('right', x, y, z))
            if (x, y - 1, z) not in cubes:
                faces.append(('front', x, y, z))
        return faces

    def face_polygon(face, ox=0, oy=0):
        kind, x, y, z = face
        if kind == 'top':
            p1 = project(x, y, z + 1, ox, oy)
            p2 = project(x + 1, y, z + 1, ox, oy)
            p3 = project(x + 1, y + 1, z + 1, ox, oy)
            p4 = project(x, y + 1, z + 1, ox, oy)
        elif kind == 'right':
            p1 = project(x + 1, y, z, ox, oy)
            p2 = project(x + 1, y + 1, z, ox, oy)
            p3 = project(x + 1, y + 1, z + 1, ox, oy)
            p4 = project(x + 1, y, z + 1, ox, oy)
        elif kind == 'front':
            p1 = project(x, y, z, ox, oy)
            p2 = project(x + 1, y, z, ox, oy)
            p3 = project(x + 1, y, z + 1, ox, oy)
            p4 = project(x, y, z + 1, ox, oy)
        return [p1, p2, p3, p4]

    def render_cubes(cubes, ox=0, oy=0):
        fill_color = {'top': 'white', 'right': '#cccccc', 'front': '#888888'}
        faces = visible_faces(cubes)
        # back-to-front: sort by depth ascending (背面から描画)
        # 視点 (+x, -y, +z) → 奥 = small x, large y, small z
        def face_depth(face):
            kind, x, y, z = face
            if kind == 'top':
                return (x + 0.5) - (y + 0.5) + (z + 1)
            elif kind == 'right':
                return (x + 1) - (y + 0.5) + (z + 0.5)
            else:  # front
                return (x + 0.5) - y + (z + 0.5)
        faces.sort(key=face_depth)

        polygons = []
        for face in faces:
            kind, _, _, _ = face
            pts = face_polygon(face, ox, oy)
            pts_str = ' '.join(f'{p[0]},{p[1]}' for p in pts)
            color = fill_color[kind]
            polygons.append(
                f'<polygon points="{pts_str}" fill="{color}" stroke="black" stroke-width="1"/>'
            )
        return polygons

    def bounding_box(cubes):
        all_corners = []
        for (x, y, z) in cubes:
            for dx in [0, 1]:
                for dy in [0, 1]:
                    for dz in [0, 1]:
                        all_corners.append(project(x + dx, y + dy, z + dz))
        min_x = min(c[0] for c in all_corners)
        max_x = max(c[0] for c in all_corners)
        min_y = min(c[1] for c in all_corners)
        max_y = max(c[1] for c in all_corners)
        return (min_x, min_y, max_x, max_y)

    def svg_for_shape(cubes, margin=8):
        bbox = bounding_box(cubes)
        bb_width = bbox[2] - bbox[0]
        bb_height = bbox[3] - bbox[1]
        ox = -bbox[0] + margin
        oy = -bbox[1] + margin
        total_w = bb_width + margin * 2
        total_h = bb_height + margin * 2
        polygons = render_cubes(cubes, ox=ox, oy=oy)
        inner = '\n'.join('        ' + p for p in polygons)
        return total_w, total_h, inner

    return svg_for_shape


# ===== 図形定義 =====

# 問1
A1 = {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}
candidates1 = [
    {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)},  # (1) 2x2x1スラブ
    {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)},  # (2) トリポッド（正解）
    {(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0)},  # (3) L字（平面）
    {(0, 0, 0), (1, 0, 0), (2, 0, 0), (1, 1, 0)},  # (4) T字（平面）
    {(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)},  # (5) S字（平面）
]

# 問2
A2 = (
    {(x, y, 0) for x in range(3) for y in range(3)} |
    {(x, y, 1) for x in range(3) for y in [0, 1]} |
    {(x, 0, 2) for x in range(3)}
)
candidates2 = [
    # (1) 正解
    {(x, 0, 0) for x in range(3)} | {(x, y, 1) for x in range(3) for y in [0, 1]},
    # (2) 3×3×1スラブ
    {(x, y, 0) for x in range(3) for y in range(3)},
    # (3) 2×2×2 + 1個突起
    {(x, y, z) for x in [0, 1] for y in [0, 1] for z in [0, 1]} | {(2, 0, 0)},
    # (4) 5+3+1ピラミッド階段（平面内）
    {(x, 0, 0) for x in range(5)} | {(x, 0, 1) for x in [1, 2, 3]} | {(2, 0, 2)},
    # (5) 3D螺旋
    {(x, 0, 0) for x in range(3)} | {(2, y, 1) for y in range(3)} | {(x, 2, 2) for x in range(3)},
]


def emit_svg(shape, S=22, margin=8, indent=8):
    render = make_renderer(S)
    w, h, inner = render(shape, margin=margin)
    pad = ' ' * indent
    return f'{pad}<svg width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.2f} {h:.2f}">\n{inner}\n{pad}</svg>'


if __name__ == '__main__':
    import sys
    section = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if section in ('all', 'q1A'):
        print('--- 問1 立体A (S=28) ---')
        print(emit_svg(A1, S=28))

    if section in ('all', 'q1cand'):
        for i, c in enumerate(candidates1, 1):
            print(f'--- 問1 候補({i}) (S=22) ---')
            print(emit_svg(c, S=22))

    if section in ('all', 'q2A'):
        print('--- 問2 立体A (S=22) ---')
        print(emit_svg(A2, S=22))

    if section in ('all', 'q2cand'):
        for i, c in enumerate(candidates2, 1):
            print(f'--- 問2 候補({i}) (S=18) ---')
            print(emit_svg(c, S=18))
