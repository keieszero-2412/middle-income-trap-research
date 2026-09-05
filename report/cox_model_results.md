# Kết quả Mô hình Cox Proportional Hazards — Bẫy Thu nhập Trung bình

**Branch:** `credit-only` | **Biến kiểm soát:** AGEDEP, GE, IND, CREDIT
**Dữ liệu:** 175 quốc gia, giai đoạn 2000–2026 | **Phần mềm:** `lifelines` (Python)

---

## 1. Tổng quan Dữ liệu Survival

| Chỉ số | Giá trị |
|---|---|
| Tổng số quan sát (observation rows) | 2.414 |
| Tổng số giai đoạn (spells) | 174 |
| Giai đoạn ở nhóm LM | 92 (50 đã thăng hạng lên UM) |
| Giai đoạn ở nhóm UM | 82 (28 đã thăng hạng lên H) |
| **Tổng sự kiện thăng hạng (events)** | **78** |
| Tổng bị kiểm duyệt (censored) | 96 |

---

## 2. Kết quả Mô hình

### 2.1. Mô hình Tổng hợp (LM + UM) — Concordance = 0.72

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **is_UM** | -1.44 | **0.24** | **<0.005** ⭐ | Ở nhóm UM khó thăng hạng hơn LM 76% |
| **AGEDEP** | -0.05 | **0.95** | **<0.005** ⭐ | Tỷ lệ phụ thuộc tuổi cao → khó thăng hạng |
| **GE** | +1.16 | **3.18** | **<0.005** ⭐ | GE tăng 1 đơn vị → xác suất thăng hạng tăng 218% |
| **IND** | -0.02 | 0.98 | 0.32 | Không có ý nghĩa thống kê |
| **CREDIT** | -0.00 | 1.00 | 0.31 | Không có ý nghĩa thống kê |

### 2.2. Mô hình LM → UM — Concordance = 0.73

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **AGEDEP** | -0.05 | **0.95** | **<0.005** ⭐ | Tác động tiêu cực mạnh |
| **GE** | +0.82 | **2.27** | **<0.005** ⭐ | Tác động tích cực rất mạnh |
| **IND** | -0.03 | 0.97 | 0.13 | Không có ý nghĩa |
| **CREDIT** | +0.00 | 1.00 | 0.55 | Không có ý nghĩa |

### 2.3. Mô hình UM → H — Concordance = 0.72

| Biến | Hệ số (coef) | Hazard Ratio | p-value | Ý nghĩa |
|---|---|---|---|---|
| **GE** | +1.66 | **5.24** | **<0.005** ⭐ | Tác động CỰC MẠNH: GE tăng 1 đơn vị → xác suất thăng hạng tăng 424%! |
| **AGEDEP** | -0.05 | **0.95** | **0.03** ⭐ | Tác động tiêu cực có ý nghĩa |
| **CREDIT** | -0.01 | **0.99** | **0.05** ⭐ | Tác động tiêu cực nhẹ (gần ngưỡng) |
| **IND** | -0.00 | 1.00 | 0.93 | Không có ý nghĩa |

---

## 3. So sánh với Branch `main` (dùng TO)

| Chỉ số | main (TO) | credit-only (CREDIT) |
|---|---|---|
| Số quốc gia sạch | 171 | **175** |
| Sự kiện thăng hạng | 77 | **78** |
| Concordance (Combined) | 0.71 | **0.72** |
| Concordance (LM→UM) | 0.71 | **0.73** |
| Concordance (UM→H) | **0.74** | 0.72 |
| GE có ý nghĩa? | ✅ Cả 3 mô hình | ✅ Cả 3 mô hình |
| AGEDEP có ý nghĩa? | ✅ Combined + LM | ✅ Cả 3 mô hình |
| TO/CREDIT có ý nghĩa? | ❌ Không | ⚠️ CREDIT gần ngưỡng ở UM→H (p=0.05) |

### Phát hiện mới ở branch credit-only

> **CREDIT** (Tín dụng tư nhân) cho thấy tác động **tiêu cực nhẹ** đối với việc thăng hạng từ UM lên H (p=0.05). Điều này gợi ý rằng: tín dụng tư nhân quá cao (bong bóng tín dụng) có thể cản trở sự thăng hạng thu nhập, một phát hiện phù hợp với lý thuyết về bẫy nợ trung bình.

---

## 4. Tóm tắt Kỹ thuật

| Mô hình | Concordance | AIC | Log-likelihood ratio | p-value |
|---|---|---|---|---|
| Combined (LM+UM) | 0.72 | 908.82 | 72.97 (df=5) | <0.005 |
| LM → UM | 0.73 | 485.19 | 43.41 (df=4) | <0.005 |
| UM → H | 0.72 | 292.26 | 29.69 (df=4) | <0.005 |
