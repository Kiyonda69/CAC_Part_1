"""
航大思考131 解の一意性検証

問1: 半径3の円の内部で半径1の円が滑らずに転がる。
     初め接点Pにあった点の軌跡 → 3尖点ハイポサイクロイド（デルトイド）

問2: 半径2の円の外部で半径1の円が滑らずに転がる。
     初め接点Pにあった点の軌跡 → 2尖点エピサイクロイド（ネフロイド）

ハイポサイクロイド（内転）:
  x(t) = (R-r) cos(t) + r cos((R-r)/r * t)
  y(t) = (R-r) sin(t) - r sin((R-r)/r * t)
  → R/r個の尖点を持つ星形

エピサイクロイド（外転）:
  x(t) = (R+r) cos(t) - r cos((R+r)/r * t)
  y(t) = (R+r) sin(t) - r sin((R+r)/r * t)
  → R/r個の尖点を持つ花形
"""
import math


def count_cusps(xs, ys, eps=5e-3):
    """軌跡の尖点（速度0となる点）を数える。
    速度がeps未満の連続区間を1つの尖点として数える。"""
    n = len(xs)
    speeds = []
    for i in range(n):
        dx = xs[(i + 1) % n] - xs[i]
        dy = ys[(i + 1) % n] - ys[i]
        speeds.append(math.hypot(dx, dy))
    # 低速領域の連続成分を数える
    low = [s < eps for s in speeds]
    cusps = 0
    in_low = False
    # 周期境界処理: 末尾が低速かつ先頭も低速なら同一クラスタ
    start_offset = 0
    if low[0] and low[-1]:
        # 末尾の低速ストリークを先頭側にローテートして数えないようにする
        start_offset = 0
    for i in range(n):
        if low[i] and not in_low:
            cusps += 1
            in_low = True
        elif not low[i]:
            in_low = False
    # 先頭と末尾が同じクラスタなら重複カウントを修正
    if low[0] and low[-1] and cusps > 0:
        cusps -= 1
    return cusps


def hypocycloid(R, r, samples=3600):
    xs, ys = [], []
    for i in range(samples):
        t = 2 * math.pi * i / samples
        x = (R - r) * math.cos(t) + r * math.cos((R - r) / r * t)
        y = (R - r) * math.sin(t) - r * math.sin((R - r) / r * t)
        xs.append(x)
        ys.append(y)
    return xs, ys


def epicycloid(R, r, samples=3600):
    xs, ys = [], []
    for i in range(samples):
        t = 2 * math.pi * i / samples
        x = (R + r) * math.cos(t) - r * math.cos((R + r) / r * t)
        y = (R + r) * math.sin(t) - r * math.sin((R + r) / r * t)
        xs.append(x)
        ys.append(y)
    return xs, ys


def verify_q1():
    """問1: R=3, r=1 → デルトイド（3尖点）"""
    xs, ys = hypocycloid(3, 1)
    cusps = count_cusps(xs, ys)
    assert cusps == 3, f"問1: 期待3尖点, 実際{cusps}尖点"

    # 比較: R=2, r=1 はデルトイドではない（直線）
    xs2, ys2 = hypocycloid(2, 1)
    # R=2,r=1の場合、yは常に0（直線）
    max_abs_y = max(abs(y) for y in ys2)
    assert max_abs_y < 1e-9, f"R=2,r=1は直線のはず: max|y|={max_abs_y}"

    # 比較: R=4, r=1 はアステロイド（4尖点）
    xs4, ys4 = hypocycloid(4, 1)
    cusps4 = count_cusps(xs4, ys4)
    assert cusps4 == 4, f"R=4,r=1は4尖点アステロイド: 実際{cusps4}"

    print(f"問1 OK: R=3,r=1 ハイポサイクロイド = デルトイド({cusps}尖点)")
    print(f"       比較 R=2,r=1 → 直線、R=4,r=1 → {cusps4}尖点アステロイド")
    return cusps


def verify_q2():
    """問2: R=2, r=1 → ネフロイド（2尖点エピサイクロイド）"""
    xs, ys = epicycloid(2, 1)
    cusps = count_cusps(xs, ys)
    assert cusps == 2, f"問2: 期待2尖点, 実際{cusps}尖点"

    # 比較: R=1, r=1 はカーディオイド（1尖点）
    xs1, ys1 = epicycloid(1, 1)
    cusps1 = count_cusps(xs1, ys1)
    assert cusps1 == 1, f"R=1,r=1はカーディオイド(1尖点): 実際{cusps1}"

    # 比較: R=3, r=1 は3尖点エピサイクロイド
    xs3, ys3 = epicycloid(3, 1)
    cusps3 = count_cusps(xs3, ys3)
    assert cusps3 == 3, f"R=3,r=1は3尖点: 実際{cusps3}"

    print(f"問2 OK: R=2,r=1 エピサイクロイド = ネフロイド({cusps}尖点)")
    print(f"       比較 R=1,r=1 → {cusps1}尖点カーディオイド、R=3,r=1 → {cusps3}尖点")
    return cusps


if __name__ == "__main__":
    print("=== 航大思考131 検証 ===")
    verify_q1()
    verify_q2()
    print("\n両問とも軌跡の尖点数が一意に決定 → 解は唯一")
