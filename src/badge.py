import os, re, math
P=open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand/wordmark_path.txt')).read()
P=re.sub(r'(\d+\.\d)\d',r'\1',P)
VB=open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand/wordmark_vb.txt')).read()
W={'C':.72,'A':.74,'R':.69,'P':.65,'E':.60,'T':.62,'U':.72,'H':.75,'O':.80,'L':.56,'S':.64,'Y':.66,'F':.58,'·':.30,' ':.26,'1':.50,'9':.62,'7':.58,'.':.28}
FF="'Plus Jakarta Sans', Arial, sans-serif"
def arc(text, r, fs, ls, top):
    adv=[W[c]*fs+ls for c in text]; total=sum(adv)-ls
    out=[]; s=0
    for c,a in zip(text,adv):
        mid=s+(a-ls)/2; s+=a
        if c==' ': continue
        if top:
            th=math.radians(-90)-total/(2*r)+mid/r; rot=math.degrees(th)+90
        else:
            th=math.radians(90)+total/(2*r)-mid/r; rot=math.degrees(th)-90
        x=900+r*math.cos(th); y=900+r*math.sin(th)
        out.append(f'<text x="{x:.1f}" y="{y:.1f}" transform="rotate({rot:.2f} {x:.1f} {y:.1f})" text-anchor="middle">{c}</text>')
    return f'<g fill="#FFFFFF" font-family="{FF}" font-weight="700" font-size="{fs}">'+''.join(out)+'</g>'
def badge(size, standalone=False):
    ns=' xmlns="http://www.w3.org/2000/svg"' if standalone else ''
    return (f'<svg{ns} viewBox="0 0 1800 1800" role="img" aria-label="Syl’s Cleaning: carpet, upholstery, floors. Established 1977" style="width: {size}px; height: {size}px; display: block">'
      '<circle cx="900" cy="900" r="900" fill="#2A4C9E"></circle>'
      '<circle cx="900" cy="900" r="855" fill="none" stroke="#FFFFFF" stroke-width="8"></circle>'
      '<circle cx="225" cy="900" r="18" fill="#FFFFFF"></circle><circle cx="1575" cy="900" r="18" fill="#FFFFFF"></circle>'
      + arc('CARPET · UPHOLSTERY · FLOORS',650,88,4,True)
      + arc('EST. 1977',600+125,150,46,False) +
      f'<svg x="512" y="505" width="776" height="530" viewBox="{VB}"><path fill="#FFFFFF" fill-rule="evenodd" d="{P}"></path></svg>'
      f'<text x="920" y="1215" fill="#FFFFFF" font-family="{FF}" font-weight="800" font-size="128" letter-spacing="40" text-anchor="middle">CLEANING</text>'
      '</svg>')
def mark(h):
    return f'<svg viewBox="{VB}" role="img" aria-label="Syl’s" style="height: {h}px; width: auto; display: block"><path fill="#2A4C9E" fill-rule="evenodd" d="{P}"></path></svg>'
