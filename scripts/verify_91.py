"""
航大思考91 検証スクリプト
問1: 進入角度指示灯の状態変化→操縦操作判定（PAPI類題）
問2: 進入角度・速度の二重監視（2変数同時補正）
"""

# ============================================================
# 問1: 進入角度指示灯システム（PAPI類題）
# ============================================================
# 4パネル P1(2.5°), P2(2.8°), P3(3.2°), P4(3.5°)
# 進入角度がパネルの閾値より低い → ● (暗色)
# 進入角度がパネルの閾値より高い → ○ (明色)
#
# 正常 (2.8〜3.2°): ○○●● (P1,P2は角度が上→○、P3,P4は角度が下→●)
#
# 状態変化: ○○●● → ○●●● (角度低下: 2.5〜2.8°に)
#
# 操作:
# ア: 操縦桿を引き、推力を上げる（機首上げ+加速=角度上昇）
# イ: 操縦桿と推力を維持する
# ウ: 推力を上げる（加速のみ、角度はほぼ変わらない）
# エ: 操縦桿を押す（機首下げ=角度低下）
# オ: 推力を下げる（減速=降下傾向）
#
# 正解: ア
# 理由: 角度を上げるには機首上げが必要だが、
#       機首上げだけでは速度低下→失速リスク
#       推力増加も同時に行う必要がある

def verify_q1():
    """問1の解の一意性を検証"""
    print("=" * 60)
    print("問1: 進入角度指示灯（PAPI類題）")
    print("=" * 60)

    # 状態変化: ○○●● → ○●●● (角度低下、やや低い)
    # 必要: 進入角度を上げる + 速度を維持する

    operations = {
        'ア': {'angle': +1, 'safe_speed': True,  'desc': '機首上げ+推力増（角度↑、速度維持）'},
        'イ': {'angle':  0, 'safe_speed': True,  'desc': '維持（何もしない）'},
        'ウ': {'angle':  0, 'safe_speed': True,  'desc': '推力増のみ（速度↑、角度ほぼ不変）'},
        'エ': {'angle': -1, 'safe_speed': True,  'desc': '機首下げ（角度↓）'},
        'オ': {'angle': -1, 'safe_speed': False, 'desc': '推力減（速度↓、降下傾向）'},
    }

    # 条件:
    # 1. 角度変化 = +1 (角度を上げて正常に戻す)
    # 2. 速度が安全に維持される (機首上げ時は推力増が必要)
    # → アのみが両方を満たす

    valid = []
    print("\n  --- 単一操作の検証 ---")
    for op, eff in operations.items():
        ok = eff['angle'] == +1 and eff['safe_speed']
        status = "有効" if ok else "無効"
        reasons = []
        if eff['angle'] != +1:
            reasons.append(f"角度変化={eff['angle']:+d}≠+1")
        if not eff['safe_speed'] and eff['angle'] > 0:
            reasons.append("速度低下リスク")
        reason_str = f" ({', '.join(reasons)})" if reasons else ""
        print(f"  {op}: {eff['desc']} → {status}{reason_str}")
        if ok:
            valid.append(op)

    print(f"\n  有効な操作: {valid}")
    assert len(valid) == 1, f"解が{len(valid)}個: {valid}"
    assert valid[0] == 'ア', f"正解がアでない: {valid[0]}"
    print(f"  正解: ア（唯一解確認済み）")

    # 選択肢配置（正解位置: 3）
    print(f"\n  選択肢配置:")
    options = {
        1: ('ア、ウ', 'ア(機首上げ+推力増)に更にウ(推力増)=速度超過'),
        2: ('イ', '維持→低角度のまま→危険'),
        3: ('ア', '機首上げ+推力増→正解'),
        4: ('ウ', '推力のみ→速度は上がるが角度不変'),
        5: ('オ', '推力減→さらに降下→危険'),
    }
    for num, (opt, reason) in options.items():
        mark = "★正解" if num == 3 else "不正解"
        print(f"    ({num}) {opt}: {reason} [{mark}]")

    return True


# ============================================================
# 問2: 進入角度・速度の二重監視
# ============================================================
# 角度指示灯 P1-P4: 2.5°/2.8°/3.2°/3.5° 正常=○○●●
# 速度指示灯 Q1-Q4: 120/130/140/150kt 正常=●●○○
#   Q: 速度が閾値を超えると●
#
# 操作と効果:
# ア: 推力を上げる → angle+1, speed+1
# イ: 推力を下げる → angle-1, speed-1
# ウ: 操縦桿を引く → angle+1, speed±0
# エ: スピードブレーキを展開 → angle±0, speed-1
# オ: スピードブレーキを格納 → angle±0, speed+1
#
# 状態変化:
# 角度: ○○●● → ○●●● (やや低い, 必要: +1)
# 速度: ●●○○ → ●●●○ (やや速い, 必要: -1)
#
# 正解: ウ+エ = (+1,0)+(0,-1) = (+1,-1) ✓

def verify_q2():
    """問2の解の一意性を検証（全組み合わせ探索）"""
    print("\n" + "=" * 60)
    print("問2: 進入角度・速度の二重監視")
    print("=" * 60)

    # 操作の効果: (角度変化, 速度変化)
    ops = {
        'ア': (+1, +1),
        'イ': (-1, -1),
        'ウ': (+1,  0),
        'エ': ( 0, -1),
        'オ': ( 0, +1),
    }

    # 必要な変化: 角度+1, 速度-1
    target = (+1, -1)

    op_names = list(ops.keys())
    valid_solutions = []

    # 単一操作
    print("\n  --- 単一操作の検証 ---")
    for name in op_names:
        effect = ops[name]
        result = "有効" if effect == target else "無効"
        print(f"  {name}: angle={effect[0]:+d}, speed={effect[1]:+d} → {result}")
        if effect == target:
            valid_solutions.append(name)

    # 2操作の組み合わせ
    print("\n  --- 2操作の組み合わせ検証 ---")
    from itertools import combinations_with_replacement
    for combo in combinations_with_replacement(op_names, 2):
        a = ops[combo[0]][0] + ops[combo[1]][0]
        s = ops[combo[0]][1] + ops[combo[1]][1]
        combo_str = f"{combo[0]}+{combo[1]}"
        if (a, s) == target:
            valid_solutions.append(combo_str)
            print(f"  {combo_str}: angle={a:+d}, speed={s:+d} → ★有効")
        else:
            print(f"  {combo_str}: angle={a:+d}, speed={s:+d} → 無効")

    print(f"\n  有効な解: {valid_solutions}")
    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個: {valid_solutions}"
    assert valid_solutions[0] == 'ウ+エ', f"正解がウ+エでない: {valid_solutions[0]}"
    print(f"  正解: ウ、エ（唯一解確認済み）")

    # 選択肢配置（正解位置: 4）
    print(f"\n  選択肢配置:")
    options_q2 = {
        1: ('ア、エ', (+1+0, +1-1), '(+1, 0) → 速度が戻らない'),
        2: ('イ、オ', (-1+0, -1+1), '(-1, 0) → 角度がさらに低下'),
        3: ('ア、ウ', (+1+1, +1+0), '(+2, +1) → 両方過剰'),
        4: ('ウ、エ', (+1+0, 0-1), '(+1, -1) → 正解'),
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
        print("問2 正解: (4) ウ、エ")
    else:
        print("検証に失敗した問題があります。")
    print("=" * 60)
