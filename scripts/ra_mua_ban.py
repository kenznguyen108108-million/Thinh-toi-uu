# Vong 30 (03/11/2026): ra soat luat MUA va BAN cua he ETH tot nhat (vong 29): tung phan, tung nam, lenh dam nhat bao nhieu R.
# Chay: python3 -I ra_mua_ban.py <thu muc data>
import sys,os,runpy,io,contextlib,datetime as dt; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
sys.argv=['chat_luong.py',sys.argv[1]]
with contextlib.redirect_stdout(io.StringIO()): g=runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)),'chat_luong.py'))
L,NG=g['L'],g['NG']
TEN={('H1',1):'MUA H1 (RSI cat len 55)',('H4',1):'MUA H4 (RSI 55, phe D1 tang)',('M15',1):'MUA M15 (MH3a RSI>=70)',('M15',-1):'BAN M15 (MH3a RSI<=30)',('H1ban',-1):'BAN H1 (H4 vua cat xuong)'}
ngay=lambda t:dt.datetime.utcfromtimestamp(t).strftime('%d/%m/%y')
def tk(g):
  if not g: return "  0L"
  w=[x['R'] for x in g if x['R']>0]
  return f"{len(g):4d}L thang {100*len(w)/len(g):3.0f}% | {sum(x['R'] for x in g)/len(g):+.2f}R/lenh | thang TB {sum(w)/max(1,len(w)):.2f}R | dam nhat {max(x['R'] for x in g):+.1f}R | thua nang nhat {min(x['R'] for x in g):+.1f}R"
for loc,f in (('TAT CA tin hieu',lambda x:True),('TOP 30% (ban dang chon)',lambda x:x['diem']>=NG[0.3])):
  print(f"\n######## {loc}, ETH 2022 -> nay")
  for k,ten in TEN.items():
    gg=[x for x in L if f(x) and x['phan']==k[0] and x['h']==k[1]]
    print(f"\n{ten}: {tk(gg)}")
    print("  theo nam R/lenh: "+" | ".join(f"{y}: {len(h)}L {sum(x['R'] for x in h)/max(1,len(h)):+.2f}" for y in range(2022,2027) for h in [[x for x in gg if dt.datetime.utcfromtimestamp(x['t']).year==y]]))
    print("  phan bo lenh thang: "+" | ".join(f"{a}-{b}R: {sum(1 for x in gg if a<x['R']<=b)}" for a,b in ((0,1),(1,2),(2,3),(3,5),(5,10),(10,99))))
    top=sorted(gg,key=lambda x:-x['R'])[:5]
    print("  5 lenh dam nhat: "+", ".join(f"{ngay(x['t'])} {x['R']:+.1f}R" for x in top))
    bo3=sorted([x['R'] for x in gg],reverse=True)[3:]
    print(f"  bo 3 lenh lon nhat con: {sum(bo3):+.1f}R (tong {sum(x['R'] for x in gg):+.1f}R)")
