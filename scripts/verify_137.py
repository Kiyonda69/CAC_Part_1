# 問題137 検証スクリプト

print("=" * 50)
print("問1: ブロック積み上げ - 右側面投影")
print("=" * 50)

# 3x3グリッドの高さ（行: front/middle/back, 列: left/center/right）
heights = {
    ('front',  'left'): 1, ('front',  'center'): 3, ('front',  'right'): 2,
    ('middle', 'left'): 1, ('middle', 'center'): 1, ('middle', 'right'): 1,
    ('back',   'left'): 1, ('back',   'center'): 2, ('back',   'right'): 2,
}

rows = ['front', 'middle', 'back']
cols = ['left', 'center', 'right']

# 正面からの投影（列ごとの最大高さ）
front_view = {col: max(heights[(row, col)] for row in rows) for col in cols}
print("正面からの投影（左・中・右）:", [front_view[c] for c in cols])

# 右側面からの投影（行ごとの最大高さ）
right_view = {row: max(heights[(row, col)] for col in cols) for row in rows}
print("右側面からの投影（手前・中・奥）:", [right_view[r] for r in rows])

# 上からの投影（各マスに1個以上あれば占有）
top_view = {(row, col): heights[(row, col)] > 0 for row in rows for col in cols}

print("\nグリッド全体（上から見た高さ）:")
print("       左  中  右")
for row in rows:
    print(f"  {row:6s}: {heights[(row,'left')]}  {heights[(row,'center')]}  {heights[(row,'right')]}")

print("\n正解（右側面投影）: 手前=3, 中=1, 奥=2")
print("選択肢配置: 正解は(5)番に配置")

# 5つの選択肢候補（正解を5番に配置）
choices = [
    ([1, 2, 3], "手前低→奥高 の昇順"),
    ([2, 3, 1], "中央が最高"),
    ([3, 2, 1], "手前高→奥低 の降順"),
    ([1, 3, 2], "手前低・中高・奥中"),
    ([3, 1, 2], "手前高・中低・奥中 ← 正解"),  # 正解を5番に
]
for i, (profile, desc) in enumerate(choices, 1):
    marker = " ← 正解" if i == 5 else ""
    print(f"  ({i}) {profile} {desc}{marker}")

print()
print("=" * 50)
print("問2: サイコロ転がし - 上面追跡")
print("=" * 50)

def rotate_die(state, direction):
    top, bottom, front, back, right, left = state
    if direction == 'forward':    # 手前に倒す
        return (back, front, top, bottom, right, left)
    elif direction == 'backward': # 奥に倒す
        return (front, back, bottom, top, right, left)
    elif direction == 'right':    # 右に倒す
        return (left, right, front, back, top, bottom)
    elif direction == 'left':     # 左に倒す
        return (right, left, front, back, bottom, top)

# 初期状態: 上=1, 下=6, 前=2, 後=5, 右=3, 左=4
state = (1, 6, 2, 5, 3, 4)
labels = ('top','bottom','front','back','right','left')

def show(state, step):
    d = dict(zip(labels, state))
    print(f"  {step}: 上={d['top']}, 下={d['bottom']}, 前={d['front']}, 後={d['back']}, 右={d['right']}, 左={d['left']}")
    # 検証: 対面の和が7
    assert d['top']+d['bottom']==7, "上下の和が7でない"
    assert d['front']+d['back']==7, "前後の和が7でない"
    assert d['right']+d['left']==7, "左右の和が7でない"

print("初期配置（上=1, 前=2）:")
show(state, "初期")

operations = [
    ('forward',  "①手前に倒す"),
    ('right',    "②右に倒す"),
    ('forward',  "③手前に倒す"),
    ('left',     "④左に倒す"),
    ('backward', "⑤奥に倒す"),
]

for direction, desc in operations:
    state = rotate_die(state, direction)
    show(state, desc)

final_top = state[0]
print(f"\n最終的な上面の数字: {final_top}")
print(f"選択肢配置: 正解は(3)番に配置")

# 正解を3番に置いた選択肢
all_nums = [1, 2, 3, 4, 5]
answer_pos = 3
# 3番にfinal_top=4を配置し、残りを適当に並べる
remaining = [n for n in all_nums if n != final_top]
choices_p2 = remaining[:answer_pos-1] + [final_top] + remaining[answer_pos-1:]
print("選択肢:", [(i+1, choices_p2[i]) for i in range(5)])
