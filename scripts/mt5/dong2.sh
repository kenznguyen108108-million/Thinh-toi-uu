S="${0:h}"; OUT=/dev/null; source "$S/lib.sh"; moi
call '{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"get_expert_advisor_parameters","arguments":{"chart_id":"70913810952245"}}}' | sed 's/\\"/"/g' | grep -oE '"InpKhoa[A-Za-z]*"[^}]*' | head -5
for c in $(call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_open_charts","arguments":{}}}' | sed 's/\\"/"/g' | grep -oE '"chart_id": "[0-9]+"' | grep -oE '[0-9]+' | grep -v 70913810952245); do
 call '{"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"chart_close","arguments":{"chart_id":"'$c'"}}}' | grep -q '"isError":false' && echo "dong $c"; done
call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_open_charts","arguments":{}}}' | sed 's/\\"/"/g' | grep -oE '"chart_id": "[0-9]+"'
