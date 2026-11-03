# Vong 6 (29/10/2026): moc phe BAN. Mo phong gan dung luat MUA/BAN cua bot EMA tren M5/M15/H1/H4 (tinh theo R).
# Moc phe giam: 0 tuan<SMA50 | 1 D1 EMA10<EMA20 & gia duoi 2 duong | 2 D1 duoi EMA99 | 3 tuan EMA10<EMA20 | 4 RSI 3D < 50
# Chay: python3 -I ban_moc.py <m5.csv> <thu muc scripts> <d1.json Binance truoc 2025>
import sys,datetime,bisect,json; sys.path.insert(0,sys.argv[2])
from lib import *
T,O,H,L,C=load(sys.argv[1]); N=len(T)
COST=16.0
def emaS(x,p):
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
# D1 Binance truoc 2025 de co du lich su cho SMA50 tuan / EMA99 D1
pre=[(r[0]//1000,float(r[1]),float(r[2]),float(r[3]),float(r[4])) for r in json.load(open(sys.argv[3])) if r[0]<T[0]]
SEC={'M5':300,'M15':900,'H1':3600,'H4':14400,'D1':86400,'3D':259200,'W1':604800}
TF={}
for k,s in SEC.items():
  B=agg(T,O,H,L,C,s)
  if k in ('D1','3D','W1'):
    # ghep lich su truoc 2025 (gop D1 thanh 3D / tuan)
    ex={}
    for t,o,h,l,c in pre:
      b=(t-(3*86400 if k=='W1' else 0))//s*s+(3*86400 if k=='W1' else 0)
      if b not in ex: ex[b]=[b,o,h,l,c,-1]
      else: ex[b][2]=max(ex[b][2],h); ex[b][3]=min(ex[b][3],l); ex[b][4]=c
    if k=='W1':
      B=[]; cur=None
      for i in range(N):
        t=T[i]//1000; b=(t-3*86400)//s*s+3*86400
        if cur is None or cur[0]!=b:
          if cur: B.append(cur)
          cur=[b,O[i],H[i],L[i],C[i],i]
        else: cur[2]=max(cur[2],H[i]); cur[3]=min(cur[3],L[i]); cur[4]=C[i]; cur[5]=i
      B.append(cur)
    B=[v for kk,v in sorted(ex.items()) if kk<B[0][0]]+B
  c=[b[4] for b in B]
  TF[k]=dict(B=B,t=[b[0]+s for b in B],c=c,h=[b[2] for b in B],l=[b[3] for b in B],
             e10=emaS(c,10),e20=emaS(c,20),e99=emaS(c,99),rsi=rsiW(c))
def idx(k,t):  # nen DA DONG gan nhat cua khung k tai thoi diem t
  return bisect.bisect_right(TF[k]['t'],t)-1

def phe_giam(moc,t):
  if moc==0:
    d=TF['W1']; i=idx('W1',t)
    if i<49: return False
    return d['c'][i]<sum(d['c'][i-49:i+1])/50
  if moc==1:
    d=TF['D1']; i=idx('D1',t); e1,e2,c=d['e10'][i],d['e20'][i],d['c'][i]
    return e1 is not None and e2 is not None and e1<e2 and c<e1 and c<e2
  if moc==2:
    d=TF['D1']; i=idx('D1',t); return d['e99'][i] is not None and d['c'][i]<d['e99'][i]
  if moc==3:
    d=TF['W1']; i=idx('W1',t); return d['e20'][i] is not None and d['e10'][i]<d['e20'][i]
  if moc==4:
    d=TF['3D']; i=idx('3D',t); return d['rsi'][i] is not None and d['rsi'][i]<50
ORD=['M5','M15','H1','H4','D1']
def chuoi(k,t,huong):
  for kk in ORD[ORD.index(k)+1:]:
    d=TF[kk]; i=idx(kk,t)
    if d['e10'][i] is None or d['e20'][i] is None: return False
    if huong>0 and not d['e10'][i]>d['e20'][i]: return False
    if huong<0 and not d['e10'][i]<d['e20'][i]: return False
  return True
def songC(d,j):
  e10,e20=d['e10'],d['e20']; lastUp=lastDn=dnTU=-1
  for i in range(max(21,j-400),j):
    if e10[i]>e20[i] and e10[i-1]<=e20[i-1]: dnTU=lastDn; lastUp=i
    if e10[i]<e20[i] and e10[i-1]>=e20[i-1]: lastDn=i
  return lastUp>=0 and dnTU>=0 and j-lastUp<60 and j-dnTU<60

def swing(arr,c,w,hi):
  return all((arr[c]>arr[q]) if hi else (arr[c]<arr[q]) for q in range(c-w,c+w+1) if q!=c)

def tin_hieu(k):
  # danh sach (t, j, huong) tin hieu MUA/BAN goc cua khung k (chua loc phe)
  d=TF[k]; e10,e20,c,r=d['e10'],d['e20'],d['c'],d['rsi']; out=[]
  for j in range(45,len(c)):
    if e10[j-22] is None or e20[j-22] is None or r[j] is None: continue
    up=e10[j]>e20[j] and e10[j-1]<=e20[j-1]; dn=e10[j]<e20[j] and e10[j-1]>=e20[j-1]
    if not (up or dn): continue
    if sum(1 for i in range(j-20,j) if (e10[i]-e20[i])*(e10[i-1]-e20[i-1])<=0)>2: continue
    if up and c[j]>e10[j] and c[j]>e20[j] and r[j]>=55: out.append((d['t'][j],j,1))
    if dn and c[j]<e10[j] and c[j]<e20[j] and r[j]<=45: out.append((d['t'][j],j,-1))
  return out
SIG={k:tin_hieu(k) for k in ('M5','M15','H1','H4')}

def chay_lenh(k,j,huong,tpR):
  d=TF[k]; B=d['B']; h,l,c=d['h'],d['l'],d['c']
  e=c[j]; sl=None
  for cc in range(j-2,max(2,j-500),-1):
    if huong>0 and swing(l,cc,2,False) and l[cc]<e: sl=l[cc]; break
    if huong<0 and swing(h,cc,2,True) and h[cc]>e: sl=h[cc]; break
  if sl is None: return None
  R=abs(e-sl)
  if R<=COST*2: return None
  bv=False; tp=e+huong*tpR*R if tpR else None
  for jj in range(j+1,len(c)):
    m0=B[jj-1][5]+1; m1=B[jj][5]
    for m in range(m0,m1+1):
      if (huong>0 and L[m]<=sl) or (huong<0 and H[m]>=sl): return (huong*(sl-e)-COST)/R, T[m]//1000
      if tp and ((huong>0 and H[m]>=tp) or (huong<0 and L[m]<=tp)): return (tpR*R-COST)/R, T[m]//1000
      if not bv and ((huong>0 and H[m]>=e+3*R) or (huong<0 and L[m]<=e-3*R)):
        bv=True; sl=max(sl,e) if huong>0 else min(sl,e)
    if bv:  # keo theo swing 10 nen da xac nhan
      for cc in range(jj-10,jj-60,-1):
        if cc>10 and swing(h if huong<0 else l,cc,10,huong<0):
          v=h[cc] if huong<0 else l[cc]
          if (huong>0 and v>sl) or (huong<0 and v<sl): sl=v
          break
  return None

def danh(moc,banM5,chanMua,tu,den):
  # moi khung moi chieu 1 lenh tai 1 thoi diem; tra ve list (huong, R, t_vao)
  res=[]
  for k in ('M5','M15','H1','H4'):
    ban_tf = (k!='M5') or banM5
    ban_tu=mua_tu=0
    for t,j,hg in SIG[k]:
      if not (tu<=t<den): continue
      phe=phe_giam(moc,t)
      if hg>0:
        if t<mua_tu: continue
        if chanMua and phe: continue
        if k=='M5' and not chuoi(k,t,1): continue
        if k!='M5':
          dl=TF[ORD[ORD.index(k)+1]]; i=idx(ORD[ORD.index(k)+1],t)
          if not (dl['e10'][i]>dl['e20'][i] or dl['e10'][i]>dl['e10'][i-1]): continue
        x=chay_lenh(k,j,1,0.5 if k=='M5' else 0)
        if x: res.append((1,x[0],t,k)); mua_tu=x[1]
      else:
        if not ban_tf or t<ban_tu or not phe: continue
        if not chuoi(k,t,-1): continue
        if moc==0 and not songC(TF[k],j): continue
        x=chay_lenh(k,j,-1,0.5 if k=='M5' else 0)
        if x: res.append((-1,x[0],t,k)); ban_tu=x[1]
  return res

def tom(ten,res):
  for hg,nm in ((1,'MUA'),(-1,'BAN')):
    R=[r for h,r,t,k in res if h==hg]
    if R: print(f"   {ten:34s} {nm}: {len(R):4d} lenh  thang {100*sum(1 for x in R if x>0)/len(R):3.0f}%  TB {sum(R)/len(R):+.2f}R  tong {sum(R):+7.1f}R")
    else: print(f"   {ten:34s} {nm}:    0 lenh")
  R=[r for h,r,t,k in sorted(res,key=lambda x:x[2])]; eq=pk=dd=0
  for x in R: eq+=x; pk=max(pk,eq); dd=max(dd,pk-eq)
  print(f"   {ten:34s} TONG: {len(R)} lenh, {sum(R):+.1f}R, sut {dd:.1f}R")

ts=lambda s: datetime.datetime.strptime(s,'%Y-%m-%d').timestamp()
GD=[('24/01-24/07/2026 (BTC giam 27%)',ts('2026-01-24'),ts('2026-07-24')),
    ('25/04-25/10/2026 (6 thang gan nhat)',ts('2026-04-25'),ts('2026-10-26')),
    ('06/2025-10/2026 (tham khao)',ts('2025-06-01'),ts('2026-10-26'))]
CH=[('0 goc tuan<SMA50+songC',0,False,False),('1 D1 EMA10<20, ban M5',1,True,False),('2 D1 duoi EMA99, ban M5',2,True,False),
    ('3 tuan EMA10<20, ban M5',3,True,False),('4 RSI 3D<50, ban M5',4,True,False),
    ('1 + chan MUA khi giam',1,True,True),('2 + chan MUA khi giam',2,True,True),('3 + chan MUA khi giam',3,True,True),('4 + chan MUA khi giam',4,True,True)]
print("Mo phong gan dung (Binance M5, phi $16, M5 chot 0.5R, khung khac 3R hoa von + keo SL swing 10)")
for g,tu,den in GD:
  print("==",g)
  for ten,moc,b5,cm in CH: tom(ten,danh(moc,b5,cm,tu,den))
