import sys,datetime,warnings; warnings.filterwarnings('ignore'); sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1])
CUT=datetime.datetime(2026,7,25).timestamp(); COST=16.0
def fmt(t): return datetime.datetime.utcfromtimestamp(t).strftime('%y-%m-%d %H:%M')
D=agg(T,O,H,L,C,86400); dC=[b[4] for b in D]
dS=[sum(dC[max(0,i-49):i+1])/len(dC[max(0,i-49):i+1]) for i in range(len(dC))]; dmap={b[0]:i for i,b in enumerate(D)}
def d1(t):
  i=dmap.get(t//86400*86400,0)-1
  return 0 if i<0 else (1 if dC[i]>dS[i] else -1)
def structure(Bh,kh):
  # tra ve ham t -> +1/-1/0 theo cau truc dinh/day khung lon da xac nhan truoc t
  P=pivots(Bh,kh); ev=sorted(((Bh[i+kh][0],t,p) for i,t,p in P if i+kh<len(Bh)))
  import bisect; times=[e[0] for e in ev]; st=[];hs=[];ls=[]
  for _,t,p in ev:
    (hs if t=='H' else ls).append(p)
    s=0
    if len(hs)>1 and len(ls)>1:
      if hs[-1]>hs[-2] and ls[-1]>ls[-2]: s=1
      elif hs[-1]<hs[-2] and ls[-1]<ls[-2]: s=-1
    st.append(s)
  def f(t):
    i=bisect.bisect_right(times,t)-1
    return st[i] if i>=0 else 0
  return f
def run(B,k,side,mode,rr,flt):
  P=pivots(B,k); conf={}
  for i,t,p in P: conf.setdefault(i+k,[]).append((i,t,p))
  hs=[];ls=[];res=[];pos=None;used=set()
  for j in range(len(B)):
    for x in conf.get(j,[]): (hs if x[1]=='H' else ls).append(x)
    if pos is not None:
      for m in range(B[j-1][5]+1,B[j][5]+1):
        s=pos['s']
        if (H[m]>=pos['sl'] if s<0 else L[m]<=pos['sl']):
          res.append((((pos['sl']-pos['e'])*s-COST)/pos['r'],pos['t'])); pos=None; break
        if mode=='rr' and (L[m]<=pos['tp'] if s<0 else H[m]>=pos['tp']):
          res.append(((rr*pos['r']-COST)/pos['r'],pos['t'])); pos=None; break
      if pos is not None and mode=='keo':
        if pos['s']<0 and hs and hs[-1][0]>pos['j'] and hs[-1][2]<pos['sl']: pos['sl']=hs[-1][2]
        if pos['s']>0 and ls and ls[-1][0]>pos['j'] and ls[-1][2]>pos['sl']: pos['sl']=ls[-1][2]
      if pos is not None: continue
    if len(hs)<2 or len(ls)<2: continue
    c=B[j][4]
    if side<0:
      h1,h2,lo=hs[-2],hs[-1],ls[-1]; ok=h2[2]<h1[2] and h2[0]<lo[0] and c<lo[2] and lo[0] not in used; key=lo[0]; sl=h2[2]
    else:
      l1,l2,hi=ls[-2],ls[-1],hs[-1]; ok=l2[2]>l1[2] and l2[0]<hi[0] and c>hi[2] and hi[0] not in used; key=hi[0]; sl=l2[2]
    if not ok: continue
    used.add(key)
    if flt and not flt(B[j][0],side): continue
    r=abs(c-sl)
    if r<=COST*2: continue
    pos={'e':c,'sl':sl,'tp':c+side*rr*r,'s':side,'j':j,'r':r,'t':B[j][0]}
  return res
def show(name,res):
  res.sort(key=lambda x:x[1])
  a=[r for r,t in res if t<CUT]; b=[r for r,t in res if t>=CUT]
  rep(name+' |HL',a); rep(name+' |KT',b)

def rng(B,N,wmax,mode,rr,flt,slmode):
  res=[];pos=None;j=N
  while j<len(B):
    if pos is not None:
      for m in range(B[j-1][5]+1,B[j][5]+1):
        sd=pos['s']
        if (H[m]>=pos['sl'] if sd<0 else L[m]<=pos['sl']): res.append((((pos['sl']-pos['e'])*sd-COST)/pos['r'],pos['t'])); pos=None; break
        if mode=='rr' and (L[m]<=pos['tp'] if sd<0 else H[m]>=pos['tp']): res.append(((rr*pos['r']-COST)/pos['r'],pos['t'])); pos=None; break
      if pos is not None and mode=='keo':  # keo theo day/dinh 12 nen
        w=B[j-11:j+1]
        if pos['s']>0: pos['sl']=max(pos['sl'],min(b[3] for b in w))
        else: pos['sl']=min(pos['sl'],max(b[2] for b in w))
      j+=1
      if pos is not None: continue
      continue
    hi=max(b[2] for b in B[j-N:j]); lo=min(b[3] for b in B[j-N:j]); c=B[j][4]
    if (hi-lo)/c<=wmax:
      sd=1 if c>hi else (-1 if c<lo else 0)
      if sd and (flt is None or flt(B[j][0],sd)):
        sl=(hi+lo)/2 if slmode=='giua' else (lo if sd>0 else hi)
        r=abs(c-sl)
        if r>COST*2: pos={'e':c,'sl':sl,'tp':c+sd*rr*r,'s':sd,'r':r,'t':B[j][0]}
    j+=1
  return res
f=lambda t,s: d1(t)==s
B=agg(T,O,H,L,C,3600)
for N in (24,48):
  for w in (0.02,0.03,0.04):
    for mode,rr in (('rr',2.0),('keo',0)):
      for fn,ff in (('khong loc',None),('D1SMA50',f)):
        show(f"H1 tich luy {N}n <={w*100:.0f}% {mode}{rr if mode=='rr' else ''} {fn}",rng(B,N,w,mode,rr,ff,'giua'))
