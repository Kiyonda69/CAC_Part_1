"""
問2: 嘘つき推論問題（高難度）
5人(A～E)のうち、ちょうど2人が嘘つき。正直者は真実、嘘つきは嘘を述べる。

A:「CとEは両方とも正直者だ。」
B:「Aは嘘つきだ。」
C:「BとDのうち、少なくとも1人は嘘つきだ。」
D:「Eは嘘つきだ。」
E:「Aは正直者だ。」

検証対象:
ア. Aは正直者である。
イ. Bは嘘つきである。
ウ. Cは嘘つきである。
"""

from itertools import combinations

people = ['A', 'B', 'C', 'D', 'E']

def check_assignment(liars_set):
    """与えられた嘘つき集合が全発言と整合するか検証"""
    def is_honest(p):
        return p not in liars_set
    
    def is_liar(p):
        return p in liars_set
    
    # A: 「CとEは両方とも正直者だ」
    a_statement = is_honest('C') and is_honest('E')
    if is_honest('A') and not a_statement:
        return False
    if is_liar('A') and a_statement:
        return False
    
    # B: 「Aは嘘つきだ」
    b_statement = is_liar('A')
    if is_honest('B') and not b_statement:
        return False
    if is_liar('B') and b_statement:
        return False
    
    # C: 「BとDのうち、少なくとも1人は嘘つきだ」
    c_statement = is_liar('B') or is_liar('D')
    if is_honest('C') and not c_statement:
        return False
    if is_liar('C') and c_statement:
        return False
    
    # D: 「Eは嘘つきだ」
    d_statement = is_liar('E')
    if is_honest('D') and not d_statement:
        return False
    if is_liar('D') and d_statement:
        return False
    
    # E: 「Aは正直者だ」
    e_statement = is_honest('A')
    if is_honest('E') and not e_statement:
        return False
    if is_liar('E') and e_statement:
        return False
    
    return True

solutions = []
for liars in combinations(people, 2):
    liars_set = set(liars)
    if check_assignment(liars_set):
        solutions.append(liars_set)
        print(f"解: 嘘つき = {liars_set}")

print(f"\n解の数: {len(solutions)}")

if len(solutions) == 1:
    sol = solutions[0]
    print(f"\n=== 正解判定 ===")
    print(f"嘘つき: {sol}")
    print(f"ア. Aは正直者 → {'A' not in sol}")
    print(f"イ. Bは嘘つき → {'B' in sol}")
    print(f"ウ. Cは嘘つき → {'C' in sol}")
    
    a_correct = 'A' not in sol
    b_correct = 'B' in sol
    c_correct = 'C' in sol
    
    if a_correct and b_correct and not c_correct:
        print("ア、イが正しい → 正解(4)")
else:
    print("解が一意でない！再設計が必要")
