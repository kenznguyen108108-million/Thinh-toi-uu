# 01-Trading / TOI-UU — Vòng nghiên cứu tối ưu bot EMA (bắt đầu 25/10/2026)

Phiên làm dự án con này. Xưng "em", gọi "anh". Link file ghi đủ đường dẫn từ `TongTuLenh/`.
Đọc file này + `01-Trading/TOI-UU/OPTIMIZATION-LOG.md` trước. Ghi kết quả mỗi vòng vào OPTIMIZATION-LOG.md trước khi dừng.

## Yêu cầu của anh (25/10)
"Chạy backtest, so với thị trường thực tế: tại sao lúc đó thua (bị kill ngay? fake out?), tại sao tăng mạnh / giảm mạnh,
ngược hay cùng pha khung lớn → kết luận → sửa code → backtest. Làm vài vòng ra bản tối ưu và mạnh nhất."
Anh ưu tiên **bảo vệ tài khoản khi thị trường khùng** hơn lợi nhuận tối đa.

## Điểm xuất phát (backtest 25/07 → 25/10/2026, BTCUSDm, M1 OHLC, vốn 243,39, chart H1)
| Bản | Lãi | PF | Lệnh (thắng/thua) | Sụt vốn equity | Sụt số dư | Thua liên tiếp max | Recovery |
|---|---|---|---|---|---|---|---|
| v2.4 (rủi ro 2%, không áo giáp) | +772,50 (+317%) | 2,21 | 113 (46/67) | 41,6% | 29,4% | 20 | 1,65 |
| v2.5 (rủi ro 1% + áo giáp 7 lớp) | +138,90 (+57%) | 2,68 | 47 (16/31) | 13,2% | 8,1% | 6 | 2,88 |
- Giai đoạn 12–25/10: v2.4 vào 6 lệnh BUY M15/M5, thua cả 6 (BTC đi ngang giật 79–85k, đỉnh thấp dần).
- v2.5 giảm sụt vốn ~3 lần nhưng cắt mất nhiều lệnh thắng (113 → 47 lệnh). Một nửa mức giảm lãi là do rủi ro 2% → 1%.

## Dữ liệu & chống "khớp quá" (BẮT BUỘC)
- Lịch sử BTCUSDm có từ 29/12/2024.
- **Tập huấn luyện (được tối ưu):** 01/01/2025 → 24/07/2026.
- **Tập kiểm tra (KHÔNG tối ưu, chỉ kiểm tra cuối):** 25/07/2026 → 25/10/2026.
- Mỗi vòng chỉ đổi **1–2 thứ**. Giữ thay đổi chỉ khi trên tập huấn luyện: PF tăng **và** sụt vốn equity không tăng **và** số lệnh không giảm quá 40%.
- Sau 3–4 vòng mới chạy tập kiểm tra 1 lần. Nếu tập kiểm tra tệ hơn rõ rệt → thay đổi bị "khớp quá", quay lại.

## Quy trình mỗi vòng
1. Backtest bản hiện tại trên tập huấn luyện (MCP MT5 22346: tester_prepare_config → tester_run_backtest wait → tester_get_report).
2. Lấy danh sách lệnh từ tester journal (dòng "ThinhTrading BUY/SELL ... | Entry | SL" và "THOAT ... R").
3. Với từng lệnh THUA (và vài lệnh THẮNG lớn để đối chiếu): get_chart_history (period M15/H1/H4/D1) quanh điểm vào, phân loại:
   - **Fake out:** giá vượt rồi quay đầu chạm SL trong ≤ N nến.
   - **Ngược pha khung lớn:** H4/D1 EMA10 < EMA20 lúc MUA (hoặc ngược lại), giá dưới SMA50 D1.
   - **Thị trường đi ngang:** biên độ hẹp nhiều ngày, EMA cắt qua lại, ADX thấp.
   - **Nến giật / tin tức:** nến vào lệnh hoặc nến chạm SL dài > 2× trung bình.
   - **SL quá sát:** khoảng SL < ~0,5× ATR của khung.
   Và với lệnh THẮNG lớn: xu hướng thế nào, cùng pha khung lớn không.
4. Đếm tỉ lệ từng nguyên nhân → **kết luận** → giả thuyết sửa (vd: bắt buộc cùng pha H4+D1 cho M5/M15; chờ nến xác nhận; SL tối thiểu theo ATR; bỏ M5).
5. Tạo file mới `01-Trading/ThinhTrading/ThinhTrading_EMA_EA_v2_6.mq5` (v2.7, v2.8... cho các vòng sau), copy từ bản tốt nhất, magic khác, sửa, biên dịch (0 lỗi), backtest, so sánh.
6. Ghi vào OPTIMIZATION-LOG.md: thay đổi, số liệu trước/sau, giữ hay bỏ, lý do.

## Kỹ thuật
- Mã nguồn UTF-8 có BOM. Chép .mq5 vào `~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Experts/ThinhTrading/`.
- Biên dịch: chạy nền MetaEditor:
  `W="/Applications/MetaTrader 5.app/Contents/SharedSupport/wine"; cd /tmp && WINEPREFIX="$HOME/Library/Application Support/net.metaquotes.wine.metatrader5" WINEDLLOVERRIDES="mscoree=" DYLD_FALLBACK_LIBRARY_PATH="$W/lib/external:/usr/lib" WINEDEBUG=-all "$W/bin/wine64" "C:\\Program Files\\MetaTrader 5\\metaeditor64.exe"`
  rồi MCP MetaEditor `http://127.0.0.1:22345/mcp` → `compile_file`. Xong: `pkill -f metaeditor64`.
- Bearer key MCP: xem ~/.claude.json (mcpServers.mt5) hoặc MT5 → Công cụ → Tùy chọn → MCP.
- get_chart_history cần: symbol, period, datetime_from, datetime_to.
- Backtest 3 tháng ~3–5 phút; 19 tháng lâu hơn nhiều → có thể chia nửa.

## Ranh giới
- KHÔNG sửa `ThinhTrading_EMA_EA_v2_4.mq5`, `BAN-GOC-v2.4/`.
- Bot đang chạy tiền thật là v2.7 trên VPS (từ 01/11/2026). Muốn đưa bản mới lên VPS: báo anh, anh tự đồng bộ.
- Chỉ chạy Strategy Tester. Không bật Algo Trading, không đặt lệnh thật.
- Báo số liệu thật, cả mặt xấu. Không hứa lợi nhuận.
