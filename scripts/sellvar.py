import sys,datetime,bisect,json; sys.path.insert(0,sys.argv[2])
exec(open(sys.argv[2]+'/v24sell.py').read().split("A=datetime.datetime(2026,9,20)")[0])
# tuan: dung them D1 Binance truoc 2025
for r in json.load(open(sys.argv[3])):
  t=r[0]//1000
  if t>=T[0]//1000: break
  wk=(t-3*86400)//604800; W.setdefault(wk,[t,0]); W[wk][1]=float(r[4])
wks=sorted(W); wt=[(w*604800+3*86400)+604800 for w in wks]; wc=[W[w][1] for w in wks]
COST=16.0; CUT=datetime.datetime(2026,7,25).timestamp()
def swingH(h,c,w):
  return all(h[c]>h[q] for q in range(c-w,c+w+1) if q!=c)
def sim(k,bo):
  d=TF[k]; B=d['B']; e10,e20=d['e10'],d['e20']; h=[b[2] for b in B]; c=d['c']
  res=[];pos=None
  for j in range(30,len(c)):
    if pos:
      for m in range(B[j][5]-int(SEC[k]/300)+1,B[j][5]+1):
        if H[m]>=pos['sl']:
          res.append((((pos['e']-pos['sl'])-COST)/pos['r'],pos['t'])); pos=None; break
        if not pos['bv'] and L[m]<=pos['e']-3*pos['r']: pos['bv']=True; pos['sl']=min(pos['sl'],pos['e'])
      if pos and pos['bv']:  # keo theo dinh swing 10 nen da xac nhan
        for cc in range(j-10,j-60,-1):
          if cc>10 and swingH(h,cc,10):
            if h[cc]<pos['sl']: pos['sl']=h[cc]
            break
      if pos: continue
    if d['t'][j]<1739577600 or e10[j-1] is None: continue
    if not (e10[j]<e20[j] and e10[j-1]>=e20[j-1]): continue
    dk,lg,r,lc=kiemtra(k,j)
    if not all(v for n,v in dk.items() if n not in bo): continue
    sl=None
    for cc in range(j-2,max(2,j-500),-1):
      if swingH(h,cc,2) and h[cc]>c[j]: sl=h[cc];break
    if sl is None: continue
    rr=sl-c[j]
    if rr<=COST*2: continue
    pos={'e':c[j],'sl':sl,'r':rr,'t':d['t'][j],'bv':False}
  return res
VAR={'v2.4 goc':set(),
     'bo dk tuan':{'tuan<SMA50'},
     'bo tuan + chi can H4&D1... (bo chuoi)':{'tuan<SMA50','khung tren deu giam'},
     'bo tuan + bo song C':{'tuan<SMA50','songC'},
     'bo tuan + bo song C + bo chuoi':{'tuan<SMA50','songC','khung tren deu giam'}}
for name,bo in VAR.items():
  allr=[]
  for k in ('M15','H1','H4'):
    allr+=sim(k,bo)
  a=[r for r,t in allr if t<CUT]; b=[r for r,t in allr if t>=CUT]
  rep(name+' |HL',a); rep(name+' |KT',b)
  okt=[(datetime.datetime.utcfromtimestamp(t).strftime('%d/%m %H:%M'),round(r,1)) for r,t in sorted(allr,key=lambda x:x[1]) if t>=datetime.datetime(2026,10,1).timestamp()]
  print('   lenh thang 10:',okt)
