"""
航大思考83 検証スクリプト
問1: 立方体の展開図（辺の重なり）
問2: 図形の回転（L字型90°時計回り回転）
"""

def verify_problem1():
    """
    問1: 立方体の展開図 - 辺アイと重なる辺を求める

    展開図（十字型）:
         ア──イ
         │ ① │
      ウ──エ──オ──カ──キ
      │ ② │ ③ │ ④ │ ⑤│
      ク──ケ──コ──サ──シ
         │ ⑥ │
         ス──セ

    ③を正面として組み立てる
    """
    print("=" * 50)
    print("問1: 立方体の展開図 - 辺の重なり検証")
    print("=" * 50)

    # 3D座標マッピング（③を正面 z=0 として配置）
    # ③: エ(0,1,0), オ(1,1,0), コ(1,0,0), ケ(0,0,0)
    # ①: 上面 (y=1平面) - エオを軸に折り上げ
    # ②: 左面 (x=0平面) - エケを軸に折り左
    # ④: 右面 (x=1平面) - オコを軸に折り右
    # ⑤: 背面 (z=1平面) - カサを軸に折り後ろ
    # ⑥: 下面 (y=0平面) - ケコを軸に折り下

    vertices_3d = {
        # 正面 ③
        'エ': (0, 1, 0),
        'オ': (1, 1, 0),
        'コ': (1, 0, 0),
        'ケ': (0, 0, 0),
        # 上面 ①
        'ア': (0, 1, 1),
        'イ': (1, 1, 1),
        # 左面 ②
        'ウ': (0, 1, 1),
        'ク': (0, 0, 1),
        # 右面 ④
        'カ': (1, 1, 1),
        'サ': (1, 0, 1),
        # 背面 ⑤
        'キ': (0, 1, 1),
        'シ': (0, 0, 1),
        # 下面 ⑥
        'ス': (0, 0, 1),
        'セ': (1, 0, 1),
    }

    # 同一頂点の確認
    print("\n【同一頂点マッピング】")
    from collections import defaultdict
    point_map = defaultdict(list)
    for name, coord in vertices_3d.items():
        point_map[coord].append(name)
    for coord, names in sorted(point_map.items()):
        if len(names) > 1:
            print(f"  {coord}: {', '.join(names)}")

    # 内部辺（2面で共有される辺）
    internal_edges = [
        ('エ', 'オ'),  # ①-③
        ('エ', 'ケ'),  # ②-③
        ('オ', 'コ'),  # ③-④
        ('ケ', 'コ'),  # ③-⑥
        ('カ', 'サ'),  # ④-⑤
    ]

    # 境界辺（外周の辺）
    boundary_edges = [
        # ① の境界辺
        ('ア', 'イ'),  # 上辺
        ('ア', 'エ'),  # 左辺
        ('イ', 'オ'),  # 右辺
        # ② の境界辺
        ('ウ', 'エ'),  # 上辺
        ('ウ', 'ク'),  # 左辺
        ('ク', 'ケ'),  # 下辺
        # ④ の境界辺
        ('オ', 'カ'),  # 上辺
        ('コ', 'サ'),  # 下辺
        # ⑤ の境界辺
        ('カ', 'キ'),  # 上辺
        ('キ', 'シ'),  # 右辺
        ('サ', 'シ'),  # 下辺
        # ⑥ の境界辺
        ('ケ', 'ス'),  # 左辺
        ('ス', 'セ'),  # 下辺
        ('セ', 'コ'),  # 右辺
    ]

    def edge_3d(v1, v2):
        return frozenset([vertices_3d[v1], vertices_3d[v2]])

    # 対応する辺のペアを検出
    print("\n【重なる辺のペア（非隣接）】")
    matching_pairs = []
    for i, e1 in enumerate(boundary_edges):
        for e2 in boundary_edges[i+1:]:
            if edge_3d(e1[0], e1[1]) == edge_3d(e2[0], e2[1]):
                # 隣接チェック（共有頂点があるか）
                shared = set(e1) & set(e2)
                if not shared:
                    matching_pairs.append((e1, e2))
                    print(f"  辺{e1[0]}{e1[1]} = 辺{e2[0]}{e2[1]}")

    # 辺アイと重なる辺を特定
    target_edge = edge_3d('ア', 'イ')
    print(f"\n【問題】辺アイ {vertices_3d['ア']}-{vertices_3d['イ']} と重なる辺は？")

    answer = None
    for e in boundary_edges:
        if e == ('ア', 'イ'):
            continue
        if edge_3d(e[0], e[1]) == target_edge:
            shared = set(('ア', 'イ')) & set(e)
            if not shared:
                answer = e
                print(f"  → 辺{e[0]}{e[1]} ({vertices_3d[e[0]]}-{vertices_3d[e[1]]})")

    assert answer == ('カ', 'キ'), f"期待: ('カ', 'キ'), 実際: {answer}"

    # 選択肢の検証
    choices = {
        1: ('ウ', 'ク'),
        2: ('ス', 'セ'),
        3: ('カ', 'キ'),  # 正解
        4: ('ケ', 'ス'),
        5: ('セ', 'コ'),
    }

    print("\n【選択肢の検証】")
    correct_count = 0
    for num, choice in choices.items():
        is_match = edge_3d(choice[0], choice[1]) == target_edge
        shared = set(('ア', 'イ')) & set(choice)
        status = "正解" if is_match and not shared else "不正解"
        if is_match and not shared:
            correct_count += 1
        print(f"  ({num}) 辺{choice[0]}{choice[1]}: "
              f"{vertices_3d[choice[0]]}-{vertices_3d[choice[1]]} → {status}")

    assert correct_count == 1, f"正解が{correct_count}個（1個であるべき）"
    print(f"\n正解は (3) 辺カキ → 解の一意性確認済み")


def verify_problem2():
    """
    問2: L字型図形の90°時計回り回転

    見本（L字型、4セル）:
      ┌───┐
      │ F │  (0, 2)
      ├───┤
      │ G │  (0, 1)
      ├───┼───┐
      │ H │ J │  (0, 0), (1, 0)
      └───┴───┘

    90°時計回り回転後:
      ┌───┬───┬───┐
      │ H │ G │ F │  (文字も90°回転)
      ├───┘   └───┘
      │ J │
      └───┘
    """
    print("\n" + "=" * 50)
    print("問2: L字型図形の90°時計回り回転検証")
    print("=" * 50)

    # 元のセル位置と文字
    original = {
        'F': (0, 2),
        'G': (0, 1),
        'H': (0, 0),
        'J': (1, 0),
    }

    def rotate_90_cw(positions):
        """90°時計回り回転: (x,y) → (y, -x)、正規化"""
        rotated = {}
        for letter, (x, y) in positions.items():
            rotated[letter] = (y, -x)
        # 正規化（最小座標を0にする）
        min_x = min(p[0] for p in rotated.values())
        min_y = min(p[1] for p in rotated.values())
        return {k: (v[0]-min_x, v[1]-min_y) for k, v in rotated.items()}

    def rotate_90_ccw(positions):
        """90°反時計回り回転: (x,y) → (-y, x)、正規化"""
        rotated = {}
        for letter, (x, y) in positions.items():
            rotated[letter] = (-y, x)
        min_x = min(p[0] for p in rotated.values())
        min_y = min(p[1] for p in rotated.values())
        return {k: (v[0]-min_x, v[1]-min_y) for k, v in rotated.items()}

    def rotate_180(positions):
        """180°回転: (x,y) → (-x, -y)、正規化"""
        rotated = {}
        for letter, (x, y) in positions.items():
            rotated[letter] = (-x, -y)
        min_x = min(p[0] for p in rotated.values())
        min_y = min(p[1] for p in rotated.values())
        return {k: (v[0]-min_x, v[1]-min_y) for k, v in rotated.items()}

    def mirror_h(positions):
        """水平鏡像: (x,y) → (max_x - x, y)"""
        max_x = max(p[0] for p in positions.values())
        mirrored = {k: (max_x - v[0], v[1]) for k, v in positions.items()}
        return mirrored

    # 正解: 90°時計回り
    correct = rotate_90_cw(original)
    print(f"\n【90°時計回り回転結果】")
    for letter, pos in sorted(correct.items()):
        print(f"  {letter}: {pos}")

    # 期待される結果
    expected_correct = {
        'F': (2, 1),
        'G': (1, 1),
        'H': (0, 1),
        'J': (0, 0),
    }
    assert correct == expected_correct, f"90°CW結果が不正: {correct}"
    print("  → 期待通り")

    # 各選択肢の定義と検証
    # (1) 180°回転
    opt1 = rotate_180(original)
    print(f"\n【選択肢(1): 180°回転】")
    for letter, pos in sorted(opt1.items()):
        print(f"  {letter}: {pos}")

    # (2) 鏡像 + 90°CW（鏡像回転）
    opt2_mirror = mirror_h(original)
    opt2 = rotate_90_cw(opt2_mirror)
    print(f"\n【選択肢(2): 鏡像+90°CW】")
    for letter, pos in sorted(opt2.items()):
        print(f"  {letter}: {pos}")

    # (3) 90°反時計回り
    opt3 = rotate_90_ccw(original)
    print(f"\n【選択肢(3): 90°CCW】")
    for letter, pos in sorted(opt3.items()):
        print(f"  {letter}: {pos}")

    # (4) 正解: 90°CW
    opt4 = correct
    print(f"\n【選択肢(4): 90°CW（正解）】")
    for letter, pos in sorted(opt4.items()):
        print(f"  {letter}: {pos}")

    # (5) 正しい形だが文字の位置が入れ替わり
    opt5 = {
        'G': (2, 1),  # FとGが入れ替わり
        'F': (1, 1),
        'H': (0, 1),
        'J': (0, 0),
    }
    print(f"\n【選択肢(5): 形は正しいが文字入れ替え】")
    for letter, pos in sorted(opt5.items()):
        print(f"  {letter}: {pos}")

    # 一意性検証
    options = [opt1, opt2, opt3, opt4, opt5]
    correct_indices = [i+1 for i, opt in enumerate(options) if opt == expected_correct]
    assert correct_indices == [4], f"正解の選択肢: {correct_indices}（4のみであるべき）"

    # すべての不正解が正解と異なることを確認
    for i, opt in enumerate(options):
        if i + 1 != 4:
            assert opt != expected_correct, f"選択肢({i+1})が正解と一致してしまう"

    print(f"\n正解は (4) 90°時計回り回転 → 解の一意性確認済み")


if __name__ == '__main__':
    verify_problem1()
    verify_problem2()
    print("\n" + "=" * 50)
    print("全検証完了: 問1・問2ともに解が一意であることを確認")
    print("=" * 50)
