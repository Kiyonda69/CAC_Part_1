#!/usr/bin/env python3
"""航大思考285: 階段ピラミッド状立体の規則性（個数・表面積）の検証

立体の定義（第n番目）:
  1辺1cmの立方体を積む。高さz段目(z=0が最下段, 0<=z<n)は
  x,y in [0, n-z) の正方形状に (n-z)^2 個。
  → 最下段 n×n、その上 (n-1)×(n-1)…最上段 1×1 の角揃え階段ピラミッド。

問1: 第6番目に必要な立方体の総数 → 91個（平方数の和）
問2: 表面積（底面を含む）が初めて400cm^2を超える番号 → 第10番目
"""


def cubes(n):
    """第n番目の立体のボクセル集合"""
    s = set()
    for z in range(n):
        k = n - z
        for x in range(k):
            for y in range(k):
                s.add((x, y, z))
    return s


def count(n):
    return len(cubes(n))


def surface(n):
    """露出面の総数（底面含む）をボクセル総当たりで数える"""
    s = cubes(n)
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    area = 0
    for (x, y, z) in s:
        for (dx, dy, dz) in dirs:
            if (x + dx, y + dy, z + dz) not in s:
                area += 1
    return area


def verify():
    # --- 個数の規則: 平方数の和 n(n+1)(2n+1)/6 ---
    for n in range(1, 13):
        assert count(n) == n * (n + 1) * (2 * n + 1) // 6, f"count({n})"
    seq = [count(n) for n in range(1, 7)]
    assert seq == [1, 5, 14, 30, 55, 91], seq
    print(f"個数列(第1〜6): {seq} → 問1の正解: 第6番目 = {seq[5]}個")

    # 問1の誤答が正解と一致しないこと
    q1_answer = 91
    q1_traps = {55: "第5番目で止める", 90: "最初の1個を落とす",
                100: "差を+10の等差と誤る(55+45等の誤算)", 140: "第7番目まで足す"}
    for v in q1_traps:
        assert v != q1_answer
    assert count(5) == 55 and count(7) == 140

    # --- 表面積の規則: S(n) = 4n^2 + 2n（底面含む） ---
    for n in range(1, 13):
        assert surface(n) == 4 * n * n + 2 * n, f"surface({n})={surface(n)}"
    ss = [surface(n) for n in range(1, 13)]
    print(f"表面積列(第1〜12): {ss}")
    # 階差が 14,22,30,… の+8等差（2階差一定）であること
    d1 = [ss[i + 1] - ss[i] for i in range(len(ss) - 1)]
    d2 = [d1[i + 1] - d1[i] for i in range(len(d1) - 1)]
    assert all(d == 8 for d in d2), d2

    # 問2: 400cm^2を初めて超える番号の一意性
    over = [n for n in range(1, 13) if surface(n) > 400]
    assert over and over[0] == 10, over
    assert surface(9) == 342 < 400 and surface(10) == 420 > 400
    print(f"問2の正解: S(9)=342 ≦ 400 < S(10)=420 → 第10番目")

    # 問2の誤答根拠の検証
    # 罠A: 立方体扱い 6n^2 > 400 → 第9番目（n=8:384, n=9:486）
    trapA = [n for n in range(1, 13) if 6 * n * n > 400][0]
    assert trapA == 9
    # 罠B: 底面を数え忘れ 3n^2+2n > 400 → 第12番目（n=11:385, n=12:456）
    trapB = [n for n in range(1, 13) if 3 * n * n + 2 * n > 400][0]
    assert trapB == 12
    print(f"罠の検証: 6n^2扱い→第{trapA}番目 / 底面忘れ3n^2+2n→第{trapB}番目")

    print("\nすべての検証に合格（問1=91個 / 問2=第10番目・唯一）")


if __name__ == "__main__":
    verify()
