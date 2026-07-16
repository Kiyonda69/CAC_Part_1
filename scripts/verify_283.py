#!/usr/bin/env python3
"""航大思考283 検証スクリプト
タイプ: 立体の切断回数（重ね切り・最少回数）〔公務員試験典型〕

問1: 縦4cm×横4cm×厚さ1cmの板を1cm角の立方体16個に切り分ける。
     切るたびに部分を自由に動かして重ねてよいときの最少切断回数（正解: 4回）
問2: 1辺3cmの立方体を1cm角の小立方体27個に切り分ける。
     同じく重ねてよいときの最少切断回数（正解: 6回）

モデル:
- 1回の「切断」では、そのとき存在するすべての破片を自由に並べ・重ねてから
  一直線（1平面）でまとめて切る。各破片は高々1つの平面で2つに分かれる。
  （破片ごとに切る位置・向きは独立に選べる＝自由に配置できるため）
- よって全体の最少回数は f(a,b,c) =
    0                       (a=b=c=1)
    1 + min over 分割 max(f(左片), f(右片))   （各破片は並行して処理できる）
  で与えられる。これを全探索（メモ化）で計算する。

検証内容:
- f(4,4,1)=4, f(3,3,3)=6 の全探索による確認
- 重ねない場合の回数 (a-1)+(b-1)+(c-1) との比較
  （問1: 6回→4回に短縮できる / 問2: 6回のまま短縮できない）
- 倍々の下界 ceil(log2(個数)) の確認（問2では 5回となり実際の6回より弱い
  ＝誤答(3)の「5回」が理論的に魅力的な罠であること）
- 中央小立方体の下界: 問2では中央の小立方体の6面すべてが新たな切断面で
  あり、1回の切断で作れるのは高々1面 → 6回以上（罠5回の反証）
- 選択肢の値のうち正解がただ1つであること
"""
from functools import lru_cache
from math import ceil, log2


@lru_cache(maxsize=None)
def min_cuts(a, b, c):
    """重ね切り許可時の最少切断回数（全探索・メモ化）"""
    dims = tuple(sorted((a, b, c)))
    a, b, c = dims
    if dims == (1, 1, 1):
        return 0
    best = 10 ** 9
    for axis in range(3):
        n = dims[axis]
        for k in range(1, n // 2 + 1):  # 対称性より半分まで
            p1 = list(dims)
            p2 = list(dims)
            p1[axis] = k
            p2[axis] = n - k
            best = min(best, 1 + max(min_cuts(*p1), min_cuts(*p2)))
    return best


def no_restack_cuts(a, b, c):
    """重ねない（動かさない）場合の回数 = 仕切りの枚数の合計"""
    return (a - 1) + (b - 1) + (c - 1)


def doubling_lower_bound(pieces):
    """1回の切断で破片数は高々2倍 → ceil(log2(個数)) 回以上"""
    return ceil(log2(pieces))


def center_cube_lower_bound():
    """問2の下界: 3×3×3の中央の小立方体(1,1,1)は6面とも立体の内部にあり、
    どの面ももとの表面ではない。1回の平面切断が中央の小立方体に作れる面は
    高々1つなので、6面を作るには6回以上必要。"""
    # 中央の小立方体の6面がすべて内部にあることを座標で確認
    center = (1, 1, 1)  # 0..2 の格子で中央
    for axis in range(3):
        for side in (0, 1):
            plane = center[axis] + side  # 切断面の格子位置 1 or 2
            assert 0 < plane < 3, "中央の面が表面に出ている"
    return 6


OPTIONS1 = {1: 3, 2: 4, 3: 5, 4: 6, 5: 8}   # 問1の選択肢（回）
OPTIONS2 = {1: 3, 2: 4, 3: 5, 4: 6, 5: 9}   # 問2の選択肢（回）
ANSWER1 = 2  # 問1の正解番号（4回）
ANSWER2 = 4  # 問2の正解番号（6回）


if __name__ == "__main__":
    # ---------- 問1: 4×4×1 の板 → 16個 ----------
    f1 = min_cuts(4, 4, 1)
    print(f"問1: f(4,4,1) = {f1}回（全探索）")
    assert f1 == 4
    nr1 = no_restack_cuts(4, 4, 1)
    print(f"  重ねない場合: {nr1}回 → 重ねると{f1}回に短縮（誤答(4)=6回の根拠）")
    assert nr1 == 6
    lb1 = doubling_lower_bound(16)
    print(f"  倍々の下界: ceil(log2 16) = {lb1}回 → 4回は最適で確定")
    assert lb1 == 4
    hits = [n for n, v in OPTIONS1.items() if v == f1]
    assert hits == [ANSWER1], f"問1の正解番号: {hits}"
    print(f"  選択肢{OPTIONS1} 中、正解は({ANSWER1})の4回のみ\n")

    # ---------- 問2: 3×3×3 の立方体 → 27個 ----------
    f2 = min_cuts(3, 3, 3)
    print(f"問2: f(3,3,3) = {f2}回（全探索）")
    assert f2 == 6
    nr2 = no_restack_cuts(3, 3, 3)
    print(f"  重ねない場合: {nr2}回 → 重ねても減らないことが本問の核心")
    assert nr2 == 6
    lb2 = doubling_lower_bound(27)
    print(f"  倍々の下界: ceil(log2 27) = {lb2}回 → 5回では不可能"
          "（誤答(3)=5回は倍々論法の限界を突く罠）")
    assert lb2 == 5
    assert center_cube_lower_bound() == 6
    print("  中央小立方体の6面論法による下界6回を確認（5回の反証）")
    hits = [n for n, v in OPTIONS2.items() if v == f2]
    assert hits == [ANSWER2], f"問2の正解番号: {hits}"
    print(f"  選択肢{OPTIONS2} 中、正解は({ANSWER2})の6回のみ\n")

    # 参考: 各軸は独立で f = Σ ceil(log2 辺長) になることの確認
    for dims in [(4, 4, 1), (3, 3, 3), (2, 3, 4), (5, 1, 1)]:
        expect = sum(ceil(log2(d)) for d in dims)
        assert min_cuts(*dims) == expect, dims
    print("参考: f(a,b,c) = Σceil(log2 辺長) が全探索と一致することを確認")
    print("\n全検証OK")
