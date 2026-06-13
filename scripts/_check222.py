# -*- coding: utf-8 -*-
from collections import deque
def roll(state,d):
    U,D,N,S,E,W=state['U'],state['D'],state['N'],state['S'],state['E'],state['W']
    if d=='E': return {'U':W,'E':U,'D':E,'W':D,'N':N,'S':S}
    if d=='W': return {'U':E,'W':U,'D':W,'E':D,'N':N,'S':S}
    if d=='S': return {'U':N,'S':U,'D':S,'N':D,'E':E,'W':W}
    if d=='N': return {'U':S,'N':U,'D':N,'S':D,'E':E,'W':W}
def fold(net):
    cells=list(net.keys())
    # 連結性チェック(4近傍)
    start=cells[0]; seen={start}; q=deque([start])
    while q:
        r,c=q.popleft()
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nb=(r+dr,c+dc)
            if nb in net and nb not in seen: seen.add(nb); q.append(nb)
    if len(seen)!=6: return None,"非連結"
    init={'U':0,'D':1,'N':2,'S':3,'E':4,'W':5}
    paint={}; visited={start}; q=deque([(start,init)])
    while q:
        (r,c),st=q.popleft()
        fid=st['D']
        if fid in paint and paint[fid]!=net[(r,c)]: return None,"面重複(無効ネット)"
        paint[fid]=net[(r,c)]
        for dr,dc,d in [(-1,0,'N'),(1,0,'S'),(0,-1,'W'),(0,1,'E')]:
            nb=(r+dr,c+dc)
            if nb in net and nb not in visited:
                visited.add(nb); q.append((nb,roll(st,d)))
    if len(set(paint.values()))!=6: return None,"6面そろわず"
    o={}
    for a,b in [(0,1),(2,3),(4,5)]:
        o[paint[a]]=paint[b]; o[paint[b]]=paint[a]
    return o,"OK"

nets={
 1:{(0,1):'P',(1,1):'Q',(1,2):'R',(2,2):'S',(2,3):'T',(3,3):'U'},
 2:{(0,0):'P',(0,1):'Q',(1,1):'R',(1,2):'S',(2,2):'T',(2,3):'U'},
 3:{(0,2):'P',(1,0):'Q',(1,1):'R',(1,2):'S',(1,3):'T',(2,2):'U'},
 4:{(0,0):'P',(0,1):'Q',(1,1):'R',(2,1):'S',(2,2):'T',(3,2):'U'},
 5:{(0,1):'P',(0,2):'Q',(1,0):'R',(1,1):'S',(1,2):'T',(2,2):'U'},
}
for k,net in nets.items():
    o,msg=fold(net)
    if o: print(f"net{k}: {msg}  P<->{o['P']} Q<->{o['Q']} R<->{o['R']}  [P-U対面={o['P']=='U'}]")
    else: print(f"net{k}: {msg}")
