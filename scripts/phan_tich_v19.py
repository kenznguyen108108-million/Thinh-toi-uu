# Vong 26 (03/11/2026): vi sao moc v19 (ETH RSI 55/45) lo nang 2023-2024? Tach theo nam x phan x chieu, ra lenh BAN thua.
# Boi canh thi truong luc vao (D1): phe giam (EMA10<EMA20 & gia duoi ca 2) / phe tang / lung chung; gia so voi EMA200 D1.
# Chay: python3 -I phan_tich_v19.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as R
from lib import load as load_ms, ema
from rsi import wma
from chan_doan import bo_sung

def dung_v19(src):
  R.TS.clear(); R.TS.update(k2=55); out=[]
  # D1 de lay boi canh EMA200
  D=R.agg(*src,86400)[:-1]; dc=[b[4] for b in D]; e200=ema(dc,200); dmap={b[0]//86400:(dc[k],e200[k]) for k,b in enumerate(D)}
  for ten,sec,lon,kieu,loc in (('H1',3600,14400,'K2','0'),('H4',14400,86400,'K2','D'),('M15',900,3600,'K5','0')):
    d=R.khung(src,sec); ph=R.phe_d1(src,d); d['lon']=R.lon_thuan(src,d,lon); d['mom']=R.quan_tinh(d)
    d['f']=ema(d['rsi'],9); d['s']=wma(d['rsi'],45); d['r']=d['rsi']
    tr=[d['h'][0]-d['l'][0]]+[max(d['h'][q]-d['l'][q],abs(d['h'][q]-d['c'][q-1]),abs(d['l'][q]-d['c'][q-1])) for q in range(1,d['n'])]
    d['atr']=ema(tr,14)
    L=R.chay(d,kieu,loc,ph); bo_sung(d,L)
    for x in L:
      x['phan']=ten; x['phe']=ph[x['i']]
      c200=dmap.get((d['t'][x['i']]+sec)//86400-1)
      x['e200']=0 if not c200 else (1 if c200[0]>c200[1] else -1)
      out.append(x)
  return out

def nam(x): return dt.datetime.utcfromtimestamp(x['t']).year
def tk(g):
  if not g: return "    -"
  return f"{len(g):4d}L {100*sum(1 for e in g if e['R']>0)/len(g):3.0f}% {sum(e['R'] for e in g):+6.1f}R"

if __name__=='__main__':
  src=load_ms(f"{sys.argv[1]}/ETH_15m.csv"); L=dung_v19(src)
  D1=R.agg(*src,86400); gn={}
  for b in D1:
    y=dt.datetime.utcfromtimestamp(b[0]).year; gn.setdefault(y,[b[1],b[4]]); gn[y][1]=b[4]
  print("ETH gia dau -> cuoi nam: "+" | ".join(f"{y}: {a:.0f}->{c:.0f} ({(c/a-1)*100:+.0f}%)" for y,(a,c) in sorted(gn.items())))
  print("\n=== Nam x phan x chieu (so lenh, % thang, tong R)")
  for y in sorted(set(map(nam,L))):
    print(f" {y}: "+" | ".join(f"{p} {'MUA' if h>0 else 'BAN'} {tk([e for e in L if nam(e)==y and e['phan']==p and e['h']==h])}" for p in ('H1','H4','M15') for h in (1,-1)))
  print("\n=== BAN theo boi canh D1 luc vao (toan ky) -- MUA de doi chieu")
  for h,tn in ((-1,'BAN'),(1,'MUA')):
    for p in ('H1','H4','M15'):
      g=[e for e in L if e['h']==h and e['phan']==p]
      print(f" {tn} {p:3s}: phe D1 giam {tk([e for e in g if e['phe']==-1])} | lung chung {tk([e for e in g if e['phe']==0])} | phe tang {tk([e for e in g if e['phe']==1])} || gia<EMA200 D1 {tk([e for e in g if e['e200']==-1])} | gia>EMA200 {tk([e for e in g if e['e200']==1])}")
  print("\n=== Ra lenh BAN THUA theo nam (loai thua; % so lenh ban thua)")
  for y in sorted(set(map(nam,L))):
    g=[e for e in L if nam(e)==y and e['h']<0 and e['R']<=0]
    if g: print(f" {y}: {len(g)} lenh ban thua, {sum(e['R'] for e in g):+.0f}R | "+" | ".join(f"{k} {100*sum(1 for e in g if e['loai']==k)/len(g):.0f}%" for k in ('quet_nhanh','vao_tre','co_lai','thua_dung','sl_hep'))+f" | ban NGUOC phe D1 (D1 tang) {100*sum(1 for e in g if e['phe']==1)/len(g):.0f}%, gia>EMA200 {100*sum(1 for e in g if e['e200']==1)/len(g):.0f}%")
  print("\n=== Lenh BAN THANG: an may R, len cao nhat bao nhieu (theo nam)")
  for y in sorted(set(map(nam,L))):
    g=[e for e in L if nam(e)==y and e['h']<0 and e['R']>0]
    if g: print(f" {y}: {len(g)} lenh, ra TB {sum(e['R'] for e in g)/len(g):.2f}R, len cao nhat TB {sum(e['mfe'] for e in g)/len(g):.2f}R, lenh >=3R: {sum(1 for e in g if e['R']>=3)}")
