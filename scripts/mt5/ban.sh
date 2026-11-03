#!/bin/zsh
S="${0:h}"; OUT="$S/ban.txt"; : > "$OUT"; source "$S/lib.sh"; moi
C="/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading"
BASE='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0.5","InpAG_Bat=false","InpAG_ThuaLT=999","InpAG_NghiGio=24","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100","InpEmaMoc=99","InpBanChuoi=true"'
mk(){ echo "$BASE,\"InpMocBan=$2\",\"InpBanM5=$3\",\"InpChanMuaGiam=$4\""; }
chay(){ local ten=$1; setf v2_6 "B_$ten" "$(mk "$@")" || return; for ky in L6 6M; do KY=$ky; rep "$ky $ten" "$(bt v2_6 ',"inputs_path":"'"$PT"'\\TT_B_'"$ten"'.set"')"; cp "$C/TEST_NhatKy_BTCUSDm_24260000.csv" "$S/nk_${ky}_B_$ten.csv"; done; }
chay B0_goc          0 false false
chay B1_D1ema20_M5   1 true  false
chay B2_D1ema99_M5   2 true  false
chay B3_TuanEma_M5   3 true  false
chay B4_RSI3D_M5     4 true  false
chay B5_D1ema20_chan 1 true  true
chay B6_D1ema99_chan 2 true  true
echo XONG >> "$OUT"
