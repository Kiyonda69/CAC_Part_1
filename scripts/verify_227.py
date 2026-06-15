# -*- coding: utf-8 -*-
"""航大思考227 検証：図形の回転認識（飛行場レイアウトの回転対応）

セル集合（ポリオミノ）で表した非対称図形について、
- 図形が無対称（D4対称群が単位元のみ＝キラル）であることを確認
- 「時計回り90°回転」の正解が選択肢中で唯一であることを確認
"""

def normalize(cells):
    """最小行・最小列を0に揃え、frozensetで正規化"""
    minr = min(r for r, c in cells)
    minc = min(c for r, c in cells)
    return frozenset((r - minr, c - minc) for r, c in cells)

def dims(cells):
    R = max(r for r, c in cells) + 1
    C = max(c for r, c in cells) + 1
    return R, C

def rot90cw(cells):
    """画像を時計回り90°回転：(r,c)->(c, R-1-r)"""
    R, C = dims(cells)
    return normalize({(c, R - 1 - r) for r, c in cells})

def rot180(cells):
    R, C = dims(cells)
    return normalize({(R - 1 - r, C - 1 - c) for r, c in cells})

def rot270cw(cells):
    """反時計回り90°（=時計回り270°）：(r,c)->(C-1-c, r)"""
    R, C = dims(cells)
    return normalize({(C - 1 - c, r) for r, c in cells})

def mirror(cells):
    """左右反転（鏡像）：(r,c)->(r, C-1-c)"""
    R, C = dims(cells)
    return normalize({(r, C - 1 - c) for r, c in cells})

def all_d4(cells):
    """D4対称群8変換の正規化形を返す"""
    base = normalize(cells)
    res = set()
    cur = base
    for _ in range(4):
        res.add(cur)
        res.add(mirror(cur))
        cur = rot90cw(cur)
    return res

def verify(name, base):
    base = normalize(base)
    group = all_d4(base)
    print(f"=== {name} ===")
    print(f"セル数: {len(base)}  形状(行,列)= {dims(base)}")
    print(f"D4による相異なる像の数: {len(group)} (8なら完全非対称＝キラル)")
    assert len(group) == 8, f"{name}: 対称性があり一意性が崩れる（像 {len(group)} 種）"

    # 正解＝時計回り90°回転
    correct = rot90cw(base)
    # 妨害肢
    distractors = {
        "反時計回り90°(=270°CW)": rot270cw(base),
        "180°回転": rot180(base),
        "鏡像(左右反転)": mirror(base),
        "鏡像+時計回り90°": rot90cw(mirror(base)),
    }
    # 正解が妨害肢のいずれとも一致しない＝唯一解
    matches = [k for k, v in distractors.items() if v == correct]
    assert not matches, f"{name}: 正解と一致する妨害肢あり {matches}"
    # 妨害肢同士も区別できる（選択肢が重複しない）
    opts = [correct] + list(distractors.values())
    assert len(set(opts)) == 5, f"{name}: 選択肢に重複あり"
    print("正解(時計回り90°)は妨害肢4種と全て相異なる → 唯一解 OK")
    print()
    return base, correct, distractors


def show(cells, label=""):
    R, C = dims(cells)
    grid = [["・"] * C for _ in range(R)]
    for r, c in cells:
        grid[r][c] = "■"
    print(label)
    for row in grid:
        print("".join(row))
    print()


if __name__ == "__main__":
    # 問1：標準（6セルのキラル図形）
    base1 = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1)}
    b1, c1, d1 = verify("問1", base1)
    show(b1, "[問1] 元図（北上）")
    show(c1, "[問1] 正解＝時計回り90°")

    # 問2：高難度（8セルのキラル図形、鏡像が紛らわしい）
    base2 = {(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3)}
    b2, c2, d2 = verify("問2", base2)
    show(b2, "[問2] 元図（北上）")
    show(c2, "[問2] 正解＝時計回り90°")

    print("全検証パス：両問とも図形はキラルで、時計回り90°回転の解は唯一。")
