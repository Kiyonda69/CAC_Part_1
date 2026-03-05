#!/usr/bin/env python3
"""
航大思考35 検証スクリプト

問1: パターン認識（XOR隣接セル規則）
  - 7セルの行が規則に従って変化する
  - 規則: next[i] = row[i] XOR row[(i+1) % 7]
  - 正解: (3)

問2: 空間推論（立方体の辺の中点が作る三角形）
  - 1辺2の立方体ABCD-EFGHの辺AB, FG, DHの中点P, Q, R
  - 三角形PQRの面積を求める
  - 正解: (1)
"""

import math

# ============================================================
# 問1: パターン認識 - XOR隣接セル規則
# ============================================================

def apply_xor_rule(row):
    """XOR規則を適用: next[i] = row[i] XOR row[(i+1) % 7]"""
    n = len(row)
    return [row[i] ^ row[(i + 1) % n] for i in range(n)]


def verify_sequence(rows):
    """4行の列が全てXOR規則に従うか検証"""
    for i in range(len(rows) - 1):
        expected = apply_xor_rule(rows[i])
        if expected != rows[i + 1]:
            return False
    return True


def verify_q1():
    """問1の検証"""
    print("=" * 60)
    print("問1: パターン認識（XOR隣接セル規則）")
    print("=" * 60)

    # 規則: next[i] = row[i] XOR row[(i+1) % 7]
    # 例題パターン（規則を示す）
    example_row1 = [1, 1, 0, 1, 0, 0, 1]

    print("\n【例題パターン（規則を示す）】")
    rows = [example_row1]
    for i in range(3):
        rows.append(apply_xor_rule(rows[-1]))

    for i, row in enumerate(rows):
        bw = ''.join(['B' if x else 'W' for x in row])
        print(f"  行{i+1}: {row} = {bw}")

    # 正解選択肢を(3)に配置するため、5つの選択肢を作成
    # 各選択肢は異なる開始行から始まる4行のパターン

    # 正解パターン（選択肢3）: XOR規則に正しく従う
    correct_start = [0, 1, 0, 1, 1, 0, 1]
    correct_rows = [correct_start]
    for i in range(3):
        correct_rows.append(apply_xor_rule(correct_rows[-1]))

    # 不正解パターン生成
    # 不正解1: XOR with LEFT neighbor (different rule)
    def apply_wrong_rule1(row):
        n = len(row)
        return [row[i] ^ row[(i - 1) % n] for i in range(n)]

    wrong1_start = [1, 0, 1, 0, 0, 1, 1]
    wrong1_rows = [wrong1_start]
    for i in range(3):
        wrong1_rows.append(apply_wrong_rule1(wrong1_rows[-1]))

    # 不正解2: AND with right neighbor
    def apply_wrong_rule2(row):
        n = len(row)
        return [row[i] & row[(i + 1) % n] for i in range(n)]

    wrong2_start = [1, 1, 0, 1, 1, 0, 1]
    wrong2_rows = [wrong2_start]
    for i in range(3):
        wrong2_rows.append(apply_wrong_rule2(wrong2_rows[-1]))

    # 不正解3: XOR右隣 + 全体反転
    def apply_wrong_rule3(row):
        n = len(row)
        xor_result = [row[i] ^ row[(i + 1) % n] for i in range(n)]
        return [1 - x for x in xor_result]

    wrong3_start = [1, 0, 0, 1, 0, 1, 0]
    wrong3_rows = [wrong3_start]
    for i in range(3):
        wrong3_rows.append(apply_wrong_rule3(wrong3_rows[-1]))

    # 不正解4: 正しいXOR規則だが行2→行3で1ビットエラー
    wrong4_start = [0, 0, 1, 1, 0, 1, 0]
    wrong4_rows = [wrong4_start]
    wrong4_rows.append(apply_xor_rule(wrong4_rows[-1]))  # 行1→行2: 正しい
    # 行2→行3: 1ビットエラーを挿入
    correct_row3 = apply_xor_rule(wrong4_rows[-1])
    error_row3 = correct_row3.copy()
    error_row3[3] = 1 - error_row3[3]  # 4番目のビットを反転
    wrong4_rows.append(error_row3)
    # 行3→行4: エラーのある行3からXOR規則を適用（正しくない連鎖）
    wrong4_rows.append(apply_xor_rule(wrong4_rows[-1]))

    # 選択肢の配置（正解は(3)）
    options = [wrong1_rows, wrong2_rows, correct_rows, wrong3_rows, wrong4_rows]

    print("\n【選択肢】")
    for idx, opt in enumerate(options):
        label = "正解" if idx == 2 else "不正解"
        follows = verify_sequence(opt)
        print(f"\n  選択肢({idx+1}) [{label}]:")
        for i, row in enumerate(opt):
            bw = ''.join(['B' if x else 'W' for x in row])
            print(f"    行{i+1}: {row} = {bw}")
        print(f"    XOR規則に従う: {follows}")

    # 検証: 正解のみがXOR規則に従うことを確認
    results = [verify_sequence(opt) for opt in options]
    print(f"\n【検証結果】")
    print(f"  XOR規則に従う選択肢: {[i+1 for i, r in enumerate(results) if r]}")
    assert results == [False, False, True, False, False], \
        f"検証失敗: 正解以外がXOR規則に従っている: {results}"
    print("  → 正解は(3)のみ: OK")

    return options


# ============================================================
# 問2: 空間推論 - 立方体の辺の中点が作る三角形
# ============================================================

def verify_q2():
    """問2の検証"""
    print("\n" + "=" * 60)
    print("問2: 空間推論（立方体の辺の中点が作る三角形）")
    print("=" * 60)

    # 1辺2の立方体 ABCD-EFGH
    # ABCD: 上面, EFGH: 底面
    a = 2
    A = (0, 0, a)
    B = (a, 0, a)
    C = (a, a, a)
    D = (0, a, a)
    E = (0, 0, 0)
    F = (a, 0, 0)
    G = (a, a, 0)
    H = (0, a, 0)

    print(f"\n立方体の頂点座標 (1辺 = {a}):")
    for name, coord in [('A', A), ('B', B), ('C', C), ('D', D),
                         ('E', E), ('F', F), ('G', G), ('H', H)]:
        print(f"  {name} = {coord}")

    # 中点
    P = tuple((A[i] + B[i]) / 2 for i in range(3))  # AB中点
    Q = tuple((F[i] + G[i]) / 2 for i in range(3))  # FG中点
    R = tuple((D[i] + H[i]) / 2 for i in range(3))  # DH中点

    print(f"\n中点:")
    print(f"  P (AB中点) = {P}")
    print(f"  Q (FG中点) = {Q}")
    print(f"  R (DH中点) = {R}")

    # 辺の長さ
    def dist(p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

    PQ = dist(P, Q)
    QR = dist(Q, R)
    RP = dist(R, P)

    print(f"\n辺の長さ:")
    print(f"  PQ = {PQ:.6f} = sqrt({PQ**2:.1f}) = sqrt(6)")
    print(f"  QR = {QR:.6f} = sqrt({QR**2:.1f}) = sqrt(6)")
    print(f"  RP = {RP:.6f} = sqrt({RP**2:.1f}) = sqrt(6)")

    # 正三角形であることを確認
    assert abs(PQ - QR) < 1e-10, f"PQ != QR: {PQ} != {QR}"
    assert abs(QR - RP) < 1e-10, f"QR != RP: {QR} != {RP}"
    print(f"\n  → 三角形PQRは正三角形 (1辺 = sqrt(6))")

    # 面積 = (sqrt(3)/4) * side^2
    side_sq = PQ ** 2  # = 6
    area = (math.sqrt(3) / 4) * side_sq
    print(f"\n面積:")
    print(f"  = (sqrt(3)/4) * {side_sq:.1f}")
    print(f"  = {area:.6f}")
    print(f"  = 3*sqrt(3)/2")
    print(f"  = {3 * math.sqrt(3) / 2:.6f}")

    # 検証
    expected = 3 * math.sqrt(3) / 2
    assert abs(area - expected) < 1e-10, f"面積不一致: {area} != {expected}"

    # 外積による検証
    vec_PQ = tuple(Q[i] - P[i] for i in range(3))
    vec_PR = tuple(R[i] - P[i] for i in range(3))
    cross = (
        vec_PQ[1] * vec_PR[2] - vec_PQ[2] * vec_PR[1],
        vec_PQ[2] * vec_PR[0] - vec_PQ[0] * vec_PR[2],
        vec_PQ[0] * vec_PR[1] - vec_PQ[1] * vec_PR[0]
    )
    cross_mag = math.sqrt(sum(c ** 2 for c in cross))
    area_cross = cross_mag / 2

    print(f"\n外積による検証:")
    print(f"  PQ = {vec_PQ}")
    print(f"  PR = {vec_PR}")
    print(f"  PQ x PR = {cross}")
    print(f"  |PQ x PR| / 2 = {area_cross:.6f}")
    assert abs(area_cross - expected) < 1e-10

    print(f"\n  → 面積 = 3√3/2 : OK")

    # 選択肢（正解は(1)）
    options = [
        ("3√3/2", expected),
        ("3", 3.0),
        ("2√3", 2 * math.sqrt(3)),
        ("√6", math.sqrt(6)),
        ("3√2", 3 * math.sqrt(2)),
    ]

    print(f"\n【選択肢】")
    for i, (label, value) in enumerate(options):
        mark = " ← 正解" if i == 0 else ""
        print(f"  ({i+1}) {label} = {value:.6f}{mark}")

    return expected


# ============================================================
# メイン
# ============================================================

if __name__ == "__main__":
    options_q1 = verify_q1()
    area_q2 = verify_q2()

    print("\n" + "=" * 60)
    print("最終結果")
    print("=" * 60)
    print("  問1 正解: (3)")
    print(f"  問2 正解: (1) 3√3/2 ≈ {area_q2:.4f}")
    print("  検証: すべてOK")
