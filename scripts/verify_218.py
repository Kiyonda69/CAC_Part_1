# -*- coding: utf-8 -*-
"""
航大思考218 検証・SVG生成スクリプト

テーマ: 立体（積み木の壁）を斜投影で描いた見取図を鏡に映したときの見え方。
ポイント: 鏡では「左右の並び」だけでなく「見える側面の向き（奥行き方向）」も
          反転する。元は右上に奥行き（上面＋右側面が見える）→ 鏡像は左上に
          奥行き（上面＋左側面が見える）。

立体の表現:
  - 奥行き1のキューブの壁。前面グリッドの (c,r) にキューブが有るか無いか。
    c=0..maxC（左→右）, r=0..maxR（上→下）。
  - marker: 特定キューブの前面に描く目印（dot=●, square=■）。
  - depth: 'R'（奥行きが右上＝上面と右側面が見える）/ 'L'（左上＝上面と左側面）。

鏡（右側に垂直に立てる）に映すと:
  - (c,r) -> (maxC-c, r)         左右反転
  - 目印も同じセルへ移動
  - depth: 'R' -> 'L'            見える側面が右から左へ
"""

# ==================== 変換ユーティリティ ====================

def hflip(cells, maxC):
    return frozenset((maxC - c, r) for (c, r) in cells)

def vflip(cells, maxR):
    return frozenset((c, maxR - r) for (c, r) in cells)

def hflip_pt(p, maxC):
    return (maxC - p[0], p[1])

def vflip_pt(p, maxR):
    return (p[0], maxR - p[1])

def flip_depth(d):
    return 'L' if d == 'R' else 'R'


class Solid:
    """立体の状態: セル集合 + 目印(dict name->cell) + 奥行き方向。"""
    def __init__(self, cells, markers, depth, maxC, maxR):
        self.cells = frozenset(cells)
        self.markers = dict(markers)
        self.depth = depth
        self.maxC = maxC
        self.maxR = maxR

    def key(self):
        # 図として区別するための正規化キー
        return (self.cells, tuple(sorted(self.markers.items())), self.depth)

    def mirror_right(self):
        """右側の鏡に映した像（左右反転＋奥行き反転）。"""
        return Solid(
            hflip(self.cells, self.maxC),
            {n: hflip_pt(p, self.maxC) for n, p in self.markers.items()},
            flip_depth(self.depth), self.maxC, self.maxR)

    def horizontal_only(self):
        """左右反転のみ（奥行きはそのまま）＝ よくある誤り。"""
        return Solid(
            hflip(self.cells, self.maxC),
            {n: hflip_pt(p, self.maxC) for n, p in self.markers.items()},
            self.depth, self.maxC, self.maxR)

    def vmirror(self):
        """上下反転＋奥行き反転（別の鏡＝罠）。"""
        return Solid(
            vflip(self.cells, self.maxR),
            {n: vflip_pt(p, self.maxR) for n, p in self.markers.items()},
            flip_depth(self.depth), self.maxC, self.maxR)

    def rot180(self):
        """180度回転（奥行きはそのまま）。"""
        return Solid(
            vflip(hflip(self.cells, self.maxC), self.maxR),
            {n: vflip_pt(hflip_pt(p, self.maxC), self.maxR)
             for n, p in self.markers.items()},
            self.depth, self.maxC, self.maxR)

    def copy_swap_markers(self):
        """目印の種類を入れ替えた像（図の形・奥行きは正解と同一の罠）。"""
        names = list(self.markers.keys())
        assert len(names) == 2
        sw = {names[0]: self.markers[names[1]], names[1]: self.markers[names[0]]}
        return Solid(self.cells, sw, self.depth, self.maxC, self.maxR)


def assert_unique(options, correct_index):
    """選択肢が全て相異なり、正解だけが鏡像と一致することを確認。"""
    keys = [o.key() for o in options]
    assert len(set(keys)) == len(keys), "選択肢に重複あり: %s" % keys
    print("  選択肢はすべて相異なる: OK (%d通り)" % len(set(keys)))
    return correct_index


# ==================== 問1の定義 ====================
# 立体: 左に高さ3の柱 + 下段に横並び（L字/階段）。奥行きは右上(R)。
# 目印: 下段右端 (2,2) の前面に ● 。
Q1_maxC, Q1_maxR = 2, 2
Q1_cells = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)}
Q1_markers = {'dot': (2, 2)}
Q1_solid = Solid(Q1_cells, Q1_markers, 'R', Q1_maxC, Q1_maxR)

# 正解スロット = 4
Q1_mirror = Q1_solid.mirror_right()          # 正解
Q1_options = [
    Q1_solid,                                 # (1) 元のまま
    Q1_solid.horizontal_only(),               # (2) 左右反転だが奥行きそのまま
    Q1_solid.vmirror(),                        # (3) 上下反転（別の鏡）
    Q1_mirror,                                 # (4) 正解: 左右反転＋奥行き反転
    Q1_solid.rot180(),                         # (5) 180度回転
]
Q1_correct = 4


# ==================== 問2の定義 ====================
# 立体: 左に高さ3、右に高さ2、下段4マスの非対称な壁。奥行きは右上(R)。
# 目印: ● を左上 (0,0)、■ を右の (3,1) に置く。
Q2_maxC, Q2_maxR = 3, 2
Q2_cells = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (3, 1)}
Q2_markers = {'dot': (0, 0), 'sq': (3, 1)}
Q2_solid = Solid(Q2_cells, Q2_markers, 'R', Q2_maxC, Q2_maxR)

# 正解スロット = 3
Q2_mirror = Q2_solid.mirror_right()           # 正解
Q2_options = [
    Q2_solid,                                  # (1) 元のまま
    Q2_solid.horizontal_only(),                # (2) 左右反転だが奥行きそのまま
    Q2_mirror,                                 # (3) 正解
    Q2_mirror.copy_swap_markers(),             # (4) 形・奥行きは正解だが目印入替
    Q2_solid.vmirror(),                         # (5) 上下反転（別の鏡）
]
Q2_correct = 3


# ==================== 検証実行 ====================
if __name__ == '__main__':
    print("=== 問1 検証 ===")
    print("  元の立体 cells:", sorted(Q1_solid.cells), "depth", Q1_solid.depth)
    print("  鏡像     cells:", sorted(Q1_mirror.cells), "depth", Q1_mirror.depth,
          "marker", Q1_mirror.markers)
    assert Q1_options[Q1_correct - 1].key() == Q1_mirror.key()
    # 正解以外は鏡像と一致しないこと
    for i, o in enumerate(Q1_options, 1):
        same = (o.key() == Q1_mirror.key())
        assert same == (i == Q1_correct), "スロット%d の一致判定が不正" % i
    assert_unique(Q1_options, Q1_correct)
    print("  正解 = (%d): OK" % Q1_correct)

    print("=== 問2 検証 ===")
    print("  元の立体 cells:", sorted(Q2_solid.cells), "markers", Q2_solid.markers)
    print("  鏡像     cells:", sorted(Q2_mirror.cells), "depth", Q2_mirror.depth,
          "markers", Q2_mirror.markers)
    assert Q2_options[Q2_correct - 1].key() == Q2_mirror.key()
    for i, o in enumerate(Q2_options, 1):
        same = (o.key() == Q2_mirror.key())
        assert same == (i == Q2_correct), "スロット%d の一致判定が不正" % i
    assert_unique(Q2_options, Q2_correct)
    print("  正解 = (%d): OK" % Q2_correct)
    print("\nすべての検証に合格しました。")
