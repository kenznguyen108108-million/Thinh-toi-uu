# VIEC CLOUD 2 (03/11/2026): ra lenh MUA cua MOC-1 (nhu vong 26 da lam cho BAN): boi canh D1, loai thua, nam nao hong.
# Boi canh luc vao (nen D1 da dong): phe D1 (EMA10/20 + gia), gia vs EMA200 D1, EMA9(RSI D1) vs WMA45, H4 EMA9(RSI) vs WMA45,
#   bien do D1 (ATR14 D1 / gia, %), RSI D1.
# Loai thua (chan_doan.bo_sung): quet_nhanh <=3 nen | sl_hep 1R<0,5ATR | vao_tre gia da chay >2ATR | co_lai da len >=1R | thua_dung.
# Chay: python3 -I viec2_ra_mua.py <data>
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import ema
from chan_doan import bo_sung
from moc import xay,nguong,chon
dd_=sys.argv[1]
L,KH,DL=xay(dd_,'ETH',tra_ve_khung=True,them_mua=True); q=nguong(L); G=chon(L,q)
D=DL['1d']; c=D['c']; e10=ema(c,10); e20=ema(c,20); e200=ema(c,200); atrp=[D['atr'][k]/c[k]*100 for k in range(D['n'])]
def kd(T): return bisect.bisect_right(D['t'],T-86400)-1
D4=DL['4h']
def k4(T): return bisect.bisect_right(D4['t'],T-14400)-1
def boi_canh(x):
  k=kd(x['t']); p=1 if (e10[k]>e20[k] and c[k]>max(e10[k],e20[k])) else (-1 if (e10[k]<e20[k] and c[k]<min(e10[k],e20[k])) else 0)
  j=k4(x['t'])
  x.update(phe=p,e200=1 if c[k]>e200[k] else -1,rd=1 if D['f'][k]>D['s'][k] else -1,h4=1 if D4['f'][j]>D4['s'][j] else -1,
           atrd=atrp[k],rsid=D['r'][k],keo=(c[k]-e20[k])/e20[k]*100)
MUA=[x for x in G if x['h']>0]
for ten in ('H1','H4','M15','H1mua'):
  g=[x for x in MUA if x['phan']==ten]; d=KH[ten] if ten in KH else DL['1h']
  bo_sung(d,g)
for x in MUA: boi_canh(x)
nam=lambda x:dt.datetime.utcfromtimestamp(x['t']).year
def tk(g):
  if not g: return "   -"
  return f"{len(g):3d}L {100*sum(1 for e in g if e['R']>0)/len(g):3.0f}% {sum(e['R'] for e in g):+6.1f}R ({sum(e['R'] for e in g)/len(g):+.2f}/l)"
print("ETH MOC-1, lenh MUA (top 30% diem). Gia nam: 2022 -67%, 2023 +91%, 2024 +46%, 2025 -11%, 2026 -24%")
print("\n=== Nam x phan")
for y in range(2022,2027):
  print(f" {y}: "+" | ".join(f"{p} {tk([e for e in MUA if nam(e)==y and e['phan']==p])}" for p in ('H1','H4','M15','H1mua'))+f" || tong {tk([e for e in MUA if nam(e)==y])}")
print("\n=== Theo boi canh luc vao (2022-23 = tap chon | 2024-26 = kiem tra)")
NH=[('phe D1 tang',lambda e:e['phe']==1),('phe D1 lung chung',lambda e:e['phe']==0),('phe D1 GIAM',lambda e:e['phe']==-1),
    ('gia>EMA200 D1',lambda e:e['e200']==1),('gia<EMA200 D1',lambda e:e['e200']==-1),
    ('RSI D1: EMA9>WMA45',lambda e:e['rd']==1),('RSI D1: EMA9<WMA45',lambda e:e['rd']==-1),
    ('H4: EMA9>WMA45',lambda e:e['h4']==1),('H4: EMA9<WMA45',lambda e:e['h4']==-1),
    ('bien do D1 <3%',lambda e:e['atrd']<3),('bien do D1 3-4,5%',lambda e:3<=e['atrd']<4.5),('bien do D1 >=4,5%',lambda e:e['atrd']>=4.5),
    ('RSI D1 <45',lambda e:e['rsid']<45),('RSI D1 45-60',lambda e:45<=e['rsid']<60),('RSI D1 >=60',lambda e:e['rsid']>=60),
    ('gia cach EMA20 D1 >8%',lambda e:e['keo']>8),('gia duoi EMA20 D1',lambda e:e['keo']<0)]
for ten,f in NH:
  a=[e for e in MUA if f(e) and nam(e)<=2023]; b=[e for e in MUA if f(e) and nam(e)>=2024]
  print(f" {ten:24s} | 22-23: {tk(a)} | 24-26: {tk(b)} | "+" ".join(f"{str(y)[2:]}:{sum(e['R'] for e in MUA if f(e) and nam(e)==y):+5.1f}" for y in range(2022,2027)))
print("\n=== Lenh MUA THUA theo nam: loai thua (% so lenh thua) + boi canh")
for y in range(2022,2027):
  g=[e for e in MUA if nam(e)==y and e['R']<=0]
  if g: print(f" {y}: {len(g)} thua {sum(e['R'] for e in g):+.0f}R | "+" | ".join(f"{k} {100*sum(1 for e in g if e['loai']==k)/len(g):.0f}%" for k in ('quet_nhanh','sl_hep','vao_tre','co_lai','thua_dung'))+
              f" || phe D1 giam {100*sum(1 for e in g if e['phe']==-1)/len(g):.0f}%, <EMA200 {100*sum(1 for e in g if e['e200']==-1)/len(g):.0f}%, RSI D1 giam {100*sum(1 for e in g if e['rd']==-1)/len(g):.0f}%, H4 giam {100*sum(1 for e in g if e['h4']==-1)/len(g):.0f}%")
print("\n=== Lenh MUA THANG theo nam: ra TB, len cao nhat TB")
for y in range(2022,2027):
  g=[e for e in MUA if nam(e)==y and e['R']>0]
  if g: print(f" {y}: {len(g)} thang, ra TB {sum(e['R'] for e in g)/len(g):.2f}R, len cao nhat TB {sum(e['mfe'] for e in g)/len(g):.2f}R, >=3R: {sum(1 for e in g if e['R']>=3)}")

# ---- Viec 2b: de xuat sua (chon tren 2022-23 o tren) -> kiem chung bang von500 tung nam
from moc import danh_gia,dong,TIEU_DE
print("\n=== Kiem chung bo loc MUA (chi ap cho lenh MUA; BAN giu nguyen)\n"+TIEU_DE)
print(dong('MOC-1',danh_gia(G)))
SUA=[('bo MUA khi RSI D1 <45',lambda e:e['rsid']<45),('bo MUA khi RSI D1 <40',lambda e:e['rsid']<40),('bo MUA khi RSI D1 <50',lambda e:e['rsid']<50),
     ('chi MUA khi RSI D1 45-60',lambda e:not 45<=e['rsid']<60),('chi MUA khi RSI D1 45-65',lambda e:not 45<=e['rsid']<65),('chi MUA khi RSI D1 45-70',lambda e:not 45<=e['rsid']<70),
     ('bo MUA khi phe D1 giam',lambda e:e['phe']==-1),('bo MUA khi gia cach EMA20 D1 >8%',lambda e:e['keo']>8),('bo MUA khi gia cach EMA20 D1 >10%',lambda e:e['keo']>10),
     ('bo MUA H1 cu khi RSI D1 <45 (giu M15/H4/H1mua)',lambda e:e['phan']=='H1' and e['rsid']<45)]
for ten,f in SUA:
  print(dong(ten,danh_gia([x for x in G if not (x['h']>0 and f(x))])),flush=True)
