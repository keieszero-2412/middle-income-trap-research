# BÁO CÁO THỰC TRẠNG DỮ LIỆU KHUYẾT (CHỈ TÍNH NHÓM QUỐC GIA CÓ SỰ THAY ĐỔI THU NHẬP)
**Tổng số quốc gia thăng hạng được phân tích:** 139 quốc gia
**Tổng số dòng dữ liệu (Quan sát):** 3753 dòng (Mỗi quốc gia 27 năm từ 2000-2026)

## 1. SO SÁNH TỶ LỆ KHUYẾT THEO BIẾN (TRƯỚC & SAU NỘI SUY)
| Biến số | Trước nội suy (Số ô khuyết) | Trước nội suy (%) | Sau nội suy (Số ô khuyết) | Sau nội suy (%) | Hiệu quả cứu dữ liệu |
|---|---|---|---|---|---|
| **TO** | 860 | 22.92% | 432 | 11.51% | Cứu được 428 ô |
| **IND** | 613 | 16.33% | 216 | 5.76% | Cứu được 397 ô |
| **GE** | 587 | 15.64% | 108 | 2.88% | Cứu được 479 ô |
| **AGEDEP** | 303 | 8.07% | 27 | 0.72% | Cứu được 276 ô |
| **IncomeGroup** | 79 | 2.10% | 79 | 2.10% | *(Không nội suy)* |

## 2. NĂM NÀO BỊ THIẾU DỮ LIỆU NHIỀU NHẤT? (TRƯỚC NỘI SUY)
*(Bảng dưới liệt kê top 5 năm bị khuyết nhiều nhất)*

| Năm | Tỷ lệ khuyết trung bình (%) |
|---|---|
| 2026 | 80.14% |
| 2025 | 66.19% |
| 2001 | 29.21% |
| 2000 | 12.52% |
| 2002 | 11.08% |

## 3. DANH SÁCH QUỐC GIA BỊ LOẠI BỎ (SAU NỘI SUY)
Dù đã cố gắng nội suy để vớt vát dữ liệu, vẫn có một số quốc gia bị loại bỏ hoàn toàn do **KHUYẾT TRẮNG (Missing 100%)** một biến số nào đó trong suốt 27 năm. Dưới đây là danh sách chi tiết các quốc gia có thăng hạng nhưng buộc phải loại bỏ khỏi mô hình Cox.

**Tổng số quốc gia bị loại:** 27 quốc gia (Còn lại 112 quốc gia sạch 100% để chạy mô hình).

| Mã Quốc Gia | Các biến bị khuyết hoàn toàn (Nguyên nhân loại bỏ) |
|---|---|
| **ANT** | AGEDEP, IND, TO |
| **ASM** | IND |
| **BGR** | IND |
| **BRB** | TO |
| **DMA** | TO |
| **FJI** | TO |
| **GIB** | GE, IND, TO |
| **GRD** | TO |
| **GUM** | IND |
| **IMN** | GE, TO |
| **JAM** | TO |
| **KNA** | TO |
| **LCA** | TO |
| **MMR** | TO |
| **MNP** | GE, IND |
| **NCL** | GE |
| **NGA** | TO |
| **NRU** | IND |
| **SSD** |  |
| **STP** | TO |
| **TLS** |  |
| **TTO** | TO |
| **TUV** | TO |
| **VCT** | TO |
| **VEN** |  |
| **XKX** |  |
| **YEM** | IND |
