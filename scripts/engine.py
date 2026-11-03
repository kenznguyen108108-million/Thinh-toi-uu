# Vong 21 (03/11/2026): ENGINE "hanh trinh RSI" (luat anh Thinh, so lieu vong 20) + NEN TANG bot EMA.
# Chi bao: RSI14, DTB nhanh EMA9(RSI), DTB cham WMA45(RSI) (khop TradingView cua anh).
# Bo khung: NHO / GIUA / LON lien ke: (M15,H1,H4) (H1,H4,D1) (H4,D1,W1).
# Bien the vao lenh (MUA; BAN doi xung):
#   V0 giua cat len, khong loc                          (moc so sanh)
#   V1 giua cat len + lon CHO PHEP (dong thuan hoac da thu hep: EMA9 lon quay dau len)
#   V2 giua cat len + lon dong thuan                    (chat hon)
#   V3 = V1 + bo lan cat len DAU TIEN sau khi RSI giua <= 20 (cam: cho retest / 2 day)
#   V4 vao o khung NHO: giua dang tang & mo rong, lon cho phep, nho het song hoi (nho cat len) -> quan ly lenh tren khung nho
# Nen tang giu nguyen (rsi.py): SL swing 2 nen, keo SL swing 10, khoa loi 2R/50%, chan SL < 0,2% gia, phi 0,06%,
# thua 3 nghi 8h, rui ro 2% (H4/D1 x1,5), moi khung moi chieu 1 lenh.
# Chay: python3 -I engine.py <thu muc data>
import sys,os,bisect,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from hanh_trinh import load,chuan_bi,tuan
from rsi import piv,mo,ao_giap,von,sl_dau,W_SL,W_TR
SEC={'15m':900,'1h':3600,'4h':14400,'1d':86400,'1w':604800}

def nap(d):
  d=chuan_bi(d); d['dinh2'],d['day2']=piv(d['h'],d['l'],W_SL); d['dinh10'],d['day10']=piv(d['h'],d['l'],W_TR); return d

def idx(D,sec,T):   # nen da dong cuoi cung cua khung D tai thoi diem T
  return bisect.bisect_right(D['t'],T-sec)-1

def cho_phep(L,k,hg,chat=False):
  F,S=L['f'],L['s']
  if k<1: return False
  if hg*(F[k]-S[k])>0: return True
  return (not chat) and hg*(F[k]-F[k-1])>0

def chay(N,G,L,sn,sg,sl,bt,chieu=(1,-1)):
  res=[]
  if bt=='V4':
    d=N; ban={1:-1,-1:-1}; f,s=d['f'],d['s']
    for i in range(60,d['n']-1):
      for hg in chieu:
        if i<=ban[hg] or not (hg*(f[i-1]-s[i-1])<=0 and hg*(f[i]-s[i])>0): continue
        T=d['t'][i]+sn; kg=idx(G,sg,T); kl=idx(L,sl,T)
        if kg<1 or kl<1: continue
        if not (hg*(G['f'][kg]-G['s'][kg])>0 and hg*((G['f'][kg]-G['s'][kg])-(G['f'][kg-1]-G['s'][kg-1]))>0): continue
        if not cho_phep(L,kl,hg): continue
        x=mo(d,i,hg)
        if x: res.append(dict(t=T,tra=d['t'][x[1]]+sn,R=x[0],h=hg,sec=sn,gia=d['c'][i],kc=abs(d['c'][i]-sl_dau(d,i,hg,d['c'][i])))); ban[hg]=x[1]
    return res
  d=G; ban={1:-1,-1:-1}; f,s,r=d['f'],d['s'],d['r']
  pha=d['P']; bd=[p[1] for p in pha]
  for i in range(60,d['n']-1):
    for hg in chieu:
      if i<=ban[hg] or not (hg*(f[i-1]-s[i-1])<=0 and hg*(f[i]-s[i])>0): continue
      T=d['t'][i]+sg; kl=idx(L,sl,T)
      if bt in ('V1','V3') and not cho_phep(L,kl,hg): continue
      if bt=='V2' and not cho_phep(L,kl,hg,True): continue
      if bt=='V3':
        # pha nguoc chieu ngay truoc lan cat nay: RSI co cham vung cam/xanh (<=20 / >=80) khong?
        p=bisect.bisect_left(bd,i)-1
        if p>=0:
          _,b0,e0=pha[p]
          cuc=min(r[b0:i+1]) if hg>0 else max(r[b0:i+1])
          if (hg>0 and cuc<=20) or (hg<0 and cuc>=80): continue
      x=mo(d,i,hg)
      if x: res.append(dict(t=T,tra=d['t'][x[1]]+sg,R=x[0],h=hg,sec=sg,gia=d['c'][i],kc=abs(d['c'][i]-sl_dau(d,i,hg,d['c'][i])))); ban[hg]=x[1]
  return res

def tk(L):
  v=[x['R'] for x in L]
  if not v: return "   0L"
  eq=pk=dd=0; m=ls=0
  for x in v: eq+=x; pk=max(pk,eq); dd=max(dd,pk-eq); m=m+1 if x<0 else 0; ls=max(ls,m)
  return f"{len(v):4d}L {100*sum(1 for x in v if x>0)/len(v):3.0f}% {sum(v):+6.1f}R sut{dd:5.1f}R tLT{ls:2d}"

if __name__=='__main__':
  dd=sys.argv[1]
  for sym in ('BTC','ETH'):
    D={tf:nap(load(f"{dd}/{sym}_{tf}.csv")) for tf in ('15m','1h','4h','1d')}
    D['1w']=tuan(D['1d']); D['1w']['dinh2'],D['1w']['day2']=piv(D['1w']['h'],D['1w']['l'],W_SL); D['1w']['dinh10'],D['1w']['day10']=piv(D['1w']['h'],D['1w']['l'],W_TR)
    cuoi=D['1h']['t'][-1]; m12=cuoi-365*86400; m6=cuoi-183*86400; m24=dt.datetime(2024,1,1).timestamp()
    print(f"\n===== {sym}  (truoc 2024 | 2024->nay | 12T gan | 6T gan) ; von 12T: lai kep 2% (H4/D1 3%), ao giap thua 3 nghi 8h")
    for nho,giua,lon in (('15m','1h','4h'),('1h','4h','1d'),('4h','1d','1w')):
      for bt in ('V0','V1','V2','V3','V4'):
        for chieu,tc in (((1,-1),'2c'),((1,),'MUA')):
          L=chay(D[nho],D[giua],D[lon],SEC[nho],SEC[giua],SEC[lon],bt,chieu)
          A=[x for x in L if x['t']<m24]; B=[x for x in L if x['t']>=m24]; C=[x for x in L if x['t']>=m12]; E=[x for x in L if x['t']>=m6]
          lai,sut=von(ao_giap(C))
          print(f"{sym} {giua.upper():3s}(nho {nho},lon {lon}) {bt} {tc:3s} | {tk(A)} | {tk(B)} | {tk(C)} | {tk(E)} | von12T {lai:+6.0f}% sut {sut:4.0f}%",flush=True)
