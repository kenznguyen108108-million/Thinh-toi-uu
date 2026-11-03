# Vong 8 (30/10/2026): luat BAN rieng cho dot giam manh tren D1: vao o nen dao chieu gan dinh, gong dai.
# Chay: python3 -I ban_d1.py <d1.json Binance truoc 2025> <m5.csv Binance 2025->
import sys,json,csv,datetime as dt
D={}
for r in json.load(open(sys.argv[1])): D[r[0]//86400000]=[float(r[1]),float(r[2]),float(r[3]),float(r[4])]
for r in csv.reader(open(sys.argv[2])):
  d=int(r[0])//86400000; o,h,l,c=map(float,r[1:5])
  if d not in D: D[d]=[o,h,l,c]
  else: D[d][1]=max(D[d][1],h); D[d][2]=min(D[d][2],l); D[d][3]=c
K=sorted(D); O=[D[k][0] for k in K]; H=[D[k][1] for k in K]; L=[D[k][2] for k in K]; C=[D[k][3] for k in K]; N=len(K)
day=lambda i: dt.datetime.utcfromtimestamp(K[i]*86400).strftime('%Y-%m-%d')
def ema(x,p):
  o=[x[0]]; a=2/(p+1)
  for v in x[1:]: o.append(o[-1]+a*(v-o[-1]))
  return o
E10,E20,E50,E200=ema(C,10),ema(C,20),ema(C,50),ema(C,200)
TR=[H[0]-L[0]]+[max(H[i]-L[i],abs(H[i]-C[i-1]),abs(L[i]-C[i-1])) for i in range(1,N)]
ATR=[sum(TR[max(0,i-13):i+1])/len(TR[max(0,i-13):i+1]) for i in range(N)]
COST=18.0

def tin_hieu(i,kieu):
  if kieu=='engulf':   # nen do nhan chim nen xanh truoc
    return C[i-1]>O[i-1] and C[i]<O[i] and O[i]>=C[i-1] and C[i]<O[i-1]
  if kieu=='engulf_dinh':  # nhan chim + gan dinh 60 ngay (dinh nen hom nay/hom qua la cao nhat)
    return tin_hieu(i,'engulf') and max(H[i],H[i-1])>=max(H[i-60:i+1])
  if kieu=='pha_ema50':    # dong cua thung EMA50 tu tren xuong, EMA50 dang di ngang/xuong
    return C[i]<E50[i] and C[i-1]>=E50[i-1] and E50[i]<=E50[i-5]
  if kieu=='day_thap':     # pha day 20 ngay khi EMA20<EMA50 (xu huong giam da xac nhan)
    return C[i]<min(L[i-20:i]) and E20[i]<E50[i]
  if kieu=='hoi_ema20':    # da giam (E20<E50), hoi len cham EMA20 roi dong nen do
    return E20[i]<E50[i] and H[i]>=E20[i] and C[i]<O[i] and C[i]<E20[i]

def ra(i,sl,cach,R):
  # gong: SL dau = tren dinh nen tin hieu; sau do keo theo cach chon; tra (R, ngay ra, so ngay)
  for j in range(i+1,N):
    if H[j]>=sl: return (C[i]-sl-COST)/R, j
    if cach=='dinh10': sl=min(sl,max(H[j-9:j+1]))
    elif cach=='dinh20': sl=min(sl,max(H[j-19:j+1]))
    elif cach=='atr3': sl=min(sl,L[j]+3*ATR[j]) if j-i>=1 else sl
    elif cach=='ema20':
      if C[j]>E20[j]: return (C[i]-C[j]-COST)/R, j
  return (C[i]-C[N-1]-COST)/R, N-1

def chay(kieu,cach,loc=None,tu='2018-01-01'):
  res=[]; ban_toi=-1; t0=dt.datetime.strptime(tu,'%Y-%m-%d').timestamp()/86400
  for i in range(210,N-1):
    if K[i]<t0 or i<=ban_toi or not tin_hieu(i,kieu): continue
    if loc=='duoi200' and not C[i]<E200[i]: continue
    if loc=='tren200' and not C[i]>E200[i]: continue
    sl=max(H[i],H[i-1])+0.1*ATR[i]; R=sl-C[i]
    if R<=0: continue
    r,j=ra(i,sl,cach,R); res.append((r,i,j)); ban_toi=j
  return res

def tom(ten,res):
  if not res: print(f"{ten:38s} 0 lenh"); return
  R=[x[0] for x in res]; w=sum(1 for x in R if x>0)
  eq=pk=dd=0
  for x in R: eq+=x; pk=max(pk,eq); dd=max(dd,pk-eq)
  giu=sum(x[2]-x[1] for x in res)/len(res)
  best=max(res); print(f"{ten:38s} {len(R):3d} lenh thang {100*w/len(R):3.0f}% TB {sum(R)/len(R):+.2f}R tong {sum(R):+6.1f}R sut {dd:4.1f}R giu TB {giu:4.1f} ngay | tot nhat {day(best[1])} {best[0]:+.1f}R")

print(f"Du lieu D1 {day(0)} -> {day(N-1)}, phi ${COST:.0f}, SL tren dinh 2 nen + 0.1ATR")
for kieu in ('engulf','engulf_dinh','pha_ema50','day_thap','hoi_ema20'):
  for cach in ('dinh10','dinh20','atr3','ema20'):
    tom(f"{kieu} / gong {cach}",chay(kieu,cach))
print("--- chi tu 2025 (giai doan gan day) ---")
for kieu in ('engulf_dinh','pha_ema50','day_thap','hoi_ema20'):
  for cach in ('dinh20','atr3'):
    tom(f"{kieu} / gong {cach}",chay(kieu,cach,tu='2025-01-01'))
print("--- lenh engulf_dinh tu 2025 (gong dinh20) ---")
for r,i,j in chay('engulf_dinh','dinh20',tu='2025-01-01'):
  print(f"  ban {day(i)} gia {C[i]:7.0f} -> ra {day(j)} gia {C[j]:7.0f}  {r:+.1f}R  ({j-i} ngay)")
