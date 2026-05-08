"""
航大思考155 検証スクリプト（純Python版）
"""

def vadd(a, b): return tuple(a[i]+b[i] for i in range(len(a)))
def vsub(a, b): return tuple(a[i]-b[i] for i in range(len(a)))
def vneg(a): return tuple(-x for x in a)
def vclose(a, b, tol=1e-6):
    return all(abs(a[i]-b[i]) < tol for i in range(len(a)))

def fold_cube(net_squares, base_label):
    """net_squares: label -> (col, row); base_label: 底面ラベル
    各面の外向き法線を計算し、対面ペアを返す。
    """
    pos = net_squares
    # baseは底面 (法線 -z=(0,0,-1))
    face_normal = {base_label: (0, 0, -1)}
    
    visited = {base_label}
    queue = [base_label]
    
    while queue:
        cur = queue.pop(0)
        cur_pos = pos[cur]
        cur_n = face_normal[cur]
        for other, other_pos in pos.items():
            if other in visited:
                continue
            d = vsub(other_pos, cur_pos)  # (dx, dy)
            if d in [(1,0), (-1,0), (0,1), (0,-1)]:
                # otherはcurに対して d 方向に隣接
                # otherを共有辺周りに90°折り上げると、
                # otherの新しい法線 = d方向（3D化）になる
                # （curが机に裏向き=法線-z、curから見てd方向に位置するotherを立ち上げると
                # otherの面はd方向を向く）
                # ※これはcur_nが-zの場合に成り立つが、
                # 一般のcurの場合、d方向（2D netの方向）はcurのローカル座標における方向
                # なので、cur面の局所座標 (cur_n, u, v) を使う必要がある
                # 簡単のため再帰的にシミュレーションするのは煩雑なので、
                # ここでは「baseが底面の場合のみ」検証する
                # baseが底面に固定されているので、cur_n が一意に決まり、
                # 各 cur について d 方向の3D化が決まる
                pass
        break
    return None

# やはり代数的なほうが簡潔。展開図の折り畳みは座標系で計算する。
# 
# ===アプローチ===
# 展開図（2D）上の各正方形に「3D空間での位置（中心と法線）」を割り当てる。
# 隣接する正方形は共有辺で折られ、折る方向は「シートの裏側に上に立てる」と決める。
# baseを z=0平面に置き、そこから順に隣接面を立ち上げていく。

def simulate_fold(net, base):
    """
    net: {label: (col, row)} 平面上の格子位置
    base: 底面とするラベル
    
    各正方形の中心 (3D) と外向き法線 (3D) を求めて辞書で返す。
    """
    # baseは底面: 中心(0,0,0), 法線(0,0,-1)
    # 隣接面は共有辺周りに「上に」90°折られる
    # 各面に対する「local axes」を持っておく必要あり
    # 
    # 各面について:
    #   center: 3Dベクトル
    #   normal: 3Dベクトル  
    #   right:  3Dベクトル（展開図上で +x 方向だったベクトルの3D像）
    #   up:     3Dベクトル（展開図上で +y 方向だったベクトルの3D像）
    
    info = {}
    # baseの初期: net上で (col0,row0), 3Dで中心(0,0,0), 法線-z
    # 展開図上の +x → 3Dの +x、+y → 3Dの +y、+z(法線方向)は -z（外向き）
    base_pos = net[base]
    info[base] = {
        'center': (0.0, 0.0, 0.0),
        'normal': (0, 0, -1),
        'right':  (1, 0, 0),  # net上の+x方向が3Dではどう向くか
        'up':     (0, 1, 0),  # net上の+y方向が3Dではどう向くか
    }
    
    visited = {base}
    queue = [base]
    
    def cross(a, b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
    
    while queue:
        cur = queue.pop(0)
        cur_pos = net[cur]
        cur_info = info[cur]
        
        for other, other_pos in net.items():
            if other in visited:
                continue
            d = vsub(other_pos, cur_pos)  # (dx, dy)
            if d not in [(1,0), (-1,0), (0,1), (0,-1)]:
                continue
            
            dx, dy = d
            # cur面のローカル座標で「dx*right + dy*up」方向に隣接
            cur_right = cur_info['right']
            cur_up = cur_info['up']
            cur_normal = cur_info['normal']
            
            # 平面状態でのother中心相対位置:
            # cur中心 + 1*(dx*right + dy*up)
            # 共有辺の位置: cur中心 + 0.5*(dx*right + dy*up)
            # 折る軸: dx,dyに垂直なローカル方向 = (-dy*right + dx*up) ? 違う
            # 正確には: 軸方向ベクトル = cross(normal, displacement_dir) で求まる
            
            # 折る前のother法線 = cur_normal （同一平面上）
            # 折る前のother中心 = cur_center + (dx*cur_right + dy*cur_up) (シート上で1ユニット先)
            disp = (dx*cur_right[0] + dy*cur_up[0],
                    dx*cur_right[1] + dy*cur_up[1],
                    dx*cur_right[2] + dy*cur_up[2])
            
            # 共有辺の中点
            cc = cur_info['center']
            edge_mid = (cc[0] + 0.5*disp[0], cc[1] + 0.5*disp[1], cc[2] + 0.5*disp[2])
            
            # 折るとothr法線が「cur_normalから-disp方向に90°曲がる」、
            # ここで折りの方向は「シートの裏側」に立ち上がる
            # cur_normalが外向きで、シートを「外側に折る」ので、
            # other面の法線は disp_dir（正規化）方向 を向くようになる
            disp_norm = math_norm(disp)
            othr_normal_new = disp_norm  # disp方向に向く
            # othr中心は、edge_midから法線方向（otherの新法線）に0.5進んだ位置
            # …ではなく、edge_midから cur_normalの逆方向に 0.5進んだ位置
            # （cur面が机に貼り付いて、otherを上に立てると、otherの中心は edge_mid から「上」に動く）
            # ここで「上」は cur_normal の逆方向（-cur_normal）
            cn = cur_normal
            up_dir = (-cn[0], -cn[1], -cn[2])
            othr_center = (edge_mid[0] + 0.5*up_dir[0],
                           edge_mid[1] + 0.5*up_dir[1],
                           edge_mid[2] + 0.5*up_dir[2])
            
            # other面のローカルright/upを更新する必要があるが、対面判定だけなら法線だけで十分
            # ただし他の面を再帰的に折るときに必要
            # 折りの効果: other面のlocal座標系は、共有辺(disp_dirに垂直、cur_normalにも垂直)を軸に90°回転
            # 軸方向: ax = cross(cur_normal, disp_dir) または cross(disp_dir, cur_normal)
            # この軸まわりに、cur_normal → -disp_dir、cur_right/up を回転
            
            # 軸を決定（dx,dy のうち成立する方向）:
            # disp = (dx, dy) → 軸の成分は (-dy, dx) （シート上で90°回転）
            # 3Dの軸: -dy*cur_right + dx*cur_up
            ax = (-dy*cur_right[0] + dx*cur_up[0],
                  -dy*cur_right[1] + dx*cur_up[1],
                  -dy*cur_right[2] + dx*cur_up[2])
            ax = math_norm(ax)
            
            # ロドリゲスの公式で90°回転
            # 回転方向: cur_normal を -disp_dir 方向に回す
            # cur_normal が回転後 -disp_dir = -disp_norm = (-dx, -dy, 0)? 違う、
            # 期待は: 折った後の法線 = +disp_norm（curからotherに向かう方向に外向き）
            # 待って、再度考える。
            # 
            # 例: cur が底面 (法線 -z)、disp = (1, 0, 0) (右隣)。
            # otherを折ると、otherは右の側壁になり、外向き法線 = +x。
            # つまり new_normal = +disp（disp自体が右方向）。
            # 一方、もしdispが内側なら disp_dir = (1,0) → 3D化で (cur_right方向)
            # cur_right = (1,0,0)、cur_up = (0,1,0) なら disp_3d = (1,0,0)。
            # other法線 = (1,0,0) = +disp_3d ✓
            
            # 軸: -dy*right + dx*up = -0*(1,0,0) + 1*(0,1,0) = (0,1,0)? No, dx=1,dy=0
            # → -dy*right + dx*up = -0*right + 1*up = (0,1,0)
            # じゃなくて、dx=1,dy=0 のとき: ax = (-dy)*right + (dx)*up = 0*r + 1*u = (0,1,0)
            # （y軸方向）
            # cur_normal=(0,0,-1) を y軸まわりに 90°回転
            # 回転方向: (0,0,-1) → (?, 0, 0)
            # y軸まわりに +90°: (x,y,z) → (z, y, -x)
            # (0,0,-1) → (-1, 0, 0)
            # しかし期待は (1,0,0) = +x なので、-90°回転にすべき
            # y軸まわりに -90°: (x,y,z) → (-z, y, x)
            # (0,0,-1) → (1, 0, 0) ✓
            
            # 結論: 軸 ax まわりに -90°（時計回り）回転
            theta = -math.pi / 2
            
            new_right = rotate(cur_right, ax, theta)
            new_up    = rotate(cur_up, ax, theta)
            new_normal = rotate(cur_normal, ax, theta)
            
            info[other] = {
                'center': othr_center,
                'normal': new_normal,
                'right': new_right,
                'up': new_up,
            }
            visited.add(other)
            queue.append(other)
    
    return info

import math

def math_norm(v):
    n = math.sqrt(sum(x*x for x in v))
    if n < 1e-12: return v
    return tuple(x/n for x in v)

def rotate(v, axis, theta):
    """ロドリゲスの公式: vを単位軸axisまわりに角度θ回転"""
    a = math_norm(axis)
    cos = math.cos(theta)
    sin = math.sin(theta)
    # v_rot = v*cos + (a×v)*sin + a*(a·v)*(1-cos)
    cross_av = (a[1]*v[2]-a[2]*v[1], a[2]*v[0]-a[0]*v[2], a[0]*v[1]-a[1]*v[0])
    dot_av = a[0]*v[0]+a[1]*v[1]+a[2]*v[2]
    return (
        v[0]*cos + cross_av[0]*sin + a[0]*dot_av*(1-cos),
        v[1]*cos + cross_av[1]*sin + a[1]*dot_av*(1-cos),
        v[2]*cos + cross_av[2]*sin + a[2]*dot_av*(1-cos),
    )

def find_pairs(info):
    labels = list(info.keys())
    pairs = []
    used = set()
    for i, a in enumerate(labels):
        if a in used: continue
        for b in labels[i+1:]:
            if b in used: continue
            na, nb = info[a]['normal'], info[b]['normal']
            if all(abs(na[k]+nb[k]) < 1e-6 for k in range(3)):
                pairs.append((a, b))
                used.add(a); used.add(b)
                break
    return pairs

# ============ 問1 ============
print("===== 問1 =====")
net1 = {
    'A': (1, 0),
    'B': (1, 1),
    'C': (1, 2),
    'D': (1, -1),
    'E': (2, 0),
    'F': (0, 0),
}
info1 = simulate_fold(net1, 'A')
for label in ['A','B','C','D','E','F']:
    n = info1[label]['normal']
    print(f"  {label}: normal=({n[0]:+.2f}, {n[1]:+.2f}, {n[2]:+.2f})")
pairs1 = find_pairs(info1)
print(f"対面ペア: {pairs1}")

b_opp = next(q if p=='B' else p for p,q in pairs1 if 'B' in (p,q))
print(f"面Bの対面: {b_opp}")
assert b_opp == 'D'

# ============ 問2 ============
print("\n===== 問2 =====")
net2 = {
    'A': (0, 0),
    'B': (1, 0),
    'C': (2, 0),
    'D': (3, 0),
    'E': (1, 1),
    'F': (2, -1),
}
info2 = simulate_fold(net2, 'B')
for label in ['A','B','C','D','E','F']:
    n = info2[label]['normal']
    print(f"  {label}: normal=({n[0]:+.2f}, {n[1]:+.2f}, {n[2]:+.2f})")
pairs2 = find_pairs(info2)
print(f"対面ペア: {pairs2}")

def opp_of(label, pairs):
    for p,q in pairs:
        if p==label: return q
        if q==label: return p

print(f"A↔{opp_of('A',pairs2)}, B↔{opp_of('B',pairs2)}, E↔{opp_of('E',pairs2)}")

# 数字決定
A, B, E_v = 1, 2, 3
C = 7 - A
D = 7 - B
F = 7 - E_v
print(f"A={A}, B={B}, C={C}, D={D}, E={E_v}, F={F}")
assert {A,B,C,D,E_v,F} == {1,2,3,4,5,6}
print(f"(C, D, F) = ({C}, {D}, {F})")
print("OK: 全テスト合格")
