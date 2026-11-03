import sys,datetime,warnings; warnings.filterwarnings('ignore'); sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1])
TF=int(sys.argv[3])
B=agg(T,O,H,L,C,TF*3600); D=agg(T,O,H,L,C,86400)
dC=[b[4] for b in D]; dS=[sum(dC[max(0,i-49):i+1])/len(dC[max(0,i-49):i+1]) for i in range(len(dC))]
dmap={b[0]:i for i,b in enumerate(D)}
def d1ctx(t):
  i=dmap.get(t//86400*86400,0)-1
  return 1 if i>=0 and dC[i]>dS[i] else -1
COST=16.0
TS=[]
def fmt(t): return datetime.datetime.utcfromtimestamp(t).strftime('%y-%m-%d %H:%M')
def run(k,side,rr,ctx=None,trail=False,show=False):
  TS.clear()
  P=pivots(B,k); conf={}
  for i,t,p in P: conf.setdefault(i+k,[]).append((i,t,p))
  hs=[];ls=[];res=[];pos=None;used=set()
  for j in range(len(B)):
    for x in conf.get(j,[]): (hs if x[1]=='H' else ls).append(x)
    if pos is not None:
      a=B[j-1][5]+1
      for m in range(a,B[j][5]+1):
        s=pos['s']
        if (H[m]>=pos['sl'] if s<0 else L[m]<=pos['sl']):
          out=((pos['sl']-pos['e'])*s-COST)/pos['r']; res.append(out); TS.append(B[j][0]); pos=None; break
        if not trail and (L[m]<=pos['tp'] if s<0 else H[m]>=pos['tp']):
          out=(rr*pos['r']-COST)/pos['r']; res.append(out); TS.append(B[j][0]); pos=None; break
      if pos is not None and trail:
        if pos['s']<0 and hs and hs[-1][0]>pos['j'] and hs[-1][2]<pos['sl']: pos['sl']=hs[-1][2]
        if pos['s']>0 and ls and ls[-1][0]>pos['j'] and ls[-1][2]>pos['sl']: pos['sl']=ls[-1][2]
      if pos is not None: continue
      if show and res: print('    ->',fmt(B[j][0]),f"{res[-1]:+.2f}R")
    if len(hs)<2 or len(ls)<2: continue
    c=B[j][4]
    if side<0:
      h1,h2,lo=hs[-2],hs[-1],ls[-1]
      ok= h2[2]<h1[2] and h2[0]<lo[0] and c<lo[2] and lo[0] not in used
      key=lo[0]; sl=h2[2]
    else:
      l1,l2,hi=ls[-2],ls[-1],hs[-1]
      ok= l2[2]>l1[2] and l2[0]<hi[0] and c>hi[2] and hi[0] not in used
      key=hi[0]; sl=l2[2]
    if not ok: continue
    used.add(key)
    if ctx is not None and d1ctx(B[j][0])!=ctx: continue
    r=abs(c-sl)
    if r<=COST*2: continue
    pos={'e':c,'sl':sl,'tp':c+side*rr*r,'s':side,'j':j,'r':r}
    if show: print(' ',fmt(B[j][0]),'BAN' if side<0 else 'MUA',round(c),'SL',round(sl))
  return res
import datetime as _d
CUT=_d.datetime(2026,7,25).timestamp()
def split(name,R):
  a=[r for r,t in zip(R,TS) if t<CUT]; b=[r for r,t in zip(R,TS) if t>=CUT]
  rep(name+' | HUAN LUYEN',a); rep(name+' | KIEM TRA',b)
if len(sys.argv)>4 and sys.argv[4]=='split':
  for k,side,rr,tr,ctx in [(3,-1,0,1,None),(5,-1,0,1,None),(5,-1,2,0,None),(3,-1,2,0,None),(5,1,0,1,None),(5,-1,2,0,1)]:
    split(f'H{TF} k={k} {"BAN" if side<0 else "MUA"} '+('keo' if tr else f'{rr}R')+(' D1>SMA' if ctx else ''),run(k,side,rr,ctx=ctx,trail=bool(tr)))
  sys.exit()
if len(sys.argv)>4:
  k,side,rr,tr=int(sys.argv[4]),int(sys.argv[5]),float(sys.argv[6]),sys.argv[7]=='1'
  rep('chi tiet',run(k,side,rr,trail=tr,show=True)); sys.exit()
for k in (3,5,8):
  for rr in (1.5,2.0,3.0):
    rep(f"H{TF} k={k} BAN pha day, an {rr}R",run(k,-1,rr))
    rep(f"H{TF} k={k} BAN {rr}R, chi khi D1>SMA50",run(k,-1,rr,ctx=1))
    rep(f"H{TF} k={k} MUA pha dinh, an {rr}R",run(k,1,rr))
  rep(f"H{TF} k={k} BAN, keo SL theo dinh",run(k,-1,0,trail=True))
  rep(f"H{TF} k={k} MUA, keo SL theo day",run(k,1,0,trail=True))
