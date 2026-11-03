# Tai nen Binance: python3 -I dl2.py <out.csv> <SYMBOL> <interval 15m/1h> <tu YYYY-MM-DD>
import json,urllib.request,time,csv,sys,datetime as dt
out,sym,iv,tu=sys.argv[1:5]; step={'5m':300,'15m':900,'1h':3600,'4h':14400}[iv]*1000
t=int(dt.datetime.strptime(tu,'%Y-%m-%d').replace(tzinfo=dt.timezone.utc).timestamp()*1000)
end=int(time.time()*1000); rows=[]
while t<end:
  d=json.load(urllib.request.urlopen(f"https://api.binance.com/api/v3/klines?symbol={sym}&interval={iv}&startTime={t}&limit=1000",timeout=30))
  if not d: break
  rows+=[[r[0],r[1],r[2],r[3],r[4]] for r in d]; t=d[-1][0]+step
with open(out,'w') as f: csv.writer(f).writerows(rows)
print(len(rows))
