# Vong 4b (28/10/2026): vao lenh truc tiep o FVG khung lon (H1 / H4) khi gia hoi ve lan dau.
# Chay: python3 -I fvg_htf.py <m5.csv> <thu muc scripts>
import sys,datetime,warnings; warnings.filterwarnings('ignore'); sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1]); T=[t//1000 for t in T]; N=len(T)
CUT=datetime.datetime(2026,7,25).timestamp(); COST=18.0

def atr(Hs,Ls,Cs,p=14):
  tr=[Hs[0]-Ls[0]]+[max(Hs[i]-Ls[i],abs(Hs[i]-Cs[i-1]),abs(Ls[i]-Cs[i-1])) for i in range(1,len(Hs))]
  out=[];s=0
  for i,v in enumerate(tr):
    s+=v
    if i>=p: s-=tr[i-p]
    out.append(s/min(i+1,p))
  return out

# D1: xu huong (SMA50) va giang co (ADX14 < 20), dung nen D1 da dong
D=agg([t*1000 for t in T],O,H,L,C,86400)
dH=[b[2] for b in D]; dL=[b[3] for b in D]; dC=[b[4] for b in D]
def adx(Hs,Ls,Cs,p=14):
  n=len(Hs); a=2/(p+1); s_tr=s_p=s_m=dxs=0; out=[0]*n
  for i in range(1,n):
    up=Hs[i]-Hs[i-1]; dn=Ls[i-1]-Ls[i]
    pdm=up if up>dn and up>0 else 0; mdm=dn if dn>up and dn>0 else 0
    tr=max(Hs[i]-Ls[i],abs(Hs[i]-Cs[i-1]),abs(Ls[i]-Cs[i-1]))
    s_tr+=a*(tr-s_tr); s_p+=a*(pdm-s_p); s_m+=a*(mdm-s_m)
    pdi=100*s_p/s_tr if s_tr else 0; mdi=100*s_m/s_tr if s_tr else 0
    dx=100*abs(pdi-mdi)/(pdi+mdi) if pdi+mdi else 0
    dxs+=a*(dx-dxs); out[i]=dxs
  return out
dA=adx(dH,dL,dC); dS=[sum(dC[max(0,i-49):i+1])/len(dC[max(0,i-49):i+1]) for i in range(len(dC))]
dmap={b[0]:i for i,b in enumerate(D)}
def d1(t):
  i=dmap.get(t//86400*86400,0)-1
  return (0,0) if i<0 else ((1 if dA[i]<20 else 0),(1 if dC[i]>dS[i] else -1))

def run(sec,gmin,entry,rr,life,hold,flt=None):
  B=agg([t*1000 for t in T],O,H,L,C,sec)
  Bh=[b[2] for b in B]; Bl=[b[3] for b in B]; Bc=[b[4] for b in B]; At=atr(Bh,Bl,Bc)
  res={'HL':[],'KT':[]}; busy=-1
  for i in range(2,len(B)-1):
    for d in (1,-1):
      if d>0: lo,hi=Bh[i-2],Bl[i]
      else:   lo,hi=Bh[i],Bl[i-2]
      if hi-lo<gmin*At[i]: continue
      st=B[i][5]+1
      if st<=busy: continue
      gc,xh=d1(T[st])
      if flt=='thuan' and xh!=d: continue
      if flt=='nguoc' and xh!=-d: continue
      if flt=='giangco' and not gc: continue
      if flt=='giangco_thuan' and (not gc or xh!=d): continue
      # gia vao: mep gan (dau vung) hoac giua vung (CE)
      e = (hi if d>0 else lo) if entry=='mep' else (lo+hi)/2
      far = lo if d>0 else hi
      sl = far-d*0.1*At[i]; R=abs(e-sl)
      if R<=0: continue
      tp=e+d*rr*R
      # cho gia hoi ve lan dau trong 'life' nen khung lon; dong cua vuot mep xa truoc do = vung hong
      end=min(N,st+life*sec//300); j1=None
      for j in range(st,end):
        if (d>0 and L[j]<=e) or (d<0 and H[j]>=e): j1=j; break
        if (d>0 and C[j]<far) or (d<0 and C[j]>far): break
      if j1 is None: continue
      r=None; jx=min(N-1,j1+hold*sec//300)
      for j in range(j1,jx+1):
        if (d>0 and L[j]<=sl) or (d<0 and H[j]>=sl): r=-1.0; jx=j; break
        if j>j1 and ((d>0 and H[j]>=tp) or (d<0 and L[j]<=tp)): r=rr; jx=j; break
      if r is None: r=d*(C[jx]-e)/R
      r-=COST/R
      res['KT' if T[j1]>=CUT else 'HL'].append(r); busy=jx
  return res

print("Vao o FVG khung lon khi gia hoi ve lan dau. Phi $%.0f. Cham SL va TP cung nen = thua. HL 01/2025-24/07/2026, KT 25/07-26/10/2026"%COST)
for tf,sec,life,hold in (('H1',3600,72,72),('H4',14400,30,30)):
  for g in (0.3,0.6):
    for entry in ('mep','CE'):
      for rr in (1.5,2.0,3.0):
        r=run(sec,g,entry,rr,life,hold)
        rep(f"{tf} gap>={g}ATR {entry:3s} {rr}R HL",r['HL']); rep(f"{tf} gap>={g}ATR {entry:3s} {rr}R KT",r['KT'])
print("--- loc theo D1 (gap>=0.3ATR, CE, 2R) ---")
for tf,sec,life,hold in (('H1',3600,72,72),('H4',14400,30,30)):
  for f in ('thuan','nguoc','giangco','giangco_thuan'):
    r=run(sec,0.3,'CE',2.0,life,hold,f)
    rep(f"{tf} {f} HL",r['HL']); rep(f"{tf} {f} KT",r['KT'])
