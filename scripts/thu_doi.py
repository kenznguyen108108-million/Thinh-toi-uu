# Vong 25b (03/11/2026): thu doi tung cho rut ra tu ra lenh (chan_doan.py), moi lan 1 thu, so voi goc.
#   khoa loi (moc, % giu) | hoa von som | SL toi thieu theo ATR | vao som hon (RSI cat len WMA45 khi pha giam da du sau)
# Danh gia: R/lenh va tong R, truoc 2024 (hoc) va 2024->nay (kiem tra), BTC H1/H4/D1 + ETH H4/D1, 2 chieu.
# Chay: python3 -I thu_doi.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,SEC
from rsi import sl_dau,PHI,SL_MIN,W_TR
M24=dt.datetime(2024,1,1).timestamp()

def mo2(d,sig,hg,khoa_tu=2.0,khoa_pt=0.5,hv=0,sl_atr=0):
  o,h,l,c=d['o'],d['h'],d['l'],d['c']; dinh,day=d['dinh10'],d['day10']
  vao=c[sig]; sl=sl_dau(d,sig,hg,vao)
  if sl is None: return None
  if sl_atr>0:   # noi SL ra it nhat sl_atr x ATR
    sl=min(sl,vao-sl_atr*d['atr'][sig]) if hg>0 else max(sl,vao+sl_atr*d['atr'][sig])
  R=abs(vao-sl)
  if R<SL_MIN*vao: return None
  best=vao; st=0; m1=m1b=0; tr=0; ds=[]
  for b in range(sig+1,d['n']):
    if hg>0 and l[b]<=sl: return ((min(sl,o[b])-vao)-PHI*vao)/R,b
    if hg<0 and h[b]>=sl: return ((vao-max(sl,o[b]))-PHI*vao)/R,b
    cc=b-W_TR
    if hg>0:
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
      if hv and best-vao>=hv*R: sl=max(sl,vao+PHI*vao)
      if best-vao>=khoa_tu*R: sl=max(sl,vao+khoa_pt*(best-vao))
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
      if hv and vao-best>=hv*R: sl=min(sl,vao-PHI*vao)
      if vao-best>=khoa_tu*R: sl=min(sl,vao-khoa_pt*(vao-best))
  return (((c[-1]-vao)*hg)-PHI*vao)/R,d['n']-1

def diem_vao(d,kieu,sau_min=3):
  # 'cat' = EMA9 cat WMA45 (goc). 'som' = RSI cat len WMA45 trong pha giam (EMA9 van < WMA45) khi pha da sau >= sau_min
  f,s,r=d['f'],d['s'],d['r']; out=[]; dau={1:0,-1:0}; da={1:False,-1:False}
  for i in range(61,d['n']-1):
    for hg in (1,-1):
      kc=f[i]-s[i]
      if hg*kc<0: dau[hg]=max(dau[hg],-hg*kc)
      if kieu=='cat':
        if hg*(f[i-1]-s[i-1])<=0 and hg*kc>0: out.append((i,hg))
      else:
        if hg*kc<0 and not da[hg] and dau[hg]>=sau_min and hg*(r[i-1]-s[i-1])<=0 and hg*(r[i]-s[i])>0:
          out.append((i,hg)); da[hg]=True
      if hg*kc>0: dau[hg]=0; da[hg]=False
  return out

def chay(d,sec,ev,**kw):
  res=[]; ban={1:-1,-1:-1}
  for i,hg in ev:
    if i<=ban[hg]: continue
    x=mo2(d,i,hg,**kw)
    if x: res.append((d['t'][i]+sec,x[0])); ban[hg]=x[1]
  return res

def tk(v):
  if not v: return "   0L"
  return f"{len(v):5d}L {sum(v)/len(v):+.3f}R/l {sum(v):+7.1f}R"

if __name__=='__main__':
  dd_=sys.argv[1]
  BO=[('BTC','1h'),('BTC','4h'),('BTC','1d'),('ETH','4h'),('ETH','1d')]
  DD={(s,t):nap(load(f"{dd_}/{s}_{t}.csv")) for s,t in BO}
  EV={k:diem_vao(d,'cat') for k,d in DD.items()}
  THU=[('GOC: khoa 2R giu 50%',{} ,'cat'),
       ('khoa 1,5R giu 50%',dict(khoa_tu=1.5),'cat'),('khoa 2R giu 60%',dict(khoa_pt=0.6),'cat'),('khoa 2R giu 70%',dict(khoa_pt=0.7),'cat'),
       ('khoa 3R giu 60%',dict(khoa_tu=3,khoa_pt=0.6),'cat'),('khoa 3R giu 70%',dict(khoa_tu=3,khoa_pt=0.7),'cat'),('khoa 4R giu 70%',dict(khoa_tu=4,khoa_pt=0.7),'cat'),
       ('hoa von o 1R',dict(hv=1),'cat'),('hoa von o 1,5R',dict(hv=1.5),'cat'),
       ('SL >= 1 ATR',dict(sl_atr=1),'cat'),('SL >= 1,5 ATR',dict(sl_atr=1.5),'cat'),
       ('VAO SOM (RSI cat WMA45, pha sau>=3)',{},'som3'),('VAO SOM (pha sau>=5)',{},'som5'),('VAO SOM sau>=5 + SL>=1 ATR',dict(sl_atr=1),'som5')]
  print("Moi dong: truoc 2024 (hoc) || 2024->nay (kiem tra). Cot: "+" | ".join(f"{s} {t.upper()}" for s,t in BO))
  for ten,kw,vao in THU:
    a=[];b=[]
    for k,d in DD.items():
      ev=EV[k] if vao=='cat' else diem_vao(d,'som',int(vao[3:]))
      L=chay(d,SEC[k[1]],ev,**kw)
      a.append([x[1] for x in L if x[0]<M24]); b.append([x[1] for x in L if x[0]>=M24])
    tong_a=[x for v in a for x in v]; tong_b=[x for v in b for x in v]
    print(f"\n{ten}\n  TONG  hoc {tk(tong_a)} || kiem tra {tk(tong_b)}")
    print("  "+" | ".join(f"{s} {t.upper()}: {sum(va)/max(1,len(va)):+.2f}/{sum(vb)/max(1,len(vb)):+.2f}" for (s,t),va,vb in zip(BO,a,b)))
