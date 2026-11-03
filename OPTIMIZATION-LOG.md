# Optimization log — nhật ký các vòng tối ưu bot

## Vòng 0 — 25/10/2026 (điểm xuất phát, tập 25/07→25/10/2026)
| Bản | Lãi | PF | Lệnh | Sụt equity | Thua LT max | Recovery |
|---|---|---|---|---|---|---|
| v2.4 | +772,50 | 2,21 | 113 | 41,6% | 20 | 1,65 |
| v2.5 (áo giáp) | +138,90 | 2,68 | 47 | 13,2% | 6 | 2,88 |

Nhận xét: áo giáp giảm sụt vốn ~3× và chuỗi thua 20 → 6, PF tăng; nhưng lãi giảm ~5,5× (một nửa do rủi ro 2%→1%, phần còn lại do các bộ lọc chặn cả lệnh thắng).
Việc vòng 1: phân tích lệnh thua v2.4 trên tập huấn luyện 01/01/2025→24/07/2026 theo quy trình trong CLAUDE.md.

## Vòng 0b — 25/10/2026: theo mức vốn & mức rủi ro (cùng tập 25/07→25/10/2026)
| Vốn | Bản | Lãi | % | Sụt equity | Thua LT | PF | Lệnh |
|---|---|---|---|---|---|---|---|
| 500 | v2.4 (2%) | +1442,51 | +288% | 43,4% | 22 | 2,05 | 121 |
| 500 | v2.5 (1%) | +204,19 | +41% | 19,4% | 10 | 2,07 | 61 |
| 500 | v2.5 (1,5%, MaxRuiRoMo 3) | +90,50 | +18% | 24,9% | 10 | 1,36 | 56 |
| 500 | v2.5 (2%, MaxRuiRoMo 4) | +237,35 | +47% | 28,9% | 9 | 1,69 | 59 |
| 2000 | v2.4 | +6315,92 | +316% | 46,6% | 23 | 2,03 | 122 |
| 2000 | v2.5 (1%) | +739,88 | +37% | 14,3% | 9 | 1,83 | 65 |
| 5000 | v2.4 | +15797,19 | +316% | 47,8% | 23 | 2,00 | 122 |
| 5000 | v2.5 (1%) | +2094,24 | +42% | 13,6% | 9 | 1,93 | 64 |

Kết luận: % lãi gần như độc lập với mức vốn. v2.4 lãi/sụt vốn tốt hơn (~6,7 vs ~2,2) nhưng sụt ~45% → không dùng được cho FTMO/vốn nhỏ.
Tăng rủi ro ở v2.5 KHÔNG tăng lãi tương ứng (1,5% còn tệ hơn 1%) → nghi phanh ngày/tuần cố định 3%/6% + lọc ATR/spread + max 2 lệnh đang chặn oan lệnh thắng.
**Mục tiêu vòng 1+:** giữ phần lớn sức tăng v2.4 với sụt equity ≤ ~20%. Thử: (a) mốc đối chiếu v2.4 rủi ro 1% không áo giáp; (b) phanh ngày/tuần co giãn theo rủi ro; (c) tắt từng bộ lọc (ATR/spread, max lệnh) xem bộ lọc nào chặn oan. Anh: vốn sắp nâng lên ~500 USD, giai đoạn đầu đánh chặt (v2.5 1%), sau tăng rủi ro nhẹ.

## Vòng 0c — 25/10/2026: v2.4 + phanh chuỗi thua (v2.5 tắt các lớp khác), vốn 500, rủi ro 2%, tập 25/07→25/10/2026
| Cấu hình | Lãi | % | Sụt equity | Sụt số dư | Thua LT | PF | Lệnh |
|---|---|---|---|---|---|---|---|
| v2.4 gốc | +1442,51 | +288% | 43,4% | — | 22 | 2,05 | 121 |
| + thua 4 → nghỉ 5h | +1592,83 | +319% | 40,2% | 27,5% | 17 | 2,19 | 114 |
| + thua 5 → nghỉ 5h | +1580,96 | +316% | 40,2% | 27,5% | 17 | 2,17 | 116 |
| + thua 4 → nghỉ 24h | +973,34 | +195% | 36,0% | 20,5% | 11 | 1,94 | 103 |
| v2.4 rủi ro 1%, không phanh | +583,92 | +117% | 32,9% | 22,6% | 22 | 2,00 | 120 |
| A: thua4/5h + tối đa 3 lệnh + rủi ro mở ≤4% | +760,80 | +152% | 28,6% | 22,6% | 13 | 2,13 | 68 |
| **B: A + TẮT nhồi lệnh** | **+1057,52** | **+211%** | **28,6%** | 22,6% | 13 | **2,23** | 79 |

Phát hiện: phanh chuỗi thua (nghỉ vài giờ) KHÔNG làm chuỗi ngắn đáng kể và sụt equity vẫn ~40% → nguyên nhân chính của sụt vốn sâu là **nhiều lệnh mở cùng lúc (6 khung + nhồi) cùng thả lỗ**, không phải chuỗi thua.
Ứng viên tốt nhất: **B** (lãi/sụt ≈ 7,4 vs v2.4 ≈ 6,7). CẢNH BÁO: các cấu hình này chọn trên chính tập 25/07→25/10 → phải kiểm tra lại trên tập 01/2025→07/2026 trước khi tin.

## Vòng 0d — 25/10/2026: từ đầu năm (01/01→25/10/2026), vốn 500, rủi ro 2%
| Cấu hình | Lãi | Vốn cuối | Sụt equity | Sụt số dư | Số dư thấp nhất | Thua LT | PF | Lệnh |
|---|---|---|---|---|---|---|---|---|
| v2.4 gốc | +2626,40 | ~3126 (+525%) | 46,5% | 35,6% | 388,11 | 23 | 1,62 | 385 |
| v2.4 + thua 4 → nghỉ 5h (anh chốt) | +1720,21 | ~2220 (+344%) | 46,6% | 29,2% | 384,02 | 17 | 1,56 | 354 |
→ Trên 10 tháng, phanh nghỉ 5h làm GIẢM lãi ~35%, sụt equity KHÔNG giảm; chỉ rút ngắn chuỗi thua 23→17 và sụt số dư 35,6→29,2%. Trái với kết quả 3 tháng → bài học "khớp quá" khi chọn luật trên dữ liệu ngắn.
| v2.4 rủi ro 1% (không phanh) | +1606,67 | ~2107 (+321%) | 38,0% | 21,0% | 390,72 | 23 | 1,67 | 387 |
→ 1%: lãi giảm ~39% so với 2% nhưng sụt số dư 35,6→21%; sụt equity vẫn 38% vì (1) vốn 500 → nhiều lệnh bị ép lot tối thiểu 0.01 (rủi ro thực > 1%, trần 4%), (2) nhiều lệnh mở cùng lúc.

## Vòng 1a — 26/10/2026: rà soát lệnh M15 (v2.4, 2%, vốn 500, 01/01→25/10/2026, 213 lệnh M15)
- Tổng M15: 213 lệnh, thắng 30%, **+75,5R** (TB +0,35R/lệnh) → M15 CÓ LÃI. 23 lệnh thắng lớn (≥3R) = +157,9R; bỏ chúng thì M15 âm → đúng kiểu đánh theo xu hướng.
- Bị quét nhanh: chỉ 17/139 lệnh thua chạm SL trong ≤60 phút; 57/139 trong ≤4h → fake out KHÔNG phải nguyên nhân chính.
- Cùng pha H4+D1 tăng: 59 lệnh, thắng 22%, TB **+0,19R** | Ngược pha (H4 hoặc D1 giảm): 154 lệnh, thắng 33%, TB **+0,42R** → lọc "chỉ đánh cùng pha" sẽ LÀM HẠI.
- Biến động H1 cao (>1,5× bình thường): 18 lệnh, thắng 67%, TB **+1,91R** (tốt nhất!) | thấp (<0,8×): +0,26R | bình thường: +0,18R → **bộ lọc "thị trường khùng" của v2.5 (chặn ATR cao) đang chặn đúng nhóm lệnh tốt nhất** → bỏ/đảo bộ lọc này.
- Lệnh KÉO M15: 16 lệnh, thắng 19%, **−6,4R** (TB −0,40R) → ứng viên tắt luật kéo ở M15.
- Theo giờ: 8–12h server thắng 23% (thấp nhất), còn lại 26–35% → chênh lệch nhỏ, chưa đủ cơ sở.
- (Dữ liệu M15 chỉ lấy được từ 12/09/2026 → thống kê SL/ATR M15 chỉ có 21 lệnh, chưa kết luận.)
**Đề xuất vòng 1b:** (1) tắt luật KÉO ở M15; (2) bỏ lọc ATR-cao của áo giáp; kiểm tra trên 01/2025→07/2026 rồi tập kiểm tra.

## Vòng 1b — 26/10/2026: tạo v2.6 (CHƯA backtest)
- File: `01-Trading/ThinhTrading/ThinhTrading_EMA_EA_v2_6.mq5` (copy v2.5, magic 24260000), biên dịch 0 lỗi / 0 cảnh báo.
- Thay đổi 1: input `InpKeoM15 = false` → tắt luật KÉO ở M15 (vòng 1a: KÉO M15 = 16 lệnh, −6,4R).
- Thay đổi 2: `InpAG_ATRNhan = 0` = tắt lọc ATR-cao của áo giáp (vẫn giữ lọc spread). Đặt lại 2.0 để so sánh.
- Còn lại giữ nguyên mặc định v2.5 (áo giáp bật, rủi ro 1%).
**Việc tiếp (cần MCP MT5 — phiên mở ở `TongTuLenh/` chưa có công cụ mt5):** trên tập huấn luyện 01/01/2025→24/07/2026, vốn 500:
  (a) v2.4 2% vs v2.6 tắt áo giáp + rủi ro 2% (chỉ đo thay đổi 1);
  (b) v2.5 mặc định vs v2.6 mặc định (đo thêm thay đổi 2).
  Giữ thay đổi khi PF tăng, sụt equity không tăng, số lệnh không giảm >40%.

## Vòng 2 — 26/10/2026: nghiên cứu luật M5 & Dow (Python, dữ liệu Binance) → chi tiết `01-Trading/TOI-UU/NGHIEN-CUU-M5-DOW.md`
- M5 "3 nến tăng → mua, ăn 2R": thắng 33% = may rủi, có phí −0,10R/lệnh → BỎ.
- Bán phá cấu trúc H1: HL đẹp nhưng KT âm (phụ thuộc giai đoạn thị trường giảm) → BỎ.
- **Tốt nhất: tích luỹ H1 (24–48 nến, biên độ ≤3%) → phá vùng cùng chiều D1/SMA50 → SL giữa vùng, kéo SL theo 12 nến.** HL +0,21 đến +0,42R/lệnh, KT +0,15 đến +0,31R/lệnh, chịu được phí $50. Lãi dồn vào vài con sóng lớn; Q4/2026 âm nhẹ.
- Việc tiếp: code thành EA v2.7 → backtest MT5 dữ liệu Exness → demo 4–8 tuần. Vòng 1b (v2.6) vẫn chờ chạy backtest ở phiên có MCP mt5.

## Vòng 2b — 26/10/2026: luật tích luỹ–phá vùng có hơn v2.4 không? → KHÔNG, không code v2.7
Cùng giai đoạn 01/01→25/10/2026, vốn 500, rủi ro mỗi lệnh tính theo số dư (v2.4 = MT5 vòng 0d; luật mới = mô phỏng Python, dữ liệu Binance):
| Bản | Lệnh | Vốn cuối | PF | Sụt số dư | Lãi/sụt |
|---|---|---|---|---|---|
| **v2.4 rủi ro 2%** | 385 | ~3126 (+525%) | 1,62 | 35,6% (equity 46,5%) | **14,7** |
| **v2.4 rủi ro 1%** | 387 | ~2107 (+321%) | 1,67 | 21,0% (equity 38,0%) | **15,3** |
| Tích luỹ 24 nến, 2% | 95 | 979 (+96%) | 1,67 | 15,7% | 6,1 |
| Tích luỹ 48 nến, 2% | 37 | 731 (+46%) | 2,16 | 9,4% | 4,9 |
| Tích luỹ 48 nến, 1% | 37 | 615 (+23%) | 2,29 | 4,8% | 4,8 |
Kết luận: luật mới sụt vốn ít hơn, PF ngang hoặc cao hơn, nhưng lãi chỉ bằng 1/5 → 1/10 và **lãi trên mỗi % sụt vốn kém v2.4 2–3 lần**. Ngay cả v2.4 rủi ro 1% (+321%, sụt 21%) cũng hơn hẳn luật mới rủi ro 2% (+96%, sụt 15,7%).
→ Không tối ưu hơn → **KHÔNG code v2.7** (theo chỉ đạo anh 26/10). Hướng tối ưu tiếp tục là v2.4/v2.6: giảm sụt equity (nhiều lệnh mở cùng lúc) mà không cắt lệnh thắng.

## Vòng 2c — 26/10/2026: vì sao v2.4 không BÁN ở 2 nhịp 87k→80k và 85k→79,5k? (Python, script v24sell.py / sellvar.py)
**Nguyên nhân:** v2.4 chỉ BÁN khi đủ cả 6 điều kiện:
1. EMA10 cắt xuống EMA20;
2. giá nằm dưới cả 2 EMA;
3. RSI ≤ 45;
4. không nhiễu (EMA cắt nhau ≤ 2 lần trong 20 nến trước);
5. **nến tuần đóng dưới SMA50 tuần**;
6. **mọi khung trên tới D1 đều EMA10 < EMA20** và đang ở sóng C.

Cả tháng 9–10 nến tuần vẫn TRÊN SMA50 tuần → **mọi tín hiệu bán đều bị chặn bởi điều kiện tuần**. D1 chỉ quay xuống từ ~15/10. Đây là thiết kế "chỉ bán trong thị trường gấu cấp tuần", không phải lỗi.

**Thử nới điều kiện bán (M15+H1+H4, SL đỉnh swing 2 nến, 3R hoà vốn, kéo theo đỉnh swing 10 nến, phí $16):**
| Biến thể | HL lệnh | HL TB | HL tổng | HL sụt | KT lệnh | KT TB | Tháng 10 |
|---|---|---|---|---|---|---|---|
| v2.4 gốc | 48 | +1,05R | +50R | 9,3R | 3 | −1,04R | không lệnh |
| Bỏ điều kiện tuần | 81 | +1,09R | +88R | 9,3R | 6 | −0,87R | 3 lệnh, đều thua/hoà |
| Bỏ tuần + bỏ sóng C | 107 | +0,90R | +96R | 7,1R | 9 | −0,71R | 5 lệnh, đều thua/hoà |
| Bỏ tuần + bỏ "khung trên đều giảm" | 305 | +0,19R | +58R | 14,8R | 57 | −0,56R | ăn 06/10 +4,3R nhưng 15 lệnh thua |
| Bỏ tuần + sóng C + khung trên | 362 | +0,17R | +60R | 20,7R | 61 | −0,46R | ăn 02/10 +3,3R, 21/10 +4,9R, 12 lệnh thua |

**Kết luận:**
- Không có luật bán nào bắt được 2 nhịp này mà vẫn có lãi. Muốn bắt được (bỏ yêu cầu khung trên đều giảm) thì phải chịu ~12–15 lệnh thua trong tháng 10, cả 3 tháng kiểm tra âm 28–32R.
- Hai nhịp này là **điều chỉnh trong xu hướng tăng cấp tuần** — giá giật hai chiều nhiều nên SL trên M15/H1 bị quét liên tục.
- Ứng viên duy nhất đáng xem: **"bỏ điều kiện tuần"**. Trên tập huấn luyện: +38R, cùng mức sụt, TB/lệnh không giảm. Nhưng 3 tháng kiểm tra tệ hơn (6 lệnh đều thua) → **CHƯA xác nhận tối ưu hơn → không code** (theo chỉ đạo anh). Chỉ xét lại nếu backtest MT5 cho kết quả rõ.

## Vòng 1c — 26/10/2026: backtest v2.6 trên TẬP HUẤN LUYỆN (01/01/2025→24/07/2026), vốn 500, BTCUSDm H1, M1 OHLC
| # | Cấu hình | Lãi | PF | Lệnh (thắng) | Sụt equity | Sụt số dư | Số dư thấp nhất | Thua LT | Recovery |
|---|---|---|---|---|---|---|---|---|---|
| a1 | v2.4 gốc (2%) | −8,34 | 0,997 | 525 (153) | 62,0% | 58,3% | 230,30 | 23 | −0,02 |
| a3 | v2.6 tắt áo giáp, 2%, BẬT kéo M15 (đối chứng) | −8,34 | 0,997 | 525 (153) | 62,0% | 58,3% | 230,30 | 23 | −0,02 |
| **a2** | **v2.6 tắt áo giáp, 2%, TẮT kéo M15** | **+512,69** | **1,119** | 608 (192) | **56,0%** | 38,1% | 340,25 | 26 | 0,92 |
| b1 | v2.5 mặc định (1%, áo giáp, lọc ATR 2,0) | −75,15 | 0,704 | 69 (19) | 23,8% | 21,5% | 424,85 | 9 | −0,57 |
| b3 | v2.6 mặc định nhưng BẬT lại lọc ATR 2,0 | −75,32 | 0,704 | 71 (19) | 24,9% | 22,0% | 424,68 | 12 | −0,54 |
| **b2** | **v2.6 mặc định (tắt kéo M15 + tắt lọc ATR)** | **+355,77** | **1,265** | 329 (101) | 26,4% | 24,0% | 453,79 | 12 | **1,83** |

Phát hiện quan trọng:
- **Trên 19 tháng huấn luyện, cả v2.4 (≈ hoà, sụt equity 62%) lẫn v2.5 (lỗ, PF 0,70) đều KHÔNG có lãi.** Lãi lớn ở vòng 0b/0d chỉ đến từ 2026.
- a3 = a1 y hệt → v2.6 khi tắt áo giáp + bật kéo M15 chạy đúng như v2.4, so sánh tách biến chuẩn.
- **Thay đổi 1 (tắt KÉO M15):** −8 → +513, PF 0,997 → 1,119, sụt equity 62 → 56%, lệnh +16% → đạt cả 3 tiêu chí → **GIỮ**. Trong áo giáp gần như không tác dụng (b1 ≈ b3) vì lọc ATR đã chặn phần lớn lệnh.
- **Thay đổi 2 (tắt lọc ATR-cao):** b3 → b2: lệnh 71 → 329, PF 0,70 → 1,27, lãi −75 → +356, recovery −0,54 → 1,83; nhưng sụt equity 24,9 → 26,4% (+1,5 điểm) → **trượt nhẹ tiêu chí "sụt không tăng"**. Đề xuất vẫn giữ (lợi ích vượt xa), chờ anh duyệt.
- Kỹ thuật: tester MT5 NHỚ inputs lần chạy trước nếu không truyền inputs_path → luôn truyền file .set ghi rõ. File v2_6.ex5 bản 21:12 MT5 không nhận ("must reference a compiled program") → biên dịch lại qua MCP MetaEditor 21:54 thì nhận.
**Việc tiếp:** chưa chạy tập kiểm tra (đúng quy trình: sau 3–4 vòng). Hướng vòng sau: giảm sụt equity 56% của bản không áo giáp (nhiều lệnh mở cùng lúc), hoặc nới áo giáp v2.6 (MaxLenh, rủi ro) để lấy thêm lãi trong giới hạn sụt ~25%.
**Quyết định anh (26/10):** chỉ giữ thay đổi 1 (tắt KÉO M15), **bật lại lọc ATR-cao 2,0**. Đã sửa mặc định `InpAG_ATRNhan = 2.0` trong v2.6, biên dịch lại 0 lỗi / 0 cảnh báo (22:32), MT5 đọc đúng mặc định. → v2.6 mặc định giờ = dòng b3 (−75,32, PF 0,70, 71 lệnh, sụt equity 24,9%); bản 2% tắt áo giáp = dòng a2.

## 28/10/2026 — v2.6 thêm nhật ký giao dịch + tổng kết tháng (không đổi luật vào/ra lệnh)
- Đổi tên file này từ NHAT-KY-VONG.md → OPTIMIZATION-LOG.md (anh yêu cầu).
- Input mới: `InpNhatKy` (mặc định bật), `InpNhatKyAo` (ghi cả lệnh theo dõi khi Algo Trading tắt), `InpTongKetNgay` (viết ngay tổng kết tạm tính tháng này khi gắn EA).
- File (thư mục chung MT5, wine): `drive_c/users/user/AppData/Roaming/MetaQuotes/Terminal/Common/Files/ThinhTrading/`
  - `NhatKy_BTCUSDm_24260000.csv`: mỗi lệnh đóng 1 dòng: loại (THAT/THEO DOI), khung, chiều, giờ/giá vào, SL ban đầu, lot, 1R USD, giờ/giá ra, R, lãi lỗ, phí, số dư, giờ giữ, lý do ra (chạm SL ban đầu / hoà vốn / SL kéo chốt lãi / bot đóng / anh đóng tay).
  - `TongKet_BTCUSDm_24260000.txt`: sang tháng mới tự viết tổng kết tháng trước (số lệnh, tỉ lệ thắng, tổng R, lãi lỗ USD và %, PF, thua liên tiếp, theo khung) + báo điện thoại. MT5 tắt qua lúc sang tháng thì lần mở sau vẫn tổng kết bù.
  - Backtest ghi file `TEST_...` riêng, mỗi lần chạy xoá file cũ.
- Kiểm tra (backtest 25/07→25/10/2026, vốn 500, v2.6 mặc định): +205,70, PF 2,09, 60 lệnh, sụt equity 18,9%. CSV 60 dòng, tổng lãi lỗ = +205,70 khớp báo cáo; tổng 4 tháng 35,00 + 128,03 + 22,24 + 20,43 = 205,70 ✓.

## Vòng 4 — 28/10/2026: M5 vào theo FVG/OB, lọc trùng FVG H1/H4, tách giằng co (Python, script `scripts/fvg.py`, dữ liệu M5 Binance)
Luật (anh gợi ý): M5 tạo FVG (nến 3 cách nến 1, gap ≥ 0,3 ATR M5) ngay trong vùng FVG H1/H4 cùng chiều còn hiệu lực → vào lệnh.
- Kiểu FVG: vào luôn giá mở nến sau; SL dưới/trên đáy/đỉnh mẫu 4 nến (+0,1 ATR).
- Kiểu OB: chờ giá hồi về nến ngược chiều cuối cùng trước cú bật (tối đa 2h); SL dưới/trên OB.
- TP 1R / 2R / 3R, giữ tối đa 1 ngày. Phí $18/lệnh, SL tối thiểu $60, chạm cả SL lẫn TP trong cùng nến = tính thua.
- "Giằng co" = ADX D1 < 20.
| Biến thể (2R) | HL lệnh | HL TB (có phí) | HL TB (không phí) | KT lệnh | KT TB (có phí) |
|---|---|---|---|---|---|
| FVG M5, không lọc | 3181 | −0,016R | +0,047R | 510 | −0,099R |
| FVG M5 trùng FVG H1 hoặc H4 | 1645 | −0,059R | +0,017R | 324 | −0,106R |
| FVG M5 trùng cả H1 và H4 | 434 | −0,052R | +0,021R | 86 | −0,237R |
| OB M5 trùng H1 hoặc H4 | 1546 | −0,182R | −0,034R | 252 | −0,076R |
| FVG trùng H1/H4, chỉ lúc giằng co | 168 | −0,120R | −0,027R | 31 | +0,536R |
| OB trùng H1/H4, chỉ lúc giằng co | 134 | −0,406R | −0,251R | 13 | +0,626R |
(TP 1R và 3R: tất cả biến thể HL đều âm khi có phí.)
Kết luận:
- **Không có biến thể nào có lãi trên tập huấn luyện sau phí.** FVG M5 tự thân chỉ có lợi thế rất mỏng (+0,02 đến +0,05R/lệnh trước phí); phí ~0,06–0,1R/lệnh ăn hết.
- **Trùng FVG khung lớn KHÔNG làm tốt hơn**: lọc H1/H4 bớt lệnh nhưng TB/lệnh không tăng (thậm chí giảm).
- OB (chờ hồi về) kém hơn FVG vào luôn.
- Giằng co: tập kiểm tra đẹp (31 lệnh, +0,54R) nhưng tập huấn luyện âm, số lệnh quá ít → may rủi, chưa dùng được.
- Lưu ý: đây là một cách định nghĩa OB/FVG máy móc; trader đánh tay còn đọc bối cảnh nên kết quả có thể khác. → Không code vào bot.

## Vòng 4b — 28/10/2026: vào lệnh TRỰC TIẾP ở FVG H1/H4 khi giá hồi về lần đầu (script `scripts/fvg_htf.py`)
Luật: FVG H1/H4 (gap ≥ 0,3 hoặc 0,6 ATR khung đó); chờ giá hồi về lần đầu (tối đa 72 nến H1 / 30 nến H4; đóng cửa vượt mép xa trước đó = vùng hỏng);
vào ở mép gần ("mep") hoặc giữa vùng ("CE"); SL vượt mép xa 0,1 ATR; TP 1,5/2/3R; giữ tối đa 72 nến H1 / 30 nến H4. Phí $18, cùng nến chạm SL và TP = thua.
| Biến thể | HL lệnh | HL TB | KT lệnh | KT TB |
|---|---|---|---|---|
| H1 gap≥0,3 mép 2R | 575 | +0,055R | 106 | +0,012R |
| H1 gap≥0,3 mép 3R | 527 | +0,059R | 103 | +0,111R |
| H1 gap≥0,6 mép 2R | 344 | +0,082R | 57 | −0,045R |
| H1 gap≥0,6 CE 3R | 335 | +0,185R | 58 | −0,250R |
| H4 gap≥0,3 mép 2R | 200 | +0,190R | 28 | −0,481R |
| H4 gap≥0,6 CE 2R | 109 | +0,152R | 18 | −0,154R |
| H1 CE 2R, chỉ lúc giằng co (ADX D1<20) | 52 | −0,302R | 18 | +0,218R |
| H4 CE 2R, chỉ lúc giằng co | 26 | −0,476R | 5 | +0,694R |
Kết luận:
- **Khung lớn tốt hơn M5 rõ rệt**: phần lớn biến thể H1/H4 có lãi trên tập huấn luyện SAU phí (+0,02 đến +0,19R/lệnh), vì SL rộng nên phí chỉ ~0,02–0,05R.
- **Nhưng tập kiểm tra 3 tháng phần lớn âm**; chỉ "H1 vào ở mép" giữ được dương nhẹ (+0,01 / +0,11R). Lợi thế có, nhưng mỏng (~+0,05R/lệnh) và chưa chắc chắn.
- **Lọc "giằng co" làm tệ đi** trên tập huấn luyện (−0,3 đến −0,5R) → giả thuyết "giằng co mới là lúc kiếm" KHÔNG được số liệu ủng hộ với FVG.
- H4 đẹp trên HL nhưng KT rất xấu và ít lệnh → không tin.
- Ứng viên duy nhất đáng xét tiếp: **FVG H1, vào ở mép, 2–3R**. Muốn dùng phải backtest MT5 dữ liệu Exness trước; chưa code vào bot.

## Vòng 3 — 28/10/2026: từng lớp áo giáp + M5 chốt lời nhanh (MT5, 6 tháng 24/01→24/07/2026, vốn 500, v2.6 tắt KÉO M15, rủi ro 2%)
Anh chốt mặc định v2.6 = tắt áo giáp + rủi ro 2% (28/10). Rút còn 6 tháng cho nhanh (anh yêu cầu). Giai đoạn này BTC 88k → 64k (−27%), có 2 đợt sập mạnh (cuối 1–đầu 2, đầu 6) và 2 đợt tăng (giữa 3, 4–5).
| # | Cấu hình | Lãi | PF | Lệnh | Sụt equity | Sụt số dư | Thua LT |
|---|---|---|---|---|---|---|---|
| E0 | không áo giáp (gốc) | +334,79 | 1,21 | 219 | 46,2% | 41,6% | 7 |
| E1 | + tối đa 3 lệnh | +282,33 | 1,19 | 204 | 42,4% | 37,9% | 7 |
| E2 | + rủi ro mở ≤ 4% | +350,66 | 1,35 | 136 | 37,3% | 28,1% | 11 |
| **E3** | **+ lỗ ngày 3% → đóng hết, nghỉ** | **+830,68** | **1,50** | 208 | 43,0% | 35,3% | 8 |
| E4 | + lỗ tuần 6% | +386,60 | 1,31 | 187 | 42,2% | 35,7% | 15 |
| **E5** | **+ thua 3 lệnh → nghỉ 24h** | +497,48 | 1,37 | 166 | **32,1%** | **17,9%** | **4** |
| E6 | + lọc ATR 2.0 | +333,52 | 1,21 | 216 | 47,5% | 43,1% | 8 |
| E7 | + lọc spread | = E0 (tester spread cố định → không tác dụng) | | | | | |
| E8 | không áo giáp, rủi ro 1% | +391,54 | 1,35 | 219 | 42,8% | 31,9% | 7 |
M5 (không áo giáp, 2%; biên dịch bản mới có `InpM5TP`, 0 lỗi):
| # | Cấu hình | Lãi | PF | Lệnh (thắng) | Sụt equity | Sụt số dư |
|---|---|---|---|---|---|---|
| G0 | M5 kéo SL như cũ (= E0) | +334,79 | 1,21 | 219 (75) | 46,2% | 41,6% |
| G1 | tắt hẳn M5 | +648,25 | 1,47 | 181 (64) | 39,4% | 28,5% |
| **G5** | **M5 chốt cố định 0,5R** | **+902,75** | **1,57** | 219 (93) | **37,5%** | 28,2% |
| G2 | M5 chốt 1R | +699,50 | 1,43 | 218 (84) | 39,5% | 30,9% |
| G3 | M5 chốt 1,5R | +783,02 | 1,44 | 219 (79) | 37,5% | 29,2% |
| G4 | M5 chốt 2R | +812,25 | 1,44 | 219 (78) | 37,5% | 27,0% |
Kết luận (chỉ trên 6 tháng, CHƯA kiểm tra giai đoạn khác):
- **M5 chốt lời nhanh tốt hơn hẳn kéo SL**: mọi mức TP đều hơn gấp đôi lãi gốc, sụt equity 46 → 37–40%. 0,5R tốt nhất, nhưng 1–2R cũng tốt → kết quả ổn định theo tham số (dấu hiệu tốt). Khác kết quả Python Vòng 2 vì tín hiệu M5 của bot đã lọc cùng chiều khung trên.
- **Lớp áo giáp đáng giữ:** lỗ ngày 3% (lãi ×2,5), thua 3 nghỉ 24h (sụt số dư 41,6 → 17,9%, thua LT 7 → 4), rủi ro mở ≤4% (sụt số dư → 28%).
- **Lớp nên bỏ:** tối đa 3 lệnh (giảm lãi), lọc ATR (không tác dụng), lọc spread (không đo được trong tester).
- Rủi ro 1% lãi HƠN 2% ở giai đoạn này → 2% đang quá tay với vốn 500.
- CẢNH BÁO khớp quá: tất cả chọn trên cùng 6 tháng → phải kiểm tra tổ hợp (M5 TP + lỗ ngày 3% + thua 3 nghỉ 24h) trên 25/07→25/10/2026 và 2025 trước khi tin.

## Vòng 5 — 29/10/2026: kiểm tra trên giai đoạn GẦN ĐÂY (anh: thị trường gần đây mới là thước đo, luật cũ chỉ tham khảo)
Vốn 500, rủi ro 2%, v2.6 tắt KÉO M15. "Gốc" = không áo giáp, M5 kéo SL. "Tổ hợp" = M5 chốt 0,5R + lỗ ngày 3% + thua 3 nghỉ 24h.
| Giai đoạn | Cấu hình | Lãi | PF | Lệnh | Sụt equity | Sụt số dư | Số dư thấp nhất | Thua LT |
|---|---|---|---|---|---|---|---|---|
| 3 tháng 25/07→25/10 | Gốc | +1579,66 | 2,16 | 118 | 40,3% | 29,8% | 491 | 21 |
| 3 tháng 25/07→25/10 | Tổ hợp | +659,70 | 2,17 | 91 | 28,6% | 7,4% | 491 | 4 |
| 6 tháng 25/04→25/10 | Gốc | +1676,82 | 1,79 | 224 | 44,2% | 33,1% | 378 | 22 |
| 6 tháng 25/04→25/10 | Tổ hợp | +763,32 | 1,69 | 172 | 39,8% | 30,1% | 500 | 4 |
| 6 tháng 25/04→25/10 | **Chỉ M5 chốt 0,5R** | **+1863,55** | **1,79** | 227 | **36,6%** | 29,4% | **489** | **9** |
| 6 tháng 25/04→25/10 | Chỉ áo giáp (lỗ ngày 3% + thua 3 nghỉ 24h) | +77,18 | 1,09 | 144 | 40,3% | 33,4% | 431 | 8 |
(2025 chưa chạy: MT5 bị tắt giữa chừng, anh nói luật cũ chỉ tham khảo → bỏ.)

**Vì sao bot thắng (nhật ký 223 lệnh, 6 tháng gần đây, bản gốc):**
1. **Thắng nhờ vài con sóng lớn:** 10% lệnh tốt nhất (22 lệnh) mang về +219R; 90% còn lại cộng lại −65R. Lệnh "SL kéo – chốt lãi" trung bình +3,95R; 117 lệnh chạm SL ban đầu = −117R. Đây là bản chất đánh theo xu hướng: thua nhiều lệnh nhỏ, sống nhờ vài lệnh gồng dài (19–20/08: H1 +32,6R, M15 +17,1R, H4 +15,1R; 31/05–01/06: SELL +19,8R, +15,9R).
2. **Tuần TĂNG là mỏ vàng:** 73 lệnh +107R (TB +1,47R). Tuần giằng co: 116 lệnh chỉ +27R (TB +0,24R). Tuần GIẢM: bot chủ yếu mua nên kém (+0,57R TB nhưng −25 USD).
3. **M15 là động cơ chính:** +90,6R, có lãi ở mọi kiểu thị trường (kể cả giằng co +38R). H1/H4 lỗ khi giằng co, ăn đậm khi có xu hướng.
4. **M5 kéo SL lỗ khi giằng co (−3R), ăn khi tăng (+22,8R).** Chốt 0,5R: M5 thắng 74%, tổng R ít hơn (+6R) NHƯNG **vốn đi đều, chuỗi thua 22 → 9** → các khung khác vào lệnh với số dư cao hơn → M15 kiếm +1356 USD so với +1091 USD cùng số R. Lãi USD tăng nhờ "lãi kép êm", không phải nhờ M5 tự kiếm nhiều.
5. **Áo giáp (nghỉ sau chuỗi thua / lỗ ngày) giết lãi ở giai đoạn gần đây** (+1677 → +77): sóng lớn thường bắt đầu ngay sau một chuỗi thua lúc giằng co; bot đang nghỉ thì lỡ mất con sóng. Ở 24/01→24/07 lại giúp → kết quả đảo chiều giữa 2 giai đoạn = không bền → BỎ.

**Luật chốt (29/10):** v2.6 mặc định = rủi ro 2%, áo giáp TẮT, tắt KÉO M15, **M5 chốt cố định 0,5R** (`InpM5TP = 0.5`), các khung khác kéo SL như cũ. Biên dịch 0 lỗi.
M5 chốt 0,5R thắng ở cả 2 giai đoạn: 24/01→24/07 (+335 → +903) và 25/04→25/10 (+1677 → +1864), sụt equity giảm ở cả hai.
Còn yếu: sụt equity vẫn ~37%; bot gần như chỉ MUA nên tuần giảm kém; H1/H4 lỗ khi giằng co (ứng viên vòng sau: tắt H1/H4 khi giằng co).

## Vòng 6 — 29/10/2026: MỐC PHE BÁN (anh: "giảm thì phải đánh giảm, bot đang 1 chiều")
Code v2.6: thêm input `InpMocBan` (0 gốc tuần<SMA50+sóng C | 1 D1 EMA10<EMA20 & giá dưới 2 đường | 2 D1 dưới EMA99 | 3 tuần EMA10<EMA20 | 4 RSI 3D<50), `InpBanM5`, `InpBanChuoi`, `InpChanMuaGiam`. Mặc định giữ luật cũ. Biên dịch 0 lỗi.
Mô phỏng Python gần đúng (`scripts/ban_moc.py`, Binance M5, phí $16, M5 chốt 0,5R, khung khác 3R hoà vốn + kéo SL swing 10; tính theo R, không lãi kép):
| Mốc | 24/01→24/07/2026 (giảm 27%) | 25/04→25/10/2026 (gần nhất) | 06/2025→10/2026 |
|---|---|---|---|
| 0 gốc (tuần<SMA50 + sóng C) | +38,8R, sụt 20,4R (bán 33 lệnh) | +52,7R, sụt 22,6R (bán 18) | +53,4R, sụt 29,9R |
| 1 D1 EMA10<20 & giá dưới, bán cả M5 | +59,2R, sụt 22,8R (bán 131) | +56,4R | +63,0R |
| 2 D1 dưới EMA99 | +48,8R | +50,2R | +48,0R |
| 3 tuần EMA10<20 | +59,2R | +60,6R | +67,2R |
| 4 RSI 3D<50 | +46,3R | +47,7R | +50,9R |
| **1 + chặn MUA khi phe giảm** | **+66,9R**, sụt 25,3R | **+68,1R**, sụt 23,1R | **+95,9R**, sụt 29,3R |
| 3 + chặn MUA khi phe giảm | +62,5R, **sụt 13,6R** | +58,0R, sụt 20,6R | +87,9R, **sụt 20,6R** |
| 4 + chặn MUA khi phe giảm | +46,8R | +57,2R | +70,7R, sụt 19,3R |
Kết luận (Python, chờ MT5 xác nhận):
- Lệnh BÁN có lãi ở mọi mốc và mọi giai đoạn (+0,2 đến +0,8R/lệnh, thắng 53–65%) → **bot đánh giảm được**, luật cũ chỉ bán quá ít.
- **Chặn MUA khi đang phe giảm** tăng lãi rõ: lệnh MUA trong phe giảm gần như toàn thua (MUA TB −0,02R → +0,11~0,15R khi chặn).
- Tốt nhất về lãi, ổn định cả 3 giai đoạn: **mốc 1 (D1 EMA10<EMA20 + giá dưới 2 đường) + chặn MUA**. Tốt nhất về sụt vốn: mốc 3 (tuần EMA10<EMA20) + chặn MUA.
- MT5 đang chạy B0–B6 (6 tháng gần nhất + 24/01→24/07) để xác nhận bằng dữ liệu Exness.
### Vòng 6 — kết quả MT5 (Exness, vốn 500, rủi ro 2%, M5 chốt 0,5R, không áo giáp)
| # | Mốc phe bán | 25/04→25/10 (gần nhất): Lãi / PF / sụt eq | 24/01→24/07 (giảm): Lãi / PF / sụt eq / sụt số dư | Cộng 2 giai đoạn |
|---|---|---|---|---|
| B0 | gốc (tuần<SMA50 + sóng C) | +1863,55 / 1,79 / 36,6% | +903,01 / 1,57 / 37,5% / 28,2% | 2767 |
| B1 | D1 EMA10<20, bán M5 | +2453,23 / 1,83 / 35,6% | +383,77 / 1,26 / 32,2% / 28,6% | 2837 |
| B2 | D1 dưới EMA99, bán M5 | +1445,62 / 1,71 / 36,1% | +337,66 / 1,23 / 34,6% | 1783 |
| B3 | tuần EMA10<20, bán M5 | **+2513,79** / 1,87 / 35,6% | +383,77 / 1,26 / 32,2% | 2898 |
| B4 | RSI 3D<50, bán M5 | +1364,51 / 1,70 / 36,4% | +183,81 / 1,14 / 39,2% | 1548 |
| **B5** | **D1 EMA10<20 + chặn MUA** | **+2161,67 / 1,90 / 34,8%** | **+796,38 / 1,57 / 35,1% / 29,0%** | **2958** |
| B6 | D1 dưới EMA99 + chặn MUA | +644,26 / 1,62 / 33,2% | +755,11 / 2,00 / 35,9% / 19,3% | 1399 |
| B7 | tuần EMA10<20 + chặn MUA | +801,39 / 2,06 / 32,5% (94 lệnh) | +901,17 / **2,64** / 33,5% / **14,9%** (91 lệnh) | 1703 |
Phân tích nhật ký giai đoạn giảm (24/01→24/07):
- Luật cũ bán ÍT nhưng CHẤT: 33 lệnh SELL TB +2,04R (sóng C ở H1/H4 ăn đậm). Mốc mới bán nhiều hơn (82 lệnh) nhưng TB chỉ +0,70R và **chiếm chỗ** của các lệnh bán sóng C lớn (mỗi khung mỗi chiều chỉ 1 lệnh): H1 SELL +19,8R → +9,4R, H4 SELL +6,5R → không có lệnh.
- **BÁN M5 gần như vô ích**: 47 lệnh, +1,0R, −7,5 USD → nên tắt.
- **Chặn MUA khi phe giảm có tác dụng thật**: MUA trong giai đoạn giảm từ −4,7R (−76 USD) → +3,1R (+55 USD).
Kết luận: MT5 khớp hướng với Python ở giai đoạn gần đây (B1/B3/B5 hơn gốc +16–35%), nhưng ở giai đoạn giảm các mốc mới KHÔNG hơn luật cũ vì làm loãng lệnh bán chất lượng. **B5 (D1 EMA10<20 + chặn MUA) cân bằng nhất**: cộng 2 giai đoạn cao nhất (2958 so với 2767), PF và sụt vốn tốt hơn gốc ở giai đoạn gần đây, chỉ kém gốc 12% ở giai đoạn giảm. B7 an toàn nhất (sụt số dư 14,9%, PF 2,64) nhưng ít lệnh, lãi thấp ở giai đoạn gần đây.
CHƯA đổi mặc định (vẫn InpMocBan=0). Vòng sau: B5 + TẮT bán M5 + giữ thêm lệnh bán sóng C của luật cũ (không để lệnh mới chiếm chỗ).

## Vòng 6b — 30/10/2026: giữ chỗ riêng cho lệnh BÁN sóng C của luật cũ (`InpBanGiuC`, slot magic +5), tắt bán M5
| # | Cấu hình (đều chặn MUA khi phe giảm, không bán M5) | 25/04→25/10: Lãi / PF / sụt eq / sụt số dư | 24/01→24/07: Lãi / PF / sụt eq / sụt số dư | Cộng |
|---|---|---|---|---|
| B0 | (nhắc lại) luật cũ | +1863,55 / 1,79 / 36,6% / 29,4% | +903,01 / 1,57 / 37,5% / 28,2% | 2767 |
| B5 | (nhắc lại) D1 EMA10<20 + chặn MUA, có bán M5 | +2161,67 / 1,90 / 34,8% / 28,5% | +796,38 / 1,57 / 35,1% / 29,0% | 2958 |
| **C1** | **D1 EMA10<20 + chặn MUA + giữ chỗ sóng C** | **+2188,60 / 1,89 / 34,7% / 28,3%** | **+1135,29 / 1,82 / 42,6% / 27,5%** | **3324** |
| C2 | D1 EMA10<20 + chặn MUA (không giữ chỗ) | +2163,68 / 1,92 / 34,9% / 28,6% | +835,17 / 1,69 / 34,7% / 28,6% | 2999 |
| C3 | tuần EMA10<20 + chặn MUA + giữ chỗ sóng C | +995,05 / 2,24 / 33,8% (83 lệnh) | +1124,60 / 3,39 / 39,6% / 16,0% (56 lệnh) | 2120 |
Kết luận:
- **C1 hơn luật cũ ở CẢ 2 giai đoạn**: +17% (gần nhất) và +26% (giảm), PF cao hơn ở cả hai, sụt số dư tương đương. Giữ chỗ cho sóng C lấy lại phần bán chất lượng mà B5 đánh mất (796 → 1135).
- Tắt bán M5: lợi nhỏ (B5 → C2: +2 / +39 USD).
- Mặt xấu: sụt equity giai đoạn giảm 37,5% → 42,6% (nhiều lệnh bán mở cùng lúc khi giá giật ngược).
**Chốt mặc định v2.6 (30/10):** `InpMocBan=1`, `InpChanMuaGiam=true`, `InpBanGiuC=true`, `InpBanM5=false` (+ rủi ro 2%, áo giáp tắt, tắt KÉO M15, M5 chốt 0,5R). Biên dịch 0 lỗi. Chưa gắn lên chart.

## CHỐT PHIÊN BẢN — 30/10/2026 18:55 (anh sắp hết usage)
**Bản chốt:** `01-Trading/ThinhTrading/BAN-CHOT-v2.6_30-10-2026/` (mq5 + ex5 chỉ đọc, SHA256.txt). Giống hệt `ThinhTrading/ThinhTrading_EMA_EA_v2_6.mq5` và bản trong MT5.
Mặc định v2.6: rủi ro 2% | áo giáp TẮT | tắt KÉO M15 | M5 chốt 0,5R | mốc phe bán = D1 EMA10<EMA20 & giá dưới 2 đường (`InpMocBan=1`) → được bán M15/H1/H4 + chặn MUA | lệnh bán sóng C luật cũ có chỗ riêng (`InpBanGiuC`) | không bán M5 | nhật ký CSV + tổng kết tháng. Magic 24260000.
Kết quả (vốn 500): 25/04→25/10/2026 +2188,60 (PF 1,89, sụt eq 34,7%); 24/01→24/07/2026 +1135,29 (PF 1,82, sụt eq 42,6%).
**Đã lưu để làm tiếp:** script MT5 `TOI-UU/scripts/mt5/` (cần `export MT5_KEY=<Bearer key>`, xem ~/.claude.json), script Python `TOI-UU/scripts/`, dữ liệu `TOI-UU/data/` (m5.csv Binance 01/2025→26/10/2026, D1 json, nhật ký lệnh các backtest trong `data/nhatky_backtest/`).
**VIỆC DỞ:** test các đợt sập mạnh — script `scripts/mt5/sap.sh` (chưa chạy được: MCP MT5 bị treo lúc 18:06, cần tắt/mở lại MT5). 4 đợt: S1 15/01→15/04/2025, S2 01/10→25/11/2025 (126k→88,6k), S3 10/01→12/02/2026 (98k→60k, −39%/23 ngày), S4 01/05→10/06/2026 (82,9k→59k). 3 bản mỗi đợt: luật cũ / C1 / C1 + bán M5. Sau đó phân tích M5 trong đợt giảm bằng `scripts/phantich_nk.py`.
Lưu ý: với C1, khi D1 sang phe giảm thì M5 gần như đứng yên (mua bị chặn, bán M5 tắt).

## Vòng 7 — 30/10/2026: test riêng 4 ĐỢT SẬP MẠNH (MT5, vốn 500, rủi ro 2%, M5 chốt 0,5R)
| Đợt | Luật cũ | C1 (bản chốt) | C1 + bán M5 |
|---|---|---|---|
| S1 15/01→15/04/2025 (≈ −32%, giảm giằng co) | −152,57 (PF 0,52, sụt eq 34,8%) | **−201,98** (PF 0,39, sụt eq 44,0%) | −177,11 |
| S2 01/10→25/11/2025 (126k→88,6k) | +0,69 (PF 1,00) | **+209,73** (PF 1,91, sụt eq 17,8%) | +189,05 |
| S3 10/01→12/02/2026 (98k→60k, −39%) | +9,01 (PF 1,03, thua LT 24) | **+154,59** (PF 1,82, thua LT 13) | +135,96 |
| S4 01/05→10/06/2026 (82,9k→59k) | +340,08 (PF 2,36) | **+649,97** (PF 4,73) | +689,62 |
Theo khung (USD, C1): lệnh BÁN M15 kiếm chính ở S2–S4 (+28 / +187 / +428); BÁN H1 +63 (S2), +97 (S4). MUA trong đợt sập vẫn lỗ (M15/H1) nhưng ít hơn luật cũ nhờ chặn mua (S3: M15 MUA −119 → −13).
**S1 là điểm yếu:** đầu 2025 giá giảm kiểu giằng co, hồi mạnh liên tục → lệnh BÁN M15 bị quét (18 lệnh −108 USD), C1 lỗ nhiều hơn luật cũ.
**Bán M5 trong đợt sập:** +25 / −21 / −19 / +40 USD → cộng ≈ +25, gần như hoà, thêm 12–27 lệnh mỗi đợt → giữ TẮT.
**M5 lúc sập:** MUA M5 vẫn có (5–14 lệnh/đợt, chủ yếu trước khi D1 chuyển phe) và ăn nhẹ (+22 / +7 / −12 / +38) nhờ chốt 0,5R.
Kết luận: C1 đánh tốt 3/4 đợt sập (lãi gấp 2 → 17 lần luật cũ), thua ở đợt giảm giằng co S1. Giữ nguyên bản chốt. Ứng viên vòng sau: lọc lệnh BÁN M15 khi biến động giằng co (nhiều nến hồi mạnh) để giảm thua kiểu S1.

## Vòng 8 — 30/10/2026: luật BÁN riêng trên D1 cho đợt giảm mạnh, gồng dài (Python `scripts/ban_d1.py`, D1 Binance 06/2023→10/2026)
SL = trên đỉnh 2 nến + 0,1 ATR; gồng không TP; phí $18. Cách kéo SL: đỉnh 10 / 20 ngày, ATR×3, hoặc thoát khi đóng trên EMA20.
| Luật vào | Gồng | Toàn bộ 2023→2026 | Từ 2025 |
|---|---|---|---|
| Nhấn chìm giảm (engulfing) bất kỳ | đỉnh 10 ngày | 50 lệnh, TB −0,05R | — |
| **Nhấn chìm giảm gần đỉnh 60 ngày** | **đỉnh 20 ngày** | 11 lệnh, thắng 27%, **TB +0,40R**, giữ TB 25 ngày | **6 lệnh, TB +1,39R**, sụt 0,9R |
| **Đóng cửa thủng EMA50 (EMA50 đi ngang/xuống)** | **đỉnh 10 ngày** | **9 lệnh, thắng 56%, TB +1,06R**, sụt 1,8R | 6 lệnh, TB +1,64R (đỉnh 20 ngày) |
| Phá đáy 20 ngày khi EMA20<EMA50 | đỉnh 10 ngày | 12 lệnh, TB +0,10R | — |
| Hồi về chạm EMA20 rồi đóng nến đỏ | đỉnh 20 ngày | 13 lệnh, TB +0,15R | 10 lệnh, +0,40R |
Lệnh "nhấn chìm gần đỉnh" từ 2025: 23/05/2025 −0,3R; 14/08/2025 +0,2R; **07/10/2025 bán 121.333 → ra 09/12 92.679 (+5,3R, 63 ngày) = bắt đỉnh 126k**; 27/04/2026 −0,9R; **07/05/2026 bán 80.006 → ra 14/07 65.044 (+5,0R)**; 28/08/2026 −0,9R.
Kết luận:
- Nến nhấn chìm đơn lẻ KHÔNG có lợi thế; phải ở GẦN ĐỈNH 60 ngày mới có ý nghĩa. Thủng EMA50 D1 là tín hiệu ổn định nhất (thắng 56%).
- Kiểu này ít lệnh (2–4 lệnh/năm), thua nhỏ −0,3~−0,9R, thắng lớn +5R nhờ gồng 1–2 tháng → đúng ý "giữ lệnh lâu nhất có thể".
- Mẫu nhỏ (9–11 lệnh) → mới là gợi ý, chưa chắc chắn.
- **Vấn đề thực tế:** SL D1 xa (≈ $3–6k giá BTC). Lot tối thiểu 0,01 BTC → rủi ro 1 lệnh ≈ $30–60 = 6–12% vốn 500 → bot sẽ bỏ qua (trần InpTranLotMin 4%). Muốn dùng cần vốn ~1.500–3.000 USD hoặc chấp nhận rủi ro lớn hơn cho riêng luật này.
Chưa code vào bot (anh còn ~9% usage tuần). Vòng sau: code "D1 swing bán" (nhấn chìm gần đỉnh 60 ngày + thủng EMA50) vào v2.7, backtest MT5.

## Vòng 9 (sơ bộ) — 01/11/2026: mẫu sóng ABC trên H4 (anh đề nghị) — Python `scripts/abc_h4.py`, H4 Binance 01/2025→10/2026
Luật: sóng A = đỉnh swing → đáy swing (5 nến mỗi bên) giảm ≥ 4%; sóng B hồi vào vùng Fib; tại đó nến H4 nhấn chìm giảm hoặc pin bar (râu trên ≥ 2× thân, ≥ 50% cây nến) → BÁN. SL trên đỉnh 2 nến + 0,1 ATR. Thoát: kéo SL theo đỉnh 10 nến H4 / TP sóng C = A / TP 3R. Phí $18.
| Biến thể | HL (01/2025→24/07/2026) | KT (25/07→26/10/2026) |
|---|---|---|
| Không lọc xu hướng, B 50–80%, nhấn chìm hoặc pin, kéo SL | 37 lệnh, TB +0,07R | 9 lệnh, −0,62R |
| **Chỉ khi D1 phe giảm**, B 50–80%, kéo SL | 19 lệnh, thắng 32%, **TB +0,47R** | 3 lệnh, −0,79R |
| D1 phe giảm, **B 38,2–61,8%** | 20 lệnh, **TB +1,23R** | 1 lệnh, −1,0R |
| D1 phe giảm, **B 60–78,6%** (vùng anh nói 60–70%) | 8 lệnh, **TB −0,57R** | 2 lệnh, −0,73R |
| D1 phe giảm, chốt TP 3R hoặc C=A thay vì kéo SL | ≈ 0 hoặc âm | âm |
Nhận xét sơ bộ:
- Mẫu ABC chỉ có lợi thế khi **lọc D1 phe giảm** và **gồng bằng kéo SL** (chốt TP cố định thì mất lợi thế).
- Hồi NÔNG (38–62%) tốt hơn hồi sâu; vùng 60–78,6% lại âm → sóng B hồi quá sâu thường là đảo chiều thật, không phải sóng B.
- Tập kiểm tra 3 tháng gần nhất gần như không có lệnh (thị trường tăng/giằng co) → chưa kiểm chứng được. Chờ xong luật D1 (anh yêu cầu) rồi mới làm tiếp.
### Vòng 9b — chỗ đặt SL cho mẫu ABC H4 (D1 phe giảm, B hồi 38–79%, nhấn chìm/pin, SL + 0,2 ATR)
| SL | Kéo SL theo đỉnh 10 nến H4 | 20 nến | **40 nến (~1 tuần)** | Không kéo (gồng tới chạm SL) |
|---|---|---|---|---|
| Trên nến tín hiệu | 31 lệnh, +0,61R | +0,25R | 23 lệnh, +1,10R, sụt 7,0R | −0,38R |
| **Trên đỉnh sóng B** | +0,43R | +0,37R | **21 lệnh, +1,11R, sụt 4,8R** | 7 lệnh, +2,10R (giữ 69 ngày) |
| Trên đỉnh sóng A | +0,07R | +0,01R | 18 lệnh, +0,55R, sụt 3,8R | −0,18R |
Không lọc D1 phe giảm: cả 3 kiểu SL đều âm (−0,06 đến −0,10R).
→ **Tốt nhất: SL trên đỉnh sóng B + kéo SL theo đỉnh cao nhất 40 nến H4.** SL trên đỉnh A quá xa → mỗi lệnh ăn ít R. Gồng rộng (40 nến) tốt hơn kéo sát (10–20 nến) vì sóng giảm hay quét ngược. Bắt buộc lọc D1 phe giảm.

## Vòng 8b — 01/11/2026: v2.7 (bán D1 gồng dài) trên MT5, 01/01/2025 → 25/10/2026 (22 tháng)
v2.7 = v2.6 chốt + module bán D1 (nhấn chìm giảm gần đỉnh 60 ngày HOẶC thủng EMA50 D1; SL trên đỉnh 2 nến + 0,1 ATR; kéo SL theo đỉnh 20 ngày; rủi ro 2%, trần lot tối thiểu 10%). Magic 24270000. Biên dịch 0 lỗi.
| Vốn | Bán D1 | Lãi | PF | Sụt eq | Sụt số dư | Số dư thấp nhất | Lệnh |
|---|---|---|---|---|---|---|---|
| 500 | tắt (= v2.6) | +813,01 | 1,30 | **67,0%** | 60,0% | **208** | 567 |
| 500 | bật | +4329,58 | 1,62 | 64,3% | 30,2% | 274 | 653 |
| 2000 | tắt | +6559,85 | 1,44 | 62,5% | 29,6% | 914 | 708 |
| 2000 | bật | +8390,63 | 1,47 | 60,3% | 31,3% | 970 | 716 |
Lệnh D1 gồng dài (vốn 2000): 22/02/2025 +2,2R (+77 USD, giữ 2 tháng); 15/08/2025 +0,2R; **08/10/2025 bán 121.398 (bắt đỉnh 126k) → ra 09/12 ở 94.218: +5,2R, +272 USD**; 19/03/2026 −0,3R; **08/05/2026 bán 80.010 → ra 14/07 ở 64.668: +5,1R, +153 USD**; 28/07/2026 −0,8R; 29/08/2026 −0,9R. Cộng trực tiếp ≈ **+285 USD** (vốn 500: ≈ +297 USD; lệnh 08/10/2025 bị bỏ vì lot 0,01 rủi ro > 10% vốn).
CẢNH BÁO khi đọc:
- Phần chênh lớn của tổng lãi (500: +813 → +4330) **không phải do lệnh D1 tự kiếm**: lệnh D1 chỉ kiếm trực tiếp ≈ +300 USD; phần còn lại do hiệu ứng dây chuyền (số dư khác → lot khác → lệnh sau khác, lãi kép). Con số này rất nhạy, đừng tin là lợi ích thật.
- **Rủi ro thật với vốn 500:** lot tối thiểu 0,01 → mỗi lệnh D1 rủi ro 30–50 USD = 6–10% vốn, không phải 2%.
- **Sụt equity 60–67% trên 22 tháng ở MỌI cấu hình** → bot vẫn có lúc sụt rất sâu (2025 nhiều đoạn khó). Đây là rủi ro lớn nhất hiện nay, cần xử lý trước khi chạy tiền thật.
Kết luận: luật bán D1 có ích (bắt được 2 con sóng sập lớn, thua nhỏ), giữ trong v2.7. Việc tiếp: (1) giảm sụt equity 60%+; (2) đưa mẫu ABC H4 (SL đỉnh B, kéo đỉnh 40 nến) vào MT5.

## 01/11/2026 — Kết quả TỪNG THÁNG của v2.7 (backtest 01/2025→10/2026) — để anh chuẩn bị chạy thật
Vốn 500: 22 tháng, **10 tháng lỗ (45%)**. Tháng tệ nhất −24% (09/2025), −21% (03/2025), −19% (01/2026). **3 tháng lỗ liên tiếp** 01–03/2025: −9%, −13%, −21% → 500 còn ≈ 313. Lãi dồn vào vài tháng: 06/2026 +126%, 02/2026 +83%, 08/2026 +75%.
Vốn 2000: 9/22 tháng lỗ (41%), tệ nhất −27% (01/2026), cũng 3 tháng lỗ liên tiếp đầu 2025.
Hiệu ứng lãi kép / dây chuyền khi chạy thật: lot = 2% số dư hiện tại → bắt đầu đúng chuỗi thua (như 01/2025) thì tài khoản teo, lệnh sau nhỏ + bị bỏ qua (lot tối thiểu vượt trần) → hồi rất chậm; bắt đầu đúng chuỗi thắng thì lãi vọt. Cùng 1 luật, kết quả thật phụ thuộc mạnh vào thời điểm bắt đầu.

## Vòng 10 — 01/11/2026: vì sao 10 tháng lỗ + cách quản lý vốn (anh: "thắng lớn xong phải đánh ít lại")
**Nguyên nhân các tháng lỗ** (v2.7, vốn 2000, 9 tháng lỗ):
- Tỉ lệ thắng sụp còn 13–29% (bình thường ~40%), mỗi tháng 14–28 lệnh chạm SL ban đầu, trong đó 30–70% bị quét trong ≤ 4 giờ → giá giật qua lại, SL đặt đúng nhưng bị quét liên tục.
- Lỗ lớn nhất: **BÁN M15 khi D1 phe giảm** (42 lệnh, −789 USD) và BÁN H1 khi D1 giảm (−388): các tháng 02/2025, 08/2025, 01/2026 giá giảm nhưng hồi mạnh. Tiếp theo: MUA M15 khi D1 "lửng chừng" (−259), MUA H1 khi D1 tăng nhưng tăng yếu (−212).
- Các tháng lỗ = giai đoạn chuyển pha / giằng co, không phải do SL sai. Đây là "giá phải trả" của đánh theo xu hướng; lọc giằng co đã thử nhiều lần (ATR, áo giáp) đều chặn luôn lệnh thắng.
**Mô phỏng quản lý vốn trên chuỗi 714 lệnh thật (R từng lệnh), vốn 2000:**
| Cách | Cuối | Sụt max | Tháng tệ nhất |
|---|---|---|---|
| 2% số dư (hiện tại) | 32.208 | 55,9% | −27% |
| Sau lệnh ≥ +5R: 10 lệnh tiếp 1% (ý "thắng lớn đánh ít lại") | 11.880 | 57,1% | −27% |
| Tháng trước lãi > 30% → tháng này 1% | 28.798 | 55,9% | −27% |
| Khoá 50% lãi | 18.582 | 71,8% | −35% |
| 2% vốn ban đầu (không lãi kép) | 9.345 | 71,3% | −35% |
| **Sụt > 15% so với đỉnh → 1%** | 19.102 | **38,5%** | **−14%** |
| Sụt > 10% → 1%, > 20% → 0,5% | 10.862 | 29,1% | −11% |
(vốn 500: 2% → 8.050, sụt 49,8%; sụt>15%→1% → 5.822, sụt 34,3%, tháng tệ nhất −21% → −11%, lãi/sụt 30,3 → 31,0)
→ "Thắng lớn đánh ít lại" KHÔNG giảm sụt vốn (sụt đến từ chuỗi thua lúc giằng co, không phải sau lệnh thắng). Cách hiệu quả: **hạ rủi ro khi đang sụt**. Đã code vào v2.7: `InpSutNguong=15`, `InpSutRuiRo=1.0` (đỉnh số dư lưu biến toàn cục). Đang backtest MT5.

## Vòng 10b — 01/11/2026: MT5, 12 tháng gần nhất 25/10/2025 → 25/10/2026, v2.7 (có bán D1)
| Vốn | Bản | Lãi | PF | Sụt eq | Sụt số dư | Tháng lỗ | Tháng tệ nhất | Thua LT |
|---|---|---|---|---|---|---|---|---|
| 500 | Gốc (luôn 2%) | **+4542,24** | 1,75 | 47,0% | 31,0% | 3/13 | −20% | 9 |
| 500 | Sụt 15% → 1% | +2254,34 | 1,57 | 42,7% | 23,9% | 5/13 | −13% | 9 |
| 500 | **Sụt 15% → 1% + thua 3 nghỉ 8h** | +3185,50 | 1,73 | **41,6%** | **18,4%** | 4/13 | −17% | **5** |
| 2000 | Gốc | **+12751,85** | 1,67 | 47,7% | 31,5% | 3/13 | −27% | 9 |
| 2000 | Sụt 15% → 1% | +4909,82 | 1,45 | 39,0% | 24,3% | 4/13 | −16% | 6 |
| 2000 | **Sụt 15% → 1% + thua 3 nghỉ 8h** | +5044,23 | 1,50 | **36,4%** | **19,5%** | 5/13 | **−14%** | **5** |
Kết luận: thêm "thua 3 nghỉ 8h" tốt hơn chỉ "sụt 15% → 1%" ở cả 2 mức vốn (lãi cao hơn, sụt thấp hơn). So với Gốc: sụt số dư 31% → 18–19%, thua liên tiếp 9 → 5, nhưng lãi giảm 30% (vốn 500) đến 60% (vốn 2000). Sụt equity vẫn 36–42% (nhiều lệnh mở cùng lúc).
Lựa chọn (anh quyết): Gốc = lãi tối đa, chịu sụt sâu; Bản bảo vệ (sụt 15%→1% + thua 3 nghỉ 8h) = an toàn hơn cho tiền thật.
**01/11: anh chọn BẢN GỐC LÃI CAO** → v2.7 mặc định `InpSutNguong=0` (tắt hạ rủi ro khi sụt), áo giáp tắt, bán D1 bật, rủi ro 2%. Biên dịch 0 lỗi. Bản chốt: `01-Trading/ThinhTrading/BAN-CHOT-v2.7_01-11-2026/` (chỉ đọc + SHA256). Đang test thêm 2 bản bảo vệ có thể giữ lãi: "chỉ thua 3 nghỉ 8h" và "bảo vệ + rủi ro 3%".
### Vòng 10c — 01/11/2026: bản bảo vệ giữ lãi (MT5, 12 tháng 25/10/2025→25/10/2026)
| Vốn | Bản | Lãi | PF | Sụt eq | Sụt số dư | Thua LT | Tháng tệ nhất |
|---|---|---|---|---|---|---|---|
| 500 | Gốc | +4542,24 | 1,75 | 47,0% | 31,0% | 9 | −20% |
| 500 | **Chỉ thua 3 → nghỉ 8h** | **+4365,55** | **1,85** | 44,7% | **22,3%** | **5** | −21% |
| 500 | Bảo vệ + rủi ro 3% (sụt → 1,5%) | +3255,78 | 1,58 | 45,2% | 24,9% | 4 | −18% |
| 2000 | Gốc | +12751,85 | 1,67 | 47,7% | 31,5% | 9 | −27% |
| 2000 | **Chỉ thua 3 → nghỉ 8h** | **+13385,11** | **1,77** | 43,4% | **24,2%** | 7 | −24% |
| 2000 | Bảo vệ + rủi ro 3% | +7944,81 | 1,48 | 45,4% | 27,0% | 4 | −17% |
→ **"Chỉ thua 3 → nghỉ 8h" = lãi tương đương gốc (−4% / +5%), sụt số dư 31% → 22–24%, PF cao hơn.** Đề xuất làm mặc định (chờ anh duyệt). Cấu hình: `InpAG_Bat=true`, `InpAG_ThuaLT=3`, `InpAG_NghiGio=8`, các lớp áo giáp khác tắt (LoNgay/LoTuan/MaxLenh/MaxRuiRoMo/PhanhTong=100, ATRNhan=0, SpreadNhan=100), `InpSutNguong=0`.

## 01/11/2026 — CHỐT v2.7 bản "thua 3 nghỉ 8h" + bảng mới + Pine v2.7
- Mặc định v2.7: rủi ro 2%, áo giáp chỉ bật lớp "thua 3 lệnh liên tiếp → nghỉ 8 giờ" (các lớp khác tắt, kể cả lọc ATR), không hạ rủi ro khi sụt, bán D1 gồng dài, mốc phe bán D1, chặn mua khi D1 giảm, M5 chốt 0,5R, tắt KÉO M15. Magic 24270000.
- Bảng trạng thái: 2 cột kiểu TradingView ở góc trên trái, chữ cỡ 12 (`InpCoChu`): Phe D1, Tiền thật, Trạng thái (nghỉ tới mấy giờ), từng khung (Quan sát / BUY/SELL ±R), Rủi ro, Số dư.
- Pine `ThinhTrading/ThinhTrading_EMA_v2_7.pine` (giữ bản v2.4 cũ): phe D1 → bán + chặn mua, bán sóng C giữ, tắt KÉO M15, M5 TP 0,5R, nhãn "SELL D1 GỒNG DÀI" + đường SL kéo theo đỉnh 20 ngày, bảng 2 cột góc trái. CHƯA dán thử trên TradingView (không có trình biên dịch Pine ở máy) → anh dán vào Pine Editor, báo lỗi nếu có.
- Bản chốt: `01-Trading/ThinhTrading/BAN-CHOT-v2.7_nghi8h_01-11-2026/` (mq5 + ex5 + pine, chỉ đọc, SHA256).
### 01/11/2026 — Nhật ký chấm điểm từng lệnh + Pine vẽ đường vào lệnh
- CSV thêm 6 cột: Phe D1 lúc vào, Cùng chiều khung trên, SL/ATR, Nến vào/ATR, Đã lên cao nhất (R), **Đánh giá**:
  Thắng đúng (cùng phe D1, khung trên đồng thuận) / Thắng may (ngược phe, khung trên chưa đồng thuận, vào nến giật) / Hoà vốn /
  Thua đúng (đúng luật, thị trường quay đầu; hoặc đã lên ≥ 2R rồi quay đầu) / Thua sai (bị quét ≤ 1 giờ, SL < 0,5 ATR, nến giật > 2 ATR, ngược phe D1).
- Tổng kết tháng có thêm mục "DANH GIA": số lệnh + tổng R mỗi loại, chi tiết lý do.
- Kiểm tra backtest 25/07→25/10/2026 vốn 500: +656,88, PF 1,88, sụt số dư 25,1%, 107 lệnh. Ví dụ 09/2026: thắng đúng 9 (+13,6R), thắng may 5 (+24,2R), thua đúng 11 (−10,5R), thua sai 11 (−10,9R, trong đó bị quét nhanh 6, nến giật 4).
- Ghi chú: "thắng may – khung trên chưa đồng thuận" kiếm nhiều R hơn "thắng đúng" → điều kiện "khung trên đồng thuận" chưa chắc là dấu hiệu tốt; theo dõi thêm vài tháng rồi mới kết luận.
- Pine v2.7: mỗi tín hiệu BUY/SELL/SELL D1 vẽ đường Giá vào (xanh dương), SL (đỏ), TP (xanh lá, nét đứt; M5 = 0,5R, khung khác = 2R tham khảo) dài 20 nến.
- Bản chốt `BAN-CHOT-v2.7_nghi8h_01-11-2026/` đã cập nhật (mq5, ex5, pine, SHA256).
### 01/11/2026 — Pine v2.7: HỘP LỆNH kiểu ENTRY / STOPLOSS / TP1-3 (anh gửi mẫu quảng cáo, định sau này bán chỉ báo)
- Mỗi tín hiệu BUY/SELL: hộp đỏ (giá vào → SL) + hộp xanh (giá vào → TP3), nhãn bên phải ENTRY / STOPLOSS / TP1 (1R; M5 = 0,5R) / TP2 (2R) / TP3 (3R); chạm TP thì thêm ✓, chạm SL thì ✗; hộp kéo dài tới khi chạm SL hoặc TP3.
- Bảng thêm thống kê THẬT trên chart: Tổng lệnh, Đang chạy, % chạm TP1 / TP2 / TP3, % chạm SL trước TP1 (không ghi "mục tiêu 80%" như quảng cáo).
- Đường giá vào/SL kiểu cũ: tắt mặc định (`veDuong=false`).
- Chưa chạy thử trên TradingView (máy không có trình biên dịch Pine).
### 01/11/2026 — Pine v2.7 (v6): hộp lệnh theo ĐÚNG luật thoát lệnh của bot (anh: "hệ thống mình có TP3 không?")
- Bỏ TP1/TP2/TP3 (bot không có TP cố định). Hộp lệnh giờ: nhãn "BUY H4 / SELL H1 (sóng C) / SELL D1 gồng dài + giá vào" chung với hộp; SL đỏ; vùng xanh tới mốc 3R ("3R: SL về hoà vốn"; M5 = "TP 0,5R"; D1 = "Gồng - kéo SL theo đỉnh 20 ngày").
- SL DI CHUYỂN theo luật bot (gần đúng): lệnh thường đạt 3R → hoà vốn → kéo theo đáy/đỉnh swing 10 nến; M5 chốt 0,5R; bán D1 kéo theo đỉnh 20 ngày. Thoát lệnh ghi "THOAT +xR / −1R".
- Mỗi khung mỗi chiều chỉ 1 lệnh cùng lúc (giống bot); chỉ giữ 3 hộp gần nhất (`soHop`). Trail cũ tắt mặc định.
- Bảng: Phe D1, Khung này, Đang chạy, Tổng lệnh, Thắng % / TB R mỗi lệnh (bật "bảng đầy đủ" thêm Tổng R, tuần SMA50, tát nước, rủi ro). Chữ nhỏ, nền hơi trong.
- Đã chuyển `//@version=6` (yêu cầu để xuất bản). Đã copy UTF-8 vào clipboard; chờ anh dán thử.

## Vòng 11 — 01/11/2026: lỗ hổng "D1 giảm chặn mất lệnh BUY H4 đầu sóng" (17/08/2026, 63k → 78k)
Anh: mục tiêu là vào ĐÚNG lúc tăng mạnh; không vào kịp thì ít nhất vào trễ, không được bỏ lỡ.
Nguyên nhân: 17/08 12:00 H4 cắt lên, nhưng nến D1 đã đóng gần nhất (16/08) vẫn phe giảm → v2.7 chặn mua. Bản cũ vào 63.567 ăn +15,1R.
Thêm: `InpChanMuaH4` (false = H4/D1/3D không bị chặn mua khi D1 giảm), `InpMuaTre` (mua bị chặn → D1 hết giảm trong N nến của khung đó, khung vẫn tăng → vào trễ, nhãn "(vao tre)").
MT5, 12 tháng 25/10/2025→25/10/2026, cấu hình "thua 3 nghỉ 8h":
| Vốn | Bản | Lãi | PF | Sụt số dư | Sụt eq | Lệnh H4 đợt 17/08 |
|---|---|---|---|---|---|---|
| 500 | Hiện tại (chặn mọi khung) | +4365,55 | 1,85 | 22,3% | 44,7% | không có |
| 500 | + mua trễ | +4942,41 | 1,89 | 24,0% | 44,7% | 18/08 00:00 ở 64.481, +7,1R |
| 500 | H4 không bị chặn | +5315,71 | 1,95 | 23,6% | 44,7% | **17/08 12:00 ở 63.567, +15,1R** |
| 500 | **H4 không bị chặn + mua trễ** | **+5519,88** | **1,95** | 23,3% | 44,7% | 17/08 12:00, +15,1R |
| 2000 | Hiện tại | +13385,11 | 1,77 | 24,2% | 43,4% | — |
| 2000 | H4 không bị chặn | +16599,37 | 1,87 | 23,9% | 43,4% | |
| 2000 | **H4 không bị chặn + mua trễ** | **+16719,16** | 1,87 | 23,9% | 43,4% | |
→ **Chốt: `InpChanMuaH4=false`, `InpMuaTre=30`** (lãi +26%/+25%, PF tăng, sụt gần như không đổi). Pine v2.7 cập nhật tương ứng. Bản chốt BAN-CHOT-v2.7_nghi8h_01-11-2026 đã cập nhật.

## Vòng 12 — 01/11/2026: đợt giảm 86k → 81k (6–9/10/2026) không có lệnh bán
Nguyên nhân: mốc phe giảm D1 (EMA10 cắt xuống EMA20) chậm — giá D1 đóng dưới EMA10 từ 07/10 nhưng EMA10 < EMA20 tới 14/10; H1 cắt xuống 07/10 02:00 bị chặn (H4 chưa giảm, D1 chưa phe giảm).
Thử (MT5, 12 tháng, vốn 500; mốc so sánh = bản chốt h4 + mua trễ: +5519,88, PF 1,95, sụt số dư 23,3%, sụt eq 44,7%):
| Bản | Lãi | PF | Sụt số dư | Sụt eq | Bán đợt 7/10 |
|---|---|---|---|---|---|
| Bán điều chỉnh M15/H1 (khung tới H4 giảm, D1 chưa giảm) | +4542,75 | 1,61 | 32,3% | 39,4% | M15 SELL 07/10 21:45 ở 83.154, +3,1R |
| Mốc phe giảm nhanh (D1 đóng dưới EMA10 & EMA10 đi xuống) | +3730,06 | 1,79 | **18,9%** | 42,8% | không |
| Cả hai | +3208,67 | 1,63 | 23,1% | 44,3% | M15 SELL 07/10, +3,1R |
→ Bắt được đợt 7/10 nhưng tổng 12 tháng KÉM hơn (bán điều chỉnh: nhiều lệnh bán ngược xu hướng D1 bị quét; mốc nhanh: chặn mua quá thường xuyên). **Không đưa vào mặc định** (`InpBanDieuChinh=false`, `InpMocBan=1`). Mốc nhanh giảm sụt số dư còn 18,9% (đổi lại −32% lãi) — có thể dùng nếu anh ưu tiên an toàn.

## Vòng 13 — 01/11/2026: KHOÁ LỜI (lệnh lên 3–5R rồi về tay trắng) + BÁN TRỄ (22/10 bỏ lỡ H4 SELL)
Khoá lời (input `InpKhoaKieu`, `InpKhoaTu`, `InpKhoaTraR`, `InpKhoaPhanTram`; tính lãi cao nhất theo nến đã đóng; chỉ là SÀN cho SL, vẫn kéo SL theo nấc):
6 tháng 25/04→25/10/2026, vốn 500 (không khoá: +2821, PF 2,16, sụt eq 34,1%, lệnh lớn nhất 32,6R):
| Kiểu | +Lãi | PF | Sụt eq |
|---|---|---|---|
| trả 2R từ 3R | 3283 | 2,26 | 26,9% (lệnh lớn nhất chỉ 15R) |
| trả 3R từ 4R | 2849 | 2,25 | 28,7% |
| trả 1,5R từ 2,5R | 2227 | 2,04 | 25,6% |
| trả 2R từ 2R | 3216 | 2,14 | 27,8% |
| giữ 30% từ 3R | 3674 | 2,30 | 29,2% |
| **giữ 40% từ 3R** | **4706** | **2,50** | 27,4% |
| giữ 40% từ 2R | 4495 | 2,39 | 27,3% |
| giữ 50% từ 2R / 3R / 4R | 4548 / 3840 / 3733 | 2,36 / 2,34 / 2,37 | 27,0 / 27,7 / 30,2% |
| giữ 60% từ 2R / 3R | 2372 / 2509 | 1,93 / 2,01 | 27,0 / 28,2% |
12 tháng vốn 500: không khoá +5519,88 (PF 1,95, eq 44,7%) | giữ 50% từ 3R +5874,75 (PF 2,14) | **giữ 40% từ 3R +6985,81 (PF 2,17, sụt số dư 23,6%, eq 47,9%)**.
→ Vùng 40–50%, bắt đầu 2–3R đều hơn hẳn không khoá (ổn định theo tham số). Kiểu "trả lại cố định" cắt mất sóng lớn. CHỌN: giữ 40% lãi cao nhất từ 3R.
Bán trễ 22/10: nguyên nhân bỏ lỡ = D1 20–21/10 đóng TRÊN EMA (hết phe giảm 2 ngày) đúng lúc H4 cắt xuống 22/10 20:00; 0h 23/10 D1 giảm lại nhưng không còn cắt mới. Thêm `InpBanTreD1` (đối xứng mua trễ). Test 12 tháng (không khoá): 0 nến +5519,88 PF 1,95 | 12 nến +5301,83 PF 1,90 | 24 nến +6518,49 PF 1,89 eq 49,8%. Bán trễ hoạt động (23/10 00:00 SELL H1 vào trễ 81.304) nhưng tổng hiệu quả lẫn lộn → đang test kết hợp với khoá 40%.
Kết hợp khoá 40% + bán trễ 24 nến (12 tháng, vốn 500): +6847,75, PF 2,07, sụt eq 52,1% → KÉM hơn chỉ khoá 40% (+6985,81, PF 2,17, eq 47,9%).
**CHỐT (01/11): `InpKhoaKieu=2`, `InpKhoaTu=3`, `InpKhoaPhanTram=40` (giữ 40% lãi cao nhất từ 3R); `InpBanTreD1=0` (tắt bán trễ, vẫn giữ code).** Pine thêm khoá lời tương ứng (`khoaPT=40`, `khoaTu=3`). Bản chốt cập nhật.

## Vòng 14 — 01/11/2026: H4 không bán ở 2 đỉnh hồi 22/10 (84.859) và 29–30/10 (81.847) — Python, giá Exness + Binance
Bot (đúng luật): H4 cắt xuống 23/10 03:00 (D1 không phe giảm), 29/10 15:00 (D1 không phe giảm), 30/10 07:00 (vùng nhiễu: 4 lần cắt / 20 nến) → không có lệnh. 2 vòng trắng = nến rút râu trên ở đỉnh hồi, hệ EMA không có luật bán kiểu này.
Thử luật "bán rút râu ở đỉnh hồi khi D1 EMA10 < EMA20": nến H4 râu trên ≥ 2× thân & ≥ 50% cây nến, đỉnh = cao nhất N nến; SL trên râu + 0,1 ATR; kéo SL theo đỉnh 40 nến + khoá 40% từ 3R; phí $18. Binance H4 01/2025→10/2026:
| Biến thể | HL (→24/07/2026) | KT (25/07→26/10) |
|---|---|---|
| đỉnh 20 nến, lọc D1 | 27 lệnh, thắng 30%, **TB +0,80R**, sụt 2,4R | 5 lệnh, TB −0,30R |
| không lọc D1 | 53 lệnh, TB +0,29R, sụt 8,9R | 12 lệnh, TB −0,27R |
| đỉnh 40 nến | 15 lệnh, TB −0,16R | 1 lệnh |
| đỉnh 10 nến | 42 lệnh, TB +0,47R | 6 lệnh, TB −0,28R |
| râu ≥ 3× thân | 16 lệnh, TB +1,17R | 2 lệnh, −0,40R |
→ Có lợi thế trên tập huấn luyện nhưng 3 tháng gần nhất âm (mẫu nhỏ); nhạy với tham số (đỉnh 40 nến âm). Tháng 10 chỉ bắt được 19/10 (+1,2R); đỉnh 22/10 bị bỏ vì lệnh 19/10 còn mở. CHƯA đưa vào bot — ứng viên, cần backtest MT5 khi có thêm dữ liệu.

## Vòng 15 — 01/11/2026: mốc phe theo "đường xanh" của anh (EMA99 H4) — `InpMocBan=6`
Đường xanh trên TradingView của anh ≈ EMA99/EMA100 H4. Ca 20/01/2026: EMA10 H4 cắt xuống dưới EMA99 ở 91.219, bot bán 29/01 ở 87.846 (D1 mới phe giảm) → bán theo đường xanh sớm hơn 9 ngày, cao hơn ~3.400.
Mốc 6: phe giảm = H4 EMA10 & EMA20 cùng dưới EMA99 (cho BÁN, chặn MUA khung nhỏ). Test MT5 3 tháng 25/07→25/10/2026, vốn 500, bản chốt (khoá 40%):
| Bản | Lãi | PF | Sụt số dư | Sụt eq | Lệnh |
|---|---|---|---|---|---|
| Hiện tại (mốc D1) | **+1373,89** | **2,54** | 20,7% | 25,8% | 108 |
| Đường xanh (vẫn cần khung trên tới D1 đều giảm) | +747,16 | 2,04 | 21,5% | 24,7% | 91 |
| Đường xanh, bỏ yêu cầu khung trên | +393,73 | 1,44 | 27,8% | 33,4% | 116 |
→ 3 tháng gần nhất: đường xanh KÉM hơn mốc D1 hiện tại (lãi −46% / −71%). Không đưa vào mặc định (code giữ, chọn bằng InpMocBan=6).

## Vòng 16 — 01/11/2026: D1 không có lệnh MUA ở đáy tháng 7–8/2026
D1 cắt lên 10/07 (RSI 54, 3D ngược), 07/08 (RSI 54,9, 3D ngược), 19/08 (nhiễu, 3D ngược) → bị chặn. RSI tuần cắt lên MA14 tuần 08/08 (anh nói đúng). Thêm `InpD1Bo3D`, `InpD1RsiMua`, `InpD1BoNhieu`.
MT5 22 tháng 01/2025→10/2026, vốn 500: gốc +7712,17 PF 1,96 | bỏ 3D +7712,17 (không đổi) | **bỏ 3D + RSI D1 ≥ 50: +8007,29 PF 1,99** (BUY D1 11/07/2026 ở 64.128, SL 61.253, lên >3R) | + bỏ nhiễu: như trên. Sụt vốn không đổi.
Lưu ý: với vốn 500 nhiều lệnh MUA D1 bị bỏ vì lot tối thiểu rủi ro 20–33% > trần 4% (SL D1 xa 6–11k).
**CHỐT: `InpD1Bo3D=true`, `InpD1RsiMua=50`.** Pine đồng bộ. EA trên chart MT5 gắn lại để nhận thông số mới. Bản chốt cập nhật.

## Vòng 17 (01/11/2026) — Khoá lời sớm hơn (anh: "lãi 2R mà thành lỗ là không chấp nhận được với khung D")
Ca gốc: BUY D1 09/04/2026 vào 71.066, đỉnh +2,2R (82,8k ngày 06/05), chưa tới 3R nên SL không dời → 03/06 chạm SL −1R.
Nhật ký 12 tháng cũ: 20 lệnh từng lên 1,5–3R rồi vẫn thua (≈ −16R).
Backtest MT5 chỉ đoạn 01/04 → 10/06/2026, vốn 5.000, M1 OHLC (theo ý anh: chạy đúng đoạn đó):
| Cách | Lãi $ | PF | Sụt số dư | Tổng R | BUY D1 71.066 | H4 BUY 01/05 (đỉnh 2,4R) |
|---|---|---|---|---|---|---|
| k3 (hiện tại: khoá từ 3R, giữ 40%) | 7.188 | 2,96 | 20,8% | +64,7 | −1,00R | −1,00R |
| k15 (từ 1,5R, giữ 40%) | 8.039 | 3,38 | 17,1% | +67,2 | +0,87R | +0,99R |
| **k2p50 (từ 2R, giữ 50%)** | **8.681** | **3,41** | 18,9% | **+70,7** | **+1,09R** | **+1,23R** |
| tra1 (từ 1,5R, đỉnh − 1R) | 2.412 | 1,62 | 15,7% | +19,2 | +1,18R | +1,47R | ← cắt lệnh lớn, loại
Kết luận: k2p50 tốt nhất đoạn này. Lưu ý: chỉ là 1 đoạn ~2 tháng (anh yêu cầu không chạy dài).

→ **ĐÃ ÁP DỤNG 01/11/2026** (anh duyệt "Đổi luôn"): InpKhoaTu 3→2, InpKhoaPhanTram 40→50 cho mọi khung; Pine khoaTu=2, khoaPT=50. Bot gắn lại chart 70913810952245, bản chốt BAN-CHOT-v2.7_nghi8h_01-11-2026 đã khoá lại.

## Vòng 17b (01/11/2026) — Khoá lời cho lệnh BÁN D1 gồng dài (slot D1 SW)
Ca gốc: SELL D1 19/03/2026 vào 71.230, lãi cao nhất +1,23R, SL kéo theo đỉnh 20 ngày → 08/04 ra −0,30R.
Module BanD1 trước đây không có khoá lời. Thêm input InpD1KhoaTu (0 = tắt) / InpD1KhoaPT. Test MT5 01/03 → 15/07/2026, vốn 5000, khoá lời lệnh thường 2R/50%:
| Cách (lệnh SELL D1) | Lãi $ | PF | SELL 19/03 | SELL 08/05 (sập tới 64,7k) | Tổng R của SELL D1 |
|---|---|---|---|---|---|
| Tắt (hiện tại) | 9.270 | 2,03 | −0,30R | **+5,07R** | +4,77R |
| Từ 1R giữ 50% | 9.109 | 2,00 | +0,62R | +0,67R (ra sớm) + vào lại +0,71R | +2,00R |
| Từ 1,5R giữ 50% | 9.550 | 2,06 | −0,30R | +0,97R (ra sớm) + vào lại 27/05 +4,68R | +5,35R (nhờ vào lại, may) |
| Từ 2R giữ 50% | 9.270 | 2,03 | −0,30R | +5,07R | +4,77R |
Kết luận: KHÔNG áp dụng. Khoá từ 1R cứu được lệnh −0,3R nhưng cắt lệnh sập lớn (+5R → +0,7R). Lệnh bán D1 gồng dài cần chừa khoảng thở. Giữ InpD1KhoaTu = 0 (code có sẵn, mặc định tắt).

## Vòng 18 (03/11/2026) — Thử nhanh hệ thống Bollinger cho ETH (dự định, chưa làm bot)
Python `scripts/bb_eth.py`, dữ liệu ETHUSDT Binance M15 05/2025 → 11/2026 (`data/eth15.csv`), phí 0,06%. BB(20,2), EMA200.
Kiểu A = chạm dải ngoài rồi đóng lại trong dải (hồi về); B = co thắt rồi phá dải; C = theo xu hướng EMA200, hồi về dải giữa rồi bật lại.
Thoát: tp_giua (chốt ở dải giữa) / giua (đóng qua dải giữa thì ra) / khoa (lên 2R thì giữ 50% lãi cao nhất).
- **M15: lỗ gần như mọi kiểu** (A tp_giữa −140R/765 lệnh) → bỏ M15.
- H1: chỉ C+giữa dương (+54,5R/749 lệnh, thắng 21%; 6 tháng gần +19R, 3 tháng +9R).
- **H4 tốt nhất nhưng ít lệnh:** C+khoá +42R/38 lệnh (thắng 47%, sụt 3,1R); B+giữa +28R/26 lệnh; A+khoá+lọc EMA200 +4,7R/43 lệnh.
Kết luận tạm: nếu làm hệ thống ETH thì nghiêng về **H4 kiểu C (theo xu hướng) + khoá lời 2R/50%**, có thể thêm H1 kiểu C. Mẫu H4 còn nhỏ (≤40 lệnh) → cần test MT5 dữ liệu Exness dài hơn trước khi chạy thật.

## Vòng 19 (03/11/2026) — Hệ thống RSI trên BTC/ETH (Python, giữ nguyên nền tảng)
Script `scripts/rsi.py` (chế độ: mặc định = quét, `ben` = tham số lân cận, `von` = ghép + vốn, `von_cu` = đoạn cũ). Dữ liệu Binance: BTC M5 01/2025→26/10/2026, ETH M15 05/2025→02/11/2026. Phí 0,06%.
**Nền tảng giữ nguyên:** SL đáy/đỉnh swing 2 nến; kéo SL bậc thang swing 10 nến; khoá lời từ 2R giữ 50%; thua 3 lệnh nghỉ 8h; rủi ro 2% (H4 ×1,5); mỗi khung mỗi chiều 1 lệnh. Chưa mô phỏng: nhồi lệnh, trần lot tối thiểu. **Thêm chặn SL < 0,2% giá → bỏ lệnh** (không có chặn này, phí/1R làm vài lệnh ra −100…−4000R; bot EMA hiện cũng không có chặn này → nên cân nhắc đưa vào nền tảng).
Tín hiệu thử: K1 hồi về (RSI cắt lên 30 / xuống 70); K2 động lượng (cắt lên 55 / xuống 45); K3 hồi trong xu hướng EMA200 (cắt 40/60); **K4 = MH2 nghiên cứu cũ của anh 09/2026** (EMA9(RSI) cắt WMA45(RSI) + khung lớn cùng chiều); **K5 = MH3a** (RSI ≥70 đủ 2 nến, máy trạng thái quán tính). Lọc: không / EMA200 / phe D1; thêm cờ S = SL 0,5–1,5% giá (luật cũ). Mã nguồn + artifact cũ lưu ở `TOI-UU/tham-khao-rsi-cu/`.

**Quét 12 tháng (R, có chặn SL 0,2%):**
- **Loại:** K1 (lỗ nặng ở M15/H1/H4, cả 2 mã), K3 (lỗ), mọi kiểu ở BTC H4.
- **K2 H1 không lọc: dương ở MỌI ngưỡng lân cận 52/55/58/60, cả 2 mã, cả 2 nửa năm.** BTC 55/45: 246 lệnh +54R (nửa đầu +8, 6T +46), sụt 13,5R. ETH: 261 lệnh +22,5R (52: +30,7; 58: +43,3; 60: +34). Mặt xấu: bỏ 3 lệnh lớn nhất thì ≈ hoà/âm → sống nhờ vài sóng lớn.
- K4 (MH2): BTC H1 dương (9/45 +26R, 7/35 +32R, 12/55 chỉ +3R); **ETH H1 âm (−20R)** → MH2 chỉ hợp BTC, không ổn định theo tham số.
- K5 (MH3a) M15: BTC +26R (nửa đầu −1,6), ETH +29R (nửa đầu +11, 6T +18).
- ETH H4 K2 lọc phe D1: 36 lệnh +38,5R nhưng gần như toàn bộ ở 6 tháng gần (nửa đầu +0,8R).

**Ghép + vốn (lãi kép, áo giáp thua 3 nghỉ 8h):**
| Tổ hợp | 12T gần: lãi / sụt | Đoạn cũ KHÔNG dùng để chọn: lãi / sụt |
|---|---|---|
| ETH: K2 H1 | +19,5% / 39,1% | +8,4% / 25,1% (6 tháng) |
| ETH: K2 H1 + K2 H4 lọc D1 | +188% / 29,5% | +32,8% / 22,5% |
| **ETH: K2 H1 + K2 H4 lọc D1 + MH3a M15** | **+341% / 38,6%**, 506 lệnh, tháng tệ −18% (05/26), 5/13 tháng âm | **+103% / 24,6%**, 225 lệnh, tháng tệ −7% |
| ETH tổ hợp trên, chỉ MUA | +140% / 34,7% | +78% / 29,6% → bỏ chiều bán làm kém hơn, giữ 2 chiều |
| ETH: K4 H1 (MH2) | −35% / 42% | +7,6% / 20% |
| BTC: K2 H1 | +103% / 25,8% | +49% / 22,2% (10 tháng) |
| BTC: K4 H1 (MH2) | +45% / 30,5% | +55% / 24,7% |
| BTC: 3 thành phần như ETH | +232% / 36% | **−29% / 49,6%** → không hợp BTC |
**Kết luận vòng 19:**
- Ứng viên **hệ thống B = ETH "RSI 55/45"**: H1 không lọc + H4 lọc phe D1 + MH3a M15, 2 chiều, nền tảng giữ nguyên. Dương ở cả đoạn chọn lẫn đoạn cũ. Mặt xấu: sụt 25–39%; lãi phụ thuộc sóng lớn; đoạn cũ (05–11/2025) là sóng tăng mạnh ETH; Python + Binance ≠ Exness (spread ETH, giờ phiên); đã chọn tổ hợp sau khi nhìn 12 tháng → còn thiên lệch chọn.
- BTC: RSI 55/45 H1 và MH2 H1 đều dương cả 2 đoạn, nhưng **trùng ý tưởng với bot A** (EMA + RSI 55/45 trên BTC) → chạy song song là nhân đôi rủi ro cùng hướng; không đề xuất làm hệ thống riêng trên BTC.
- Việc tiếp: (1) dựng bot ETH từ khung `v2_8.mq5` (magic 3xxxxxxx), biên dịch bằng `bd_cli.sh`; (2) backtest MT5 dữ liệu Exness ETHUSDm khi MCP chạy lại; (3) đo tương quan lỗ cùng lúc với bot A trước khi chạy chung tài khoản.

## Vòng 20 (03/11/2026) — Đo "hành trình RSI" của anh trên dữ liệu (chưa phải backtest lệnh)
Anh: không đánh RSI kiểu mốc (vòng 19) mà theo hành trình: quán tính tăng/giảm, phân kỳ, EMA9(RSI) cắt WMA45(RSI) rồi mở rộng/thu hẹp, đáy sâu → retest / 2 đáy, khung nhỏ là xúc tác cho khung lớn liền kề, khung lớn chi phối khung nhỏ.
Dữ liệu Binance từ 2018 (D1/H4/H1) và 2022 (M15), `data/{BTC,ETH}_{15m,1h,4h,1d}.csv` (tải bằng `scripts/dl_dai.py`). Script `scripts/hanh_trinh.py`, `scripts/nho_lon.py`.
**Đối chiếu TradingView (03/11, BTCUSD D1):** Python khớp chỉ báo của anh (RSI 35,58 / EMA9 38,66 / WMA45 47,38 vs TV 35,56 / 38,63 / 47,29). Vạch màu trên chart: **xanh = RSI ≥ 80, cam = RSI ≤ 20** (không phải 70/30). Ngưỡng này cần anh xác nhận.

**1. Khung nhỏ cắt ngược khung lớn — bên nào thắng?** (theo dõi 8 nến khung lớn; "lớn thu hẹp" = EMA9(RSI) khung lớn đã quay đầu về phía khung nhỏ, "lớn mở rộng" = vẫn đi xa)
| Cặp | Lớn MỞ RỘNG: lớn quay theo / nhỏ quay lại | Lớn THU HẸP: lớn quay theo / nhỏ quay lại |
|---|---|---|
| M15→H1 (BTC, ETH) | 26% / 61–63% | 44–49% / 49–53% |
| H1→H4 | 25–27% / 60–63% | 45–50% / 48–52% |
| H4→D1 | 18–22% / 75–79% | 31–49% / 49–69% |
| D1→W1 (ít mẫu) | 10–17% / 80–90% | 50–62% / 38–50% |
→ **Khớp lời anh:** khung lớn còn mở rộng thì khung nhỏ cắt ngược phần lớn là sóng hồi rồi quay lại (60–90%). Khung nhỏ chỉ "kéo" được khung lớn khi khung lớn đã thu hẹp (tỉ lệ kéo được gấp ~2 lần). Khung càng lớn thì khung lớn chi phối càng mạnh.
→ Hướng giá: riêng việc cắt, ở M15/H1/H4 đúng hướng ~50% (không có lợi thế). MUA đồng thuận ở cặp H4/D1 đúng 55–57%; D1/W1 đúng 71–77%, +28% sau 8 tuần (26–31 lần, BTC/ETH). BÁN đồng thuận khung lớn thì kém (đúng 41–48%) → sóng giảm khác sóng tăng, đúng ý anh.
**2. Đa khung khi khung giữa cắt** (vòng 20b): "khung lớn cho phép" cải thiện tỉ lệ đi thuận/đi ngược ở mọi khung, vd MUA H4 với D1 cho phép: 1,35 (BTC) / 1,51 (ETH) so với 1,05 khi D1 chặn; MUA D1 với W1 cho phép: 1,89 / 2,73.
**3. Đỉnh:** quán tính tăng (RSI ≥ 80) + phân kỳ âm rồi EMA9 cắt xuống → **chưa chắc giảm**: BTC D1 30 ngày sau vẫn +10%, chỉ 42% lần thấp hơn (12 lần). Lần cắt xuống đầu tiên sau quán tính tăng thường chỉ là nghỉ.
**4. Đáy theo độ sâu RSI** (đo lúc EMA9 cắt lên): sau cắt lên, giá retest/thủng đáy cũ trong 30 nến khoảng 40–55% ở mọi nhóm → "cắt lên chưa mua ngay" đúng. Riêng BTC D1: RSI < 20 → thủng đáy 67% (6 lần), 20–30 → 43%, 30–35 → 29% (đúng hướng anh nói nhưng ít mẫu); H4/H1 và ETH không thấy khác biệt rõ.
**5. Độ mở rộng** (đo từ nến thứ 5 sau cắt, không nhìn trước): mở rộng nhiều thì giá ít đi ngược hơn (2,6–2,9 vs 3,4–3,9 ATR) nhưng không đi xa hơn rõ rệt (bản đo đầu bị nhìn trước, đã sửa).
**Luật rút ra để code (chờ anh xác nhận):** chỉ vào theo khung giữa khi khung lớn liền kề ĐỒNG THUẬN hoặc ĐÃ THU HẸP về phía mình; khung nhỏ cắt ngược khung lớn đang mở rộng = sóng hồi, không vào (hoặc là điểm vào theo khung lớn khi khung nhỏ quay lại); ưu tiên chiều MUA; quán tính 80/20.

## Vòng 21 (03/11/2026) — ENGINE "hành trình RSI" (Python) + nền tảng, BTC/ETH từ 2018
Script `scripts/engine.py`. Chỉ báo RSI14 + EMA9(RSI) + WMA45(RSI). Bộ khung nhỏ/giữa/lớn: M15/H1/H4 (M15 từ 2022), H1/H4/D1, H4/D1/W1. Nền tảng như vòng 19 (SL swing 2, kéo SL 10, khoá 2R/50%, SL ≥ 0,2% giá, phí 0,06%, thua 3 nghỉ 8h, 2%/lệnh, H4/D1 ×1,5).
Biến thể: V0 khung giữa cắt (mốc) · V1 + khung lớn cho phép (đồng thuận HOẶC thu hẹp) · V2 + khung lớn đồng thuận · V3 = V1 + bỏ lần cắt đầu sau vùng cam/xanh (RSI ≤20/≥80) · V4 vào ở khung nhỏ khi hết sóng hồi (giữa mở rộng, lớn cho phép).
R/lệnh (trước 2024 → 2024-nay), 12T gần (R), vốn 12T:
| Bản | BTC | ETH |
|---|---|---|
| H1 V0 2 chiều | 0,16 → 0,11; 12T +46R; vốn +88% sụt 25% | 0,12 → 0,08; 12T −9,6R; vốn −48% sụt 55% |
| H1 V0 chỉ MUA | 0,22 → 0,23; +17,5R | 0,17 → 0,14; −3,4R |
| H1 V1 chỉ MUA | 0,17 → 0,37; +18,6R; +33% sụt 21% | 0,18 → 0,21; −10R; −39% |
| **H1 V2 chỉ MUA** | **0,32 → 0,46; 12T +22,5R, 6T +27,5R; vốn +41% sụt 24%** | **0,13 → 0,21; 12T +6,1R; vốn +7% sụt 21%** (bản H1 duy nhất của ETH dương 12T) |
| H4 V2 2 chiều | 0,38 → 0,32; +6,6R; +17% sụt 27% | 0,46 → 0,27; +4,7R; +10% sụt 21% |
| H4 V4 chỉ MUA | 0,63 → 0,30; +11R; +18% sụt 15% | 0,19 → 0,31; +13,7R; +23% sụt 10% |
| D1 V2 chỉ MUA | 9 lệnh +65,6R (trước 2024); 4 lệnh +2,8R | 17 lệnh +12,2R; 7 lệnh +8,6R |
Nhận xét:
- Bản V0 (chỉ cắt khung giữa) đã dương dài hạn nhờ phần thoát lệnh của nền tảng; ETH H1 12 tháng gần âm.
- **Lọc khung lớn ĐỒNG THUẬN (V2) + chỉ MUA** cải thiện R/lệnh rõ nhất và ổn định ở cả 2 giai đoạn, cả 2 mã. "Thu hẹp" (V1) cho thêm lệnh nhưng các lệnh thêm không tốt hơn mốc → khi vào lệnh nên chờ đồng thuận hẳn; "thu hẹp" chỉ dùng để chuẩn bị.
- V3 (bỏ lần cắt đầu sau vùng cam) gần như không đổi so với V1 → chưa thấy lợi ích, chưa đưa vào.
- V4 vào ở M15: lỗ (phí + nhiễu). Vào ở H1 (bộ H4) thì dương nhẹ, ổn hơn ở ETH.
- Chiều BÁN theo engine: kém hơn MUA ở hầu hết bộ (khớp "sóng giảm khác sóng tăng").
- Mặt xấu: lãi khiêm tốn (ETH 12T chỉ +7%), sụt 21–24%; D1 quá ít lệnh; Binance ≠ Exness; chưa thử nhồi lệnh.
Ứng viên: **"RSI hành trình" H1, khung lớn H4 đồng thuận, chỉ MUA** (BTC hoặc ETH). Trên BTC trùng hướng với bot A (cùng là theo xu hướng H1) → cần đo lệnh trùng trước khi chạy chung.
**Vòng 21b — mô phỏng tiền thật vốn 500 USD** (`scripts/von500.py`; lot thật, lot min rủi ro > 4% thì bỏ, 2%/lệnh, H4 ×1,5, thua 3 nghỉ 8h; giả định lot BTC min 0,01 / ETH min 0,1 — cần kiểm lại trên Exness):
| Bản | 12 tháng | 6 tháng | 3 tháng | Sụt từ đỉnh (12T) |
|---|---|---|---|---|
| BTC H1 V2 chỉ MUA | 500 → 713 (+213), 49 lệnh, bỏ 13 vì lot min | +223 | +284 | 21%, tháng tệ 02/26 −60 |
| ETH H1 V2 chỉ MUA | 500 → 502 (+2), 60 lệnh | −9 | +63 | 17%, tháng tệ 10/26 −61 |
| ETH H4 V4 chỉ MUA | 500 → 565 (+65), 31 lệnh | +47 | +116 | 9% |
| BTC H4 V4 chỉ MUA | 500 → 569 (+69), 28 lệnh | +56 | +105 | 12% |
| ETH ghép H1V2 + H4V4 | 500 → 486 (−14), 89 lệnh | −32 | +47 | 23% (ghép tệ hơn từng phần: lệnh thua dồn cùng lúc + áo giáp cắt lệnh thắng) |
So sánh: bot A EMA v2.7 cùng vốn 500, 12 tháng (MT5) +4366 USD, sụt số dư 22% → engine RSI hành trình hiện YẾU hơn nhiều. Riêng ETH chưa có bản engine nào ra lãi đáng kể 12 tháng. Kết luận: engine chưa đủ để làm bot riêng; hữu ích nhất là làm BỘ LỌC (khung lớn đồng thuận theo EMA9/WMA45 của RSI) — thử gắn vào hệ thống B ETH vòng 19 hoặc bot A ở vòng sau.

## Vòng 22 (03/11/2026) — Mỗi khung ĐỘC LẬP, không khung nào chi phối (ý anh)
Script `scripts/tung_khung.py`. Luật MUA trên chính khung đó: pha giảm (EMA9(RSI) < WMA45(RSI)) → thu hẹp → EMA9 cắt lên → 2 đường mở rộng (khoảng cách tăng 2 nến liền) + RSI trên cả 2 đường → BUY; BÁN đối xứng. E0 = vào ngay lúc cắt; E1 = chờ mở rộng (tối đa 10 nến); E2/E3 = E1 + pha trước phải sâu ≥ 3 / ≥ 5 điểm. Nền tảng giữ nguyên; tiền = vốn 500 USD, lot thật, thua 3 nghỉ 8h.
Vốn 500 USD, 12 tháng gần (bản tốt nhất mỗi khung, 2 chiều trừ khi ghi):
| Khung | BTC | ETH |
|---|---|---|
| M15 | lỗ hoặc sụt 50–85% ở mọi bản (phí + nhiễu) → loại | E0 +176 nhưng sụt 52%, 6T −65 → loại |
| H1 | **E1: 500 → 946 (+446), sụt 25%, 6T +271**; R: +274R trước 2024, +73R sau | mọi bản âm 12T (−64…−222) dù dài hạn dương |
| H4 | E0 MUA +113 (sụt 7%); E3 BÁN +173 | **E3: 500 → 647 (+147), sụt 10%, 6T +106**; E0 chỉ +0 → độ sâu pha trước giúp rõ ở ETH H4 |
| D1 | +34…+53 (ít lệnh; nhiều lệnh bị bỏ vì lot min 0,01 BTC rủi ro > 4% vốn 500) | +16…+36 |
Ghép nhiều khung (cùng tài khoản, cùng áo giáp):
- BTC H1E1 + H4E1 + D1E1: 12T 500 → 1254 (+754), sụt 36%, tháng tệ 07/26 −109; 6T +645; 3T +162. Bỏ 57 lệnh vì lot min.
- ETH H4E3 + D1E1: 12T 500 → 733 (+233), sụt 13%; 6T +123; 3T +103.
- ETH thêm H1E3: tệ hơn (12T +90, sụt 36%).
Kết luận: tách từng khung độc lập TỐT HƠN có khung lớn chi phối (vòng 21: BTC H1 +213 → +446; ETH +2/+65 → +147/+233). Chờ "mở rộng" (E1) giúp ở BTC H1; "pha trước đủ sâu" (E3) giúp ở ETH H4. M15 không dùng được. Vẫn thua xa bot A (+4366 / 12T, có nhồi lệnh + chạy M5…D1 cùng lúc, dữ liệu MT5 Exness) — so sánh chưa ngang hàng.
Ứng viên: **ETH: H4 (E3) + D1 (E1), 2 chiều** — sụt thấp, dương cả 3/6/12 tháng; BTC: H1E1 + H4E1 + D1E1 (lãi cao hơn nhưng sụt 36% và trùng thị trường với bot A).

## Vòng 23 (03/11/2026) — Bỏ chia hộp E0–E3: chấm điểm hành trình bằng số liên tục (ý anh: "thị trường đa dạng, có trạng thái nằm giữa")
Script `scripts/diem.py`. Mỗi lần EMA9(RSI) cắt WMA45(RSI) (mỗi khung độc lập, H1/H4/D1, BTC+ETH, 2 chiều) ghi 8 đặc điểm liên tục: độ sâu pha trước, độ dài pha, RSI cực trị pha trước, dốc EMA9, dốc WMA45, RSI cách WMA45, ATR/giá, vị trí giá trong biên 50 nến. Học đường kết quả (R theo 10 ô, làm trơn với ô bên cạnh) trên **6.743 lần cắt trước 2024**; điểm = cộng độ lệch của 8 đặc điểm. **Kiểm tra trên 3.283 lần cắt từ 2024 (không dùng để học).**
Đường kết quả học được (khớp lời anh):
- RSI cực trị pha trước < 20,5 (vùng cam) → R −0,09 (tệ nhất); 29–49 → +0,14…+0,41. → đáy cam dễ retest/thủng.
- Pha trước quá sâu (khoảng cách > 13 điểm, 10% sâu nhất) → −0,11; sâu vừa 6,5–9,4 → +0,39…+0,59.
- WMA45 vẫn còn dốc ngược mạnh lúc cắt (chưa thu hẹp xong) → −0,07; WMA45 vừa phẳng → +0,54.
- Giá đang sát đáy biên 50 nến → +0,06 (kém); giữa/trên biên → +0,3…+0,4.
Điểm → R thật trên tập KIỂM TRA (chia 5 nhóm): nhóm điểm thấp nhất −0,17 R/lệnh (−111R); 4 nhóm còn lại +0,12…+0,25 R/lệnh. → Lợi ích chính là **loại 20–40% tín hiệu xấu**, không phải một ngưỡng cứng.
Tập kiểm tra, mỗi khung (tất cả → điểm > 0), R/lệnh: BTC H1 0,08 → 0,18; BTC H4 0,20 → 0,31; BTC D1 0,34 → 0,52; ETH H1 0,08 → 0,16; ETH H4 0,20 → 0,45; ETH D1 0,28 → 1,52 (13 lệnh).
Vốn 500 USD (lot thật, áo giáp), tất cả → điểm > 0:
| Tổ hợp | 12T | 6T | 3T | Sụt (điểm>0, 12T) |
|---|---|---|---|---|
| **ETH H4+D1** | +28 → **+320** | +49 → +536 | +37 → +313 | 20% (6T: 10%), tháng tệ 10/26 −83 |
| ETH H1+H4+D1 | −161 → +236 | −54 → +299 | −40 → +237 | 35% |
| BTC H1+H4+D1 | +737 → +436 | +716 → +661 | +180 → +91 | 31% |
| BTC H4+D1 | +87 → +83 | +108 → +86 | +67 → −6 | 17% |
Nhận xét: điểm tăng R/lệnh ở mọi mã/khung trên dữ liệu chưa học; với ETH chuyển từ lỗ/hoà sang lãi rõ. Với BTC tổng tiền giảm (ít lệnh hơn, BTC 2024–2026 lệnh nào cũng ăn) nhưng sụt giảm. Điểm học chung BTC+ETH+3 khung → ít khớp quá hơn học riêng.
Mặt xấu: 8 đặc điểm × 10 ô = nhiều tham số (nhưng 6.743 mẫu, kiểm tra ngoài mẫu ổn); tháng 10/26 ETH lỗ −83…−108; Binance ≠ Exness; chưa có nhồi lệnh.

## Vòng 24 (03/11/2026) — Bảng so CÔNG BẰNG cho ETH (anh: "mới phải tốt hơn bản cũ, tệ hơn thì code làm gì")
Script `scripts/so_sanh.py`: mọi bản chạy cùng mô phỏng vốn 500 USD (lot thật, lot min 0,1 ETH giả định, trần 4%, thua 3 nghỉ 8h), cùng giai đoạn. Dữ liệu ETH M15 từ 2022.
| Bản (ETH) | 12T | 6T | 3T | Năm 2024 | Năm 2023* |
|---|---|---|---|---|---|
| MỐC v19 RSI 55/45 H1 + H4 lọc D1 + MH3a M15 | **+1242** (sụt 33%) | **+573** | **+773** | **−31** (sụt 47%) | **−313** (sụt 65%) |
| v19 + chấm điểm (điểm > 0) | +1116 (31%) | +637 | +545 | +24 (47%) | −179 (49%) |
| v22 H4E3 + D1E1 | +204 (12%) | +84 | +114 | +35 | +4 |
| v23 H4 + D1, điểm > 0 | +320 (20%) | +217 | +324 | **+321** (16%) | **+201** (19%) |
(*2023: điểm v23 đã học trên năm này.) → v19 chỉ thắng ở 12 tháng gần (bản được chọn khi đã nhìn đoạn đó), lỗ nặng 2023–2024. v23 lãi ít hơn nhưng dương mọi giai đoạn, sụt thấp. Chưa có bản nào vừa lãi như v19 năm gần vừa bền như v23.

## Vòng 25 (03/11/2026) — Rà từng lệnh: thua đúng/sai, thắng mấy R, entry trễ, khoá lời
Script `scripts/chan_doan.py` (tín hiệu hành trình RSI, ETH H4+D1, BTC H1/H4/D1, từ 2018):
- Thắng 37–40%. Lệnh thắng ra TB 2,4–3,3R nhưng đã lên cao nhất TB 4,3–5,5R → **trả lại ~2R/lệnh**. Phần lớn lệnh thắng ra ở 1–2R (khoá lời 2R/50%).
- Thua: bị quét ≤ 3 nến 15–17%; đã lên ≥ 1R rồi thua 5–6%; còn lại thua theo luật. Lúc vào, giá đã chạy TB **2–3 ATR từ đáy/đỉnh pha trước** (EMA9 cắt WMA45 là tín hiệu muộn). SL < 1 ATR → R TB âm.
Script `scripts/thu_doi.py`, đổi từng thứ một, so gốc (khoá 2R giữ 50%), R/lệnh trước 2024 → 2024-nay, tổng 5 bộ:
| Thay đổi | Trước 2024 | 2024→nay | Giữ? |
|---|---|---|---|
| GỐC khoá 2R/50% | +0,260 (+673R) | +0,153 (+195R) | — |
| Khoá 1,5R/50% | +0,230 | +0,130 | bỏ |
| Khoá 2R/60% · 2R/70% | +0,147 · +0,071 | +0,144 · +0,066 | bỏ (cắt lệnh lớn) |
| Khoá 3R/60% | +0,208 (+520R) | +0,183 (+221R) | bỏ (tốt ở kiểm tra, kém ở học → không ổn định) |
| Khoá 3R/70% · 4R/70% | +0,101 · +0,181 | +0,115 · +0,112 | bỏ |
| Hoà vốn 1R · 1,5R | +0,196 · +0,259 | +0,099 · +0,135 | bỏ |
| SL ≥ 1 ATR · ≥ 1,5 ATR | +0,247 · +0,244 | +0,144 · +0,136 | bỏ |
| Vào sớm (RSI cắt WMA45, pha sâu ≥ 3) | +0,067 | +0,115 | bỏ |
| Vào sớm (pha sâu ≥ 5) (+SL ≥ 1 ATR) | +0,064 (+0,074) | +0,054 (+0,042) | bỏ |
Kết luận: **nền tảng hiện tại (khoá 2R/50%, SL swing, kéo SL 10) đã là tốt nhất trong các phương án thử**; trả lại ~2R là cái giá để giữ lệnh lớn. Vào sớm hơn làm kém đi nhiều (nhiều tín hiệu giả). Không đổi gì ở nền tảng.

## Vòng 26 (03/11/2026) — Vì sao mốc v19 ETH lỗ 2023–2024? Rà lệnh BÁN (anh: "thị trường càng sập càng phải kiếm")
Script `scripts/phan_tich_v19.py`, `scripts/ban_thu.py`. ETH giá năm: 2022 −67%, 2023 +91%, 2024 +46%, 2025 −11%, 2026 −24%.
R theo năm (MUA / BÁN, cộng 3 phần H1+H4+M15): 2022 +19,4 / **+26,9** · 2023 **+19,6 / −40,5** · 2024 +13,0 / −5,1 · 2025 +7,9 / +11,2 · 2026 +83,0 / +26,4.
- **Năm sập 2022 lệnh bán chỉ +27R**: bán thắng ra TB 1,5R trong khi đã đi đúng TB ~2,9R (trả lại một nửa); lệnh MUA thắng ra 2,6–3,3R.
- 2023: bán thua 173 lệnh (−162R), 72% vào lúc giá TRÊN EMA200 D1, 47% ngược phe D1. Nhưng MUA cũng chỉ +19,6R trong năm +91% → cả 2 chiều đều yếu.
- 2023 là năm ETH **biến động thấp nhất** (biên độ ngày TB 3,6% so với 5–9% các năm khác; chỉ 73 ngày > 5%) → giá nhích lên đều, ít sóng, RSI 55/45 cắt qua lại liên tục.
- BÁN H1 tổng 5 năm −14R, kể cả khi D1 phe giảm (−19,7R).
Thử sửa RIÊNG chiều BÁN (MUA giữ nguyên), R lệnh bán theo năm 2022/23/24/25/26 và USD (vốn 500 mỗi năm):
| Cách | R bán 5 năm | 2022 | 2023 | 2024 | 2025 | 2026 | USD 2022/23/24/25/26 |
|---|---|---|---|---|---|---|---|
| gốc (khoá 2R/50%) | +19 | +28 | −42 | −4 | +10 | +27 | +609 / −313 / −31 / +192 / +1242 |
| bỏ khoá lời | +28 | +24 | −51 | +3 | +20 | +32 | +246 / −322 / +24 / +242 / +1312 |
| gồng theo đỉnh 40 nến | **+51** | **+38** | −52 | +13 | +20 | +32 | +373 / −313 / −16 / +130 / +1906 |
| gồng theo đỉnh 20 nến | +19 | +21 | −61 | +1 | +22 | +35 | +272 / −365 / −215 / +69 / +1708 |
| kéo SL swing 5 | −44 | +17 | −54 | −14 | +1 | +6 | (kém) |
| chỉ bán khi giá < EMA200 D1 | +12 | +26 | −12 | +2 | −26 | +22 | +539 / −230 / +28 / −84 / +896 |
| bỏ BÁN H1 | +33 | +17 | −25 | +7 | +10 | +25 | +295 / −165 / +141 / +231 / +1098 |
Kết luận: **không cách sửa phần thoát lệnh bán nào tốt hơn gốc ở mọi năm**. "Gồng theo đỉnh 40 nến" ăn sập tốt hơn (2022 +38R so với +28R, tổng 5 năm +51R so với +19R) nhưng không cứu được 2023. Lỗ 2023 không chỉ do lệnh bán mà do tín hiệu RSI 55/45 bị nhiễu trong năm biến động thấp (cả MUA cũng yếu). Hướng tiếp: (1) bộ lọc biến động (ATR% D1 thấp → giảm/nghỉ), (2) mô-đun BÁN riêng cho lúc sập (gồng dài như bán D1 của bot A) thay vì bán đối xứng.

## Vòng 27 (03/11/2026) — Mô-đun BÁN LÚC SẬP (thay bán đối xứng)
Script `scripts/ban_sap.py` (108 cấu hình, BTC+ETH H1/H4 từ 2018), `scripts/ghep_sap.py`. Chỉ bán khi D1 giảm thật (P1 phe D1 giảm / P2 + giá dưới EMA200 D1 / P3 dưới EMA200 + EMA9(RSI D1) < WMA45), vào khi T1 EMA9(RSI) cắt xuống / T2 RSI cắt xuống 45 / T3 phá đáy 20 nến, gồng theo đỉnh cao nhất 20/40 nến (không khoá lời) hoặc nền tảng. Chọn cấu hình trên 2018–2021, kiểm tra 2022–2026.
- Tốt nhất ETH (chọn trên 2018–21): **H1, P2, RSI cắt xuống 45, gồng đỉnh 40 nến**: 2018–21 +128R (2018 sập −82%: +118R); kiểm tra 2022–26 +19,7R / 177 lệnh (bán đối xứng cũ +19R / 1.273 lệnh); 2022 +11,5R, 2023 −10,4R (cũ −42R), 2024 +0,6, 2025 +3,0, 2026 +15,0.
- BTC tốt nhất: H1 P1/P2 EMA9 cắt xuống, nền tảng: kiểm tra 22–26 +45…+48R (2026 +37R), 2023–25 âm nhẹ.
Ghép vào v19 ETH (vốn 500 USD mỗi năm):
| Bản | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | 12T gần |
|---|---|---|---|---|---|---|---|
| MỐC v19 (bán đối xứng) | **+609** | −313 (sụt 65%) | −31 | +192 | **+1242** | **+1699** | +1242 |
| v19 MUA + bán sập (RSI 45, đỉnh 40) | +148 | **−95** | +30 | +83 | +1040 | +1206 | +778 |
| v19 MUA + bán sập (EMA9 cắt, đỉnh 20) | +197 | −46 | −59 | +73 | +961 | +1126 | +651 |
| v19 đầy đủ + bán sập | +368 | −326 | −1 | +141 | +822 | +1004 | +486 |
| v19 chỉ MUA | +71 | +20 | +10 | +31 | +772 | +904 | +452 |
Kết luận: **mô-đun bán sập KHÔNG hơn mốc** về tổng tiền (+1206 so với +1699). Nó giảm lỗ năm xấu (2023: −95 so với −313) nhưng ăn ít hơn hẳn ở 2022 (+148 so với +609): sập 2022 có nhiều nhịp hồi mạnh làm mất điều kiện "D1 giảm + dưới EMA200", nên bỏ lỡ nhiều nhịp. Sập 2018 thì ăn rất tốt (+118R). Bán đối xứng của v19 vẫn đóng góp lớn ở 2022/2026 → giữ. Không đưa mô-đun vào. Lỗ 2023 nằm ở chất lượng tín hiệu trong năm biến động thấp → thử bộ lọc biến động.

## Vòng 28 (03/11/2026) — Luật BÁN của anh: BÁN H1 khi H4 vừa cắt xuống dốc mạnh; BÁN H4 khi D1 vừa cắt xuống
Lý thuyết bán cũ hỏng ở: (1) bán đối xứng không nhìn khung trên (2023: 47% lệnh bán thua ngược phe D1, 72% trên EMA200); (2) ra quá sớm (bán thắng ra 1,5R / đã đi ~2,9R); (3) mô-đun sập vòng 27 quá chặt (EMA200) → lỡ các nhịp 2022.
Script `scripts/ban_dakhung.py` (36 cấu hình/cặp/mã): "vừa cắt" = EMA9(RSI) khung trên cắt xuống WMA45 trong K = 2/4 nến gần nhất và vẫn đang dưới; "dốc" = EMA9 khung trên giảm ≥ X = 0/3/6 điểm trong 3 nến; vào = RSI cắt 45 / EMA9 khung dưới cắt / NGAY nến đầu tiên đủ điều kiện; thoát = nền tảng / gồng đỉnh 40 nến.
- **ETH BÁN H1 khi H4 vừa cắt, vào NGAY: dương ở tập kiểm tra 2022–26 trong cả 12 biến thể (K, X, thoát)** → quy luật bền. Bản gọn: K2, X0, gồng đỉnh 40: kiểm tra +75,7R/255 lệnh, năm nào cũng dương (22 +8,4 · 23 +4,8 · 24 +42,7 · 25 +10,8 · 26 +9,0); 2018–21 +31,7R (2018 +56, nhưng 2021 tăng mạnh −31,7R). Bán đối xứng cũ cùng giai đoạn +19R.
- ETH BÁN H4 khi D1 vừa cắt: yếu (2/36 cấu hình dương ở kiểm tra) → bỏ.
- BTC BÁN H1 khi H4 vừa cắt + dốc ≥ 6, vào ngay: học +14R, kiểm tra +16…+20R (ổn nhẹ).
Ghép vào v19 ETH (script `scripts/ghep_ban_moi.py`, vốn 500 USD mỗi năm):
| Bản | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | 12T gần |
|---|---|---|---|---|---|---|---|
| MỐC v19 | +609 (sụt 27%) | −313 (65%) | −31 (47%) | +192 (44%) | +1242 (35%) | +1699 | +1242 (33%) |
| **v19 MUA + BÁN M15 cũ + BÁN H1 mới** (bỏ bán H1/H4 đối xứng) | +567 (29%) | **−118 (54%)** | **+772 (36%)** | +172 (38%) | +1092 (25%) | **+2485** | +1030 (28%) |
| v19 MUA + BÁN H1 mới | +144 | +145 | +672 | +17 | +843 | +1821 | +350 |
| v19 đầy đủ + BÁN H1 mới | +644 | −332 (67%) | +478 | +235 | +1594 | +2619 | +1359 |
Kết luận: **luật bán mới HƠN mốc**: bản thay bán H1/H4 đối xứng bằng bán H1 khi H4 vừa cắt: cộng 5 năm +2485 so với +1699 (+46%), sụt vốn thấp hơn ở 4/5 năm, 2023 lỗ ít hơn (−118 so với −313), 2024 từ −31 lên +772. Đổi lại 2022 và 12 tháng gần thấp hơn chút (+567 so với +609; +1030 so với +1242). Lưu ý thiên lệch: cấu hình gọn chọn theo độ bền ở cả 12 biến thể (có nhìn tập kiểm tra), không phải chỉ theo tập học.

## Vòng 29 (03/11/2026) — Vào ÍT lệnh hơn, chọn thời điểm chất lượng (anh: "RSI yếu hơn EMA?")
Script `scripts/chat_luong.py`. Hệ gốc = hệ tốt nhất vòng 28 (v19 MUA + BÁN M15 MH3a + BÁN H1 khi H4 vừa cắt). Chấm từng tín hiệu: (a) điểm hành trình (mô hình vòng 23, học BTC+ETH trước 2024), (b) đồng thuận = số khung trên H4/D1 có EMA9(RSI) cùng chiều. Ngưỡng điểm đặt trên lệnh 2022–23; 2024→nay là ngoài mẫu. Vốn 500 USD mỗi năm.
| Bản | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | 12T |
|---|---|---|---|---|---|---|---|
| GỐC (tất cả, 2%) | +567 (sụt 29%) | −118 (54%) | +772 (36%) | +172 (38%) | +1092 (25%) | +2485 | +1030 |
| top 50% điểm, 2% | +139 | −64 | +405 | +122 | +2642 | +3244 | +1688 → hơn nhờ riêng 2026, kém gốc 4/5 năm → không bền |
| đồng thuận ≥ 1, 2% | +286 (28%) | −50 (40%) | +869 (27%) | +292 (29%) | +1682 (17%) | +3079 | +1524 → hơn gốc 4/5 năm, sụt thấp hơn mọi năm |
| top 30% điểm, 2% | +239 (14%) | +81 (28%) | +312 (16%) | +148 (23%) | +1592 (17%) | +2372 | +1431 → năm nào cũng lãi, R/lệnh gấp đôi |
| **top 30% điểm, 3%** | +322 (23%) | +126 (40%) | +447 (25%) | +85 (31%) | +2802 (27%) | **+3782** | **+2667** |
| **top 30% + đồng thuận ≥ 1, 3%** | +419 (21%) | +248 (37%) | +88 (25%) | +92 (31%) | +3012 (25%) | **+3859** | **+2817** |
| top 30% điểm, 4% | +427 (30%) | +121 (51%) | +452 (35%) | +189 (42%) | +4153 (34%) | +5342 | +3438 → sụt 51% (2023), quá rủi ro |
| đồng thuận ≥ 1, 3% | +217 (41%) | −99 (57%) | +994 | +517 | +2759 | +4388 | +2648 → sụt 57% |
Kết luận: anh đúng: **ít lệnh mà chất lượng** tốt hơn. Bản "top 30% điểm (+ đồng thuận ≥ 1 khung trên), rủi ro 3%/lệnh": năm nào cũng lãi (kể cả 2023), sụt vốn 21–40% (≤ gốc 2%), cộng 5 năm +3782…+3859 (gốc +2485, mốc v19 +1699), 12T +2667…+2817. Mặt xấu: phần lớn lãi vẫn dồn vào 2026; 2024–2025 lãi mỏng (+85…+447); ngưỡng điểm đặt trên 2022–23 (2 năm đó trong mẫu). So bot A (+4366/12T): bot A là MT5, BTC, M5→D1 + nhồi lệnh → chưa so ngang hàng.

## Vòng 30 (03/11/2026) — Rà luật MUA / BÁN của hệ ETH (vòng 29), lệnh đậm nhất bao nhiêu R
Script `scripts/ra_mua_ban.py`. ETH 2022→nay (riêng BÁN H1 tính từ 2018). Bản đang chọn = top 30% điểm.
| Phần (top 30%) | Lệnh | Thắng | R/lệnh | Thắng TB | Đậm nhất | Bỏ 3 lệnh lớn nhất |
|---|---|---|---|---|---|---|
| MUA H1 (RSI cắt lên 55) | 202 | 40% | +0,29 | 2,25R | **+21,9R** (17/08/26) | +15,8R (còn dương) |
| MUA H4 (RSI 55, phe D1 tăng) | 15 | 47% | +1,90 | 5,26R | **+29,5R** (18/08/26) | −4,3R (sống nhờ 1 lệnh) |
| MUA M15 (MH3a) | 168 | 48% | +0,37 | 1,74R | **+24,5R** (19/08/26) | +19,0R |
| BÁN M15 (MH3a) | 171 | 42% | **+0,00** | 1,24R | +7,2R (01/07/24) | **−16,2R** |
| BÁN H1 (H4 vừa cắt xuống) | 138 | 30% | **+0,63** | 4,21R | **+28,3R** (29/09/24); +20,1R (09/06/22) | +19,0R |
Tất cả tín hiệu (chưa lọc): MUA H1 +0,09R/lệnh, MUA M15 +0,09, MUA H4 +0,40 (2022–23 âm), BÁN M15 +0,04, BÁN H1 +0,23. Lọc top 30% tăng R/lệnh ở mọi phần trừ BÁN M15.
- 3 lệnh MUA đậm nhất (21,9 / 24,5 / 29,5R) cùng một sóng tăng 17–19/08/2026 → lãi 2026 dồn vào 1 sóng.
- Lệnh BÁN đậm nhất +28,7R (03/07/24, bản chưa lọc) và +28,3R (29/09/24) — luật bán H1 mới ăn được sóng giảm dài.
- BÁN M15 không có lợi thế (0R/lệnh, bỏ 3 lệnh lớn thì −16R) → thử bỏ:
| Top 30%, 3% | 2022 | 2023 | 2024 | 2025 | 2026 | Lãi kép 500 từ 2022 |
|---|---|---|---|---|---|---|
| Hiện tại | +322 | +126 | +447 | +85 | +2802 | 18.213 USD, sụt 40% |
| **Bỏ BÁN M15** | +327 | **+233** | +334 | **+278** | +2260 | **22.240 USD, sụt 38%** |
| Bỏ MUA H4 | +322 | +143 | +528 | +85 | +1488 | 12.591 USD |
Kết luận: **bỏ BÁN M15** (hơn ở 2023, 2025, lãi kép, sụt thấp hơn; kém ở 2024, 2026). Giữ MUA H4 dù ít lệnh (bỏ thì mất lệnh lớn). Luật MUA còn yếu ở MUA H1 năm 2022 (−0,17R/lệnh) và MUA H4 2022–24.

## Vòng 31 (03/11/2026, phiên cloud) — Việc 1–7 theo `VIEC-CLOUD.md`
Chi tiết + bảng số: `KET-QUA-CLOUD.md`. Script: `scripts/moc.py` (MỐC chung), `scripts/viec1_mua_dakhung.py`, `viec1b_ghep.py`, `viec2_ra_mua.py`, `viec3_nguong.py`, `viec4_phi.py`, `viec5_bien_dong.py`, `viec6_btc.py`.
- **Giữ:** MUA H1 khi H4 vừa cắt lên (K2, vào RSI H1 cắt 55, gồng đáy 40) → MỐC-1: lãi kép 500 từ 2022 → 90.792 USD (sụt 33%), MỐC vòng 30 chạy lại 23.250 (34%).
- **Bỏ:** lọc MUA theo RSI D1/phe D1; lọc biến động thấp; áp cho BTC (tương quan tháng +0,61).
- **Mặt xấu:** ngưỡng top 30% không bền; walk-forward thật từ 2023 chỉ ~10.000 USD, sụt 58%. Phí 0,1% làm lãi kép giảm ~3,5 lần. Vàng PAXG chưa làm (mạng cloud chặn Binance).
