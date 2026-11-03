# Vong 9 (01/11/2026): mau song ABC tren H4 (y anh): song A giam, song B hoi 50-80%,
# o dinh B co nen nhan chim giam hoac nen rut rau (pin bar) -> BAN an song C.
# Chay: python3 -I abc_h4.py <m5.csv> <thu muc scripts>
import sys,datetime as dt; sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1])
B=agg(T,O,H,L,C,14400); n=len(B)
o=[b[1] for b in B]; h=[b[2] for b in B]; l=[b[3] for b in B]; c=[b[4] for b in B]; t=[b[0] for b in B]
tr=[h[0]-l[0]]+[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,n)]
atr=[sum(tr[max(0,i-13):i+1])/len(tr[max(0,i-13):i+1]) for i in range(n)]
COST=18.0; CUT=dt.datetime(2026,7,25).timestamp()
day=lambda i: dt.datetime.utcfromtimestamp(t[i]).strftime('%Y-%m-%d %H:%M')

def nen_ban(j,kieu):
  eng = c[j-1]>o[j-1] and c[j]<o[j] and o[j]>=c[j-1] and c[j]<o[j-1]
  rng=h[j]-l[j]; body=abs(c[j]-o[j]); rau=h[j]-max(o[j],c[j])
  pin = rng>0 and rau>=2*body and rau>=0.5*rng and (c[j]-l[j])<=0.4*rng
  return eng if kieu=='engulf' else pin if kieu=='pin' else (eng or pin)

def chay(k=5,ahmin=0.04,blo=0.5,bhi=0.8,kieu='ca2',thoat='swing',rr=3.0):
  # dinh/day swing da xac nhan (sau k nen)
  res=[]; da=set(); busy=-1
  piv=[]  # (i_xac_nhan, i, 'H'/'L', gia)
  for i in range(k,n-k):
    if h[i]==max(h[i-k:i+k+1]): piv.append((i+k,i,'H',h[i]))
    if l[i]==min(l[i-k:i+k+1]): piv.append((i+k,i,'L',l[i]))
  piv.sort(); p=0; lastH=None; A=None
  for j in range(k+2,n-1):
    while p<len(piv) and piv[p][0]<=j:
      _,i,tp,v=piv[p]; p+=1
      if tp=='H': lastH=(i,v)
      elif lastH and i>lastH[0] and (lastH[1]-v)/lastH[1]>=ahmin: A=(lastH[0],lastH[1],i,v)   # song A: dinh -> day
    if not A or j<=busy or A in da: continue
    ia,ha,ib,la=A
    if j<=ib: continue
    dA=ha-la; hoi=(h[j]-la)/dA; maxhoi=(max(h[ib+1:j+1])-la)/dA
    if maxhoi>bhi+0.1: da.add(A); continue      # hoi qua sau -> mau hong
    if not (blo<=hoi<=bhi) or not nen_ban(j,kieu): continue
    e=c[j]; sl=max(h[j],h[j-1])+0.1*atr[j]; R=sl-e
    if R<=0: continue
    tp = (e-rr*R) if thoat=='rr' else (max(h[ib+1:j+1])-dA if thoat=='C=A' else None)
    s=sl; r=None
    for q in range(j+1,n):
      if h[q]>=s: r=(e-s-COST)/R; break
      if tp is not None and l[q]<=tp: r=(e-tp-COST)/R; break
      if thoat=='swing' and q-j>=3: s=min(s,max(h[q-9:q+1]))   # keo theo dinh 10 nen H4
    if r is None: q=n-1; r=(e-c[q]-COST)/R
    res.append((r,j,q)); da.add(A); busy=q
  return res

def tom(ten,res):
  if not res: print(f"{ten:44s}   0 lenh"); return
  for nm,R in (('HL',[x for x in res if t[x[1]]<CUT]),('KT',[x for x in res if t[x[1]]>=CUT])):
    v=[x[0] for x in R]
    if not v: print(f"{ten:44s} {nm}   0 lenh"); continue
    eq=pk=dd=0
    for x in v: eq+=x;pk=max(pk,eq);dd=max(dd,pk-eq)
    print(f"{ten:44s} {nm} {len(v):3d} lenh thang {100*sum(1 for x in v if x>0)/len(v):3.0f}% TB {sum(v)/len(v):+.2f}R tong {sum(v):+6.1f}R sut {dd:4.1f}R")

print("H4 Binance 01/2025-10/2026, phi $18. HL = toi 24/07/2026, KT = 25/07-26/10/2026")
for kieu in ('engulf','pin','ca2'):
  for thoat in ('swing','C=A','rr'):
    tom(f"nen {kieu:6s} thoat {thoat}",chay(kieu=kieu,thoat=thoat))
print("--- vung hoi B ---")
for blo,bhi in ((0.382,0.618),(0.5,0.8),(0.6,0.786)):
  tom(f"B {blo}-{bhi} ca2 swing",chay(blo=blo,bhi=bhi))
print("--- song A toi thieu ---")
for a in (0.03,0.05,0.08):
  tom(f"A>={a*100:.0f}% ca2 swing",chay(ahmin=a))
print("--- cac lenh (ca2, swing) ---")
for r,j,q in chay():
  print(f"  {day(j)} ban {c[j]:7.0f} -> {day(q)} {r:+.1f}R")
