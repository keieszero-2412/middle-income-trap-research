# Phạm vi nghiên cứu và tình trạng thoát bẫy thu nhập

**Ngày tạo:** 2026-09-06  
**Nguồn:** `survival_data.csv` của branch `main`  
**Đơn vị phân tích:** spell quốc gia trong một nhóm thu nhập

## 1. Phạm vi nghiên cứu

| Khía cạnh | Phạm vi |
|---|---|
| Không gian | Các quốc gia có đủ dữ liệu cho bộ biến main và xuất hiện trong survival sample |
| Thời gian | 2000-2026, tối đa 27 năm mỗi quốc gia |
| Hiện tượng | Thời gian thoát khỏi nhóm thu nhập trung bình |
| Chặng 1 | `LM -> UM`, thoát nhóm thu nhập trung bình thấp |
| Chặng 2 | `UM -> H`, thoát nhóm thu nhập trung bình cao |
| Loại khỏi event | `LM -> H` bị loại; `L -> UM` không được xem là event |
| Main variables | `TFP, GE, AGEDEP, IND, TO, CREDIT, ECI` |
| Branch 5-vars | `TFP, GE, AGEDEP, TO, CREDIT` |

## 2. Quy tắc phân loại

- **Đã thoát:** spell có `event = 1` và duration `<=` median duration của các spell có event trong cùng chặng.
- **Chưa thoát:** spell bị censor, hoặc có event nhưng duration `>` median của cùng chặng.
- Median được tính riêng cho LM và UM, không gộp hai chặng.
- “Chưa thoát” bao gồm cả quốc gia bị censor, nên không đồng nghĩa với khẳng định quốc gia đó vĩnh viễn không thể thoát bẫy.

## 3. Thống kê tổng quát

| Chỉ số | Giá trị |
|---|---:|
| Số quốc gia trong survival sample | 71 |
| Số spells | 135 |
| Số event hợp lệ | 64 |
| Số spell censored | 71 |

| Chặng | Median (năm) | Spells | Event | Censored | Đã thoát | Chưa thoát |
|---|---:|---:|---:|---:|---:|---:|
| LM -> UM | 8.0 | 66 | 38 | 28 | 21 | 45 |
| UM -> H | 7.5 | 69 | 26 | 43 | 13 | 56 |

## 4. Danh sách quốc gia: LM -> UM

### Đã thoát

| Quốc gia | Giai đoạn quan sát | Duration (năm) | Event |
|---|---|---:|---|
| ALB | 2011-2011 | 1.0 | Có |
| JOR | 2016-2016 | 1.0 | Có |
| LTU | 2000-2000 | 1.0 | Có |
| LVA | 2000-2000 | 1.0 | Có |
| IDN | 2020-2021 | 2.0 | Có |
| IRN | 2020-2022 | 3.0 | Có |
| JOR | 2022-2024 | 3.0 | Có |
| TUR | 2001-2003 | 3.0 | Có |
| ZAF | 2001-2003 | 3.0 | Có |
| BRA | 2002-2005 | 4.0 | Có |
| RUS | 2000-2003 | 4.0 | Có |
| ROU | 2000-2004 | 5.0 | Có |
| KAZ | 2000-2005 | 6.0 | Có |
| LKA | 2019-2024 | 6.0 | Có |
| AGO | 2004-2010 | 7.0 | Có |
| MNG | 2007-2013 | 7.0 | Có |
| COL | 2000-2007 | 8.0 | Có |
| DOM | 2000-2007 | 8.0 | Có |
| MNG | 2015-2022 | 8.0 | Có |
| NAM | 2000-2007 | 8.0 | Có |
| PER | 2000-2007 | 8.0 | Có |

### Chưa thoát

| Quốc gia | Giai đoạn quan sát | Duration (năm) | Event |
|---|---|---:|---|
| MRT | 2010-2010 | 1.0 | Không |
| TGO | 2025-2026 | 2.0 | Không |
| NAM | 2024-2026 | 3.0 | Không |
| TJK | 2014-2016 | 3.0 | Không |
| ZMB | 2022-2026 | 5.0 | Không |
| SEN | 2009-2014 | 6.0 | Không |
| TJK | 2020-2026 | 7.0 | Không |
| BEN | 2019-2026 | 8.0 | Không |
| TZA | 2019-2026 | 8.0 | Không |
| ALB | 2000-2008 | 9.0 | Có |
| IRN | 2000-2008 | 9.0 | Có |
| SEN | 2018-2026 | 9.0 | Không |
| ZWE | 2018-2026 | 9.0 | Không |
| CHN | 2000-2009 | 10.0 | Có |
| ECU | 2000-2009 | 10.0 | Có |
| JOR | 2000-2009 | 10.0 | Có |
| THA | 2000-2009 | 10.0 | Có |
| TUN | 2000-2009 | 10.0 | Có |
| AGO | 2016-2026 | 11.0 | Không |
| ZMB | 2010-2020 | 11.0 | Không |
| IRQ | 2000-2011 | 12.0 | Có |
| SDN | 2007-2018 | 12.0 | Không |
| TUN | 2015-2026 | 12.0 | Không |
| KEN | 2014-2026 | 13.0 | Không |
| KGZ | 2013-2026 | 14.0 | Không |
| PRY | 2000-2013 | 14.0 | Có |
| ARM | 2002-2016 | 15.0 | Có |
| MDA | 2005-2019 | 15.0 | Có |
| MRT | 2012-2026 | 15.0 | Không |
| IDN | 2003-2018 | 16.0 | Có |
| GTM | 2000-2016 | 17.0 | Có |
| LAO | 2010-2026 | 17.0 | Không |
| LKA | 2000-2017 | 18.0 | Có |
| CIV | 2008-2026 | 19.0 | Không |
| IND | 2007-2026 | 20.0 | Không |
| UKR | 2002-2022 | 21.0 | Có |
| CMR | 2005-2026 | 22.0 | Không |
| NIC | 2005-2026 | 22.0 | Không |
| SLV | 2000-2021 | 22.0 | Có |
| PHL | 2000-2024 | 25.0 | Có |
| BOL | 2000-2026 | 27.0 | Không |
| EGY | 2000-2026 | 27.0 | Không |
| HND | 2000-2026 | 27.0 | Không |
| MAR | 2000-2026 | 27.0 | Không |
| SWZ | 2000-2026 | 27.0 | Không |

## 4. Danh sách quốc gia: UM -> H

### Đã thoát

| Quốc gia | Giai đoạn quan sát | Duration (năm) | Event |
|---|---|---:|---|
| BHR | 2000-2000 | 1.0 | Có |
| HRV | 2016-2016 | 1.0 | Có |
| KOR | 2000-2000 | 1.0 | Có |
| PAN | 2020-2020 | 1.0 | Có |
| ROU | 2020-2020 | 1.0 | Có |
| ARG | 2015-2016 | 2.0 | Có |
| HUN | 2012-2013 | 2.0 | Có |
| LVA | 2010-2011 | 2.0 | Có |
| SAU | 2000-2003 | 4.0 | Có |
| CZE | 2000-2005 | 6.0 | Có |
| EST | 2000-2005 | 6.0 | Có |
| HUN | 2000-2006 | 7.0 | Có |
| SVK | 2000-2006 | 7.0 | Có |

### Chưa thoát

| Quốc gia | Giai đoạn quan sát | Duration (năm) | Event |
|---|---|---:|---|
| IDN | 2019-2019 | 1.0 | Không |
| LKA | 2018-2018 | 1.0 | Không |
| MNG | 2014-2014 | 1.0 | Không |
| TUR | 2000-2000 | 1.0 | Không |
| ZAF | 2000-2000 | 1.0 | Không |
| ALB | 2009-2010 | 2.0 | Không |
| BRA | 2000-2001 | 2.0 | Không |
| JOR | 2025-2026 | 2.0 | Không |
| LKA | 2025-2026 | 2.0 | Không |
| PHL | 2025-2026 | 2.0 | Không |
| IRN | 2023-2026 | 4.0 | Không |
| MNG | 2023-2026 | 4.0 | Không |
| UKR | 2023-2026 | 4.0 | Không |
| AGO | 2011-2015 | 5.0 | Không |
| IDN | 2022-2026 | 5.0 | Không |
| JOR | 2017-2021 | 5.0 | Không |
| SLV | 2022-2026 | 5.0 | Không |
| TUN | 2010-2014 | 5.0 | Không |
| JOR | 2010-2015 | 6.0 | Không |
| MDA | 2020-2026 | 7.0 | Không |
| MUS | 2020-2026 | 7.0 | Không |
| HRV | 2000-2007 | 8.0 | Có |
| LVA | 2001-2008 | 8.0 | Có |
| RUS | 2004-2011 | 8.0 | Có |
| RUS | 2015-2022 | 8.0 | Có |
| ARG | 2018-2026 | 9.0 | Không |
| POL | 2000-2008 | 9.0 | Có |
| ARM | 2017-2026 | 10.0 | Không |
| GTM | 2017-2026 | 10.0 | Không |
| IRN | 2009-2019 | 11.0 | Không |
| LTU | 2001-2011 | 11.0 | Có |
| CHL | 2000-2011 | 12.0 | Có |
| URY | 2000-2011 | 12.0 | Có |
| PRY | 2014-2026 | 13.0 | Không |
| ARG | 2000-2013 | 14.0 | Có |
| ROU | 2005-2018 | 14.0 | Có |
| ALB | 2012-2026 | 15.0 | Không |
| IRQ | 2012-2026 | 15.0 | Không |
| NAM | 2008-2023 | 16.0 | Không |
| CHN | 2010-2026 | 17.0 | Không |
| ECU | 2010-2026 | 17.0 | Không |
| PAN | 2000-2016 | 17.0 | Có |
| THA | 2010-2026 | 17.0 | Không |
| COL | 2008-2026 | 19.0 | Không |
| DOM | 2008-2026 | 19.0 | Không |
| MUS | 2000-2018 | 19.0 | Có |
| PER | 2008-2026 | 19.0 | Không |
| BRA | 2006-2026 | 21.0 | Không |
| KAZ | 2006-2026 | 21.0 | Không |
| TUR | 2004-2026 | 23.0 | Không |
| ZAF | 2004-2026 | 23.0 | Không |
| CRI | 2000-2023 | 24.0 | Có |
| BWA | 2000-2026 | 27.0 | Không |
| GAB | 2000-2026 | 27.0 | Không |
| MEX | 2000-2026 | 27.0 | Không |
| MYS | 2000-2026 | 27.0 | Không |

## 5. Lưu ý diễn giải

Danh sách được lập ở cấp spell. Nếu một quốc gia có nhiều spell ở cùng nhóm sau khi tụt hạng, quốc gia đó có thể xuất hiện nhiều lần hoặc có trạng thái khác nhau giữa các spell.

Phân loại median là mô tả dữ liệu, không thay thế mô hình Cox. Kết luận về tốc độ thoát bẫy nên đọc cùng hazard ratio, khoảng tin cậy và p-value trong `report/cox_model_results.md`.
