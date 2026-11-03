# Phan tich nhat ky lenh (CSV cua bot v2.6) theo khung, chieu, ly do ra, thang, va trang thai tuan (tang/giam/giang co).
# Chay: python3 -I phantich_nk.py <d1.json tu MCP get_chart_history> <nhatky1.csv> [nhatky2.csv ...]
import sys,csv,re,datetime as dt
from collections import defaultdict
raw=open(sys.argv[1]).read()
D=[(m[0],float(m[1]),float(m[2]),float(m[3]),float(m[4])) for m in re.findall(r'time\\": \\"([0-9-]+)T[^,]*, \\"open\\": ([0-9.]+), \\"high\\": ([0-9.]+), \\"low\\": ([0-9.]+), \\"close\\": ([0-9.]+)',raw)]
# tuan: thay doi > +4% = TANG, < -4% = GIAM, con lai = GIANG CO
W={}
for t,o,h,l,c in D:
  d=dt.date.fromisoformat(t); k=d-dt.timedelta(days=d.weekday())
  if k not in W: W[k]=[o,h,l,c]
  else: W[k][1]=max(W[k][1],h); W[k][2]=min(W[k][2],l); W[k][3]=c
def loai_tuan(k):
  o,h,l,c=W[k]; ch=(c-o)/o*100
  return 'TANG' if ch>4 else ('GIAM' if ch<-4 else 'GIANG CO')
def tuan_cua(s):
  d=dt.datetime.strptime(s,'%Y.%m.%d %H:%M').date(); return d-dt.timedelta(days=d.weekday())

def bang(ten,rows,key):
  g=defaultdict(list)
  for r in rows: g[key(r)].append(r)
  print(f"  {ten}:")
  for k in sorted(g):
    v=g[k]; R=[x['R'] for x in v]; usd=sum(x['usd'] for x in v); w=sum(1 for x in R if x>0.05)
    print(f"    {str(k):24s} {len(v):4d} lenh  thang {100*w/len(v):4.0f}%  tong {sum(R):+7.1f}R  TB {sum(R)/len(v):+.2f}R  {usd:+9.2f} USD")

for p in sys.argv[2:]:
  rows=[]
  for r in csv.DictReader(open(p)):
    if r['Loai']!='THAT' or not r['Ket qua R']: continue
    rows.append({'k':r['Khung'],'chieu':r['Chieu'],'vao':r['TG vao'],'ra':r['TG ra'],'R':float(r['Ket qua R']),
                 'usd':float(r['Lai lo (USD)']),'ly':r['Ly do ra'],'gio':float(r['Gio giu'] or 0)})
  R=[x['R'] for x in rows]
  print(f"=== {p.split('/')[-1]}: {len(rows)} lenh, tong {sum(R):+.1f}R, {sum(x['usd'] for x in rows):+.2f} USD")
  bang('Theo khung',rows,lambda r:r['k'])
  bang('Theo chieu',rows,lambda r:r['chieu'])
  bang('Theo ly do ra',rows,lambda r:r['ly'])
  bang('Theo thang (thoat lenh)',rows,lambda r:r['ra'][:7])
  bang('Theo tuan thi truong (luc vao)',rows,lambda r:loai_tuan(tuan_cua(r['vao'])) if tuan_cua(r['vao']) in W else '?')
  bang('Khung x tuan',rows,lambda r:r['k']+' / '+(loai_tuan(tuan_cua(r['vao'])) if tuan_cua(r['vao']) in W else '?'))
  big=sorted(rows,key=lambda x:-x['R'])[:6]
  print("  Lenh thang lon nhat:", "; ".join(f"{x['k']} {x['chieu']} {x['vao']} {x['R']:+.1f}R" for x in big))
  # tong lai cua 10% lenh tot nhat
  s=sorted(R,reverse=True); n=max(1,len(s)//10)
  print(f"  10% lenh tot nhat ({n} lenh) mang ve {sum(s[:n]):+.1f}R; 90% con lai {sum(s[n:]):+.1f}R")
print("Tuan thi truong:", ", ".join(f"{k.strftime('%d/%m')} {loai_tuan(k)}" for k in sorted(W)))
