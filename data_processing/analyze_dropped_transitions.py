import pandas as pd

df_trans = pd.read_csv('income_data/income_data_transitioned.csv')
trans_codes = df_trans['Code'].unique()

df_dropped = pd.read_csv('dropped_codes_missing_data.csv')
dropped_codes = df_dropped['Dropped_Code'].unique()

dropped_transitioned = list(set(trans_codes) & set(dropped_codes))

df_final = pd.read_csv('final_lifelines_data.csv')
df_dropped_trans_data = df_final[df_final['Code'].isin(dropped_transitioned)]

print("=== DROPPED TRANSITIONED COUNTRIES MATCHING ===")
print(f"- Total transitioned countries (initial): {len(trans_codes)}")
print(f"- Transitioned countries DROPPED: {len(dropped_transitioned)}")
print(f"- Transitioned countries KEPT (100% clean): {len(trans_codes) - len(dropped_transitioned)}")

print("\n=== REASONS FOR DROPPING ===")
reasons = []
for code in sorted(dropped_transitioned):
    country_data = df_dropped_trans_data[df_dropped_trans_data['Code'] == code]
    missing_cols = []
    
    if country_data['AGEDEP'].isnull().all(): missing_cols.append('AGEDEP')
    if country_data['GE'].isnull().all(): missing_cols.append('GE')
    if country_data['GFCF'].isnull().all(): missing_cols.append('GFCF')
    if country_data['TO'].isnull().all(): missing_cols.append('TO')
    if country_data['IncomeGroup'].isnull().all(): missing_cols.append('IncomeGroup')
    
    reason_str = ", ".join(missing_cols)
    reasons.append({'Code': code, 'Missing_Variables': reason_str})
    print(f"- {code}: Dropped due to completely missing data for [{reason_str}]")

pd.DataFrame(reasons).to_csv('data_processing/dropped_transitions_reasons.csv', index=False)
print("\nExported details to: 'data_processing/dropped_transitions_reasons.csv'")
