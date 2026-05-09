"""類題166のSVG生成: サイコロ3D視点図と十字型展開図"""

# ===== サイコロ3D視点図 =====
def dice_3d(top, front, right, x=0, y=0, s=50, d=18):
    """斜投影でサイコロの3面（top, front, right）を描き、各面に数字を配置"""
    # 頂点 (x, y を加算)
    def p(px, py):
        return f"{x+px},{y+py}"
    # 面ポリゴン
    front_poly = f'<polygon points="{p(0,d)} {p(s,d)} {p(s,s+d)} {p(0,s+d)}" fill="white" stroke="black" stroke-width="2"/>'
    top_poly = f'<polygon points="{p(d,0)} {p(s+d,0)} {p(s,d)} {p(0,d)}" fill="white" stroke="black" stroke-width="2"/>'
    right_poly = f'<polygon points="{p(s,d)} {p(s+d,0)} {p(s+d,s)} {p(s,s+d)}" fill="white" stroke="black" stroke-width="2"/>'
    # 数字位置
    front_cx, front_cy = x + s/2, y + d + s/2
    top_cx, top_cy = x + (s+d)/2, y + d/2
    right_cx, right_cy = x + s + d/2, y + (s+d)/2
    # 数字（フロントは普通、上は小さく、右もやや傾斜なので少し小さめ）
    nums = (
        f'<text x="{front_cx:g}" y="{front_cy:g}" text-anchor="middle" '
        f'dominant-baseline="central" font-size="22" font-weight="bold">{front}</text>'
        f'<text x="{top_cx:g}" y="{top_cy:g}" text-anchor="middle" '
        f'dominant-baseline="central" font-size="14" font-weight="bold">{top}</text>'
        f'<text x="{right_cx:g}" y="{right_cy:g}" text-anchor="middle" '
        f'dominant-baseline="central" font-size="14" font-weight="bold">{right}</text>'
    )
    return front_poly + top_poly + right_poly + nums


# ===== 十字型展開図（数字付き） =====
def cross_net(values, x=0, y=0, s=50, font=22, blanks=None):
    """十字型展開図 values=[上, 左, 前, 右, 後, 下]
    blanks: その位置の値の代わりに表示する文字列（例: 'ア'）の dict {idx: label}
    座標: 各セル s×s。配置:
        [0:上]
    [1:左][2:前][3:右][4:後]
        [5:下]
    """
    if blanks is None:
        blanks = {}
    positions = [
        (s, 0),       # 0: 上
        (0, s),       # 1: 左
        (s, s),       # 2: 前
        (2*s, s),     # 3: 右
        (3*s, s),     # 4: 後
        (s, 2*s),     # 5: 下
    ]
    parts = []
    for i, ((px, py), v) in enumerate(zip(positions, values)):
        rx, ry = x + px, y + py
        parts.append(
            f'<rect x="{rx}" y="{ry}" width="{s}" height="{s}" '
            f'fill="white" stroke="black" stroke-width="2"/>'
        )
        label = blanks.get(i, str(v))
        parts.append(
            f'<text x="{rx + s/2:g}" y="{ry + s/2:g}" text-anchor="middle" '
            f'dominant-baseline="central" font-size="{font}" font-weight="bold">{label}</text>'
        )
    return "".join(parts)


# ===== 問1: 標準サイコロ視点（3視点）=====
print("=" * 30, "問1 視点SVG（3視点）", "=" * 30)
views_q1 = [(1, 2, 3), (3, 2, 6), (4, 2, 1)]
for i, (t, f, r) in enumerate(views_q1):
    print(f"\n視点{i+1}: top={t}, front={f}, right={r}")
    print(dice_3d(t, f, r, x=5, y=5))

# ===== 問1: 展開図（部分埋め込み）=====
# 与えるのは「前=2」のみ。他の (上=1, 右=3) は視点から推論。
# 求める空欄: ア=左, イ=後, ウ=下
print("\n" + "=" * 30, "問1 展開図SVG", "=" * 30)
# 前=2 のみ与え、上、左、右、後、下 はすべて空欄記号 or ?
q1_values = [1, 4, 2, 3, 5, 6]  # 真の値
q1_blanks = {0: "?", 1: "(ア)", 3: "?", 4: "(イ)", 5: "(ウ)"}
print(cross_net(q1_values, x=5, y=5, s=60, font=24, blanks=q1_blanks))

# ===== 問1: 選択肢（5つ）=====
# 正解位置: 3
# 正解: (ア, イ, ウ) = (4, 5, 6)
print("\n" + "=" * 30, "問1 選択肢", "=" * 30)
q1_choices = [
    (5, 4, 6),
    (4, 6, 5),
    (4, 5, 6),  # 正解
    (6, 5, 4),
    (5, 6, 4),
]
for i, (a, b, c) in enumerate(q1_choices):
    print(f"({i+1}) ア={a}, イ={b}, ウ={c}")

# ===== 問2: 非標準サイコロ視点（4視点）=====
print("\n" + "=" * 30, "問2 視点SVG（4視点）", "=" * 30)
views_q2 = [(1, 2, 5), (5, 2, 4), (1, 5, 3), (6, 2, 1)]
for i, (t, f, r) in enumerate(views_q2):
    print(f"\n視点{i+1}: top={t}, front={f}, right={r}")
    print(dice_3d(t, f, r, x=5, y=5))

# ===== 問2: 展開図 =====
print("\n" + "=" * 30, "問2 展開図SVG", "=" * 30)
q2_values = [1, 6, 2, 5, 3, 4]
q2_blanks = {0: "?", 1: "(ア)", 3: "?", 4: "(イ)", 5: "(ウ)"}
print(cross_net(q2_values, x=5, y=5, s=60, font=24, blanks=q2_blanks))

# ===== 問2: 選択肢 =====
# 正解位置: 2
# 正解: (ア, イ, ウ) = (6, 3, 4)
print("\n" + "=" * 30, "問2 選択肢", "=" * 30)
q2_choices = [
    (3, 6, 4),
    (6, 3, 4),  # 正解
    (6, 4, 3),
    (4, 3, 6),
    (3, 4, 6),
]
for i, (a, b, c) in enumerate(q2_choices):
    print(f"({i+1}) ア={a}, イ={b}, ウ={c}")
