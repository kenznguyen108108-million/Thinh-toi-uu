import sys; sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1]); n=len(C)
e1=ema(C,12*20); e2=ema(C,12*50)
def run(side, flt=None, minrisk=0, rr=2.0, cost=16.0):
  res=[];i=3
  while i<n-1:
    a,b,c=i-3,i-2,i-1
    ok=all((C[k]>O[k]) if side>0 else (C[k]<O[k]) for k in (a,b,c))
    if ok and (flt is None or flt(c,side)):
      e=C[c]; sl=L[a] if side>0 else H[a]; r=abs(e-sl)
      if r>=max(minrisk,1e-9):
        tp=e+side*rr*r; j=i; out=None
        while j<n:
          if (L[j]<=sl if side>0 else H[j]>=sl): out=-1;break
          if (H[j]>=tp if side>0 else L[j]<=tp): out=rr;break
          j+=1
        if out is None: break
        res.append(out-cost/r); i=j+1; continue
    i+=1
  return res
up=lambda c,s: (e1[c]>e2[c]) if s>0 else (e1[c]<e2[c])
rep("MUA 3 nen tang, KHONG phi (ly thuyet)",run(1,cost=0))
for mr in (0,50,100,200):
  rep(f"MUA 3 nen tang, risk>={mr}$",run(1,minrisk=mr))
  rep(f"MUA 3 nen + H1 tang, risk>={mr}$",run(1,up,minrisk=mr))
  rep(f"BAN 3 nen giam + H1 giam, risk>={mr}$",run(-1,up,minrisk=mr))
print('--- doi ti le an')
for rr in (1.0,1.5,3.0):
  rep(f"MUA 3 nen + H1 tang, an {rr}R, khong phi",run(1,up,rr=rr,cost=0))
  rep(f"MUA 3 nen + H1 tang, an {rr}R, co phi",run(1,up,rr=rr,minrisk=100))
