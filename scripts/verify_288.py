#!/usr/bin/env python3
"""航大思考288: ペンキ塗り立方体（塗られた面の数の分類）の検証

第n番目の立体 = 1辺1cmの小立方体を積んだ1辺n cmの立方体。
表面全体（底面含む）にペンキを塗り、ばらしたときの
「ちょうどk面塗られた小立方体」の個数をボクセル総当たりで数える。

問1: 第7番目の「ちょうど2面塗られた」個数 → 60
問2: 「1面だけ塗られた」＝「0面塗られた」(いずれも1個以上)となる番目は
     第8番目のみで、そのときの「2面塗られた」個数 → 72
"""


def count_by_painted_faces(n):
    """1辺nの立方体の小立方体を、塗られた面の数ごとに数える"""
    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for x in range(n):
        for y in range(n):
            for z in range(n):
                faces = 0
                for c in (x, y, z):
                    if c == 0:
                        faces += 1
                    if c == n - 1:
                        faces += 1
                counts[faces] += 1
    return counts


def verify():
    # 公式との一致確認: 3面=8, 2面=12(n-2), 1面=6(n-2)^2, 0面=(n-2)^3
    for n in range(2, 13):
        c = count_by_painted_faces(n)
        k = n - 2
        assert sum(c.values()) == n ** 3
        assert c[3] == 8, f"n={n}: 3面={c[3]}"
        assert c[2] == 12 * k, f"n={n}: 2面={c[2]}"
        assert c[1] == 6 * k * k, f"n={n}: 1面={c[1]}"
        assert c[0] == k ** 3, f"n={n}: 0面={c[0]}"

    # 問1: 第7番目の2面塗り
    c7 = count_by_painted_faces(7)
    assert c7[2] == 60, f"問1の正解が60でない: {c7[2]}"
    # 図に示す第2〜4番目の数列（0, 12, 24: 公差12）
    seq = [count_by_painted_faces(n)[2] for n in range(2, 5)]
    assert seq == [0, 12, 24], seq
    # 問1の罠が正解と一致しないこと
    assert c7[2] not in (72, 84, 125, 150)
    assert c7[1] == 150       # 罠(5): 1面塗りとの混同
    assert c7[0] == 125       # 罠(4): 内部(0面塗り)との混同
    assert 12 * 6 == 72       # 罠(2): 各辺で片端だけ除く
    assert 12 * 7 == 84       # 罠(3): かどを除き忘れ

    # 問2: 1面塗り = 0面塗り（いずれも1個以上）となる番目の一意性
    solutions = []
    for n in range(2, 51):
        c = count_by_painted_faces(n)
        if c[1] == c[0] and c[1] >= 1:
            solutions.append(n)
    assert solutions == [8], f"解が一意でない: {solutions}"
    # n=2は両方0個で除外されることの確認
    c2 = count_by_painted_faces(2)
    assert c2[1] == c2[0] == 0

    c8 = count_by_painted_faces(8)
    assert c8[2] == 72, f"問2の正解が72でない: {c8[2]}"
    # 罠の根拠確認
    assert 12 * 4 == 48   # 6n^2=n^3と立式(−2忘れ)→n=6→12(6-2)
    assert 12 * 5 == 60   # 6(n-1)^2=(n-1)^3→n=7→12(7-2)
    assert 12 * 7 == 84   # 辺上の個数をn-1と誤る
    assert 12 * 8 == 96   # nから2を引き忘れ

    print("問1: 第7番目の2面塗り =", c7[2], "(正解(1))")
    print("問2: 第8番目のみ 1面=0面 =", c8[1], "個, 2面塗り =", c8[2], "(正解(3))")
    print("数列(2面塗り, n=2..8):",
          [count_by_painted_faces(n)[2] for n in range(2, 9)])
    print("全検証OK")


if __name__ == "__main__":
    verify()
