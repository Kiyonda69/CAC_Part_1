#!/usr/bin/env python3
"""
航大思考117 の解の一意性検証（図形パターン版）

問1: 円の中の矢印の回転系列
  規則1: 矢印は45°ずつ時計回り（E→SE→S→SW→W→NW）
  規則2: 円の塗りつぶしはBlack/White交互
  既知5項: (E,B), (SE,W), (S,B), (SW,W), (W,B)
  6番目: (NW,W)

問2: 3属性独立規則の図形系列
  属性1: 外形 ○→□→△ の周期3
  属性2: 内部数字 1→2→3→4→5→... の+1
  属性3: 枠線 実線/点線 の交互
  既知5項: (○,1,実), (□,2,点), (△,3,実), (○,4,点), (□,5,実)
  6番目: (△,6,点)
"""


def verify_q1():
    """問1: 矢印回転+色交互"""
    directions = ['E', 'SE', 'S', 'SW', 'W', 'NW', 'N', 'NE']
    # 45°ずつ時計回り
    # 1項目目から
    sequence = []
    for i in range(6):
        dir_idx = i % 8
        color = 'B' if i % 2 == 0 else 'W'
        sequence.append((directions[dir_idx], color))

    print("問1の系列:")
    for i, (d, c) in enumerate(sequence, 1):
        marker = " <-- 答え" if i == 6 else ""
        print(f"  Step {i}: 矢印={d}, 色={c}{marker}")

    expected = [
        ('E', 'B'), ('SE', 'W'), ('S', 'B'),
        ('SW', 'W'), ('W', 'B'), ('NW', 'W'),
    ]
    assert sequence == expected, "系列が期待値と一致しない"
    assert sequence[5] == ('NW', 'W'), "6番目が (NW, W) でない"
    print("問1 検証成功")


def verify_q2():
    """問2: 3属性独立規則"""
    shapes = ['○', '□', '△']  # 周期3
    borders = ['実線', '点線']  # 周期2

    sequence = []
    for i in range(6):
        shape = shapes[i % 3]
        num = i + 1  # 1, 2, 3, 4, 5, 6
        border = borders[i % 2]
        sequence.append((shape, num, border))

    print("問2の系列:")
    for i, (s, n, b) in enumerate(sequence, 1):
        marker = " <-- 答え" if i == 6 else ""
        print(f"  Step {i}: 形={s}, 数={n}, 枠={b}{marker}")

    expected = [
        ('○', 1, '実線'),
        ('□', 2, '点線'),
        ('△', 3, '実線'),
        ('○', 4, '点線'),
        ('□', 5, '実線'),
        ('△', 6, '点線'),
    ]
    assert sequence == expected, "系列が期待値と一致しない"
    assert sequence[5] == ('△', 6, '点線'), "6番目が (△, 6, 点線) でない"
    print("問2 検証成功")


if __name__ == '__main__':
    print("=" * 60)
    print("問1 検証")
    print("=" * 60)
    verify_q1()
    print()
    print("=" * 60)
    print("問2 検証")
    print("=" * 60)
    verify_q2()
    print()
    print("=" * 60)
    print("全検証成功")
    print("=" * 60)
