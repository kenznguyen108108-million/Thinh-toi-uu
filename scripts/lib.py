import csv
def load(p):
  T=[];O=[];H=[];L=[];C=[]
  for r in csv.reader(open(p)):
    T.append(int(float(r[0])));O.append(float(r[1]));H.append(float(r[2]));L.append(float(r[3]));C.append(float(r[4]))
  return T,O,H,L,C
def ema(x,p):
  a=2/(p+1); o=[x[0]]
  for v in x[1:]: o.append(o[-1]+a*(v-o[-1]))
  return o
def rep(name,R):
  if not R: print(f"{name:44s} 0 lenh");return
  w=sum(1 for x in R if x>0)/len(R); eq=pk=dd=0; ls=m=0
  for x in R:
    eq+=x; pk=max(pk,eq); dd=max(dd,pk-eq); m=m+1 if x<0 else 0; ls=max(ls,m)
  h=len(R)//2; mean=lambda a:sum(a)/len(a) if a else 0
  print(f"{name:44s} lenh {len(R):5d} thang {w*100:4.1f}%  TB {mean(R):+.3f}R  tong {sum(R):+8.1f}R  sut {dd:6.1f}R  thuaLT {ls:3d}  nua1 {mean(R[:h]):+.3f} nua2 {mean(R[h:]):+.3f}")
def agg(T,O,H,L,C,sec):
  out=[]  # t,o,h,l,c,idx_last_m5
  cur=None
  for i in range(len(T)):
    b=T[i]//1000//sec*sec
    if cur is None or cur[0]!=b:
      if cur: out.append(cur)
      cur=[b,O[i],H[i],L[i],C[i],i]
    else:
      cur[2]=max(cur[2],H[i]);cur[3]=min(cur[3],L[i]);cur[4]=C[i];cur[5]=i
  out.append(cur); return out
def pivots(B,k):
  P=[]  # (index, 'H'/'L', price)  confirmed at index+k
  for i in range(k,len(B)-k):
    if all(B[i][2]>=B[j][2] for j in range(i-k,i+k+1)): P.append((i,'H',B[i][2]))
    if all(B[i][3]<=B[j][3] for j in range(i-k,i+k+1)): P.append((i,'L',B[i][3]))
  return P
