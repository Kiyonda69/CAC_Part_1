#!/usr/bin/env python3
"""航大思考233: 地図とコックピット前方視界の対応 - 解の一意性検証"""
import math


def bearing(x, y):
    """北=0°、時計回りの方位角（地図座標: x=東, y=北）"""
    return math.degrees(math.atan2(x, y)) % 360


def rel_bearing(b, heading):
    """機首方位headingに対する相対方位（-180〜180、負=左）"""
    r = (b - heading) % 360
    return r - 360 if r > 180 else r


def forward_view(landmarks, heading, fov):
    """前方視界(±fov°)内の地標を左から順に返す"""
    vis = []
    for name, (x, y) in landmarks.items():
        r = rel_bearing(bearing(x, y), heading)
        if abs(r) <= fov:
            vis.append((r, name))
    return [n for r, n in sorted(vis)]


# ========== 問1: 機首方位「南」・視界±90°・5地標の左右順序 ==========
LM1 = {"工場": (4, -1), "湖": (2, -2), "鉄塔": (0, -5),
       "タンク": (-3, -3), "山": (-4, -1)}


def verify_q1():
    order = forward_view(LM1, 180, 90)
    # 全5地標が前方視界内にあること
    assert len(order) == 5, f"前方に{len(order)}個しか見えない"
    expected = ["工場", "湖", "鉄塔", "タンク", "山"]
    assert order == expected, f"順序不一致: {order}"
    # 相対方位に十分な間隔があること（隣接15°以上、視認判別可能）
    rels = sorted(rel_bearing(bearing(x, y), 180) for x, y in LM1.values())
    gaps = [rels[i + 1] - rels[i] for i in range(4)]
    assert min(gaps) >= 15, f"間隔が狭すぎる: {gaps}"
    assert max(abs(r) for r in rels) <= 80, "視界の端に近すぎる"
    # 誤答選択肢がすべて正解と異なること
    distractors = [
        ["山", "タンク", "鉄塔", "湖", "工場"],   # 地図の左右をそのまま読む
        ["湖", "工場", "鉄塔", "タンク", "山"],   # 左側2つの入れ替え
        ["工場", "湖", "鉄塔", "山", "タンク"],   # 右側2つの入れ替え
        ["鉄塔", "湖", "タンク", "工場", "山"],   # 正面からの角度順
    ]
    for d in distractors:
        assert d != expected
    assert len({tuple(d) for d in distractors}) == 4, "誤答に重複"
    print(f"問1 OK: 左→右 = {order}")
    print(f"  相対方位: {[(n, round(rel_bearing(bearing(x, y), 180), 1)) for n, (x, y) in LM1.items()]}")
    return order


# ========== 問2: 方位不明→観測から方位推定→右90°旋回後の視界 ==========
LM2 = {"湖": (0, 3), "鉄塔": (3, 3), "タンク": (-3, 3),
       "工場": (4, -4), "山": (0, -4)}
OBSERVED = ["タンク", "湖", "鉄塔"]  # 旋回前に見えた3地標（左→右）
FOV2 = 60


def verify_q2():
    headings = {0: "北", 45: "北東", 90: "東", 135: "南東",
                180: "南", 225: "南西", 270: "西", 315: "北西"}
    # 観測と一致する機首方位が8方位中ただ一つであること
    matches = [h for h in headings if forward_view(LM2, h, FOV2) == OBSERVED]
    assert len(matches) == 1, f"方位が{len(matches)}個一致: {matches}"
    h0 = matches[0]
    assert h0 == 0, f"想定方位(北)と不一致: {headings[h0]}"
    # 各地標の相対方位が視界境界(60°)から十分離れていること
    for name, (x, y) in LM2.items():
        r = abs(rel_bearing(bearing(x, y), h0))
        assert abs(r - FOV2) >= 10, f"{name}が視界境界に近すぎる({r}°)"
    # 右90°旋回後の視界
    h1 = (h0 + 90) % 360
    after = forward_view(LM2, h1, FOV2)
    expected = ["鉄塔", "工場"]
    assert after == expected, f"旋回後の視界不一致: {after}"
    for name, (x, y) in LM2.items():
        r = abs(rel_bearing(bearing(x, y), h1))
        assert abs(r - FOV2) >= 10, f"旋回後{name}が視界境界に近すぎる({r}°)"
    # 誤答選択肢がすべて正解と異なること
    distractors = [
        ["タンク", "湖"],          # 左90°旋回側と混同（北西向きの視界）
        ["工場", "鉄塔"],          # 左右の反転
        ["湖", "鉄塔"],            # 45°しか回さない誤り（北東向きの視界）
        ["鉄塔", "工場", "山"],    # 視界±60°を±90°と誤る
    ]
    for d in distractors:
        assert d != expected
    assert len({tuple(d) for d in distractors}) == 4, "誤答に重複"
    # 各誤答が対応する誤推論の視界と実際に一致すること（罠の妥当性）
    assert forward_view(LM2, 315, FOV2) == ["タンク", "湖"]
    assert forward_view(LM2, 45, FOV2) == ["湖", "鉄塔"]
    # 罠(鉄塔・工場・山): 山は旋回後ちょうど真右90°にあり視界(±60°)外
    assert rel_bearing(bearing(*LM2["山"]), h1) == 90
    print(f"問2 OK: 機首方位={headings[h0]}(一意), 右90°旋回後 左→右 = {after}")
    for h in sorted(headings):
        print(f"  方位{headings[h]:>2}: {forward_view(LM2, h, FOV2)}")
    return after


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 問1・問2とも解は一意")
