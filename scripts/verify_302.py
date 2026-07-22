#!/usr/bin/env python3
"""航大思考302 検証スクリプト

問題: 球を正三角錐（三角錐）状に積み上げる規則性
- 第n番目の立体: 上から第m段目（m=1..n）が1辺m個の正三角形状（球の数はT(m)=m(m+1)/2個）
- 問1: 第6番目の立体に使われる球の総数
- 問2: 第12番目の立体で、4つの面（底面と3つの斜面）のいずれにも
       現れない「内部の球」の個数

球の位置は (L, a, b) で表す:
- L: 段番号（0=最上段, n-1=最下段）
- 段L内の球: a>=0, b>=0, a+b<=L
- 3つの斜面: a=0 の球全体 / b=0 の球全体 / a+b=L の球全体
- 底面: L=n-1 の球全体
"""


def build_solid(n):
    """第n番目の立体の球の位置集合を総当たりで生成"""
    balls = []
    for L in range(n):
        for a in range(L + 1):
            for b in range(L + 1 - a):
                balls.append((L, a, b))
    return balls


def count_total(n):
    """問1: 球の総数（総当たり）"""
    return len(build_solid(n))


def count_inner(n):
    """問2: 4つの面のいずれにも現れない球の個数（総当たり）"""
    inner = 0
    for (L, a, b) in build_solid(n):
        on_face = (
            L == n - 1        # 底面
            or a == 0         # 斜面1
            or b == 0         # 斜面2
            or a + b == L     # 斜面3
        )
        if not on_face:
            inner += 1
    return inner


def verify_q1():
    """問1の検証: 第6番目の球の総数"""
    # 数列の確認: 1, 4, 10, 20, 35, 56（三角錐数）
    seq = [count_total(n) for n in range(1, 7)]
    assert seq == [1, 4, 10, 20, 35, 56], f"数列が想定と不一致: {seq}"

    answer = count_total(6)
    # 公式 n(n+1)(n+2)/6 とも一致することを確認
    assert answer == 6 * 7 * 8 // 6 == 56

    # 選択肢の中で正解が唯一であることを確認
    choices = [56, 66, 84, 91, 120]  # 正解は(1)
    valid = [c for c in choices if c == answer]
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    print(f"問1 OK: 第6番目の球の総数 = {answer}（数列: {seq}）")
    return answer


def verify_q2():
    """問2の検証: 第12番目の内部の球の個数"""
    # 内部の球の数列（第n番目）: n=4まで0, n=5で初めて1個
    inner_seq = [count_inner(n) for n in range(1, 13)]
    assert inner_seq[:5] == [0, 0, 0, 0, 1], f"序盤が想定と不一致: {inner_seq}"

    answer = count_inner(12)
    # 内部の球は第(n-4)番目の三角錐数 C(n-2,3) と一致することを確認
    from math import comb
    for n in range(2, 13):
        assert count_inner(n) == comb(n - 2, 3), f"n={n}で公式と不一致"
    assert answer == comb(10, 3) == 120

    # 段ごとの内訳（上から第m段: T(m-3)個, 最下段は0個）でも確認
    layer_sum = sum((m - 3) * (m - 2) // 2 for m in range(4, 12))
    assert layer_sum == answer, f"段ごとの合計 {layer_sum} != {answer}"

    # 選択肢の中で正解が唯一であることを確認
    choices = [56, 84, 120, 165, 220]  # 正解は(3)
    valid = [c for c in choices if c == answer]
    assert len(valid) == 1, f"解が{len(valid)}個存在"
    print(f"問2 OK: 第12番目の内部の球 = {answer}（数列: {inner_seq}）")
    return answer


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("すべての検証に合格しました。")
