#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""航大思考251 検証: 整備規程と飛行記録簿の読み取り（点検期限管理）"""


def check_hours(last_a, last_b, current, hours_needed):
    """A点検・B点検の残時間チェック。
    規則3: B点検実施時はA点検も同時実施とみなす → A基点 = max(last_a, last_b)
    """
    eff_a = max(last_a, last_b)
    rem_a = 50.0 - (current - eff_a)
    rem_b = 100.0 - (current - last_b)
    return rem_a, rem_b, (rem_a >= hours_needed and rem_b >= hours_needed)


def verify_q1():
    """問1: 点検なしで第何便まで飛行できるか（正解: 第5便まで = 選択肢5）"""
    last_a = 2286.5   # 前回A点検時の総飛行時間
    last_b = 2304.0   # 前回B点検時の総飛行時間（A点検より後 → 規則3が効く）
    current = 2326.0  # 現在の総飛行時間
    flights = [4.5, 5.0, 6.0, 5.5, 6.5]  # 第1便〜第5便

    eff_a = max(last_a, last_b)
    due_a = eff_a + 50.0    # 2354.0
    due_b = last_b + 100.0  # 2404.0

    ok_upto = 0
    total = current
    for i, f in enumerate(flights, 1):
        total += f
        if total <= due_a and total <= due_b:
            ok_upto = i
        else:
            break
    assert ok_upto == 5, f"問1: 第{ok_upto}便まで（期待: 5）"
    # 余裕の確認（自明でないこと）: 累計27.5h vs A残28.0h
    assert abs((due_a - current) - 28.0) < 1e-9
    assert abs(sum(flights) - 27.5) < 1e-9

    # トラップ検証: 規則3を見落とすと A基点=2286.5 → 残10.5h → 第2便まで
    naive_due_a = last_a + 50.0
    naive = 0
    total = current
    for i, f in enumerate(flights, 1):
        total += f
        if total <= naive_due_a and total <= due_b:
            naive = i
        else:
            break
    assert naive == 2, f"トラップ: 第{naive}便（期待: 2）"
    print(f"問1 OK: 正解=第5便まで(選択肢5) / 見落とし時=第{naive}便(誤答2)")


def verify_q2():
    """問2: 訓練飛行22.0hを点検なしで実施できる機体（正解: 機体C = 選択肢3）"""
    # (機体, 前回A点検, 前回B点検, 現在総飛行時間, 年次検査実施年月)
    fleet = [
        ("A", 980.0, 920.0, 1010.0, (2025, 12)),
        ("B", 2455.0, 2410.0, 2480.0, (2025, 6)),
        ("C", 1530.0, 1560.0, 1572.0, (2025, 10)),
        ("D", 760.0, 700.0, 785.0, (2025, 9)),
        ("E", 1236.0, 1262.0, 1296.0, (2025, 8)),
    ]
    NEED = 22.0
    # 年次検査: 実施月の翌年同月末日まで有効。訓練最終日 2026-07-12 まで有効が必要
    # → (実施年+1, 実施月) >= (2026, 7) すなわち実施月が2025年7月以降
    valid = []
    detail = {}
    for name, la, lb, cur, (yy, mm) in fleet:
        rem_a, rem_b, hours_ok = check_hours(la, lb, cur, NEED)
        annual_ok = (yy + 1, mm) >= (2026, 7)
        detail[name] = (rem_a, rem_b, annual_ok)
        if hours_ok and annual_ok:
            valid.append(name)
    assert valid == ["C"], f"問2: 解={valid}（期待: ['C']）"
    for name, (ra, rb, an) in detail.items():
        print(f"  機体{name}: A残={ra:.1f}h B残={rb:.1f}h 年次={'有効' if an else '失効'}")
    # トラップ検証: 規則3を無視すると機体Cは A残=8.0h で不適合 → 該当機体なし
    naive_valid = [n for n, la, lb, cur, (yy, mm) in fleet
                   if (50.0 - (cur - la)) >= NEED and (100.0 - (cur - lb)) >= NEED
                   and (yy + 1, mm) >= (2026, 7)]
    assert naive_valid == [], f"トラップ: {naive_valid}"
    print("問2 OK: 正解=機体C(選択肢3) / 規則3見落とし時=該当なし")


if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("全検証 PASS: 両問とも解は一意")
