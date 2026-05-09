"""
verify_164.py - 立方体の展開図問題の検証

問1: 立方体ABCD-EFGHの上面に対角線BDを引いたとき、
     十字型の展開図のどこに現れるか。

問2: 上面の対角線A→Cと右面の対角線C→Fが描かれているとき、
     展開図でこれらの線分はどの位置に現れるか。
"""

# 立方体の頂点を3D座標で定義
# 上面: ABCD (A=手前左, B=手前右, C=奥右, D=奥左)
# 下面: EFGH (E=手前左, F=手前右, G=奥右, H=奥左)
vertices = {
    'A': (0, 0, 1),
    'B': (1, 0, 1),
    'C': (1, 1, 1),
    'D': (0, 1, 1),
    'E': (0, 0, 0),
    'F': (1, 0, 0),
    'G': (1, 1, 0),
    'H': (0, 1, 0),
}

# 各面の頂点（順序は反時計回り）
faces = {
    'top':    ['A', 'B', 'C', 'D'],
    'bottom': ['E', 'F', 'G', 'H'],
    'front':  ['A', 'B', 'F', 'E'],
    'back':   ['C', 'D', 'H', 'G'],
    'left':   ['D', 'A', 'E', 'H'],
    'right':  ['B', 'C', 'G', 'F'],
}

# 十字型展開図の各パネルの2D座標（パネルサイズ=1）
# 中央: front
# front の上: top（上に展開）
# front の下: bottom（下に展開）
# front の左: left（左に展開）
# front の右: right（右に展開）
# right の右: back（さらに右に展開）
#
# パネルの左下を原点として、各頂点が展開後にどの位置に来るか
# Y軸は下向きが正（SVGに合わせる）
panels_2d = {
    # 上パネル: TL=D(0,0), TR=C(1,0), BL=A(0,1), BR=B(1,1)
    'top':    {'D': (1, 0), 'C': (2, 0), 'A': (1, 1), 'B': (2, 1)},
    # 左パネル: TL=D(0,1), TR=A(1,1), BL=H(0,2), BR=E(1,2)
    'left':   {'D': (0, 1), 'A': (1, 1), 'H': (0, 2), 'E': (1, 2)},
    # 前パネル: TL=A(1,1), TR=B(2,1), BL=E(1,2), BR=F(2,2)
    'front':  {'A': (1, 1), 'B': (2, 1), 'E': (1, 2), 'F': (2, 2)},
    # 右パネル: TL=B(2,1), TR=C(3,1), BL=F(2,2), BR=G(3,2)
    'right':  {'B': (2, 1), 'C': (3, 1), 'F': (2, 2), 'G': (3, 2)},
    # 後パネル: TL=C(3,1), TR=D(4,1), BL=G(3,2), BR=H(4,2)
    'back':   {'C': (3, 1), 'D': (4, 1), 'G': (3, 2), 'H': (4, 2)},
    # 下パネル: TL=E(1,2), TR=F(2,2), BL=H(1,3), BR=G(2,3)
    'bottom': {'E': (1, 2), 'F': (2, 2), 'H': (1, 3), 'G': (2, 3)},
}


def get_diagonal_type(panel, v1, v2):
    """パネル内の2頂点を結ぶ線が "/" か "\" か判定"""
    p1 = panels_2d[panel][v1]
    p2 = panels_2d[panel][v2]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0 or dy == 0:
        return 'edge'  # 辺
    # 同じ符号なら"\"、異なる符号なら"/"
    if (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
        return '\\'  # 左上から右下
    else:
        return '/'  # 左下から右上


def verify_q1():
    """問1: 上面の対角線BDの位置を確認"""
    # 線分BDは上面に存在する
    assert 'B' in faces['top'] and 'D' in faces['top']
    # 上面パネル上で BD の対角線方向
    diag = get_diagonal_type('top', 'B', 'D')
    print(f"問1: 上面パネル上のBD対角線の向き = '{diag}'")
    # 上面パネルにおいて: B=(2,1), D=(1,0) → dx=-1, dy=-1 → "\"
    assert diag == '\\', f"期待:'\\\\', 実際:'{diag}'"

    # 5択の各候補を検証
    # (1) 上面パネルでA→C対角線（"/"方向）
    assert get_diagonal_type('top', 'A', 'C') == '/'
    # (2) 前面パネルでA→F対角線（"\"方向、別パネル）
    assert get_diagonal_type('front', 'A', 'F') == '\\'
    # (3) 上面パネルで縦中央線（線ではないので別図）
    # (4) 上面パネルでD→B対角線（"\"方向） ← 正解
    assert get_diagonal_type('top', 'D', 'B') == '\\'
    # (5) 下面パネルでE→G対角線（"\"方向、別パネル）
    assert get_diagonal_type('bottom', 'E', 'G') == '\\'

    print("問1: 正解は (4) — 上面パネルの D(左上)→B(右下) 対角線")
    return 4


def verify_q2():
    """問2: 折れ線 A→C(上面) → C→F(右面) の位置を確認"""
    # AC は上面の対角線
    assert 'A' in faces['top'] and 'C' in faces['top']
    diag_top = get_diagonal_type('top', 'A', 'C')
    print(f"問2: 上面パネル上のA→C対角線の向き = '{diag_top}'")
    # A=(1,1), C=(2,0) → dx=1, dy=-1 → "/"
    assert diag_top == '/'

    # CF は右面の対角線
    assert 'C' in faces['right'] and 'F' in faces['right']
    diag_right = get_diagonal_type('right', 'C', 'F')
    print(f"問2: 右面パネル上のC→F対角線の向き = '{diag_right}'")
    # C=(3,1), F=(2,2) → dx=-1, dy=1 → "/"
    assert diag_right == '/'

    # 5択候補：
    # (1) 上面"/" (A→C), 右面"\" (B→G)
    assert get_diagonal_type('top', 'A', 'C') == '/'
    assert get_diagonal_type('right', 'B', 'G') == '\\'
    # (2) 上面"\" (D→B), 右面"/" (F→C)
    assert get_diagonal_type('top', 'D', 'B') == '\\'
    assert get_diagonal_type('right', 'F', 'C') == '/'
    # (3) 上面"/" (A→C), 右面"/" (F→C) ← 正解
    # (4) 上面"\" (D→B), 右面"\" (B→G)
    # (5) 前面"/" (E→B), 右面"/" (F→C)
    assert get_diagonal_type('front', 'E', 'B') == '/'

    print("問2: 正解は (3) — 上面 A(左下)→C(右上) かつ 右面 F(左下)→C(右上)")
    return 3


def verify_uniqueness():
    """5択の各選択肢が視覚的に区別できることを確認"""
    # 問1の各選択肢が異なるパネル/向きであることを確認
    q1_options = [
        ('top', '/', 'A-C'),
        ('front', '\\', 'A-F'),
        ('top', 'vertical', '中央縦線'),
        ('top', '\\', 'D-B'),  # 正解
        ('bottom', '\\', 'E-G'),
    ]
    # 全選択肢が異なることを確認
    keys = [(p, t) for p, t, _ in q1_options]
    assert len(set(keys)) == 5, "問1の選択肢に重複があります"

    # 問2の各選択肢が異なる組み合わせであることを確認
    q2_options = [
        (('top', '/', 'A-C'), ('right', '\\', 'B-G')),
        (('top', '\\', 'D-B'), ('right', '/', 'F-C')),
        (('top', '/', 'A-C'), ('right', '/', 'F-C')),  # 正解
        (('top', '\\', 'D-B'), ('right', '\\', 'B-G')),
        (('front', '/', 'E-B'), ('right', '/', 'F-C')),
    ]
    keys2 = [(o1[:2], o2[:2]) for o1, o2 in q2_options]
    assert len(set(keys2)) == 5, "問2の選択肢に重複があります"

    print("5択選択肢の一意性: OK")


if __name__ == '__main__':
    print("=" * 50)
    ans1 = verify_q1()
    print()
    ans2 = verify_q2()
    print()
    verify_uniqueness()
    print("=" * 50)
    print(f"問1 正解: ({ans1})")
    print(f"問2 正解: ({ans2})")
