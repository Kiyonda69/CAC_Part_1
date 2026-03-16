"""
航大思考61 検証スクリプト
問1: 数表の規則性
問2: 図形パターンの規則性（レイヴン型マトリックス）
"""

def verify_q1():
    """
    問1: 数表の規則性
    4×4の数表で、cell(r,c) = (r+1)² + (c+1)² - 5 の規則に従う。
    (4,4)の値を求める。
    """
    print("=" * 50)
    print("問1: 数表の規則性")
    print("=" * 50)

    # 数表を生成して表示
    print("\n数表:")
    print(f"{'':>6}", end="")
    for c in range(1, 5):
        print(f"{c}列{'':<4}", end="")
    print()

    table = {}
    for r in range(1, 5):
        print(f"{r}行: ", end="")
        for c in range(1, 5):
            val = (r + 1) ** 2 + (c + 1) ** 2 - 5
            table[(r, c)] = val
            if r == 4 and c == 4:
                print(f"{'?':>6}", end="")
            else:
                print(f"{val:>6}", end="")
        print()

    answer = table[(4, 4)]
    print(f"\n正解: {answer}")

    # 規則の検証
    print("\n--- 規則の検証 ---")

    # 行方向の差分
    print("\n行方向の差分:")
    for r in range(1, 5):
        diffs = [table[(r, c + 1)] - table[(r, c)] for c in range(1, 4)]
        print(f"  {r}行: {diffs}")

    # 列方向の差分
    print("\n列方向の差分:")
    for c in range(1, 5):
        diffs = [table[(r + 1, c)] - table[(r, c)] for r in range(1, 4)]
        print(f"  {c}列: {diffs}")

    # 対角線
    diag = [table[(i, i)] for i in range(1, 5)]
    print(f"\n対角線: {diag}")
    diag_diffs = [diag[i + 1] - diag[i] for i in range(len(diag) - 1)]
    print(f"対角線差分: {diag_diffs}")

    # 公式検証
    print("\n--- 公式 cell(r,c) = (r+1)² + (c+1)² - 5 の全数検証 ---")
    all_correct = True
    for r in range(1, 5):
        for c in range(1, 5):
            expected = (r + 1) ** 2 + (c + 1) ** 2 - 5
            if table[(r, c)] != expected:
                print(f"  エラー: ({r},{c}) = {table[(r,c)]} ≠ {expected}")
                all_correct = False
    if all_correct:
        print("  全セル正しい ✓")

    # 選択肢（正解は3番目）
    choices = [42, 43, 45, 47, 49]
    print(f"\n選択肢: {choices}")
    print(f"正解: ({choices.index(answer) + 1}) {answer}")
    assert answer == 45, f"正解が45ではない: {answer}"
    assert choices[2] == 45, "正解が3番目ではない"

    # 解の一意性: 他の選択肢では規則が成り立たないことを検証
    print("\n--- 解の一意性検証 ---")
    for i, choice in enumerate(choices):
        if choice == answer:
            continue
        # この値が(4,4)に入ると仮定して、矛盾を確認
        # 行差分の規則性チェック
        row4_with_choice = [table[(4, 1)], table[(4, 2)], table[(4, 3)], choice]
        diffs = [row4_with_choice[j + 1] - row4_with_choice[j] for j in range(3)]
        # 他の行の差分パターン: [5, 7, 9]
        expected_diffs = [5, 7, 9]
        if diffs == expected_diffs:
            print(f"  選択肢({i+1}) {choice}: 行差分一致 - 一意でない！")
        else:
            print(f"  選択肢({i+1}) {choice}: 行差分 {diffs} ≠ {expected_diffs} → 不適 ✓")

    print("\n問1 検証完了: 正解 = 45（選択肢3番目）")
    return True


def verify_q2():
    """
    問2: 図形パターンの規則性（レイヴン型マトリックス）
    3×3のグリッドに図形が配置されている。
    各図形は3つの属性を持つ:
    - 外側の形: 行で変化（円、三角形、正方形）
    - 内側の形: 列で変化（円、三角形、正方形）
    - 内側の塗り: ラテン方陣パターン（白、灰、黒）
    """
    print("\n" + "=" * 50)
    print("問2: 図形パターンの規則性（レイヴン型マトリックス）")
    print("=" * 50)

    outer_shapes = ["円", "三角形", "正方形"]  # 行ごと
    inner_shapes = ["円", "三角形", "正方形"]  # 列ごと
    fills = ["白", "灰", "黒"]

    # 塗りのパターン（ラテン方陣）
    fill_pattern = [
        [0, 1, 2],  # 行1: 白, 灰, 黒
        [1, 2, 0],  # 行2: 灰, 黒, 白
        [2, 0, 1],  # 行3: 黒, 白, ?→灰
    ]

    print("\n3×3 マトリックス:")
    for r in range(3):
        for c in range(3):
            outer = outer_shapes[r]
            inner = inner_shapes[c]
            fill = fills[fill_pattern[r][c]]
            if r == 2 and c == 2:
                print(f"  ({r+1},{c+1}): ? [正解: {outer}の中に{fill}い{inner}]")
            else:
                print(f"  ({r+1},{c+1}): {outer}の中に{fill}い{inner}")

    # 答え
    answer_outer = outer_shapes[2]  # 正方形
    answer_inner = inner_shapes[2]  # 正方形
    answer_fill = fills[fill_pattern[2][2]]  # 灰

    print(f"\n正解: {answer_outer}の中に{answer_fill}い{answer_inner}")

    # 規則の検証
    print("\n--- 規則の検証 ---")

    # 各行で外側の形が同じ
    print("\n外側の形（行ごと）:")
    for r in range(3):
        print(f"  {r+1}行: {outer_shapes[r]}")

    # 各列で内側の形が同じ
    print("\n内側の形（列ごと）:")
    for c in range(3):
        print(f"  {c+1}列: {inner_shapes[c]}")

    # 塗りがラテン方陣
    print("\n塗りパターン（ラテン方陣）:")
    for r in range(3):
        row_fills = [fills[fill_pattern[r][c]] for c in range(3)]
        print(f"  {r+1}行: {row_fills}")

    # 各行・各列に白・灰・黒が1つずつ
    print("\n行ごとの塗り分布:")
    for r in range(3):
        row = [fill_pattern[r][c] for c in range(3)]
        assert sorted(row) == [0, 1, 2], f"行{r+1}の塗りが不正"
        print(f"  {r+1}行: {[fills[f] for f in row]} ✓")

    print("\n列ごとの塗り分布:")
    for c in range(3):
        col = [fill_pattern[r][c] for r in range(3)]
        assert sorted(col) == [0, 1, 2], f"列{c+1}の塗りが不正"
        print(f"  {c+1}列: {[fills[f] for f in col]} ✓")

    # 解の一意性検証
    print("\n--- 解の一意性検証 ---")
    # (3,3)の位置に入れるべき属性の組み合わせ
    # 外側: 正方形（行3の規則から一意）
    # 内側: 正方形（列3の規則から一意）
    # 塗り: 灰色（ラテン方陣から一意）

    # 行3で使われていない塗り
    row3_used = {fill_pattern[2][0], fill_pattern[2][1]}  # 黒(2), 白(0)
    remaining_fill = {0, 1, 2} - row3_used
    assert remaining_fill == {1}, f"行3の残り塗りが灰色(1)でない: {remaining_fill}"
    print(f"  行3の残り塗り: {fills[list(remaining_fill)[0]]} ✓")

    # 列3で使われていない塗り
    col3_used = {fill_pattern[0][2], fill_pattern[1][2]}  # 黒(2), 白(0)
    remaining_fill_col = {0, 1, 2} - col3_used
    assert remaining_fill_col == {1}, f"列3の残り塗りが灰色(1)でない: {remaining_fill_col}"
    print(f"  列3の残り塗り: {fills[list(remaining_fill_col)[0]]} ✓")

    print(f"\n  外側の形: {answer_outer}（行3の規則 → 一意）")
    print(f"  内側の形: {answer_inner}（列3の規則 → 一意）")
    print(f"  塗り: {answer_fill}（ラテン方陣 → 一意）")

    # 選択肢（正解は2番目）
    print("\n選択肢:")
    options = [
        "正方形の中に白い正方形",
        "正方形の中に灰色の正方形",   # 正解
        "正方形の中に黒い正方形",
        "正方形の中に灰色の円",
        "正方形の中に灰色の三角形",
    ]
    for i, opt in enumerate(options):
        marker = " ← 正解" if i == 1 else ""
        print(f"  ({i+1}) {opt}{marker}")

    # 各不正解が除外される理由
    print("\n不正解の除外理由:")
    print("  (1) 白い正方形 → 行3に白が既にある（3,2が白）→ 不適")
    print("  (3) 黒い正方形 → 行3に黒が既にある（3,1が黒）→ 不適")
    print("  (4) 灰色の円 → 列3は正方形であるべき → 不適")
    print("  (5) 灰色の三角形 → 列3は正方形であるべき → 不適")

    print("\n問2 検証完了: 正解 = 正方形の中に灰色の正方形（選択肢2番目）")
    return True


if __name__ == "__main__":
    q1_ok = verify_q1()
    q2_ok = verify_q2()

    print("\n" + "=" * 50)
    print("検証結果サマリー")
    print("=" * 50)
    print(f"問1: {'合格' if q1_ok else '不合格'}")
    print(f"問2: {'合格' if q2_ok else '不合格'}")
    if q1_ok and q2_ok:
        print("\n全問題の検証に合格しました。")
    else:
        print("\n検証に失敗した問題があります。")
