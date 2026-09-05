import pandas as pd

print("Reading and converting data (Wide -> Long)...")

df_inc = pd.read_csv('income_data_cleaned.csv')
df_inc_long = df_inc.melt(id_vars=['Code'], var_name='Year', value_name='IncomeGroup')
df_inc_long['Year'] = df_inc_long['Year'].astype(str)

def process_covariate(filename, value_name):
    df = pd.read_csv(filename)
    code_col = 'Country Code' if 'Country Code' in df.columns else 'Code'
    year_cols = [c for c in df.columns if str(c).strip().isdigit()]
    
    df_sub = df[[code_col] + year_cols].copy()
    df_sub.rename(columns={code_col: 'Code'}, inplace=True)
    
    df_long = df_sub.melt(id_vars=['Code'], var_name='Year', value_name=value_name)
    df_long['Year'] = df_long['Year'].astype(str)
    
    return df_long

df_agedep = process_covariate('AGEDEP.csv', 'AGEDEP')
df_ge = process_covariate('GE.csv', 'GE')
df_gfcf = process_covariate('GFCF.csv', 'GFCF')
df_to = process_covariate('TO.csv', 'TO')

print("Merging all dataframes...")
df_final = pd.merge(df_inc_long, df_agedep, on=['Code', 'Year'], how='outer')
df_final = pd.merge(df_final, df_ge, on=['Code', 'Year'], how='outer')
df_final = pd.merge(df_final, df_gfcf, on=['Code', 'Year'], how='outer')
df_final = pd.merge(df_final, df_to, on=['Code', 'Year'], how='outer')

df_final.sort_values(by=['Code', 'Year'], inplace=True)
df_final = df_final.dropna(subset=['Code'])

output_file = 'merged_long_format.csv'
df_final.to_csv(output_file, index=False)

print(f"Done! Data saved to '{output_file}'")
print(f"Shape: {df_final.shape}")
print("Columns:", df_final.columns.tolist())
