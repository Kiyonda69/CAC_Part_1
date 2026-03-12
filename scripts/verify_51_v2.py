#!/usr/bin/env python3
"""
セット51 検証スクリプト v2
問2の命題を再設計（正しい命題が2つになるよう調整）
"""

stops = ['P', 'Q', 'R', 'S', 'T', 'U']

valid_configs = []
X_stops = {'P', 'Q', 'R'}

for y_third in ['T', 'U']:
    Y_stops = {'R', 'S', y_third}
    possible_z = ['R', 'T', 'U']
    from itertools import combinations
    for z_combo in combinations(possible_z, 2):
        Z_stops = set(z_combo)
        all_covered = all(
            s in X_stops or s in Y_stops or s in Z_stops for s in stops
        )
        if not all_covered:
            continue
        if 'P' in Y_stops or 'P' in Z_stops:
            continue
        if 'Q' in Y_stops or 'Q' in Z_stops:
            continue
        if 'S' in X_stops or 'S' in Z_stops:
            continue
        
        stop_routes = {}
        for s in stops:
            sr = set()
            if s in X_stops: sr.add('X')
            if s in Y_stops: sr.add('Y')
            if s in Z_stops: sr.add('Z')
            stop_routes[s] = sr
        valid_configs.append(stop_routes)

print(f"有効な配置数: {len(valid_configs)}")
for i, sr in enumerate(valid_configs):
    print(f"配置{i+1}: ", {s: sorted(r) for s, r in sr.items()})

# 新しい命題
statements = {}

# ア: 路線Zが通る停留所のうち少なくとも1つは路線Yも通る
statements["ア"] = []
for sr in valid_configs:
    z_stops = [s for s in stops if 'Z' in sr[s]]
    result = any('Y' in sr[s] for s in z_stops)
    statements["ア"].append(result)

# イ: Rには路線X, Y, Zの3つすべてが通る
statements["イ"] = []
for sr in valid_configs:
    statements["イ"].append(len(sr['R']) == 3)

# ウ: TとUのうち路線Yが通るのはちょうど1つ
statements["ウ"] = []
for sr in valid_configs:
    y_count = sum(1 for s in ['T', 'U'] if 'Y' in sr[s])
    statements["ウ"].append(y_count == 1)

# エ: 2つ以上の路線が通る停留所はちょうど2つ
statements["エ"] = []
for sr in valid_configs:
    multi = sum(1 for s in stops if len(sr[s]) >= 2)
    statements["エ"].append(multi == 2)

print("\n命題検証:")
for name, results in statements.items():
    always = all(results)
    print(f"  {name}: {'常に真 ✓' if always else '場合による ✗'} ({sum(results)}/{len(results)})")

certain = [k for k, v in statements.items() if all(v)]
print(f"\n確実にいえる命題: {', '.join(certain)}")
print("正解: ア、ウ の組み合わせ")

