"""
航大思考178 解の一意性検証

問1: ブラックボックスNの入出力表からN(7)を求める
問2: ブラックボックスPとQ(並列構成)からS(6)を求める
"""


def verify_q1():
    """問1: N(x) = x(x+2) の規則一致と一意性を検証"""
    table = {1: 3, 2: 8, 3: 15, 4: 24, 5: 35}

    # 候補関数群を網羅的に試し、表に完全一致する一次・二次関数を列挙
    valid_rules = []
    for a in range(-3, 4):
        for b in range(-10, 11):
            for c in range(-10, 11):
                ok = all(a * x * x + b * x + c == y for x, y in table.items())
                if ok:
                    valid_rules.append((a, b, c))

    print(f"問1: 表に一致する二次関数の候補数 = {len(valid_rules)}")
    print(f"     候補: {valid_rules}")
    assert len(valid_rules) == 1, f"規則が一意でない: {valid_rules}"
    a, b, c = valid_rules[0]
    assert (a, b, c) == (1, 2, 0), f"想定外の規則: {(a, b, c)}"

    ans = a * 7 * 7 + b * 7 + c
    print(f"問1: N(7) = {ans}")
    assert ans == 63
    options = [48, 56, 63, 72, 80]
    assert sorted(set(options)) == sorted(options), "選択肢に重複あり"
    assert 63 in options and options.index(63) == 2, "正解位置(3)が正しくない"
    print(f"問1: 選択肢 = {options}, 正解 = (3) {ans}")

    # 罠選択肢の根拠検証
    assert 1 * 6 * 6 + 2 * 6 == 48, "(1)はN(6)"
    assert 7 * 7 + 7 == 56, "(2)はx²+x"
    assert 8 * 9 == 72, "(4)は(x+1)(x+2)"
    assert 1 * 8 * 8 + 2 * 8 == 80, "(5)はN(8)"
    return ans


def verify_q2():
    """問2: P(x)=2x²-1, Q(x)=3x+1 の一意性とS(6)を検証"""
    P_table = {1: 1, 2: 7, 4: 31, 5: 49}  # P(3) は (イ) で未知
    Q_table = {1: 4, 3: 10, 4: 13}  # Q(2)=(ア), Q(5)=(ウ) は未知

    # P: 二次関数を網羅
    p_rules = []
    for a in range(-3, 4):
        for b in range(-10, 11):
            for c in range(-10, 11):
                if all(a * x * x + b * x + c == y for x, y in P_table.items()):
                    p_rules.append((a, b, c))
    print(f"問2: Pの候補 = {p_rules}")
    assert len(p_rules) == 1, f"Pの規則が一意でない: {p_rules}"
    pa, pb, pc = p_rules[0]
    assert (pa, pb, pc) == (2, 0, -1), f"想定外のP: {(pa, pb, pc)}"

    # Q: 一次関数を網羅
    q_rules = []
    for a in range(-5, 6):
        for b in range(-10, 11):
            if all(a * x + b == y for x, y in Q_table.items()):
                q_rules.append((a, b))
    print(f"問2: Qの候補 = {q_rules}")
    assert len(q_rules) == 1, f"Qの規則が一意でない: {q_rules}"
    qa, qb = q_rules[0]
    assert (qa, qb) == (3, 1), f"想定外のQ: {(qa, qb)}"

    # 未知値検算
    a_val = qa * 2 + qb  # (ア) = Q(2)
    i_val = pa * 3 * 3 + pb * 3 + pc  # (イ) = P(3)
    u_val = qa * 5 + qb  # (ウ) = Q(5)
    assert a_val == 7, f"(ア)={a_val}"
    assert i_val == 17, f"(イ)={i_val}"
    assert u_val == 16, f"(ウ)={u_val}"
    print(f"問2: (ア)=Q(2)={a_val}, (イ)=P(3)={i_val}, (ウ)=Q(5)={u_val}")

    p6 = pa * 36 + pb * 6 + pc
    q6 = qa * 6 + qb
    s6 = p6 + q6
    print(f"問2: P(6)={p6}, Q(6)={q6}, S(6)={s6}")
    assert p6 == 71 and q6 == 19 and s6 == 90

    options = [65, 90, 71, 78, 91]
    assert len(set(options)) == 5, "選択肢重複あり"
    assert options.index(90) == 1, "正解位置(2)が正しくない"
    print(f"問2: 選択肢 = {options}, 正解 = (2) {s6}")

    # 罠選択肢の根拠検証
    p5 = pa * 25 + pb * 5 + pc
    q5 = qa * 5 + qb
    assert p5 + q5 == 65, "(1)はS(5)=49+16=65"
    assert p6 == 71, "(3)はP(6)のみ"
    assert p6 + a_val == 78, "(4)はP(6)+(ア)=71+7=78"
    # (5)91: P(x)=2x²+1と誤読 → 2(36)+1 + 3(6)+1 = 73+19 = 92...
    # 別解釈: 2x²+3x+1 = 72+18+1 = 91 (P,Qを一括式 S(x)=2x²+3x+1 と誤読)
    assert 2 * 36 + 3 * 6 + 1 == 91, "(5)はS(x)=2x²+3x+1と誤導出した値"
    return s6


if __name__ == "__main__":
    print("=" * 50)
    print("航大思考178 検証")
    print("=" * 50)
    a1 = verify_q1()
    print()
    a2 = verify_q2()
    print()
    print("=" * 50)
    print(f"問1正解: 63 (3)  /  問2正解: 90 (2)")
    print("両問とも解は一意。検証完了。")
    print("=" * 50)
