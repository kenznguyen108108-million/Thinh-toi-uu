import json,urllib.request,time,csv,sys
out=sys.argv[1]; t=1735689600000  # 2025-01-01 UTC
end=int(time.time()*1000); rows=[]
while t<end:
  u=f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=5m&startTime={t}&limit=1000"
  d=json.load(urllib.request.urlopen(u,timeout=30))
  if not d: break
  rows+= [[r[0],r[1],r[2],r[3],r[4]] for r in d]
  t=d[-1][0]+300000
with open(out,'w') as f: csv.writer(f).writerows(rows)
print(len(rows))
