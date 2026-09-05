"""Export current main Cox results and trap classification to Excel."""
from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / 'report'
OUTPUT = REPORT_DIR / 'cox_results_main.xlsx'
VARIABLES = ['TFP', 'GE', 'AGEDEP', 'IND', 'TO', 'CREDIT', 'ECI']


def stars(p_value):
    if p_value < 0.01:
        return '***'
    if p_value < 0.05:
        return '**'
    if p_value < 0.10:
        return '*'
    return ''


def load_model_summary(filename):
    summary = pd.read_csv(REPORT_DIR / filename)
    summary['Significance'] = summary['p'].map(stars)
    summary['Hazard Ratio'] = summary.apply(
        lambda row: f"{row['exp(coef)']:.3f}{row['Significance']}", axis=1
    )
    return summary[['covariate', 'coef', 'Hazard Ratio', 'p', 'Significance']].rename(
        columns={'covariate': 'Variable', 'p': 'p-value'}
    )


def trap_summary(data, group):
    spells = data[data['spell_group'] == group].groupby('spell_id').agg(
        duration=('stop', 'max'), event=('event', 'max'),
        **{variable: (variable, 'mean') for variable in VARIABLES}
    ).reset_index()
    median_duration = spells.loc[spells['event'] == 1, 'duration'].median()
    spells['Status'] = 'Chưa thoát'
    spells.loc[(spells['event'] == 1) & (spells['duration'] <= median_duration), 'Status'] = 'Đã thoát'

    rows = []
    for variable in VARIABLES:
        escaped = spells.loc[spells['Status'] == 'Đã thoát', variable]
        trapped = spells.loc[spells['Status'] == 'Chưa thoát', variable]
        rows.append({
            'Group': group,
            'Median duration': median_duration,
            'Variable': variable,
            'Mean - Đã thoát': escaped.mean(),
            'Mean - Chưa thoát': trapped.mean(),
            'Mann-Whitney p-value': mannwhitneyu(escaped, trapped, alternative='two-sided').pvalue,
        })
    return pd.DataFrame(rows), spells


def format_workbook(writer):
    from openpyxl.styles import Font, PatternFill

    for worksheet in writer.book.worksheets:
        worksheet.freeze_panes = 'A2'
        worksheet.auto_filter.ref = worksheet.dimensions
        for cell in worksheet[1]:
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill('solid', fgColor='1F4E78')
        for column in worksheet.columns:
            width = max(len(str(cell.value or '')) for cell in column) + 2
            worksheet.column_dimensions[column[0].column_letter].width = min(width,  thirty := 30)


if __name__ == '__main__':
    data = pd.read_csv(BASE_DIR / 'survival_data.csv')
    with pd.ExcelWriter(OUTPUT, engine='openpyxl') as writer:
        for sheet_name, filename in [
            ('Combined', 'cox_summary_combined.csv'),
            ('LM_to_UM', 'cox_summary_lm.csv'),
            ('UM_to_H', 'cox_summary_um.csv'),
        ]:
            load_model_summary(filename).to_excel(writer, sheet_name=sheet_name, index=False)

        for group, sheet_name in [('LM', 'Trap_LM'), ('UM', 'Trap_UM')]:
            result, _ = trap_summary(data, group)
            result.to_excel(writer, sheet_name=sheet_name, index=False)

        for sheet_name, filename in [
            ('PH_Combined', 'ph_assumptions_combined.csv'),
            ('PH_LM', 'ph_assumptions_lm.csv'),
            ('PH_UM', 'ph_assumptions_um.csv'),
        ]:
            pd.read_csv(REPORT_DIR / filename).to_excel(writer, sheet_name=sheet_name, index=False)

        format_workbook(writer)
    print(f'Excel report saved to: {OUTPUT}')
