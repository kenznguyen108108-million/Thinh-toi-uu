# Vong 22 (03/11/2026): moi khung DOC LAP, khong khung nao chi phoi (y anh Thinh).
# Hanh trinh MUA tren chinh khung do: pha giam (EMA9(RSI) < WMA45(RSI)) -> thu hep -> EMA9 cat len WMA45
#   -> 2 duong mo rong (khoang cach EMA9-WMA45 tang 2 nen lien tiep) va RSI nam tren ca 2 duong -> BUY.  BAN doi xung.
# Bien the:
#   E0 vao ngay luc cat (moc so sanh)
#   E1 cat + cho mo rong 2 nen + RSI tren 2 duong (trong toi da 10 nen sau cat)
#   E2 = E1 + pha truoc da "di het hanh trinh": khoang cach sau nhat cua pha truoc >= 3 diem RSI
#   E3 = E1 + pha truoc sau >= 5 diem
# Nen tang giu nguyen (rsi.mo): SL swing 2, keo SL 10, khoa 2R/50%, SL >= 0,2% gia, phi 0,06%; von500: lot that, thua 3 nghi 8h.
# Chay: python3 -I tung_khung.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,tk,SEC
from rsi import mo,sl_dau
from von500 import mo_phong
M=10

def chay(d,sec,bt,chieu=(1,-1),sau=0):
  f,s,r,c=d['f'],d['s'],d['r'],d['c']; kc=[f[i]-s[i] for i in range(d['n'])]
  res=[]; ban={1:-1,-1:-1}; cho={1:None,-1:None}; dau={1:0.0,-1:0.0}
  for i in range(61,d['n']-1):
    for hg in chieu:
      # theo doi do sau pha nguoc chieu dang chay
      if hg*kc[i]<0: dau[hg]=max(dau[hg],-hg*kc[i])
      cat=hg*kc[i-1]<=0 and hg*kc[i]>0
      if cat:
        cho[hg]=(i,dau[hg]); dau[hg]=0.0
      if cho[hg] is None: continue
      ic,do_sau=cho[hg]
      if i-ic>M or hg*kc[i]<=0: cho[hg]=None; continue
      if bt=='E0': ok=(i==ic)
      else:
        ok=hg*(kc[i]-kc[i-1])>0 and hg*(kc[i-1]-kc[i-2])>0 and hg*(r[i]-f[i])>0 and hg*(r[i]-s[i])>0
        if bt in ('E2','E3') and do_sau<(3 if bt=='E2' else 5): cho[hg]=None; continue
      if not ok: continue
      cho[hg]=None
      if i<=ban[hg]: continue
      x=mo(d,i,hg)
      if x:
        T=d['t'][i]+sec
        res.append(dict(t=T,tra=d['t'][x[1]]+sec,R=x[0],h=hg,sec=sec,gia=c[i],kc=abs(c[i]-sl_dau(d,i,hg,c[i])))); ban[hg]=x[1]
  return res

if __name__=='__main__':
  dd_=sys.argv[1]; tom=[]
  for sym in ('BTC','ETH'):
    D={tf:nap(load(f"{dd_}/{sym}_{tf}.csv")) for tf in ('15m','1h','4h','1d')}
    cuoi=D['1h']['t'][-1]; m24=dt.datetime(2024,1,1).timestamp(); m12=cuoi-365*86400; m6=cuoi-183*86400
    print(f"\n===== {sym}  R: truoc 2024 | 2024->nay | 12T gan ; tien: von 500 USD 12 thang (lot that, ao giap)")
    for tf in ('15m','1h','4h','1d'):
      for bt in ('E0','E1','E2','E3'):
        for ch,tc in (((1,-1),'2c'),((1,),'MUA'),((-1,),'BAN')):
          L=chay(D[tf],SEC[tf],bt,ch)
          A=[x for x in L if x['t']<m24]; B=[x for x in L if x['t']>=m24]; C=[x for x in L if x['t']>=m12]
          v12=mo_phong(C,sym); v6=mo_phong([x for x in L if x['t']>=m6],sym)
          print(f"{sym} {tf.upper():3s} {bt} {tc:3s} | {tk(A)} | {tk(B)} | {tk(C)} | 12T: {v12.split('|')[1].strip()} sut{v12.split('sut tu dinh')[1].split('%')[0]}% | 6T: {v6.split('|')[1].strip()}",flush=True)
