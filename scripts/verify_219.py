# -*- coding: utf-8 -*-
"""航大思考219 断面図問題の検証
問1: 立方体(一辺6)を頂点B,D,Eを通る平面で切断 → 断面の形
問2: 立方体の1平面断面として「現れ得ない」形
"""
import itertools, math, random

# 立方体頂点 (一辺6)
A=(0,0,0); B=(6,0,0); C=(6,6,0); D=(0,6,0)
E=(0,0,6); F=(6,0,6); G=(6,6,6); H=(0,6,6)

def dist(p,q):
    return math.sqrt(sum((a-b)**2 for a,b in zip(p,q)))

# ---------- 問1: 断面 BDE ----------
print("=== 問1: 平面 B,D,E による断面 ===")
sBD=dist(B,D); sDE=dist(D,E); sEB=dist(E,B)
print(f"BD={sBD:.4f}, DE={sDE:.4f}, EB={sEB:.4f}")
assert abs(sBD-sDE)<1e-9 and abs(sDE-sEB)<1e-9, "正三角形でない"
print("→ 3辺がすべて等しい = 正三角形。問1正解=(3) 正三角形  [OK]")
print()

# ---------- 問2: 立方体断面に現れる形 ----------
# 平面 a*x+b*y+c*z = d で切断し、断面多角形を求める汎用関数
edges = [(A,B),(B,C),(C,D),(D,A),(E,F),(F,G),(G,H),(H,E),(A,E),(B,F),(C,G),(D,H)]

def section_polygon(n, d):
    """法線n, 切片d の平面 n・x = d による断面頂点群を返す"""
    pts=[]
    nx,ny,nz=n
    for p,q in edges:
        fp=nx*p[0]+ny*p[1]+nz*p[2]-d
        fq=nx*q[0]+ny*q[1]+nz*q[2]-d
        if abs(fp)<1e-9:
            pts.append(p)
        if fp*fq<0:
            t=fp/(fp-fq)
            pts.append(tuple(p[i]+t*(q[i]-p[i]) for i in range(3)))
    # 重複除去
    uniq=[]
    for pt in pts:
        if not any(dist(pt,u)<1e-6 for u in uniq):
            uniq.append(pt)
    return uniq

def order_polygon(pts, n):
    """平面上で頂点を角度順に並べる"""
    if len(pts)<3: return pts
    cx=sum(p[0] for p in pts)/len(pts)
    cy=sum(p[1] for p in pts)/len(pts)
    cz=sum(p[2] for p in pts)/len(pts)
    c=(cx,cy,cz)
    # 平面内基底
    nx,ny,nz=n
    ref=(1,0,0) if abs(nx)<0.9 else (0,1,0)
    u=(ny*ref[2]-nz*ref[1], nz*ref[0]-nx*ref[2], nx*ref[1]-ny*ref[0])
    ul=math.sqrt(sum(x*x for x in u)); u=tuple(x/ul for x in u)
    v=(ny*u[2]-nz*u[1], nz*u[0]-nx*u[2], nx*u[1]-ny*u[0])
    def ang(p):
        dx=p[0]-c[0]; dy=p[1]-c[1]; dz=p[2]-c[2]
        return math.atan2(dx*v[0]+dy*v[1]+dz*v[2], dx*u[0]+dy*u[1]+dz*u[2])
    return sorted(pts, key=ang)

def is_regular(poly):
    n=len(poly)
    sides=[dist(poly[i],poly[(i+1)%n]) for i in range(n)]
    if max(sides)-min(sides)>1e-6: return False
    # 角度チェック
    angs=[]
    for i in range(n):
        a=poly[(i-1)%n]; b=poly[i]; c=poly[(i+1)%n]
        v1=[a[j]-b[j] for j in range(3)]; v2=[c[j]-b[j] for j in range(3)]
        d1=math.sqrt(sum(x*x for x in v1)); d2=math.sqrt(sum(x*x for x in v2))
        cosA=sum(v1[j]*v2[j] for j in range(3))/(d1*d2)
        angs.append(math.acos(max(-1,min(1,cosA))))
    return max(angs)-min(angs)<1e-6

def has_parallel_pair(poly):
    n=len(poly)
    dirs=[]
    for i in range(n):
        v=[poly[(i+1)%n][j]-poly[i][j] for j in range(3)]
        l=math.sqrt(sum(x*x for x in v)); dirs.append([x/l for x in v])
    for i in range(n):
        for j in range(i+1,n):
            cross=[dirs[i][1]*dirs[j][2]-dirs[i][2]*dirs[j][1],
                   dirs[i][2]*dirs[j][0]-dirs[i][0]*dirs[j][2],
                   dirs[i][0]*dirs[j][1]-dirs[i][1]*dirs[j][0]]
            if math.sqrt(sum(x*x for x in cross))<1e-6:
                return True
    return False

print("=== 問2: 各形が断面として現れ得るか ===")
# 正三角形: B,D,E (確認済)
print("正三角形: 平面B,D,Eで実現可能  [可]")
# 正方形: 上下面に平行な平面 z=3
poly=order_polygon(section_polygon((0,0,1),3),(0,0,1))
print(f"正方形: z=3 → 頂点数{len(poly)}, 正多角形={is_regular(poly)}  [可]")
# 正六角形: 対角線AGに垂直な中央平面 x+y+z=9
poly=order_polygon(section_polygon((1,1,1),9),(1,1,1))
print(f"正六角形: x+y+z=9 → 頂点数{len(poly)}, 正多角形={is_regular(poly)}  [可]")
# 台形(等脚台形): わずかに傾けた平面で四角形
poly=order_polygon(section_polygon((0,1,2),9),(0,1,2))
print(f"台形類: y+2z=9 → 頂点数{len(poly)}  [可]")

# 五角形を多数サンプリングし、正五角形が現れないことを確認
print("\n--- 五角形断面のサンプリング (正五角形は出るか?) ---")
random.seed(0)
pent_count=0; regular_pent=0; all_have_parallel=True
for _ in range(200000):
    n=(random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1))
    if sum(x*x for x in n)<0.01: continue
    d=random.uniform(0,18)
    raw=section_polygon(n,d)
    if len(raw)==5:
        poly=order_polygon(raw,n)
        pent_count+=1
        if not has_parallel_pair(poly):
            all_have_parallel=False
        if is_regular(poly):
            regular_pent+=1
print(f"発見した五角形断面: {pent_count}個")
print(f"そのうち正五角形: {regular_pent}個")
print(f"全五角形が平行な辺の組を持つ: {all_have_parallel}")
assert regular_pent==0, "正五角形が見つかった!"
assert all_have_parallel, "平行辺を持たない五角形が存在"
print("→ 立方体の五角形断面は必ず平行な辺を持つ(3組の平行面のうち少なくとも1組を切るため)。")
print("→ 正五角形は平行な辺を持たないので断面として現れ得ない。問2正解=(1) 正五角形  [OK]")
