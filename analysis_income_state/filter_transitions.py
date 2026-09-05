import pandas as pd

# Đọc file dữ liệu đã làm sạch
df = pd.read_csv('income_data_cleaned.csv')
years = df.columns[1:]

# Định nghĩa thứ bậc các nhóm thu nhập
# L (Low), LM (Lower Middle), UM (Upper Middle), H (High)
rank = {'L': 1, 'LM': 2, 'UM': 3, 'H': 4}

def check_transition(row):
    # Lấy danh sách các trạng thái thu nhập theo thời gian, bỏ qua các giá trị NaN
    states = row[years].dropna().tolist()
    
    if len(states) < 2:
        return False
        
    # Kiểm tra xem có bất kỳ sự chuyển đổi đi lên nào không
    for i in range(len(states) - 1):
        s1 = states[i]
        s2 = states[i+1]
        
        if s1 in rank and s2 in rank:
            # Nếu thứ bậc sau > thứ bậc trước (tức là có nâng hạng thu nhập)
            if rank[s2] > rank[s1]:
                return True
    return False

# Lọc dữ liệu: Chỉ giữ lại những quốc gia thỏa mãn điều kiện check_transition
df_transitioned = df[df.apply(check_transition, axis=1)]
df_not_transitioned = df[~df.apply(check_transition, axis=1)]

print("=== KET QUA LOC DU LIEU CHUYEN DOI ===")
print(f"Tong so quoc gia ban dau: {len(df)}")
print(f"So quoc gia co nang hang (L->LM, LM->UM, UM->H): {len(df_transitioned)}")
print(f"So quoc gia KHONG nang hang (bi loai bo): {len(df_not_transitioned)}")

# Lưu lại danh sách
output_file = 'income_data_transitioned.csv'
df_transitioned.to_csv(output_file, index=False)
print(f"\nDa luu danh sach cac quoc gia co nang hang vao file: '{output_file}'")
