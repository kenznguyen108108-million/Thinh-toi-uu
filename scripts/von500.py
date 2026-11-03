# Vong 21b: mo phong tien that von 500 USD cho ung vien engine (lot that, tran 4%, ao giap thua 3 nghi 8h)
# Gia dinh lot: BTC hop dong 1 BTC, lot min 0,01 buoc 0,01; ETH hop dong 1 ETH, lot min 0,1 buoc 0,1 (CAN KIEM LAI tren Exness)
# Chay: python3 -I von500.py <thu muc data>
import sys,os,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import nap,load,tuan,chay,SEC,piv,W_SL,W_TR
from rsi import ao_giap
LOT={'BTC':(0.01,0.01),'ETH':(0.1,0.1)}

def mo_phong(L,sym,von=500.0,rr=2.0,tran=4.0):
  mn,buoc=LOT[sym]; L=ao_giap(L); ev=[]
  for x in L: ev+= [(x['t'],0,x),(x['tra'],1,x)]
  ev.sort(key=lambda e:(e[0],-e[1]))   # dong truoc mo neu cung gio
  b=von; pk=von; dd=0; mo_={}; bo=0; n=0; thang={}
  for t,loai,x in ev:
    if loai==0:
      r=rr*(1.5 if x['sec']>=14400 else 1)/100*b
      lot=int(r/x['kc']/buoc)*buoc
      if lot<mn:
        if mn*x['kc']>tran/100*b: bo+=1; continue
        lot=mn
      mo_[id(x)]=lot
    elif id(x) in mo_:
      lai=x['R']*mo_.pop(id(x))*x['kc']; b+=lai; n+=1
      k=dt.datetime.utcfromtimestamp(t).strftime('%m/%y'); thang[k]=thang.get(k,0)+lai
      pk=max(pk,b); dd=max(dd,1-b/pk)
  tt=min(thang,key=thang.get) if thang else '-'
  return f"{n:3d} lenh (bo {bo:2d} vi lot min >4%) | 500 -> {b:7.0f} USD ({b-von:+6.0f}) | sut tu dinh {dd*100:4.0f}% | thang te nhat {tt} {thang.get(tt,0):+5.0f} USD"

if __name__=='__main__':
  dd_=sys.argv[1]
  CAU=[('BTC','15m','1h','4h','V2',(1,),'H1 V2 chi MUA'),('ETH','15m','1h','4h','V2',(1,),'H1 V2 chi MUA'),
       ('ETH','1h','4h','1d','V4',(1,),'H4 V4 chi MUA'),('BTC','1h','4h','1d','V4',(1,),'H4 V4 chi MUA')]
  cache={}
  for sym,n,g,l,bt,ch,ten in CAU:
    if sym not in cache:
      D={tf:nap(load(f"{dd_}/{sym}_{tf}.csv")) for tf in ('15m','1h','4h','1d')}; cache[sym]=D
    D=cache[sym]; cuoi=D['1h']['t'][-1]
    L=chay(D[n],D[g],D[l],SEC[n],SEC[g],SEC[l],bt,ch)
    for thg in (12,6,3):
      tu=cuoi-int(thg*30.5*86400)
      print(f"{sym} {ten:14s} {thg:2d} thang gan | {mo_phong([x for x in L if x['t']>=tu],sym)}",flush=True)
  # ghep ETH H1 V2 + H4 V4 (cung tai khoan, cung ao giap)
  D=cache['ETH']; cuoi=D['1h']['t'][-1]
  L=chay(D['15m'],D['1h'],D['4h'],900,3600,14400,'V2',(1,))+chay(D['1h'],D['4h'],D['1d'],3600,14400,86400,'V4',(1,))
  for thg in (12,6,3):
    tu=cuoi-int(thg*30.5*86400)
    print(f"ETH ghep H1V2+H4V4  {thg:2d} thang gan | {mo_phong([x for x in L if x['t']>=tu],'ETH')}")
