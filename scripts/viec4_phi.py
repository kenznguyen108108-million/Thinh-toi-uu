# VIEC CLOUD 4 (03/11/2026): phi/spread nang hon. PHI (rsi.py) = 0,06% (goc) / 0,10% / 0,15% gia moi lenh (khu hoi).
# Dat rsi.PHI TRUOC khi nap cac module khac (chung import PHI theo gia tri). Moi muc phi chay 1 tien trinh rieng.
# Phi ap cho moi cho tinh R (ca mo hinh diem, ban H1, mua moi). Chay: python3 -I viec4_phi.py <data> [phi]
import sys,os,subprocess; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv)>2:
  import rsi; rsi.PHI=float(sys.argv[2])
  import ban_thu,ban_sap,viec1_mua_dakhung
  for m in (ban_thu,ban_sap,viec1_mua_dakhung): m.PHI=rsi.PHI
  from moc import xay,nguong,chon,danh_gia,dong
  L=xay(sys.argv[1],'ETH',them_mua=True); q=nguong(L)
  print(dong(f'MOC-1 phi {rsi.PHI*100:.2f}% (nguong tinh lai {q:+.2f})',danh_gia(chon(L,q))))
  L0=xay(sys.argv[1],'ETH'); print(dong(f'MOC vong 30 phi {rsi.PHI*100:.2f}%',danh_gia(chon(L0,nguong(L0)))),flush=True)
else:
  from moc import TIEU_DE; print(TIEU_DE,flush=True)
  for p in ('0.0006','0.001','0.0015'):
    subprocess.run([sys.executable,'-I',os.path.abspath(__file__),sys.argv[1],p])
