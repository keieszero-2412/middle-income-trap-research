import pandas as pd

df = pd.read_csv('merged_long_format.csv')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df_filtered = df[df['Year'] >= 2000].copy()

output_file = 'merged_data_2000_2026.csv'
df_filtered.to_csv(output_file, index=False)

print("=== 1. DATA CUTTING RESULTS ===")
print(f"- Rows remaining: {len(df_filtered)}")
print(f"- Saved to: '{output_file}'\n")

cols_to_check = ['IncomeGroup', 'AGEDEP', 'GE', 'GFCF', 'TO']
missing_stats = df_filtered.groupby('Year')[cols_to_check].apply(lambda x: x.isnull().sum() / len(x) * 100)
missing_stats['Avg_Missing_%'] = missing_stats.mean(axis=1)

print("=== 2. MISSING PERCENTAGE BY YEAR (2000 onwards) ===")
print(missing_stats.round(2).to_string())

print("\n=== 3. OVERALL MISSING PERCENTAGE BY VARIABLE (2000-2026) ===")
overall_missing = (df_filtered[cols_to_check].isnull().sum() / len(df_filtered)) * 100
print(overall_missing.round(2).to_string())
