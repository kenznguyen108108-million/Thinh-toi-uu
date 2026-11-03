# Vong 4 (28/10/2026): vao lenh M5 theo FVG/OB, loc trung FVG khung lon H1/H4, tach theo giang co / xu huong.
# Chay: python3 -I fvg.py <m5.csv> <thu muc scripts>
import sys,datetime,warnings; warnings.filterwarnings('ignore'); sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1]); T=[t//1000 for t in T]; N=len(T)
CUT=datetime.datetime(2026,7,25).timestamp(); COST=18.0   # spread BTCUSDm ~ $18/BTC
MINR=60.0                                                  # SL toi thieu (gia), tranh SL qua sat

def atr(Hs,Ls,Cs,p=14):
  out=[0.0]*len(Hs); s=0.0
  for i in range(len(Hs)):
    tr=Hs[i]-Ls[i] if i==0 else max(Hs[i]-Ls[i],abs(Hs[i]-Cs[i-1]),abs(Ls[i]-Cs[i-1]))
    s+=tr
    if i>=p: s-=(Hs[i-p]-Ls[i-p]) if i-p==0 else max(Hs[i-p]-Ls[i-p],abs(Hs[i-p]-Cs[i-p-1]),abs(Ls[i-p]-Cs[i-p-1]))
    out[i]=s/min(i+1,p)
  return out
A5=atr(H,L,C)

# ---- vung FVG khung lon: (m5 bat dau hieu luc, m5 het han, huong, lo, hi)
def htf_fvg(sec,life):
  B=agg([t*1000 for t in T],O,H,L,C,sec)
  Bh=[b[2] for b in B]; Bl=[b[3] for b in B]; Bc=[b[4] for b in B]; At=atr(Bh,Bl,Bc)
  Z=[]
  for i in range(2,len(B)-1):
    st=B[i][5]+1
    if Bl[i]>Bh[i-2] and Bl[i]-Bh[i-2]>=0.1*At[i]: Z.append([st,1,Bh[i-2],Bl[i],life])
    if Bh[i]<Bl[i-2] and Bl[i-2]-Bh[i]>=0.1*At[i]: Z.append([st,-1,Bh[i],Bl[i-2],life])
  # tinh m5 het han: bi lap kin (dong cua M5 vuot qua mep xa) hoac qua 'life' nen khung lon
  for z in Z:
    st,d,lo,hi,lf=z; end=min(N,st+lf*sec//300)
    for j in range(st,end):
      if (d>0 and C[j]<lo) or (d<0 and C[j]>hi): end=j; break
    z[4]=end
  return Z
ZH1=htf_fvg(3600,120); ZH4=htf_fvg(14400,60)

def active(Z):
  # mang theo m5: danh sach vung con hieu luc (quet tuyen tinh)
  ev=[[] for _ in range(N+1)]
  for k,z in enumerate(Z): ev[z[0]].append(k)
  return ev
def zones_at(Z,ev):
  cur=set(); out=[None]*N
  for j in range(N):
    for k in ev[j]: cur.add(k)
    if j%1==0:
      dead=[k for k in cur if Z[k][4]<=j]
      for k in dead: cur.discard(k)
    out[j]=tuple(cur)
  return out
AH1=zones_at(ZH1,active(ZH1)); AH4=zones_at(ZH4,active(ZH4))

# ---- che do thi truong D1: ADX14 < 20 = giang co
D=agg([t*1000 for t in T],O,H,L,C,86400)
dH=[b[2] for b in D]; dL=[b[3] for b in D]; dC=[b[4] for b in D]
def adx(Hs,Ls,Cs,p=14):
  n=len(Hs); pdm=[0]*n; mdm=[0]*n; tr=[0]*n
  for i in range(1,n):
    up=Hs[i]-Hs[i-1]; dn=Ls[i-1]-Ls[i]
    pdm[i]=up if up>dn and up>0 else 0; mdm[i]=dn if dn>up and dn>0 else 0
    tr[i]=max(Hs[i]-Ls[i],abs(Hs[i]-Cs[i-1]),abs(Ls[i]-Cs[i-1]))
  a=2/(p+1); s_tr=s_p=s_m=0; dx_s=0; out=[0]*n
  for i in range(1,n):
    s_tr+=a*(tr[i]-s_tr); s_p+=a*(pdm[i]-s_p); s_m+=a*(mdm[i]-s_m)
    pdi=100*s_p/s_tr if s_tr else 0; mdi=100*s_m/s_tr if s_tr else 0
    dx=100*abs(pdi-mdi)/(pdi+mdi) if pdi+mdi else 0
    dx_s+=a*(dx-dx_s); out[i]=dx_s
  return out
dADX=adx(dH,dL,dC); dS=[sum(dC[max(0,i-49):i+1])/len(dC[max(0,i-49):i+1]) for i in range(len(dC))]
dmap={b[0]:i for i,b in enumerate(D)}
def d1_info(t):  # dung nen D1 da dong (hom truoc)
  i=dmap.get(t//86400*86400,0)-1
  if i<0: return 0,0
  return (1 if dADX[i]<20 else 0), (1 if dC[i]>dS[i] else -1)

def trung(Z,act,j,d,px):
  # M5: day/dinh cua mau nam trong vung FVG khung lon cung chieu
  for k in act[j]:
    z=ZH1[k] if Z is ZH1 else ZH4[k]
    if z[1]==d and z[2]<=px<=z[3]: return True
  return False

def sim(e,sl,tp,d,j0):
  for j in range(j0,min(N,j0+288)):
    if d>0:
      if L[j]<=sl: return -1.0,j
      if H[j]>=tp: return None,j
    else:
      if H[j]>=sl: return -1.0,j
      if L[j]<=tp: return None,j
  j=min(N-1,j0+287); return d*(C[j]-e)/abs(e-sl),j

def run(entry,loc,rr,regime=None,thuan=False):
  res={'HL':[], 'KT':[]}; busy=-1
  for j in range(4,N-1):
    if j<=busy: continue
    for d in (1,-1):
      g = L[j]-H[j-2] if d>0 else L[j-2]-H[j]
      if g<0.3*A5[j]: continue
      px = min(L[j-3:j+1]) if d>0 else max(H[j-3:j+1])
      okH1 = trung(ZH1,AH1,j,d,px); okH4 = trung(ZH4,AH4,j,d,px)
      if loc=='H1' and not okH1: continue
      if loc=='H4' and not okH4: continue
      if loc=='H1+H4' and not (okH1 and okH4): continue
      if loc=='H1|H4' and not (okH1 or okH4): continue
      gc,xh = d1_info(T[j])
      if regime=='giangco' and not gc: continue
      if regime=='xuhuong' and gc: continue
      if thuan and xh!=d: continue
      buf=0.1*A5[j]
      if entry=='FVG':          # vao luon gia mo nen sau
        e=O[j+1]; sl=px-d*buf; j1=j+1
      else:                     # 'OB': cho gia hoi ve dinh/day nen nguoc chieu cuoi cung (toi da 24 nen)
        ob=None
        for q in range(j-1,max(0,j-7),-1):
          if (d>0 and C[q]<O[q]) or (d<0 and C[q]>O[q]): ob=q; break
        if ob is None: continue
        e = H[ob] if d>0 else L[ob]; sl = (L[ob] if d>0 else H[ob])-d*buf; j1=None
        for q in range(j+1,min(N,j+25)):
          if (d>0 and L[q]<=e) or (d<0 and H[q]>=e): j1=q; break
        if j1 is None: continue
      R=abs(e-sl)
      if R<MINR or d*(e-sl)<=0: continue
      tp=e+d*rr*R
      if entry=='OB' and ((d>0 and L[j1]<=sl) or (d<0 and H[j1]>=sl)): r,jx=-1.0,j1
      else: r,jx=sim(e,sl,tp,d,j1 if entry=='FVG' else j1+1)
      if r is None: r=rr
      r-=COST/R
      res['KT' if T[j]>=CUT else 'HL'].append(r); busy=jx; break
  return res

print("Phi $%.0f/lenh, SL toi thieu $%.0f, cham ca SL va TP cung nen = thua. HL 01/2025-24/07/2026, KT 25/07-26/10/2026"%(COST,MINR))
for entry in ('FVG','OB'):
  for loc in ('none','H1','H4','H1|H4','H1+H4'):
    for rr in (1.0,2.0,3.0):
      r=run(entry,loc,rr)
      rep(f"{entry} loc={loc:5s} {rr}R HL",r['HL']); rep(f"{entry} loc={loc:5s} {rr}R KT",r['KT'])
print("--- tach theo che do D1 (ADX<20 = giang co), loc H1|H4, 2R ---")
for entry in ('FVG','OB'):
  for reg in ('giangco','xuhuong'):
    for th in (False,True):
      r=run(entry,'H1|H4',2.0,reg,th)
      rep(f"{entry} {reg} thuanD1={th} HL",r['HL']); rep(f"{entry} {reg} thuanD1={th} KT",r['KT'])
