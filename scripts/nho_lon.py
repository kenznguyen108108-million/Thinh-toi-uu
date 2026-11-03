# Vong 20c (03/11/2026): khung NHO tang trong khi khung LON giam (va nguoc lai) -> ben nao thang?
# Y anh Thinh: khung nho la chat xuc tac cho khung lon lien ke, khung lon chi phoi khung nho.
# Trang thai 1 khung: EMA9(RSI) > WMA45(RSI) = tang, < = giam (chi bao tren TradingView cua anh).
# Su kien: khung nho vua cat LEN (EMA9 cat len WMA45) trong luc khung lon dang giam.
# Theo doi toi da H nen khung lon:
#   "lon quay len"  = khung lon cat len truoc khi khung nho cat xuong lai  (xuc tac thanh cong)
#   "nho quay xuong" = khung nho cat xuong lai truoc                        (khung lon chi phoi)
# Chia theo trang thai khung lon luc do: dang THU HEP (EMA9 lon dang di len) hay van MO RONG giam.
# Chay: python3 -I nho_lon.py <thu muc data> [BTC|ETH]
import sys,os,bisect; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from hanh_trinh import load,chuan_bi,tuan,pct,tb
H=8   # so nen khung lon theo doi

def su_kien(dn,DL,secn,secl,huong):
  f,s,c=dn['f'],dn['s'],dn['c']; F,S=DL['f'],DL['s']
  tl=DL['t']; out=[]
  for i in range(60,dn['n']-1):
    if not (huong*(f[i-1]-s[i-1])<=0 and huong*(f[i]-s[i])>0): continue
    T=dn['t'][i]+secn
    k=bisect.bisect_right(tl,T-secl)-1          # nen lon da dong cuoi cung
    if k<50 or k+H>=DL['n']: continue
    if huong*(F[k]-S[k])>=0: lon='dong thuan'
    else: lon='lon thu hep' if huong*(F[k]-F[k-1])>0 else 'lon mo rong'
    # theo doi
    het=T+H*secl; kq='chua ro'; j=i+1; kk=k+1
    while j<dn['n'] and dn['t'][j]+secn<=het:
      Tj=dn['t'][j]+secn
      while kk<DL['n'] and tl[kk]+secl<=Tj:
        if lon!='dong thuan' and huong*(F[kk]-S[kk])>0: kq='lon quay theo'; break
        kk+=1
      if kq!='chua ro': break
      if huong*(f[j]-s[j])<0: kq='nho quay lai'; break
      j+=1
    # gia sau H nen lon, tinh theo huong khung nho, don vi ATR khung lon
    j2=min(dn['n']-1,i+H*secl//secn); a=DL['atr'][k]
    seg_h=max(dn['h'][i+1:j2+1]); seg_l=min(dn['l'][i+1:j2+1])
    thuan=((seg_h-c[i]) if huong>0 else (c[i]-seg_l))/a; nguoc=((c[i]-seg_l) if huong>0 else (seg_h-c[i]))/a
    out.append((lon,kq,thuan,nguoc,(c[j2]-c[i])/c[i]*100*huong))
  return out

if __name__=='__main__':
  dd=sys.argv[1]; syms=sys.argv[2:] or ['BTC','ETH']
  SEC={'15m':900,'1h':3600,'4h':14400,'1d':86400,'1w':604800}
  for sym in syms:
    D={}
    for tf in ('15m','1h','4h','1d'):
      p=f"{dd}/{sym}_{tf}.csv"
      if tf=='15m' and not os.path.exists(p): continue
      d=load(p)
      if tf!='15m': # dung cung giai doan voi M15 (tu 2022) cho cong bang? -> giu het, ghi ro
        pass
      D[tf]=chuan_bi(d)
    D['1w']=tuan(D['1d'])
    for nho,lon in (('15m','1h'),('1h','4h'),('4h','1d'),('1d','1w')):
      if nho not in D: continue
      print(f"\n===== {sym}: NHO {nho.upper()} vs LON {lon.upper()} (theo doi {H} nen {lon.upper()}; gia tinh theo huong khung nho, don vi ATR khung lon)")
      for huong,ten in ((1,'nho cat LEN'),(-1,'nho cat XUONG')):
        ev=su_kien(D[nho],D[lon],SEC[nho],SEC[lon],huong)
        for lon_tt in ('dong thuan','lon thu hep','lon mo rong'):
          v=[x for x in ev if x[0]==lon_tt]
          if not v: continue
          qt=[x[1]=='lon quay theo' for x in v]; ql=[x[1]=='nho quay lai' for x in v]
          nhan=f"{ten} | {lon_tt:11s}"
          if lon_tt=='dong thuan':
            print(f"  {nhan} {len(v):5d} lan |                                       | di thuan {tb([x[2] for x in v])} nguoc {tb([x[3] for x in v])} ATR | gia sau {tb([x[4] for x in v])}%, dung huong {pct([x[4]>0 for x in v])}")
          else:
            print(f"  {nhan} {len(v):5d} lan | lon quay theo {pct(qt)}, nho quay lai {pct(ql)} | di thuan {tb([x[2] for x in v])} nguoc {tb([x[3] for x in v])} ATR | gia sau {tb([x[4] for x in v])}%, dung huong {pct([x[4]>0 for x in v])}")
