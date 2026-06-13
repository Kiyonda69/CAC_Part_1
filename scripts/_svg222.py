# -*- coding: utf-8 -*-
# 展開図SVGを自動生成
def net_svg(cells, cell=46, pad=14, fs=22, label=None):
    rows=[r for r,c in cells]; cols=[c for r,c in cells]
    minr,minc=min(rows),min(cols)
    w=(max(cols)-minc+1)*cell; h=(max(rows)-minr+1)*cell
    extra=24 if label else 0
    W=w+pad*2; H=h+pad*2+extra
    s=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    if label:
        s.append(f'<text x="{W/2:.0f}" y="16" class="svg-text" text-anchor="middle" font-weight="bold">{label}</text>')
    oy=pad+extra
    for (r,c),lab in sorted(cells.items()):
        x=pad+(c-minc)*cell; y=oy+(r-minr)*cell
        s.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="white" stroke="black" stroke-width="2"/>')
        s.append(f'<text x="{x+cell/2:.0f}" y="{y+cell/2+fs/3:.0f}" class="svg-text" text-anchor="middle" font-size="{fs}" font-weight="bold">{lab}</text>')
    s.append('</svg>')
    return '\n'.join(s)

def face_svg(letter,num):
    return ('<svg width="80" height="100" viewBox="0 0 80 100">\n'
            f'<text x="40" y="16" class="svg-text" text-anchor="middle">({num})</text>\n'
            '<rect x="16" y="28" width="48" height="48" fill="white" stroke="black" stroke-width="2"/>\n'
            f'<text x="40" y="60" class="svg-text" text-anchor="middle" font-size="24" font-weight="bold">{letter}</text>\n'
            '</svg>')

# 問1 メインネット
net1={(0,1):'A',(1,0):'B',(1,1):'C',(1,2):'D',(1,3):'E',(2,1):'F'}
open('/tmp/q1_net.svg','w').write(net_svg(net1,cell=54,fs=26))

# 問1 選択肢(面): pos1=A,2=B,3=E(正),4=D,5=F
import json
q1opts=[('A',1),('B',2),('E',3),('D',4),('F',5)]
with open('/tmp/q1_opts.html','w') as f:
    for letter,num in q1opts:
        f.write(f'<button class="option-figure-button" data-option="{num}" onclick="selectAnswer(1, {num}, 3)">\n')
        f.write(face_svg(letter,num)+'\n</button>\n')

# 問2 選択肢ネット: pos5=正解(cross P<->U)
q2nets={
 1:{(0,1):'S',(1,0):'R',(1,1):'P',(1,2):'U',(1,3):'T',(2,2):'Q'},
 2:{(0,0):'R',(0,1):'U',(1,1):'S',(1,2):'P',(2,2):'T',(2,3):'Q'},
 3:{(0,1):'P',(1,0):'U',(1,1):'R',(1,2):'S',(1,3):'Q',(2,1):'T'},
 4:{(0,1):'P',(1,1):'R',(1,2):'U',(1,3):'T',(1,4):'S',(2,1):'Q'},
 5:{(0,1):'Q',(1,0):'U',(1,1):'S',(1,2):'P',(1,3):'T',(2,1):'R'},
}
with open('/tmp/q2_opts.html','w') as f:
    for num in range(1,6):
        f.write(f'<button class="option-figure-button" data-option="{num}" onclick="selectAnswer(2, {num}, 5)">\n')
        f.write(net_svg(q2nets[num],cell=30,fs=16,label=f"({num})")+'\n</button>\n')
print("生成完了")
print("--- q1_net 行数 ---"); print(sum(1 for _ in open('/tmp/q1_net.svg')))
