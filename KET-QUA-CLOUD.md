# KẾT QUẢ PHIÊN CLOUD (03/11/2026) — hệ B (ETH, RSI)

## TÓM TẮT
(viết khi xong các việc)

## Cách so
- Script chung `scripts/moc.py`: dựng MỐC vòng 30 (MUA H1 RSI 55 + MUA H4 lọc D1 + MUA M15 MH3a + BÁN H1 khi H4 vừa cắt xuống, top 30% điểm, rủi ro 3%, trần lot min 6%, thua 3 nghỉ 8h), đánh giá bằng `von500.mo_phong`: mỗi năm 500 USD (lãi, sụt) + lãi kép 500 từ 01/2022.
- Chạy lại MỐC với dữ liệu hiện có (tới 02/11/2026): **lãi kép 500 → 23.250 USD, sụt 34%** (vòng 30 ghi 22.240 / 38%; lệch nhẹ do ngưỡng điểm tính lại trên bộ lệnh không có BÁN M15). Ngưỡng điểm top 30% giữ nguyên của MỐC cho mọi bản thử (lệnh mới không được dùng để đặt ngưỡng).

## Việc 1 — Luật MUA đối xứng luật bán mới (H4 vừa có EMA9(RSI) cắt LÊN WMA45)
Script `scripts/viec1_mua_dakhung.py` (36 cấu hình/mã: K 2/4, dốc X 0/3/6, vào ngay / RSI H1 cắt lên 55 / EMA9 H1 cắt, thoát nền tảng NT / gồng đáy 40 G40), `scripts/viec1b_ghep.py`.
**A. R lệnh MUA H1 ETH, chọn trên 2018–21, kiểm tra 2022–26:**
| Cấu hình | Học 18–21 | Kiểm tra 22–26 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|
| **K2 X0, vào RSI cắt 55, G40** (tốt nhất R/lệnh tập học) | 70L +55,7R (+0,80/l) | 86L +70,6R (+0,82/l) | −1,6 | +5,2 | +16,8 | +19,4 | +30,8 |
| K4 X0, RSI 55, G40 (lân cận) | 120L +33,6R | 137L +67,2R | +3,7 | +14,7 | +12,6 | +12,5 | +23,7 |
| K2 X0, RSI 55, NT (lân cận) | 70L +25,1R | 87L +32,6R | −3,7 | +6,2 | +15,2 | +2,6 | +12,3 |
| K2 X0, vào ngay, G40 (tổng R học lớn nhất) | 208L +103R | 259L +84R | +15,7 | +44,8 | +14,6 | +23,0 | **−13,8** |
| K2 X3 (dốc ≥3), RSI 55, G40 | 25L +15R | 31L +31R (2026 +36,6; các năm khác âm) | | | | | |
- Vào theo EMA9 H1 cắt: ít lệnh, tập học âm → bỏ. Dốc X 6: quá ít lệnh. BTC: K4 X0 RSI 55 G40 học +38R / kiểm tra +84R (cũng dương).

**B. Ghép vào MỐC (vốn 500 USD/năm; top 30% điểm; 3%):**
| Bản | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | Lãi kép 500 từ 2022 (sụt) | Lệnh |
|---|---|---|---|---|---|---|---|---|
| MỐC vòng 30 | +257 (27%) | +257 (34%) | +331 (26%) | +387 (24%) | +2260 (25%) | +3492 | 23.250 (34%) | 464 |
| **THÊM K2 X0 RSI55 G40, bỏ lệnh MUA H1 cũ trùng nến (4 lệnh)** | +256 (27%) | **+446** (33%) | **+884** (25%) | **+750** (29%) | **+2865** (25%) | **+5201** | **90.792 (33%)** | 491 |
| THÊM K2 X0 RSI55 G40 (cho trùng, gấp đôi rủi ro) | +244 | +492 | +854 | +750 | +2763 | +5103 | 82.994 (33%) | 494 |
| THAY MUA H1 cũ bằng K2 X0 RSI55 G40 | +327 (23%) | +173 (29%) | +624 (14%) | +391 (25%) | +2764 (21%) | +4279 | 33.411 (31%) | 303 |
| Lân cận: THÊM K4 X0 RSI55 G40 (không trùng) | +370 | +439 | +824 | +645 | +2735 | +5013 | 93.730 (37%) | 509 |
| Lân cận: THÊM K2 X0 RSI55 NT (không trùng) | +256 | +557 (27%) | +648 | +437 | +3069 | +4967 | 63.552 (29%) | 492 |
| THÊM K2 X0 vào ngay G40 | +129 (37%) | +1151 (42%) | +738 | +333 | +2224 | +4575 | 68.399 (46%) | 548 |
| Đối chiếu: MỐC rủi ro 3,5% | +334 | +351 | +353 | +473 | +2603 | +4114 | 34.250 (39%) | 464 |

**Kết luận việc 1: GIỮ** — thêm "MUA H1 khi H4 vừa cắt lên (K2, không đòi dốc), vào lúc RSI H1 cắt lên 55, gồng theo đáy thấp nhất 40 nến", lọc top 30% như cũ, lệnh MUA H1 cũ cùng nến thì bỏ. HƠN MỐC 4/5 năm (2022 hoà), sụt bằng/thấp hơn trừ 2025 (29% so với 24%), lãi kép gấp ~3,9 lần. Lân cận (K4, thoát NT) đều hơn mốc → quy luật bền, không phải 1 điểm may. Tăng rủi ro MỐC lên 3,5% không đạt được như vậy → lợi thế không chỉ do thêm rủi ro.
Mặt xấu: chỉ **32 lệnh thêm trong 5 năm** (top 30%); 2022 luật mới vẫn thua (2 lệnh, −1,05R/lệnh) → **chưa sửa được điểm yếu MUA năm 2022**; lãi kép tăng mạnh vì lãi kép khuếch đại vài lệnh lớn (R/lệnh 2025 +4,3R từ 6 lệnh). "Vào ngay" có R học lớn hơn nhưng 2026 âm và sụt 42–46% → bỏ.
→ **MỐC-1** (dùng cho các việc sau) = MỐC + luật này (`xay(..., them_mua=True)` + `chon()` trong `scripts/moc.py`): **lãi kép 90.792 USD, sụt 33%**.
