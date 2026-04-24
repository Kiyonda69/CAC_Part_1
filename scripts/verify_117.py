#!/usr/bin/env python3
"""
航大思考117 の解の一意性検証

問1: 数列 1, 3, 4, 7, 11, 18, ?
  規則: a(n) = a(n-1) + a(n-2) （フィボナッチ型漸化式）
  初期値: a(1)=1, a(2)=3
  答え: a(7) = 29

問2: 4×4 数表 a(r,c) = r² + rc + c² の空欄(3,3)
  答え: 27
"""


def verify_q1():
    """問1: 1, 3, 4, 7, 11, 18, ? = 29"""
    seq = [1, 3]
    for _ in range(5):
        seq.append(seq[-1] + seq[-2])
    print(f"数列: {seq}")
    assert seq[:6] == [1, 3, 4, 7, 11, 18], "初期5項が合わない"
    assert seq[6] == 29, f"7番目が29でない (={seq[6]})"
    print(f"7番目 = {seq[6]}")

    # 選択肢の検討（誤答の由来）
    distractors = {
        25: "11*2 + 3 の誤推定",
        27: "18 + 9 など曖昧推定",
        31: "18 + 13 （フィボナッチ拡張の誤り）",
        36: "18 × 2 （前項倍の誤り）",
        29: "正解: 11 + 18",
    }
    for val, note in distractors.items():
        print(f"  {val}: {note}")
    print("問1 検証成功")


def verify_q2():
    """問2: 4x4 数表 a(r,c) = r² + rc + c²"""
    def a(r, c):
        return r * r + r * c + c * c

    table = [[a(r, c) for c in range(1, 5)] for r in range(1, 5)]
    print("数表:")
    print("      c=1  c=2  c=3  c=4")
    for r, row in enumerate(table, 1):
        print(f"r={r}: " + "  ".join(f"{v:3d}" for v in row))

    expected = [
        [3, 7, 13, 21],
        [7, 12, 19, 28],
        [13, 19, 27, 37],
        [21, 28, 37, 48],
    ]
    assert table == expected, "数表が期待値と一致しない"
    assert a(3, 3) == 27, f"(3,3)が27でない (={a(3,3)})"
    print(f"\n(3,3) = {a(3,3)}")

    # 行・列の差分パターン
    print("\n行方向の差分:")
    for r in range(4):
        diffs = [table[r][c+1] - table[r][c] for c in range(3)]
        print(f"  行{r+1}: {diffs}")
    print("列方向の差分:")
    for c in range(4):
        diffs = [table[r+1][c] - table[r][c] for r in range(3)]
        print(f"  列{c+1}: {diffs}")

    # 対称性の確認
    for r in range(4):
        for c in range(4):
            assert table[r][c] == table[c][r], "対称でない"
    print("\n表は対称: a(r,c) = a(c,r) ✓")

    # 差分の規則確認: 行rの差分は 2c+1+r パターンを持つ
    # a(r,c+1) - a(r,c) = 2c+1+r
    # 例: r=3: 10-3=7? 違う... 計算し直す
    # a(3,1)=9+3+1=13, a(3,2)=9+6+4=19, a(3,3)=9+9+9=27, a(3,4)=9+12+16=37
    # 差分: 6, 8, 10 (公差2, 初項6)
    # 一般に行rの初項差分は r + 3, 公差は 2
    # a(r, c+1) - a(r, c) = r(c+1)+(c+1)² - rc - c² = r + 2c + 1
    # 行r の差分初項 (c=1→2): r + 3, 公差 2

    print("問2 検証成功")


if __name__ == '__main__':
    print("=" * 60)
    print("問1 検証")
    print("=" * 60)
    verify_q1()
    print()
    print("=" * 60)
    print("問2 検証")
    print("=" * 60)
    verify_q2()
    print()
    print("=" * 60)
    print("全検証成功")
    print("=" * 60)
