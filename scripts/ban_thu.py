# Vong 26b (03/11/2026): sua RIENG chieu BAN cua moc v19 ETH (MUA giu nguyen), kiem tung nam 2022-2026 + von 500 USD.
# Ly do (phan_tich_v19.py): nam sap 2022 lenh ban chi +27R; ban thang ra TB 1,5R trong khi da di dung ~3R;
# 2023 (+91%) ban lo -40R, 72% lenh ban thua luc gia tren EMA200 D1.
# Cac cach thu cho lenh BAN:
#   goc        nen tang: keo SL swing 10 + khoa 2R/50%
#   khong_khoa bo khoa loi, chi keo SL swing 10
#   donchianN  bo khoa, SL = dinh cao nhat N nen (gong song giam, giong ban D1 cua bot A)
#   keo5       keo SL swing 5 nen + khoa 2R/50%
#   duoi200    chi BAN khi gia D1 duoi EMA200 D1 (thi truong giam that)
#   bo_H1      khong BAN o H1
# Chay: python3 -I ban_thu.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms, ema
from rsi import wma,piv,sl_dau,PHI,SL_MIN
from von500 import mo_phong

def mo_ban(d,sig,cach):
  o,h,l,c=d['o'],d['h'],d['l'],d['c']; vao=c[sig]; sl=sl_dau(d,sig,-1,vao)
  if sl is None: return None
  Rr=sl-vao
  if Rr<SL_MIN*vao: return None
  W=5 if cach=='keo5' else 10; dinh,day=(d['dinh5'],d['day5']) if W==5 else (d['dinh10'],d['day10'])
  khoa=cach in ('goc','keo5','duoi200','bo_H1'); N=int(cach[8:]) if cach.startswith('donchian') else 0
  best=vao; st=0; m1=m1b=0; tr=0; ds=[]
  for b in range(sig+1,d['n']):
    if h[b]>=sl: return ((vao-max(sl,o[b]))-PHI*vao)/Rr,b
    best=min(best,l[b])
    if N:
      if b-N>sig: sl=min(sl,max(h[b-N+1:b+1]))
      continue
    cc=b-W
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
    if khoa and vao-best>=2*Rr: sl=min(sl,vao-0.5*(vao-best))
  return ((vao-c[-1])-PHI*vao)/Rr,d['n']-1

def chay(d,kieu,loc,ph,cach,phan,d200):
  res=[]; ban={1:-1,-1:-1}
  for i in range(220,d['n']-1):
    s=R.tin_hieu(d,i,kieu,loc,ph)
    if not s or i<=ban[s]: continue
    if s<0:
      if cach=='bo_H1' and phan=='H1': continue
      if cach=='duoi200' and d200[i]!=-1: continue
      x=mo_ban(d,i,cach)
    else: x=R.mo(d,i,1)
    if x:
      kc=abs(d['c'][i]-sl_dau(d,i,s,d['c'][i]))
      res.append(dict(t=d['t'][i]+d['sec'],tra=d['t'][x[1]]+d['sec'],R=x[0],h=s,sec=d['sec'],kc=kc,phan=phan,i=i)); ban[s]=x[1]
  return res

if __name__=='__main__':
  src=load_ms(f"{sys.argv[1]}/ETH_15m.csv"); R.TS.clear(); R.TS.update(k2=55)
  Dd=R.agg(*src,86400)[:-1]; dc=[b[4] for b in Dd]; e2=ema(dc,200); m200={b[0]//86400:(1 if dc[k]>e2[k] else -1) for k,b in enumerate(Dd)}
  KH=[]
  for ten,sec,lon,kieu,loc in (('H1',3600,14400,'K2','0'),('H4',14400,86400,'K2','D'),('M15',900,3600,'K5','0')):
    d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d)
    d['dinh5'],d['day5']=piv(d['h'],d['l'],5)
    d200=[m200.get((t+sec)//86400-1,0) for t in d['t']]
    KH.append((ten,d,kieu,loc,ph,d200))
  NAM=[(y,dt.datetime(y,1,1).timestamp(),dt.datetime(y+1,1,1).timestamp()) for y in range(2022,2027)]
  print("Lenh BAN theo nam (R) | MUA giu nguyen. Von 500 USD moi nam cho ca he (MUA+BAN). ETH gia: 2022 -67%, 2023 +91%, 2024 +46%, 2025 -11%, 2026 -24%")
  for cach in ('goc','khong_khoa','donchian10','donchian20','donchian40','keo5','duoi200','bo_H1'):
    L=[x for ten,d,kieu,loc,ph,d200 in KH for x in chay(d,kieu,loc,ph,cach,ten,d200)]
    ban=[x for x in L if x['h']<0]
    dong=" | ".join(f"{y}: {sum(x['R'] for x in ban if a<=x['t']<b):+6.1f}R" for y,a,b in NAM)
    tien=" | ".join(f"{y}: {mo_phong([x for x in L if a<=x['t']<b],'ETH').split('(')[2].split(')')[0].strip():>6s}" for y,a,b in NAM)
    print(f"\n{cach:11s} BAN {len(ban)}L tong {sum(x['R'] for x in ban):+6.1f}R | {dong}\n{'':11s} USD (500/nam): {tien}")
