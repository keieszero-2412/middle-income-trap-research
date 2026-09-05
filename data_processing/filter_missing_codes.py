import pandas as pd

df = pd.read_csv('final_lifelines_data.csv')
codes_with_missing = df[df.isnull().any(axis=1)]['Code'].unique()
df_clean = df[~df['Code'].isin(codes_with_missing)]

df_clean.to_csv('final_lifelines_data_clean.csv', index=False)
pd.DataFrame({'Dropped_Code': codes_with_missing}).to_csv('dropped_codes_missing_data.csv', index=False)

print("=== DATA FILTERING RESULTS ===")
print(f"- Initial total countries: {df['Code'].nunique()}")
print(f"- Countries dropped due to missing data: {len(codes_with_missing)}")
print(f"- Remaining completely clean countries: {df_clean['Code'].nunique()}")
print("- Saved clean data to: 'final_lifelines_data_clean.csv'")
print("- Saved list of dropped countries to: 'dropped_codes_missing_data.csv'")
