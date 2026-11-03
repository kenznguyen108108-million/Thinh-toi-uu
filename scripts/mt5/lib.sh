# Thu vien chung: backtest qua MCP MT5, moi luot mo phien moi + thu lai
K="${MT5_KEY:?Dat MT5_KEY = Bearer key MCP MT5 (xem ~/.claude.json)}"; U=http://127.0.0.1:22346/mcp
D='C:\\Program Files\\MetaTrader 5\\MQL5'; PT="$D"'\\Profiles\\Tester'
SID=""
moi(){ local H=$(mktemp)
  curl -s -D "$H" -o /dev/null -m 15 -X POST $U -H "Authorization: Bearer $K" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"0.1"}}}'
  SID=$(grep -i '^mcp-session-id' "$H" | awk '{print $2}' | tr -d '\r')
  call1 '{"jsonrpc":"2.0","method":"notifications/initialized"}' >/dev/null
  call1 '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_workspace_info","arguments":{}}}' >/dev/null; }
call1(){ curl -s -m 3700 -X POST $U -H "Authorization: Bearer $K" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -H "Mcp-Session-Id: $SID" -d "$1"; echo; }
# goi, neu loi phien / rong thi mo phien moi va thu lai (toi da 3 lan)
call(){ local r; for n in 1 2 3; do r=$(call1 "$1"); if [ -n "${r// /}" ] && ! echo "$r" | grep -q 'not initialized\|"error"'; then echo "$r"; return; fi; sleep 10; moi; done; echo "$r"; }
setf(){ call '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"tester_prepare_inputs","arguments":{"mql5_program_path":"'"$D"'\\Experts\\ThinhTrading\\ThinhTrading_EMA_EA_'"$1"'.ex5","parameters":['"$3"'],"output_path":"'"$PT"'\\TT_'"$2"'.set"}}}' | grep -q '"isError":false' || { echo "LOI SET $2 -> bo qua" >> "$OUT"; return 1; }; }
bt(){ call '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"tester_run_backtest","arguments":{"config_path":"'"$PT"'\\TT_'"${KY:-HL}"'_'"$1"'.ini"'"$2"',"wait":true,"timeout_sec":3600}}}'; }
rep(){ local RID=$(echo "$2" | grep -oE 'run_id[^0-9]*[0-9]+' | grep -oE '[0-9]+$') r=""
  for n in 1 2 3 4 5 6; do
    r=$(call '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"tester_get_report","arguments":{"run_id":"'"$RID"'"}}}' | sed 's/\\n/ /g; s/\\"/"/g' | grep -oE '"(profit|profit_factor|trades|profit_trades|rel_drawdown_percent_equity|drawdown_percent_balance|max_consecutive_loss_trades|balance_min|recovery_factor)": ?[^,}]*' | sed 's/"//g' | tr '\n' ' ')
    [ -n "$r" ] && break; sleep 15; done
  echo "$1 [run $RID]: $r" >> "$OUT"; [ -z "$r" ] && echo "  raw: $(echo "$2" | head -c 400)" >> "$OUT"; }
