#!/usr/bin/env python3
"""
航大思考73 検証スクリプト
問1・問2: ポリオミノパズル（パーツ組み合わせ問題）

問1（標準）: 5×5グリッドに4つのパーツを敷き詰める。5つのうち不要な1つを答える。
問2（高難度）: 5×5グリッドに4つのパーツを敷き詰める。5つのうち不要な1つを答える（より複雑なピース形状）。
"""

from copy import deepcopy


def normalize_piece(cells):
    """ピースの座標を正規化（左上を原点に）"""
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return tuple(sorted((r - min_r, c - min_c) for r, c in cells))


def rotate_90(cells):
    """90度時計回りに回転: (r,c) -> (c, -r)"""
    rotated = [(c, -r) for r, c in cells]
    return normalize_piece(rotated)


def get_rotations(cells):
    """0, 90, 180, 270度の回転を取得（裏返しなし）"""
    rotations = set()
    current = normalize_piece(cells)
    for _ in range(4):
        rotations.add(current)
        current = rotate_90(current)
    return list(rotations)


def can_place(grid, piece, start_r, start_c, rows, cols):
    """ピースを(start_r, start_c)をオフセットとして配置できるか確認"""
    for r, c in piece:
        nr, nc = start_r + r, start_c + c
        if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
            return False
        if grid[nr][nc] != 0:
            return False
    return True


def place_piece(grid, piece, start_r, start_c, piece_id):
    """ピースを配置"""
    new_grid = [row[:] for row in grid]
    for r, c in piece:
        new_grid[start_r + r][start_c + c] = piece_id
    return new_grid


def find_first_empty(grid, rows, cols):
    """最初の空きセルを見つける（行優先）"""
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                return r, c
    return None


def solve(grid, pieces_with_rotations, piece_indices, rows, cols, solutions, max_solutions=2):
    """バックトラッキングで敷き詰めを試みる"""
    if len(solutions) >= max_solutions:
        return

    empty = find_first_empty(grid, rows, cols)
    if empty is None:
        solutions.append([row[:] for row in grid])
        return

    target_r, target_c = empty

    for idx in piece_indices:
        for rotation in pieces_with_rotations[idx]:
            # ピースの各セルが(target_r, target_c)に重なるオフセットを試す
            for pr, pc in rotation:
                start_r = target_r - pr
                start_c = target_c - pc
                if can_place(grid, rotation, start_r, start_c, rows, cols):
                    new_grid = place_piece(grid, rotation, start_r, start_c, idx + 1)
                    remaining = [i for i in piece_indices if i != idx]
                    solve(new_grid, pieces_with_rotations, remaining, rows, cols, solutions, max_solutions)


def solve_puzzle(rows, cols, pieces, excluded_idx):
    """特定のピースを除外して、残りでグリッドを敷き詰められるか検証"""
    used_indices = [i for i in range(len(pieces)) if i != excluded_idx]
    used_cells = sum(len(pieces[i]) for i in used_indices)
    total_cells = rows * cols

    if used_cells != total_cells:
        return {"solvable": False, "reason": f"セル数不一致: {used_cells} != {total_cells}", "num_solutions": 0}

    # 各ピースの回転を事前計算（インデックスは0から）
    pieces_with_rotations = {}
    for new_idx, orig_idx in enumerate(used_indices):
        pieces_with_rotations[new_idx] = get_rotations(pieces[orig_idx])

    grid = [[0] * cols for _ in range(rows)]
    solutions = []
    solve(grid, pieces_with_rotations, list(range(len(used_indices))), rows, cols, solutions, max_solutions=2)

    return {
        "solvable": len(solutions) > 0,
        "num_solutions": len(solutions),
        "solution": solutions[0] if solutions else None,
        "used_pieces": used_indices
    }


def print_piece_shape(piece, label=""):
    """ピースを視覚的に表示"""
    cells = normalize_piece(piece)
    max_r = max(r for r, c in cells)
    max_c = max(c for r, c in cells)
    grid = [['.' for _ in range(max_c + 1)] for _ in range(max_r + 1)]
    for r, c in cells:
        grid[r][c] = '#'
    if label:
        print(f"  {label}:")
    for row in grid:
        print("    " + " ".join(row))


def print_grid(grid):
    """グリッドを表示"""
    for row in grid:
        print("  " + " ".join(str(x) for x in row))


def verify_problem(name, rows, cols, pieces):
    """問題を検証"""
    print(f"\n{'=' * 60}")
    print(f"{name}")
    print(f"{'=' * 60}")

    print(f"\nグリッドサイズ: {rows}x{cols} = {rows*cols}セル")
    print(f"ピース数: {len(pieces)}")
    sizes = [len(p) for p in pieces]
    print(f"ピースサイズ: {sizes} (合計: {sum(sizes)})")

    print("\nピース一覧:")
    for i, piece in enumerate(pieces):
        print_piece_shape(piece, f"ピース{i+1} ({len(piece)}セル)")
        rots = get_rotations(piece)
        print(f"    回転パターン数: {len(rots)}")

    print(f"\n--- 各ピースを除外した場合の検証 ---")
    solvable_excludes = []

    for excluded in range(len(pieces)):
        result = solve_puzzle(rows, cols, pieces, excluded)
        status = "解あり" if result["solvable"] else "解なし"
        reason = result.get("reason", "")
        num = result["num_solutions"]
        print(f"\nピース{excluded+1}を除外: {status} (解の数: {num}) {reason}")
        if result["solvable"] and result["solution"]:
            print("  配置:")
            print_grid(result["solution"])
            solvable_excludes.append((excluded + 1, num))

    print(f"\n--- サマリー ---")
    print(f"解が存在する除外パターン: {solvable_excludes}")
    if len(solvable_excludes) == 1:
        ans_piece, ans_num = solvable_excludes[0]
        print(f"正解: ピース{ans_piece}が不要（解の数: {ans_num}）")
        if ans_num > 1:
            print("  注意: 配置の解は複数あるが、不要ピースは一意に定まる")
    else:
        print("警告: 複数の除外パターンで解が存在します。問題の再設計が必要。")

    return solvable_excludes


# ========================================
# 問1（標準）: 5×5グリッド
# ========================================
# 設計方針:
# - ピースサイズ: 5, 6, 7, 7, 5 (合計30)
# - {5a, 6, 7a, 7b}=25 と {6, 7a, 7b, 5b}=25 の2パターンがセル数一致
# - 空間的に1パターンのみ解が存在

# 既知の敷き詰め:
# A A B B B    A(5): (0,0),(0,1),(1,0),(1,1),(2,1)
# A A B C C    B(6): (0,2),(0,3),(0,4),(1,2),(2,2),(3,2)
# D A B C C    C(7): (1,3),(1,4),(2,3),(2,4),(3,3),(3,4),(4,4)
# D D B C C    D(7): (2,0),(3,0),(3,1),(4,0),(4,1),(4,2),(4,3)
# D D D D C
#
# デコイ E(5): T型ペントミノ

q1_pieces = [
    # ピース1 (A, 5セル): P型
    [(0,0),(0,1),(1,0),(1,1),(2,1)],
    # ピース2 (B, 6セル): J型ヘクソミノ
    [(0,0),(0,1),(0,2),(1,0),(2,0),(3,0)],
    # ピース3 (C, 7セル): 不規則型
    [(0,0),(0,1),(1,0),(1,1),(2,0),(2,1),(3,1)],
    # ピース4 (D, 7セル): 不規則L型
    [(0,0),(1,0),(1,1),(2,0),(2,1),(2,2),(2,3)],
    # ピース5 (E, 5セル): T型ペントミノ（デコイ）
    [(0,0),(0,1),(0,2),(1,1),(2,1)],
]

result1 = verify_problem("問1（標準）: 5×5グリッドのポリオミノパズル", 5, 5, q1_pieces)


# ========================================
# 問2（高難度）: 5×5グリッド
# ========================================
# 設計方針:
# - ピースサイズ: 8, 7, 5, 5, 5 (合計30)
# - {8, 7, 5a, 5b}=25, {8, 7, 5a, 5c}=25, {8, 7, 5b, 5c}=25
# - 3パターンのセル数一致だが、空間的に1パターンのみ解が存在

# 既知の敷き詰め:
# A A A B B    A(8): (0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)
# A A A B B    B(5): (0,3),(0,4),(1,3),(1,4),(2,4)
# A A C C B    C(7): (2,2),(2,3),(3,2),(3,3),(3,4),(4,3),(4,4)
# D D C C C    D(5): (3,0),(3,1),(4,0),(4,1),(4,2)
# D D D C C

q2_pieces = [
    # ピース1 (A, 8セル): 2×3 + 2
    [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)],
    # ピース2 (B, 5セル): P型
    [(0,0),(0,1),(1,0),(1,1),(2,1)],
    # ピース3 (C, 7セル): 不規則型
    [(0,0),(0,1),(1,0),(1,1),(1,2),(2,1),(2,2)],
    # ピース4 (D, 5セル): P型（反転）
    [(0,0),(0,1),(1,0),(1,1),(1,2)],
    # ピース5 (E, 5セル): プラス型（デコイ）
    [(0,1),(1,0),(1,1),(1,2),(2,1)],
]

result2 = verify_problem("問2（高難度）: 5×5グリッドのポリオミノパズル", 5, 5, q2_pieces)


# ========================================
# 最終サマリー
# ========================================
print("\n" + "=" * 60)
print("最終検証結果")
print("=" * 60)

if len(result1) == 1:
    print(f"問1: 正解はピース{result1[0][0]}が不要 ✓")
else:
    print(f"問1: 要再設計 (解パターン: {len(result1)})")

if len(result2) == 1:
    print(f"問2: 正解はピース{result2[0][0]}が不要 ✓")
else:
    print(f"問2: 要再設計 (解パターン: {len(result2)})")
