# Việc cho phiên CLOUD (dùng credit cloud, hết hạn 05/11/2026 14:59 GMT+7)

Bối cảnh: nghiên cứu hệ thống B (ETH) cho anh Thịnh. Đọc `CLAUDE.md` (của TOI-UU) và `OPTIMIZATION-LOG.md` từ **Vòng 19 tới Vòng 30** trước.
Bot A (EMA v2.7, BTC) đang chạy tiền thật trên VPS — phiên cloud KHÔNG liên quan, không có MT5, chỉ Python.

## Quy tắc
- Chạy `python3 -I scripts/<file>.py data ...` từ thư mục gốc repo. Dữ liệu Binance trong `data/` (BTC/ETH 15m từ 2022; 1h/4h/1d từ 2018).
- Mỗi việc đổi 1 thứ, so với **MỐC** bằng cùng bộ mô phỏng `scripts/von500.py` (vốn 500 USD, lot thật, áo giáp thua 3 nghỉ 8h) và theo từng năm 2022–2026. Không hơn mốc thì ghi "bỏ".
- Chống khớp quá: chọn tham số trên dữ liệu cũ, kiểm tra trên dữ liệu sau; thử tham số lân cận; báo cả mặt xấu.
- **MỐC hiện tại** = hệ ETH vòng 30: MUA (RSI 55/45 H1, H4 lọc phe D1, MH3a M15) + BÁN H1 khi H4 vừa có EMA9(RSI) cắt xuống WMA45 (gồng đỉnh 40 nến), chỉ giữ top 30% điểm hành trình, rủi ro 3% (script `scripts/chat_luong.py`, bỏ phần BÁN M15). Lãi kép 500 USD từ 2022 → ~22.240 USD, sụt 38%.
- Ghi kết quả từng việc vào **`KET-QUA-CLOUD.md`** (tiếng Việt, ngắn, có bảng số), commit + push sau MỖI việc (để nếu hết credit giữa chừng vẫn còn kết quả).

## Danh sách việc (làm theo thứ tự, hết credit thì dừng)
1. **Luật MUA đối xứng luật bán mới:** MUA H1 khi H4 vừa có EMA9(RSI) cắt LÊN WMA45 (vào ngay, gồng theo đáy thấp nhất 40 nến / hoặc nền tảng). Thay hoặc thêm vào MUA H1 cũ. Thử K=2/4 nến, dốc 0/3/6 (giống `scripts/ban_dakhung.py`). Luật MUA hiện yếu năm 2022 (MUA H1 −0,17R/lệnh).
2. **Rà lệnh MUA thua** (như vòng 26 đã làm cho BÁN, `scripts/phan_tich_v19.py`): bối cảnh D1, loại thua, năm nào hỏng → đề xuất sửa → kiểm chứng.
3. **Độ bền ngưỡng chất lượng:** top 20/25/30/35/40%; đặt ngưỡng walk-forward (mỗi năm dùng ngưỡng từ các năm trước).
4. **Phí/spread nặng hơn:** PHI 0,1% và 0,15% (biến `PHI` trong `scripts/rsi.py`) — hệ còn lãi không.
5. **Lọc biến động thấp:** ATR% D1 thấp (như năm 2023, biên độ ngày TB 3,6%) → giảm rủi ro/nghỉ. Ngưỡng chọn trên 2018–2021.
6. **Áp hệ cho BTC** (cùng luật) và đo tương quan lỗ cùng tháng với hệ ETH.
7. (Nếu còn credit) vàng: tải PAXGUSDT 1h/4h/1d từ Binance bằng `scripts/dl_dai.py`, chạy cùng hệ.

Cuối cùng: tóm tắt 5–10 dòng ở đầu `KET-QUA-CLOUD.md`: cái gì HƠN mốc (giữ), cái gì bỏ.
