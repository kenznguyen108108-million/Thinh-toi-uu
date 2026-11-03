S="${0:h}"   # bien dich v2.7 qua MCP MetaEditor (mo MetaEditor truoc, xem TOI-UU/CLAUDE.md); ket qua -> bien_dich.txt
K="${MT5_KEY:?dat bien MT5_KEY}"; U=http://127.0.0.1:22345/mcp; for i in $(seq 1 40); do curl -s -o /dev/null -m 3 $U && break; sleep 2; done; sleep 3; H=$(mktemp)
curl -s -D "$H" -o /dev/null -m 15 -X POST $U -H "Authorization: Bearer $K" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"0.1"}}}'
SID=$(grep -i '^mcp-session-id' "$H" | awk '{print $2}' | tr -d '\r')
call(){ curl -s -m 180 -X POST $U -H "Authorization: Bearer $K" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -H "Mcp-Session-Id: $SID" -d "$1"; echo; }
call '{"jsonrpc":"2.0","method":"notifications/initialized"}' >/dev/null; call '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_workspace_info","arguments":{}}}' >/dev/null
call '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"compile_file","arguments":{"path":"C:\\Program Files\\MetaTrader 5\\MQL5\\Experts\\ThinhTrading\\ThinhTrading_EMA_EA_v2_7.mq5"}}}' | sed 's/\\n/\n/g; s/\\"/"/g' | grep -v "^info: C:" > "$S/bien_dich.txt"
pkill -f metaeditor64
