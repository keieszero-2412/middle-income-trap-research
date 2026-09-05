"""Create the research scope and country escape-status report."""
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SURVIVAL_FILE = BASE_DIR / 'survival_data.csv'
REPORT_FILE = BASE_DIR / 'report' / 'research_scope_and_escape_status.md'

VARIABLES_MAIN = ['TFP', 'GE', 'AGEDEP', 'IND', 'TO', 'CREDIT', 'ECI']
VARIABLES_5VARS = ['TFP', 'GE', 'AGEDEP', 'TO', 'CREDIT']


def classify_spells(data):
    variables = [column for column in VARIABLES_MAIN if column in data.columns]
    spells = data.groupby(['spell_id', 'spell_group']).agg(
        Code=('Code', 'first'),
        start_year=('Year', 'min'),
        end_year=('Year', 'max'),
        duration=('stop', 'max'),
        event=('event', 'max'),
        **{variable: (variable, 'mean') for variable in variables},
    ).reset_index()

    medians = spells.loc[spells['event'] == 1].groupby('spell_group')['duration'].median()
    spells['median_duration'] = spells['spell_group'].map(medians)
    spells['status'] = 'Chưa thoát'
    escaped = (spells['event'] == 1) & (spells['duration'] <= spells['median_duration'])
    spells.loc[escaped, 'status'] = 'Đã thoát'
    spells['transition'] = spells['spell_group'].map({'LM': 'LM -> UM', 'UM': 'UM -> H'})
    return spells, medians


def country_table(spells, group, status):
    selected = spells[(spells['spell_group'] == group) & (spells['status'] == status)].copy()
    selected.sort_values(['duration', 'Code'], inplace=True)
    return selected


def format_country_rows(selected):
    if selected.empty:
        return '| (Không có) | - | - | - |\n'
    return ''.join(
        f"| {row.Code} | {int(row.start_year)}-{int(row.end_year)} | "
        f"{row.duration:.1f} | {'Có' if row.event else 'Không'} |\n"
        for row in selected.itertuples()
    )


def write_report(spells, medians):
    lines = [
        '# Phạm vi nghiên cứu và tình trạng thoát bẫy thu nhập',
        '',
        '**Ngày tạo:** 2026-09-06  ',
        '**Nguồn:** `survival_data.csv` của branch `main`  ',
        '**Đơn vị phân tích:** spell quốc gia trong một nhóm thu nhập',
        '',
        '## 1. Phạm vi nghiên cứu',
        '',
        '| Khía cạnh | Phạm vi |',
        '|---|---|',
        '| Không gian | Các quốc gia có đủ dữ liệu cho bộ biến main và xuất hiện trong survival sample |',
        '| Thời gian | 2000-2026, tối đa 27 năm mỗi quốc gia |',
        '| Hiện tượng | Thời gian thoát khỏi nhóm thu nhập trung bình |',
        '| Chặng 1 | `LM -> UM`, thoát nhóm thu nhập trung bình thấp |',
        '| Chặng 2 | `UM -> H`, thoát nhóm thu nhập trung bình cao |',
        '| Loại khỏi event | `LM -> H` bị loại; `L -> UM` không được xem là event |',
        '| Main variables | `TFP, GE, AGEDEP, IND, TO, CREDIT, ECI` |',
        '| Branch 5-vars | `TFP, GE, AGEDEP, TO, CREDIT` |',
        '',
        '## 2. Quy tắc phân loại',
        '',
        '- **Đã thoát:** spell có `event = 1` và duration `<=` median duration của các spell có event trong cùng chặng.',
        '- **Chưa thoát:** spell bị censor, hoặc có event nhưng duration `>` median của cùng chặng.',
        '- Median được tính riêng cho LM và UM, không gộp hai chặng.',
        '- “Chưa thoát” bao gồm cả quốc gia bị censor, nên không đồng nghĩa với khẳng định quốc gia đó vĩnh viễn không thể thoát bẫy.',
        '',
        '## 3. Thống kê tổng quát',
        '',
        '| Chỉ số | Giá trị |',
        '|---|---:|',
        f"| Số quốc gia trong survival sample | {spells['Code'].nunique()} |",
        f"| Số spells | {spells['spell_id'].nunique()} |",
        f"| Số event hợp lệ | {int(spells['event'].sum())} |",
        f"| Số spell censored | {int((spells['event'] == 0).sum())} |",
        '',
        '| Chặng | Median (năm) | Spells | Event | Censored | Đã thoát | Chưa thoát |',
        '|---|---:|---:|---:|---:|---:|---:|',
    ]

    for group, transition in [('LM', 'LM -> UM'), ('UM', 'UM -> H')]:
        subset = spells[spells['spell_group'] == group]
        lines.append(
            f"| {transition} | {medians[group]:.1f} | {len(subset)} | "
            f"{int(subset['event'].sum())} | {int((subset['event'] == 0).sum())} | "
            f"{int((subset['status'] == 'Đã thoát').sum())} | "
            f"{int((subset['status'] == 'Chưa thoát').sum())} |"
        )

    for group, transition in [('LM', 'LM -> UM'), ('UM', 'UM -> H')]:
        lines.extend([
            '',
            f'## 4. Danh sách quốc gia: {transition}',
            '',
            '### Đã thoát',
            '',
            '| Quốc gia | Giai đoạn quan sát | Duration (năm) | Event |',
            '|---|---|---:|---|',
            format_country_rows(country_table(spells, group, 'Đã thoát')).rstrip(),
            '',
            '### Chưa thoát',
            '',
            '| Quốc gia | Giai đoạn quan sát | Duration (năm) | Event |',
            '|---|---|---:|---|',
            format_country_rows(country_table(spells, group, 'Chưa thoát')).rstrip(),
        ])

    lines.extend([
        '',
        '## 5. Lưu ý diễn giải',
        '',
        'Danh sách được lập ở cấp spell. Nếu một quốc gia có nhiều spell ở cùng nhóm sau khi tụt hạng, quốc gia đó có thể xuất hiện nhiều lần hoặc có trạng thái khác nhau giữa các spell.',
        '',
        'Phân loại median là mô tả dữ liệu, không thay thế mô hình Cox. Kết luận về tốc độ thoát bẫy nên đọc cùng hazard ratio, khoảng tin cậy và p-value trong `report/cox_model_results.md`.',
        '',
    ])
    REPORT_FILE.write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    survival = pd.read_csv(SURVIVAL_FILE)
    classified, medians = classify_spells(survival)
    write_report(classified, medians)
    print(f'Report saved to: {REPORT_FILE}')
    print(f'Countries: {classified["Code"].nunique()} | Spells: {classified["spell_id"].nunique()}')
