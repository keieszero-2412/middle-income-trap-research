import pandas as pd

# BƯỚC 1: Lấy lại quy trình gộp dữ liệu gốc (Chưa qua điền khuyết)
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
df_merged.sort_values(by=['Code', 'Year'], inplace=True)
df_merged = df_merged.dropna(subset=['Code'])

# Dữ liệu df_merged lúc này là THÔ (Raw), chưa qua bất kỳ thuật toán nội suy (impute) nào.
cols_to_check = ['IncomeGroup', 'AGEDEP', 'GE', 'IND', 'TO']

# BƯỚC 2: Thống kê chi tiết
report = []
report.append("# Báo cáo Chi tiết Dữ liệu Khuyết (Với biến IND)\n")
report.append("Báo cáo này phân tích dữ liệu gốc từ năm 2000 đến 2026, **TRƯỚC KHI** áp dụng bất kỳ thuật toán điền khuyết (imputation) nào.\n")

# 2.1 Biến nào bị khuyết nhiều nhất?
report.append("## 1. Biến nào bị thiếu dữ liệu nhiều nhất?\n")
total_rows = len(df_merged)
missing_by_var = df_merged[cols_to_check].isnull().sum().sort_values(ascending=False)
report.append("| Biến số | Số ô khuyết | Tỷ lệ khuyết (%) |\n|---|---|---|\n")
for var, count in missing_by_var.items():
    pct = (count / total_rows) * 100
    report.append(f"| **{var}** | {count} | {pct:.2f}% |\n")
report.append("\n")

# 2.2 Năm nào bị khuyết nhiều nhất?
report.append("## 2. Năm nào bị thiếu dữ liệu nhiều nhất?\n")
report.append("Tỷ lệ khuyết tính trung bình trên cả 5 biến cho từng năm.\n\n")
missing_by_year = df_merged.groupby('Year')[cols_to_check].apply(lambda x: x.isnull().sum().sum() / (len(x) * len(cols_to_check)) * 100)
missing_by_year_sorted = missing_by_year.sort_values(ascending=False)
report.append("| Năm | Tỷ lệ khuyết trung bình (%) |\n|---|---|\n")
for year, pct in missing_by_year_sorted.head(10).items():
    report.append(f"| {int(year)} | {pct:.2f}% |\n")
report.append("\n*(Các năm còn lại dao động ổn định quanh mức 16-18%)*\n\n")

# 2.3 Quốc gia (Code) nào bị khuyết?
report.append("## 3. Quốc gia nào bị thiếu toàn bộ dữ liệu (Bị loại)?\n")
report.append("Sau bước điền khuyết (ffill, bfill), những quốc gia bị loại là những quốc gia **hoàn toàn không có dữ liệu (Missing 100%)** ở một biến bất kỳ trong suốt 27 năm.\n\n")

# Lấy lại danh sách 109 quốc gia bị loại từ kết quả cuối cùng (để phân tích)
df_imputed = df_merged.copy()
df_imputed[cols_to_check] = df_imputed.groupby('Code')[cols_to_check].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)
dropped_codes = df_imputed[df_imputed.isnull().any(axis=1)]['Code'].unique()
df_dropped = df_imputed[df_imputed['Code'].isin(dropped_codes)]

reasons = []
for code in sorted(dropped_codes):
    c_data = df_dropped[df_dropped['Code'] == code]
    missing_cols = []
    if c_data['AGEDEP'].isnull().all(): missing_cols.append('AGEDEP')
    if c_data['GE'].isnull().all(): missing_cols.append('GE')
    if c_data['IND'].isnull().all(): missing_cols.append('IND')
    if c_data['TO'].isnull().all(): missing_cols.append('TO')
    if c_data['IncomeGroup'].isnull().all(): missing_cols.append('IncomeGroup')
    
    r_str = ", ".join(missing_cols)
    reasons.append(f"| **{code}** | {r_str} |")

report.append("| Mã Quốc Gia | Biến bị khuyết 100% (Nguyên nhân bị loại) |\n|---|---|\n")
report.extend([r + "\n" for r in reasons])

# Ghi ra file markdown
with open('data_processing/missing_data_report_ind.md', 'w', encoding='utf-8') as f:
    f.writelines(report)

print("Đã xuất báo cáo chi tiết ra file 'data_processing/missing_data_report_ind.md'")
