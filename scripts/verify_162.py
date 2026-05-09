"""
航大思考162 検証スクリプト
問1: 十字型展開図候補から、向かい合う面の和=7になるものを選ぶ（5択）
問2: 展開図を組み立て、特定の向きでの右側面の目を求める（5択）
"""

# ==================== 問1の検証 ====================
def is_valid_dice_cross(arrangement):
    """十字型展開図 [a, b, c, d, e, f] が正しいサイコロかチェック
    配置:
         [a]
      [b][c][d][e]
         [f]
    対面: a-f, b-d, c-e
    """
    a, b, c, d, e, f = arrangement
    # 1〜6が1つずつ
    if sorted(arrangement) != [1, 2, 3, 4, 5, 6]:
        return False
    # 対面の和が7
    return a + f == 7 and b + d == 7 and c + e == 7


print("=" * 50)
print("問1: 5つの展開図候補")
print("=" * 50)
options_q1 = [
    [1, 2, 3, 4, 5, 6],   # (1)
    [2, 3, 1, 4, 6, 5],   # (2) ★正解狙い
    [1, 3, 2, 5, 4, 6],   # (3)
    [1, 4, 3, 2, 5, 6],   # (4)
    [3, 1, 2, 5, 4, 6],   # (5)
]
correct_q1 = []
for i, opt in enumerate(options_q1):
    a, b, c, d, e, f = opt
    pairs = f"a+f={a+f}, b+d={b+d}, c+e={c+e}"
    valid = is_valid_dice_cross(opt)
    if valid:
        correct_q1.append(i + 1)
    print(f"({i+1}): {opt}  対面: {pairs}  →  {'★正解' if valid else '不正解'}")

assert len(correct_q1) == 1, f"問1: 解が{len(correct_q1)}個 ({correct_q1})"
print(f"\n問1 正解: ({correct_q1[0]})")


# ==================== 問2の検証 ====================
# サイコロ状態: (top, bottom, front, back, left, right)
def roll_fwd(s):
    """前に倒す: 上→前, 前→下, 下→後, 後→上"""
    t, b, f, bk, l, r = s
    return (bk, f, t, b, l, r)

def roll_bwd(s):
    """後ろに倒す"""
    t, b, f, bk, l, r = s
    return (f, bk, b, t, l, r)

def roll_lft(s):
    """左に倒す: 上→左, 左→下, 下→右, 右→上"""
    t, b, f, bk, l, r = s
    return (r, l, f, bk, t, b)

def roll_rgt(s):
    """右に倒す"""
    t, b, f, bk, l, r = s
    return (l, r, f, bk, b, t)

def yaw_cw(s):
    """上から見て時計回り: 前→右, 右→後, 後→左, 左→前"""
    t, b, f, bk, l, r = s
    return (t, b, l, r, bk, f)

def yaw_ccw(s):
    t, b, f, bk, l, r = s
    return (t, b, r, l, f, bk)


def all_orientations(initial):
    seen = set()
    stack = [initial]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        for op in [roll_fwd, roll_bwd, roll_lft, roll_rgt, yaw_cw, yaw_ccw]:
            stack.append(op(s))
    return seen


print("\n" + "=" * 50)
print("問2: 展開図を組み立てたサイコロの向き")
print("=" * 50)
# 展開図:
#      [3]
#   [2][1][5][6]
#      [4]
# 中央(c=1)を前面、上(a=3)を上面、下(f=4)を下面、
# 左(b=2)を左面、右(d=5)を右面、その先(e=6)を後面
initial = (3, 4, 1, 6, 2, 5)  # (top, bottom, front, back, left, right)
print(f"初期状態: 上={initial[0]}, 下={initial[1]}, 前={initial[2]}, 後={initial[3]}, 左={initial[4]}, 右={initial[5]}")

orients = all_orientations(initial)
print(f"全向き数: {len(orients)} (24であるべき)")
assert len(orients) == 24

# 問題: 上面=4, 前面=2 のとき、右側面は?
target_top = 4
target_front = 2
matches = [s for s in orients if s[0] == target_top and s[2] == target_front]
print(f"\n上面={target_top}, 前面={target_front} となる向き: {len(matches)}通り (1であるべき)")
assert len(matches) == 1
right_value = matches[0][5]
print(f"そのときの右側面 = {right_value}")

# 選択肢: 正解番号(1)に配置するための数字
# 4は上面、2は前面なので除外。残り {1,3,5,6} に正解値を加える
options_q2 = [
    right_value,  # (1) ★正解 = 6
    1,            # (2)
    2,            # (3) 前面の値だがダミーとして
    3,            # (4)
    5,            # (5)
]
print(f"\n選択肢:")
for i, v in enumerate(options_q2):
    mark = "★正解" if v == right_value else "不正解"
    print(f"  ({i+1}): {v}  →  {mark}")

# 重複チェック
assert len(set(options_q2)) == len(options_q2), "選択肢に重複あり"
print("\n問2 正解: (1)")
