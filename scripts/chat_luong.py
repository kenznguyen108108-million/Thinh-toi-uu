# Vong 29 (03/11/2026): VAO IT LENH HON, CHON THOI DIEM CHAT LUONG (y anh). He goc = he tot nhat vong 28:
#   v19 MUA (RSI 55/45 H1, H4 loc D1, MH3a M15) + BAN M15 (MH3a) + BAN H1 khi H4 vua cat xuong (gong dinh 40).
# Cham chat luong tung tin hieu:
#   (a) diem hanh trinh (mo hinh vong 23, hoc tren BTC+ETH H1/H4/D1 truoc 2024)
#   (b) dong thuan: so khung tren (H4, D1) co EMA9(RSI) cung chieu lenh (0/1/2)
# Giu top 70/50/30% theo diem (nguong dat tren lenh 2022-2023), hoac chi dong thuan 2 khung. So tien tung nam (500 USD/nam).
# Chay: python3 -I chat_luong.py <thu muc data>
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms, ema
from rsi import piv,wma
from ban_thu import chay as chay_v19
from ban_dakhung import dieu_kien, chay as chay_moi
from engine import nap,load,SEC
from diem import su_kien,hoc,cham,M24
from so_sanh import dac_diem
from von500 import mo_phong
dd_=sys.argv[1]
E=[]
for sym in ('BTC','ETH'):
  for tf in ('1h','4h','1d'): E+=su_kien(nap(load(f"{dd_}/{sym}_{tf}.csv")),SEC[tf],sym,tf)
_,M=hoc([e for e in E if e['t']<M24])
DL={tf:nap(load(f"{dd_}/ETH_{tf}.csv")) for tf in ('1h','4h','1d')}
def huong_tren(tf,T):
  D=DL[tf]; k=bisect.bisect_right(D['t'],T-SEC[tf])-1
  return 1 if D['f'][k]>D['s'][k] else -1
src=load_ms(f"{dd_}/ETH_15m.csv"); R.TS.clear(); R.TS.update(k2=55)
Dd=R.agg(*src,86400)[:-1]; dc=[b[4] for b in Dd]; e2=ema(dc,200); m200={b[0]//86400:(1 if dc[k]>e2[k] else -1) for k,b in enumerate(Dd)}
L=[]
for ten,sec,lon,kieu,loc in (('H1',3600,14400,'K2','0'),('H4',14400,86400,'K2','D'),('M15',900,3600,'K5','0')):
  d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d); d['dinh5'],d['day5']=piv(d['h'],d['l'],5)
  d['f']=ema(d['rsi'],9); d['s']=wma(d['rsi'],45); d['r']=d['rsi']
  tr=[d['h'][0]-d['l'][0]]+[max(d['h'][q]-d['l'][q],abs(d['h'][q]-d['c'][q-1]),abs(d['l'][q]-d['c'][q-1])) for q in range(1,d['n'])]; d['atr']=ema(tr,14)
  for x in chay_v19(d,kieu,loc,ph,'goc',ten,[m200.get((t+sec)//86400-1,0) for t in d['t']]):
    if x['h']>0 or ten=='M15':
      x.update(dac_diem(d,x['i'],x['h'])); L.append(x)
moi=chay_moi(DL['1h'],3600,DL['4h'],14400,dieu_kien(DL['4h'],2,0),'ngay','G40')
for x in moi: x.update(dac_diem(DL['1h'],x['i'],-1)); x['sec']=3601; x['phan']='H1ban'; L.append(x)
for x in L:
  x['diem']=cham(x,M); x['dt']=sum(1 for tf in ('4h','1d') if huong_tren(tf,x['t'])==x['h'])
M22,M24_=dt.datetime(2022,1,1).timestamp(),dt.datetime(2024,1,1).timestamp()
v=sorted(x['diem'] for x in L if M22<=x['t']<M24_)
NG={p:v[int(len(v)*(1-p))] for p in (0.7,0.5,0.3)}
LOC=[('GOC (tat ca)',lambda x:True)]+[(f'top {int(p*100)}% diem',(lambda q:lambda x:x['diem']>=q)(NG[p])) for p in (0.7,0.5,0.3)]+\
    [('dong thuan H4+D1',lambda x:x['dt']==2),('dong thuan >=1',lambda x:x['dt']>=1),('top 50% + dong thuan>=1',lambda x:x['diem']>=NG[0.5] and x['dt']>=1)]
NAM=[(str(y),dt.datetime(y,1,1).timestamp(),dt.datetime(y+1,1,1).timestamp()) for y in range(2022,2027)]
cuoi=max(x['t'] for x in L); NAM+=[('12T',cuoi-365*86400,cuoi+1)]
print("ETH he tot nhat vong 28, von 500 USD moi giai doan. (nguong diem dat tren lenh 2022-23; 2024->nay la ngoai mau)")
for ten,f in LOC:
  g=[x for x in L if f(x)]; tong=0; out=[]
  for y,a,b in NAM:
    h=[x for x in g if a<=x['t']<b]; s=mo_phong(h,'ETH'); usd=int(s.split('(')[2].split(')')[0]); sut=s.split('sut tu dinh')[1].split('%')[0].strip()
    rl=sum(x['R'] for x in h)/max(1,len(h))
    if y.isdigit(): tong+=usd
    out.append(f"{y}:{len(h):3d}L {rl:+.2f}R/l {usd:+5d}$ s{sut}%")
  print(f"\n{ten:26s} cong 5 nam {tong:+6d}$\n  "+" | ".join(out))

# Vong 29b: it lenh + chat luong cao -> thu tang rui ro moi lenh
print("\n=== Tang rui ro cho ban it lenh (cung luat, chi doi % rui ro; tran lot min 4%)")
for ten,f,rr in (('GOC 2%',lambda x:True,2.0),('dong thuan>=1, 2%',lambda x:x['dt']>=1,2.0),('dong thuan>=1, 3%',lambda x:x['dt']>=1,3.0),
                 ('top 30% diem, 3%',lambda x:x['diem']>=NG[0.3],3.0),('top 30% diem, 4%',lambda x:x['diem']>=NG[0.3],4.0),
                 ('top 30% + dong thuan>=1, 3%',lambda x:x['diem']>=NG[0.3] and x['dt']>=1,3.0)):
  g=[x for x in L if f(x)]; tong=0; out=[]
  for y,a,b in NAM:
    s=mo_phong([x for x in g if a<=x['t']<b],'ETH',rr=rr,tran=max(4.0,rr*2)); usd=int(s.split('(')[2].split(')')[0]); sut=s.split('sut tu dinh')[1].split('%')[0].strip()
    if y.isdigit(): tong+=usd
    out.append(f"{y}: {usd:+5d}$ s{sut}%")
  print(f"{ten:30s} cong 5 nam {tong:+6d}$ | "+" | ".join(out))
