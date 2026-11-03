# VIEC CLOUD 1 (03/11/2026): luat MUA doi xung luat BAN vong 28.
#   MUA H1 khi H4 VUA co EMA9(RSI) cat LEN WMA45(RSI) (trong K nen H4 gan nhat, van dang tren) + doc EMA9 H4 tang >= X diem / 3 nen.
#   Vao: ngay = nen H1 dau tien du dieu kien | rsi55 = RSI H1 cat len 55 | ema = EMA9(RSI) H1 cat len WMA45.
#   Thoat: NT nen tang (keo swing 10 + khoa 2R/50%) | G40 gong theo DAY thap nhat 40 nen (khong khoa loi).
# Phan A: R theo nam 2018-2026 (chon tren 2018-21, kiem tra 2022-26) - ETH va BTC.
# Phan B: ghep vao MOC (vong 30) bang von500: THAY MUA H1 cu / THEM vao. Nguong diem top 30% giu nguyen cua MOC.
# Chay: python3 -I viec1_mua_dakhung.py <data>
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,SEC
from rsi import mo,sl_dau,PHI,SL_MIN
from so_sanh import dac_diem

def dieu_kien_len(Dl,K,X):
  F,S=Dl['f'],Dl['s']; n=Dl['n']; ok=[False]*n; cat=-999
  for k in range(4,n):
    if F[k-1]<=S[k-1] and F[k]>S[k]: cat=k
    ok[k]= F[k]>S[k] and k-cat<K and (F[k]-F[k-3])>=X
  return ok

def mo_g_mua(d,sig,N):
  o,l,c=d['o'],d['l'],d['c']; vao=c[sig]; sl=sl_dau(d,sig,1,vao)
  if sl is None: return None
  Rr=vao-sl
  if Rr<SL_MIN*vao: return None
  for b in range(sig+1,d['n']):
    if l[b]<=sl: return ((min(sl,o[b])-vao)-PHI*vao)/Rr,b
    if b-N>sig: sl=max(sl,min(l[b-N+1:b+1]))
  return ((c[-1]-vao)-PHI*vao)/Rr,d['n']-1

def chay(d,sec,Dl,secl,ok,vao,thoat):
  f,s,r=d['f'],d['s'],d['r']; res=[]; ban=-1; dung=-1
  for i in range(60,d['n']-1):
    if i<=ban: continue
    k=bisect.bisect_right(Dl['t'],d['t'][i]+sec-secl)-1
    if k<4 or not ok[k]: continue
    if vao=='rsi55': t=r[i-1]<55<=r[i]
    elif vao=='ema': t=f[i-1]<=s[i-1] and f[i]>s[i]
    else:
      t=k!=dung and not ok[k-1]
      if t: dung=k
    if not t: continue
    x=mo(d,i,1) if thoat=='NT' else mo_g_mua(d,i,40)
    if x: res.append(dict(t=d['t'][i]+sec,tra=d['t'][x[1]]+sec,R=x[0],h=1,sec=3602,i=i,kc=abs(d['c'][i]-sl_dau(d,i,1,d['c'][i])),phan='H1mua')); ban=x[1]
  return res

def nam(t): return dt.datetime.utcfromtimestamp(t).year
M22=dt.datetime(2022,1,1).timestamp()

if __name__=='__main__':
  dd_=sys.argv[1]; KQ={}
  print("===== PHAN A: R lenh MUA H1 (hoc 2018-21 | kiem tra 2022-26 | tung nam)")
  for sym in ('ETH','BTC'):
    D={tf:nap(load(f"{dd_}/{sym}_{tf}.csv")) for tf in ('1h','4h')}
    for K in (2,4):
      for X in (0,3,6):
        ok=dieu_kien_len(D['4h'],K,X)
        for vao in ('ngay','rsi55','ema'):
          for th in ('NT','G40'):
            L=chay(D['1h'],3600,D['4h'],14400,ok,vao,th); KQ[(sym,K,X,vao,th)]=L
            a=[x['R'] for x in L if x['t']<M22]; b=[x['R'] for x in L if x['t']>=M22]
            yr=" ".join(f"{str(y)[2:]}:{sum(x['R'] for x in L if nam(x['t'])==y):+5.1f}" for y in range(2018,2027))
            print(f"{sym} K{K} X{X} {vao:5s} {th:3s} | hoc {len(a):4d}L {sum(a):+6.1f}R {sum(a)/max(1,len(a)):+.2f}/l | kt {len(b):4d}L {sum(b):+6.1f}R {sum(b)/max(1,len(b)):+.2f}/l | {yr}",flush=True)
  # chon cau hinh ETH tot nhat theo R/lenh tap hoc (>=40 lenh hoc)
  ung=[(sum(x['R'] for x in L if x['t']<M22)/max(1,sum(1 for x in L if x['t']<M22)),k) for k,L in KQ.items() if k[0]=='ETH' and sum(1 for x in L if x['t']<M22)>=40]
  ung.sort(reverse=True); print("\nTop 5 ETH theo R/lenh tap hoc 2018-21:",[(round(a,2),k) for a,k in ung[:5]])
  ung2=[(sum(x['R'] for x in L if x['t']<M22),k) for k,L in KQ.items() if k[0]=='ETH']
  ung2.sort(reverse=True); print("Top 5 ETH theo tong R tap hoc 2018-21:",[(round(a,1),k) for a,k in ung2[:5]])
  # PHAN B
  from moc import xay,nguong,danh_gia,dong,TIEU_DE
  L0,KH,DL=xay(dd_,'ETH',tra_ve_khung=True); q=nguong(L0)
  moc=[x for x in L0 if x['diem']>=q]
  print("\n===== PHAN B: ghep vao MOC (top 30% diem, 3%), von 500/nam + lai kep tu 2022\n"+TIEU_DE)
  print(dong('MOC',danh_gia(moc)))
  chon=[k for _,k in ung[:2]]+[k for _,k in ung2[:2]]
  for k in ('ETH',2,0,'ngay','G40'),('ETH',2,0,'ngay','NT'),('ETH',4,0,'ngay','G40'):
    if k not in chon: chon.append(k)
  for k in chon:
    moi=[x for x in KQ[k] if x['t']>=M22]
    for x in moi: x.update(dac_diem(DL['1h'],x['i'],1)); x['diem']=__import__('moc').cham(x,__import__('moc').mo_hinh(dd_))
    tk=f"K{k[1]} X{k[2]} {k[3]} {k[4]}"
    for ten,G in ((f'THEM {tk} (top30)',moc+[x for x in moi if x['diem']>=q]),(f'THEM {tk} (khong loc diem)',moc+moi),
                  (f'THAY MUA H1 cu bang {tk} (top30)',[x for x in moc if not (x['phan']=='H1' and x['h']>0)]+[x for x in moi if x['diem']>=q])):
      print(dong(ten,danh_gia(G)),flush=True)
