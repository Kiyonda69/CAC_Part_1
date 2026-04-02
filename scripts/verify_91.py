"""
航大思考91 検証スクリプト
問1: 感温表示パネルシステム（状態変化→操作判定）
問2: 温度・圧力二重監視パネル（2変数同時補正）
"""

# ============================================================
# 問1: 感温表示パネルシステム
# ============================================================
# 4パネル P1(180°C), P2(200°C), P3(220°C), P4(240°C)
# 正常: ●●○○ (レベル2: 200-220°C)
# 状態変化: ●●○○ → ●○○○ (レベル2→レベル1: 温度低下)
#
# 操作:
# ア: 加熱出力を上げ、攪拌速度を上げる（温度上昇+均一化）
# イ: 現状の設定を維持する
# ウ: 加熱出力を上げる（温度上昇のみ、局所過熱リスク）
# エ: 攪拌速度を下げる
# オ: 加熱出力を下げる
#
# 正解: ア (加熱+攪拌の複合操作が必要)
# 理由: 加熱だけ(ウ)では温度むらが生じ局所過熱する
#       攪拌も同時に上げる必要がある

def verify_q1():
    """問1の解の一意性を検証"""
    print("=" * 60)
    print("問1: 感温表示パネルシステム")
    print("=" * 60)

    # 状態変化: レベル2→レベル1 (温度低下)
    # 必要な操作: 温度を上げる + 温度むらを防ぐ

    operations = {
        'ア': {'temp_change': +1, 'stir_change': +1, 'desc': '加熱↑・攪拌↑'},
        'イ': {'temp_change': 0, 'stir_change': 0, 'desc': '維持'},
        'ウ': {'temp_change': +1, 'stir_change': 0, 'desc': '加熱↑のみ'},
        'エ': {'temp_change': 0, 'stir_change': -1, 'desc': '攪拌↓'},
        'オ': {'temp_change': -1, 'stir_change': 0, 'desc': '加熱↓'},
    }

    current_level = 1  # ●○○○
    target_level = 2   # ●●○○ (正常)
    needed_temp = target_level - current_level  # +1

    # 条件:
    # 1. 温度変化 = +1 (レベル1→レベル2に戻す)
    # 2. 攪拌変化 >= 0 (温度を上げる際に攪拌も上げないと局所過熱)
    # 3. 加熱と攪拌を同時に行う必要がある（問題文の制約）

    # 単一操作で条件を満たすか検証
    valid_single = []
    for op, effect in operations.items():
        if effect['temp_change'] == needed_temp and effect['stir_change'] > 0:
            valid_single.append(op)
            print(f"  単一操作 {op}({effect['desc']}): temp={effect['temp_change']:+d}, stir={effect['stir_change']:+d} → 有効")
        else:
            reason = []
            if effect['temp_change'] != needed_temp:
                reason.append(f"温度変化{effect['temp_change']:+d}≠{needed_temp:+d}")
            if effect['stir_change'] <= 0 and effect['temp_change'] > 0:
                reason.append("攪拌不足(局所過熱リスク)")
            print(f"  単一操作 {op}({effect['desc']}): temp={effect['temp_change']:+d}, stir={effect['stir_change']:+d} → 無効 ({', '.join(reason) if reason else '不適切'})")

    print(f"\n  有効な操作: {valid_single}")
    assert len(valid_single) == 1, f"解が{len(valid_single)}個: {valid_single}"
    assert valid_single[0] == 'ア', f"正解がアでない: {valid_single[0]}"
    print(f"  正解: ア（唯一解確認済み）")

    # 選択肢の検証（正解位置: 3）
    print(f"\n  選択肢配置:")
    options = {
        1: ('ア、ウ', '加熱+攪拌 かつ 追加加熱 → 過加熱'),
        2: ('イ', '維持 → 温度低下のまま'),
        3: ('ア', '加熱+攪拌 → 正解'),
        4: ('ウ', '加熱のみ → 局所過熱リスク'),
        5: ('オ', '加熱↓ → さらに温度低下'),
    }
    for num, (opt, reason) in options.items():
        mark = "★正解" if num == 3 else "不正解"
        print(f"    ({num}) {opt}: {reason} [{mark}]")

    return True

# ============================================================
# 問2: 温度・圧力二重監視パネル
# ============================================================
# 温度パネル P1-P4: 180/200/220/240°C, 正常=●●○○
# 圧力パネル Q1-Q4: 0.5/1.0/1.5/2.0 MPa, 正常=●●○○
#
# 操作と効果:
# ア: 加熱出力を上げる → temp+1, pressure+1
# イ: 加熱出力を下げる → temp-1, pressure-1
# ウ: 冷却水バルブを開く → temp-1, pressure±0
# エ: 圧力逃し弁を開く → temp±0, pressure-1
# オ: 圧力逃し弁を閉じる → temp±0, pressure+1
#
# 状態変化:
# 温度: ●●○○(L2) → ●●●○(L3) → 必要: -1
# 圧力: ●●○○(L2) → ●○○○(L1) → 必要: +1
#
# 正解: ウ+オ = (-1,0)+(0,+1) = (-1,+1)

def verify_q2():
    """問2の解の一意性を検証（全組み合わせ探索）"""
    print("\n" + "=" * 60)
    print("問2: 温度・圧力二重監視パネル")
    print("=" * 60)

    # 操作の効果: (温度変化, 圧力変化)
    ops = {
        'ア': (+1, +1),
        'イ': (-1, -1),
        'ウ': (-1, 0),
        'エ': (0, -1),
        'オ': (0, +1),
    }

    # 必要な変化: 温度-1, 圧力+1
    target = (-1, +1)

    op_names = list(ops.keys())
    valid_solutions = []

    # 単一操作
    print("\n  --- 単一操作の検証 ---")
    for name in op_names:
        effect = ops[name]
        result = "有効" if effect == target else "無効"
        print(f"  {name}: temp={effect[0]:+d}, pres={effect[1]:+d} → {result}")
        if effect == target:
            valid_solutions.append(name)

    # 2操作の組み合わせ（同じ操作の重複も含む）
    print("\n  --- 2操作の組み合わせ検証 ---")
    from itertools import combinations_with_replacement
    for combo in combinations_with_replacement(op_names, 2):
        t = ops[combo[0]][0] + ops[combo[1]][0]
        p = ops[combo[0]][1] + ops[combo[1]][1]
        result = "有効" if (t, p) == target else "無効"
        combo_str = f"{combo[0]}+{combo[1]}"
        if (t, p) == target:
            valid_solutions.append(combo_str)
            print(f"  {combo_str}: temp={t:+d}, pres={p:+d} → ★有効")
        else:
            print(f"  {combo_str}: temp={t:+d}, pres={p:+d} → 無効")

    print(f"\n  有効な解: {valid_solutions}")
    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個: {valid_solutions}"
    assert valid_solutions[0] == 'ウ+オ', f"正解がウ+オでない: {valid_solutions[0]}"
    print(f"  正解: ウ、オ（唯一解確認済み）")

    # 選択肢の検証（正解位置: 4）
    print(f"\n  選択肢配置:")
    options_q2 = {
        1: ('ア、ウ', (+1-1, +1+0), '(0, +1) → 温度が戻らない'),
        2: ('イ、オ', (-1+0, -1+1), '(-1, 0) → 圧力が戻らない'),
        3: ('ウ、エ', (-1+0, 0-1), '(-1, -1) → 圧力がさらに低下'),
        4: ('ウ、オ', (-1+0, 0+1), '(-1, +1) → 正解'),
        5: ('イ、ア', (-1+1, -1+1), '(0, 0) → 何も変わらない'),
    }
    for num, (opt, effect, reason) in options_q2.items():
        mark = "★正解" if num == 4 else "不正解"
        print(f"    ({num}) {opt}: ({effect[0]:+d}, {effect[1]:+d}) {reason} [{mark}]")

    return True

# ============================================================
# メイン実行
# ============================================================
if __name__ == '__main__':
    print("航大思考91 検証開始\n")

    q1_ok = verify_q1()
    q2_ok = verify_q2()

    print("\n" + "=" * 60)
    if q1_ok and q2_ok:
        print("全問題の検証に成功しました。")
        print("問1 正解: (3) ア")
        print("問2 正解: (4) ウ、オ")
    else:
        print("検証に失敗した問題があります。")
    print("=" * 60)
