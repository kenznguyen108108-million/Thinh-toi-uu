# VIEC CLOUD 3 (03/11/2026): do ben nguong chat luong cua MOC-1.
# A: top 20/25/30/35/40% (nguong dat tren lenh 2022-23, mo hinh diem hoc truoc 2024 nhu MOC).
# B: WALK-FORWARD that: moi nam Y (2023..2026) hoc lai mo hinh diem tren su kien < Y va dat nguong tren lenh he 2022..Y-1;
#    nam 2022 khong co lenh truoc do (du lieu M15 tu 2022) -> khong tinh. So voi MOC-1 cung giai doan 2023-2026.
# Chay: python3 -I viec3_nguong.py <data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,SEC
from diem import su_kien,hoc,cham
from moc import xay,nguong,chon,danh_gia,dong,TIEU_DE,tach
from von500 import mo_phong
dd_=sys.argv[1]
L=xay(dd_,'ETH',them_mua=True)
print("=== A: ty le giu (nguong dat tren 2022-23)\n"+TIEU_DE)
for p in (0.2,0.25,0.3,0.35,0.4,0.5):
  print(dong(f'top {int(p*100)}%',danh_gia(chon(L,nguong(L,p)))),flush=True)
# B walk-forward
E=[]
for sym in ('BTC','ETH'):
  for tf in ('1h','4h','1d'): E+=su_kien(nap(load(f"{dd_}/{sym}_{tf}.csv")),SEC[tf],sym,tf)
Y=lambda y:dt.datetime(y,1,1).timestamp()
q30=nguong(L,0.3); MOC=chon(L,q30)
def tk(G,a,b):
  u,s,n=tach(mo_phong([x for x in G if a<=x['t']<b],'ETH',rr=3.0,tran=6.0)); return u,s,n
print("\n=== B: walk-forward (moi nam hoc lai mo hinh + nguong tu cac nam truoc). USD von 500/nam (sut)")
for p in (0.25,0.3,0.35):
  WF=[]; info=[]
  for y in range(2023,2027):
    _,M=hoc([e for e in E if e['t']<Y(y)])
    for x in L: x['dwf']=cham(x,M)
    v=sorted(x['dwf'] for x in L if Y(2022)<=x['t']<Y(y) and x.get('phan')!='H1mua'); q=v[int(len(v)*(1-p))]
    G=[dict(x,diem=x['dwf']) for x in L if Y(y)<=x['t']<Y(y+1)]
    WF+=chon(G,q); info.append(f"{y}: nguong {q:+.2f}")
  r=[tk(WF,Y(y),Y(y+1)) for y in range(2023,2027)]; k=tk(WF,Y(2023),Y(2030))
  print(f"| WF top {int(p*100)}% | "+" | ".join(f"{u:+d} ({s}%)" for u,s,n in r)+f" | cong {sum(u for u,_,_ in r):+d} | lai kep tu 2023 {500+k[0]:,} ({k[1]}%) | {k[2]}L | {'; '.join(info)}",flush=True)
r=[tk(MOC,Y(y),Y(y+1)) for y in range(2023,2027)]; k=tk(MOC,Y(2023),Y(2030))
print(f"| MOC-1 (nguong co dinh 2022-23, mo hinh <2024) | "+" | ".join(f"{u:+d} ({s}%)" for u,s,n in r)+f" | cong {sum(u for u,_,_ in r):+d} | lai kep tu 2023 {500+k[0]:,} ({k[1]}%) | {k[2]}L")
G=[x for x in L]; r=[tk(G,Y(y),Y(y+1)) for y in range(2023,2027)]; k=tk(G,Y(2023),Y(2030))
print(f"| khong loc diem (tat ca) | "+" | ".join(f"{u:+d} ({s}%)" for u,s,n in r)+f" | cong {sum(u for u,_,_ in r):+d} | lai kep tu 2023 {500+k[0]:,} ({k[1]}%) | {k[2]}L")
