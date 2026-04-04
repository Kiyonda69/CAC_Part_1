#!/usr/bin/env python3
"""セット101の解の一意性検証"""

def verify_q1():
    """問1: 住民1人あたりの年間施設利用回数が最も多い地区"""
    print("=== 問1: 公共施設利用状況 ===")
    
    districts = {
        "A地区": {"population": 25000, "usage": 187500},
        "B地区": {"population": 18000, "usage": 144000},
        "C地区": {"population": 32000, "usage": 224000},
        "D地区": {"population": 15000, "usage": 127500},
        "E地区": {"population": 22000, "usage": 176000},
    }
    
    per_capita = {}
    for name, data in districts.items():
        rate = data["usage"] / data["population"]
        per_capita[name] = rate
        print(f"  {name}: {data['usage']:,} / {data['population']:,} = {rate:.2f}回")
    
    best = max(per_capita, key=per_capita.get)
    print(f"\n  最多: {best} ({per_capita[best]:.2f}回)")
    
    # 選択肢の対応: (1)A, (2)B, (3)C, (4)D, (5)E
    assert best == "D地区", f"正解がD地区ではない: {best}"
    print("  → 正解: (4) D地区")
    
    # 唯一解であることを確認（2番目との差）
    sorted_rates = sorted(per_capita.items(), key=lambda x: x[1], reverse=True)
    gap = sorted_rates[0][1] - sorted_rates[1][1]
    print(f"  1位と2位の差: {gap:.2f}回")
    assert gap > 0, "同率1位が存在する"
    
    return True

def verify_q2():
    """問2: 実効不良率の2番目と3番目の差"""
    print("\n=== 問2: 製造品質管理 ===")
    
    lines = {
        "P": {"production": 12000, "defects": 360, "reinspect_pass": 180},
        "Q": {"production": 9500, "defects": 228, "reinspect_pass": 114},
        "R": {"production": 15000, "defects": 525, "reinspect_pass": 225},
        "S": {"production": 8000, "defects": 200, "reinspect_pass": 120},
        "T": {"production": 11000, "defects": 385, "reinspect_pass": 165},
    }
    
    effective_rates = {}
    for name, data in lines.items():
        net_defects = data["defects"] - data["reinspect_pass"]
        rate = net_defects / data["production"] * 100
        effective_rates[name] = rate
        print(f"  ライン{name}: ({data['defects']} - {data['reinspect_pass']}) / {data['production']} * 100 = {rate:.2f}%")
    
    sorted_rates = sorted(effective_rates.items(), key=lambda x: x[1])
    print(f"\n  低い順:")
    for i, (name, rate) in enumerate(sorted_rates):
        print(f"    {i+1}位: ライン{name} = {rate:.2f}%")
    
    second = sorted_rates[1][1]
    third = sorted_rates[2][1]
    diff = third - second
    print(f"\n  2番目: {sorted_rates[1][0]} = {second:.2f}%")
    print(f"  3番目: {sorted_rates[2][0]} = {third:.2f}%")
    print(f"  差: {diff:.2f}ポイント")
    
    assert abs(diff - 0.30) < 0.001, f"差が0.30ではない: {diff}"
    print("  → 正解: (5) 0.30ポイント")
    
    # 唯一解確認: 2番目と3番目が明確に異なる
    assert second != third, "2番目と3番目が同率"
    
    # 選択肢の検証
    choices = {1: 0.10, 2: 0.20, 3: 0.25, 4: 0.35, 5: 0.30}
    correct_count = sum(1 for v in choices.values() if abs(v - diff) < 0.001)
    assert correct_count == 1, f"正解が{correct_count}個ある"
    
    return True

if __name__ == "__main__":
    q1_ok = verify_q1()
    q2_ok = verify_q2()
    
    if q1_ok and q2_ok:
        print("\n✓ 両問とも検証OK: 解は唯一")
    else:
        print("\n✗ 検証失敗")
