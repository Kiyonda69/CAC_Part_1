"""
航大思考186 サイコロ転がし問題の検証
- 問1: 上面=1, 南=2, 東=3 から、東・北・東・南の順に転がした後の上面
- 問2: 上面=1, 南=2, 東=3 から、東・東・北・西・南・南・東の順に転がした後の (上面, 東面)
"""

def roll(die, direction):
    """サイコロを指定方向に1回転がす。
    die: {'top','bottom','north','south','east','west'} のdict
    """
    d = dict(die)
    if direction == 'east':
        d['top'] = die['west']
        d['east'] = die['top']
        d['bottom'] = die['east']
        d['west'] = die['bottom']
    elif direction == 'west':
        d['top'] = die['east']
        d['west'] = die['top']
        d['bottom'] = die['west']
        d['east'] = die['bottom']
    elif direction == 'north':
        d['top'] = die['south']
        d['north'] = die['top']
        d['bottom'] = die['north']
        d['south'] = die['bottom']
    elif direction == 'south':
        d['top'] = die['north']
        d['south'] = die['top']
        d['bottom'] = die['south']
        d['north'] = die['bottom']
    # 整合性チェック: 対面の和は7
    assert d['top'] + d['bottom'] == 7
    assert d['north'] + d['south'] == 7
    assert d['east'] + d['west'] == 7
    return d


def solve(initial, sequence):
    die = dict(initial)
    print(f"初期: {die}")
    for i, direction in enumerate(sequence, 1):
        die = roll(die, direction)
        print(f"  {i}回目 {direction}: top={die['top']}, south={die['south']}, east={die['east']}")
    return die


print("=" * 60)
print("問1: 東・北・東・南")
print("=" * 60)
initial = {'top':1, 'bottom':6, 'south':2, 'north':5, 'east':3, 'west':4}
result1 = solve(initial, ['east','north','east','south'])
print(f"\n問1答え: 上面 = {result1['top']}")

print()
print("=" * 60)
print("問2: 東・東・北・西・南・南・東")
print("=" * 60)
result2 = solve(initial, ['east','east','north','west','south','south','east'])
print(f"\n問2答え: (上面, 東面) = ({result2['top']}, {result2['east']})")


# 解の一意性: 初期向きが標準サイコロ（上1・南2・東3）に固定されているため、
# 転がし操作も決定論的であり、解は一意に定まる（手順は1通り）
print()
print("検証: 標準サイコロ初期配置(top=1,south=2,east=3)は1通りに決まる")
print("       転がし操作も1通りで、最終状態も1通りに定まる ✓")
