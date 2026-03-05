"""
航大思考34 検証スクリプト
問1: 積み木の三面図（各段配置→正しい右側面図を特定）
問2: 三面図からの最小ブロック数推定
"""

from itertools import combinations


def compute_views(grid, n):
    """3Dグリッドから正面図・右側面図・上面図を計算"""
    front = [[0]*n for _ in range(n)]  # F[x][z]
    right = [[0]*n for _ in range(n)]  # R[y][z]
    top   = [[0]*n for _ in range(n)]  # T[x][y]

    for x in range(n):
        for y in range(n):
            for z in range(n):
                if grid[x][y][z]:
                    front[x][z] = 1
                    right[y][z] = 1
                    top[x][y] = 1
    return front, right, top


def veq(v1, v2):
    return all(v1[i][j] == v2[i][j] for i in range(len(v1)) for j in range(len(v1[0])))


def pv(view, n, label=""):
    """3×3ビューを表示"""
    if label:
        print(f"  {label}:")
    for z in range(n-1, -1, -1):
        row = "    "
        for a in range(n):
            row += "■ " if view[a][z] else "□ "
        print(row)


N = 3

# ============================================================
# 問1: 積み木の三面図
# ============================================================
print("=" * 60)
print("問1: 積み木の投影図")
print("=" * 60)

grid1 = [[[0]*N for _ in range(N)] for _ in range(N)]

# z=0 (底面): 全面
for x in range(3):
    for y in range(3):
        grid1[x][y][0] = 1

# z=1 (中段): 手前2列 + 左端
z1 = [(0,0), (1,0), (2,0), (0,1), (1,1)]
for x, y in z1:
    grid1[x][y][1] = 1

# z=2 (上段): 左手前の1ブロック
grid1[0][0][2] = 1

total = sum(grid1[x][y][z] for x in range(N) for y in range(N) for z in range(N))
print(f"総ブロック数: {total}")

print("\n各段の配置 (上から見た図):")
for z in range(N-1, -1, -1):
    print(f"  z={z} ({'上段' if z==2 else '中段' if z==1 else '底面'}):")
    for y in range(N-1, -1, -1):
        row = "    "
        for x in range(N):
            row += "■ " if grid1[x][y][z] else "□ "
        print(f"{row}  (y={y})")
    print(f"    {'x=0 x=1 x=2'}")

front, right, top = compute_views(grid1, N)

print("\n正面図 F[x][z] (手前y=0から見る):")
pv(front, N)
print("\n右側面図 R[y][z] (右x=2から見る) ★正解:")
pv(right, N)
print("\n上面図 T[x][y] (上から見る):")
for y in range(N-1, -1, -1):
    row = "    "
    for x in range(N):
        row += "■ " if top[x][y] else "□ "
    print(row)

# 不正解の右側面図を4つ作成
wrongs = []

# 正解のright:
# R[0][0]=1, R[1][0]=1, R[2][0]=1  (z=0: ■ ■ ■)
# R[0][1]=1, R[1][1]=1, R[2][1]=0  (z=1: ■ ■ □)
# R[0][2]=1, R[1][2]=0, R[2][2]=0  (z=2: ■ □ □)

# 不正解A: z=2をR[1][2]=1に
wA = [[right[y][z] for z in range(N)] for y in range(N)]
wA[1][2] = 1
wrongs.append(("A", wA))

# 不正解B: z=1のR[2][1]=1（中段奥が見える）
wB = [[right[y][z] for z in range(N)] for y in range(N)]
wB[2][1] = 1
wrongs.append(("B", wB))

# 不正解C: z=1のR[1][1]=0（中段中央が見えない）
wC = [[right[y][z] for z in range(N)] for y in range(N)]
wC[1][1] = 0
wrongs.append(("C", wC))

# 不正解D: z=2をR[0][2]=0に（上段手前が見えない）
wD = [[right[y][z] for z in range(N)] for y in range(N)]
wD[0][2] = 0
wrongs.append(("D", wD))

print("\n--- 選択肢一覧 ---")
print("正解:")
pv(right, N)

for name, w in wrongs:
    print(f"\n不正解{name}:")
    for z in range(N-1, -1, -1):
        row = "    "
        for y in range(N):
            row += "■ " if w[y][z] else "□ "
        print(row)

# 重複チェック
all_opts = [right] + [w for _, w in wrongs]
for i in range(len(all_opts)):
    for j in range(i+1, len(all_opts)):
        vi = all_opts[i]
        vj = all_opts[j]
        same = True
        for y in range(N):
            for z in range(N):
                if vi[y][z] != vj[y][z]:
                    same = False
        if same:
            print(f"警告: 選択肢{i}と{j}が同一!")

print("\n全選択肢が異なることを確認: OK")


# ============================================================
# 問2: 三面図からの最小ブロック数
# ============================================================
print("\n" + "=" * 60)
print("問2: 三面図からの最小ブロック数")
print("=" * 60)

# 正面図・右側面図・上面図を定義
# より非対称で面白い三面図

# 正面図 F[x][z]:
# z=2: ■ □ □
# z=1: ■ ■ □
# z=0: ■ ■ ■
q2_F = [[1,1,1], [1,1,0], [1,0,0]]

# 右側面図 R[y][z]:
# z=2: □ □ ■
# z=1: □ ■ ■
# z=0: ■ ■ ■
q2_R = [[1,0,0], [1,1,0], [1,1,1]]

# 上面図 T[x][y]:
# y=2: ■ □ □
# y=1: ■ ■ □
# y=0: ■ ■ ■
q2_T = [[1,1,1], [1,1,0], [1,0,0]]

print("正面図 F[x][z]:")
for z in range(N-1, -1, -1):
    row = "  "
    for x in range(N):
        row += "■ " if q2_F[x][z] else "□ "
    print(row)

print("\n右側面図 R[y][z]:")
for z in range(N-1, -1, -1):
    row = "  "
    for y in range(N):
        row += "■ " if q2_R[y][z] else "□ "
    print(row)

print("\n上面図 T[x][y]:")
for y in range(N-1, -1, -1):
    row = "  "
    for x in range(N):
        row += "■ " if q2_T[x][y] else "□ "
    print(row)

# 配置可能なセル
possible = []
for x in range(N):
    for y in range(N):
        for z in range(N):
            if q2_F[x][z] and q2_R[y][z] and q2_T[x][y]:
                possible.append((x, y, z))

print(f"\n配置可能セル数: {len(possible)}")
for c in possible:
    print(f"  {c}")

# 最大配置の検証
grid_max = [[[0]*N for _ in range(N)] for _ in range(N)]
for x, y, z in possible:
    grid_max[x][y][z] = 1

f_m, r_m, t_m = compute_views(grid_max, N)
assert veq(f_m, q2_F), "最大配置の正面図が不一致"
assert veq(r_m, q2_R), "最大配置の右側面図が不一致"
assert veq(t_m, q2_T), "最大配置の上面図が不一致"
print(f"最大ブロック数: {len(possible)} (検証OK)")

# 最小ブロック数を探索
print("\n最小ブロック数を探索...")
min_found = None
min_configs = []

for num in range(1, len(possible) + 1):
    configs_at_num = []
    for chosen in combinations(possible, num):
        grid = [[[0]*N for _ in range(N)] for _ in range(N)]
        for x, y, z in chosen:
            grid[x][y][z] = 1
        f, r, t = compute_views(grid, N)
        if veq(f, q2_F) and veq(r, q2_R) and veq(t, q2_T):
            configs_at_num.append(chosen)
    if configs_at_num:
        if min_found is None:
            min_found = num
            min_configs = configs_at_num
        print(f"  {num}個: {len(configs_at_num)}通り")

print(f"\n最小ブロック数: {min_found}")
print(f"最大ブロック数: {len(possible)}")
print(f"最小配置の例:")
for cfg in min_configs[:3]:
    print(f"  {cfg}")

# ============================================================
# 問2: 別のパターンも試す
# ============================================================
print("\n" + "=" * 60)
print("問2: パターンB（正面と右側面が逆向き階段）")
print("=" * 60)

# 正面図:
# z=2: □ ■ □
# z=1: ■ ■ ■
# z=0: ■ ■ ■
q2b_F = [[1,1,0], [1,1,1], [1,1,0]]

# 右側面図:
# z=2: □ ■ □
# z=1: ■ ■ □
# z=0: ■ ■ ■
q2b_R = [[1,1,0], [1,1,1], [1,0,0]]

# 上面図:
# y=2: ■ ■ □
# y=1: ■ ■ ■
# y=0: ■ ■ ■
q2b_T = [[1,1,1], [1,1,1], [1,1,0]]

print("正面図:")
for z in range(N-1, -1, -1):
    row = "  "
    for x in range(N):
        row += "■ " if q2b_F[x][z] else "□ "
    print(row)

print("\n右側面図:")
for z in range(N-1, -1, -1):
    row = "  "
    for y in range(N):
        row += "■ " if q2b_R[y][z] else "□ "
    print(row)

print("\n上面図:")
for y in range(N-1, -1, -1):
    row = "  "
    for x in range(N):
        row += "■ " if q2b_T[x][y] else "□ "
    print(row)

possible_b = []
for x in range(N):
    for y in range(N):
        for z in range(N):
            if q2b_F[x][z] and q2b_R[y][z] and q2b_T[x][y]:
                possible_b.append((x, y, z))

grid_max_b = [[[0]*N for _ in range(N)] for _ in range(N)]
for x, y, z in possible_b:
    grid_max_b[x][y][z] = 1

f_b, r_b, t_b = compute_views(grid_max_b, N)
if veq(f_b, q2b_F) and veq(r_b, q2b_R) and veq(t_b, q2b_T):
    print(f"\n整合的 - 配置可能セル数: {len(possible_b)}")

    min_b = None
    for num in range(1, len(possible_b) + 1):
        cnt = 0
        first_cfg = None
        for chosen in combinations(possible_b, num):
            grid = [[[0]*N for _ in range(N)] for _ in range(N)]
            for x, y, z in chosen:
                grid[x][y][z] = 1
            f, r, t = compute_views(grid, N)
            if veq(f, q2b_F) and veq(r, q2b_R) and veq(t, q2b_T):
                cnt += 1
                if first_cfg is None:
                    first_cfg = chosen
        if cnt > 0:
            if min_b is None:
                min_b = num
            print(f"  {num}個: {cnt}通り (例: {first_cfg})")

    print(f"\n最小: {min_b}, 最大: {len(possible_b)}")
else:
    print("不整合!")


# ============================================================
# 問2: パターンC
# ============================================================
print("\n" + "=" * 60)
print("問2: パターンC（十字型）")
print("=" * 60)

# 正面図:
# z=2: □ ■ □
# z=1: ■ ■ ■
# z=0: ■ ■ ■
q2c_F = [[1,1,0], [1,1,1], [1,1,0]]

# 右側面図:
# z=2: ■ □ □
# z=1: ■ ■ □
# z=0: ■ ■ ■
q2c_R = [[1,1,1], [1,1,0], [1,0,0]]

# 上面図:
# y=2: ■ ■ ■
# y=1: ■ ■ ■
# y=0: ■ ■ ■
q2c_T = [[1,1,1], [1,1,1], [1,1,1]]

possible_c = []
for x in range(N):
    for y in range(N):
        for z in range(N):
            if q2c_F[x][z] and q2c_R[y][z] and q2c_T[x][y]:
                possible_c.append((x, y, z))

grid_max_c = [[[0]*N for _ in range(N)] for _ in range(N)]
for x, y, z in possible_c:
    grid_max_c[x][y][z] = 1

f_c, r_c, t_c = compute_views(grid_max_c, N)
if veq(f_c, q2c_F) and veq(r_c, q2c_R) and veq(t_c, q2c_T):
    print(f"整合的 - 配置可能セル数: {len(possible_c)}")

    min_c = None
    for num in range(1, len(possible_c) + 1):
        cnt = 0
        first_cfg = None
        for chosen in combinations(possible_c, num):
            grid = [[[0]*N for _ in range(N)] for _ in range(N)]
            for x, y, z in chosen:
                grid[x][y][z] = 1
            f, r, t = compute_views(grid, N)
            if veq(f, q2c_F) and veq(r, q2c_R) and veq(t, q2c_T):
                cnt += 1
                if first_cfg is None:
                    first_cfg = chosen
        if cnt > 0:
            if min_c is None:
                min_c = num
            print(f"  {num}個: {cnt}通り")

    print(f"\n最小: {min_c}, 最大: {len(possible_c)}")
else:
    print("不整合!")


print("\n" + "=" * 60)
print("検証完了")
print("=" * 60)
