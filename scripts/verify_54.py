#!/usr/bin/env python3
"""
セット54 検証スクリプト
問1: 港湾の種類別取扱状況 - 入港船舶1隻あたりの貨物取扱量が2番目に多い区分
問2: 交通機関別旅客輸送状況 - 4つの記述の正誤判定
"""

print("=" * 60)
print("セット54 解の検証")
print("=" * 60)

# ========== 問1: 港湾データ ==========
print("\n【問1】港湾の種類別取扱状況")
print("-" * 40)

data_q1 = {
    "国際戦略港湾": {"港湾数": 5, "入港船舶数": 168420, "貨物取扱量": 458720, "外貿コンテナ": 18245},
    "国際拠点港湾": {"港湾数": 18, "入港船舶数": 225680, "貨物取扱量": 312560, "外貿コンテナ": 4128},
    "重要港湾":     {"港湾数": 102, "入港船舶数": 245600, "貨物取扱量": 285350, "外貿コンテナ": 1256},
    "地方港湾":     {"港湾数": 808, "入港船舶数": 186320, "貨物取扱量": 82480, "外貿コンテナ": 428},
    "56条港湾":     {"港湾数": 42, "入港船舶数": 8650, "貨物取扱量": 3280, "外貿コンテナ": 12},
}

# 小計（国際港湾）
intl_ships = data_q1["国際戦略港湾"]["入港船舶数"] + data_q1["国際拠点港湾"]["入港船舶数"]
intl_cargo = data_q1["国際戦略港湾"]["貨物取扱量"] + data_q1["国際拠点港湾"]["貨物取扱量"]
intl_container = data_q1["国際戦略港湾"]["外貿コンテナ"] + data_q1["国際拠点港湾"]["外貿コンテナ"]
intl_ports = data_q1["国際戦略港湾"]["港湾数"] + data_q1["国際拠点港湾"]["港湾数"]
print(f"国際港湾小計: 港湾数={intl_ports}, 入港={intl_ships}, 貨物={intl_cargo}, コンテナ={intl_container}")

# 合計
total_ports = sum(d["港湾数"] for d in data_q1.values())
total_ships = sum(d["入港船舶数"] for d in data_q1.values())
total_cargo = sum(d["貨物取扱量"] for d in data_q1.values())
total_container = sum(d["外貿コンテナ"] for d in data_q1.values())
print(f"合計: 港湾数={total_ports}, 入港={total_ships}, 貨物={total_cargo}, コンテナ={total_container}")

# 入港船舶1隻あたりの貨物取扱量を計算
print("\n【入港船舶1隻あたりの貨物取扱量（千トン/隻）】")
ratios_q1 = {}
for name, d in data_q1.items():
    ratio = d["貨物取扱量"] / d["入港船舶数"]
    ratios_q1[name] = ratio
    print(f"  {name}: {d['貨物取扱量']:,} / {d['入港船舶数']:,} = {ratio:.3f}")

# 順位
sorted_q1 = sorted(ratios_q1.items(), key=lambda x: x[1], reverse=True)
print("\n【順位】")
for i, (name, ratio) in enumerate(sorted_q1):
    print(f"  {i+1}位: {name} ({ratio:.3f})")

answer_q1 = sorted_q1[1][0]  # 2番目
print(f"\n→ 2番目に多いのは: {answer_q1}")

# ========== 問2: 交通機関データ ==========
print("\n\n【問2】交通機関別旅客輸送状況")
print("-" * 40)

data_q2 = {
    "鉄道(JR)":   {"事業者数": 6,     "旅客数": 9284,  "旅客キロ": 2845, "営業収入": 42680, "従業員数": 128},
    "鉄道(民鉄)": {"事業者数": 189,   "旅客数": 5482,  "旅客キロ": 1326, "営業収入": 18450, "従業員数": 86},
    "バス":       {"事業者数": 2245,  "旅客数": 3856,  "旅客キロ": 428,  "営業収入": 12340, "従業員数": 185},
    "タクシー":    {"事業者数": 58420, "旅客数": 1248,  "旅客キロ": 85,   "営業収入": 15680, "従業員数": 295},
    "航空":       {"事業者数": 28,    "旅客数": 1056,  "旅客キロ": 1128, "営業収入": 34520, "従業員数": 62},
}

print("\n【ア】旅客1人あたりの平均移動距離が最も長い交通機関は航空である")
print("  旅客キロ(億人km) / 旅客数(百万人) × 100 = 平均距離(km)")
avg_dist = {}
for name, d in data_q2.items():
    dist = (d["旅客キロ"] / d["旅客数"]) * 100
    avg_dist[name] = dist
    print(f"  {name}: ({d['旅客キロ']}/{d['旅客数']})×100 = {dist:.1f} km")
max_dist = max(avg_dist.items(), key=lambda x: x[1])
print(f"  → 最長: {max_dist[0]} ({max_dist[1]:.1f} km)")
a_correct = max_dist[0] == "航空"
print(f"  → ア: {'正しい' if a_correct else '誤り'}")

print("\n【イ】従業員1千人あたりの営業収入が最も高い交通機関は鉄道(JR)である")
rev_per_emp = {}
for name, d in data_q2.items():
    r = d["営業収入"] / d["従業員数"]
    rev_per_emp[name] = r
    print(f"  {name}: {d['営業収入']:,} / {d['従業員数']} = {r:.1f}")
max_rev = max(rev_per_emp.items(), key=lambda x: x[1])
print(f"  → 最高: {max_rev[0]} ({max_rev[1]:.1f})")
b_correct = max_rev[0] == "鉄道(JR)"
print(f"  → イ: {'正しい' if b_correct else '誤り'}")

print("\n【ウ】旅客キロ1億人kmあたりの営業収入が最も高い交通機関はタクシーである")
rev_per_km = {}
for name, d in data_q2.items():
    r = d["営業収入"] / d["旅客キロ"]
    rev_per_km[name] = r
    print(f"  {name}: {d['営業収入']:,} / {d['旅客キロ']} = {r:.1f}")
max_rpk = max(rev_per_km.items(), key=lambda x: x[1])
print(f"  → 最高: {max_rpk[0]} ({max_rpk[1]:.1f})")
c_correct = max_rpk[0] == "タクシー"
print(f"  → ウ: {'正しい' if c_correct else '誤り'}")

print("\n【エ】鉄道(民鉄)の従業員数は全交通機関の合計従業員数の15%を超える")
total_emp = sum(d["従業員数"] for d in data_q2.values())
mintetsu_ratio = data_q2["鉄道(民鉄)"]["従業員数"] / total_emp * 100
print(f"  合計従業員数: {total_emp}千人")
print(f"  民鉄: {data_q2['鉄道(民鉄)']['従業員数']}千人")
print(f"  割合: {mintetsu_ratio:.1f}%")
d_correct = mintetsu_ratio > 15
print(f"  → エ: {'正しい' if d_correct else '誤り'}")

print(f"\n【結果】")
print(f"  ア: {'正' if a_correct else '誤'}, イ: {'正' if b_correct else '誤'}, ウ: {'正' if c_correct else '誤'}, エ: {'正' if d_correct else '誤'}")
correct_stmts = []
if a_correct: correct_stmts.append("ア")
if b_correct: correct_stmts.append("イ")
if c_correct: correct_stmts.append("ウ")
if d_correct: correct_stmts.append("エ")
print(f"  正しい記述: {', '.join(correct_stmts)}")
assert len(correct_stmts) == 2, f"正しい記述が{len(correct_stmts)}個（2個必要）"
assert correct_stmts == ["ア", "ウ"], f"正しい記述がア,ウでない: {correct_stmts}"
print("\n検証完了: 問1・問2ともに解が一意です。")
