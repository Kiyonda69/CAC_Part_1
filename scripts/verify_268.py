#!/usr/bin/env python3
"""航大思考268 サイコロの転がし問題の検証
状態: (top, north, east)。対面の和は7。
bottom=7-top, south=7-north, west=7-east
"""

def roll(state, d):
    top, north, east = state
    if d == 'E':   # 東へ転がす: west→top, top→east
        return (7 - east, north, top)
    if d == 'W':   # 西へ転がす: east→top, top→west
        return (east, north, 7 - top)
    if d == 'S':   # 南（手前）へ転がす: north→top, top→south
        return (north, 7 - top, east)
    if d == 'N':   # 北（奥）へ転がす: south→top, top→north
        return (7 - north, top, east)
    raise ValueError(d)


def simulate(start, moves):
    """各マス（開始マス含む）での状態列を返す"""
    states = [start]
    s = start
    for m in moves:
        s = roll(s, m)
        states.append(s)
    return states


def verify_q1():
    # 上面1・手前(南)2・右(東)3 → north=5
    start = (1, 5, 3)
    moves = ['E', 'E', 'S', 'S']
    states = simulate(start, moves)
    tops = [s[0] for s in states]
    print(f"問1 各マスの上面: {tops}")
    final_top = states[-1][0]
    print(f"問1 最終上面 = {final_top}")
    assert final_top == 1, "問1: 想定解(1)と不一致"
    # 罠の確認: 途中の上面（4,6,5）が選択肢2〜5に含まれること
    assert set(tops[1:-1]) == {4, 6, 5}
    return final_top


def verify_q2():
    # 同じ初期状態で6回転がす（7マス）
    start = (1, 5, 3)
    moves = ['E', 'S', 'E', 'E', 'N', 'E']
    states = simulate(start, moves)
    bottoms = [7 - s[0] for s in states]
    tops = [s[0] for s in states]
    print(f"問2 各マスの上面: {tops}")
    print(f"問2 各マスの底面: {bottoms}")
    total = sum(bottoms)
    print(f"問2 底面の合計 = {total}")
    # 誤答パターン
    wrong_no_start = total - bottoms[0]   # 開始マスを除外した誤り
    wrong_tops = sum(tops)                # 上面を合計した誤り
    print(f"  誤答(開始マス除外): {wrong_no_start}")
    print(f"  誤答(上面合計): {wrong_tops}")
    assert total != wrong_no_start and total != wrong_tops
    return total, wrong_no_start, wrong_tops


if __name__ == '__main__':
    t1 = verify_q1()
    t2, w1, w2 = verify_q2()
    print("\n=== 検証結果 ===")
    print(f"問1 正解: 上面 = {t1} → 選択肢(1)")
    print(f"問2 正解: 合計 = {t2}")
