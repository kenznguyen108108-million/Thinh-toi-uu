# Vong 28 (03/11/2026): luat BAN cua anh: BAN H1 chi khi H4 VUA cat xuong + doc manh; BAN H4 chi khi D1 VUA cat xuong + doc manh.
# "Cat xuong" = EMA9(RSI) cat xuong WMA45(RSI) tren khung tren (nen da dong).
#   vua  : lan cat nam trong K nen gan nhat cua khung tren, va khung tren van dang EMA9 < WMA45
#   doc  : EMA9(RSI) khung tren giam >= X diem trong 3 nen gan nhat
# Diem vao o khung duoi: rsi45 = RSI cat xuong 45 (nhu v19) | ema = EMA9(RSI) khung duoi cat xuong | ngay = nen dau tien du dieu kien
# Thoat: NT nen tang (keo swing 10 + khoa 2R/50%) | G40 gong theo dinh cao nhat 40 nen.
# Chon tren 2018-2021, kiem tra 2022-2026.  Chay: python3 -I ban_dakhung.py <thu muc data>
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,SEC
from rsi import mo,sl_dau
from ban_sap import mo_g

def dieu_kien(Dl,K,X):
  # mang bool theo nen khung tren: vua cat xuong (trong K nen) + doc manh
  F,S=Dl['f'],Dl['s']; n=Dl['n']; ok=[False]*n; cat=-999
  for k in range(4,n):
    if F[k-1]>=S[k-1] and F[k]<S[k]: cat=k
    ok[k]= F[k]<S[k] and k-cat<K and (F[k-3]-F[k])>=X
  return ok

def chay(d,sec,Dl,secl,ok,vao,thoat):
  f,s,r=d['f'],d['s'],d['r']; res=[]; ban=-1; dung=-1
  for i in range(60,d['n']-1):
    if i<=ban: continue
    k=bisect.bisect_right(Dl['t'],d['t'][i]+sec-secl)-1
    if k<4 or not ok[k]: continue
    if vao=='rsi45': t=r[i-1]>45>=r[i]
    elif vao=='ema': t=f[i-1]>=s[i-1] and f[i]<s[i]
    else:   # vao ngay nen dau tien sau khi khung tren vua du dieu kien (1 lan moi chuoi)
      t=k!=dung and not ok[k-1]
      if t: dung=k
    if not t: continue
    x=mo(d,i,-1) if thoat=='NT' else mo_g(d,i,40)
    if x: res.append(dict(t=d['t'][i]+sec,tra=d['t'][x[1]]+sec,R=x[0],h=-1,sec=sec,i=i,kc=abs(d['c'][i]-sl_dau(d,i,-1,d['c'][i])))); ban=x[1]
  return res

def nam(t): return dt.datetime.utcfromtimestamp(t).year
M22=dt.datetime(2022,1,1).timestamp()

if __name__=='__main__':
  dd_=sys.argv[1]
  for sym in ('ETH','BTC'):
    D={tf:nap(load(f"{dd_}/{sym}_{tf}.csv")) for tf in ('1h','4h','1d')}
    print(f"\n===== {sym}  (R lenh BAN) hoc 2018-21 | kiem tra 2022-26 | tung nam 18..26")
    for duoi,tren in (('1h','4h'),('4h','1d')):
      for K in (2,4):
        for X in (0,3,6):
          ok=dieu_kien(D[tren],K,X)
          for vao in ('rsi45','ema','ngay'):
            for th in ('NT','G40'):
              L=chay(D[duoi],SEC[duoi],D[tren],SEC[tren],ok,vao,th)
              a=[x['R'] for x in L if x['t']<M22]; b=[x['R'] for x in L if x['t']>=M22]
              yr=" ".join(f"{str(y)[2:]}:{sum(x['R'] for x in L if nam(x['t'])==y):+5.1f}" for y in range(2018,2027))
              print(f"{sym} BAN {duoi.upper()} khi {tren.upper()} vua cat(K{K}) doc>={X} vao={vao:5s} {th:3s} | {len(a):4d}L {sum(a):+6.1f}R | {len(b):4d}L {sum(b):+6.1f}R | {yr}",flush=True)
