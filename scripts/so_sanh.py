# Vong 24 (03/11/2026): BANG SO SANH CONG BANG cho ETH. Moi ban chay cung bo mo phong von 500 USD (lot that, tran 4%, ao giap),
# cung giai doan. Ban moi chi giu neu HON moc (ban tot nhat dang co).
# Moc ETH = vong 19: RSI 55/45 H1 (khong loc) + H4 (loc phe D1) + MH3a M15.
# Them: moc + cham diem hanh trinh vong 23 (loai tin hieu diem thap).
# Chay: python3 -I so_sanh.py <thu muc data>
import sys,os,datetime as dt,math; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms
from engine import nap,load,SEC
from diem import su_kien,hoc,cham,mot_lenh,DT,M24
from tung_khung import chay as chay_tk
from von500 import mo_phong

def dac_diem(d,i,hg):
  # dac diem hanh trinh tai nen bat ky i (theo huong hg): pha nguoc chieu gan nhat truoc i
  f,s,r,c,h,l,a=d['f'],d['s'],d['r'],d['c'],d['h'],d['l'],d['atr']
  k=i
  while k>60 and hg*(f[k]-s[k])>0: k-=1      # lui ve pha nguoc
  e=k
  while k>60 and hg*(f[k]-s[k])<=0: k-=1
  pha=range(k+1,e+1) if e>k else range(i-1,i)
  lo=min(l[i-49:i+1]); hi=max(h[i-49:i+1]); vt=(c[i]-lo)/(hi-lo) if hi>lo else .5
  return dict(sau=max(0,max(-hg*(f[q]-s[q]) for q in pha)),dai=math.log(max(2,len(pha))),
    cuc=(min(r[q] for q in pha) if hg>0 else 100-max(r[q] for q in pha)),
    docf=hg*(f[i]-f[i-3]),docs=hg*(s[i]-s[i-3]),rs=hg*(r[i]-s[i]),bd=a[i]/c[i]*100,vt=(vt if hg>0 else 1-vt))

if __name__=='__main__':
  dd_=sys.argv[1]
  # model diem (hoc truoc 2024, BTC+ETH, H1/H4/D1) nhu vong 23
  E=[]
  for sym in ('BTC','ETH'):
    for tf in ('1h','4h','1d'): E+=su_kien(nap(load(f"{dd_}/{sym}_{tf}.csv")),SEC[tf],sym,tf)
  _,M=hoc([e for e in E if e['t']<M24])
  for e in E: e['diem']=cham(e,M)
  # moc vong 19 tren ETH M15 tu 2022
  src=load_ms(f"{dd_}/ETH_15m.csv"); R.TS.clear(); R.TS.update(k2=55)
  moc=[]
  for sec,lon,kieu,loc in ((3600,14400,'K2','0'),(14400,86400,'K2','D'),(900,3600,'K5','0')):
    d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d)
    # them f/s/atr de cham diem
    from lib import ema
    from rsi import wma
    d['f']=ema(d['rsi'],9); d['s']=wma(d['rsi'],45)
    tr=[d['h'][0]-d['l'][0]]+[max(d['h'][q]-d['l'][q],abs(d['h'][q]-d['c'][q-1]),abs(d['l'][q]-d['c'][q-1])) for q in range(1,d['n'])]
    d['atr']=ema(tr,14); d['r']=d['rsi']
    for x in R.chay(d,kieu,loc,ph):
      x.update(dac_diem(d,x['i'],x['h'])); x['diem']=cham(x,M); x['sym']='ETH'; x['tf']=f"{kieu}{sec}"; moc.append(x)
  # ban vong 22 va 23 (ETH H4+D1)
  D={tf:nap(load(f"{dd_}/ETH_{tf}.csv")) for tf in ('4h','1d')}
  v22=chay_tk(D['4h'],SEC['4h'],'E3')+chay_tk(D['1d'],SEC['1d'],'E1')
  v23=mot_lenh([e for e in E if e['sym']=='ETH' and e['tf'] in ('4h','1d') and e['diem']>0])
  cuoi=max(x['t'] for x in moc)
  GD=[('12 thang gan',cuoi-int(12*30.5*86400),cuoi+1),('6 thang gan',cuoi-int(6*30.5*86400),cuoi+1),('3 thang gan',cuoi-int(3*30.5*86400),cuoi+1),
      ('2024 (ca nam)',dt.datetime(2024,1,1).timestamp(),dt.datetime(2025,1,1).timestamp()),('2023 (ca nam)*',dt.datetime(2023,1,1).timestamp(),dt.datetime(2024,1,1).timestamp())]
  BAN=[('MOC v19 RSI55/45 H1+H4D+MH3a M15',moc),('v19 + bo diem thap (diem>-0,15)',[x for x in moc if x['diem']>-0.15]),('v19 + chi diem>0',[x for x in moc if x['diem']>0]),
       ('v22 ETH H4E3+D1E1',v22),('v23 ETH H4+D1 diem>0',v23)]
  print("ETH, von 500 USD moi giai doan, lot that (min 0,1 ETH - gia dinh), rui ro 2% (H4/D1 3%), thua 3 nghi 8h. (*2023: diem da hoc tren nam nay)")
  for ten,tu,den in GD:
    print(f"\n--- {ten}")
    for b,L in BAN:
      print(f"  {b:36s} | {mo_phong([x for x in L if tu<=x['t']<den],'ETH')}")
