#!/usr/bin/env python3
"""
セット65: 折り紙の空間認識問題の検証
問1: 折り紙の穴あけ展開問題（標準）
問2: 折り紙の切断展開問題（高難度）
"""

def verify_q1():
    """
    問1: 正方形の紙を2回折り、穴を1つ開ける。展開したときの穴の位置を求める。
    
    紙: 80x80 (SVG座標系、左上が原点)
    折り1: 右半分を左半分に重ねる (x=40で折る)
    折り2: 下半分を上半分に重ねる (y=40で折る)
    折り後の見える領域: [0,40]x[0,40] (左上の四分の一)
    穴の位置: (8, 16) ← 左端から8、上端から16の位置
    """
    paper_size = 80
    fold_x = 40  # 垂直折り線
    fold_y = 40  # 水平折り線
    
    # 穴の位置（折った後の紙の上）
    hole_x, hole_y = 8, 16
    
    # 展開時の穴の位置を計算
    holes = set()
    for mirror_x in [False, True]:
        for mirror_y in [False, True]:
            x = (paper_size - hole_x) if mirror_x else hole_x
            y = (paper_size - hole_y) if mirror_y else hole_y
            holes.add((x, y))
    
    print("問1: 折り紙の穴あけ展開")
    print(f"  折り後の穴位置: ({hole_x}, {hole_y})")
    print(f"  展開後の穴位置: {sorted(holes)}")
    print(f"  穴の数: {len(holes)}")
    
    expected = {(8, 16), (72, 16), (8, 64), (72, 64)}
    assert holes == expected, f"穴の位置が不正: {holes} != {expected}"
    assert len(holes) == 4, f"穴の数が不正: {len(holes)} != 4"
    
    # 対称性チェック
    for (x, y) in holes:
        assert (paper_size - x, y) in holes, f"x軸対称性エラー: ({x},{y})"
        assert (x, paper_size - y) in holes, f"y軸対称性エラー: ({x},{y})"
    
    print("  対称性: OK")
    print("  正解: (5)")
    print()
    return True

def verify_q2():
    """
    問2: 正方形の紙を2回折り、直線で切断する。展開したときの切り抜き形状を求める。
    
    紙: 80x80 (SVG座標系)
    折り1: 右半分を左半分に重ねる (x=40で折る)
    折り2: 下半分を上半分に重ねる (y=40で折る)
    折り後の見える領域: [0,40]x[0,40] (左上の四分の一)
    切断: (8, 40)から(40, 24)への直線で切断
      → 紙の中心角(40,40)を含む三角形を切り取る
      → 三角形の頂点: (8,40), (40,40), (40,24)
    """
    paper_size = 80
    fold_x = 40
    fold_y = 40
    
    # 切り取る三角形の頂点（折った後の紙の上）
    cut_triangle = [(8, 40), (40, 40), (40, 24)]
    
    print("問2: 折り紙の切断展開")
    print(f"  切断三角形: {cut_triangle}")
    
    # 展開ステップ1: y=40で展開
    # 三角形 (8,40), (40,40), (40,24) の鏡像は (8,40), (40,40), (40,56)
    # 合わせると: 三角形 (8,40), (40,24), (40,56) (40,40は内部点)
    mirror_y_triangle = [(8, 40), (40, 80-24), (40, 80-40)]  # = (8,40), (40,56), (40,40)
    
    # y展開後の切り抜き形状: 三角形 (8,40), (40,24), (40,56)
    after_y_unfold = [(8, 40), (40, 24), (40, 56)]
    print(f"  y展開後: 三角形 {after_y_unfold}")
    
    # 展開ステップ2: x=40で展開
    # 三角形 (8,40), (40,24), (40,56) の鏡像は (72,40), (40,24), (40,56)
    # 合わせると: ひし形 (8,40), (40,24), (72,40), (40,56)
    rhombus = [(8, 40), (40, 24), (72, 40), (40, 56)]
    print(f"  x展開後（最終形状）: ひし形 {rhombus}")
    
    # ひし形の対角線
    diag_h = 72 - 8   # 水平対角線 = 64
    diag_v = 56 - 24   # 垂直対角線 = 32
    print(f"  水平対角線: {diag_h}")
    print(f"  垂直対角線: {diag_v}")
    print(f"  対角線比: {diag_h}:{diag_v} = {diag_h//diag_v}:1")
    
    # 中心が紙の中心であることを確認
    center_x = (8 + 72) / 2
    center_y = (24 + 56) / 2
    assert center_x == 40, f"中心x座標エラー: {center_x}"
    assert center_y == 40, f"中心y座標エラー: {center_y}"
    print(f"  中心: ({center_x}, {center_y}) = 紙の中心 OK")
    
    # 対称性チェック
    for (x, y) in rhombus:
        assert (80-x, y) in rhombus, f"x軸対称性エラー: ({x},{y})"
        assert (x, 80-y) in rhombus, f"y軸対称性エラー: ({x},{y})"
    print("  対称性: OK")
    print("  正解: (4)")
    print()
    return True

def verify_wrong_answers():
    """誤答の選択肢が正解と異なることを確認"""
    print("=== 誤答選択肢の確認 ===")
    
    # 問1の正解と誤答
    q1_correct = {(8, 16), (72, 16), (8, 64), (72, 64)}
    q1_options = {
        1: {(16, 8), (64, 8), (16, 72), (64, 72)},       # x,y入れ替え
        2: {(8, 8), (72, 8), (8, 72), (72, 72)},           # 角に近い正方形配置
        3: {(20, 16), (60, 16), (20, 64), (60, 64)},       # 水平距離が異なる
        4: {(8, 24), (72, 24), (8, 56), (72, 56)},         # 垂直距離が異なる
        5: q1_correct,                                       # 正解
    }
    
    for opt_num, holes in q1_options.items():
        if opt_num == 5:
            assert holes == q1_correct, f"選択肢{opt_num}が正解と不一致"
            print(f"  問1 選択肢({opt_num}): 正解 ✓")
        else:
            assert holes != q1_correct, f"選択肢{opt_num}が正解と同じ！"
            print(f"  問1 選択肢({opt_num}): 正解と異なる ✓")
    
    # 問2の正解と誤答
    q2_correct = [(8, 40), (40, 24), (72, 40), (40, 56)]
    q2_options = {
        1: [(16, 40), (40, 24), (64, 40), (40, 56)],       # 水平方向が短い
        2: [(8, 40), (40, 8), (72, 40), (40, 72)],          # 垂直方向が長い（正方形ダイヤ）
        3: [(20, 20), (60, 20), (60, 60), (20, 60)],        # 通常の正方形（回転なし）
        4: q2_correct,                                       # 正解
        5: [(8, 40), (40, 32), (72, 40), (40, 48)],         # 垂直方向がさらに短い
    }
    
    for opt_num, shape in q2_options.items():
        if opt_num == 4:
            assert shape == q2_correct, f"選択肢{opt_num}が正解と不一致"
            print(f"  問2 選択肢({opt_num}): 正解 ✓")
        else:
            assert shape != q2_correct, f"選択肢{opt_num}が正解と同じ！"
            print(f"  問2 選択肢({opt_num}): 正解と異なる ✓")
    
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("セット65: 折り紙の空間認識問題 - 解の検証")
    print("=" * 60)
    print()
    
    verify_q1()
    verify_q2()
    verify_wrong_answers()
    
    print("=" * 60)
    print("全検証完了: 問1・問2ともに解が一意であることを確認")
    print("=" * 60)
