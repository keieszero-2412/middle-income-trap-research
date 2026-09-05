import pandas as pd

df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

df_raw = pd.read_csv('controlling_var/merged_data_2000_2026.csv')
df_trans_data = df_raw[df_raw['Code'].isin(trans_codes)]

cols_to_check = ['IncomeGroup', 'AGEDEP', 'GE', 'GFCF', 'TO']
missing_counts = df_trans_data[cols_to_check].isnull().sum()
total_cells = len(df_trans_data)

print(f"=== MISSING COUNTS IN THE 139 TRANSITIONED COUNTRIES ===")
print(f"Total rows (139 countries x 27 years) = {total_cells} rows")
print("-" * 50)
for col in cols_to_check:
    count = missing_counts[col]
    percent = (count / total_cells) * 100
    print(f"- {col.ljust(12)}: Missing {count} cells ({percent:.2f}%)")
