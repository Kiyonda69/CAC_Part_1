#!/usr/bin/env python3
"""
航大思考33 解の検証スクリプト
問1・問2: 生産機械スケジューリング最適化問題
"""

# =============================================================================
# 問1: 3機械・240分・最大2台同時稼働
# =============================================================================
def verify_q1():
    """240分間で最大生産量を求める（3機械）"""
    print("=" * 60)
    print("問1: 機械P・Q・R / 240分 / 最大2台同時稼働")
    print("=" * 60)

    machines = {
        "P": {"rate": 12, "run": 30, "cool": 10},  # 40分/サイクル, 360個/サイクル
        "Q": {"rate": 10, "run": 40, "cool": 20},  # 60分/サイクル, 400個/サイクル
        "R": {"rate": 16, "run": 25, "cool": 15},  # 40分/サイクル, 400個/サイクル
    }
    total_time = 240

    # 各機械の単独性能
    for name, m in machines.items():
        cycle = m["run"] + m["cool"]
        per_cycle = m["rate"] * m["run"]
        cycles = total_time // cycle
        production = cycles * per_cycle
        print(f"  機械{name}: {m['run']}+{m['cool']}={cycle}分/サイクル, "
              f"{m['rate']}×{m['run']}={per_cycle}個/サイクル, "
              f"{total_time}/{cycle}={cycles}サイクル → {production}個")

    print()

    # 2機械同時運転（単純: 両機械が300分間ずっと稼働する場合）
    print("2機械同時稼働（単純計算）:")
    combos = [("P", "Q"), ("P", "R"), ("Q", "R")]
    max_simple = 0
    best_simple = None
    for a, b in combos:
        cycle_a = machines[a]["run"] + machines[a]["cool"]
        cycle_b = machines[b]["run"] + machines[b]["cool"]
        per_cycle_a = machines[a]["rate"] * machines[a]["run"]
        per_cycle_b = machines[b]["rate"] * machines[b]["run"]
        n_a = total_time // cycle_a
        n_b = total_time // cycle_b
        prod = n_a * per_cycle_a + n_b * per_cycle_b
        print(f"  {a}+{b}: {n_a}×{per_cycle_a} + {n_b}×{per_cycle_b} = {n_a * per_cycle_a} + {n_b * per_cycle_b} = {prod}個")
        if prod > max_simple:
            max_simple = prod
            best_simple = f"{a}+{b}"

    print(f"\n  最大: {best_simple} = {max_simple}個")

    # 3機械スケジューリング検討
    print("\n3機械スケジューリング（切替え検討）:")
    # P, R がともに40分サイクルで240分を完全に埋める
    # → P+R同時稼働中はQが入れない
    # 切替えパターン: P+Q → P+R or P+Q → Q+R
    best_switch = 0
    best_switch_desc = ""

    machines_list = ["P", "Q", "R"]
    # 切替えタイミングを総当たり（0から240まで10分刻み）
    for t_switch in range(0, total_time + 1, 10):
        for a1, b1, a2, b2 in [
            ("P", "Q", "P", "R"), ("P", "Q", "Q", "R"),
            ("P", "R", "P", "Q"), ("P", "R", "Q", "R"),
            ("Q", "R", "P", "Q"), ("Q", "R", "P", "R"),
        ]:
            if a1 == a2 or b1 == b2 or a1 == b2 or b1 == a2:
                # 切替えで3台すべてを使う組み合わせのみ
                pass
            # phase1: a1+b1 を 0〜t_switch まで
            # phase2: a2+b2 を t_switch〜240 まで
            # ただし各機械はサイクル途中で停止不可
            def cycles_in_window(machine, t_start, t_end):
                cycle = machines[machine]["run"] + machines[machine]["cool"]
                window = t_end - t_start
                return window // cycle

            n_a1 = cycles_in_window(a1, 0, t_switch)
            n_b1 = cycles_in_window(b1, 0, t_switch)
            n_a2 = cycles_in_window(a2, t_switch, total_time)
            n_b2 = cycles_in_window(b2, t_switch, total_time)

            # 各機械の総サイクル数
            used = set([a1, b1, a2, b2])
            if len(used) < 3:
                continue  # 3機械使わない場合はスキップ

            prod_a1 = n_a1 * machines[a1]["rate"] * machines[a1]["run"]
            prod_b1 = n_b1 * machines[b1]["rate"] * machines[b1]["run"]
            prod_a2 = n_a2 * machines[a2]["rate"] * machines[a2]["run"]
            prod_b2 = n_b2 * machines[b2]["rate"] * machines[b2]["run"]

            # 各機械の合計（重複を避ける）
            machine_prod = {}
            for m, p in [(a1, prod_a1), (b1, prod_b1), (a2, prod_a2), (b2, prod_b2)]:
                machine_prod[m] = machine_prod.get(m, 0) + p

            total_prod = sum(machine_prod.values())
            if total_prod > best_switch:
                best_switch = total_prod
                best_switch_desc = f"t={t_switch}: {a1}+{b1} → {a2}+{b2} = {total_prod}個"

    print(f"  最良の切替えパターン: {best_switch_desc}")
    print(f"  2機械単純計算の最大: {max_simple}個")
    print(f"  切替えで改善できるか: {'Yes' if best_switch > max_simple else 'No'}")

    overall_max = max(max_simple, best_switch)
    print(f"\n問1 正解: {overall_max}個")
    return overall_max


# =============================================================================
# 問2: 4機械・300分・最大2台同時稼働
# =============================================================================
def verify_q2():
    """300分間で最大生産量を求める（4機械）"""
    print()
    print("=" * 60)
    print("問2: 機械W・X・Y・Z / 300分 / 最大2台同時稼働")
    print("=" * 60)

    machines = {
        "W": {"rate": 15, "run": 40, "cool": 20},  # 60分/サイクル, 600個/サイクル
        "X": {"rate": 12, "run": 40, "cool": 10},  # 50分/サイクル, 480個/サイクル
        "Y": {"rate": 20, "run": 20, "cool": 10},  # 30分/サイクル, 400個/サイクル
        "Z": {"rate": 18, "run": 30, "cool": 20},  # 50分/サイクル, 540個/サイクル
    }
    total_time = 300

    # 各機械の単独性能
    for name, m in machines.items():
        cycle = m["run"] + m["cool"]
        per_cycle = m["rate"] * m["run"]
        cycles = total_time // cycle
        production = cycles * per_cycle
        print(f"  機械{name}: {m['run']}+{m['cool']}={cycle}分/サイクル, "
              f"{m['rate']}×{m['run']}={per_cycle}個/サイクル, "
              f"{total_time}/{cycle}={cycles}サイクル → {production}個")

    print()

    # 2機械同時運転
    print("2機械同時稼働（単純計算）:")
    from itertools import combinations
    machine_names = list(machines.keys())
    max_simple = 0
    best_simple = None
    results = {}
    for a, b in combinations(machine_names, 2):
        cycle_a = machines[a]["run"] + machines[a]["cool"]
        cycle_b = machines[b]["run"] + machines[b]["cool"]
        per_cycle_a = machines[a]["rate"] * machines[a]["run"]
        per_cycle_b = machines[b]["rate"] * machines[b]["run"]
        n_a = total_time // cycle_a
        n_b = total_time // cycle_b
        prod = n_a * per_cycle_a + n_b * per_cycle_b
        results[f"{a}+{b}"] = prod
        print(f"  {a}+{b}: {n_a}×{per_cycle_a} + {n_b}×{per_cycle_b} = "
              f"{n_a * per_cycle_a} + {n_b * per_cycle_b} = {prod}個")
        if prod > max_simple:
            max_simple = prod
            best_simple = f"{a}+{b}"

    print(f"\n  最大: {best_simple} = {max_simple}個")

    # 3機械スケジューリング検討
    print("\n3機械スケジューリング（切替え検討）:")
    best_switch = 0
    best_switch_desc = ""

    for t_switch in range(0, total_time + 1, 10):
        for (a1, b1), (a2, b2) in [
            (("W", "X"), ("W", "Y")), (("W", "X"), ("W", "Z")),
            (("W", "X"), ("X", "Y")), (("W", "X"), ("X", "Z")),
            (("W", "X"), ("Y", "Z")),
            (("W", "Y"), ("W", "X")), (("W", "Y"), ("W", "Z")),
            (("W", "Y"), ("X", "Y")), (("W", "Y"), ("X", "Z")),
            (("W", "Y"), ("Y", "Z")),
            (("W", "Z"), ("W", "X")), (("W", "Z"), ("W", "Y")),
            (("W", "Z"), ("X", "Y")), (("W", "Z"), ("X", "Z")),
            (("W", "Z"), ("Y", "Z")),
            (("X", "Y"), ("W", "X")), (("X", "Y"), ("W", "Y")),
            (("X", "Y"), ("W", "Z")), (("X", "Y"), ("X", "Z")),
            (("X", "Y"), ("Y", "Z")),
            (("X", "Z"), ("W", "X")), (("X", "Z"), ("W", "Y")),
            (("X", "Z"), ("W", "Z")), (("X", "Z"), ("X", "Y")),
            (("X", "Z"), ("Y", "Z")),
            (("Y", "Z"), ("W", "X")), (("Y", "Z"), ("W", "Y")),
            (("Y", "Z"), ("W", "Z")), (("Y", "Z"), ("X", "Y")),
            (("Y", "Z"), ("X", "Z")),
        ]:
            used = set([a1, b1, a2, b2])
            if len(used) < 3:
                continue

            def cycles_in(machine, t_start, t_end):
                cycle = machines[machine]["run"] + machines[machine]["cool"]
                window = t_end - t_start
                return window // cycle

            n = {
                (a1, "phase1"): cycles_in(a1, 0, t_switch),
                (b1, "phase1"): cycles_in(b1, 0, t_switch),
                (a2, "phase2"): cycles_in(a2, t_switch, total_time),
                (b2, "phase2"): cycles_in(b2, t_switch, total_time),
            }
            machine_prod = {}
            for (m, phase), cnt in n.items():
                per_c = machines[m]["rate"] * machines[m]["run"]
                machine_prod[m] = machine_prod.get(m, 0) + cnt * per_c

            total_prod = sum(machine_prod.values())
            if total_prod > best_switch:
                best_switch = total_prod
                best_switch_desc = f"t={t_switch}: {a1}+{b1} → {a2}+{b2} = {total_prod}個"

    print(f"  最良の切替えパターン: {best_switch_desc}")
    print(f"  2機械単純計算の最大: {max_simple}個")
    print(f"  切替えで改善できるか: {'Yes' if best_switch > max_simple else 'No'}")

    overall_max = max(max_simple, best_switch)
    print(f"\n問2 正解: {overall_max}個")
    return overall_max


if __name__ == "__main__":
    q1_ans = verify_q1()
    q2_ans = verify_q2()
    print()
    print("=" * 60)
    print(f"問1 正解: {q1_ans:,}個")
    print(f"問2 正解: {q2_ans:,}個")
    print("=" * 60)
