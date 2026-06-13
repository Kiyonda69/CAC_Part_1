import math

def comp_bearing(dx, dy):
    # compass bearing clockwise from north; dx=east, dy=north
    return math.degrees(math.atan2(dx, dy)) % 360

def rel_bearing(px, py, ox, oy, heading):
    b = comp_bearing(px-ox, py-oy)
    r = (b - heading + 180) % 360 - 180  # (-180,180]
    return r

def order_left_to_right(objs, O, heading, fov=90):
    vis=[]
    for name,(x,y) in objs.items():
        r=rel_bearing(x,y,O[0],O[1],heading)
        if abs(r)<fov-1e-9:
            vis.append((r,name))
    vis.sort()
    return [n for _,n in vis], {n:round(rel_bearing(x,y,O[0],O[1],heading),1) for n,(x,y) in objs.items()}

print("=== 問1: heading 090 (East) ===")
O=(0,0); H=90
objs1={'A':(3,2),'B':(4,-1),'C':(2,1),'D':(5,-2)}
order,rels=order_left_to_right(objs1,O,H)
print("rel bearings:",rels)
print("left->right:", "→".join(order))

print("\n=== 問2: heading 135 (SE) ===")
O2=(0,0); H2=135
objs2={'P':(2,-1),'Q':(1,-3),'R':(3,-3),'S':(1,-1),'T':(-2,2)}
order2,rels2=order_left_to_right(objs2,O2,H2)
print("rel bearings:",rels2)
print("visible left->right:", "→".join(order2))
print("(T should be behind / excluded if |rel|>=90)")
