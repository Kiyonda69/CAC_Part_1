#!/usr/bin/env python3
"""
航大思考273 検証スクリプト
図形の系列（3×3方眼の外周を移動する2記号）の規則性問題

外周8マスの位置番号（時計回り）:
  pos0=(左上) pos1=(上中) pos2=(右上)
  pos7=(左中)   中央     pos3=(右中)
  pos6=(左下) pos5=(下中) pos4=(右下)

規則:
- ■(黒マス): 1番目は pos0。n番目→n+1番目で時計回りに n マス移動
  （移動量が1,2,3,...と増える）→ 位置 = T(n-1) mod 8（T=三角数）
- ○(白丸): 1番目は pos5。毎回反時計回りに2マス移動
  → 位置 = (5 - 2(n-1)) mod 8
"""

POS_NAMES = ["左上", "上中", "右上", "右中", "右下", "下中", "左下", "左中"]
# 3×3グリッドの (row, col) 対応
POS_RC = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]


def black_pos(n):
    """n番目(1始まり)の■の位置"""
    t = (n - 1) * n // 2  # 累積移動量 1+2+...+(n-1)
    return t % 8


def circle_pos(n):
    """n番目(1始まり)の○の位置"""
    return (5 - 2 * (n - 1)) % 8


def verify_q1():
    """問1: 図1〜4を提示し5番目を選ばせる。系列の整合性と選択肢の一意性を確認"""
    print("=== 問1 検証 ===")
    for n in range(1, 6):
        b, c = black_pos(n), circle_pos(n)
        assert b != c, f"図{n}で■と○が重なる（pos{b}）"
        print(f"図{n}: ■=pos{b}({POS_NAMES[b]}), ○=pos{c}({POS_NAMES[c]})")

    correct = (black_pos(5), circle_pos(5))
    assert correct == (2, 5), f"問1正解が想定と異なる: {correct}"

    # 選択肢（(■pos, ○pos)）: 正解 + 典型的誤答4種
    options = {
        "正解: ■+4マス累積, ○反時計2": (2, 5),
        "誤答A: ■を+3固定と誤解": ((6 + 3) % 8, 5),          # (1,5)
        "誤答B: ○を時計回り2と誤解": (2, (7 + 2) % 8),        # (2,1)
        "誤答C: ○を反時計1と誤解": (2, (7 - 1) % 8),          # (2,6)
        "誤答D: ■を+5と誤計算": ((6 + 5) % 8, 5),             # (3,5)
    }
    vals = list(options.values())
    assert len(set(vals)) == 5, "問1選択肢に重複あり"
    for k, v in options.items():
        print(f"  {k}: ■=pos{v[0]}, ○=pos{v[1]}")
    print("問1 OK: 系列整合・選択肢5種すべて相異なる・正解は■右上/○下中\n")


def verify_q2():
    """問2: ■と○が初めて同じマスに重なるのは何番目か（唯一解の確認）"""
    print("=== 問2 検証 ===")
    first = None
    for n in range(1, 100):
        if black_pos(n) == circle_pos(n):
            first = n
            break
    assert first is not None, "重なりが発生しない"
    print(f"初めて重なるのは 図{first}（pos{black_pos(first)}={POS_NAMES[black_pos(first)]}）")
    # 14番目より前に重なりがないことを総当たりで確認
    for n in range(1, first):
        assert black_pos(n) != circle_pos(n), f"図{n}で先に重なっている"
    assert first == 14, f"想定(14)と異なる: {first}"

    # 参考: 以後の重なり
    laters = [n for n in range(1, 50) if black_pos(n) == circle_pos(n)]
    print(f"重なる番号一覧(〜49): {laters}")
    print("問2 OK: 初回の重なりは14番目で唯一\n")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証 PASS")
