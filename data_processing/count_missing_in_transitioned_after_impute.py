import pandas as pd

df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

df_imputed = pd.read_csv('final_lifelines_data.csv')
df_trans_data = df_imputed[df_imputed['Code'].isin(trans_codes)]

cols_to_check = ['IncomeGroup', 'AGEDEP', 'GE', 'IND', 'TO']
missing_counts = df_trans_data[cols_to_check].isnull().sum()
total_cells = len(df_trans_data)

print(f"=== MISSING COUNTS AFTER IMPUTATION (139 COUNTRIES) ===")
print(f"Total rows (139 countries x 27 years) = {total_cells} rows")
print("-" * 50)
for col in cols_to_check:
    count = missing_counts[col]
    percent = (count / total_cells) * 100
    print(f"- {col.ljust(12)}: Missing {count} cells ({percent:.2f}%)")
