# Nghiên cứu luật M5 & Dow — 26/10/2026

Dữ liệu: nến BTCUSDT 5 phút của Binance, 01/01/2025 → 26/10/2026 (191.116 nến; giá sát BTCUSDm Exness).
Phí: trừ $16/lệnh (spread ước tính), đã thử thêm $30 và $50. Lệnh chạm cả SL lẫn TP trong cùng 1 nến M5 → tính là thua.
Tập huấn luyện (HL): đến 24/07/2026. Tập kiểm tra (KT): 25/07 → 26/10/2026. Kết quả tính bằng R (1R = khoản chấp nhận mất).
Script: `01-Trading/TOI-UU/scripts/` (dl.py tải dữ liệu; m5.py, dow*.py, rng*.py là các luật).

## 1. M5 "3 nến tăng → mua, SL đáy nến 1, ăn 2R" → BỎ
| Biến thể | Lệnh | Thắng | TB/lệnh | Tổng |
|---|---|---|---|---|
| Chưa tính phí | 4023 | 33,0% | −0,01R | −39R |
| Có phí | 4023 | 33,0% | −0,10R | −401R |
| + H1 xu hướng tăng, SL ≥ $100 | 2039 | 32,7% | −0,09R | −179R |
| Bán đối xứng (3 nến giảm, H1 giảm) | 2525 | 33,5% | −0,09R | −216R |
| Ăn 1R / 1,5R / 3R (H1 tăng, chưa tính phí) | — | 48% / 38% / 24% | −0,04 / −0,04 / −0,05R | — |
→ Thắng đúng bằng tỉ lệ may rủi (1:2 → 33%). Ba nến tăng **không** báo trước nến tiếp theo tăng. Phí spread ăn ~0,1R mỗi lệnh vì SL M5 rất ngắn.
→ **Ăn ngắn trên M5 với luật đơn giản thì không có lợi thế, càng đánh nhiều càng lỗ phí.**

## 2. Dow: phá cấu trúc (đỉnh thấp dần + phá đáy → bán; ngược lại → mua)
- Hai nhịp anh nói có thật trên H4: đỉnh đôi 87,2k/87,0k → phá đáy 84,97k → 80,4k; hồi 84,9k (thấp hơn) → phá 80,94k → 79,2k.
- **Bán phá đáy H1:** HL rất đẹp (+0,2 đến +0,6R/lệnh), nhưng **KT âm** (−0,4 đến −0,6R). Lý do: 2025–07/2026 phần lớn là thị trường giảm (126k → 64k), còn tháng 8–10/2026 là thị trường tăng.
- **Hai chiều + kéo SL + lọc D1/SMA50:** k=5 rất đẹp (HL +0,38R, KT +1,07R) nhưng **không bền**. Đổi k sang 4/6/7 là KT âm; lãi dồn vào 2 lệnh (+18R, +14R); bỏ 5 lệnh lớn nhất thì tổng âm.
- Hai nhịp tháng 10: bot vào nhưng đều thua (13/10 −1,3R; 21/10 −1,0R). Giá giật qua lại quanh đỉnh/đáy nên SL theo đỉnh H1 bị quét.
→ **Không dùng.** Đây là kiểu chọn tham số "trúng số" trên dữ liệu cũ.

## 3. Dow: tích luỹ → phá vùng → kéo SL — ỨNG VIÊN TỐT NHẤT
Luật:
- Vùng tích luỹ = biên độ N nến H1 gần nhất ≤ 3% giá.
- Nến H1 đóng cửa vượt đỉnh vùng → MUA, thủng đáy vùng → BÁN, **chỉ khi cùng chiều D1** (giá đóng cửa D1 trên SMA50 thì chỉ mua, dưới thì chỉ bán).
- SL ở giữa vùng. Kéo SL theo đáy/đỉnh thấp nhất/cao nhất của 12 nến H1, không đặt TP — để lệnh chạy theo xu hướng.

| N nến | Tập | Lệnh | Thắng | TB/lệnh | Tổng | Sụt max | Thua LT |
|---|---|---|---|---|---|---|---|
| 24 | HL | 168 | 37,5% | +0,28R | +46,4R | 13,3R | 8 |
| 24 | KT | 38 | 26,3% | +0,15R | +5,7R | 6,7R | 9 |
| 36 | HL | 103 | 34,0% | +0,21R | +21,5R | 7,3R | 8 |
| 36 | KT | 26 | 30,8% | +0,15R | +4,0R | 3,3R | 6 |
| 48 | HL | 65 | 40,0% | +0,42R | +27,4R | 5,4R | 6 |
| 48 | KT | 19 | 36,8% | +0,31R | +5,8R | 2,8R | 4 |

Điểm mạnh: dương ở cả HL lẫn KT với mọi N (24/36/48) và mọi độ rộng 2–4% (trừ 48 nến ≤2%: KT 7 lệnh âm). Phí $50 vẫn dương. 6/8 quý dương (24 nến).
Điểm yếu, nói thẳng:
- Lãi nhỏ (+0,15 đến +0,4R/lệnh). Phần lớn lãi đến từ vài con sóng lớn: bỏ 5 lệnh lớn nhất thì gần hoà (24 nến) hoặc âm (36/48 nến). Đây là bản chất của đánh theo xu hướng: thua nhỏ nhiều lần, chờ 1 con sóng lớn.
- Quý gần nhất (Q4/2026) âm nhẹ (−1,5 đến −2,9R). Tháng 10: 9 lệnh, chỉ 2 lệnh lãi nhỏ.
- Đặc tính giống bot EMA v2.4 (M15 +0,35R/lệnh, vòng 1a) — chưa chắc tốt hơn, có thể dùng **bổ sung** cho nhau.
- Mô phỏng bằng Python trên dữ liệu Binance (giờ UTC), chưa chạy trong MT5 với dữ liệu Exness thật.

## Kết luận
1. Bỏ M5 ăn ngắn. Bỏ "bán phá đáy" đứng một mình.
2. Logic tốt nhất tìm được: **tích luỹ → phá vùng cùng chiều D1 → kéo SL**. Đúng tinh thần Dow anh nói: không có vùng tích luỹ thì không vào; khi thị trường giảm mạnh thì có ăn phía bán.
3. **Chưa đủ để chạy tiền thật.** Các bước còn thiếu:
   (a) đưa luật vào EA MT5 (v2.7, magic riêng) và backtest trên dữ liệu Exness;
   (b) chạy demo/theo dõi 4–8 tuần;
   (c) nếu khớp với backtest thì vào tiền thật rủi ro 0,5–1%/lệnh với vốn nhỏ.

## Cập nhật 2b — so với v2.4: KÉM HƠN → không code
v2.4 (MT5, 01/01→25/10/2026, vốn 500, 2%): +525%, sụt số dư 35,6%. Luật tích luỹ 24 nến cùng điều kiện: +96%, sụt 15,7%. Lãi/sụt: v2.4 ≈ 15, luật mới ≈ 5–6. Chi tiết ở OPTIMIZATION-LOG.md vòng 2b.
