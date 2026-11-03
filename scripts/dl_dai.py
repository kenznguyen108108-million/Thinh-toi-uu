# Tai nen dai tu Binance: python3 -I dl_dai.py <SYMBOL> <interval> <tu_ms> <file_ra>
import json,urllib.request,time,csv,sys
sym,itv,t,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]; rows=[]
end=int(time.time()*1000)
while t<end:
  d=json.load(urllib.request.urlopen(f"https://api.binance.com/api/v3/klines?symbol={sym}&interval={itv}&startTime={t}&limit=1000",timeout=30))
  if not d: break
  rows+=[[r[0],r[1],r[2],r[3],r[4]] for r in d]; t=d[-1][6]+1
with open(out,'w') as f: csv.writer(f).writerows(rows)
print(sym,itv,len(rows))
