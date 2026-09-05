import pandas as pd

df = pd.read_csv('merged_data_2000_2026.csv')
df.sort_values(by=['Code', 'Year'], inplace=True)

cols_to_impute = ['AGEDEP', 'GE', 'GFCF', 'TO']

df[cols_to_impute] = df.groupby('Code')[cols_to_impute].transform(
    lambda x: x.interpolate(method='linear').ffill().bfill()
)

output_file = 'final_lifelines_data.csv'
df.to_csv(output_file, index=False)

print("=== IMPUTATION SUCCESSFUL ===")
print(f"Saved completed file to: '{output_file}'")

missing_after = (df[cols_to_impute].isnull().sum() / len(df)) * 100
print("\nMissing percentage AFTER imputation:")
print(missing_after.round(2).to_string())
