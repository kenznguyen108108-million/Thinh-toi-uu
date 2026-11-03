#!/bin/zsh
S="${0:h}"; OUT="$S/kiemtra.txt"; : > "$OUT"; source "$S/lib.sh"; moi
mkcfg(){ call '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"tester_prepare_config","arguments":{"mql5_program_path":"'"$D"'\\Experts\\ThinhTrading\\ThinhTrading_EMA_EA_v2_6.ex5","symbol":"BTCUSDm","model":"m1 ohlc","timeframe":"H1","from_date":"'"$2"'T00:00:00","to_date":"'"$3"'T00:00:00","deposit":500,"deposit_currency":"USD","leverage":200,"output_path":"'"$PT"'\\TT_'"$1"'_v2_6.ini"}}}' | grep -q '"isError":false' || echo "LOI CONFIG $1" >> "$OUT"; }
mkcfg KT3 2026-07-25 2026-10-25
mkcfg L6 2026-04-25 2026-10-25
GOC='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0","InpAG_Bat=false","InpAG_ThuaLT=999","InpAG_NghiGio=24","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100"'
TOHOP='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0.5","InpAG_Bat=true","InpAG_ThuaLT=3","InpAG_NghiGio=24","InpAG_LoNgay=3.0","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100"'
setf v2_6 KT_goc "$GOC"; setf v2_6 KT_tohop "$TOHOP"
chay(){ KY=$1; rep "$1 $2" "$(bt v2_6 ',"inputs_path":"'"$PT"'\\TT_KT_'"$2"'.set"')"; cp "/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading/TEST_NhatKy_BTCUSDm_24260000.csv" "$S/nk_$1_$2.csv"; }
chay KT3 goc
chay KT3 tohop
chay L6 goc
chay L6 tohop
echo XONG >> "$OUT"
