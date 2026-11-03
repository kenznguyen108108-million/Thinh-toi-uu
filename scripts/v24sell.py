import sys,datetime,bisect; sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1])
def emaS(x,p):  # EMA kieu Pine: seed bang SMA
  o=[None]*len(x)
  if len(x)<p: return o
  o[p-1]=sum(x[:p])/p; a=2/(p+1)
  for i in range(p,len(x)): o[i]=a*x[i]+(1-a)*o[i-1]
  return o
def rsiW(c,p=14):
  o=[None]*len(c); g=l=0
  for i in range(1,p+1):
    d=c[i]-c[i-1]; g+=max(d,0); l+=max(-d,0)
  g/=p;l/=p; o[p]=100 if l==0 else 100-100/(1+g/l)
  for i in range(p+1,len(c)):
    d=c[i]-c[i-1]; g=(g*(p-1)+max(d,0))/p; l=(l*(p-1)+max(-d,0))/p; o[i]=100 if l==0 else 100-100/(1+g/l)
  return o
SEC={'M15':900,'H1':3600,'H4':14400,'D1':86400}
TF={}
for k,s in SEC.items():
  B=agg(T,O,H,L,C,s); c=[b[4] for b in B]
  TF[k]=dict(B=B,t=[b[0]+s for b in B],c=c,e10=emaS(c,10),e20=emaS(c,20),rsi=rsiW(c))
# tuan bat dau chu nhat (MT5)
W={}
for i in range(len(T)):
  wk=(T[i]//1000-3*86400)//604800; W.setdefault(wk,[T[i]//1000,0]); W[wk][1]=C[i]
wks=sorted(W); wt=[(w*604800+3*86400)+604800 for w in wks]; wc=[W[w][1] for w in wks]
def xhTuan(t):
  i=bisect.bisect_right(wt,t)-1
  if i<49: return 0
  sma=sum(wc[i-49:i+1])/50
  return 1 if wc[i]>sma else -1 if wc[i]<sma else 0
ORD=['M15','H1','H4','D1']
def lonGiam(k,t):
  out=[]
  for kk in ORD[ORD.index(k)+1:]:
    d=TF[kk]; i=bisect.bisect_right(d['t'],t)-1
    out.append((kk,d['e10'][i]<d['e20'][i]))
  return out
def kiemtra(k,j):
  d=TF[k]; e10,e20,c,r=d['e10'],d['e20'],d['c'],d['rsi']; t=d['t'][j]
  cr=lambda i: (e10[i]-e20[i])*(e10[i-1]-e20[i-1])<=0
  lanCat=sum(1 for i in range(j-20,j) if cr(i))
  lastUp=lastDn=dnTU=-1
  for i in range(max(21,j-400),j):
    if e10[i]>e20[i] and e10[i-1]<=e20[i-1]: dnTU=lastDn; lastUp=i
    if e10[i]<e20[i] and e10[i-1]>=e20[i-1]: lastDn=i
  songC= lastUp>=0 and dnTU>=0 and j-lastUp<60 and j-dnTU<60
  lg=lonGiam(k,t)
  dk={'gia<EMA':c[j]<e10[j] and c[j]<e20[j],'khongNhieu':lanCat<=2,'RSI<=45':r[j]<=45,
      'tuan<SMA50':xhTuan(t)==-1,'khung tren deu giam':all(x[1] for x in lg),'songC':songC}
  return dk,lg,r[j],lanCat
A=datetime.datetime(2026,9,20).timestamp(); Z=datetime.datetime(2026,10,26).timestamp()
for k in ('M15','H1','H4'):
  d=TF[k]; e10,e20=d['e10'],d['e20']
  for j in range(30,len(d['c'])):
    if not (A<=d['t'][j]<Z): continue
    if e10[j]<e20[j] and e10[j-1]>=e20[j-1]:
      dk,lg,r,lc=kiemtra(k,j)
      bad=[n for n,v in dk.items() if not v]
      if k=='M15' and len(bad)>3: continue
      print(f"{k:3s} {datetime.datetime.utcfromtimestamp(d['t'][j]).strftime('%d/%m %H:%M')} gia {d['c'][j]:7.0f} RSI {r:4.1f} catNhieu {lc}  khung tren: {' '.join(kk+('↓' if g else '↑') for kk,g in lg)}  => {'OK BAN' if not bad else 'chan: '+', '.join(bad)}")
print('tuan<SMA50 hien tai:',xhTuan(Z))
