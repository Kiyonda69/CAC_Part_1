"""
航大思考114 検証スクリプト

問1: 数列 2, 5, 11, 23, 47, ? の規則
  - a(n+1) = 2·a(n) + 1
  - 差分: 3, 6, 12, 24 (公比2の等比数列)
  - 一般項: a(n) = 3·2^(n-1) - 1
  
問2: 4×4数表 a(r,c) = 2^r + 3^c - 1 の規則
  - 行方向: 公比3の差分（6, 18, 54）
  - 列方向: 公比2の差分（2, 4, 8）
  - 空欄(3,3)の値を求める
"""

def verify_q1():
    """問1: 数列の規則性検証"""
    print("=" * 60)
    print("問1: 数列 2, 5, 11, 23, 47, ? の検証")
    print("=" * 60)
    
    # 規則1: a(n+1) = 2·a(n) + 1
    seq = [2]
    for i in range(5):
        seq.append(2 * seq[-1] + 1)
    print(f"規則1 (a(n+1)=2·a(n)+1): {seq}")
    
    # 規則2: 差分が公比2
    diffs = [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    print(f"差分: {diffs}")
    diff_ratios = [diffs[i+1] / diffs[i] for i in range(len(diffs)-1)]
    print(f"差分の比: {diff_ratios}")
    
    # 規則3: 一般項 a(n) = 3·2^(n-1) - 1
    formula_seq = [3 * 2**(n-1) - 1 for n in range(1, 7)]
    print(f"一般項 a(n) = 3·2^(n-1) - 1: {formula_seq}")
    
    assert seq == formula_seq, "規則1と一般項が一致しない"
    
    answer = seq[5]
    print(f"\n答え: a(6) = {answer}")
    
    # 選択肢の検討
    print("\n誤答候補の分析:")
    print(f"  47 + 24 (差分倍化せず) = {47 + 24}")
    print(f"  47 + 30 (差分公差6と誤認) = {47 + 30}")
    print(f"  47 + 36 (差分公差12と誤認) = {47 + 36}")
    print(f"  47 + 42 (差分公差を恣意的) = {47 + 42}")
    print(f"  47 × 2 - 1 (規則誤認) = {47 * 2 - 1}")
    print(f"  47 × 2 + 2 (規則誤認) = {47 * 2 + 2}")
    print(f"  47 + 48 (正解) = {47 + 48}")
    
    return answer


def verify_q2():
    """問2: 4×4数表の規則性検証"""
    print("\n" + "=" * 60)
    print("問2: 数表 a(r,c) = 2^r + 3^c - 1 の検証")
    print("=" * 60)
    
    # 数表生成
    table = {}
    for r in range(1, 5):
        for c in range(1, 5):
            table[(r, c)] = 2**r + 3**c - 1
    
    print("\n数表:")
    print("       c=1   c=2   c=3   c=4")
    for r in range(1, 5):
        row = f"r={r}: "
        for c in range(1, 5):
            row += f"  {table[(r,c)]:4d}"
        print(row)
    
    # 行方向の差分検証
    print("\n行方向の差分（公比3になるはず）:")
    for r in range(1, 5):
        row_vals = [table[(r,c)] for c in range(1, 5)]
        diffs = [row_vals[i+1] - row_vals[i] for i in range(3)]
        ratios = [diffs[i+1] / diffs[i] for i in range(2)]
        print(f"  行{r}: 値={row_vals}, 差分={diffs}, 比={ratios}")
    
    # 列方向の差分検証
    print("\n列方向の差分（公比2になるはず）:")
    for c in range(1, 5):
        col_vals = [table[(r,c)] for r in range(1, 5)]
        diffs = [col_vals[i+1] - col_vals[i] for i in range(3)]
        ratios = [diffs[i+1] / diffs[i] for i in range(2)]
        print(f"  列{c}: 値={col_vals}, 差分={diffs}, 比={ratios}")
    
    # 空欄 (3,3) の値
    answer = table[(3, 3)]
    print(f"\n空欄 (r=3, c=3) の値: {answer}")
    
    # 検証: 行3から
    print("\n【行3からの検証】")
    print(f"  10, 16 → 差分6")
    print(f"  16 + 18 (6×3) = 34")
    print(f"  34 + 54 (18×3) = 88 ✓")
    
    # 検証: 列3から
    print("\n【列3からの検証】")
    print(f"  28, 30 → 差分2")
    print(f"  30 + 4 (2×2) = 34")
    print(f"  34 + 8 (4×2) = 42 ✓")
    
    # 一意性検証: 行・列のパターンに合うのは34のみ
    print("\n【一意性検証】")
    candidates = []
    for v in range(0, 200):
        # 行3条件: 10, 16, v, 88 → 差分6, v-16, 88-v が公比3
        d1 = 6
        d2 = v - 16
        d3 = 88 - v
        # 列3条件: 28, 30, v, 42 → 差分2, v-30, 42-v が公比2
        e1 = 2
        e2 = v - 30
        e3 = 42 - v
        
        row_ok = (d2 == d1 * 3) and (d3 == d2 * 3)
        col_ok = (e2 == e1 * 2) and (e3 == e2 * 2)
        
        if row_ok and col_ok:
            candidates.append(v)
    
    print(f"  両パターンを満たす値: {candidates}")
    assert len(candidates) == 1 and candidates[0] == answer, "解が一意でない"
    print(f"  ✓ 解は一意 ({candidates[0]})")
    
    # 誤答候補の分析
    print("\n誤答候補の分析:")
    print(f"  16 × 2 = 32 (列の規則を値に適用)")
    print(f"  30 + 2 = 32 (差分を倍化せず)")
    print(f"  16 + 8 = 24 (列の差分を行に適用)")
    print(f"  6 × 6 = 36 (誤った積)")
    print(f"  42 = (4,3)の値と誤認")
    print(f"  30 + 6 = 36 (差分混同)")
    print(f"  正解: {answer}")
    
    return answer


if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print("\n" + "=" * 60)
    print(f"問1の答え: {a1}")
    print(f"問2の答え: {a2}")
    print("=" * 60)
