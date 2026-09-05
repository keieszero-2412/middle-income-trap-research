# Kết quả Mô hình Cox Proportional Hazards — Bẫy Thu nhập Trung bình

**Branch:** `credit-and-to` | **Biến kiểm soát:** AGEDEP, GE, IND, TO, CREDIT
**Dữ liệu:** 161 quốc gia, giai đoạn 2000–2026 | **Phần mềm:** `lifelines` (Python)

---

## 1. Tổng quan Dữ liệu Survival

| Chỉ số | Giá trị |
|---|---|
| Tổng số quan sát (observation rows) | 2.180 |
| Tổng số giai đoạn (spells) | 159 |
| Giai đoạn ở nhóm LM | 86 (47 đã thăng hạng lên UM) |
| Giai đoạn ở nhóm UM | 73 (25 đã thăng hạng lên H) |
| **Tổng sự kiện thăng hạng (events)** | **72** |
| Tổng bị kiểm duyệt (censored) | 87 |

---

## 2. Kết quả Mô hình

### 2.1. Mô hình Tổng hợp (LM + UM) — Concordance = 0.72

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **is_UM** | -1.22 | **0.30** | **<0.005** ⭐ | Ở nhóm UM khó thăng hạng hơn LM 70% |
| **AGEDEP** | -0.05 | **0.95** | **<0.005** ⭐ | Tỷ lệ phụ thuộc tuổi cao → khó thăng hạng |
| **GE** | +1.10 | **3.00** | **<0.005** ⭐ | GE tăng 1 đơn vị → xác suất thăng hạng tăng 200% |
| **IND** | -0.02 | 0.98 | 0.19 | Không có ý nghĩa |
| **TO** | +0.00 | 1.00 | 0.93 | Không có ý nghĩa |
| **CREDIT** | -0.00 | 1.00 | 0.33 | Không có ý nghĩa |

### 2.2. Mô hình LM → UM — Concordance = 0.72

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **AGEDEP** | -0.05 | **0.95** | **<0.005** ⭐ | Tác động tiêu cực mạnh |
| **GE** | +0.73 | **2.07** | **0.01** ⭐ | Tác động tích cực có ý nghĩa |
| **IND** | -0.03 | 0.97 | 0.16 | Không có ý nghĩa |
| **TO** | -0.00 | 1.00 | 0.24 | Không có ý nghĩa |
| **CREDIT** | +0.00 | 1.00 | 0.59 | Không có ý nghĩa |

### 2.3. Mô hình UM → H — Concordance = 0.74

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **GE** | +1.63 | **5.09** | **<0.005** ⭐ | Tác động CỰC KỲ MẠNH: GE tăng 1 đơn vị → xác suất thăng hạng tăng 409%! |
| **AGEDEP** | -0.04 | 0.97 | 0.13 | Không có ý nghĩa |
| **IND** | -0.03 | 0.97 | 0.31 | Không có ý nghĩa |
| **TO** | +0.00 | 1.00 | 0.26 | Không có ý nghĩa |
| **CREDIT** | -0.01 | 0.99 | 0.09 | Không có ý nghĩa (nhưng xu hướng âm) |

---

## 3. So sánh với các Branch khác

| Chỉ số | main (TO) | credit-only | **credit-and-to** |
|---|---|---|---|
| Số quốc gia sạch | 171 | **175** | 161 |
| Sự kiện thăng hạng | 77 | **78** | 72 |
| Concordance (Combined) | 0.71 | **0.72** | **0.72** |
| Concordance (LM→UM) | 0.71 | **0.73** | 0.72 |
| Concordance (UM→H) | **0.74** | 0.72 | **0.74** |

### Phát hiện từ branch credit-and-to
> Việc thêm biến **TO** vào chung với **CREDIT** làm giảm đáng kể số lượng quốc gia trong mẫu (từ 175 xuống 161). Cả TO và CREDIT đều **không có ý nghĩa thống kê** ở mô hình có cả hai biến. Do đó, việc giữ cả hai biến không mang lại lợi ích nào lớn về mặt mô hình, nhưng lại khiến chúng ta mất đi nhiều dữ liệu của các quốc gia thăng hạng (chỉ còn 72 events).

---

## 4. Tóm tắt Kỹ thuật

| Mô hình | Concordance | AIC | Log-likelihood ratio | p-value |
|---|---|---|---|---|
| Combined (LM+UM) | 0.72 | 821.72 | 62.07 (df=6) | <0.005 |
| LM → UM | 0.72 | 451.05 | 37.45 (df=5) | <0.005 |
| UM → H | 0.74 | 250.68 | 29.20 (df=5) | <0.005 |
