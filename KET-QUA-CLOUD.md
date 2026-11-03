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

## Việc 2 — Rà lệnh MUA thua (MỐC-1, top 30%)
Script `scripts/viec2_ra_mua.py`. Bối cảnh lấy từ nến D1/H4 đã đóng lúc vào lệnh.
**R lệnh MUA theo năm × phần:**
| Năm | MUA H1 cũ | MUA H4 | MUA M15 | MUA H1 mới (việc 1) | Tổng MUA |
|---|---|---|---|---|---|
| 2022 (−67%) | 27L **−4,7R** | 2L 0 | 38L +14,4 | 1L −1,1 | 68L +8,6R (+0,13/l) |
| 2023 (+91%) | 47L +16,7 | 4L +0,1 | 32L **−3,0** | 9L +9,7 | 92L +23,5 |
| 2024 | 55L +12,6 | 2L −2,0 | 27L +2,2 | 9L +22,5 | 93L +35,3 |
| 2025 | 35L +19,7 | – | 44L +10,9 | 6L +26,0 | 85L +56,7 |
| 2026 | 32L +17,3 | 7L +30,5 | 29L +38,7 | 6L +9,0 | 74L +95,5 |
**Loại thua:** quét nhanh ≤ 3 nến 3–17%, vào trễ (giá đã chạy > 2 ATR) 9–25%, có lãi ≥ 1R rồi thua 4–29% (2026 cao nhất), còn lại 44–68% thua đúng luật. SL hẹp < 0,5 ATR: 0%. Năm 2022: 92% lệnh MUA thua ở dưới EMA200 D1, 55% ngược phe D1. Lệnh thắng 2022 ra TB 1,47R trong khi đã lên TB 2,83R (trả lại 1 nửa, giống bán 2022).
**Bối cảnh (R/lệnh) — 2022–23 dùng để chọn | 2024–26 kiểm tra:**
| Bối cảnh lúc MUA | 2022–23 | 2024–26 |
|---|---|---|
| RSI D1 < 45 | 60L −0,01 | 75L +0,10 |
| **RSI D1 45–60** | 67L **+0,45** | 115L **+1,57** |
| RSI D1 ≥ 60 | 33L +0,09 | 62L −0,01 |
| phe D1 giảm | 66L +0,08 | 86L +0,21 |
| giá dưới EMA200 D1 | 84L +0,24 | 119L +0,81 (không phải nguyên nhân) |
| giá cách EMA20 D1 > 8% | 18L −0,28 | 33L +0,25 |
→ Đề xuất: lọc MUA theo RSI D1 (bỏ khi RSI D1 thấp hoặc quá cao), hoặc bỏ MUA khi phe D1 giảm / giá kéo xa EMA20.
**Kiểm chứng (chỉ lọc lệnh MUA):**
| Bản | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | Lãi kép 500 từ 2022 (sụt) | Lệnh |
|---|---|---|---|---|---|---|---|---|
| MỐC-1 | +256 (27%) | +446 (33%) | +884 (25%) | +750 (29%) | +2865 (25%) | +5201 | 90.792 (33%) | 491 |
| bỏ MUA khi RSI D1 < 45 | +219 (18%) | +514 (28%) | +422 (30%) | +1180 (23%) | +3212 (21%) | +5547 | 78.213 (33%) | 358 |
| bỏ MUA khi RSI D1 < 40 | +144 (23%) | +511 (30%) | +814 (28%) | +1330 (24%) | +3226 (19%) | +6025 | 110.303 (30%) | 409 |
| bỏ MUA khi RSI D1 < 50 | +90 (17%) | +490 (25%) | +138 (30%) | +1464 (19%) | +2591 (19%) | +4773 | 40.625 (34%) | 295 |
| chỉ MUA khi RSI D1 45–60 | +228 (16%) | +500 (28%) | +566 (20%) | +858 (23%) | +4033 (18%) | +6185 | 92.520 (29%) | 267 |
| chỉ MUA khi RSI D1 45–65 | +194 (16%) | +500 (28%) | +447 (28%) | +858 (23%) | +3348 (21%) | +5347 | 60.088 (31%) | 307 |
| bỏ MUA khi phe D1 giảm | +177 (19%) | +427 (29%) | +328 (22%) | +1334 (19%) | +3213 (21%) | +5479 | 71.043 (29%) | 344 |
| bỏ MUA khi giá cách EMA20 D1 > 8% | +237 (26%) | +670 (32%) | +953 (24%) | +496 (29%) | +2998 (25%) | +5354 | 87.581 (33%) | 444 |
**Kết luận việc 2: BỎ (không đưa vào MỐC).** Không bộ lọc nào hơn MỐC-1 một cách bền: "RSI D1 < 40" lãi kép cao hơn (110k) nhưng lân cận < 45 / < 50 lại kém hơn mốc (78k / 41k) → điểm may; kém mốc năm 2022 và 2024. "Chỉ MUA khi RSI D1 45–60" **giảm sụt vốn ở cả 5 năm** (16–28% so với 25–33%), lãi kép ngang (92,5k), nhưng cắt 46% số lệnh, kém năm 2022/2024, lân cận 45–65 kém mốc → để làm **phương án phòng thủ** nếu anh ưu tiên sụt thấp, chưa phải bản chính. Điểm yếu MUA H1 năm 2022 là "thua đúng luật" trong năm sập (không phải vào trễ / SL hẹp) → không sửa bằng lọc đơn giản được; phần BÁN H1 đã bù năm đó.

## Việc 3 — Độ bền ngưỡng chất lượng (MỐC-1)
Script `scripts/viec3_nguong.py`.
**A. Tỉ lệ giữ (ngưỡng đặt trên lệnh 2022–23, mô hình điểm học trước 2024 như MỐC):**
| Giữ | 2022 | 2023 | 2024 | 2025 | 2026 | Cộng 5 năm | Lãi kép 500 từ 2022 (sụt) | Lệnh |
|---|---|---|---|---|---|---|---|---|
| top 20% | **−136** (37%) | +221 (39%) | +1013 (21%) | +284 (27%) | +2543 (16%) | +3925 | 16.471 (46%) | 341 |
| top 25% | **−172** (40%) | +286 (30%) | +927 (26%) | +227 (29%) | +2502 (20%) | +3770 | 12.893 (45%) | 432 |
| **top 30% (MỐC-1)** | +256 (27%) | +446 (33%) | +884 (25%) | +750 (29%) | +2865 (25%) | +5201 | **90.792 (33%)** | 491 |
| top 35% | +311 (31%) | +130 (48%) | +817 (27%) | +676 (36%) | +6469 (24%) | +8403 | 123.157 (**49%**) | 564 |
| top 40% | +241 (33%) | +52 (56%) | +733 (30%) | +519 (36%) | +4971 (29%) | +6516 | 64.695 (57%) | 632 |
| top 50% | +55 (38%) | +47 (62%) | +691 (40%) | +197 (52%) | +5082 (34%) | +6072 | 30.226 (64%) | 785 |
**B. Walk-forward thật (mỗi năm Y học lại mô hình điểm trên dữ liệu < Y và đặt ngưỡng trên lệnh 2022…Y−1; 2022 không có năm trước nên không tính):**
| Bản | 2023 | 2024 | 2025 | 2026 | Cộng 4 năm | Lãi kép 500 từ 2023 (sụt) | Lệnh |
|---|---|---|---|---|---|---|---|
| WF top 25% | +73 (48%) | +927 (26%) | +70 (33%) | +2417 (26%) | +3487 | 10.057 (48%) | 398 |
| WF top 30% | +46 (**58%**) | +884 (25%) | +51 (34%) | +3062 (21%) | +4043 | 10.069 (58%) | 457 |
| WF top 35% | +205 (49%) | +817 (27%) | +25 (43%) | +5286 (19%) | +6333 | 19.844 (49%) | 526 |
| MỐC-1 (ngưỡng cố định) | +446 (33%) | +884 (25%) | +750 (29%) | +2865 (25%) | +4945 | 55.320 (33%) | 410 |
| Không lọc điểm (tất cả) | +42 (69%) | +1632 (42%) | +59 (58%) | +2311 (43%) | +4044 | 13.559 (69%) | 1236 |
**Kết luận việc 3 (mặt xấu quan trọng):** ngưỡng chất lượng **KHÔNG bền**. Đổi top 30% → 25% làm 2022 từ lãi thành lỗ; 35% lãi nhiều hơn nhưng sụt 49%. Khi làm walk-forward thật, năm 2023 chỉ +46 USD với sụt 58% (MỐC +446 / 33%) và 2025 chỉ +51 (MỐC +750) → **kết quả đẹp của MỐC ở 2023 có phần do mô hình điểm đã học trên chính năm 2023** (học trước 2024), và năm 2025 nhạy với ngưỡng. Kỳ vọng thực tế nên lấy theo dòng WF: lãi kép từ 2023 ~10.000 USD với sụt ~58%, không phải 55.000 / 33%. Lọc điểm vẫn giảm sụt so với không lọc (58% so với 69%) nhưng lợi nhuận tương đương. **Không đổi MỐC** (giữ top 30% cố định để so các việc sau), nhưng **không nên tin con số lãi kép của MỐC** khi quyết định tiền thật; nếu chạy thật nên cân nhắc rủi ro thấp hơn 3%.
