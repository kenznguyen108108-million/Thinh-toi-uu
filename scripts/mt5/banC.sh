#!/bin/zsh
S="${0:h}"; OUT="$S/banC.txt"; : > "$OUT"; source "$S/lib.sh"; moi
C="/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading"
BASE='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0.5","InpAG_Bat=false","InpAG_ThuaLT=999","InpAG_NghiGio=24","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100","InpEmaMoc=99","InpBanChuoi=true"'
mk(){ echo "$BASE,\"InpMocBan=$2\",\"InpBanM5=$3\",\"InpChanMuaGiam=$4\",\"InpBanGiuC=$5\""; }
chay(){ local ten=$1; setf v2_6 "C_$ten" "$(mk "$@")" || return; for ky in L6 6M; do KY=$ky; rep "$ky $ten" "$(bt v2_6 ',"inputs_path":"'"$PT"'\\TT_C_'"$ten"'.set"')"; cp "$C/TEST_NhatKy_BTCUSDm_24260000.csv" "$S/nk_${ky}_C_$ten.csv"; done; }
chay C1_D1_chan_giuC  1 false true true
chay C2_D1_chan_tatM5 1 false true false
chay C3_Tuan_chan_giuC 3 false true true
echo XONG >> "$OUT"
