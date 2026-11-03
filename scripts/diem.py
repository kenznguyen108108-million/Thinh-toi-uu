# Vong 23 (03/11/2026): khong chia hop E0-E3 nua. Moi lan EMA9(RSI) cat WMA45(RSI) (moi khung doc lap) ghi hanh trinh
# bang SO LIEN TUC, de du lieu ve duong cong ket qua theo tung dac diem, roi CHAM DIEM tin hieu (cong don, khong nguong cung).
# Hoc tren du lieu truoc 2024, kiem tra 2024 -> nay (khong dung de hoc).
# Dac diem (lat doi xung cho BAN):
#   sau   do sau pha truoc (|EMA9-WMA45| lon nhat, diem RSI)     dai   so nen cua pha truoc
#   cuc   RSI cuc tri pha truoc (MUA: RSI thap nhat; BAN: 100-RSI cao nhat)
#   docf  doc EMA9 3 nen        docs  doc WMA45 3 nen (WMA45 da quay dau chua)
#   rs    RSI cach WMA45 luc cat   bd    ATR/gia (%)        vt    gia o dau trong bien 50 nen (0 = day, 1 = dinh)
# Ket qua: R theo nen tang (SL swing 2, keo SL 10, khoa 2R/50%, phi, SL>=0,2%).
# Chay: python3 -I diem.py <thu muc data>
import sys,os,datetime as dt,math; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,SEC
from rsi import mo,sl_dau
from von500 import mo_phong
DT=['sau','dai','cuc','docf','docs','rs','bd','vt']; NB=10
M24=dt.datetime(2024,1,1).timestamp()

def su_kien(d,sec,sym,tf):
  f,s,r,c,h,l,a=d['f'],d['s'],d['r'],d['c'],d['h'],d['l'],d['atr']; out=[]; b0=60
  for i in range(61,d['n']-1):
    kc0=f[i-1]-s[i-1]; kc1=f[i]-s[i]
    if kc0*kc1>0 or kc1==0: continue
    hg=1 if kc1>0 else -1
    pha=range(b0,i); b0=i
    if len(pha)<2: continue
    x=mo(d,i,hg)
    if not x: continue
    lo=min(l[i-49:i+1]); hi=max(h[i-49:i+1]); vt=(c[i]-lo)/(hi-lo) if hi>lo else .5
    e=dict(sym=sym,tf=tf,sec=sec,h=hg,t=d['t'][i]+sec,tra=d['t'][x[1]]+sec,R=x[0],i=i,gia=c[i],kc=abs(c[i]-sl_dau(d,i,hg,c[i])),
      sau=max(-hg*(f[k]-s[k]) for k in pha), dai=math.log(len(pha)),
      cuc=(min(r[k] for k in pha) if hg>0 else 100-max(r[k] for k in pha)),
      docf=hg*(f[i]-f[i-3]), docs=hg*(s[i]-s[i-3]), rs=hg*(r[i]-s[i]), bd=a[i]/c[i]*100, vt=(vt if hg>0 else 1-vt))
    out.append(e)
  return out

def bins(E,k):
  v=sorted(e[k] for e in E); return [v[int(len(v)*q/NB)] for q in range(1,NB)]
def ngan(b,x):
  j=0
  while j<len(b) and x>b[j]: j+=1
  return j

def hoc(E):
  tb=sum(e['R'] for e in E)/len(E); M={}
  for k in DT:
    b=bins(E,k); g=[[] for _ in range(NB)]
    for e in E: g[ngan(b,e[k])].append(e['R'])
    m=[(sum(x)/len(x) if x else tb) for x in g]
    sm=[(m[max(0,j-1)]+2*m[j]+m[min(NB-1,j+1)])/4 for j in range(NB)]   # lam tron: trang thai giua 2 o cung duoc tinh
    M[k]=(b,[x-tb for x in sm],[len(x) for x in g],m)
  return tb,M

def cham(e,M): return sum(M[k][1][ngan(M[k][0],e[k])] for k in DT)

def mot_lenh(E):
  # moi khung, moi chieu 1 lenh cung luc
  E=sorted(E,key=lambda e:e['t']); ban={}; out=[]
  for e in E:
    k=(e['sym'],e['tf'],e['h'])
    if e['t']<ban.get(k,0): continue
    out.append(e); ban[k]=e['tra']
  return out

def tk(E):
  v=[e['R'] for e in E]
  if not v: return "   0L"
  eq=pk=dd=0
  for x in v: eq+=x; pk=max(pk,eq); dd=max(dd,pk-eq)
  return f"{len(v):5d}L {100*sum(1 for x in v if x>0)/len(v):3.0f}% {sum(v)/len(v):+.3f}R/l {sum(v):+7.1f}R sut{dd:6.1f}R"

if __name__=='__main__':
  dd_=sys.argv[1]; E=[]
  for sym in ('BTC','ETH'):
    for tf in ('1h','4h','1d'):
      E+=su_kien(nap(load(f"{dd_}/{sym}_{tf}.csv")),SEC[tf],sym,tf)
  hocE=[e for e in E if e['t']<M24]; kt=[e for e in E if e['t']>=M24]
  tb,M=hoc(hocE)
  print(f"Hoc: {len(hocE)} lan cat truoc 2024 (BTC+ETH, H1/H4/D1, 2 chieu), R TB {tb:+.3f}. Kiem tra: {len(kt)} lan tu 2024.")
  print("\n=== DUONG KET QUA theo tung dac diem (tap hoc; R TB moi o 10% tu thap -> cao; o giua nguong o)")
  for k in DT:
    b,_,n,m=M[k]
    print(f"{k:5s} nguong {' '.join(f'{x:6.2f}' for x in b)}\n      R TB  {' '.join(f'{x:+6.2f}' for x in m)}")
  # kiem chung o tap kiem tra: R TB theo nhom diem
  for e in E: e['diem']=cham(e,M)
  print("\n=== DIEM -> R that (tap KIEM TRA 2024->nay, chua dung de hoc)")
  v=sorted(kt,key=lambda e:e['diem']); q=len(v)//5
  for j in range(5):
    g=v[j*q:(j+1)*q] if j<4 else v[4*q:]
    print(f"  nhom diem {j+1}/5 ({g[0]['diem']:+.2f}..{g[-1]['diem']:+.2f}): {tk(g)}")
  print("\n=== Theo tung ma/khung (2024->nay), giu 1 lenh/khung/chieu: tat ca | diem>0")
  for sym in ('BTC','ETH'):
    for tf in ('1h','4h','1d'):
      g=[e for e in kt if e['sym']==sym and e['tf']==tf]
      print(f"  {sym} {tf.upper():3s} | {tk(mot_lenh(g))} | {tk(mot_lenh([e for e in g if e['diem']>0]))}")
  print("\n=== Von 500 USD (lot that, ao giap): tat ca tin hieu vs chi diem>0")
  cuoi=max(e['t'] for e in E)
  for sym,tfs in (('ETH',('4h','1d')),('ETH',('1h','4h','1d')),('BTC',('1h','4h','1d')),('BTC',('4h','1d'))):
    for thg in (12,6,3):
      tu=cuoi-int(thg*30.5*86400); g=[e for e in kt if e['sym']==sym and e['tf'] in tfs and e['t']>=tu]
      print(f"  {sym} {'+'.join(tfs):10s} {thg:2d}T | tat ca: {mo_phong(mot_lenh(g),sym).split('|')[1].strip():28s} | diem>0: {mo_phong(mot_lenh([e for e in g if e['diem']>0]),sym)}")
