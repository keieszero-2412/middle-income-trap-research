import pandas as pd

df_ind = pd.read_csv('controlling_var/IND.csv')
code_col = 'Country Code' if 'Country Code' in df_ind.columns else 'Code'
year_cols = [c for c in df_ind.columns if str(c).strip().isdigit()]
df_sub = df_ind[[code_col] + year_cols].copy()
df_sub.rename(columns={code_col: 'Code'}, inplace=True)
df_ind_long = df_sub.melt(id_vars=['Code'], var_name='Year', value_name='IND')
df_ind_long['Year'] = pd.to_numeric(df_ind_long['Year'], errors='coerce')

df_ind_long = df_ind_long[df_ind_long['Year'] >= 2000].copy()
df_ind_long.sort_values(by=['Code', 'Year'], inplace=True)

df_ind_long['IND'] = df_ind_long.groupby('Code')['IND'].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

df_trans_ind = df_ind_long[df_ind_long['Code'].isin(trans_codes)]
missing_count = df_trans_ind['IND'].isnull().sum()
total_cells = len(df_trans_ind)
missing_percent = (missing_count / total_cells) * 100

print("=== COMPARING IND VS GFCF IN 139 TRANSITIONED COUNTRIES ===")
print(f"Total cells needed (139 countries x 27 years): {total_cells}")
print(f"IND missing cells: {missing_count} ({missing_percent:.2f}%)")
print(f"GFCF missing cells (old): 567 (15.11%)")

if missing_count < 567:
    print("\n=> CONCLUSION: Great! Using IND saves a lot of data.")
else:
    print("\n=> CONCLUSION: Unfortunately, IND is missing even more than GFCF.")
