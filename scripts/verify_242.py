#!/usr/bin/env python3
"""航大思考242: 場周経路（トラフィックパターン）の空間推論 検証スクリプト

方位ベクトル: N=(0,1), E=(1,0), S=(0,-1), W=(-1,0)  ※北が上の地図座標
左旋回90°: (x,y) -> (-y,x) / 右旋回90°: (x,y) -> (y,-x)
機体の左手方向 = 機首方位を反時計回り90°回転 = (-y,x)
"""

DIRS = {"北": (0, 1), "東": (1, 0), "南": (0, -1), "西": (-1, 0)}
NAME = {v: k for k, v in DIRS.items()}


def turn_left(h):
    return (-h[1], h[0])


def turn_right(h):
    return (h[1], -h[0])


def legs(landing_heading, turn):
    """アップウィンドから始まる5レグの機首方位を返す"""
    h = landing_heading
    out = [h]  # 上昇（離陸方向=着陸方向）
    for _ in range(4):
        h = turn(h)
        out.append(h)
    return out  # [上昇, クロスウィンド, ダウンウィンド, ベース, 最終進入]


def side_of(pos, target, heading):
    """機体位置posから見たtargetの左右・前後を返す"""
    v = (target[0] - pos[0], target[1] - pos[1])
    fwd = heading
    left = (-heading[1], heading[0])
    f = v[0] * fwd[0] + v[1] * fwd[1]
    l = v[0] * left[0] + v[1] * left[1]
    lr = "左" if l > 0 else ("右" if l < 0 else "正面")
    fb = "前方" if f > 0 else ("後方" if f < 0 else "真横")
    return lr, fb


def verify_q1():
    # 南北滑走路・北向きに離着陸・左旋回場周経路
    L = legs(DIRS["北"], turn_left)
    down = L[2]  # ダウンウィンド（滑走路と平行な反対側のレグ）
    assert NAME[down] == "南", "ダウンウィンドの機首方位が南でない"
    # 幾何: 滑走路(0,0)-(0,4)。上昇(0,4)->(0,6)N, クロス(0,6)->(-3,6)W,
    # ダウン(-3,6)->(-3,-2)S, ベース(-3,-2)->(0,-2)E, 最終(0,-2)->(0,0)N
    p = (-3, 2)
    runway_center = (0, 2)
    lr, _ = side_of(p, runway_center, down)
    assert lr == "左", "滑走路が左側に見えない"
    # 選択肢: (機首方位, 滑走路の見える側)
    options = {1: ("北", "左"), 2: ("北", "右"), 3: ("南", "左"),
               4: ("南", "右"), 5: ("西", "正面")}
    truth = (NAME[down], lr)
    valid = [k for k, v in options.items() if v == truth]
    assert valid == [3], f"問1の解が一意でない: {valid}"
    print(f"問1 OK: 機首方位={truth[0]}, 滑走路={truth[1]}側 -> 正解(3)")


def verify_q2():
    # 東西滑走路・西向きに離着陸・右旋回場周経路
    L = legs(DIRS["西"], turn_right)
    down, base = L[2], L[3]
    assert NAME[down] == "東" and NAME[base] == "南", "レグ方位の導出誤り"
    # 幾何: 滑走路(2,0)-(6,0)。上昇(2,0)->(0,0)W, クロス(0,0)->(0,3)N,
    # ダウン(0,3)->(8,3)E, ベース(8,3)->(8,0)S, 最終(8,0)->(6,0)W
    a, b = (8, 1.5), (4, 3)  # A=ベース上, B=ダウンウィンド上
    lr, fb = side_of(a, b, base)
    assert (lr, fb) == ("右", "後方"), f"Bの相対方位の導出誤り: {lr}{fb}"
    # 選択肢: (Aの機首方位, Bの見える方向)
    # 誤答は一貫した誤りパターンに対応:
    # (1)周回方向の逆転(A北向きと誤解), (2)AとBのレグ取り違え(A東向き),
    # (3)南向き時の左右混同, (5)前後の取り違え
    options = {1: ("北", "左前方"), 2: ("東", "左後方"), 3: ("南", "左後方"),
               4: ("南", "右後方"), 5: ("南", "右前方")}
    truth = (NAME[base], lr + fb)
    valid = [k for k, v in options.items() if v == truth]
    assert valid == [4], f"問2の解が一意でない: {valid}"
    print(f"問2 OK: A機首方位={truth[0]}, B={truth[1]} -> 正解(4)")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証 PASS: 解は一意")
