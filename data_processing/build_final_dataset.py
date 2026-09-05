import pandas as pd

print("=== STEP 1: READ AND MELT DATA ===")
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
df_credit = process_cov('controlling_var/CREDIT.csv', 'CREDIT')

print("=== STEP 2: MERGE AND FILTER (2000-2026) ===")
df_merged = pd.merge(df_inc_long, df_agedep, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_ge, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_ind, on=['Code', 'Year'], how='outer')
df_merged = pd.merge(df_merged, df_credit, on=['Code', 'Year'], how='outer')

df_merged = df_merged[df_merged['Year'] >= 2000].copy()
df_merged.sort_values(by=['Code', 'Year'], inplace=True)
df_merged = df_merged.dropna(subset=['Code'])

print("=== STEP 3: IMPUTATION ===")
cols_to_impute = ['AGEDEP', 'GE', 'IND', 'CREDIT']
df_merged[cols_to_impute] = df_merged.groupby('Code')[cols_to_impute].transform(
    lambda x: x.interpolate(method='linear', limit_direction='both').ffill().bfill()
)

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
print("=> Done! Variables: IncomeGroup, AGEDEP, GE, IND, CREDIT")
