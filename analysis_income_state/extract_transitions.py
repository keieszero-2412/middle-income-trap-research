import pandas as pd

df = pd.read_csv('income_data_transitioned.csv')
years = df.columns[1:]

rank = {'L': 1, 'LM': 2, 'UM': 3, 'H': 4}

transitions = []

for _, row in df.iterrows():
    code = row['Code']
    valid_data = row[years].dropna()
    
    if len(valid_data) < 2:
        continue
        
    prev_state = None
    
    for year, state in valid_data.items():
        if state not in rank:
            continue
            
        if prev_state is None:
            prev_state = state
            continue
            
        if rank[state] > rank[prev_state]:
            transitions.append({
                'Code': code,
                'From': prev_state,
                'To': state,
                'Year': year
            })
            
        prev_state = state

# Lưu dữ liệu thô ra file CSV (cho mô hình lifelines sau này)
transitions_df = pd.DataFrame(transitions)
transitions_df.to_csv('transition_events.csv', index=False)

# Tạo báo cáo Markdown
report_lines = ["# Báo cáo Tổng hợp Sự kiện Chuyển đổi Thu nhập\n"]
report_lines.append("Danh sách chi tiết các quốc gia đã chuyển đổi nhóm thu nhập (nâng hạng) trong giai đoạn quan sát (1991-2026).\n")
report_lines.append("> **Lưu ý:** Cột 'Năm chuyển đổi' là năm ĐẦU TIÊN mà quốc gia đó được ghi nhận ở mức thu nhập mới.\n")

# Nhóm theo loại chuyển đổi
grouped = transitions_df.groupby(['From', 'To'])

for trans_type, group in grouped:
    from_g, to_g = trans_type
    report_lines.append(f"## {from_g} $\\rightarrow$ {to_g} ({len(group)} sự kiện)")
    report_lines.append("| Quốc gia | Năm chuyển đổi |")
    report_lines.append("|---|---|")
    
    sorted_group = group.sort_values(by=['Year', 'Code'])
    for _, r in sorted_group.iterrows():
        report_lines.append(f"| {r['Code']} | {r['Year']} |")
    report_lines.append("\n")

artifact_path = r"C:\Users\zero\.gemini\antigravity-ide\brain\f2354809-c2e2-4da3-a721-6f315b89e352\transition_report.md"
with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(report_lines))

print("=== HOAN TAT ===")
print("Da luu transition_events.csv")
print("Da tao artifact transition_report.md")
