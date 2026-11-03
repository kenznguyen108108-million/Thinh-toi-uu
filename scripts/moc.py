# VIEC CLOUD (03/11/2026): MOC chung cho moi viec 1-7 = he ETH vong 30:
#   MUA H1 (RSI cat len 55) + MUA H4 (RSI 55, loc phe D1) + MUA M15 (MH3a) + BAN H1 khi H4 vua cat xuong (gong dinh 40),
#   chi giu top 30% diem hanh trinh (nguong dat tren lenh 2022-23), rui ro 3% (H4 x1,5), tran lot min 6%, thua 3 nghi 8h.
# Dung: from moc import xay, danh_gia ; hoac chay: python3 -I moc.py <data> [SYM]
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms, ema
from rsi import piv,wma
from ban_thu import chay as chay_v19
from ban_dakhung import dieu_kien, chay as chay_moi
from engine import nap,load,SEC
from diem import su_kien,hoc,cham,M24
from so_sanh import dac_diem
import von500
from von500 import mo_phong

_M=None
def mo_hinh(dd_):
  # mo hinh diem vong 23 (hoc BTC+ETH H1/H4/D1 truoc 2024) - giu nguyen nhu moc
  global _M
  if _M is None:
    E=[]
    for sym in ('BTC','ETH'):
      for tf in ('1h','4h','1d'): E+=su_kien(nap(load(f"{dd_}/{sym}_{tf}.csv")),SEC[tf],sym,tf)
    _,_M=hoc([e for e in E if e['t']<M24])
  return _M

def atr_(d):
  tr=[d['h'][0]-d['l'][0]]+[max(d['h'][q]-d['l'][q],abs(d['h'][q]-d['c'][q-1]),abs(d['l'][q]-d['c'][q-1])) for q in range(1,d['n'])]
  return ema(tr,14)

def xay(dd_,sym='ETH',ban_m15=False,tra_ve_khung=False,them_mua=False):
  # tra danh sach TAT CA tin hieu (da cham diem 'diem', dong thuan 'dt', 'phan'), chua loc top 30%
  M=mo_hinh(dd_)
  DL={tf:nap(load(f"{dd_}/{sym}_{tf}.csv")) for tf in ('1h','4h','1d')}
  def huong_tren(tf,T):
    D=DL[tf]; k=bisect.bisect_right(D['t'],T-SEC[tf])-1
    return 1 if D['f'][k]>D['s'][k] else -1
  src=load_ms(f"{dd_}/{sym}_15m.csv"); R.TS.clear(); R.TS.update(k2=55)
  Dd=R.agg(*src,86400)[:-1]; dc=[b[4] for b in Dd]; e2=ema(dc,200); m200={b[0]//86400:(1 if dc[k]>e2[k] else -1) for k,b in enumerate(Dd)}
  L=[]; KH={}
  for ten,sec,lon,kieu,loc in (('H1',3600,14400,'K2','0'),('H4',14400,86400,'K2','D'),('M15',900,3600,'K5','0')):
    d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d); d['dinh5'],d['day5']=piv(d['h'],d['l'],5)
    d['f']=ema(d['rsi'],9); d['s']=wma(d['rsi'],45); d['r']=d['rsi']; d['atr']=atr_(d); d['ph']=ph
    KH[ten]=d
    for x in chay_v19(d,kieu,loc,ph,'goc',ten,[m200.get((t+sec)//86400-1,0) for t in d['t']]):
      if x['h']>0 or (ten=='M15' and ban_m15):
        x.update(dac_diem(d,x['i'],x['h'])); L.append(x)
  moi=chay_moi(DL['1h'],3600,DL['4h'],14400,dieu_kien(DL['4h'],2,0),'ngay','G40')
  for x in moi: x.update(dac_diem(DL['1h'],x['i'],-1)); x['sec']=3601; x['phan']='H1ban'; L.append(x)
  if them_mua:   # viec 1 (GIU): MUA H1 khi H4 vua cat len (K2 X0), vao RSI H1 cat len 55, gong day 40
    from viec1_mua_dakhung import dieu_kien_len,chay as chay_len
    for x in chay_len(DL['1h'],3600,DL['4h'],14400,dieu_kien_len(DL['4h'],2,0),'rsi55','G40'):
      if x['t']>=src[0][0]//1000+86400*10: x.update(dac_diem(DL['1h'],x['i'],1)); L.append(x)
  for x in L:
    x['diem']=cham(x,M); x['dt']=sum(1 for tf in ('4h','1d') if huong_tren(tf,x['t'])==x['h'])
  if tra_ve_khung: return L,KH,DL
  return L

def nguong(L,p=0.3,tu=2022,den=2024):
  a,b=dt.datetime(tu,1,1).timestamp(),dt.datetime(den,1,1).timestamp()
  v=sorted(x['diem'] for x in L if a<=x['t']<b and x.get('phan')!='H1mua')
  return v[int(len(v)*(1-p))]

def chon(L,q):
  # loc top diem; neu co lenh MUA moi (H1mua) cung nen voi MUA H1 cu -> bo lenh cu (khong gap doi rui ro)
  G=[x for x in L if x['diem']>=q]; tm={x['t'] for x in G if x.get('phan')=='H1mua'}
  return [x for x in G if not (x['phan']=='H1' and x['h']>0 and x['t'] in tm)]

NAM=[(str(y),dt.datetime(y,1,1).timestamp(),dt.datetime(y+1,1,1).timestamp()) for y in range(2022,2027)]
def tach(s):
  return int(s.split('(')[2].split(')')[0]), int(s.split('sut tu dinh')[1].split('%')[0]), int(s.split('lenh')[0])

def danh_gia(L,sym='ETH',rr=3.0,tran=None):
  # tra dict: tung nam (500 USD/nam): (usd, sut%, so lenh); 'kep' = lai kep 500 tu 2022 -> nay: (von cuoi, sut%)
  tran=tran or max(4.0,rr*2); out={}
  for y,a,b in NAM:
    out[y]=tach(mo_phong([x for x in L if a<=x['t']<b],sym,rr=rr,tran=tran))
  a=NAM[0][1]; u,s,n=tach(mo_phong([x for x in L if x['t']>=a],sym,rr=rr,tran=tran)); out['kep']=(500+u,s,n)
  out['cong']=sum(out[y][0] for y,_,_ in NAM)
  return out

def dong(ten,o):
  return f"| {ten} | "+" | ".join(f"{o[y][0]:+d} ({o[y][1]}%)" for y,_,_ in NAM)+f" | {o['cong']:+d} | {o['kep'][0]:,} ({o['kep'][1]}%) | {o['kep'][2]} |"
TIEU_DE="| Bản | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | Lãi kép 500 từ 2022 (sụt) | Lệnh |\n|---|---|---|---|---|---|---|---|---|"

if __name__=='__main__':
  dd_=sys.argv[1]; sym=sys.argv[2] if len(sys.argv)>2 else 'ETH'
  L=xay(dd_,sym); q=nguong(L)
  print(TIEU_DE); print(dong(f'MOC {sym} top30% 3% (vong 30)',danh_gia(chon(L,q),sym)))
  L=xay(dd_,sym,them_mua=True); print(dong(f'MOC-1 {sym} (+ MUA H1 khi H4 vua cat len)',danh_gia(chon(L,q),sym)))
