#!/bin/zsh
# Bien dich EA bang dong lenh MetaEditor (KHONG can MCP). Dung: bd_cli.sh ThinhTrading_EMA_EA_v2_8
# Chep .mq5 + NenTang/*.mqh tu 01-Trading/ThinhTrading vao MT5 roi bien dich; in dong ket qua.
TEN="${1:?ten file khong co .mq5}"; SRC="$HOME/TongTuLenh/01-Trading/ThinhTrading"
P="$HOME/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5"; E="$P/MQL5/Experts/ThinhTrading"
W="/Applications/MetaTrader 5.app/Contents/SharedSupport/wine"
mkdir -p "$E/NenTang" && cp "$SRC/$TEN.mq5" "$E/" && cp "$SRC"/NenTang/*.mqh "$E/NenTang/"
cd "$P" && WINEPREFIX="$HOME/Library/Application Support/net.metaquotes.wine.metatrader5" WINEDLLOVERRIDES="mscoree=" \
  DYLD_FALLBACK_LIBRARY_PATH="$W/lib/external:/usr/lib" WINEDEBUG=-all "$W/bin/wine64" metaeditor64.exe \
  "/compile:MQL5\\Experts\\ThinhTrading\\$TEN.mq5" "/log:MQL5\\Experts\\ThinhTrading\\$TEN.log"
iconv -f UTF-16 -t UTF-8 "$E/$TEN.log" | grep -E "error|warning|Result" | tail -15
cp "$E/$TEN.ex5" "$SRC/" 2>/dev/null && echo "da chep $TEN.ex5 ve $SRC"
