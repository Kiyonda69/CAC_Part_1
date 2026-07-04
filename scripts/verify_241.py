#!/usr/bin/env python3
"""航大思考241: 真下から見上げた機体の見え方（視点変換・鏡像）の検証

モデル:
- 世界座標: x=東, y=北
- 機体: 機首方位 h（単位ベクトル）。機体の左方向 = CCW90(h)、後方 = -h
- マーキング: 左主翼端が黒、右水平尾翼端が黒（上下両面塗装）
- 観測者: あおむけで頭方向 hd を向き真上を見上げる
  視野の上 = hd、視野の右 = CCW90(hd)
  （検算: 頭=北(0,1) → 右手=西(-1,0)。地図の見下ろしとは左右が逆＝鏡像）

各選択肢は「機首の向き・黒い主翼端の側・黒い尾翼端の側」の3成分
（視野座標）で表現し、物理モデルの結果と一致する選択肢が
ちょうど1つであることを確認する。
"""

N, S, E, W = (0, 1), (0, -1), (1, 0), (-1, 0)


def ccw90(v):
    """反時計回り90度回転（左方向の算出）"""
    return (-v[1], v[0])


def direction_label(v, view_right, view_up):
    """世界ベクトル v を視野座標のラベルに変換"""
    r = v[0] * view_right[0] + v[1] * view_right[1]
    u = v[0] * view_up[0] + v[1] * view_up[1]
    assert (r, u) in [(1, 0), (-1, 0), (0, 1), (0, -1)], "斜め方位は扱わない"
    if u == 1:
        return "up"
    if u == -1:
        return "down"
    return "right" if r == 1 else "left"


def seen_from_below(heading, head_dir):
    """真下の観測者が見上げたときの (機首, 黒主翼端, 黒尾翼端) を返す"""
    view_up = head_dir
    view_right = ccw90(head_dir)          # あおむけ→地図と左右反転
    aircraft_left = ccw90(heading)        # 左主翼端の張り出す方向
    aircraft_right = (-aircraft_left[0], -aircraft_left[1])
    return (
        direction_label(heading, view_right, view_up),        # 機首
        direction_label(aircraft_left, view_right, view_up),  # 黒主翼端
        direction_label(aircraft_right, view_right, view_up), # 黒尾翼端
    )


def verify(name, physical, options, expected_correct):
    """選択肢群の中で物理モデルと一致するものが唯一であることを検証"""
    assert len(set(options.values())) == 5, f"{name}: 選択肢に重複がある"
    matches = [no for no, sig in options.items() if sig == physical]
    assert len(matches) == 1, f"{name}: 一致する選択肢が{len(matches)}個"
    assert matches[0] == expected_correct, \
        f"{name}: 正解は({matches[0]})だが設定は({expected_correct})"
    print(f"{name}: 物理モデル={physical} → 唯一の正解=({matches[0]}) OK")


# ============ 問1: 機首=北, 観測者の頭=北 (正解:(5)) ============
q1_physical = seen_from_below(heading=N, head_dir=N)
# 期待: 機首は上のまま、西に張り出す左主翼端は視野の右、東の右尾翼端は左
assert q1_physical == ("up", "right", "left")
q1_options = {
    1: ("up", "left", "right"),    # 上から見た図のまま（反転忘れ）
    2: ("down", "right", "left"),  # 180度回転
    3: ("up", "right", "right"),   # 主翼だけ反転し尾翼を忘れた
    4: ("down", "left", "right"),  # 上下反転
    5: ("up", "right", "left"),    # 正解: 左右（東西）のみ反転
}
verify("問1", q1_physical, q1_options, expected_correct=5)

# ============ 問2: 機首=西, 観測者の頭=東 (正解:(2)) ============
q2_physical = seen_from_below(heading=W, head_dir=E)
# 期待: 視野の上=東・右=北。機首(西)は下、左主翼端(南)は左、右尾翼端(北)は右
assert q2_physical == ("down", "left", "right")
q2_options = {
    1: ("down", "right", "left"),  # 見下ろし地図のまま（左右反転忘れ）
    2: ("down", "left", "right"),  # 正解
    3: ("right", "down", "up"),    # 頭の向きを無視して北を上に描いた
    4: ("up", "right", "left"),    # 機首方位の取り違え（180度回転）
    5: ("down", "left", "left"),   # 尾翼端の反転を忘れた
}
verify("問2", q2_physical, q2_options, expected_correct=2)

# ============ 検算: 見上げ視点が鏡像であること ============
# 頭=北であおむけ → 視野の右は西（地図では東が右）
assert ccw90(N) == W
# 頭=東であおむけ → 視野の右は北（南が右になる見下ろしとは逆）
assert ccw90(E) == N

print("すべての検証に合格: 問1=(5), 問2=(2)")
