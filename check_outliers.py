import pandas as pd
import numpy as np

# Load survival data from main branch
df = pd.read_csv('survival_data.csv')
vars_to_check = ['AGEDEP', 'GE', 'IND', 'TO']

# Also load CREDIT from controlling_var to check it as well
try:
    df_credit = pd.read_csv('controlling_var/CREDIT.csv')
    df_credit_melt = df_credit.melt(id_vars=['Country Code'], var_name='Year', value_name='CREDIT')
    df_credit_melt['CREDIT'] = pd.to_numeric(df_credit_melt['CREDIT'], errors='coerce')
    credit_series = df_credit_melt['CREDIT'].dropna()
except Exception as e:
    credit_series = pd.Series(dtype=float)

def analyze_var(series, name):
    print(f"\n--- Analyzing {name} ---")
    p1 = series.quantile(0.01)
    p5 = series.quantile(0.05)
    p95 = series.quantile(0.95)
    p99 = series.quantile(0.99)
    min_val = series.min()
    max_val = series.max()
    
    print(f"Min: {min_val:.2f} | 1%: {p1:.2f} | 5%: {p5:.2f} | 95%: {p95:.2f} | 99%: {p99:.2f} | Max: {max_val:.2f}")
    
    # Simple outlier check using IQR
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = series[(series < lower_bound) | (series > upper_bound)]
    
    print(f"IQR Lower Bound: {lower_bound:.2f} | Upper Bound: {upper_bound:.2f}")
    print(f"Number of Outliers (IQR): {len(outliers)} ({len(outliers)/len(series)*100:.2f}%)")

for v in vars_to_check:
    analyze_var(df[v], v)

if not credit_series.empty:
    analyze_var(credit_series, 'CREDIT')
