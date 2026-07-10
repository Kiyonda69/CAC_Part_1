#!/usr/bin/env python3
"""航大思考266 検証スクリプト: 折り紙のパンチ穴問題

紙は4x4グリッド（座標は穴の中心、x:0.5〜3.5, y:0.5〜3.5、yは上向き）。
折りは反射変換としてモデル化し、逆順に展開して穴の位置を全列挙する。
"""


def unfold(holes, fold):
    """holes: set of (x, y). fold: 展開時に穴を複製する反射変換"""
    new = set(holes)
    for (x, y) in holes:
        new.add(fold(x, y))
    return new


def q1():
    # 問1: 右半分を左へ折る(x=2で反射) → 下半分を上へ折る(y=2で反射)
    # 折った状態([0,2]x[2,4])で (1.5, 3.5) に1穴パンチ
    holes = {(1.5, 3.5)}
    # 展開は逆順: まず y=2 の折りを開き、次に x=2 の折りを開く
    holes = unfold(holes, lambda x, y: (x, 4 - y))
    holes = unfold(holes, lambda x, y: (4 - x, y))
    expected = {(1.5, 3.5), (2.5, 3.5), (1.5, 0.5), (2.5, 0.5)}
    assert holes == expected, f"問1不一致: {sorted(holes)}"
    print(f"問1 OK: 穴{len(holes)}個 {sorted(holes)}")
    return holes


def q2():
    # 問2: 上半分を下へ折る(y=2で反射) → 右半分を左へ折る(x=2で反射)
    # → 対角線 y=x で左上の三角形を右下へ折る((x,y)->(y,x))
    # 折った状態(三角形 y<=x, [0,2]^2)で (1.5, 0.5) に1穴パンチ
    holes = {(1.5, 0.5)}
    holes = unfold(holes, lambda x, y: (y, x))        # 対角線を開く
    holes = unfold(holes, lambda x, y: (4 - x, y))    # x=2 を開く
    holes = unfold(holes, lambda x, y: (x, 4 - y))    # y=2 を開く
    expected = {(1.5, 0.5), (0.5, 1.5), (2.5, 0.5), (3.5, 1.5),
                (1.5, 3.5), (0.5, 2.5), (2.5, 3.5), (3.5, 2.5)}
    assert holes == expected, f"問2不一致: {sorted(holes)}"
    print(f"問2 OK: 穴{len(holes)}個 {sorted(holes)}")
    return holes


def check_distractors(correct, distractors, label):
    """誤答選択肢が正解と一致しないこと・互いに異なることを確認"""
    all_opts = [correct] + distractors
    for i in range(len(all_opts)):
        for j in range(i + 1, len(all_opts)):
            assert all_opts[i] != all_opts[j], f"{label}: 選択肢{i+1}と{j+1}が同一"
    print(f"{label}: 全5選択肢が互いに異なることを確認")


if __name__ == "__main__":
    h1 = q1()
    # 問1の誤答: 展開忘れ(2穴) / 平行移動ミス / 反射軸ミス / 四隅
    d1 = [
        {(1.5, 3.5), (2.5, 3.5)},
        {(0.5, 3.5), (1.5, 3.5), (0.5, 0.5), (1.5, 0.5)},
        {(1.5, 3.5), (2.5, 3.5), (1.5, 2.5), (2.5, 2.5)},
        {(0.5, 0.5), (3.5, 0.5), (0.5, 3.5), (3.5, 3.5)},
    ]
    check_distractors(h1, d1, "問1")

    h2 = q2()
    # 問2の誤答: 対角展開忘れ(4穴) / 対角を平行移動扱い / 8穴だが配置ミス / 6穴
    d2 = [
        {(1.5, 0.5), (2.5, 0.5), (1.5, 3.5), (2.5, 3.5)},
        {(1.5, 0.5), (1.5, 1.5), (2.5, 0.5), (2.5, 1.5),
         (1.5, 3.5), (1.5, 2.5), (2.5, 3.5), (2.5, 2.5)},
        {(0.5, 0.5), (1.5, 1.5), (2.5, 1.5), (3.5, 0.5),
         (0.5, 3.5), (1.5, 2.5), (2.5, 2.5), (3.5, 3.5)},
        {(1.5, 0.5), (0.5, 1.5), (2.5, 0.5), (1.5, 3.5), (0.5, 2.5), (2.5, 3.5)},
    ]
    check_distractors(h2, d2, "問2")
    print("検証完了: 両問とも解は一意に定まる")
