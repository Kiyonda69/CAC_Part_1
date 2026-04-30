"""
問134 - 中国人郵便配達問題（一筆書き最短路）の検証
問1: 4×2 + 3×1 の格子道路網
問2: 2×1 + 4×2 + 2×1 のH型格子道路網
"""
from itertools import combinations
import heapq

def build_graph(squares):
    """squares: [(row, col), ...] の格子マスリストからグラフを構築"""
    edges = set()
    for (r, c) in squares:
        # 上辺: (r,c)-(r,c+1)
        edges.add((min((r,c),(r,c+1)), max((r,c),(r,c+1))))
        # 下辺: (r+1,c)-(r+1,c+1)
        edges.add((min((r+1,c),(r+1,c+1)), max((r+1,c),(r+1,c+1))))
        # 左辺: (r,c)-(r+1,c)
        edges.add((min((r,c),(r+1,c)), max((r,c),(r+1,c))))
        # 右辺: (r,c+1)-(r+1,c+1)
        edges.add((min((r,c+1),(r+1,c+1)), max((r,c+1),(r+1,c+1))))
    
    # 隣接リスト
    adj = {}
    for (u, v) in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    
    return list(edges), adj

def get_odd_degree_vertices(adj):
    return [v for v, neighbors in adj.items() if len(neighbors) % 2 == 1]

def shortest_path(adj, start, end):
    """BFSで最短路を計算（辺の重みは全て1）"""
    dist = {start: 0}
    queue = [start]
    i = 0
    while i < len(queue):
        u = queue[i]; i += 1
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist.get(end, float('inf'))

def min_matching(odd_vertices, adj):
    """奇数次数頂点の最小マッチング（全探索）"""
    n = len(odd_vertices)
    if n == 0:
        return 0
    
    # 全頂点間の最短路を事前計算
    dists = {}
    for i in range(n):
        for j in range(i+1, n):
            u, v = odd_vertices[i], odd_vertices[j]
            d = shortest_path(adj, u, v)
            dists[(i,j)] = d
            dists[(j,i)] = d
    
    # 最小マッチングをビットマスクDPで計算
    # (2^n状態)
    INF = float('inf')
    dp = [INF] * (1 << n)
    dp[0] = 0
    
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        # 最初の未使用頂点を見つける
        first = -1
        for i in range(n):
            if not (mask >> i & 1):
                first = i
                break
        if first == -1:
            continue
        # firstと別の未使用頂点をペアにする
        for second in range(first+1, n):
            if not (mask >> second & 1):
                new_mask = mask | (1 << first) | (1 << second)
                cost = dists[(first, second)]
                if dp[mask] + cost < dp[new_mask]:
                    dp[new_mask] = dp[mask] + cost
    
    return dp[(1 << n) - 1]

def solve(name, squares, p_label="P"):
    print(f"\n{'='*50}")
    print(f"{name}")
    edges, adj = build_graph(squares)
    total_edges = len(edges)
    print(f"総辺数: {total_edges}")
    
    odd_verts = get_odd_degree_vertices(adj)
    print(f"奇数次数頂点数: {len(odd_verts)}")
    print(f"奇数次数頂点: {sorted(odd_verts)}")
    
    extra = min_matching(odd_verts, adj)
    print(f"追加辺数（最小マッチング）: {extra}")
    answer = total_edges + extra
    print(f"最小道路数: {answer}")
    return answer

# 問1: 4×2 + 3×1 の格子（上2行は幅4、下1行は幅3）
# Row 0: cols 0-3, Row 1: cols 0-3, Row 2: cols 0-2
squares_q1 = [(r, c) for r in range(2) for c in range(4)] + [(2, c) for c in range(3)]
ans1 = solve("問1: 4x2+3x1 格子", squares_q1)

# 問2: H型 (上2行は幅2、中2行は幅4、下2行は幅2)
# Row 0-1: cols 0-1, Row 2-3: cols 0-3, Row 4-5: cols 2-3
squares_q2 = ([(r, c) for r in range(2) for c in range(2)] + 
              [(r, c) for r in range(2,4) for c in range(4)] + 
              [(r, c) for r in range(4,6) for c in range(2,4)])
ans2 = solve("問2: H型格子", squares_q2)

print(f"\n{'='*50}")
print(f"問1の答え: {ans1}本")
print(f"問2の答え: {ans2}本")

# 正解番号のランダム化
import random
random.seed()
pos1 = random.randint(1, 5)
pos2 = random.randint(1, 5)
print(f"問1正解位置: {pos1}")
print(f"問2正解位置: {pos2}")

# 選択肢の生成（正解を指定位置に配置）
def make_choices(answer, pos):
    choices = list(range(answer - pos + 1, answer - pos + 6))
    return choices

print(f"問1選択肢: {make_choices(ans1, pos1)}")
print(f"問2選択肢: {make_choices(ans2, pos2)}")

print("\n\n--- 別設計の検証 ---")

# 案2a: T字型 (上5行=幅4、下3行=幅2で中央寄り)
# Row 0: cols 0-3 (4 squares top)
# Row 1: cols 1-2 (2 squares stem)
# Row 2: cols 1-2 (2 squares stem)
squares_T = [(0, c) for c in range(4)] + [(r, c) for r in range(1,3) for c in range(1,3)]
ans_T = solve("T字型", squares_T)

# 案2b: 階段型4段 (4x1ずつオフセット)
# Row 0: col 0 (1 sq)
# Row 1: cols 0-1 (2 sq)
# Row 2: cols 1-2 (2 sq)
# Row 3: cols 2-3 (2 sq)
# Row 4: col 3 (1 sq)
squares_stairs = ([(0,0)] + [(1,c) for c in range(2)] + [(2,c) for c in range(1,3)] + 
                  [(3,c) for c in range(2,4)] + [(4,3)])
ans_stairs = solve("階段型4段", squares_stairs)

# 案2c: 5×2 + 4×1 (問1より大きい同型の問題)
# Row 0: cols 0-4 (5 squares)
# Row 1: cols 0-4 (5 squares)
# Row 2: cols 0-3 (4 squares)
squares_q2c = [(r, c) for r in range(2) for c in range(5)] + [(2, c) for c in range(4)]
ans_q2c = solve("5x2+4x1 格子", squares_q2c)

# 案2d: 4×3 から角を除いた形（L字）
# Row 0: cols 0-3 (4 squares)
# Row 1: cols 0-3 (4 squares)
# Row 2: cols 0-1 (2 squares, 左下のみ)
squares_L = [(r, c) for r in range(2) for c in range(4)] + [(2, c) for c in range(2)]
ans_L = solve("L字型(4x2+2x1)", squares_L)

