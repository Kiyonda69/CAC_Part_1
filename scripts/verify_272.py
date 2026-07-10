#!/usr/bin/env python3
"""航大思考272 検証: 回転・鏡像判別問題（方眼図形）

問1: 4x4方眼の図形F。選択肢5つのうち、回転のみで元と一致するのは1つ
     （正解=回転像、他4つ=鏡像の回転）
問2: 5x5方眼の図形G。正解=回転像、誤答=鏡像の回転3つ＋1マス移動した図形
"""


def normalize(cells):
    """左上詰めに平行移動して正規化"""
    rmin = min(r for r, c in cells)
    cmin = min(c for r, c in cells)
    return frozenset((r - rmin, c - cmin) for r, c in cells)


def rot90(cells):
    """時計回りに90度回転"""
    return normalize({(c, -r) for r, c in cells})


def mirror(cells):
    """左右反転（鏡像）"""
    return normalize({(r, -c) for r, c in cells})


def rotations(cells):
    """4方位の回転像の集合"""
    out = []
    cur = normalize(cells)
    for _ in range(4):
        out.append(cur)
        cur = rot90(cur)
    return out


def show(cells, size):
    cells = normalize(cells)
    for r in range(size):
        print("".join("■" if (r, c) in cells else "□" for c in range(size)))
    print()


# ---------- 問1: 図形F (4x4, 6マス) ----------
F = {(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)}

rots_F = rotations(F)
mir_F = mirror(F)
rots_MF = rotations(mir_F)

# 回転対称性なし（4方位すべて異なる）
assert len(set(rots_F)) == 4, "Fに回転対称性がある"
# キラル（鏡像は回転では一致しない）
assert not set(rots_F) & set(rots_MF), "Fが鏡像対称（アキラル）"

# 選択肢: 正解=rot90(F)、誤答=鏡像の0/90/180/270度回転
q1_correct_shape = rots_F[1]
q1_options_shapes = [q1_correct_shape] + list(rots_MF)
assert len(set(q1_options_shapes)) == 5, "問1の選択肢に重複がある"
match1 = [s in set(rots_F) for s in q1_options_shapes]
assert sum(match1) == 1 and match1[0], "問1の解が一意でない"

# ---------- 問2: 図形G (5x5, 9マス) ----------
G = {(0, 0), (0, 1), (0, 2), (1, 2), (2, 1), (2, 2), (3, 1), (4, 0), (4, 1)}

rots_G = rotations(G)
mir_G = mirror(G)
rots_MG = rotations(mir_G)

assert len(set(rots_G)) == 4, "Gに回転対称性がある"
assert not set(rots_G) & set(rots_MG), "Gが鏡像対称（アキラル）"

# 正解=rot270(G)（反時計回り90度）
q2_correct_shape = rots_G[3]

# 1マス移動ディストラクター: 正解形状 rot270(G) の (2,4) を (2,3) に移動
# 見た目は正解と酷似するが、回転でも鏡像でも G と一致しない
base = q2_correct_shape
assert (2, 4) in base and (2, 3) not in base
M = normalize((set(base) - {(2, 4)}) | {(2, 3)})
moved = ((2, 4), (2, 3))
assert M not in set(rots_G) and M not in set(rots_MG), "Mが正規図形と合同"

q2_options_shapes = [q2_correct_shape, rots_MG[1], rots_MG[2], rots_MG[3], M]
assert len(set(q2_options_shapes)) == 5, "問2の選択肢に重複がある"
match2 = [s in set(rots_G) for s in q2_options_shapes]
assert sum(match2) == 1 and match2[0], "問2の解が一意でない"

# ---------- 表示 ----------
print("=== 問1 図形F ===")
show(F, 4)
print("--- 正解形状 rot90(F) ---")
show(q1_correct_shape, 4)
for i, s in enumerate(rots_MF):
    print(f"--- 鏡像の{i*90}度回転 ---")
    show(s, 4)

print("=== 問2 図形G ===")
show(G, 5)
print("--- 正解形状 rot270(G) ---")
show(q2_correct_shape, 5)
for i in (1, 2, 3):
    print(f"--- 鏡像の{i*90}度回転 ---")
    show(rots_MG[i], 5)
print(f"--- 1マス移動M（{moved[0]}→{moved[1]}） ---")
show(M, 5)

print("検証OK: 問1・問2とも解は一意")
