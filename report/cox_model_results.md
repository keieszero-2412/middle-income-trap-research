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

## 3. Kiểm định proportional hazards

Lifelines không hỗ trợ Schoenfeld residuals cho dữ liệu có `entry` time. Branch dùng kiểm định thay thế bằng tương tác `covariate x log(stop)`. Kết quả chi tiết nằm trong `report/ph_assumptions_*.csv` và `.txt`; chưa có bằng chứng vi phạm PH ở ngưỡng 5%.

## 4. Output

- Summary: `report/cox_summary_combined.csv`, `report/cox_summary_lm.csv`, `report/cox_summary_um.csv`
- Forest plots: `report/cox_forest_combined.png`, `report/cox_forest_lm.png`, `report/cox_forest_um.png`
- Kaplan-Meier: `report/kaplan_meier.png`
