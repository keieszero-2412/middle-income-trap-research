# Middle Income Trap Cox Models

Dự án phân tích khả năng chuyển nhóm thu nhập của các quốc gia trong giai đoạn 2000-2026 bằng Cox proportional hazards với dữ liệu counting-process.

## Chạy pipeline

Từ thư mục gốc của dự án:

```powershell
.\.venv\Scripts\python.exe data_processing\build_final_dataset.py
.\.venv\Scripts\python.exe survival_data_prep.py
.\.venv\Scripts\python.exe cox_model.py
 .\.venv\Scripts\python.exe cox_model_5vars.py
```

`main` trong `cox_model.py` dùng toàn bộ 7 biến: `TFP`, `GE`, `AGEDEP`, `IND`, `TO`, `CREDIT`, `ECI`.

Branch 5 biến trong `cox_model_5vars.py` dùng: `TFP`, `GE`, `AGEDEP`, `TO`, `CREDIT`.

Chỉ hai chuyển đổi hợp lệ được đưa vào mô hình: `LM -> UM` và `UM -> H`. Các bước nhảy `LM -> H` bị loại khỏi mẫu; `L -> UM` không được xem là event.

## Kiểm định PH

Lifelines không hỗ trợ Schoenfeld residuals cho dữ liệu có `entry` time. Mỗi branch vì vậy lưu kiểm định thay thế dựa trên tương tác `covariate x log(stop)` tại `report/ph_assumptions_*.txt` và `.csv`. p-value dưới 0.05 là dấu hiệu cần xem xét vi phạm giả định proportional hazards.
