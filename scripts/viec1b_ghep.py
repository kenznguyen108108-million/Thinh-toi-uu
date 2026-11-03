# VIEC CLOUD 1b: kiem tra ung vien MUA H1 khi H4 vua cat len (vao RSI cat len 55, gong day 40) + lan can, co tinh TRUNG lenh voi MUA H1 cu.
# "GHEP khong trung" = them luat moi, bo lenh MUA H1 cu vao CUNG nen voi lenh moi (tranh gap doi rui ro).
# Chay: python3 -I viec1b_ghep.py <data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load
from so_sanh import dac_diem
from viec1_mua_dakhung import dieu_kien_len,chay,M22
import moc
from moc import xay,nguong,danh_gia,dong,TIEU_DE,cham,mo_hinh
dd_=sys.argv[1]
L0,KH,DL=xay(dd_,'ETH',tra_ve_khung=True); q=nguong(L0); M=mo_hinh(dd_)
MOC=[x for x in L0 if x['diem']>=q]; cu=[x for x in MOC if x['phan']=='H1' and x['h']>0]
print(TIEU_DE); print(dong('MOC',danh_gia(MOC)))
for K,X,vao,th in ((2,0,'rsi55','G40'),(4,0,'rsi55','G40'),(2,3,'rsi55','G40'),(2,0,'rsi55','NT'),(2,0,'ngay','G40')):
  moi=[x for x in chay(DL['1h'],3600,DL['4h'],14400,dieu_kien_len(DL['4h'],K,X),vao,th) if x['t']>=M22]
  for x in moi: x.update(dac_diem(DL['1h'],x['i'],1)); x['diem']=cham(x,M)
  m30=[x for x in moi if x['diem']>=q]; tm={x['t'] for x in m30}
  trung=sum(1 for x in cu if x['t'] in tm)
  tk=f"K{K} X{X} {vao} {th}"
  print(dong(f'THEM {tk} (top30)',danh_gia(MOC+m30)))
  print(dong(f'GHEP khong trung {tk} (top30, bo {trung} lenh cu trung nen)',danh_gia([x for x in MOC if not (x['phan']=='H1' and x['h']>0 and x['t'] in tm)]+m30)))
  print(dong(f'THAY MUA H1 cu bang {tk} (top30)',danh_gia([x for x in MOC if not (x['phan']=='H1' and x['h']>0)]+m30)))
  for y in range(2022,2027):
    g=[x for x in m30 if dt.datetime.utcfromtimestamp(x['t']).year==y]
  print(f"  luat moi top30: {len(m30)}L, R/lenh theo nam: "+" | ".join(f"{y}: {len(g)}L {sum(x['R'] for x in g)/max(1,len(g)):+.2f}" for y in range(2022,2027) for g in [[x for x in m30 if dt.datetime.utcfromtimestamp(x['t']).year==y]]),flush=True)
# rui ro tuong duong: MOC voi rr 3,3% (cung so lenh tang) de xem loi the khong chi do rui ro
print(dong('MOC rui ro 3,5% (doi chieu)',danh_gia(MOC,rr=3.5)))
