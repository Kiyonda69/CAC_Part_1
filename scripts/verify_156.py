"""航大思考156 検証スクリプト"""

# ===== 問1: 4支店四半期別売上 =====
data1 = {
    'A': [124, 156, 188, 212],
    'B': [198, 172, 154, 166],
    'C': [80, 95, 116, 145],
    'D': [168, 174, 186, 192],
}
years = {k: sum(v) for k, v in data1.items()}
quarters = [sum(data1[s][i] for s in 'ABCD') for i in range(4)]

print('=== 問1 ===')
print('年間売上:', years)
print('四半期合計:', quarters)

opts1 = {}
opts1[1] = abs(quarters[0]/4 - 143.5) < 0.05
opts1[2] = abs(quarters[3]/quarters[0] - 1.25) < 0.01
opts1[3] = abs(data1['A'][3]/data1['A'][0] - 1.5) < 0.05
opts1[4] = abs(years['B']/years['C'] - 1.8) < 0.05
opts1[5] = abs(data1['D'][2]/quarters[2] - 0.25) < 0.01

print('Q1平均:', quarters[0]/4)
print('Q4/Q1:', quarters[3]/quarters[0])
print('A Q4/Q1:', data1['A'][3]/data1['A'][0])
print('B年/C年:', years['B']/years['C'])
print('D Q3/全Q3:', data1['D'][2]/quarters[2])

print('選択肢正誤:', opts1)
correct1 = [k for k, v in opts1.items() if v]
print('正解:', correct1)
assert correct1 == [2], f"問1: 正解が一意ではない {correct1}"

# ===== 問2: 3製品月別販売 =====
sales = {
    'P': [120, 145, 168, 192],
    'Q': [200, 175, 160, 145],
    'R': [80, 110, 140, 165],
}
price = {'P': 5000, 'Q': 8000, 'R': 12000}
cost = {'P': 3200, 'Q': 5400, 'R': 8800}
profit_per = {p: price[p]-cost[p] for p in 'PQR'}

print('\n=== 問2 ===')
print('利益/個:', profit_per)

monthly_sales = [sum(sales[p][m]*price[p] for p in 'PQR') for m in range(4)]
monthly_profit = [sum(sales[p][m]*profit_per[p] for p in 'PQR') for m in range(4)]
total_units = {p: sum(sales[p]) for p in 'PQR'}
total_sales = {p: total_units[p]*price[p] for p in 'PQR'}

print('月別売上:', monthly_sales)
print('月別利益:', monthly_profit)
print('製品別売上合計:', total_sales)
print('製品別販売数合計:', total_units)

opts2 = {}
opts2[1] = max(total_sales, key=total_sales.get) == 'Q'
opts2[2] = abs(total_sales['P'] - 3_250_000) < 50_000
opts2[3] = sales['R'][3]*profit_per['R'] / monthly_profit[3] >= 0.5
opts2[4] = abs(monthly_profit[3]/monthly_profit[0] - 1.26) < 0.005
opts2[5] = max(total_units, key=total_units.get) == 'R'

print('最大売上製品:', max(total_sales, key=total_sales.get))
print('Pの合計売上:', total_sales['P'])
print('R 4月利益/全利益:', sales['R'][3]*profit_per['R']/monthly_profit[3])
print('4月利益/1月利益:', monthly_profit[3]/monthly_profit[0])
print('最大販売数製品:', max(total_units, key=total_units.get))

print('選択肢正誤:', opts2)
correct2 = [k for k, v in opts2.items() if v]
print('正解:', correct2)
assert correct2 == [4], f"問2: 正解が一意ではない {correct2}"

print('\n検証OK: 問1=(2), 問2=(4)')
