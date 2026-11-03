#!/bin/zsh
S="${0:h}"; OUT="$S/khoa2r.txt"; : > "$OUT"; source "$S/lib.sh"; moi
C="/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading"
BASE='"InpRuiRoGoc=2.0","InpAG_Bat=true","InpAG_ThuaLT=3","InpAG_NghiGio=8","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100","InpSutNguong=0","InpD1Ban=true","InpMuaTre=30","InpChanMuaH4=false","InpBanDieuChinh=false","InpKhoaKieu=2","InpBanTreD1=0","InpEmaMoc=99","InpMocBan=1","InpBanChuoi=true","InpD1Bo3D=true","InpD1RsiMua=50","InpD1BoNhieu=false"'
P40=1
chay(){ local X="$3"; [[ "$X" == *PhanTram* ]] || X="$X,\"InpKhoaPhanTram=40\""; setf v2_7 "KR_$1_$2" "$BASE,$X" || return; KY=$1; rep "$1 $2" "$(bt v2_7 ',"inputs_path":"'"$PT"'\\TT_KR_'"$1_$2"'.set"')"; cp "$C/TEST_NhatKy_BTCUSDm_24270000.csv" "$S/nk_KR_$1_$2.csv"; }
chay T500 k3    '"InpKhoaTu=3"'
chay T500 k2    '"InpKhoaTu=2"'
chay T500 k15   '"InpKhoaTu=1.5"'
chay T500 k2p50 '"InpKhoaTu=2","InpKhoaPhanTram=50"'
chay T500 k1p50 '"InpKhoaTu=1","InpKhoaPhanTram=50"'
chay T2K  k3    '"InpKhoaTu=3"'
chay T2K  k2p50 '"InpKhoaTu=2","InpKhoaPhanTram=50"'
echo XONG >> "$OUT"
