"""航大思考214 検証コード: ペンキ塗り分け問題"""

def verify_q1():
    """問1: 3x4x5直方体を全面塗装、1cm角に切断。塗装面数別に集計"""
    X, Y, Z = 3, 4, 5
    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for x in range(1, X + 1):
        for y in range(1, Y + 1):
            for z in range(1, Z + 1):
                faces = 0
                faces += (x == 1) + (x == X)
                faces += (y == 1) + (y == Y)
                faces += (z == 1) + (z == Z)
                counts[faces] += 1
    assert sum(counts.values()) == X * Y * Z == 60
    print("問1 (3x4x5 全面塗装):", counts)
    assert counts[2] == 24, counts
    return counts[2]

def verify_q2():
    """問2: 5x5x5立方体を底面(z=1の下面)以外の5面塗装、125個に切断"""
    N = 5
    counts = {k: 0 for k in range(6)}
    for x in range(1, N + 1):
        for y in range(1, N + 1):
            for z in range(1, N + 1):
                faces = 0
                faces += (x == 1) + (x == N)
                faces += (y == 1) + (y == N)
                faces += (z == N)  # 上面のみ塗装、底面(z=1)は塗らない
                counts[faces] += 1
    assert sum(counts.values()) == N ** 3 == 125
    print("問2 (5x5x5 底面以外塗装):", counts)
    assert counts[1] == 57, counts
    # 罠の検証: 全面塗装なら1面=54
    full = sum(1 for x in range(1, 6) for y in range(1, 6) for z in range(1, 6)
               if ((x == 1) + (x == 5) + (y == 1) + (y == 5) + (z == 1) + (z == 5)) == 1)
    print("罠（全面塗装と誤読した場合の1面の個数）:", full)
    return counts[1]

if __name__ == "__main__":
    a1 = verify_q1()
    a2 = verify_q2()
    print(f"問1の答え: {a1}個 / 問2の答え: {a2}個")
