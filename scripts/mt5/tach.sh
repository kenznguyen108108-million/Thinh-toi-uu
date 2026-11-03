#!/bin/zsh
S="${0:h}"; OUT="$S/tach.txt"; : > "$OUT"; source "$S/lib.sh"; moi
C="/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading"
M5ONLY='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0.5","InpAG_Bat=false","InpAG_ThuaLT=999","InpAG_NghiGio=24","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100"'
AGONLY='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0","InpAG_Bat=true","InpAG_ThuaLT=3","InpAG_NghiGio=24","InpAG_LoNgay=3.0","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100"'
setf v2_6 KT_m5only "$M5ONLY"; setf v2_6 KT_agonly "$AGONLY"
for x in m5only agonly; do KY=L6; rep "L6 $x" "$(bt v2_6 ',"inputs_path":"'"$PT"'\\TT_KT_'"$x"'.set"')"; cp "$C/TEST_NhatKy_BTCUSDm_24260000.csv" "$S/nk_L6_$x.csv"; done
echo XONG >> "$OUT"
