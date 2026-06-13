# -*- coding: utf-8 -*-
"""
航大思考217 解の一意性検証
立体（積み木）を真上から見た個数グリッドの「鏡像（左右反転）」を求める問題。
鏡を右側に立てる = 左右反転 = 各行を逆順にする。
罠: 180度回転 / 上下反転 / 転置 / 元のまま。
"""
import random


def mirror_lr(g):
    """左右反転（鏡像）: 各行を逆順に"""
    return [row[::-1] for row in g]


def flip_ud(g):
    """上下反転: 行の並びを逆順に"""
    return g[::-1]


def rot180(g):
    """180度回転"""
    return [row[::-1] for row in g[::-1]]


def transpose(g):
    """転置（対角線対称）"""
    return [list(col) for col in zip(*g)]


def verify_q1():
    G = [
        [3, 1, 0],
        [2, 0, 1],
        [1, 2, 2],
    ]
    answer = mirror_lr(G)
    candidates = {
        "鏡像(左右反転)": mirror_lr(G),
        "元のまま": [r[:] for r in G],
        "上下反転": flip_ud(G),
        "180度回転": rot180(G),
        "転置": transpose(G),
    }
    # 鏡像と一致する候補がちょうど1つであることを確認
    matches = [k for k, v in candidates.items() if v == answer]
    assert matches == ["鏡像(左右反転)"], f"問1: 一致候補が複数/不正 {matches}"
    # 全候補が相異なることを確認
    seen = []
    for v in candidates.values():
        assert v not in seen, "問1: 重複する選択肢がある"
        seen.append(v)
    print("[問1] 元の立体(真上図):")
    for r in G:
        print("   ", r)
    print("[問1] 正解(鏡像):")
    for r in answer:
        print("   ", r)
    return answer


def verify_q2():
    # 4x4 個数グリッド。printだけ高さ。星(★)つきマスを (row, col) で管理。
    G = [
        [2, 0, 3, 1],
        [1, 3, 0, 2],
        [0, 2, 1, 3],
        [3, 1, 2, 0],
    ]
    star = (1, 0)  # ★の位置（左下寄り）。高さは下表参照
    # ★を含む立体の鏡像: 高さは左右反転、★の列も反転 col -> (W-1-col)
    W = len(G[0])
    answer_grid = mirror_lr(G)
    answer_star = (star[0], W - 1 - star[1])

    def apply_star(transform_name, g_t, st):
        return (g_t, st)

    candidates = {}
    # 鏡像（正解）
    candidates["鏡像(左右反転)"] = (mirror_lr(G), (star[0], W - 1 - star[1]))
    # 元のまま
    candidates["元のまま"] = ([r[:] for r in G], star)
    # 上下反転: row -> H-1-row
    H = len(G)
    candidates["上下反転"] = (flip_ud(G), (H - 1 - star[0], star[1]))
    # 180度回転
    candidates["180度回転"] = (rot180(G), (H - 1 - star[0], W - 1 - star[1]))
    # 転置
    candidates["転置"] = (transpose(G), (star[1], star[0]))

    answer = (answer_grid, answer_star)
    matches = [k for k, v in candidates.items() if v == answer]
    assert matches == ["鏡像(左右反転)"], f"問2: 一致候補が複数/不正 {matches}"
    # 全候補が相異なる（グリッド+星の組で）
    seen = []
    for v in candidates.values():
        assert v not in seen, "問2: 重複する選択肢がある"
        seen.append(v)
    print("[問2] 元の立体(真上図) ★=", star)
    for r in G:
        print("   ", r)
    print("[問2] 正解(鏡像) ★=", answer_star)
    for r in answer_grid:
        print("   ", r)
    return answer


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("\n[OK] 問1・問2ともに鏡像と一致する選択肢は唯一")
    print("正解番号ランダム化:")
    print("  問1 ->", random.randint(1, 5))
    print("  問2 ->", random.randint(1, 5))
