import pandas as pd
import os
import sys

# Đảm bảo đường dẫn tuyệt đối
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

print("=== STEP 1: READ AND MELT DATA ===")
df_inc = pd.read_csv('income_data/income_data_cleaned.csv')
df_inc_long = df_inc.melt(id_vars=['Code'], var_name='Year', value_name='IncomeGroup')
df_inc_long['Year'] = pd.to_numeric(df_inc_long['Year'], errors='coerce')

def process_cov(filename, val_name):
    filepath = os.path.join('controlling_var', filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found.")
        return None
    df = pd.read_csv(filepath)
    c_col = 'Country Code' if 'Country Code' in df.columns else 'Code'
    y_cols = [c for c in df.columns if str(c).strip().isdigit()]
    df_sub = df[[c_col] + y_cols].copy()
    df_sub.rename(columns={c_col: 'Code'}, inplace=True)
    df_long = df_sub.melt(id_vars=['Code'], var_name='Year', value_name=val_name)
    df_long['Year'] = pd.to_numeric(df_long['Year'], errors='coerce')
    return df_long

# Đọc 5 biến
df_agedep = process_cov('AGEDEP.csv', 'AGEDEP')
df_ge = process_cov('GE.csv', 'GE')
df_ind = process_cov('IND.csv', 'IND')
df_credit = process_cov('CREDIT.csv', 'CREDIT')
df_to = process_cov('TO.csv', 'TO')

# ECI is supplied in long format with different source column names.
eci_path = os.path.join('controlling_var', 'ECI.csv')
df_eci = pd.read_csv(eci_path)
df_eci.rename(columns={'country_iso3_code': 'Code', 'year': 'Year', 'eci_hs92': 'ECI'}, inplace=True)
df_eci['Year'] = pd.to_numeric(df_eci['Year'], errors='coerce')

# TFP đã ở dạng long format
tfp_path = os.path.join('controlling_var', 'TFP.csv')
df_tfp = None
if os.path.exists(tfp_path):
    df_tfp = pd.read_csv(tfp_path)
    if 'Country Code' in df_tfp.columns:
        df_tfp.rename(columns={'Country Code': 'Code'}, inplace=True)
    df_tfp['Year'] = pd.to_numeric(df_tfp['Year'], errors='coerce')

print("=== STEP 2: MERGE AND FILTER (2000-2026) ===")
df_merged = df_inc_long.copy()
for df_cov in [df_tfp, df_ge, df_agedep, df_ind, df_to, df_credit, df_eci]:
    if df_cov is not None:
        df_merged = pd.merge(df_merged, df_cov, on=['Code', 'Year'], how='outer')

df_merged = df_merged[df_merged['Year'] >= 2000].copy()
df_merged.sort_values(by=['Code', 'Year'], inplace=True)
df_merged = df_merged.dropna(subset=['Code'])

print("=== STEP 3: IMPUTATION ===")
# Khai báo các cột có trong DataFrame để Impute và Winsorize
all_potential_cols = ['TFP', 'GE', 'AGEDEP', 'IND', 'TO', 'CREDIT', 'ECI']
cols_to_impute = [col for col in all_potential_cols if col in df_merged.columns]

df_merged[cols_to_impute] = df_merged.groupby('Code')[cols_to_impute].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

print("=== STEP 3.5: WINSORIZE (5% - 95%) ===")
from scipy.stats.mstats import winsorize
for col in cols_to_impute:
    df_merged[col] = winsorize(df_merged[col], limits=[0.05, 0.05])

df_merged.to_csv('final_lifelines_data.csv', index=False)

print("=== STEP 4: FILTER OUT COUNTRIES WITH MISSING DATA ===")
codes_with_missing = df_merged[df_merged.isnull().any(axis=1)]['Code'].unique()
df_clean = df_merged[~df_merged['Code'].isin(codes_with_missing)]

print(f"- Total Countries: {df_merged['Code'].nunique()}")
print(f"- Dropped: {len(codes_with_missing)}")
print(f"- Kept (100% Clean): {df_clean['Code'].nunique()}")

df_clean.to_csv('final_lifelines_data_clean.csv', index=False)
pd.DataFrame({'Dropped_Code': codes_with_missing}).to_csv('dropped_codes_missing_data.csv', index=False)

df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()
dropped_transitioned = list(set(trans_codes) & set(codes_with_missing))
print(f"- Transitioned dropped: {len(dropped_transitioned)} / {len(trans_codes)}")
print(f"- Transitioned kept: {len(trans_codes) - len(dropped_transitioned)}")
print(f"=> Done! Variables: IncomeGroup, {', '.join(cols_to_impute)}")
