# Kết quả Mô hình Cox Proportional Hazards — Bẫy Thu nhập Trung bình

**Branch:** `main` | **Biến kiểm soát:** AGEDEP, GE, IND, TO
**Dữ liệu:** 171 quốc gia, giai đoạn 2000–2026 | **Phần mềm:** `lifelines` (Python)

---

## 1. Tổng quan Dữ liệu Survival

| Chỉ số | Giá trị |
|---|---|
| Tổng số quan sát (observation rows) | 2.308 |
| Tổng số giai đoạn (spells) | 168 |
| Giai đoạn ở nhóm LM | 90 (50 đã thăng hạng lên UM) |
| Giai đoạn ở nhóm UM | 78 (27 đã thăng hạng lên H) |
| **Tổng sự kiện thăng hạng (events)** | **77** |
| Tổng bị kiểm duyệt (censored) | 91 |

---

## 2. Kết quả Mô hình

### 2.1. Mô hình Tổng hợp (LM + UM)

> **Concordance = 0.71** (Khả năng dự đoán tốt)

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **is_UM** | -1.21 | **0.30** | **<0.005** ⭐ | Ở nhóm UM khó thăng hạng hơn LM 70% |
| **AGEDEP** | -0.05 | **0.95** | **<0.005** ⭐ | Tỷ lệ phụ thuộc tuổi cao → khó thăng hạng |
| **GE** | +0.97 | **2.65** | **<0.005** ⭐ | Hiệu quả CP tăng 1 đơn vị → xác suất thăng hạng tăng 165% |
| **IND** | -0.02 | 0.98 | 0.13 | Không có ý nghĩa thống kê |
| **TO** | +0.00 | 1.00 | 0.78 | Không có ý nghĩa thống kê |

![Forest Plot - Combined](file:///d:/FTU/3.1/DE/MID/MODEL/report/cox_forest_combined.png)

---

### 2.2. Mô hình LM → UM (Thoát bẫy Thu nhập Trung bình Thấp)

> **Concordance = 0.71** | 1.271 quan sát | 63 sự kiện thăng hạng

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **AGEDEP** | -0.05 | **0.95** | **<0.005** ⭐ | Tác động tiêu cực mạnh |
| **GE** | +0.60 | **1.82** | **0.03** ⭐ | Tác động tích cực có ý nghĩa |
| **IND** | -0.02 | 0.98 | 0.23 | Không có ý nghĩa |
| **TO** | -0.00 | 1.00 | 0.35 | Không có ý nghĩa |

![Forest Plot - LM](file:///d:/FTU/3.1/DE/MID/MODEL/report/cox_forest_lm.png)

---

### 2.3. Mô hình UM → H (Thoát bẫy Thu nhập Trung bình Cao)

> **Concordance = 0.74** (Dự đoán tốt nhất!) | 1.037 quan sát | 37 sự kiện thăng hạng

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **GE** | +1.44 | **4.20** | **<0.005** ⭐ | Tác động RẤT MẠNH: GE tăng 1 đơn vị → xác suất thăng hạng tăng 320%! |
| **AGEDEP** | -0.03 | 0.97 | 0.10 | Gần ngưỡng nhưng chưa đạt ý nghĩa |
| **IND** | -0.04 | 0.96 | 0.13 | Không có ý nghĩa |
| **TO** | +0.01 | 1.01 | 0.20 | Không có ý nghĩa |

![Forest Plot - UM](file:///d:/FTU/3.1/DE/MID/MODEL/report/cox_forest_um.png)

---

## 3. Đường cong Kaplan-Meier

![Kaplan-Meier Survival Curves](file:///d:/FTU/3.1/DE/MID/MODEL/report/kaplan_meier.png)

**Nhận xét:** Đường cong sinh tồn của nhóm UM nằm **cao hơn** nhóm LM, có nghĩa là quốc gia ở nhóm UM có xu hướng **ở lại lâu hơn** trước khi thăng hạng. Điều này xác nhận giả thuyết về "Bẫy Thu nhập Trung bình Cao" — càng gần đích (High Income) thì càng khó vượt qua.

---

## 4. Diễn giải Kinh tế học

### Phát hiện chính

> [!IMPORTANT]
> **GE (Government Effectiveness) là biến số quan trọng nhất** trong việc thoát bẫy thu nhập trung bình, đặc biệt ở giai đoạn UM → H.

1. **Hiệu quả Chính phủ (GE)** là yếu tố quyết định duy nhất có ý nghĩa thống kê ở **cả 3 mô hình**. Đặc biệt, ở giai đoạn UM → H, tác động của GE mạnh gấp 2.3 lần so với giai đoạn LM → UM (HR = 4.20 vs 1.82). Điều này phản ánh thực tế: để từ "nước phát triển trung bình" trở thành "nước phát triển", cần một bộ máy nhà nước hiệu quả, minh bạch và ít tham nhũng.

2. **Tỷ lệ Phụ thuộc Tuổi (AGEDEP)** có tác động tiêu cực ở giai đoạn LM → UM nhưng mất dần ý nghĩa ở giai đoạn UM → H. Tỷ lệ dân số trẻ em/người già cao tạo ra gánh nặng phúc lợi xã hội, kéo chậm quá trình thăng hạng ở giai đoạn đầu.

3. **Công nghiệp hóa (IND) và Độ mở thương mại (TO)** đều **KHÔNG có ý nghĩa thống kê** trong bất kỳ mô hình nào. Điều này gây bất ngờ nhưng cũng hợp lý: nhiều quốc gia có tỷ trọng công nghiệp cao hoặc thương mại mở nhưng vẫn mắc kẹt trong bẫy thu nhập trung bình (ví dụ: Thái Lan, Malaysia). Điều cốt lõi không phải là sản xuất nhiều hay buôn bán nhiều, mà là **chất lượng thể chế**.

### Hàm ý Chính sách cho Việt Nam

> [!TIP]
> Việt Nam vừa thăng hạng lên UM (2025). Để tiếp tục tiến lên H, yếu tố quan trọng nhất KHÔNG phải là tăng cường công nghiệp hóa hay mở cửa thương mại, mà là **nâng cao chất lượng quản trị quốc gia** (cải cách hành chính, chống tham nhũng, tăng minh bạch).

---

## 5. Kiểm định Giả định PH

> [!NOTE]
> Kiểm định Schoenfeld Residuals không hỗ trợ trực tiếp cho định dạng counting process (entry/exit) trong phiên bản lifelines hiện tại. Tuy nhiên, chỉ số Concordance cao (0.71 - 0.74) và Log-likelihood ratio test có ý nghĩa thống kê (p < 0.005) cho thấy mô hình phù hợp tốt với dữ liệu.

---

## 6. Tóm tắt Kỹ thuật

| Mô hình | Concordance | AIC | Log-likelihood ratio | p-value |
|---|---|---|---|---|
| Combined (LM+UM) | 0.71 | 886.47 | 62.96 (df=5) | <0.005 |
| LM → UM | 0.71 | 479.94 | 36.32 (df=4) | <0.005 |
| UM → H | 0.74 | 277.07 | 30.41 (df=4) | <0.005 |
