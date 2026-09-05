# Kết quả mô hình Cox Proportional Hazards - Main

**Branch:** `main`  
**Biến:** `TFP`, `GE`, `AGEDEP`, `IND`, `TO`, `CREDIT`, `ECI`  
**Dữ liệu:** 2000-2026  
**Phương pháp:** counting-process Cox PH, robust SE clustered theo `Code`

## 1. Survival sample

| Chỉ số | Giá trị |
|---|---:|
| Quan sát | 1,404 |
| Spells | 135 |
| LM spells | 66 |
| LM events | 38 |
| UM spells | 69 |
| UM events | 26 |
| Tổng events | 64 |
| Censored | 71 |

Chỉ giữ hai transition `LM -> UM` và `UM -> H`. Các bước nhảy `LM -> H` bị loại khỏi mẫu.

## 2. Kết quả mô hình

### Combined LM + UM

| Biến | Hazard ratio | p-value |
|---|---:|---:|
| TFP | 5.63 | 0.176 |
| GE | 2.38 | 0.077 |
| AGEDEP | 0.95 | 0.015 |
| IND | 0.94 | 0.142 |
| TO | 1.00 | 0.567 |
| CREDIT | 0.99 | 0.263 |
| ECI | 2.21 | 0.081 |
| is_UM | 0.23 | 0.005 |

Concordance: `0.77`; partial AIC: `498.45`.

### LM -> UM

| Biến | Hazard ratio | p-value |
|---|---:|---:|
| TFP | 57.83 | 0.049 |
| GE | 1.50 | 0.546 |
| AGEDEP | 0.93 | 0.004 |
| IND | 0.95 | 0.244 |
| TO | 0.99 | 0.375 |
| CREDIT | 1.01 | 0.626 |
| ECI | 1.12 | 0.839 |

Concordance: `0.72`; partial AIC: `249.94`.

### UM -> H

| Biến | Hazard ratio | p-value |
|---|---:|---:|
| TFP | 2.90 | 0.662 |
| GE | 7.25 | 0.005 |
| AGEDEP | 0.95 | 0.388 |
| IND | 0.82 | 0.026 |
| TO | 1.00 | 0.955 |
| CREDIT | 0.98 | 0.094 |
| ECI | 22.01 | <0.005 |

Concordance: `0.88`; partial AIC: `151.45`.

## 3. Phân loại đã thoát và chưa thoát khỏi bẫy

Quy tắc phân loại được áp dụng riêng cho từng nhóm thu nhập:

- **Đã thoát:** spell có `event = 1` và thời gian chuyển đổi `<=` median duration của các spell đã event trong cùng nhóm.
- **Chưa thoát:** spell bị censor, hoặc spell có `event = 1` nhưng thời gian chuyển đổi **> median**.

| Nhóm | Median duration | Tổng spells | Đã thoát | Chưa thoát | Censored |
|---|---:|---:|---:|---:|---:|
| LM -> UM | 8.0 năm | 66 | 21 | 45 | 28 |
| UM -> H | 7.5 năm | 69 | 13 | 56 | 43 |

### So sánh đặc trưng giữa hai nhóm - LM -> UM

| Biến | Mean đã thoát | Mean chưa thoát | Mann-Whitney p |
|---|---:|---:|---:|
| TFP | 0.991 | 1.001 | 0.2766 |
| GE | -0.318 | -0.490 | 0.1231 |
| AGEDEP | 55.346 | 66.600 | 0.0040 |
| IND | 14.789 | 13.825 | 0.2103 |
| TO | 70.284 | 72.472 | 0.6496 |
| CREDIT | 45.960 | 34.636 | 0.0286 |
| ECI | 0.003 | -0.434 | 0.0160 |

### So sánh đặc trưng giữa hai nhóm - UM -> H

| Biến | Mean đã thoát | Mean chưa thoát | Mann-Whitney p |
|---|---:|---:|---:|
| TFP | 1.057 | 1.015 | 0.0643 |
| GE | 0.399 | -0.015 | 0.0028 |
| AGEDEP | 49.051 | 52.485 | 0.1558 |
| IND | 15.819 | 14.272 | 0.3859 |
| TO | 101.537 | 74.206 | 0.0201 |
| CREDIT | 47.630 | 53.730 | 0.5242 |
| ECI | 0.852 | 0.147 | 0.0001 |

Các p-value trên là kiểm định hai phía ở cấp spell, dùng để mô tả sự khác biệt giữa nhóm nhanh/đã thoát và nhóm chưa thoát; chúng không thay thế cho hazard ratio của mô hình Cox.

## 4. Kiểm định proportional hazards

Lifelines không hỗ trợ Schoenfeld residuals cho dữ liệu có `entry` time. Branch dùng kiểm định thay thế bằng tương tác `covariate x log(stop)`. Kết quả chi tiết nằm trong `report/ph_assumptions_*.csv` và `.txt`; chưa có bằng chứng vi phạm PH ở ngưỡng 5%.

## 5. Output

- Summary: `report/cox_summary_combined.csv`, `report/cox_summary_lm.csv`, `report/cox_summary_um.csv`
- Forest plots: `report/cox_forest_combined.png`, `report/cox_forest_lm.png`, `report/cox_forest_um.png`
- Kaplan-Meier: `report/kaplan_meier.png`
