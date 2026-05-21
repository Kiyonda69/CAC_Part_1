"""
航大思考175 - 航空にちなんだ空間認識問題
問1: 空港の建物配置から南からのシルエットを特定
問2: 南からのシルエットと東からのシルエットから建物配置を特定
"""
from itertools import permutations


def silhouette_south(buildings, n_cols):
    """南から見たシルエット (列ごとの最大高さ、西→東)"""
    sil = [0] * n_cols
    for col, row, h in buildings:
        sil[col - 1] = max(sil[col - 1], h)
    return sil


def silhouette_east(buildings, n_rows):
    """東から見たシルエット (行ごとの最大高さ、北→南)"""
    sil = [0] * n_rows
    for col, row, h in buildings:
        sil[row - 1] = max(sil[row - 1], h)
    return sil


def verify_q1():
    """問1検証: 4x4グリッドの建物配置から南シルエットを求める"""
    # 建物配置: (col, row, height)
    # col: 1-4 (西→東), row: 1-4 (北→南)
    buildings = [
        (2, 2, 5),  # 管制塔
        (3, 3, 3),  # ターミナル
        (1, 4, 2),  # 格納庫A
        (4, 1, 2),  # 格納庫B
    ]
    sil = silhouette_south(buildings, 4)
    print(f"問1 南シルエット (西→東): {sil}")
    assert sil == [2, 5, 3, 2], f"期待値と異なる: {sil}"

    # 5つの選択肢のうち、正解は1つだけ
    options = [
        [2, 5, 3, 2],  # (1) 正解
        [2, 3, 5, 2],  # (2) 列2,3入れ替え
        [2, 2, 5, 3],  # (3) ずれ
        [3, 5, 2, 2],  # (4) 列1,3入れ替え
        [2, 5, 2, 3],  # (5) 列3,4入れ替え
    ]
    correct_indices = [i for i, opt in enumerate(options) if opt == sil]
    assert correct_indices == [0], f"正解が一意でない: {correct_indices}"
    print(f"問1 正解: 選択肢{correct_indices[0] + 1}")
    return True


def verify_q2():
    """問2検証: 南・東シルエットから4x4配置を特定"""
    # 与えられたシルエット
    south_given = [2, 5, 4, 3]  # 西→東
    east_given = [3, 5, 2, 4]   # 北→南

    # 4つの建物 (異なる高さ)
    heights = {
        '管制塔': 5,
        '旅客ターミナル': 4,
        '第2ターミナル': 3,
        '整備格納庫': 2,
    }

    # 全ての配置パターンを総当たり
    positions = [(c, r) for c in range(1, 5) for r in range(1, 5)]
    names = list(heights.keys())
    valid_configs = []
    for combo in permutations(positions, len(names)):
        buildings = [(combo[i][0], combo[i][1], heights[names[i]])
                     for i in range(len(names))]
        if (silhouette_south(buildings, 4) == south_given and
                silhouette_east(buildings, 4) == east_given):
            valid_configs.append(buildings)

    print(f"問2 有効な配置数: {len(valid_configs)}")
    assert len(valid_configs) == 1, f"配置が一意でない: {len(valid_configs)}個"

    config = valid_configs[0]
    print("問2 唯一の配置:")
    for i, name in enumerate(names):
        c, r, h = config[i]
        print(f"  {name}(高さ{h}): 列{c}, 行{r}")

    # 期待される配置
    expected = {
        '管制塔': (2, 2),
        '旅客ターミナル': (3, 4),
        '第2ターミナル': (4, 1),
        '整備格納庫': (1, 3),
    }
    for i, name in enumerate(names):
        c, r, _ = config[i]
        assert (c, r) == expected[name], f"{name}の位置が期待値と異なる"

    # 5つの選択肢
    options = [
        # (1) 第2ターミナルと整備格納庫の行を入れ替え
        {'管制塔': (2, 2), '旅客ターミナル': (3, 4),
         '第2ターミナル': (4, 4), '整備格納庫': (1, 1)},
        # (2) 旅客と第2ターミナルの位置を入れ替え
        {'管制塔': (2, 2), '旅客ターミナル': (4, 1),
         '第2ターミナル': (3, 4), '整備格納庫': (1, 3)},
        # (3) 正解
        {'管制塔': (2, 2), '旅客ターミナル': (3, 4),
         '第2ターミナル': (4, 1), '整備格納庫': (1, 3)},
        # (4) 整備格納庫の位置違い
        {'管制塔': (2, 2), '旅客ターミナル': (3, 4),
         '第2ターミナル': (4, 1), '整備格納庫': (1, 1)},
        # (5) 管制塔の位置違い
        {'管制塔': (2, 3), '旅客ターミナル': (3, 4),
         '第2ターミナル': (4, 1), '整備格納庫': (1, 2)},
    ]

    correct_indices = []
    for i, opt in enumerate(options):
        bldgs = [(opt[n][0], opt[n][1], heights[n]) for n in names]
        s = silhouette_south(bldgs, 4)
        e = silhouette_east(bldgs, 4)
        if s == south_given and e == east_given:
            correct_indices.append(i)
        print(f"  選択肢{i + 1}: 南={s}, 東={e}")

    assert correct_indices == [2], f"正解が一意でない: {correct_indices}"
    print(f"問2 正解: 選択肢{correct_indices[0] + 1}")
    return True


if __name__ == '__main__':
    verify_q1()
    print()
    verify_q2()
    print("\n=== すべての検証成功 ===")
