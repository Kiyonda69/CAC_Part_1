"""
セット95 解の一意性検証スクリプト

問1: 棒グラフ式数値符号化（3進法ベース）
問2: マンション階数配置（制約充足問題）
"""

from itertools import permutations

# =====================================================
# 問1: 棒の高さによる数値符号化
# =====================================================
# 4本の棒、各棒は3段階の高さ（低=0, 中=1, 高=2）
# 数値 n の符号 = (n-1) の3進表現
# 桁順: 左から 27の位, 9の位, 3の位, 1の位

def number_to_bars(n):
    """数値nを棒の高さ(0,1,2)の4桁タプルに変換"""
    val = n - 1
    d3 = val % 3; val //= 3
    d2 = val % 3; val //= 3
    d1 = val % 3; val //= 3
    d0 = val % 3
    return (d0, d1, d2, d3)

def bars_to_number(bars):
    """棒の高さタプルを数値に変換"""
    return bars[0]*27 + bars[1]*9 + bars[2]*3 + bars[3] + 1

print("=" * 50)
print("問1: 棒グラフ式数値符号化の検証")
print("=" * 50)

# 例の検証 (1-12)
print("\n例の確認:")
for n in range(1, 13):
    bars = number_to_bars(n)
    height_names = {0: "低", 1: "中", 2: "高"}
    bar_str = ", ".join(height_names[b] for b in bars)
    roundtrip = bars_to_number(bars)
    assert roundtrip == n, f"往復変換エラー: {n} → {bars} → {roundtrip}"
    print(f"  {n:2d}: ({bar_str}) = {bars}")

# 目標: 65
target = 65
target_bars = number_to_bars(target)
print(f"\n目標 {target}: {target_bars}")
print(f"  高さ: {', '.join({0:'低',1:'中',2:'高'}[b] for b in target_bars)}")
assert bars_to_number(target_bars) == target

# 選択肢の検証
choices = {
    1: (2, 1, 0, 0),  # 64
    2: (1, 2, 0, 1),  # 47
    3: (2, 1, 0, 1),  # 65 ← 正解
    4: (2, 0, 1, 1),  # 59
    5: (2, 1, 1, 0),  # 67
}

print("\n選択肢の検証:")
correct_count = 0
for i, bars in choices.items():
    num = bars_to_number(bars)
    is_correct = (num == target)
    if is_correct:
        correct_count += 1
    print(f"  ({i}) {bars} → {num} {'← 正解' if is_correct else ''}")

assert correct_count == 1, f"正解が{correct_count}個存在"
print(f"\n正解は選択肢(3)のみ → 解の一意性確認OK")

assert len(set(choices.values())) == 5, "重複する選択肢あり"
print("全選択肢が異なることを確認OK")


# =====================================================
# 問2: マンション階数配置（制約充足問題）
# =====================================================
print("\n" + "=" * 50)
print("問2: マンション階数配置の検証")
print("=" * 50)

# 5人: A, B, C, D, E が5階建てマンションの1階〜5階に住む（各人異なる階）
# 条件:
# 1. BはAより上の階に住んでいる (B > A)
# 2. DはCのちょうど2階上に住んでいる (D = C + 2)
# 3. Eは偶数階に住んでいる (E ∈ {2, 4})
# 4. Aは1階に住んでいない (A ≠ 1)
# 5. BとEは隣の階に住んでいない (|B - E| ≠ 1)

conditions = {
    "条件1 (B>A)": lambda A,B,C,D,E: B > A,
    "条件2 (D=C+2)": lambda A,B,C,D,E: D == C + 2,
    "条件3 (E偶数)": lambda A,B,C,D,E: E % 2 == 0,
    "条件4 (A≠1)": lambda A,B,C,D,E: A != 1,
    "条件5 (|B-E|≠1)": lambda A,B,C,D,E: abs(B - E) != 1,
}

valid_solutions = []

for perm in permutations([1, 2, 3, 4, 5]):
    A, B, C, D, E = perm
    if all(cond(A, B, C, D, E) for cond in conditions.values()):
        valid_solutions.append(perm)
        print(f"  有効解: A={A}F, B={B}F, C={C}F, D={D}F, E={E}F")

assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在"
A, B, C, D, E = valid_solutions[0]
print(f"\n唯一解: A={A}F, B={B}F, C={C}F, D={D}F, E={E}F")

# 質問: Dは何階に住んでいるか
print(f"\nDは何階に住んでいるか → {D}階")
assert D == 3, f"Dは3階想定だが{D}階"

# 各条件の必要性検証
print("\n各条件の必要性検証:")
for skip_name in conditions:
    count = 0
    for perm in permutations([1, 2, 3, 4, 5]):
        A, B, C, D, E = perm
        all_ok = True
        for name, cond in conditions.items():
            if name == skip_name:
                continue
            if not cond(A, B, C, D, E):
                all_ok = False
                break
        if all_ok:
            count += 1
    necessary = count > 1
    print(f"  {skip_name}を除外 → {count}個の解 (必要性: {'確認' if necessary else '不要!'})")
    assert necessary, f"{skip_name}は冗長な条件"

print(f"\n全条件が解導出に必要であることを確認OK")

# 選択肢: (1)1階 (2)2階 (3)3階 (4)4階 (5)5階
# 正解: (3)3階
print(f"\n選択肢: (1)1階 (2)2階 (3)3階 (4)4階 (5)5階")
print(f"正解: (3) 3階 → 解の一意性確認OK")

print("\n" + "=" * 50)
print("全検証完了")
print("=" * 50)
