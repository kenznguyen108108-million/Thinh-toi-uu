# Vong 18 (03/11/2026): he thong Bollinger tren ETH. 3 kieu: A hoi ve (cham dai ngoai roi quay vao),
# B pha vo sau co that (squeeze), C theo xu huong (gia tren/duoi EMA200, hoi ve dai giua/dai trong roi bat lai).
# Chay: python3 -I bb_eth.py <eth15.csv> <thu muc scripts>
import sys,datetime as dt,math; sys.path.insert(0,sys.argv[2])
from lib import load,agg
T,O,H,L,C=load(sys.argv[1])
PHI=0.0006   # phi + spread khu hoi ~0.06% gia
def chuan_bi(sec):
  B=agg(T,O,H,L,C,sec); n=len(B)
  t=[b[0] for b in B]; o=[b[1] for b in B]; h=[b[2] for b in B]; l=[b[3] for b in B]; c=[b[4] for b in B]
  mid=[None]*n; up=[None]*n; dn=[None]*n; bw=[None]*n
  for i in range(19,n):
    w=c[i-19:i+1]; m=sum(w)/20; sd=math.sqrt(sum((x-m)**2 for x in w)/20)
    mid[i]=m; up[i]=m+2*sd; dn[i]=m-2*sd; bw[i]=(4*sd)/m
  e200=[c[0]]; a=2/201
  for x in c[1:]: e200.append(e200[-1]+a*(x-e200[-1]))
  tr=[h[0]-l[0]]+[max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1])) for i in range(1,n)]
  atr=[sum(tr[max(0,i-13):i+1])/len(tr[max(0,i-13):i+1]) for i in range(n)]
  return dict(n=n,t=t,o=o,h=h,l=l,c=c,mid=mid,up=up,dn=dn,bw=bw,e200=e200,atr=atr)

def mo(d,i,huong,sl,thoat,tp=None):
  # vao o gia dong nen i; tra (R, nen ra)
  c,h,l,mid=d['c'],d['h'],d['l'],d['mid']; e=c[i]; R=abs(e-sl)
  if R<=0: return None
  s=sl; best=e
  for j in range(i+1,d['n']):
    if huong>0:
      if l[j]<=s: return ((s-e)-PHI*e)/R,j
      if tp and h[j]>=tp: return ((tp-e)-PHI*e)/R,j
      best=max(best,h[j])
      if thoat=='giua' and c[j]<mid[j]: return ((c[j]-e)-PHI*e)/R,j
      if thoat=='khoa' and (best-e)>=2*R: s=max(s,e+0.5*(best-e))
    else:
      if h[j]>=s: return ((e-s)-PHI*e)/R,j
      if tp and l[j]<=tp: return ((e-tp)-PHI*e)/R,j
      best=min(best,l[j])
      if thoat=='giua' and c[j]>mid[j]: return ((e-c[j])-PHI*e)/R,j
      if thoat=='khoa' and (e-best)>=2*R: s=min(s,e-0.5*(e-best))
  return ((c[-1]-e)*huong-PHI*e)/R,d['n']-1

def chay(d,kieu,thoat,loc=True):
  c,h,l,o=d['c'],d['h'],d['l'],d['o']; mid,up,dn,bw,e2,atr=d['mid'],d['up'],d['dn'],d['bw'],d['e200'],d['atr']
  res=[]; ban=-1
  for i in range(220,d['n']-1):
    if i<=ban: continue
    sig=0
    if kieu=='A':   # cham dai ngoai roi dong lai trong dai
      if c[i-1]<dn[i-1] and c[i]>dn[i] and c[i]>o[i] and (not loc or c[i]>e2[i]): sig=1
      if c[i-1]>up[i-1] and c[i]<up[i] and c[i]<o[i] and (not loc or c[i]<e2[i]): sig=-1
      if sig: sl=(min(l[i-1],l[i])-0.2*atr[i]) if sig>0 else (max(h[i-1],h[i])+0.2*atr[i]); tp=mid[i] if thoat=='tp_giua' else None
    elif kieu=='B': # co that: do rong dai thap nhat 100 nen trong 5 nen gan, roi dong ngoai dai
      co=min(bw[i-5:i])<=min(x for x in bw[i-100:i] if x)*1.05
      if co and c[i]>up[i] and (not loc or c[i]>e2[i]): sig=1
      if co and c[i]<dn[i] and (not loc or c[i]<e2[i]): sig=-1
      if sig: sl=mid[i]; tp=None
    elif kieu=='C': # xu huong: tren EMA200 + EMA200 di len, gia cham dai giua/duoi roi nen xanh dong tren dai giua
      if c[i]>e2[i] and e2[i]>e2[i-20] and min(l[i-3:i+1])<=mid[i] and c[i]>mid[i] and c[i]>o[i] and c[i-1]<=mid[i-1]: sig=1
      if c[i]<e2[i] and e2[i]<e2[i-20] and max(h[i-3:i+1])>=mid[i] and c[i]<mid[i] and c[i]<o[i] and c[i-1]>=mid[i-1]: sig=-1
      if sig: sl=(min(l[i-5:i+1])-0.2*atr[i]) if sig>0 else (max(h[i-5:i+1])+0.2*atr[i]); tp=None
    if not sig: continue
    th='giua' if thoat=='giua' else ('khoa' if thoat=='khoa' else None)
    r=mo(d,i,sig,sl,th,tp if kieu=='A' else None)
    if r: res.append((r[0],i,sig)); ban=r[1]
  return res

def tom(ten,res,d):
  cuoi=d['t'][-1]; m6=cuoi-183*86400; m3=cuoi-92*86400
  out=[]
  for nm,R in (('18T',res),('6T',[x for x in res if d['t'][x[1]]>=m6]),('3T',[x for x in res if d['t'][x[1]]>=m3])):
    v=[x[0] for x in R]
    if not v: out.append(f"{nm}:  0 lenh"); continue
    eq=pk=dd=0
    for x in v: eq+=x;pk=max(pk,eq);dd=max(dd,pk-eq)
    out.append(f"{nm}:{len(v):4d}L {100*sum(1 for x in v if x>0)/len(v):3.0f}% {sum(v):+6.1f}R sut{dd:5.1f}")
  print(f"{ten:30s} | "+" | ".join(out))

print("ETH Binance 05/2025 -> 11/2026, phi 0.06%. 18T = toan bo, 6T/3T = gan day")
for ten,sec in (('M15',900),('H1',3600),('H4',14400)):
  d=chuan_bi(sec)
  print(f"--- {ten} ({d['n']} nen) ---")
  for kieu,ths in (('A',('tp_giua','khoa')),('B',('giua','khoa')),('C',('giua','khoa'))):
    for th in ths:
      for loc in (True,False):
        tom(f"{ten} {kieu} {th:7s} {'locEMA200' if loc else 'khongLoc'}",chay(d,kieu,th,loc),d)
