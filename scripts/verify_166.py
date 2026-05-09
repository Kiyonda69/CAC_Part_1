"""類題166: サイコロ展開図問題（5択）の解の一意性検証

問1（標準）: 標準的な西洋サイコロ（1↔6, 2↔5, 3↔4）の3視点を与え、
            十字型展開図の空欄(ア)左、(イ)後、(ウ)下を求める。

問2（高難度）: 非標準サイコロ（1↔4, 2↔3, 5↔6）の4視点を与え、
              十字型展開図の空欄(ア)左、(イ)後、(ウ)下を求める。
"""
import itertools


def tip_back(state):
    """top→back, back→bottom, bottom→front, front→top（左右不変）"""
    t, f, r, bo, ba, l = state
    return (f, bo, r, ba, t, l)


def yaw_right(state):
    """front→left, left→back, back→right, right→front（上下不変）"""
    t, f, r, bo, ba, l = state
    return (t, r, ba, bo, l, f)


def all_rotations(state):
    seen = set()
    queue = [state]
    while queue:
        s = queue.pop()
        if s in seen:
            continue
        seen.add(s)
        queue.append(tip_back(s))
        queue.append(yaw_right(s))
    return seen


def view(state):
    return (state[0], state[1], state[2])


def canonical(state):
    return min(all_rotations(state))


def find_unique_dice(views):
    """与えた視点と一致する dice 配置（rotation-class）を全列挙"""
    matches = set()
    for perm in itertools.permutations([1, 2, 3, 4, 5, 6]):
        rots = all_rotations(perm)
        all_views = {view(r) for r in rots}
        if all(v in all_views for v in views):
            matches.add(canonical(perm))
    return matches


def find_orientation_with_view(state, target_view):
    """指定した視点を持つ向き（top, front, right, bottom, back, left）を返す"""
    for r in all_rotations(state):
        if view(r) == target_view:
            return r
    return None


# --- 問1: 標準サイコロ（1↔6, 2↔5, 3↔4） ---
print("=" * 60)
print("問1: 標準サイコロ")
print("=" * 60)
views_q1 = [
    (1, 2, 3),  # 視点1
    (3, 2, 6),  # 視点2: roll left
    (4, 2, 1),  # 視点3: roll right
]
unique_q1 = find_unique_dice(views_q1)
print(f"一致するサイコロ数: {len(unique_q1)}")
assert len(unique_q1) == 1, f"問1: 解が一意でない（{len(unique_q1)}個）"

# 「前=2, 右=3」の向きで配置を確認
state_q1 = next(iter(unique_q1))
oriented_q1 = find_orientation_with_view(state_q1, (1, 2, 3))
print(f"前=2, 右=3, 上=1 の向き: top={oriented_q1[0]}, front={oriented_q1[1]}, "
      f"right={oriented_q1[2]}, bottom={oriented_q1[3]}, "
      f"back={oriented_q1[4]}, left={oriented_q1[5]}")

# 展開図上の値: 上, 左, 前, 右, 後, 下
top, front, right, bottom, back, left = oriented_q1
print(f"展開図: 上={top}, 左={left}, 前={front}, 右={right}, 後={back}, 下={bottom}")
print(f"問1の正解: ア(左)={left}, イ(後)={back}, ウ(下)={bottom}")
assert (left, back, bottom) == (4, 5, 6), f"想定と不一致: {(left, back, bottom)}"


# --- 問2: 非標準サイコロ（1↔4, 2↔3, 5↔6） ---
print()
print("=" * 60)
print("問2: 非標準サイコロ")
print("=" * 60)
views_q2 = [
    (1, 2, 5),  # 視点1
    (5, 2, 4),  # 視点2: roll left
    (1, 5, 3),  # 視点3: yaw right
    (6, 2, 1),  # 視点4: roll right
]
unique_q2 = find_unique_dice(views_q2)
print(f"一致するサイコロ数: {len(unique_q2)}")
assert len(unique_q2) == 1, f"問2: 解が一意でない（{len(unique_q2)}個）"

state_q2 = next(iter(unique_q2))
oriented_q2 = find_orientation_with_view(state_q2, (1, 2, 5))
print(f"前=2, 右=5, 上=1 の向き: top={oriented_q2[0]}, front={oriented_q2[1]}, "
      f"right={oriented_q2[2]}, bottom={oriented_q2[3]}, "
      f"back={oriented_q2[4]}, left={oriented_q2[5]}")

top, front, right, bottom, back, left = oriented_q2
print(f"展開図: 上={top}, 左={left}, 前={front}, 右={right}, 後={back}, 下={bottom}")
print(f"問2の正解: ア(左)={left}, イ(後)={back}, ウ(下)={bottom}")
assert (left, back, bottom) == (6, 3, 4), f"想定と不一致: {(left, back, bottom)}"


# --- 視点の最小性チェック（各視点を1つずつ抜いて、一意性が保たれるか） ---
print()
print("=" * 60)
print("視点の最小性チェック")
print("=" * 60)
for i in range(len(views_q1)):
    sub = views_q1[:i] + views_q1[i+1:]
    cnt = len(find_unique_dice(sub))
    print(f"問1: 視点{i+1}を除く ({sub}) → {cnt}個")
for i in range(len(views_q2)):
    sub = views_q2[:i] + views_q2[i+1:]
    cnt = len(find_unique_dice(sub))
    print(f"問2: 視点{i+1}を除く ({sub}) → {cnt}個")

print()
print("✓ 検証完了: 両問とも解は唯一")
