# Vong 27 (03/11/2026): MO-DUN BAN LUC SAP (y anh: "thi truong cang sap cang phai kiem").
# Khac ban doi xung cu: CHI ban khi D1 dang giam that, vao o song hoi/pha day, GONG DAI theo dinh cao nhat N nen (khong khoa loi som).
# Pha (D1, nen da dong):
#   P1 phe D1 giam: EMA10<EMA20 & gia dong duoi ca 2 (moc phe ban cua bot A)
#   P2 P1 + gia duoi EMA200 D1 (thi truong giam dai)
#   P3 gia duoi EMA200 D1 + EMA9(RSI D1) < WMA45(RSI D1) (hanh trinh RSI D1 dang giam)
# Diem vao (khung H1 / H4):
#   T1 EMA9(RSI) cat xuong WMA45(RSI)    T2 RSI cat xuong 45    T3 gia dong pha day 20 nen
# Thoat: G20/G40 = SL keo theo dinh cao nhat 20/40 nen (khong khoa loi); NT = nen tang (keo swing 10 + khoa 2R/50%).
# SL ban dau: dinh swing 2 nen (nen tang). Chon cau hinh tren 2018-2021, KIEM TRA 2022-2026.
# Chay: python3 -I ban_sap.py <thu muc data>
import sys,os,datetime as dt,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,SEC
from lib import ema
from rsi import sl_dau,mo,PHI,SL_MIN

def pha_d1(D):
  c=D['c']; e10=ema(c,10); e20=ema(c,20); e200=ema(c,200); P={}
  for k in range(len(c)):
    p1=e10[k]<e20[k] and c[k]<min(e10[k],e20[k]); u=c[k]<e200[k]
    P[D['t'][k]]=(p1,p1 and u,u and D['f'][k]<D['s'][k])
  return P

def mo_g(d,sig,N):
  o,h,c=d['o'],d['h'],d['c']; vao=c[sig]; sl=sl_dau(d,sig,-1,vao)
  if sl is None: return None
  R=sl-vao
  if R<SL_MIN*vao: return None
  for b in range(sig+1,d['n']):
    if h[b]>=sl: return ((vao-max(sl,o[b]))-PHI*vao)/R,b
    if b-N>sig: sl=min(sl,max(h[b-N+1:b+1]))
  return ((vao-c[-1])-PHI*vao)/R,d['n']-1

def chay(d,sec,P,dt1,pha,tg,thoat):
  f,s,r,c,l=d['f'],d['s'],d['r'],d['c'],d['l']; res=[]; ban=-1; pi=('P1','P2','P3').index(pha)
  for i in range(60,d['n']-1):
    if i<=ban: continue
    k=bisect.bisect_right(dt1,d['t'][i]+sec-86400)-1      # D1 da dong
    if k<0 or not P[dt1[k]][pi]: continue
    if tg=='T1': ok=f[i-1]>=s[i-1] and f[i]<s[i]
    elif tg=='T2': ok=r[i-1]>45>=r[i]
    else: ok=c[i]<min(l[i-20:i])
    if not ok: continue
    x=mo(d,i,-1) if thoat=='NT' else mo_g(d,i,int(thoat[1:]))
    if x: res.append(dict(t=d['t'][i]+sec,tra=d['t'][x[1]]+sec,R=x[0],h=-1,sec=sec,i=i,kc=abs(c[i]-sl_dau(d,i,-1,c[i])))); ban=x[1]
  return res

def nam(t): return dt.datetime.utcfromtimestamp(t).year

if __name__=='__main__':
  dd_=sys.argv[1]; KQ=[]
  for sym in ('ETH','BTC'):
    D={tf:nap(load(f"{dd_}/{sym}_{tf}.csv")) for tf in ('1h','4h','1d')}
    P=pha_d1(D['1d']); dt1=D['1d']['t']
    gia={}
    for k in range(D['1d']['n']): y=nam(dt1[k]); gia.setdefault(y,[D['1d']['o'][k],0]); gia[y][1]=D['1d']['c'][k]
    print(f"\n===== {sym} gia nam: "+" ".join(f"{y}:{(b/a-1)*100:+.0f}%" for y,(a,b) in sorted(gia.items())))
    for tf in ('1h','4h'):
      for pha in ('P1','P2','P3'):
        for tg in ('T1','T2','T3'):
          for th in ('NT','G20','G40'):
            L=chay(D[tf],SEC[tf],P,dt1,pha,tg,th)
            hoc=[x['R'] for x in L if x['t']<dt.datetime(2022,1,1).timestamp()]; kt=[x['R'] for x in L if x['t']>=dt.datetime(2022,1,1).timestamp()]
            yr={y:sum(x['R'] for x in L if nam(x['t'])==y) for y in range(2018,2027)}
            KQ.append((sym,tf,pha,tg,th,len(hoc),sum(hoc),len(kt),sum(kt),yr))
            print(f"{sym} {tf.upper():2s} {pha} {tg} {th:3s} | hoc 18-21 {len(hoc):4d}L {sum(hoc):+6.1f}R | kiem 22-26 {len(kt):4d}L {sum(kt):+6.1f}R | "+" ".join(f"{str(y)[2:]}:{v:+5.1f}" for y,v in yr.items()),flush=True)
