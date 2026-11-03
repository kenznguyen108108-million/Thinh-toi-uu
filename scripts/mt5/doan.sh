#!/bin/zsh
S="${0:h}"; OUT="$S/doan.txt"; : > "$OUT"; source "$S/lib.sh"; moi
# cho tester rong (lượt cũ bị dừng có thể còn chạy)
for n in {1..60}; do c=$(ps -Ao pcpu,comm | grep -i metatester | awk '{s+=$1}END{print s+0}'); [ "${c%.*}" -lt 5 ] && break; sleep 20; done
C="/Users/nguyencongquan/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading"
call '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"tester_prepare_config","arguments":{"mql5_program_path":"'"$D"'\\Experts\\ThinhTrading\\ThinhTrading_EMA_EA_v2_7.ex5","symbol":"BTCUSDm","model":"m1 ohlc","timeframe":"H1","from_date":"2026-04-01T00:00:00","to_date":"2026-06-10T00:00:00","deposit":5000,"deposit_currency":"USD","leverage":200,"output_path":"'"$PT"'\\TT_DOAN_v2_7.ini"}}}' | grep -q '"isError":false' || echo "LOI INI" >> "$OUT"
BASE='"InpRuiRoGoc=2.0","InpAG_Bat=true","InpAG_ThuaLT=3","InpAG_NghiGio=8","InpAG_LoNgay=100","InpAG_LoTuan=100","InpAG_ATRNhan=0","InpAG_SpreadNhan=100","InpAG_MaxLenh=100","InpAG_MaxRuiRoMo=100","InpAG_PhanhTong=100","InpSutNguong=0","InpD1Ban=true","InpMuaTre=30","InpChanMuaH4=false","InpBanDieuChinh=false","InpBanTreD1=0","InpEmaMoc=99","InpMocBan=1","InpBanChuoi=true","InpD1Bo3D=true","InpD1RsiMua=50","InpD1BoNhieu=false"'
chay(){ setf v2_7 "DOAN_$1" "$BASE,$2" || return; KY=DOAN; rep "$1" "$(bt v2_7 ',"inputs_path":"'"$PT"'\\TT_DOAN_'"$1"'.set"')"; cp "$C/TEST_NhatKy_BTCUSDm_24270000.csv" "$S/nk_DOAN_$1.csv"; }
chay k3     '"InpKhoaKieu=2","InpKhoaTu=3","InpKhoaPhanTram=40"'
chay k15    '"InpKhoaKieu=2","InpKhoaTu=1.5","InpKhoaPhanTram=40"'
chay k2p50  '"InpKhoaKieu=2","InpKhoaTu=2","InpKhoaPhanTram=50"'
chay tra1   '"InpKhoaKieu=1","InpKhoaTu=1.5","InpKhoaTraR=1"'
echo XONG >> "$OUT"
