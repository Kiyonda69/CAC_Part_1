#!/usr/bin/env python3
"""航大思考281 検証スクリプト
サイコロの貼り合わせ（接する面の目の和）問題

問1: 対面の和7のサイコロ4個を左右一列に貼り合わせる。
     接する面の目の和はすべて6。左端のサイコロの左側面が5のとき、
     右端のサイコロの右側面の目を求める。

問2: 同じサイコロ4個を机の上に一列にすき間なく並べるとき、
     外から見えない面（接する面6面＋机に接する面4面）の目の和の最小値。
"""
from itertools import product

# サイコロの状態: (top, north, east) で表現。対面の和は7。
# bottom=7-top, south=7-north, west=7-east
# 標準サイコロ（右手系: 1上・2南・3東）の24回転を生成する。

def rotations(state):
    """(top, north, east) から到達可能な24姿勢を生成"""
    def roll_e(s):  # 東へ転がす
        t, n, e = s
        return (7 - e, n, t)
    def roll_n(s):  # 北へ転がす
        t, n, e = s
        return (n, 7 - t, e)
    def spin(s):    # 上下軸まわり時計回り(上から見て)
        t, n, e = s
        return (t, e, 7 - n)
    seen = set()
    stack = [state]
    while stack:
        s = stack.pop()
        if s in seen:
            continue
        seen.add(s)
        stack.extend([roll_e(s), roll_n(s), spin(s)])
    return sorted(seen)

ORIENTS = rotations((1, 2, 3))
assert len(ORIENTS) == 24, f"回転数が{len(ORIENTS)}"


def faces(state):
    """(top, north, east) → 全6面 dict"""
    t, n, e = state
    return {"top": t, "bottom": 7 - t, "north": n,
            "south": 7 - n, "east": e, "west": 7 - e}


def verify_q1():
    """問1: 接面和6・左端の左側面=5 → 右端の右側面は一意に5か"""
    results = set()
    count = 0
    # 東西一列: die1(西端)〜die4(東端)。接面 = die_i東面 + die_{i+1}西面
    for combo in product(ORIENTS, repeat=4):
        fs = [faces(s) for s in combo]
        if fs[0]["west"] != 5:
            continue
        if any(fs[i]["east"] + fs[i + 1]["west"] != 6 for i in range(3)):
            continue
        results.add(fs[3]["east"])
        count += 1
    assert results == {5}, f"問1の解が一意でない: {results}"
    print(f"問1 OK: 右端の右側面 = 5（成立配置 {count} 通り、答えは全て一致）")
    # 中間チェーンの確認（解説用）
    for combo in product(ORIENTS, repeat=4):
        fs = [faces(s) for s in combo]
        if fs[0]["west"] == 5 and all(
                fs[i]["east"] + fs[i + 1]["west"] == 6 for i in range(3)):
            chain = [(fs[i]["east"], fs[i + 1]["west"]) for i in range(3)]
            print(f"  チェーン例: 東面/西面ペア = {chain}, "
                  f"各サイコロ東面 = {[f['east'] for f in fs]}")
            break


def verify_q2():
    """問2: 見えない面（接面6+底面4）の目の和の最小値 = 22 か"""
    best = 99
    worst = 0
    for combo in product(ORIENTS, repeat=4):
        fs = [faces(s) for s in combo]
        hidden = sum(f["bottom"] for f in fs)
        hidden += sum(fs[i]["east"] + fs[i + 1]["west"] for i in range(3))
        best = min(best, hidden)
        worst = max(worst, hidden)
    assert best == 22, f"最小値が22でない: {best}"
    print(f"問2 OK: 見えない面の和の最小値 = {best}（最大値 = {worst}）")
    # 内訳の理論値確認: 中間2個は東西面が対面ペアで和7+底面最小1=8、
    # 両端は接面1+底面2(隣接面)=3 → 3+8+8+3=22
    print("  理論値: 端3 + 中8 + 中8 + 端3 = 22")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証 OK")
