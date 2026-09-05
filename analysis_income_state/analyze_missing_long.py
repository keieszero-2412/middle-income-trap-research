import pandas as pd

df = pd.read_csv('merged_long_format.csv')

# Các cột cần kiểm tra dữ liệu khuyết
cols_to_check = ['IncomeGroup', 'AGEDEP', 'GE', 'GFCF', 'TO']

# Tính phần trăm missing của từng cột theo từng năm
missing_stats = df.groupby('Year')[cols_to_check].apply(lambda x: x.isnull().sum() / len(x) * 100)

# Tính trung bình tỷ lệ missing của cả 5 cột để xếp hạng năm nào tệ nhất
missing_stats['Avg_Missing_%'] = missing_stats.mean(axis=1)

# Sắp xếp theo tỷ lệ missing giảm dần
worst_years = missing_stats.sort_values(by='Avg_Missing_%', ascending=False)

print("=== TOP 15 YEARS WITH MOST MISSING DATA (%) ===")
print(worst_years.head(15).round(2).to_string())

print("\n=== TOP 10 YEARS WITH LEAST MISSING DATA (%) ===")
print(worst_years.tail(10).round(2).to_string())
