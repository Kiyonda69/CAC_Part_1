"""
航大思考2 検証スクリプト
問1: 図形マトリクスの規則性（3属性の循環規則）
問2: 白黒パターン行列のXOR規則
"""


def verify_q1():
    """
    問1: 図形マトリクスの規則性

    3×3マトリクスの各セルには3つの属性がある:
    - 形: circle(○), triangle(△), square(□)
    - 塗り: empty(空), striped(斜線), solid(黒)
    - 点の数: 1, 2, 3

    規則:
    - 形: 行ごとに巡回シフト (R1: ○△□, R2: □○△, R3: △□○)
    - 塗り: 行ごとに巡回シフト (R1: 空斜黒, R2: 斜黒空, R3: 黒空斜)
    - 点: ラテン方陣 (R1: 1,2,3  R2: 3,1,2  R3: 2,3,?)

    各行・各列にそれぞれの属性が1つずつ出現する（ラテン方陣構造）
    """
    shapes = ['circle', 'triangle', 'square']
    fills = ['empty', 'striped', 'solid']
    dots = [1, 2, 3]

    # マトリクス定義 (行, 列) → (形, 塗り, 点)
    matrix = {
        (0, 0): ('circle',   'empty',   1),
        (0, 1): ('triangle', 'striped', 2),
        (0, 2): ('square',   'solid',   3),
        (1, 0): ('square',   'striped', 3),
        (1, 1): ('circle',   'solid',   1),
        (1, 2): ('triangle', 'empty',   2),
        (2, 0): ('triangle', 'solid',   2),
        (2, 1): ('square',   'empty',   3),
        # (2, 2) is unknown
    }

    # 全組み合わせを総当たり
    valid = []
    for s in shapes:
        for f in fills:
            for d in dots:
                candidate = (s, f, d)
                ok = True

                # 行チェック: 行2の形は {triangle, square, ?}
                row2_shapes = [matrix[(2, 0)][0], matrix[(2, 1)][0]]
                row2_fills = [matrix[(2, 0)][1], matrix[(2, 1)][1]]
                row2_dots = [matrix[(2, 0)][2], matrix[(2, 1)][2]]

                if s in row2_shapes:
                    ok = False
                if f in row2_fills:
                    ok = False
                if d in row2_dots:
                    ok = False

                # 列チェック: 列2の形は {square, triangle, ?}
                col2_shapes = [matrix[(0, 2)][0], matrix[(1, 2)][0]]
                col2_fills = [matrix[(0, 2)][1], matrix[(1, 2)][1]]
                col2_dots = [matrix[(0, 2)][2], matrix[(1, 2)][2]]

                if s in col2_shapes:
                    ok = False
                if f in col2_fills:
                    ok = False
                if d in col2_dots:
                    ok = False

                if ok:
                    valid.append(candidate)

    assert len(valid) == 1, f"解が{len(valid)}個: {valid}"
    answer = valid[0]
    print(f"問1 正解: 形={answer[0]}, 塗り={answer[1]}, 点={answer[2]}")
    assert answer == ('circle', 'striped', 1), f"期待と異なる: {answer}"

    # マトリクスの全行・全列を検証
    matrix[(2, 2)] = answer
    for r in range(3):
        row_shapes = set(matrix[(r, c)][0] for c in range(3))
        row_fills = set(matrix[(r, c)][1] for c in range(3))
        row_dots = set(matrix[(r, c)][2] for c in range(3))
        assert row_shapes == set(shapes), f"行{r}の形が不正: {row_shapes}"
        assert row_fills == set(fills), f"行{r}の塗りが不正: {row_fills}"
        assert row_dots == set(dots), f"行{r}の点が不正: {row_dots}"

    for c in range(3):
        col_shapes = set(matrix[(r, c)][0] for r in range(3))
        col_fills = set(matrix[(r, c)][1] for r in range(3))
        col_dots = set(matrix[(r, c)][2] for r in range(3))
        assert col_shapes == set(shapes), f"列{c}の形が不正: {col_shapes}"
        assert col_fills == set(fills), f"列{c}の塗りが不正: {col_fills}"
        assert col_dots == set(dots), f"列{c}の点が不正: {col_dots}"

    print("問1 検証完了: 解は唯一で全規則を満たす")
    return answer


def verify_q2():
    """
    問2: 白黒パターン行列のXOR規則

    3×3マトリクスの各セルに3×3の白黒パターンを配置
    規則: 各行の3番目 = 1番目 XOR 2番目
          各列の3番目 = 1番目 XOR 2番目

    XOR: 両方同じ色→白、異なる色→黒
    """

    def xor_grid(a, b):
        return [[a[i][j] ^ b[i][j] for j in range(3)] for i in range(3)]

    def grids_equal(a, b):
        return all(a[i][j] == b[i][j] for i in range(3) for j in range(3))

    # マトリクス定義
    A = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]  # X pattern
    B = [[0, 1, 0], [1, 0, 1], [0, 0, 1]]
    C = xor_grid(A, B)  # = [[1,1,1],[1,1,1],[1,0,0]]

    D = [[1, 1, 0], [1, 0, 0], [0, 1, 0]]
    E = [[0, 0, 1], [1, 1, 0], [0, 1, 1]]
    F = xor_grid(D, E)  # = [[1,1,1],[0,1,0],[0,0,1]]

    G = xor_grid(A, D)  # = [[0,1,1],[1,1,0],[1,1,1]]
    H = xor_grid(B, E)  # = [[0,1,1],[0,1,1],[0,1,0]]

    # 答え: 行方向と列方向の両方で計算
    I_from_row = xor_grid(G, H)
    I_from_col = xor_grid(C, F)

    # 両方が一致することを確認
    assert grids_equal(I_from_row, I_from_col), \
        f"行方向と列方向の結果が不一致!\n行: {I_from_row}\n列: {I_from_col}"

    answer = I_from_row
    print(f"問2 正解パターン:")
    symbols = {0: '□', 1: '■'}
    for row in answer:
        print("  " + " ".join(symbols[c] for c in row))

    # 期待値の確認
    expected = [[0, 0, 0], [1, 0, 1], [1, 0, 1]]
    assert grids_equal(answer, expected), f"期待と異なる: {answer}"

    # 全行のXOR規則を検証
    matrix = [
        [A, B, C],
        [D, E, F],
        [G, H, answer]
    ]

    for r in range(3):
        xor_result = xor_grid(matrix[r][0], matrix[r][1])
        assert grids_equal(xor_result, matrix[r][2]), \
            f"行{r}のXOR規則が不正"

    for c in range(3):
        xor_result = xor_grid(matrix[0][c], matrix[1][c])
        assert grids_equal(xor_result, matrix[2][c]), \
            f"列{c}のXOR規則が不正"

    # 解の一意性: (2,2)を総当たりで確認
    valid_count = 0
    for mask in range(512):  # 2^9 = 512 通り
        candidate = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                candidate[i][j] = (mask >> (i * 3 + j)) & 1

        # 行方向チェック: G XOR H == candidate
        if not grids_equal(xor_grid(G, H), candidate):
            continue
        # 列方向チェック: C XOR F == candidate
        if not grids_equal(xor_grid(C, F), candidate):
            continue
        valid_count += 1

    assert valid_count == 1, f"解が{valid_count}個存在"

    # 選択肢の検証（全て異なることを確認）
    choices = [
        [[0, 0, 0], [1, 0, 1], [1, 0, 1]],  # 正解
        [[1, 0, 1], [0, 0, 0], [1, 0, 1]],  # 行シフト
        [[0, 0, 0], [1, 1, 1], [1, 0, 1]],  # 中央行が異なる
        [[1, 0, 1], [1, 0, 1], [0, 0, 0]],  # 上下反転
        [[0, 1, 0], [1, 0, 1], [1, 0, 1]],  # 上段が異なる
    ]

    # 正解が選択肢に含まれることを確認
    assert grids_equal(choices[0], answer), "正解が選択肢1でない"

    # 全選択肢が互いに異なることを確認
    for i in range(len(choices)):
        for j in range(i + 1, len(choices)):
            assert not grids_equal(choices[i], choices[j]), \
                f"選択肢{i+1}と{j+1}が同一"

    # 不正解の選択肢がXOR規則を満たさないことを確認
    for idx in range(1, len(choices)):
        satisfies_row = grids_equal(xor_grid(G, H), choices[idx])
        satisfies_col = grids_equal(xor_grid(C, F), choices[idx])
        assert not (satisfies_row and satisfies_col), \
            f"選択肢{idx+1}も正解になってしまう"

    print("問2 検証完了: 解は唯一で全規則を満たす")
    return answer


if __name__ == "__main__":
    print("=" * 50)
    print("航大思考2 検証")
    print("=" * 50)
    print()
    verify_q1()
    print()
    verify_q2()
    print()
    print("全検証パス!")
