#!/usr/bin/env python3
"""セット255検証: MEL（最低装備品目録）による出発可否判定問題

問1: MEL表の条件（必要数・飛行条件・(M)(O)処置）による出発可否
問2: 修理期限カテゴリ（B/C/D）・RIE延長・同一系統複数故障の規則を追加
"""
from datetime import date, timedelta

# MEL表（抜粋）: 項目番号 -> (装備品, 装備数, 出発に必要な数, カテゴリ, 条件)
# 条件は関数: (flight, aircraft_state) -> (OK?, 理由)
MEL = {
    "23-1": ("VHF無線機", 2, 1, "B", "IFRでは2台必要"),
    "25-1": ("客室蛍光灯", 4, 0, "D", "条件なし"),
    "25-3": ("客室読書灯", 6, 0, "C", "条件なし"),
    "33-4": ("着陸灯", 2, 1, "C", "夜間は2個必要/(M)電球取外し"),
    "34-1": ("機上気象レーダー", 1, 0, "D", "(O)昼間VFRに限る"),
    "36-2": ("客室スピーカー", 2, 1, "C", "(O)口頭ブリーフィング"),
}

def item_ok(item, n_failed, action_done, night, ifr, pax):
    """規則1〜3: 1件の故障がMEL条件を満たすか"""
    if item not in MEL:
        return False  # 規則2: MEL表に記載なし
    _, installed, required, _, _ = MEL[item]
    working = installed - n_failed
    # 飛行条件による必要数の引き上げ
    if item == "23-1" and ifr:
        required = 2
    if item == "33-4" and night:
        required = 2
    if working < required:
        return False
    # (M)/(O) 処置
    if item in ("33-4", "34-1", "36-2") and not action_done:
        return False
    # 飛行条件の制限
    if item == "34-1" and (night or ifr):
        return False  # 昼間VFRに限る
    return True

def can_dispatch(defects, night, ifr, pax):
    """defects: list of (item, n_failed, action_done). 記載外故障は item=None"""
    # 規則7相当は問2で別判定
    return all(
        (item is not None) and item_ok(item, n, act, night, ifr, pax)
        for (item, n, act) in defects
    )

# ===== 問1: 夜間IFR連絡飛行（乗客あり） =====
Q1 = {
    "A": [("23-1", 1, True)],                          # VHF1台故障→IFRは2台必要
    "B": [("36-2", 1, True), ("25-3", 1, True)],       # 処置済み→出発可
    "C": [("34-1", 1, True)],                          # 昼間VFR限定→夜間IFR不可
    "D": [("25-3", 2, True), ("33-4", 1, True)],       # 夜間は着陸灯2個必要
    "E": [(None, 1, False)],                           # MEL表に記載なし（規則2）
}

def verify_q1():
    ok = [k for k, d in Q1.items() if can_dispatch(d, night=True, ifr=True, pax=True)]
    assert ok == ["B"], f"問1: 出発可能機体が {ok}（期待: ['B']）"
    print("問1 OK: 出発できる機体は B のみ → 正解(2)")

# ===== 問2: 7/7〜7/11 毎日夜間IFR、修理不可 =====
# 記録: (item, n_failed, action_done, 発見日, RIE適用)
Q2 = {
    "A": [("25-3", 1, True, date(2026, 6, 28), True)],   # C:6/29-7/8, RIEで7/18まで
    "B": [("25-3", 1, True, date(2026, 6, 28), False)],  # 7/8まで→7/9以降NG
    "C": [("25-1", 1, True, date(2026, 6, 20), False),   # 系統25が2件→規則7
          ("25-3", 1, True, date(2026, 7, 3), False)],
    "D": [("34-1", 1, True, date(2026, 7, 1), False)],   # 昼間VFR限定→夜間IFR不可
    "E": [("33-4", 1, True, date(2026, 7, 2), False)],   # 期限内でも夜間2個必要
}
CAT_DAYS = {"B": 3, "C": 10, "D": 120}

def deadline(item, found, rie):
    days = CAT_DAYS[MEL[item][3]]
    end = found + timedelta(days=days)  # 発見日を除き days 日 → 最終日
    if rie and MEL[item][3] != "B":     # 規則6: カテゴリBはRIE不可
        end += timedelta(days=days)
    return end

def can_dispatch_q2(records, day):
    systems = [r[0][:2] for r in records]
    if any(systems.count(s) >= 2 for s in set(systems)):
        return False  # 規則7: 同一系統2件以上
    for (item, n, act, found, rie) in records:
        if day > deadline(item, found, rie):
            return False  # 規則8: 修理期限超過
        if not item_ok(item, n, act, night=True, ifr=True, pax=True):
            return False
    return True

def verify_q2():
    days = [date(2026, 7, 7) + timedelta(days=i) for i in range(5)]
    ok = [k for k, r in Q2.items() if all(can_dispatch_q2(r, d) for d in days)]
    assert ok == ["A"], f"問2: 全日出発可能機体が {ok}（期待: ['A']）"
    # 各機体の脱落理由の確認（すべての条件が解導出に必要）
    assert can_dispatch_q2(Q2["B"], date(2026, 7, 8))
    assert not can_dispatch_q2(Q2["B"], date(2026, 7, 9))  # Bは期限で脱落
    assert deadline("25-3", date(2026, 6, 28), True) == date(2026, 7, 18)
    print("問2 OK: 5日間すべて出発できる機体は A のみ → 正解(1)")
    print("  A: 期限7/8→RIE延長で7/18まで / B: 7/9以降期限超過")
    print("  C: 系統25複数故障 / D: 夜間IFR不可 / E: 着陸灯夜間2個必要")

if __name__ == "__main__":
    verify_q1()
    verify_q2()
    print("検証完了: 両問とも解は一意")
