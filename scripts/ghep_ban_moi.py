# Vong 28b: ghep luat BAN moi (BAN H1 ngay khi H4 vua cat xuong, gong dinh 40 nen) vao moc v19 ETH, so theo nam (500 USD/nam).
# Chay: python3 -I ghep_ban_moi.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms, ema
from rsi import piv
from ban_thu import chay as chay_v19
from ban_dakhung import dieu_kien, chay as chay_moi
from engine import nap,load,SEC
from von500 import mo_phong
dd_=sys.argv[1]
src=load_ms(f"{dd_}/ETH_15m.csv"); R.TS.clear(); R.TS.update(k2=55)
Dd=R.agg(*src,86400)[:-1]; dc=[b[4] for b in Dd]; e2=ema(dc,200); m200={b[0]//86400:(1 if dc[k]>e2[k] else -1) for k,b in enumerate(Dd)}
v19=[]
for ten,sec,lon,kieu,loc in (('H1',3600,14400,'K2','0'),('H4',14400,86400,'K2','D'),('M15',900,3600,'K5','0')):
  d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d); d['dinh5'],d['day5']=piv(d['h'],d['l'],5)
  v19+=chay_v19(d,kieu,loc,ph,'goc',ten,[m200.get((t+sec)//86400-1,0) for t in d['t']])
D={tf:nap(load(f"{dd_}/ETH_{tf}.csv")) for tf in ('1h','4h')}
moi=chay_moi(D['1h'],3600,D['4h'],14400,dieu_kien(D['4h'],2,0),'ngay','G40')
for x in moi: x['sec']=3601
mua=[x for x in v19 if x['h']>0]; ban_m15=[x for x in v19 if x['h']<0 and x['phan']=='M15']
BAN=[('MOC v19',v19),('v19 MUA + BAN M15 cu + BAN moi H1',mua+ban_m15+moi),('v19 MUA + BAN moi H1',mua+moi),('v19 day du + BAN moi H1',v19+moi)]
NAM=[(str(y),dt.datetime(y,1,1).timestamp(),dt.datetime(y+1,1,1).timestamp()) for y in range(2022,2027)]
cuoi=max(x['t'] for x in v19); NAM+=[('12T gan',cuoi-365*86400,cuoi+1),('6T gan',cuoi-183*86400,cuoi+1)]
print("ETH, von 500 USD moi giai doan. Gia: 2022 -67%, 2023 +91%, 2024 +46%, 2025 -11%, 2026 -24%")
for ten,L in BAN:
  tong=0; dong=[]
  for y,a,b in NAM:
    s=mo_phong([x for x in L if a<=x['t']<b],'ETH'); usd=int(s.split('(')[2].split(')')[0]); sut=s.split('sut tu dinh')[1].split('%')[0].strip()
    if y.isdigit(): tong+=usd
    dong.append(f"{y}: {usd:+5d} (sut {sut}%)")
  print(f"\n{ten}  | cong 5 nam {tong:+d}\n  "+" | ".join(dong))
