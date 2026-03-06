#!/usr/bin/env python3
"""
航大思考46 検証スクリプト
問1: 農場の1haあたり出荷額の順位
問2: 支店の従業員1人あたり年間利益額の順位
"""

# ============================================================
# 問1: 5つの農場の収穫データ
# ============================================================
print("=" * 60)
print("問1: 農場の1ヘクタールあたり出荷額（高い順）")
print("=" * 60)

farms = {
    'A': {'area_ha': 12, 'harvest_t': 84, 'pesticide_kg': 36, 'workers': 8, 'revenue_万円': 420},
    'B': {'area_ha': 18, 'harvest_t': 108, 'pesticide_kg': 72, 'workers': 12, 'revenue_万円': 540},
    'C': {'area_ha': 8, 'harvest_t': 72, 'pesticide_kg': 16, 'workers': 6, 'revenue_万円': 504},
    'D': {'area_ha': 15, 'harvest_t': 105, 'pesticide_kg': 60, 'workers': 10, 'revenue_万円': 480},
    'E': {'area_ha': 10, 'harvest_t': 60, 'pesticide_kg': 25, 'workers': 5, 'revenue_万円': 360},
}

print("\n農場データ:")
print(f"{'農場':<6} {'面積(ha)':<10} {'収穫量(t)':<10} {'出荷額(万円)':<12} {'1ha出荷額':<10}")
ratios = {}
for name, data in farms.items():
    ratio = data['revenue_万円'] / data['area_ha']
    ratios[name] = ratio
    print(f"  {name:<4} {data['area_ha']:<10} {data['harvest_t']:<10} {data['revenue_万円']:<12} {ratio:.1f}")

sorted_farms = sorted(ratios.items(), key=lambda x: x[1], reverse=True)
print(f"\n順位（高い順）: {'→'.join(f'{name}({val:.1f})' for name, val in sorted_farms)}")
order_q1 = '→'.join(name for name, _ in sorted_farms)
print(f"正解の並び順: {order_q1}")

# 全ての値が異なることを確認
values = list(ratios.values())
assert len(values) == len(set(values)), "同じ値が存在します！"
print("\n✓ 全ての値が異なることを確認")

# ============================================================
# 問2: 5つの支店の半期業績データ
# ============================================================
print("\n" + "=" * 60)
print("問2: 支店の従業員1人あたり年間利益額（大きい順）")
print("=" * 60)

branches = {
    '甲': {'h1_sales': 180, 'h1_cost': 120, 'h2_sales': 240, 'h2_cost': 150, 'employees': 30},
    '乙': {'h1_sales': 250, 'h1_cost': 170, 'h2_sales': 200, 'h2_cost': 130, 'employees': 40},
    '丙': {'h1_sales': 150, 'h1_cost': 90, 'h2_sales': 190, 'h2_cost': 110, 'employees': 25},
    '丁': {'h1_sales': 300, 'h1_cost': 210, 'h2_sales': 280, 'h2_cost': 190, 'employees': 50},
    '戊': {'h1_sales': 200, 'h1_cost': 140, 'h2_sales': 220, 'h2_cost': 140, 'employees': 35},
}

print("\n支店データ:")
print(f"{'支店':<6} {'上半期利益':<12} {'下半期利益':<12} {'年間利益':<10} {'従業員':<8} {'1人利益':<10}")
profit_per_emp = {}
for name, data in branches.items():
    h1_profit = data['h1_sales'] - data['h1_cost']
    h2_profit = data['h2_sales'] - data['h2_cost']
    annual = h1_profit + h2_profit
    per_emp = annual / data['employees']
    profit_per_emp[name] = per_emp
    print(f"  {name:<4} {h1_profit:<12} {h2_profit:<12} {annual:<10} {data['employees']:<8} {per_emp:.2f}")

sorted_branches = sorted(profit_per_emp.items(), key=lambda x: x[1], reverse=True)
print(f"\n順位（大きい順）: {'→'.join(f'{name}({val:.2f})' for name, val in sorted_branches)}")
order_q2 = '→'.join(name for name, _ in sorted_branches)
print(f"正解の並び順: {order_q2}")

# 全ての値が異なることを確認
values2 = list(profit_per_emp.values())
assert len(values2) == len(set(values2)), "同じ値が存在します！"
print("\n✓ 全ての値が異なることを確認")

print("\n" + "=" * 60)
print("検証完了: 両問とも解が唯一であることを確認")
print("=" * 60)
