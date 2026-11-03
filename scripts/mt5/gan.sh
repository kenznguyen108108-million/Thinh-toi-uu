S="${0:h}"; OUT=/dev/null; source "$S/lib.sh"; moi
call '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"chart_add_expert","arguments":{"chart_id":"70913810952245","expert_path":"C:\\Program Files\\MetaTrader 5\\MQL5\\Experts\\ThinhTrading\\ThinhTrading_EMA_EA_v2_7.ex5"}}}' | head -c 300; echo
sleep 3
call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_open_charts","arguments":{}}}' | sed 's/\\"/"/g' | grep -oE '"(title|name|chart_id)": "[^"]*"'
T0=$(date -v-2M '+%Y-%m-%dT%H:%M:%S'); T1=$(date -v+1M '+%Y-%m-%dT%H:%M:%S')
call '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"get_expert_journal","arguments":{"datetime_from":"'"$T0"'","datetime_to":"'"$T1"'","limit":30}}}' | sed 's/\\"/"/g' | grep -oE '"message": "[^"]*"' | tail -6
