import pandas as pd

# 1. Đọc CREDIT.csv (Wide format giống AGEDEP, GE)
df_credit = pd.read_csv('controlling_var/CREDIT.csv')
code_col = 'Country Code'
year_cols = [c for c in df_credit.columns if str(c).strip().isdigit()]
df_sub = df_credit[[code_col] + year_cols].copy()
df_sub.rename(columns={code_col: 'Code'}, inplace=True)
df_credit_long = df_sub.melt(id_vars=['Code'], var_name='Year', value_name='CREDIT')
df_credit_long['Year'] = pd.to_numeric(df_credit_long['Year'], errors='coerce')

# Lọc từ năm 2000 - 2026
df_credit_long = df_credit_long[df_credit_long['Year'] >= 2000].copy()
df_credit_long.sort_values(by=['Code', 'Year'], inplace=True)

# 2. Lấy 139 quốc gia thăng hạng
df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

# Tạo grid chuẩn 139 x 27 = 3753
idx = pd.MultiIndex.from_product([trans_codes, range(2000, 2027)], names=['Code', 'Year'])
df_trans_credit = pd.DataFrame(index=idx).reset_index()
df_trans_credit = pd.merge(df_trans_credit, df_credit_long[['Code', 'Year', 'CREDIT']], on=['Code', 'Year'], how='left')

# Tính missing TRƯỚC NỘI SUY
missing_raw = df_trans_credit['CREDIT'].isnull().sum()

# 3. Nội suy
df_trans_credit['CREDIT'] = df_trans_credit.groupby('Code')['CREDIT'].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

# Missing SAU NỘI SUY
missing_imputed = df_trans_credit['CREDIT'].isnull().sum()
total_cells = len(df_trans_credit)

print("=== SO SANH CREDIT VOI TO TRONG NHOM 139 NUOC ===")
print(f"Tong so o du lieu (139 nuoc x 27 nam) = {total_cells} o")
print("-" * 50)
print(f"[CREDIT] Khuyet TRUOC noi suy: {missing_raw} o ({missing_raw/total_cells*100:.2f}%)")
print(f"[CREDIT] Khuyet SAU noi suy:   {missing_imputed} o ({missing_imputed/total_cells*100:.2f}%)")
print("-" * 50)
print(f"[TO]     Khuyet SAU noi suy (cu): 432 o (11.51%)")

if missing_imputed < 432:
    print("\n=> KET LUAN: Tuyet voi! CREDIT it khuyet hon TO.")
else:
    print("\n=> KET LUAN: Khong tot hon. CREDIT bi khuyet nhieu hon TO.")
