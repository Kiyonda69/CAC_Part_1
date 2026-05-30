#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""航大思考194 検証: 資料空欄穴埋め問題の一意性確認"""
from itertools import product


def verify_q1():
    """問1: 製品別・月別生産台数表の空欄ア・イ・ウ"""
    # 行合計
    row_total = {"A": 600, "B": 700, "C": 720}
    # 既知の値（空欄は None）
    A = [120, 150, None, 180]   # 3月=ア
    B = [None, 200, 170, 160]   # 1月=イ
    C = [140, None, 190, 210]   # 2月=ウ
    # 月別合計と総合計
    col_total = [430, 530, 510, 550]
    grand_total = 2020

    # 行合計から空欄を一意に算出
    a = row_total["A"] - sum(v for v in A if v is not None)  # ア
    i = row_total["B"] - sum(v for v in B if v is not None)  # イ
    u = row_total["C"] - sum(v for v in C if v is not None)  # ウ
    assert a == 150, a
    assert i == 170, i
    assert u == 180, u

    A[2], B[0], C[1] = a, i, u
    # 行合計整合
    assert sum(A) == row_total["A"]
    assert sum(B) == row_total["B"]
    assert sum(C) == row_total["C"]
    # 列合計整合
    for c in range(4):
        assert A[c] + B[c] + C[c] == col_total[c], c
    # 総合計整合
    assert sum(col_total) == grand_total
    assert sum(A) + sum(B) + sum(C) == grand_total

    s = a + i + u
    assert s == 500, s
    print("Q1 OK: ア=%d イ=%d ウ=%d 合計=%d" % (a, i, u, s))
    return s


def verify_q2():
    """問2: 部門別・四半期別人件費表の空欄ア〜キ（連鎖計算）"""
    row_total = {"営業": 1400, "製造": 1770, "開発": 1190, "管理": 780}
    col_total = [1090, 1240, 1350, 1460]
    grand_total = 5140

    # 既知 (None=空欄)
    sales = [None, None, 350, 400]      # ア,イ
    mfg = [300, None, None, 510]        # ウ,エ
    dev = [280, 260, None, None]        # オ,カ
    admin = [180, 190, 210, None]       # キ

    # 連鎖計算（この順序でしか解けない）
    ki = row_total["管理"] - 180 - 190 - 210          # 管理部行
    admin[3] = ki
    ka = col_total[3] - 400 - 510 - ki                # Q4列
    dev[3] = ka
    o = row_total["開発"] - 280 - 260 - ka            # 開発部行
    dev[2] = o
    e = col_total[2] - 350 - o - 210                  # Q3列
    mfg[2] = e
    u = row_total["製造"] - 300 - e - 510             # 製造部行
    mfg[1] = u
    i = col_total[1] - u - 260 - 190                  # Q2列
    sales[1] = i
    a = row_total["営業"] - i - 350 - 400             # 営業部行
    sales[0] = a

    assert ki == 200
    assert ka == 350
    assert o == 300
    assert e == 490
    assert u == 470
    assert i == 320
    assert a == 330

    # 全行合計整合
    assert sum(sales) == row_total["営業"]
    assert sum(mfg) == row_total["製造"]
    assert sum(dev) == row_total["開発"]
    assert sum(admin) == row_total["管理"]
    # 全列合計整合
    rows = [sales, mfg, dev, admin]
    for c in range(4):
        assert sum(r[c] for r in rows) == col_total[c], c
    # 総合計
    assert sum(col_total) == grand_total
    assert sum(sum(r) for r in rows) == grand_total

    # 一意性: 7空欄を未知数とし、各行・列合計を制約に総当たり的に唯一解を確認
    # 各空欄の探索範囲を広めに取り、整合する組合せが1つだけであることを示す
    rng = range(100, 601, 10)
    solutions = 0
    # 効率化のため連立で順に絞るが、形式上は制約充足で一意性を確認
    for KI in rng:
        if 180 + 190 + 210 + KI != row_total["管理"]:
            continue
        for KA in rng:
            if 400 + 510 + KI + KA != col_total[3]:
                continue
            for O in rng:
                if 280 + 260 + KA + O != row_total["開発"]:
                    continue
                for E in rng:
                    if 350 + O + 210 + E != col_total[2]:
                        continue
                    for U in rng:
                        if 300 + E + 510 + U != row_total["製造"]:
                            continue
                        for I in rng:
                            if U + 260 + 190 + I != col_total[1]:
                                continue
                            for AA in rng:
                                if I + 350 + 400 + AA != row_total["営業"]:
                                    continue
                                # Q1列整合
                                if AA + 300 + 280 + 180 != col_total[0]:
                                    continue
                                solutions += 1
    assert solutions == 1, "解が%d個" % solutions
    print("Q2 OK: ア=%d イ=%d ウ=%d エ=%d オ=%d カ=%d キ=%d (解は一意)" % (a, i, u, e, o, ka, ki))
    return a


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("ALL VERIFIED: 解は一意")
