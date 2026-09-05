import pandas as pd

# 1. Đọc ECI.csv (đã ở sẵn định dạng long)
df_eci_long = pd.read_csv('controlling_var/ECI.csv')

# Đổi tên cột cho khớp với các file khác
df_eci_long.rename(columns={'country_iso3_code': 'Code', 'year': 'Year', 'eci_hs92': 'ECI'}, inplace=True)
df_eci_long['Year'] = pd.to_numeric(df_eci_long['Year'], errors='coerce')

# Lọc từ năm 2000 - 2026
df_eci_long = df_eci_long[df_eci_long['Year'] >= 2000].copy()

# Sắp xếp
df_eci_long.sort_values(by=['Code', 'Year'], inplace=True)

# Lấy 139 quốc gia thăng hạng
df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

# Để có đủ 27 năm (2000-2026) cho 139 quốc gia, ta tạo ra một grid chuẩn để xem khuyết bao nhiêu so với mức chuẩn 3753 dòng.
idx = pd.MultiIndex.from_product([trans_codes, range(2000, 2027)], names=['Code', 'Year'])
df_trans_eci = pd.DataFrame(index=idx).reset_index()

# Gộp dữ liệu ECI vào grid chuẩn
df_trans_eci = pd.merge(df_trans_eci, df_eci_long[['Code', 'Year', 'ECI']], on=['Code', 'Year'], how='left')

# Tính missing TRƯỚC KHI NỘI SUY
missing_raw = df_trans_eci['ECI'].isnull().sum()

# 2. Nội suy cho biến ECI (interpolate, ffill, bfill)
df_trans_eci['ECI'] = df_trans_eci.groupby('Code')['ECI'].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

# 3. Tính tỷ lệ missing SAU KHI NỘI SUY
missing_imputed = df_trans_eci['ECI'].isnull().sum()
total_cells = len(df_trans_eci)
missing_percent = (missing_imputed / total_cells) * 100

print("=== SO SANH BIEN MOI (ECI) VOI TO TRONG NHOM 139 NUOC ===")
print(f"Tong so o du lieu (139 nuoc x 27 nam) = {total_cells} o")
print("-" * 50)
print(f"[ECI] Khuyet TRUOC noi suy: {missing_raw} o")
print(f"[ECI] Khuyet SAU noi suy: {missing_imputed} o ({missing_percent:.2f}%)")
print("-" * 50)
print(f"[TO] Khuyet SAU noi suy (cu): 432 o (11.51%)")

if missing_imputed < 432:
    print("\n=> KET LUAN: Tuyet voi! Thay TO bang ECI giup luu giu them nhieu du lieu.")
else:
    print("\n=> KET LUAN: Khong tot hon. ECI bi khuyet nhieu hon (hoac bang) TO.")
