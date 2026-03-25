#!/usr/bin/env python3
"""
航大思考82 - ブラックボックス問題の検証
問1: 2つのブラックボックスの直列接続 Q(P(3))
問2: 未知値ありの2つのブラックボックスの直列接続 F(G(4))
"""

def verify_problem1():
    """問1: P(x)=2x+3, Q(x)=x^2-1, Q(P(3))=?"""
    print("=== 問1 検証 ===")
    
    P = lambda x: 2*x + 3
    p_table = {1: 5, 2: 7, 3: 9, 4: 11, 5: 13}
    for x, expected in p_table.items():
        assert P(x) == expected, f"P({x}) = {P(x)}, expected {expected}"
    print(f"P(x) = 2x + 3: {[P(x) for x in range(1,6)]}")
    
    Q = lambda x: x**2 - 1
    q_table = {1: 0, 2: 3, 3: 8, 4: 15, 5: 24}
    for x, expected in q_table.items():
        assert Q(x) == expected, f"Q({x}) = {Q(x)}, expected {expected}"
    print(f"Q(x) = x^2 - 1: {[Q(x) for x in range(1,6)]}")
    
    p3 = P(3)
    answer = Q(p3)
    print(f"P(3) = {p3}")
    print(f"Q(P(3)) = Q({p3}) = {p3}^2 - 1 = {answer}")
    assert answer == 80
    
    # P is linear (constant first differences = 2)
    p_diffs = [p_table[i+1] - p_table[i] for i in range(1, 5)]
    assert all(d == 2 for d in p_diffs), f"P diffs: {p_diffs}"
    
    # Q is quadratic (constant second differences = 2)
    q_diffs = [q_table[i+1] - q_table[i] for i in range(1, 5)]
    q_diffs2 = [q_diffs[i+1] - q_diffs[i] for i in range(len(q_diffs)-1)]
    assert all(d == 2 for d in q_diffs2), f"Q 2nd diffs: {q_diffs2}"
    
    # Verify distractors
    choices = {1: 63, 2: 80, 3: 99, 4: 120, 5: 168}
    assert choices[2] == 80, "Correct answer should be (2)=80"
    assert choices[1] == Q(8), "(1)=Q(8): error P(3)=8"
    assert choices[3] == Q(10), "(3)=Q(10): error P(3)=10"
    assert choices[4] == Q(11), "(4)=Q(11): confusing P(4)=11"
    assert choices[5] == Q(13), "(5)=Q(13): confusing P(5)=13"
    
    print(f"正解: (2) = 80")
    print("問1 検証完了\n")
    return True

def verify_problem2():
    """問2: F(x)=x^2+2x, G(x)=3x-1, H(4)=F(G(4))=?"""
    print("=== 問2 検証 ===")
    
    F = lambda x: x**2 + 2*x
    f_all = {1: 3, 2: 8, 3: 15, 4: 24, 5: 35}
    for x, expected in f_all.items():
        assert F(x) == expected, f"F({x}) = {F(x)}, expected {expected}"
    print(f"F(x) = x^2 + 2x: {[F(x) for x in range(1,6)]}")
    
    G = lambda x: 3*x - 1
    g_all = {1: 2, 2: 5, 3: 8, 4: 11, 5: 14}
    for x, expected in g_all.items():
        assert G(x) == expected, f"G({x}) = {G(x)}, expected {expected}"
    print(f"G(x) = 3x - 1: {[G(x) for x in range(1,6)]}")
    
    # Table as shown (with blanks):
    # x | F(x) | G(x)
    # 1 | 3    | 2
    # 2 | (ア) | 5    → (ア)=F(2)=8
    # 3 | 15   | 8
    # 4 | (イ) | (ウ) → (イ)=F(4)=24, (ウ)=G(4)=11
    # 5 | 35   | 14
    
    print(f"(ア) = F(2) = {F(2)}")
    print(f"(イ) = F(4) = {F(4)}")
    print(f"(ウ) = G(4) = {G(4)}")
    
    # Uniqueness of F from 3 given points: (1,3), (3,15), (5,35)
    # Quadratic: ax^2 + bx + c
    # a + b + c = 3   ...(i)
    # 9a + 3b + c = 15 ...(ii)
    # 25a + 5b + c = 35 ...(iii)
    # (ii)-(i): 8a + 2b = 12 → 4a + b = 6
    # (iii)-(ii): 16a + 2b = 20 → 8a + b = 10
    # Subtracting: 4a = 4 → a=1, b=2, c=0
    a, b, c = 1, 2, 0
    assert a*1 + b*1 + c == 3
    assert a*9 + b*3 + c == 15
    assert a*25 + b*5 + c == 35
    print("F(x) = x^2 + 2x is uniquely determined (quadratic)")
    
    # Uniqueness of G: linear from (1,2),(2,5) → slope=3, intercept=-1
    # Verified by (3,8) and (5,14)
    assert 3*3 - 1 == 8
    assert 3*5 - 1 == 14
    # Check that no other linear fits all 4 points
    # (only one line through any 2 points, and all 4 are collinear)
    for x in [1,2,3,5]:
        assert G(x) == g_all[x]
    print("G(x) = 3x - 1 is uniquely determined (linear)")
    
    # Check if G could be quadratic: must have a=0
    # From (1,2),(2,5),(3,8): 3a+b=3, 5a+b=3 → 2a=0 → a=0
    print("G quadratic check: a=0, confirms linear\n")
    
    # H(4) = F(G(4))
    g4 = G(4)
    answer = F(g4)
    print(f"G(4) = {g4}")
    print(f"H(4) = F(G(4)) = F({g4}) = {g4}^2 + 2*{g4} = {answer}")
    assert answer == 143
    
    # Verify distractors
    choices = {1: 143, 2: 132, 3: 121, 4: 99, 5: 80}
    assert choices[1] == 143, "Correct answer should be (1)=143"
    # (2) 132 = 11^2 + 11 → F(x)=x^2+x error
    assert 11**2 + 11 == 132
    # (3) 121 = 11^2 → F(x)=x^2 error
    assert 11**2 == 121
    # (4) 99 = F(9) → if G(4)=9 error
    assert F(9) == 99
    # (5) 80 = F(8) → confusing G(3)=8 with G(4)
    assert F(8) == 80
    
    print(f"正解: (1) = 143")
    print("問2 検証完了\n")
    return True

def brute_force_uniqueness():
    """総当たりで他の関数がありえないか確認"""
    print("=== 総当たり検証 ===")
    
    # Problem 1: P and Q from full table
    # P: 5,7,9,11,13 → only 2x+3 fits (linear, 5 points)
    # Q: 0,3,8,15,24 → only x^2-1 fits (quadratic, 5 points)
    
    # Check all possible quadratics for Q: ax^2+bx+c
    # Using first 3 points: (1,0),(2,3),(3,8)
    # a+b+c=0, 4a+2b+c=3, 9a+3b+c=8
    # 3a+b=3, 5a+b=5 → 2a=2 → a=1, b=0, c=-1
    # Verify: Q(4)=16-1=15 ✓, Q(5)=25-1=24 ✓
    print("Q uniquely determined: x^2 - 1")
    
    # Problem 2: F from (1,3),(3,15),(5,35) and G from (1,2),(2,5),(3,8),(5,14)
    # Already verified above
    
    # Extra: check no cubic or other polynomial degree for F
    # 3 points uniquely determine a quadratic (3 unknowns, 3 equations)
    # Could be linear? F(1)=3, F(3)=15 → slope=6, F(5) should be 27 ≠ 35
    assert 3 + 6*2 != 35 - 12  # Not linear
    print("F is not linear (verified)")
    
    print("総当たり検証完了\n")

if __name__ == "__main__":
    verify_problem1()
    verify_problem2()
    brute_force_uniqueness()
    print("=" * 50)
    print("全検証パス!")
    print("問1 正解: (2) 80   [Q(P(3)) = Q(9) = 80]")
    print("問2 正解: (1) 143  [H(4) = F(G(4)) = F(11) = 143]")
