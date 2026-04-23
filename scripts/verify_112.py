"""
セット112 検証スクリプト
問1: 階段型(2-2-2)展開図の対面ペア判定
問2: 階段型展開図上の5つの頂点マークが立方体の何個の異なる頂点に重なるか
"""

# ---------------------------------------------------------------
# 階段型(2-2-2)展開図のレイアウト
# ---------------------------------------------------------------
# 各セルは1x1の正方形（左上隅の(col, row)で位置を表す）。
# レイアウト:
#   (0,0)A  (1,0)B
#           (1,1)C  (2,1)D
#                   (2,2)E  (3,2)F
#
# C を「正面 (front, y=0)」として組み立てる。
# 各面が立方体のどこに来るかは以下の通り:
#   A → 左 (left, x=0)         [B の左隣]
#   B → 上 (top, z=1)          [C の上]
#   C → 正面 (front, y=0)      [基準]
#   D → 右 (right, x=1)        [C の右隣]
#   E → 底 (bottom, z=0)       [D の下、折り畳むと底]
#   F → 背 (back, y=1)         [E の右、折り畳むと背]
#
# 対面ペア:
#   C ↔ F (front ↔ back)
#   B ↔ E (top ↔ bottom)
#   A ↔ D (left ↔ right)
# ---------------------------------------------------------------

# 各セルの net 上の4頂点位置（TL, TR, BR, BL の順）を 3D 立方体頂点へ写像
# 立方体は 0~1 の単位立方体: x ∈ {0,1}, y ∈ {0,1}, z ∈ {0,1}
def build_net_to_3d():
    # (cell_label, net_x, net_y) -> (x_3d, y_3d, z_3d)
    m = {}

    # C (front, y=0)
    # net cell: (col=1, row=1) -> 4 corners (1,1)TL (2,1)TR (2,2)BR (1,2)BL
    # 3D: TL=(0,0,1) TR=(1,0,1) BR=(1,0,0) BL=(0,0,0)
    m[('C', 1, 1)] = (0, 0, 1)
    m[('C', 2, 1)] = (1, 0, 1)
    m[('C', 2, 2)] = (1, 0, 0)
    m[('C', 1, 2)] = (0, 0, 0)

    # B (top, z=1)
    # net cell: (col=1, row=0) -> 4 corners (1,0)TL (2,0)TR (2,1)BR (1,1)BL
    # 折り畳み: B は C の上辺 (3D の z=1, y=0) を蝶番として奥側 (y=1) へ折り上げる
    # BR と BL は蝶番で C と共有 → (1,0,1), (0,0,1)
    # TR と TL は奥側へ折り → (1,1,1), (0,1,1)
    m[('B', 1, 1)] = (0, 0, 1)
    m[('B', 2, 1)] = (1, 0, 1)
    m[('B', 1, 0)] = (0, 1, 1)
    m[('B', 2, 0)] = (1, 1, 1)

    # A (left, x=0)
    # net cell: (col=0, row=0) -> 4 corners (0,0)TL (1,0)TR (1,1)BR (0,1)BL
    # B の左辺 (3D の x=0, z=1) を蝶番として下 (z=0) へ折り下げる
    # TR と BR は蝶番で B と共有 → (0,1,1), (0,0,1)
    # TL と BL は下方 (z=0) へ折り → (0,1,0), (0,0,0)
    m[('A', 1, 0)] = (0, 1, 1)
    m[('A', 1, 1)] = (0, 0, 1)
    m[('A', 0, 0)] = (0, 1, 0)
    m[('A', 0, 1)] = (0, 0, 0)

    # D (right, x=1)
    # net cell: (col=2, row=1) -> 4 corners (2,1)TL (3,1)TR (3,2)BR (2,2)BL
    # C の右辺 (3D の x=1, y=0) を蝶番として奥側 (y=1) へ折り
    # TL と BL は蝶番で C と共有 → (1,0,1), (1,0,0)
    # TR と BR は折り → (1,1,1), (1,1,0)
    m[('D', 2, 1)] = (1, 0, 1)
    m[('D', 2, 2)] = (1, 0, 0)
    m[('D', 3, 1)] = (1, 1, 1)
    m[('D', 3, 2)] = (1, 1, 0)

    # E (bottom, z=0)
    # net cell: (col=2, row=2) -> 4 corners (2,2)TL (3,2)TR (3,3)BR (2,3)BL
    # D の下辺 (3D の x=1, z=0) を蝶番として手前 (x=0方向) へ折り
    # TL と TR は蝶番で D と共有 → (1,0,0), (1,1,0)
    # BL と BR は折り → (0,0,0), (0,1,0)
    m[('E', 2, 2)] = (1, 0, 0)
    m[('E', 3, 2)] = (1, 1, 0)
    m[('E', 2, 3)] = (0, 0, 0)
    m[('E', 3, 3)] = (0, 1, 0)

    # F (back, y=1)
    # net cell: (col=3, row=2) -> 4 corners (3,2)TL (4,2)TR (4,3)BR (3,3)BL
    # E の右辺 (3D の y=1, z=0) を蝶番として上 (z=1) へ折り
    # TL と BL は蝶番で E と共有 → (1,1,0), (0,1,0)
    # TR と BR は折り → (1,1,1), (0,1,1)
    m[('F', 3, 2)] = (1, 1, 0)
    m[('F', 3, 3)] = (0, 1, 0)
    m[('F', 4, 2)] = (1, 1, 1)
    m[('F', 4, 3)] = (0, 1, 1)

    return m


def verify_folding(m):
    """折り畳みの整合性を検証する"""
    # 1. 全頂点が立方体の8頂点に集まること
    all_3d = set(m.values())
    assert len(all_3d) == 8, f"立方体の8頂点を期待、実際: {len(all_3d)}"
    expected_8 = {(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)}
    assert all_3d == expected_8, f"立方体の頂点と一致しない: {all_3d ^ expected_8}"

    # 2. 共有された net 頂点（複数の面の境界上）が同じ 3D 座標に写像されること
    by_pos = {}
    for (face, nx, ny), v3d in m.items():
        by_pos.setdefault((nx, ny), []).append((face, v3d))
    for pos, lst in by_pos.items():
        v3ds = {v for _, v in lst}
        assert len(v3ds) == 1, f"net位置 {pos} が複数の3D頂点に写像: {lst}"

    # 3. 各面が正しく4頂点を持つこと
    by_face = {}
    for (face, nx, ny), v3d in m.items():
        by_face.setdefault(face, set()).add(v3d)
    for face, vs in by_face.items():
        assert len(vs) == 4, f"面{face}が4頂点でない: {vs}"

    # 4. 対面が頂点を共有しないこと
    opposite = [('A', 'D'), ('B', 'E'), ('C', 'F')]
    for f1, f2 in opposite:
        shared = by_face[f1] & by_face[f2]
        assert len(shared) == 0, f"対面 {f1}-{f2} が頂点を共有: {shared}"

    print("折り畳みの整合性: OK")
    return by_face


# ---------------------------------------------------------------
# 問1 検証: ラベル割り当てと対面ペア
# ---------------------------------------------------------------
# 階段の位置 → 日本語ラベル割り当て
LABEL_MAP = {
    'A': 'エ',  # 左
    'B': 'ア',  # 上
    'C': 'カ',  # 正面
    'D': 'ウ',  # 右
    'E': 'オ',  # 底
    'F': 'イ',  # 背
}


def verify_q1():
    """問1: 対面ペアを判定"""
    print("=" * 60)
    print("問1 検証: 対面ペアの組み合わせ")
    print("=" * 60)

    m = build_net_to_3d()
    by_face = verify_folding(m)

    # 対面ペア: A↔D, B↔E, C↔F
    opposite = [('A', 'D'), ('B', 'E'), ('C', 'F')]
    labeled_opposite = []
    for f1, f2 in opposite:
        labeled_opposite.append(tuple(sorted([LABEL_MAP[f1], LABEL_MAP[f2]])))

    correct_pairs = set(labeled_opposite)
    print(f"\n正しい対面ペア: {correct_pairs}")
    # 期待: {('ウ','エ'), ('ア','オ'), ('イ','カ')}

    # 選択肢
    # (1) ア-ウ, イ-エ, オ-カ
    # (2) ア-イ, ウ-カ, エ-オ
    # (3) ア-カ, イ-ウ, エ-オ
    # (4) ア-エ, イ-オ, ウ-カ
    # (5) ア-オ, イ-カ, ウ-エ ← 正解
    choices = {
        1: {('ア', 'ウ'), ('イ', 'エ'), ('オ', 'カ')},
        2: {('ア', 'イ'), ('ウ', 'カ'), ('エ', 'オ')},
        3: {('ア', 'カ'), ('イ', 'ウ'), ('エ', 'オ')},
        4: {('ア', 'エ'), ('イ', 'オ'), ('ウ', 'カ')},
        5: {('ア', 'オ'), ('イ', 'カ'), ('ウ', 'エ')},
    }

    correct_count = 0
    for k, v in choices.items():
        match = (v == correct_pairs)
        marker = "← 正解" if match else ""
        print(f"  ({k}) {sorted(v)}  {marker}")
        if match:
            correct_count += 1

    assert correct_count == 1, f"正解が一意でない: {correct_count}個"
    print("\n問1: 正解=(5), 一意性 OK")
    return True


# ---------------------------------------------------------------
# 問2 検証: 5つの頂点マークが何個の異なる立方体頂点に対応するか
# ---------------------------------------------------------------
def verify_q2():
    """問2: 5つの頂点マーク P,Q,R,S,T が組み立て後に何個の異なる立方体頂点に重なるか"""
    print("\n" + "=" * 60)
    print("問2 検証: 5頂点マークの一致判定")
    print("=" * 60)

    m = build_net_to_3d()
    verify_folding(m)

    # 各 net 頂点位置 → 3D 頂点
    pos_to_3d = {}
    for (_, nx, ny), v3d in m.items():
        pos_to_3d[(nx, ny)] = v3d

    # ===========================================================
    # 5つのマーク位置を慎重に選ぶ
    # 階段レイアウトの net 頂点とその3D頂点の対応:
    #   (0,0): A単独    → (0,1,0)
    #   (1,0): A & B    → (0,1,1)
    #   (2,0): B単独    → (1,1,1)
    #   (0,1): A単独    → (0,0,0)
    #   (1,1): A,B,C共有→ (0,0,1)
    #   (2,1): B,C,D共有→ (1,0,1)
    #   (3,1): D単独    → (1,1,1)
    #   (1,2): C単独    → (0,0,0)
    #   (2,2): C,D,E共有→ (1,0,0)
    #   (3,2): D,E,F共有→ (1,1,0)
    #   (4,2): F単独    → (1,1,1)
    #   (2,3): E単独    → (0,0,0)
    #   (3,3): E & F    → (0,1,0)
    #   (4,3): F単独    → (0,1,1)
    # ===========================================================

    # マーク位置（学習者が見て、隣接面上にないため一致しないように見えるもの）
    marks = {
        'P': (0, 1),  # A単独    → (0,0,0)
        'Q': (2, 0),  # B単独    → (1,1,1)
        'R': (3, 3),  # E&F     → (0,1,0)
        'S': (4, 2),  # F単独    → (1,1,1) ← Qと同じ!
        'T': (1, 2),  # C単独    → (0,0,0) ← Pと同じ!
    }

    print("\nマーク位置と3D頂点:")
    mark_3d = {}
    for name, pos in marks.items():
        v3d = pos_to_3d[pos]
        mark_3d[name] = v3d
        print(f"  {name} at net {pos} → 3D {v3d}")

    distinct_vertices = set(mark_3d.values())
    n_distinct = len(distinct_vertices)
    print(f"\n異なる立方体頂点の個数: {n_distinct}")
    print(f"異なる頂点: {sorted(distinct_vertices)}")

    # 一致するペアを検証
    print("\n一致するマークのペア:")
    found_pairs = []
    names = list(mark_3d.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if mark_3d[names[i]] == mark_3d[names[j]]:
                found_pairs.append((names[i], names[j]))
                print(f"  {names[i]} と {names[j]} → {mark_3d[names[i]]}")

    # 期待: P=T, Q=S, Rは単独 → 3個の異なる頂点
    assert n_distinct == 3, f"3個を期待、実際: {n_distinct}"

    # 選択肢
    # (1) 5個（全て異なる）
    # (2) 4個
    # (3) 1個（全て同じ）
    # (4) 2個
    # (5) 3個 ← 正解
    choices = {
        1: 5,
        2: 4,
        3: 1,
        4: 2,
        5: 3,
    }

    correct_count = 0
    for k, v in choices.items():
        match = (v == n_distinct)
        marker = "← 正解" if match else ""
        print(f"  ({k}) {v}個  {marker}")
        if match:
            correct_count += 1

    assert correct_count == 1, f"正解が一意でない: {correct_count}個"
    print("\n問2: 正解=(5), 一意性 OK")
    return True


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n" + "=" * 60)
    print("全検証完了")
    print("=" * 60)
