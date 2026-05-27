"""
航大思考191 検証スクリプト: 立体図形の一筆書き（オイラー路・閉路）

一筆書きの定理:
- 連結グラフが一筆書き可能 <=> 奇数次数の頂点が 0個 または 2個
- 出発点に戻れる(オイラー閉路) <=> 奇数次数の頂点が 0個
- 0個: 任意の点から始め同じ点に戻れる(閉路)
- 2個: その2点を始点・終点とする一筆書き(路)のみ
"""
from itertools import combinations


def degrees(n_vertices, edges):
    deg = {v: 0 for v in range(n_vertices)}
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    return deg


def is_connected(n_vertices, edges):
    """辺を持つ頂点が全て連結か(孤立点は無視)"""
    used = set()
    for a, b in edges:
        used.add(a)
        used.add(b)
    if not used:
        return True
    adj = {v: set() for v in used}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    start = next(iter(used))
    stack = [start]
    seen = {start}
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen == used


def odd_count(n_vertices, edges):
    return sum(1 for d in degrees(n_vertices, edges).values() if d % 2 == 1)


def min_strokes(n_vertices, edges):
    """連結グラフの全辺を描く最小筆数 = max(1, 奇点数/2)"""
    assert is_connected(n_vertices, edges)
    oc = odd_count(n_vertices, edges)
    return max(1, oc // 2)


# ---- 立体の辺グラフ定義 ----
# 正四面体: 4頂点・全結合(6辺)、各次数3
tetra = (4, list(combinations(range(4), 2)))

# 立方体: 8頂点・12辺、各次数3
cube = (8, [(0, 1), (1, 2), (2, 3), (3, 0),       # 上面
            (4, 5), (5, 6), (6, 7), (7, 4),       # 下面
            (0, 4), (1, 5), (2, 6), (3, 7)])      # 垂直

# 三角柱: 6頂点・9辺、各次数3
prism = (6, [(0, 1), (1, 2), (2, 0),              # 上三角
             (3, 4), (4, 5), (5, 3),              # 下三角
             (0, 3), (1, 4), (2, 5)])             # 垂直

# 四角錐: 頂点0=apex, 1-4=底面正方形。8辺。apex次数4、底面各次数3
sq_pyramid = (5, [(1, 2), (2, 3), (3, 4), (4, 1),  # 底面
                  (0, 1), (0, 2), (0, 3), (0, 4)])  # 側面

# 三角双錐: 0=上頂点,1=下頂点,2,3,4=赤道三角形。9辺
# 上下頂点 次数3、赤道頂点 次数4 -> 奇数頂点2個
tri_bipyramid = (5, [(2, 3), (3, 4), (4, 2),        # 赤道三角形
                     (0, 2), (0, 3), (0, 4),        # 上頂点
                     (1, 2), (1, 3), (1, 4)])       # 下頂点

# 正八面体(=四角双錐): 0=上,1=下,2,3,4,5=赤道正方形。12辺、全次数4 -> 奇数0個
octahedron = (6, [(2, 3), (3, 4), (4, 5), (5, 2),   # 赤道正方形
                  (0, 2), (0, 3), (0, 4), (0, 5),   # 上頂点
                  (1, 2), (1, 3), (1, 4), (1, 5)])   # 下頂点

# 切妻屋根の家型立体: 0-3=底面正方形, 4-7=壁の上(天井)正方形, 8,9=屋根の棟の両端
# 底面4頂点=次数3(奇), 天井4頂点=次数4(偶), 棟2頂点=次数3(奇) -> 奇点6個 -> 最小3筆
house = (10, [(0, 1), (1, 2), (2, 3), (3, 0),       # 底面正方形
              (0, 4), (1, 5), (2, 6), (3, 7),       # 垂直の柱
              (4, 5), (5, 6), (6, 7), (7, 4),       # 天井(壁の上)正方形
              (8, 4), (8, 5), (9, 6), (9, 7), (8, 9)])  # 屋根(妻面2枚+棟)

solids = {
    "正四面体": tetra,
    "立方体": cube,
    "三角柱": prism,
    "四角錐": sq_pyramid,
    "三角双錐": tri_bipyramid,
    "正八面体": octahedron,
    "切妻屋根の家": house,
}

print("=== 各立体の解析 ===")
for name, (n, edges) in solids.items():
    oc = odd_count(n, edges)
    conn = is_connected(n, edges)
    drawable = conn and oc in (0, 2)
    circuit = conn and oc == 0
    print(f"{name:6s}: 辺数={len(edges):2d} 奇数頂点={oc} "
          f"一筆書き={'可' if drawable else '不可'} "
          f"閉路={'可' if circuit else '不可'}")

# ---- 問1: 一筆書き可能なものは1つだけか ----
q1_set = ["正四面体", "立方体", "三角柱", "四角錐", "三角双錐"]
q1_ok = [name for name in q1_set
         if is_connected(*solids[name]) and odd_count(*solids[name]) in (0, 2)]
print("\n=== 問1(一筆書き可能) ===")
print(f"選択肢: {q1_set}")
print(f"一筆書き可能: {q1_ok}")
assert q1_ok == ["三角双錐"], f"問1の解が一意でない: {q1_ok}"
print("OK: 正解は三角双錐のみ")

# ---- 問2: 切妻屋根の家型立体の全辺を描く最小筆数 ----
n, edges = solids["切妻屋根の家"]
print("\n=== 問2(家型立体の最小筆数) ===")
deg = degrees(n, edges)
print(f"辺数={len(edges)} 各頂点の次数={sorted(deg.values())}")
oc = odd_count(n, edges)
ms = min_strokes(n, edges)
print(f"連結={is_connected(n, edges)} 奇点数={oc} 最小筆数={ms}")
assert is_connected(n, edges), "家型が連結でない"
assert oc == 6, f"奇点数が6でない: {oc}"
assert ms == 3, f"最小筆数が3でない: {ms}"
# 罠の確認: 底面のみ/天井のみを見ると誤る。底面4頂点(奇)+棟2頂点(奇)=6が正しい
odd_vertices = sorted(v for v, d in deg.items() if d % 2 == 1)
assert odd_vertices == [0, 1, 2, 3, 8, 9], f"奇点の位置が想定外: {odd_vertices}"
print("OK: 最小筆数は3筆(奇点は底面4頂点と棟2頂点の計6個)")

print("\n全検証パス")
