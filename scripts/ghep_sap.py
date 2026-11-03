# Vong 27b: ghep mo-dun BAN LUC SAP vao moc v19 ETH, so theo nam (von 500 USD/nam, lot that, ao giap chung).
# Chay: python3 -I ghep_sap.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms, ema
from rsi import piv
from ban_thu import chay as chay_v19
from ban_sap import pha_d1, chay as chay_sap
from engine import nap,load,SEC
from von500 import mo_phong
dd_=sys.argv[1]
src=load_ms(f"{dd_}/ETH_15m.csv"); R.TS.clear(); R.TS.update(k2=55)
Dd=R.agg(*src,86400)[:-1]; dc=[b[4] for b in Dd]; e2=ema(dc,200); m200={b[0]//86400:(1 if dc[k]>e2[k] else -1) for k,b in enumerate(Dd)}
v19=[]
for ten,sec,lon,kieu,loc in (('H1',3600,14400,'K2','0'),('H4',14400,86400,'K2','D'),('M15',900,3600,'K5','0')):
  d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d); d['dinh5'],d['day5']=piv(d['h'],d['l'],5)
  v19+=chay_v19(d,kieu,loc,ph,'goc',ten,[m200.get((t+sec)//86400-1,0) for t in d['t']])
D={tf:nap(load(f"{dd_}/ETH_{tf}.csv")) for tf in ('1h','1d')}; P=pha_d1(D['1d'])
CH={'P2T2G40':chay_sap(D['1h'],3600,P,D['1d']['t'],'P2','T2','G40'),'P2T1G20':chay_sap(D['1h'],3600,P,D['1d']['t'],'P2','T1','G20')}
for x in CH['P2T2G40']+CH['P2T1G20']: x['sec']=3601  # khac khung voi v19 H1 (de ao giap/1 lenh tach rieng); rui ro 2%
BAN=[('MOC v19 (MUA+BAN doi xung)',v19),('v19 MUA + sap P2T2G40',[x for x in v19 if x['h']>0]+CH['P2T2G40']),
     ('v19 day du + sap P2T2G40',v19+CH['P2T2G40']),('v19 MUA + sap P2T1G20',[x for x in v19 if x['h']>0]+CH['P2T1G20']),
     ('v19 chi MUA (khong ban)',[x for x in v19 if x['h']>0])]
NAM=[(str(y),dt.datetime(y,1,1).timestamp(),dt.datetime(y+1,1,1).timestamp()) for y in range(2022,2027)]
cuoi=max(x['t'] for x in v19); NAM+=[('12T gan',cuoi-int(365*86400),cuoi+1)]
print("ETH, von 500 USD moi giai doan. Gia: 2022 -67%, 2023 +91%, 2024 +46%, 2025 -11%, 2026 -24%")
for ten,L in BAN:
  print(f"\n{ten}")
  for y,a,b in NAM:
    s=mo_phong([x for x in L if a<=x['t']<b],'ETH'); print(f"  {y:8s} {s.split('|')[1].strip():30s} | {s.split('|')[2].strip()}")
