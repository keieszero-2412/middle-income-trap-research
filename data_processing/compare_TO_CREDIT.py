import pandas as pd

# 1. Đọc danh sách 139 quốc gia thăng hạng
df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

# 2. Gộp tất cả dữ liệu gốc (IncomeGroup, AGEDEP, GE, IND, TO, CREDIT)
df_inc = pd.read_csv('income_data/income_data_cleaned.csv')
df_inc_long = df_inc.melt(id_vars=['Code'], var_name='Year', value_name='IncomeGroup')
df_inc_long['Year'] = pd.to_numeric(df_inc_long['Year'], errors='coerce')

def process_wide(filename, val_name):
    df = pd.read_csv(filename)
    c_col = 'Country Code' if 'Country Code' in df.columns else 'Code'
    y_cols = [c for c in df.columns if str(c).strip().isdigit()]
    df_sub = df[[c_col] + y_cols].copy()
    df_sub.rename(columns={c_col: 'Code'}, inplace=True)
    df_long = df_sub.melt(id_vars=['Code'], var_name='Year', value_name=val_name)
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
    return df_long

df_agedep = process_wide('controlling_var/AGEDEP.csv', 'AGEDEP')
df_ge = process_wide('controlling_var/GE.csv', 'GE')
df_ind = process_wide('controlling_var/IND.csv', 'IND')
df_to = process_wide('controlling_var/TO.csv', 'TO')
df_credit = process_wide('controlling_var/CREDIT.csv', 'CREDIT')

df_merged = pd.merge(df_inc_long, df_agedep, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_ge, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_ind, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_to, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_credit, on=['Code', 'Year'], how='outer')

df_merged = df_merged[(df_merged['Year'] >= 2000) & (df_merged['Code'].isin(trans_codes))].copy()
df_merged.sort_values(by=['Code', 'Year'], inplace=True)

# 3. Nội suy
cols_impute = ['AGEDEP', 'GE', 'IND', 'TO', 'CREDIT']
df_merged[cols_impute] = df_merged.groupby('Code')[cols_impute].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

# 4. Tìm quốc gia bị loại
dropped_codes = df_merged[df_merged.isnull().any(axis=1)]['Code'].unique()
kept_codes = [c for c in trans_codes if c not in dropped_codes]

# So sánh: Nếu chỉ dùng TO (không có CREDIT)
df_to_only = df_merged.drop(columns=['CREDIT'])
dropped_to_only = df_to_only[df_to_only.isnull().any(axis=1)]['Code'].unique()

# So sánh: Nếu chỉ dùng CREDIT (không có TO)
df_credit_only = df_merged.drop(columns=['TO'])
dropped_credit_only = df_credit_only[df_credit_only.isnull().any(axis=1)]['Code'].unique()

# Quốc gia bị loại thêm khi giữ cả 2
extra_dropped = set(dropped_codes) - set(dropped_to_only)

print("=== SO SANH 3 KICH BAN ===")
print(f"[Chi dung TO]:          Bi loai {len(dropped_to_only)} nuoc, Giu lai {len(trans_codes)-len(dropped_to_only)} nuoc")
print(f"[Chi dung CREDIT]:      Bi loai {len(dropped_credit_only)} nuoc, Giu lai {len(trans_codes)-len(dropped_credit_only)} nuoc")
print(f"[Giu ca TO va CREDIT]:  Bi loai {len(dropped_codes)} nuoc, Giu lai {len(trans_codes)-len(dropped_codes)} nuoc")

print(f"\n=== DANH SACH {len(dropped_codes)} QUOC GIA THANH HANG BI LOAI (KHI GIU CA 2) ===")
for code in sorted(dropped_codes):
    c_data = df_merged[df_merged['Code'] == code]
    m = []
    if c_data['AGEDEP'].isnull().all(): m.append('AGEDEP')
    if c_data['GE'].isnull().all(): m.append('GE')
    if c_data['IND'].isnull().all(): m.append('IND')
    if c_data['TO'].isnull().all(): m.append('TO')
    if c_data['CREDIT'].isnull().all(): m.append('CREDIT')
    if c_data['IncomeGroup'].isnull().all(): m.append('IncomeGroup')
    print(f"  {code}: [{', '.join(m)}]")

if extra_dropped:
    print(f"\n=== QUOC GIA BI LOAI THEM (so voi chi dung TO) ===")
    for code in sorted(extra_dropped):
        c_data = df_merged[df_merged['Code'] == code]
        m = []
        if c_data['CREDIT'].isnull().all(): m.append('CREDIT')
        print(f"  {code}: [{', '.join(m)}]")
else:
    print("\n=> Khong co quoc gia nao bi loai THEM khi giu ca 2 bien!")
