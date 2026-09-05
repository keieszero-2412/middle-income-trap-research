import pandas as pd

# 1. Đọc danh sách các quốc gia có sự thay đổi nhóm thu nhập (Thăng hạng)
df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

# 2. Xây dựng lại dữ liệu gốc (Thô - Chưa nội suy)
df_inc = pd.read_csv('income_data/income_data_cleaned.csv')
df_inc_long = df_inc.melt(id_vars=['Code'], var_name='Year', value_name='IncomeGroup')
df_inc_long['Year'] = pd.to_numeric(df_inc_long['Year'], errors='coerce')

def process_cov(filename, val_name):
    df = pd.read_csv(filename)
    c_col = 'Country Code' if 'Country Code' in df.columns else 'Code'
    y_cols = [c for c in df.columns if str(c).strip().isdigit()]
    df_sub = df[[c_col] + y_cols].copy()
    df_sub.rename(columns={c_col: 'Code'}, inplace=True)
    df_long = df_sub.melt(id_vars=['Code'], var_name='Year', value_name=val_name)
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
    return df_long

df_agedep = process_cov('controlling_var/AGEDEP.csv', 'AGEDEP')
df_ge = process_cov('controlling_var/GE.csv', 'GE')
df_ind = process_cov('controlling_var/IND.csv', 'IND')
df_to = process_cov('controlling_var/TO.csv', 'TO')

df_merged = pd.merge(df_inc_long, df_agedep, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_ge, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_ind, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_to, on=['Code', 'Year'], how='outer')

df_merged = df_merged[df_merged['Year'] >= 2000].copy()
df_merged = df_merged.dropna(subset=['Code'])
df_merged.sort_values(by=['Code', 'Year'], inplace=True)

# 3. LỌC: CHỈ GIỮ LẠI CÁC QUỐC GIA THĂNG HẠNG (LOẠI BỎ CÁC NƯỚC ĐỨNG IM)
df_raw = df_merged[df_merged['Code'].isin(trans_codes)].copy()
total_countries = len(trans_codes)
total_rows = len(df_raw)
cols = ['IncomeGroup', 'AGEDEP', 'GE', 'IND', 'TO']

# 4. THỐNG KÊ TRƯỚC NỘI SUY
missing_raw = df_raw[cols].isnull().sum().sort_values(ascending=False)
missing_by_year_raw = df_raw.groupby('Year')[cols].apply(lambda x: x.isnull().sum().sum() / (len(x)*5) * 100).sort_values(ascending=False)

# 5. THỰC HIỆN NỘI SUY (IMPUTATION)
cols_to_impute = ['AGEDEP', 'GE', 'IND', 'TO']
df_imputed = df_raw.copy()
df_imputed[cols_to_impute] = df_imputed.groupby('Code')[cols_to_impute].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

# 6. THỐNG KÊ SAU NỘI SUY
missing_imputed = df_imputed[cols].isnull().sum().sort_values(ascending=False)
missing_by_year_imputed = df_imputed.groupby('Year')[cols].apply(lambda x: x.isnull().sum().sum() / (len(x)*5) * 100).sort_values(ascending=False)

# 7. QUỐC GIA BỊ LOẠI SAU NỘI SUY (Missing 100%)
dropped_codes = df_imputed[df_imputed.isnull().any(axis=1)]['Code'].unique()
df_dropped = df_imputed[df_imputed['Code'].isin(dropped_codes)]

# 8. TẠO BÁO CÁO MARKDOWN
rep = []
rep.append("# BÁO CÁO THỰC TRẠNG DỮ LIỆU KHUYẾT (CHỈ TÍNH NHÓM QUỐC GIA CÓ SỰ THAY ĐỔI THU NHẬP)\n")
rep.append(f"**Tổng số quốc gia thăng hạng được phân tích:** {total_countries} quốc gia\n")
rep.append(f"**Tổng số dòng dữ liệu (Quan sát):** {total_rows} dòng (Mỗi quốc gia 27 năm từ 2000-2026)\n\n")

rep.append("## 1. SO SÁNH TỶ LỆ KHUYẾT THEO BIẾN (TRƯỚC & SAU NỘI SUY)\n")
rep.append("| Biến số | Trước nội suy (Số ô khuyết) | Trước nội suy (%) | Sau nội suy (Số ô khuyết) | Sau nội suy (%) | Hiệu quả cứu dữ liệu |\n")
rep.append("|---|---|---|---|---|---|\n")

for var in missing_raw.index:
    c_raw = missing_raw[var]
    p_raw = (c_raw / total_rows) * 100
    c_imp = missing_imputed[var]
    p_imp = (c_imp / total_rows) * 100
    saved = c_raw - c_imp
    
    if var == 'IncomeGroup':
        rep.append(f"| **{var}** | {c_raw} | {p_raw:.2f}% | {c_imp} | {p_imp:.2f}% | *(Không nội suy)* |\n")
    else:
        rep.append(f"| **{var}** | {c_raw} | {p_raw:.2f}% | {c_imp} | {p_imp:.2f}% | Cứu được {saved} ô |\n")

rep.append("\n## 2. NĂM NÀO BỊ THIẾU DỮ LIỆU NHIỀU NHẤT? (TRƯỚC NỘI SUY)\n")
rep.append("*(Bảng dưới liệt kê top 5 năm bị khuyết nhiều nhất)*\n\n")
rep.append("| Năm | Tỷ lệ khuyết trung bình (%) |\n")
rep.append("|---|---|\n")
for year, pct in missing_by_year_raw.head(5).items():
    rep.append(f"| {int(year)} | {pct:.2f}% |\n")

rep.append("\n## 3. DANH SÁCH QUỐC GIA BỊ LOẠI BỎ (SAU NỘI SUY)\n")
rep.append("Dù đã cố gắng nội suy để vớt vát dữ liệu, vẫn có một số quốc gia bị loại bỏ hoàn toàn do **KHUYẾT TRẮNG (Missing 100%)** một biến số nào đó trong suốt 27 năm. Dưới đây là danh sách chi tiết các quốc gia có thăng hạng nhưng buộc phải loại bỏ khỏi mô hình Cox.\n\n")
rep.append(f"**Tổng số quốc gia bị loại:** {len(dropped_codes)} quốc gia (Còn lại {total_countries - len(dropped_codes)} quốc gia sạch 100% để chạy mô hình).\n\n")

rep.append("| Mã Quốc Gia | Các biến bị khuyết hoàn toàn (Nguyên nhân loại bỏ) |\n")
rep.append("|---|---|\n")
for code in sorted(dropped_codes):
    c_data = df_dropped[df_dropped['Code'] == code]
    m_cols = []
    if c_data['AGEDEP'].isnull().all(): m_cols.append('AGEDEP')
    if c_data['GE'].isnull().all(): m_cols.append('GE')
    if c_data['IND'].isnull().all(): m_cols.append('IND')
    if c_data['TO'].isnull().all(): m_cols.append('TO')
    if c_data['IncomeGroup'].isnull().all(): m_cols.append('IncomeGroup')
    
    rep.append(f"| **{code}** | {', '.join(m_cols)} |\n")

with open('report/missing_data_report.md', 'w', encoding='utf-8') as f:
    f.writelines(rep)

print("Đã tạo xong báo cáo mới tại: report/missing_data_report.md")
