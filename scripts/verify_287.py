#!/usr/bin/env python3
"""航大思考287 検証スクリプト

3次元市松模様（白黒交互）積み上げ問題の検証。
規則: 1辺1cmの白黒立方体を、面で接する立方体どうしが必ず異なる色に
なるように積み、1辺n cmの立方体（第n番目）を作る。かど（頂点）の
8個はすべて黒とする。

問1: 第7番目（7x7x7）に使われている黒い立方体の個数
問2: 第7番目から表面に面が出ている立方体をすべて取り除いた残り
      （内部5x5x5）に含まれる白い立方体の個数
"""


def color(x, y, z):
    """(1,1,1)を黒とする市松模様。黒=True"""
    return (x + y + z) % 2 == 1  # (1,1,1) -> 3 odd -> 黒


def count_black(n):
    return sum(
        1
        for x in range(1, n + 1)
        for y in range(1, n + 1)
        for z in range(1, n + 1)
        if color(x, y, z)
    )


def count_hidden_white(n):
    """表面に面が出ていない（内部の）白い立方体"""
    return sum(
        1
        for x in range(2, n)
        for y in range(2, n)
        for z in range(2, n)
        if not color(x, y, z)
    )


def verify():
    # 市松模様の整合性: 面で接する立方体は必ず異色（定義上自明だが確認）
    n = 7
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            for z in range(1, n + 1):
                for dx, dy, dz in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if nx <= n and ny <= n and nz <= n:
                        assert color(x, y, z) != color(nx, ny, nz)
    # かど8個がすべて黒
    for x in (1, n):
        for y in (1, n):
            for z in (1, n):
                assert color(x, y, z), "かどが黒でない"

    # 規則性の確認（第1〜3番目）
    assert count_black(1) == 1
    assert count_black(2) == 4
    assert count_black(3) == 14

    # 問1: 第7番目の黒の個数
    q1 = count_black(7)
    assert q1 == 172, f"問1: {q1}"
    # 層ごとの検算: 奇数段(4段)は25個、偶数段(3段)は24個
    assert 4 * 25 + 3 * 24 == 172

    # 問2: 内部5x5x5に含まれる白の個数（内部のかどは白になる）
    q2 = count_hidden_white(7)
    assert q2 == 63, f"問2: {q2}"
    # 内部のかど(2,2,2)は白であることの確認（ひっかけ62の根拠）
    assert not color(2, 2, 2)
    # 層ごとの検算: 内部の5層のうち白13の層が3層、白12の層が2層
    assert 3 * 13 + 2 * 12 == 63

    # 解の一意性: 選択肢の中で正解は1つのみ（数値問題のため自明だが確認）
    q1_choices = [164, 168, 171, 172, 175]  # 正解(4)=172
    q2_choices = [54, 58, 60, 62, 63]  # 正解(5)=63
    assert q1_choices.count(q1) == 1
    assert q2_choices.count(q2) == 1
    assert q1_choices == sorted(q1_choices) and q2_choices == sorted(q2_choices)

    print(f"問1（第7番目の黒の個数）: {q1} -> 正解(4)")
    print(f"問2（内部に残る白の個数）: {q2} -> 正解(5)")
    print("検証OK: 解は一意")


if __name__ == "__main__":
    verify()
