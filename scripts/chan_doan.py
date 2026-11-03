# Vong 25 (03/11/2026): RA TUNG LENH (y anh): thua dung hay thua sai, thang an may R, tra lai bao nhieu, entry tre khong.
# Doi tuong: tin hieu hanh trinh RSI moi khung doc lap (vong 22/23), ETH H4+D1 va BTC H1/H4/D1, ca 2 chieu, tu 2018.
# Phan loai lenh THUA (theo thu tu uu tien):
#   quet_nhanh  ra trong <= 3 nen            sl_hep    1R < 0,5 ATR
#   vao_tre     gia da chay > 2 ATR tu cuc tri pha truoc luc vao
#   co_lai      da len >= 1R roi quay ve thua (thua do quan ly lenh)
#   thua_dung   con lai: dung luat, thi truong di nguoc
# Chay: python3 -I chan_doan.py <thu muc data>
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rsi as RS
from engine import nap,load,SEC
from diem import su_kien,hoc,cham,M24

def bo_sung(d,E):
  h,l,c,a,f,s=d['h'],d['l'],d['c'],d['atr'],d['f'],d['s']
  for e in E:
    i=e['i']; hg=e['h']; R=e['kc']; vao=c[i]
    j=i
    while j>0 and d['t'][j]+e['sec']<e['tra']: j+=1
    e['nen']=j-i
    seg=range(i+1,min(j,d['n']-1)+1)
    if hg>0: e['mfe']=(max(h[q] for q in seg)-vao)/R if seg else 0; e['mae']=(vao-min(l[q] for q in seg))/R if seg else 0
    else:    e['mfe']=(vao-min(l[q] for q in seg))/R if seg else 0; e['mae']=(max(h[q] for q in seg)-vao)/R if seg else 0
    # cuc tri pha truoc
    k=i-1
    while k>60 and hg*(f[k]-s[k])<=0: k-=1
    pha=range(k+1,i+1)
    cuc=min(l[q] for q in pha) if hg>0 else max(h[q] for q in pha)
    e['chay']=hg*(vao-cuc)/a[i]          # gia da chay bao nhieu ATR tu day/dinh
    e['sl_atr']=R/a[i]
    if e['R']>0: e['loai']='thang'
    elif e['nen']<=3: e['loai']='quet_nhanh'
    elif e['sl_atr']<0.5: e['loai']='sl_hep'
    elif e['chay']>2: e['loai']='vao_tre'
    elif e['mfe']>=1: e['loai']='co_lai'
    else: e['loai']='thua_dung'

def bao_cao(ten,E):
  if not E: return
  T=[e for e in E if e['R']>0]; L=[e for e in E if e['R']<=0]
  print(f"\n===== {ten}: {len(E)} lenh, thang {len(T)} ({100*len(T)/len(E):.0f}%), tong {sum(e['R'] for e in E):+.1f}R, TB {sum(e['R'] for e in E)/len(E):+.3f}R")
  bk=[(0,0.5),(0.5,1),(1,2),(2,3),(3,5),(5,99)]
  print("  THANG an duoc: "+" | ".join(f"{a}-{b}R: {sum(1 for e in T if a<e['R']<=b)}" for a,b in bk))
  if T: print(f"  THANG: R TB {sum(e['R'] for e in T)/len(T):.2f}, len cao nhat TB {sum(e['mfe'] for e in T)/len(T):.2f}R -> tra lai TB {sum(e['mfe']-e['R'] for e in T)/len(T):.2f}R/lenh; lenh len >=2R: {sum(1 for e in T if e['mfe']>=2)} lenh, ra TB {sum(e['R'] for e in T if e['mfe']>=2)/max(1,sum(1 for e in T if e['mfe']>=2)):.2f}R (len TB {sum(e['mfe'] for e in T if e['mfe']>=2)/max(1,sum(1 for e in T if e['mfe']>=2)):.2f}R)")
  for k in ('quet_nhanh','sl_hep','vao_tre','co_lai','thua_dung'):
    g=[e for e in L if e['loai']==k]
    if g: print(f"  THUA {k:10s}: {len(g):4d} ({100*len(g)/max(1,len(L)):3.0f}% so lenh thua) tong {sum(e['R'] for e in g):+7.1f}R, da len TB {sum(e['mfe'] for e in g)/len(g):.2f}R")
  print("  ENTRY: gia da chay tu cuc tri pha truoc (ATR) -> R TB:  "+" | ".join(f"{a}-{b}: {len(g)}L {sum(e['R'] for e in g)/len(g):+.2f}" for a,b in ((0,0.5),(0.5,1),(1,1.5),(1.5,2),(2,3),(3,99)) for g in [[e for e in E if a<=e['chay']<b]] if g))
  print("  SL: 1R/ATR -> R TB:  "+" | ".join(f"{a}-{b}: {len(g)}L {sum(e['R'] for e in g)/len(g):+.2f}" for a,b in ((0,0.5),(0.5,1),(1,1.5),(1.5,2.5),(2.5,99)) for g in [[e for e in E if a<=e['sl_atr']<b]] if g))

if __name__=='__main__':
  dd_=sys.argv[1]; E=[]; DD={}
  for sym in ('BTC','ETH'):
    for tf in ('1h','4h','1d'):
      d=nap(load(f"{dd_}/{sym}_{tf}.csv")); DD[(sym,tf)]=d
      ev=su_kien(d,SEC[tf],sym,tf); bo_sung(d,ev); E+=ev
  _,M=hoc([e for e in E if e['t']<M24])
  for e in E: e['diem']=cham(e,M)
  for sym,tfs in (('ETH',('4h','1d')),('BTC',('1h','4h','1d'))):
    for diem in (False,True):
      g=[e for e in E if e['sym']==sym and e['tf'] in tfs and (e['diem']>0 or not diem)]
      bao_cao(f"{sym} {'+'.join(tfs)} {'diem>0' if diem else 'tat ca'} (2018->nay)",g)
