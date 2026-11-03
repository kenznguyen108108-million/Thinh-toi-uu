# VIEC CLOUD 5 (03/11/2026): loc bien dong thap. ATR% D1 = ATR14 D1 / gia dong (nen D1 da dong luc vao lenh).
# Chon nguong tren 2018-2021: dung cac tin hieu co du lieu tu 2018 (H1 1h: RSI cat 55/45 khong loc, BAN H1 khi H4 vua cat xuong,
#   MUA H1 khi H4 vua cat len) -> R/lenh theo nhom ATR% D1. Roi ap len MOC-1 2022-2026: NGHI (bo lenh) hoac GIAM rui ro 1/2.
# Chay: python3 -I viec5_bien_dong.py <data>
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from engine import nap,load,SEC
from ban_dakhung import dieu_kien,chay as chay_ban
from viec1_mua_dakhung import dieu_kien_len,chay as chay_mua
from moc import xay,nguong,chon,danh_gia,dong,TIEU_DE
dd_=sys.argv[1]
DL={tf:nap(load(f"{dd_}/ETH_{tf}.csv")) for tf in ('1h','4h','1d')}
D=DL['1d']; atrp=[D['atr'][k]/D['c'][k]*100 for k in range(D['n'])]
def ad(T): return atrp[bisect.bisect_right(D['t'],T-86400)-1]
M22=dt.datetime(2022,1,1).timestamp(); M18=dt.datetime(2018,3,1).timestamp()
# tin hieu 1h tu 2018: RSI 55/45 tren 1h (giong MUA H1 / ban doi xung cu), ban H1 moi, mua H1 moi
d=DL['1h']; d['rsi']=d['r']; d['e200']=R.ema(d['c'],200) if hasattr(R,'ema') else d['c']; d['sec']=3600
T=[]
for i in range(220,d['n']-1):
  r=d['r']
  if r[i-1]<55<=r[i]:
    x=R.mo(d,i,1)
    if x: T.append(dict(t=d['t'][i]+3600,R=x[0],ten='RSI55 MUA H1'))
T+= [dict(x,ten='BAN H1 (H4 vua cat xuong)') for x in chay_ban(d,3600,DL['4h'],14400,dieu_kien(DL['4h'],2,0),'ngay','G40')]
T+= [dict(x,ten='MUA H1 (H4 vua cat len)') for x in chay_mua(d,3600,DL['4h'],14400,dieu_kien_len(DL['4h'],2,0),'rsi55','G40')]
hoc=[x for x in T if M18<=x['t']<M22]; kt=[x for x in T if x['t']>=M22]
v=sorted(ad(x['t']) for x in hoc)
print("ATR% D1 ETH theo nam (TB): "+" ".join(f"{y}:{sum(a for k,a in enumerate(atrp) if dt.datetime.utcfromtimestamp(D['t'][k]).year==y)/max(1,sum(1 for k in range(D['n']) if dt.datetime.utcfromtimestamp(D['t'][k]).year==y)):.1f}%" for y in range(2018,2027)))
print("\n=== R/lenh theo nhom ATR% D1 (2018-21 = chon | 2022-26 = kiem tra)")
BIN=[(0,3),(3,3.5),(3.5,4),(4,4.5),(4.5,5),(5,6),(6,8),(8,99)]
for ten in ('RSI55 MUA H1','BAN H1 (H4 vua cat xuong)','MUA H1 (H4 vua cat len)',None):
  out=[]
  for a,b in BIN:
    g=[x['R'] for x in hoc if (ten is None or x['ten']==ten) and a<=ad(x['t'])<b]; h=[x['R'] for x in kt if (ten is None or x['ten']==ten) and a<=ad(x['t'])<b]
    out.append(f"{a}-{b}%: {len(g)}L {sum(g)/max(1,len(g)):+.2f} | {len(h)}L {sum(h)/max(1,len(h)):+.2f}")
  print(f" {ten or 'TAT CA'}:\n    "+"\n    ".join(out))
# chon nguong tren 2018-21: nguong lon nhat sao cho nhom duoi nguong co R/lenh < 0 (tat ca tin hieu)
ung=[]
for th in (2.5,3,3.5,4,4.5,5):
  g=[x['R'] for x in hoc if ad(x['t'])<th]
  ung.append((th,len(g),sum(g)/max(1,len(g))))
print("\nNhom duoi nguong, 2018-21 (nguong, so lenh, R/lenh):",[(a,n,round(r,2)) for a,n,r in ung])
L=xay(dd_,'ETH',them_mua=True); q=nguong(L); G=chon(L,q)
for x in G: x['atrd']=ad(x['t'])
print("\n=== Ap len MOC-1\n"+TIEU_DE); print(dong('MOC-1',danh_gia(G)))
for th in (3,3.5,4,4.5):
  print(dong(f'NGHI khi ATR% D1 < {th}%',danh_gia([x for x in G if x['atrd']>=th])))
  print(dong(f'rui ro 1/2 khi ATR% D1 < {th}%',danh_gia([dict(x,hs=0.5 if x['atrd']<th else 1.0) for x in G])),flush=True)
