# Vong 19 (03/11/2026): he thong RSI tren BTC/ETH, giu NEN TANG cua bot EMA:
# SL ban dau = swing 2 nen, keo SL bac thang swing 10 nen (TinhSLKeo), khoa loi 2R giu 50%,
# ao giap thua 3 lenh nghi 8h, rui ro 2% (H4 x1.5). Chua co: nhoi lenh, tran lot min.
# Tin hieu (RSI14 Wilder, nen da dong, vao o gia dong):
#   K1 hoi ve   : RSI cat len 30 -> MUA, cat xuong 70 -> BAN
#   K2 dong luc : RSI cat len 55 -> MUA, cat xuong 45 -> BAN
#   K3 hoi trong xu huong: gia tren EMA200 & EMA200 di len, RSI cat len 40 -> MUA (nguoc lai 60 -> BAN)
#   K4 = MH2 nghien cuu cu cua anh (09/2026): EMA9(RSI) cat len WMA45(RSI), khung lon EMA9(RSI)>WMA45(RSI)
#        (M15/H1, H1/H4, H4/D1); BAN doi xung
#   K5 = MH3a: quan tinh tang vua bat (RSI>=70 du 2 nen, may trang thai co 'suy yeu'); BAN doi xung (<=30)
# Them co S: chi vao khi SL cach gia 0,5-1,5% (luat loc SL cua ban cu)
# Loc: 0 khong loc | E = EMA200 cung chieu | D = phe D1 (EMA10/20 + gia duoi/tren ca 2) cung chieu
# Chay: python3 -I rsi.py <m5_btc.csv> <eth15.csv> <thu muc scripts> [che do]
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import load,agg,ema
PHI=0.0006; SL_MIN=0.002; W_SL=2; W_TR=10; KHOA_TU=2.0; KHOA_PT=0.5

def rsi(c,p=14):
  r=[50.0]*len(c); g=l=0.0
  for i in range(1,len(c)):
    d=c[i]-c[i-1]; up=max(d,0); dn=max(-d,0)
    if i<=p: g+=up/p; l+=dn/p
    else: g=(g*(p-1)+up)/p; l=(l*(p-1)+dn)/p
    if i>=p: r[i]=100 if l==0 else 100-100/(1+g/l)
  return r

def wma(x,p):
  o=[x[0]]*len(x); den=p*(p+1)/2
  for i in range(p-1,len(x)): o[i]=sum(x[i-p+1+k]*(k+1) for k in range(p))/den
  return o

def lon_thuan(src,d,sec_lon):
  # huong EMA9(RSI) vs WMA45(RSI) cua nen khung lon da dong truoc khi nen i dong
  D=khung_nhe(src,sec_lon); m={}
  for k,t in enumerate(D['t']): m[t]=1 if D['e9r'][k]>D['w45r'][k] else -1
  return [m.get(((t+d['sec'])//sec_lon-1)*sec_lon,0) for t in d['t']]

def khung_nhe(src,sec):
  B=agg(*src,sec)[:-1]; c=[b[4] for b in B]; r=rsi(c)
  return dict(t=[b[0] for b in B],e9r=ema(r,TS.get('ef',9)),w45r=wma(r,TS.get('ws',45)))

def quan_tinh(d):
  # tra mang mom[i] theo may trang thai cua ban cu (vung 70/30 du 2 nen, suy yeu khi dinh moi RSI<70)
  r,h,l=d['rsi'],d['h'],d['l']; n=d['n']; mom=0; z7=z3=0; sH=[]; sL=[]; out=[0]*n
  for i in range(4,n):
    c=i-2
    dm=d['dinh2'][c]; dy=d['day2'][c]
    if dm: sH.append((h[c],r[c]))
    if dy: sL.append((l[c],r[c]))
    z7=z7+1 if r[i]>=70 else 0; z3=z3+1 if r[i]<=30 else 0
    if z7>=2: mom=1
    elif z3>=2: mom=-1
    else:
      if mom==1 and dm and len(sH)>=2 and sH[-1][0]>sH[-2][0] and sH[-1][1]<70: mom=2
      if mom==-1 and dy and len(sL)>=2 and sL[-1][0]<sL[-2][0] and sL[-1][1]>30: mom=-2
    out[i]=mom
  return out

def piv(h,l,w):
  n=len(h); dinh=[False]*n; day=[False]*n
  for c in range(w,n-w):
    dinh[c]=all(h[q]<h[c] for q in range(c-w,c+w+1) if q!=c)
    day[c]=all(l[q]>l[c] for q in range(c-w,c+w+1) if q!=c)
  return dinh,day

def khung(src,sec):
  B=agg(*src,sec)[:-1]   # bo nen chua dong
  d=dict(sec=sec,n=len(B),t=[b[0] for b in B],o=[b[1] for b in B],h=[b[2] for b in B],l=[b[3] for b in B],c=[b[4] for b in B])
  d['rsi']=rsi(d['c']); d['e200']=ema(d['c'],200)
  d['e9r']=ema(d['rsi'],TS.get('ef',9)); d['w45r']=wma(d['rsi'],TS.get('ws',45))
  d['dinh2'],d['day2']=piv(d['h'],d['l'],W_SL); d['dinh10'],d['day10']=piv(d['h'],d['l'],W_TR)
  return d

def phe_d1(src,d):
  D=agg(*src,86400)[:-1]; c=[b[4] for b in D]; e10=ema(c,10); e20=ema(c,20)
  ph={}
  for k,b in enumerate(D):
    p=0
    if e10[k]<e20[k] and c[k]<min(e10[k],e20[k]): p=-1
    if e10[k]>e20[k] and c[k]>max(e10[k],e20[k]): p=1
    ph[b[0]//86400]=p
  # phe tai nen i = D1 da dong truoc khi nen i dong
  return [ph.get((t+d['sec'])//86400-1,0) for t in d['t']]

def sl_dau(d,j,huong,gia):
  for c in range(j-W_SL,max(W_SL,j-499)-1,-1):
    if huong>0 and d['day2'][c] and d['l'][c]<gia: return d['l'][c]
    if huong<0 and d['dinh2'][c] and d['h'][c]>gia: return d['h'][c]
  return None

def mo(d,sig,huong):
  # tra (R, nen ra, maxR)
  o,h,l,c=d['o'],d['h'],d['l'],d['c']; dinh,day=d['dinh10'],d['day10']
  vao=c[sig]; sl=sl_dau(d,sig,huong,vao)
  if sl is None: return None
  R=abs(vao-sl)
  if R<SL_MIN*vao: return None   # SL sat hon 0,2% gia -> phi an het (bo qua)
  best=vao; st=0; m1=m1b=0; tr=0; ds=[]
  for b in range(sig+1,d['n']):
    if huong>0 and l[b]<=sl: ra=min(sl,o[b]); return ((ra-vao)-PHI*vao)/R,b,(best-vao)/R
    if huong<0 and h[b]>=sl: ra=max(sl,o[b]); return ((vao-ra)-PHI*vao)/R,b,(vao-best)/R
    cc=b-W_TR
    if huong>0:
      best=max(best,h[b])
      if cc>sig:
        if st==0 and dinh[cc]: m1=h[cc]; m1b=cc; st=1
        elif st>=1 and cc>m1b and day[cc]:
          ds.append(cc)
          if st==1: tr=l[cc]; st=2
      if st==2 and h[b]>m1: st=3
      if st==3:
        for q in ds:
          if l[q]>tr and l[q]<c[b]: tr=l[q]
        sl=max(sl,tr)
      if best-vao>=KHOA_TU*R: sl=max(sl,vao+KHOA_PT*(best-vao))
    else:
      best=min(best,l[b])
      if cc>sig:
        if st==0 and day[cc]: m1=l[cc]; m1b=cc; st=1
        elif st>=1 and cc>m1b and dinh[cc]:
          ds.append(cc)
          if st==1: tr=h[cc]; st=2
      if st==2 and l[b]<m1: st=3
      if st==3:
        for q in ds:
          if h[q]<tr and h[q]>c[b]: tr=h[q]
        sl=min(sl,tr)
      if vao-best>=KHOA_TU*R: sl=min(sl,vao-KHOA_PT*(vao-best))
  ra=c[-1]; return (((ra-vao) if huong>0 else (vao-ra))-PHI*vao)/R,d['n']-1,0

TS=dict(k2=55)
def tin_hieu(d,i,kieu,loc,ph):
  r,c,e=d['rsi'],d['c'],d['e200']; s=0
  if kieu=='K4':
    a,b=d['e9r'],d['w45r']
    if a[i-1]<=b[i-1] and a[i]>b[i] and d['lon'][i]==1: s=1
    if a[i-1]>=b[i-1] and a[i]<b[i] and d['lon'][i]==-1: s=-1
  elif kieu=='K5':
    m=d['mom']
    if m[i]==1 and m[i-1]!=1: s=1
    if m[i]==-1 and m[i-1]!=-1: s=-1
  elif kieu=='K1':
    if r[i-1]<30<=r[i]: s=1
    if r[i-1]>70>=r[i]: s=-1
  elif kieu=='K2':
    a=TS['k2']; b=100-a
    if r[i-1]<a<=r[i]: s=1
    if r[i-1]>b>=r[i]: s=-1
  elif kieu=='K3':
    if c[i]>e[i] and e[i]>e[i-20] and r[i-1]<40<=r[i]: s=1
    if c[i]<e[i] and e[i]<e[i-20] and r[i-1]>60>=r[i]: s=-1
  if s and loc=='E' and (c[i]-e[i])*s<=0: s=0
  if s and loc=='D' and ph[i]!=s: s=0
  return s

def chay(d,kieu,loc,ph,locSL=False):
  res=[]; ban={1:-1,-1:-1}   # moi chieu 1 lenh cung luc
  for i in range(220,d['n']-1):
    s=tin_hieu(d,i,kieu,loc,ph)
    if not s or i<=ban[s]: continue
    if locSL:
      sl=sl_dau(d,i,s,d['c'][i])
      if sl is None or not 0.005<=abs(d['c'][i]-sl)/d['c'][i]<=0.015: continue
    x=mo(d,i,s)
    if x: res.append(dict(t=d['t'][i]+d['sec'],tra=d['t'][x[1]]+d['sec'],R=x[0],max=x[2],h=s,sec=d['sec'],i=i,gia=d['c'][i],kc=abs(d['c'][i]-sl_dau(d,i,s,d['c'][i])))); ban[s]=x[1]
  return res

def ao_giap(L):
  # thua 3 lenh lien tiep -> nghi 8h (dem theo thu tu dong lenh)
  nhan=[]
  for x in sorted(L,key=lambda x:x['t']):
    dong=sorted([y for y in nhan if y['tra']<=x['t']],key=lambda y:y['tra'])
    thua=0; nghi=0
    for y in dong:
      thua=thua+1 if y['R']<0 else 0
      if thua>=3: nghi=y['tra']+8*3600; thua=0
    if x['t']<nghi: continue
    nhan.append(x)
  return nhan

def von(L,rr=2.0):
  # % so du, rui ro 2% (H4 x1.5), tinh lai kep theo thu tu dong lenh
  ev=sorted(L,key=lambda x:x['tra']); b=100.0; pk=100.0; dd=0
  for x in ev:
    b*=1+x['R']*rr*(1.5 if x['sec']>=14400 else 1)/100; pk=max(pk,b); dd=max(dd,1-b/pk)
  return b-100,dd*100

def tk(L,tu):
  v=[x['R'] for x in L if x['t']>=tu]
  if not v: return "   0L"
  eq=pk=dd=0; m=ls=0
  for x in v:
    eq+=x; pk=max(pk,eq); dd=max(dd,pk-eq); m=m+1 if x<0 else 0; ls=max(ls,m)
  top=sorted(v,reverse=True)[:3]
  return f"{len(v):4d}L {100*sum(1 for x in v if x>0)/len(v):3.0f}% {sum(v):+6.1f}R sut{dd:5.1f} thuaLT{ls:2d} top3{sum(top):5.1f}"

def tk4(L,m12,m6,m3):
  dau=[x for x in L if x['t']<m6]
  return f"{tk(L,m12)} | nua dau {sum(x['R'] for x in dau):+6.1f}R | {tk(L,m6)} | {tk(L,m3)}"

def ben():
  # vong 19b: ung vien + tham so lan can, co chan SL min 0,2%
  US=[('K2','0',False),('K2','D',False),('K2','D',True),('K4','0',False),('K4','0',True),('K4','D',False),('K5','0',False),('K5','D',False)]
  for ten,p in (('BTC',sys.argv[1]),('ETH',sys.argv[2])):
    src=load(p); cuoi=src[0][-1]//1000; m12,m6,m3=cuoi-365*86400,cuoi-183*86400,cuoi-92*86400
    print(f"===== {ten} (12T | nua dau 12T | 6T | 3T)")
    for tf,sec,lon in (('M15',900,3600),('H1',3600,14400),('H4',14400,86400)):
      for bien in ({},{'k2':52},{'k2':58},{'k2':60},{'ef':7,'ws':35},{'ef':12,'ws':55}):
        TS.clear(); TS.update(k2=55); TS.update(bien)
        d=khung(src,sec); ph=phe_d1(src,d); d['lon']=lon_thuan(src,d,lon); d['mom']=quan_tinh(d)
        for kieu,loc,ls in US:
          if bien and kieu=='K5': continue
          if 'k2' in bien and kieu!='K2': continue
          if 'ef' in bien and kieu!='K4': continue
          L=[x for x in chay(d,kieu,loc,ph,ls) if x['t']>=m12]
          print(f"{ten} {tf:3s} {kieu} loc{loc}{'S' if ls else ' '} {str(bien):22s}| {tk4(L,m12,m6,m3)}",flush=True)

def thang_te(L,rr=2.0):
  import datetime as dt
  m={}
  for x in L:
    k=dt.datetime.utcfromtimestamp(x['tra']).strftime('%m/%y'); m[k]=m.get(k,0)+x['R']*rr*(1.5 if x['sec']>=14400 else 1)
  k=min(m,key=m.get); return f"{k} {m[k]:+.1f}%", sum(1 for v in m.values() if v<0), len(m)

def von_ghep(cu=False):
  # vong 19c: ghep cac thanh phan, ao giap thua 3 nghi 8h, rui ro 2% (H4 3%), lai kep
  TP={'K2H1':('H1',3600,14400,'K2','0',False),'K2H4D':('H4',14400,86400,'K2','D',False),
      'K5M15':('M15',900,3600,'K5','0',False),'K4H1':('H1',3600,14400,'K4','0',False)}
  GH=[('K2H1',),('K2H1','K2H4D'),('K2H1','K2H4D','K5M15'),('K4H1',),('K2H1','K4H1')]
  for ten,p in (('BTC',sys.argv[1]),('ETH',sys.argv[2])):
    src=load(p); cuoi=src[0][-1]//1000; m12,m6=cuoi-365*86400,cuoi-183*86400
    TS.clear(); TS.update(k2=55); cache={}
    for k,(tf,sec,lon,kieu,loc,ls) in TP.items():
      d=khung(src,sec); ph=phe_d1(src,d); d['lon']=lon_thuan(src,d,lon); d['mom']=quan_tinh(d)
      cache[k]=[dict(x,tp=k) for x in chay(d,kieu,loc,ph,ls) if (x['t']<m12 if cu else x['t']>=m12)]
    if cu:
      import datetime as dt
      a=min(x['t'] for v in cache.values() for x in v); print(f"===== {ten} DOAN CU {dt.datetime.utcfromtimestamp(a):%d/%m/%Y} -> {dt.datetime.utcfromtimestamp(m12):%d/%m/%Y} (khong dung de chon)")
    else: print(f"===== {ten} 12 thang, von 100%, rui ro 2% (H4 3%), thua 3 nghi 8h")
    for g in GH:
      L0=[x for k in g for x in cache[k]]; L=ao_giap(L0)
      lai,dd=von(L); lai6,dd6=von([x for x in L if x['t']>=m6])
      mua=[x['R'] for x in L if x['h']>0]; ban=[x['R'] for x in L if x['h']<0]
      v=sorted([x['R'] for x in L],reverse=True)
      tt,am,nt=thang_te(L)
      print(f"{'+'.join(g):22s} {len(L):4d}L (ao giap bo {len(L0)-len(L):2d}) | 12T lai {lai:+7.1f}% sut {dd:5.1f}% | 6T lai {lai6:+6.1f}% sut {dd6:5.1f}% | MUA {len(mua)}L {sum(mua):+.1f}R BAN {len(ban)}L {sum(ban):+.1f}R | bo 3 lenh lon nhat {sum(v[3:]):+.1f}R | thang te {tt}, {am}/{nt} thang am")

if __name__=='__main__':
  che=sys.argv[4] if len(sys.argv)>4 else 'quet'
  if che=='ben': ben(); sys.exit()
  if che=='von': von_ghep(); sys.exit()
  if che=='von_cu': von_ghep(True); sys.exit()
  for ten,p in (('BTC',sys.argv[1]),('ETH',sys.argv[2])):
    src=load(p); cuoi=src[0][-1]//1000
    m12,m6,m3=cuoi-365*86400,cuoi-183*86400,cuoi-92*86400
    print(f"===== {ten}: du lieu den {__import__('datetime').datetime.utcfromtimestamp(cuoi):%d/%m/%Y}  (12T | 6T | 3T; top3 = tong R 3 lenh lon nhat)")
    for tf,sec,lon in (('M15',900,3600),('H1',3600,14400),('H4',14400,86400)):
      d=khung(src,sec); ph=phe_d1(src,d); d['lon']=lon_thuan(src,d,lon); d['mom']=quan_tinh(d)
      for kieu in ('K1','K2','K3','K4','K5'):
        for loc in ('0','E','D'):
          for ls in (False,True):
            L=[x for x in chay(d,kieu,loc,ph,ls) if x['t']>=m12]
            print(f"{ten} {tf:3s} {kieu} loc{loc}{'S' if ls else ' '} | {tk(L,m12)} | {tk(L,m6)} | {tk(L,m3)}",flush=True)
