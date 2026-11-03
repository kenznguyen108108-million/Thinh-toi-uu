#!/bin/zsh
S="${0:h}"; OUT="$S/sap.txt"; : > "$OUT"; source "$S/lib.sh"; moi
C="/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading"
mkcfg(){ call '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"tester_prepare_config","arguments":{"mql5_program_path":"'"$D"'\\Experts\\ThinhTrading\\ThinhTrading_EMA_EA_v2_6.ex5","symbol":"BTCUSDm","model":"m1 ohlc","timeframe":"H1","from_date":"'"$2"'T00:00:00","to_date":"'"$3"'T00:00:00","deposit":500,"deposit_currency":"USD","leverage":200,"output_path":"'"$PT"'\\TT_'"$1"'_v2_6.ini"}}}' | grep -q '"isError":false' || echo "LOI CONFIG $1" >> "$OUT"; }
mkcfg S1 2025-01-15 2025-04-15
mkcfg S2 2025-10-01 2025-11-25
mkcfg S3 2026-01-10 2026-02-12
mkcfg S4 2026-05-01 2026-06-10
BASE='"InpRuiRoGoc=2.0","InpKeoM15=false","InpTranLotMin=4.0","InpM5TP=0.5","InpAG_Bat=false","InpAG_ThuaLT=999","InpAG_NghiGio=24","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100","InpEmaMoc=99","InpBanChuoi=true"'
setf v2_6 S_cu   "$BASE,\"InpMocBan=0\",\"InpBanM5=false\",\"InpChanMuaGiam=false\",\"InpBanGiuC=false\""
setf v2_6 S_C1   "$BASE,\"InpMocBan=1\",\"InpBanM5=false\",\"InpChanMuaGiam=true\",\"InpBanGiuC=true\""
setf v2_6 S_C1M5 "$BASE,\"InpMocBan=1\",\"InpBanM5=true\",\"InpChanMuaGiam=true\",\"InpBanGiuC=true\""
for ky in S1 S2 S3 S4; do for x in cu C1 C1M5; do
  KY=$ky; rep "$ky $x" "$(bt v2_6 ',"inputs_path":"'"$PT"'\\TT_S_'"$x"'.set"')"; cp "$C/TEST_NhatKy_BTCUSDm_24260000.csv" "$S/nk_${ky}_$x.csv"
done; done
echo XONG >> "$OUT"
