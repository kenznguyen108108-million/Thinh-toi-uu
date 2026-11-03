# Vong 20 (03/11/2026): do "hanh trinh RSI" cua anh Thinh so voi gia (khong phai backtest lenh).
# RSI14, DTB nhanh = EMA9(RSI), DTB cham = WMA45(RSI). Quan tinh tang = RSI>=70, quan tinh giam = RSI<=30.
# Pha giam = tu luc EMA9 cat xuong WMA45 den luc cat len lai (pha tang doi xung).
# Do:
#  D1 dinh: pha giam co truoc do quan tinh tang + phan ky am (gia dinh cao hon, RSI thap hon) vs pha giam thuong
#  D2 cat len trong song giam = chi thu hep? -> sau cat len, gia co retest/pha day cu khong, theo RSI sau nhat
#  D3 do mo rong/do doc luc cat -> song di xa hon khong
# Chay: python3 -I hanh_trinh.py <thu muc data> <thu muc scripts>
import sys,csv,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import ema
from rsi import rsi,wma
N=30   # so nen theo doi sau tin hieu
QT_TANG=80   # vach xanh tren chart cua anh = RSI>=80 (cam = RSI<=20), doi chieu TradingView 03/11

def load(p):
  R=list(csv.reader(open(p)))[:-1]
  return dict(t=[int(r[0])//1000 for r in R],o=[float(r[1]) for r in R],h=[float(r[2]) for r in R],l=[float(r[3]) for r in R],c=[float(r[4]) for r in R])

def chuan_bi(d):
  n=len(d['c']); d['n']=n; d['r']=rsi(d['c']); d['f']=ema(d['r'],9); d['s']=wma(d['r'],45)
  tr=[d['h'][0]-d['l'][0]]+[max(d['h'][i]-d['l'][i],abs(d['h'][i]-d['c'][i-1]),abs(d['l'][i]-d['c'][i-1])) for i in range(1,n)]
  d['atr']=ema(tr,14)
  # cac pha: list (huong, bat dau, ket thuc)
  P=[]; st=None
  for i in range(60,n):
    if d['f'][i-1]>=d['s'][i-1] and d['f'][i]<d['s'][i]:
      if st: P.append((st[0],st[1],i))
      st=(-1,i)
    if d['f'][i-1]<=d['s'][i-1] and d['f'][i]>d['s'][i]:
      if st: P.append((st[0],st[1],i))
      st=(1,i)
  d['P']=P; return d

def pct(a): return f"{100*sum(a)/len(a):3.0f}%" if a else "  - "
def tb(a): return f"{sum(a)/len(a):+5.1f}" if a else "   - "

def do_dinh(d):
  # D1: dau pha giam. Co quan tinh tang (RSI>=70) trong 40 nen truoc va phan ky am?
  r,h,l,c,a=d['r'],d['h'],d['l'],d['c'],d['atr']; nhom={'QT+phan ky':[],'QT khong PK':[],'khong QT':[]}
  for hg,b,e in d['P']:
    if hg!=-1 or b+N>=d['n']: continue
    w=range(max(0,b-40),b+1)
    qt=[i for i in w if r[i]>=QT_TANG]
    if qt:
      ip=max(qt,key=lambda i:r[i])                    # dinh RSI trong quan tinh
      ih=max(range(ip,b+1),key=lambda i:h[i])         # dinh gia sau do
      pk= ih>ip and h[ih]>max(h[ip-2:ip+3]) and r[ih]<r[ip]
      k='QT+phan ky' if pk else 'QT khong PK'
    else: k='khong QT'
    giam=(c[b]-min(l[b+1:b+N+1]))/a[b]; tang=(max(h[b+1:b+N+1])-c[b])/a[b]
    nhom[k].append((giam,tang,(c[b+N]-c[b])/c[b]*100))
  out=[]
  for k,v in nhom.items():
    if v: out.append(f"{k}: {len(v):3d} lan, {N} nen sau giam sau nhat TB {tb([x[0] for x in v])} ATR, len cao nhat {tb([x[1] for x in v])} ATR, gia sau {N} nen {tb([x[2] for x in v])}%, % lan gia thap hon {pct([x[2]<0 for x in v])}")
  return out

def do_day(d):
  # D2: pha giam ket thuc bang cat len. Phan theo RSI sau nhat trong pha giam.
  r,h,l,c,a=d['r'],d['h'],d['l'],d['c'],d['atr']; nhom={}
  for hg,b,e in d['P']:
    if hg!=-1 or e+N>=d['n']: continue
    rmin=min(r[b:e+1]); iL=min(range(b,e+1),key=lambda i:l[i]); L=l[iL]
    k='<20' if rmin<20 else '20-30' if rmin<30 else '30-35' if rmin<35 else '35-45' if rmin<45 else '>=45'
    sau=l[e+1:e+N+1]; mn=min(sau)
    retest=(mn-L)<=0.5*a[e]          # ve lai gan day cu (trong 0,5 ATR) hoac thung
    pha=mn<L
    len_=(max(h[e+1:e+N+1])-c[e])/a[e]
    # 2 day roi tang: retest khong pha, sau do vuot dinh pha giam (dinh cao nhat tu iL den e)
    dinh=max(h[iL:e+1]); haiday=retest and not pha and max(h[e+1:e+N+1])>dinh
    nhom.setdefault(k,[]).append((retest,pha,haiday,len_,(c[e+N]-c[e])/c[e]*100))
  out=[]
  for k in ('<20','20-30','30-35','35-45','>=45'):
    v=nhom.get(k,[])
    if v: out.append(f"RSI sau nhat {k:5s}: {len(v):3d} lan | sau cat len: retest day {pct([x[0] for x in v])}, thung day {pct([x[1] for x in v])}, 2 day roi vuot dinh {pct([x[2] for x in v])} | gia sau {N} nen {tb([x[4] for x in v])}%")
  return out

def do_mo_rong(d):
  # D3: do mo rong 5 nen sau cat (|f-s|) va do doc RSI -> song di bao xa (theo huong pha)
  r,f,s,h,l,c,a=d['r'],d['f'],d['s'],d['h'],d['l'],d['c'],d['atr']; V=[]
  for hg,b,e in d['P']:
    if b+5+N>=d['n']: continue
    # do tu nen b+5 (luc da biet do mo rong) -> khong nhin truoc
    j=b+5; mr=abs(f[j]-s[j]); di=((max(h[j+1:j+N+1])-c[j]) if hg>0 else (c[j]-min(l[j+1:j+N+1])))/a[j]
    nguoc=((c[j]-min(l[j+1:j+N+1])) if hg>0 else (max(h[j+1:j+N+1])-c[j]))/a[j]
    V.append((hg,mr,di,nguoc))
  out=[]
  for hg,ten in ((1,'pha tang'),(-1,'pha giam')):
    v=sorted([x for x in V if x[0]==hg],key=lambda x:x[1]); k=len(v)//3
    if k<3: continue
    for nm,g in (('mo hep',v[:k]),('vua',v[k:2*k]),('mo rong',v[2*k:])):
      out.append(f"{ten} {nm:7s} (|EMA9-WMA45| sau 5 nen {g[0][1]:4.1f}-{g[-1][1]:4.1f}): {len(g):3d} lan, di thuan TB {tb([x[2] for x in g])} ATR, nguoc lai {tb([x[3] for x in g])} ATR")
  return out

if __name__=='__main__' and len(sys.argv)>3 and sys.argv[3]=='dakhung':
  import atexit; atexit.register(lambda:[da_khung(sys.argv[1],x) for x in ('BTC','ETH')])
elif __name__=='__main__':
  dd=sys.argv[1]
  for sym in ('BTC','ETH'):
    for tf in ('1d','4h','1h'):
      d=chuan_bi(load(f"{dd}/{sym}_{tf}.csv"))
      print(f"\n===== {sym} {tf.upper()} ({len(d['P'])} pha, 2018 -> nay; theo doi {N} nen sau tin hieu)")
      for ten,fn in (('DINH',do_dinh),('DAY',do_day),('MO RONG',do_mo_rong)):
        for line in fn(d): print(f"  [{ten}] {line}")

# ---- Da khung (vong 20b): khung giua cat len/xuong; khung nho xuc tac? khung lon cho phep? ----
def trang_thai(d):
  # 1 = EMA9(RSI)>WMA45(RSI) (dang tang), -1 nguoc lai; kem thoi diem dong nen
  return d['t'],[1 if d['f'][i]>d['s'][i] else -1 for i in range(d['n'])]

def tra(tt,st,sec,T):
  # trang thai nen da dong cuoi cung co gio dong <= T
  import bisect
  k=bisect.bisect_right(tt,T-sec)-1
  return st[k] if k>=0 else 0

def tuan(d):
  W={}
  for i in range(d['n']):
    k=(d['t'][i]-345600)//604800   # tuan bat dau thu 2
    if k not in W: W[k]=[d['t'][i],d['o'][i],d['h'][i],d['l'][i],d['c'][i]]
    else: w=W[k]; w[2]=max(w[2],d['h'][i]); w[3]=min(w[3],d['l'][i]); w[4]=d['c'][i]
  v=[W[k] for k in sorted(W)][:-1]
  return chuan_bi(dict(t=[x[0] for x in v],o=[x[1] for x in v],h=[x[2] for x in v],l=[x[3] for x in v],c=[x[4] for x in v]))

def da_khung(dd,sym):
  D={tf:chuan_bi(load(f"{dd}/{sym}_{tf}.csv")) for tf in ('1h','4h','1d')}; D['1w']=tuan(D['1d'])
  SEC={'1h':3600,'4h':14400,'1d':86400,'1w':604800}
  for giua,nho,lon in (('1h',None,'4h'),('4h','1h','1d'),('1d','4h','1w')):
    d=D[giua]; sg=SEC[giua]; h,l,c,a=d['h'],d['l'],d['c'],d['atr']
    TN=trang_thai(D[nho]) if nho else None; TL=trang_thai(D[lon]); nhom={}
    for hg,b,e in d['P']:
      if b+N>=d['n']: continue
      T=d['t'][b]+sg
      xn=tra(TN[0],TN[1],SEC[nho],T)==hg if nho else None
      cp=tra(TL[0],TL[1],SEC[lon],T)==hg
      k=('MUA' if hg>0 else 'BAN')+(' | nho '+('dong' if xn else 'nguoc') if nho else '')+' | lon '+('cho phep' if cp else 'chan')
      thuan=((max(h[b+1:b+N+1])-c[b]) if hg>0 else (c[b]-min(l[b+1:b+N+1])))/a[b]
      nguoc=((c[b]-min(l[b+1:b+N+1])) if hg>0 else (max(h[b+1:b+N+1])-c[b]))/a[b]
      kq=(c[b+N]-c[b])/c[b]*100*hg
      nhom.setdefault(k,[]).append((thuan,nguoc,kq))
    print(f"\n== {sym} khung giua {giua.upper()} (nho {nho or '-'}, lon {lon}); {N} nen sau luc EMA9(RSI) cat WMA45(RSI)")
    for k in sorted(nhom):
      v=nhom[k]
      print(f"  {k:32s} {len(v):4d} lan | di thuan {tb([x[0] for x in v])} ATR, nguoc {tb([x[1] for x in v])} ATR, thuan/nguoc {sum(x[0] for x in v)/max(1e-9,sum(x[1] for x in v)):4.2f} | gia sau {N} nen theo huong {tb([x[2] for x in v])}%, dung huong {pct([x[2]>0 for x in v])}")
