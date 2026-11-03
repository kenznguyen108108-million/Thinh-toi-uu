# VIEC CLOUD 6 (03/11/2026): ap he MOC-1 (cung luat, cung cach dat nguong top 30% tren lenh 2022-23 cua chinh ma do) cho BTC,
# va do tuong quan lai/lo theo thang voi he ETH. Thang = % von theo R x rui ro (3%, H4 x1,5) sau ao giap, khong lai kep.
# Chay: python3 -I viec6_btc.py <data>
import sys,os,datetime as dt,math; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from moc import xay,nguong,chon,danh_gia,dong,TIEU_DE
from rsi import ao_giap
dd_=sys.argv[1]; HE={}
print(TIEU_DE)
for sym in ('ETH','BTC'):
  L=xay(dd_,sym,them_mua=True); q=nguong(L); G=chon(L,q); HE[sym]=G
  print(dong(f'{sym} MOC-1 (nguong {q:+.2f})',danh_gia(G,sym)))
  L0=xay(dd_,sym); print(dong(f'{sym} MOC vong 30',danh_gia(chon(L0,nguong(L0)),sym)),flush=True)
  if sym=='BTC':
    for p in (0.3,0.5,1.01):
      print(dong(f'BTC MOC-1 top {int(min(p,1)*100)}%',danh_gia(chon(L,nguong(L,p) if p<1 else -1e9),sym)))
def thang(G):
  m={}
  for x in ao_giap(G):
    if x['t']<dt.datetime(2022,1,1).timestamp(): continue
    k=dt.datetime.utcfromtimestamp(x['tra']).strftime('%Y-%m'); m[k]=m.get(k,0)+x['R']*3*(1.5 if x['sec']>=14400 else 1)
  return m
a,b=thang(HE['ETH']),thang(HE['BTC']); K=sorted(set(a)|set(b)); x=[a.get(k,0) for k in K]; y=[b.get(k,0) for k in K]
mx,my=sum(x)/len(x),sum(y)/len(y); cov=sum((p-mx)*(q-my) for p,q in zip(x,y)); r=cov/math.sqrt(sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))
am_e=[k for k in K if a.get(k,0)<0]; am_b=[k for k in K if b.get(k,0)<0]; ca2=[k for k in K if a.get(k,0)<0 and b.get(k,0)<0]
print(f"\nTheo thang 2022-nay ({len(K)} thang, % von khong lai kep): tuong quan ETH-BTC = {r:+.2f}")
print(f"  ETH thang am {len(am_e)}, BTC thang am {len(am_b)}, CUNG am {len(ca2)} (neu doc lap ~{len(am_e)*len(am_b)/len(K):.0f})")
print(f"  ETH thang te nhat {min(x):+.1f}% | BTC te nhat {min(y):+.1f}% | gop 50/50 te nhat {min((p+q)/2 for p,q in zip(x,y)):+.1f}%")
print("  10 thang ETH te nhat (ETH% / BTC%): "+", ".join(f"{k} {a.get(k,0):+.0f}/{b.get(k,0):+.0f}" for k in sorted(K,key=lambda k:a.get(k,0))[:10]))
for y_ in range(2022,2027):
  ks=[k for k in K if k.startswith(str(y_))]
  print(f"  {y_}: ETH {sum(a.get(k,0) for k in ks):+6.1f}% | BTC {sum(b.get(k,0) for k in ks):+6.1f}% | cung am {sum(1 for k in ks if k in ca2)}/{len(ks)} thang")
