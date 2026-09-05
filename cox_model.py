"""Run the main Cox PH branch with all model covariates."""
import io
import os
from contextlib import redirect_stdout

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
FULL_COVARIATES = ['TFP', 'GE', 'AGEDEP', 'IND', 'TO', 'CREDIT', 'ECI']


def check_ph(model, data, output_path):
    """Check PH and fall back to time interactions for left-truncated data."""
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            model.check_assumptions(data, p_value_threshold=0.05, show_plots=False)
        status = 'completed'
    except Exception as exc:
        buffer.write(f'Schoenfeld check unavailable: {type(exc).__name__}: {exc}\n')
        covariates = [column for column in data.columns if column not in {'start', 'stop', 'event', 'Code'}]
        interaction_data = data.copy()
        log_stop = np.log(np.maximum(interaction_data['stop'], 1))
        interaction_columns = []
        for column in covariates:
            interaction_column = f'{column}_x_log_stop'
            interaction_data[interaction_column] = interaction_data[column] * log_stop
            interaction_columns.append(interaction_column)

        interaction_model = CoxPHFitter()
        interaction_model.fit(
            interaction_data[['start', 'stop', 'event', 'Code'] + covariates + interaction_columns],
            duration_col='stop', event_col='event', entry_col='start', cluster_col='Code'
        )
        interaction_summary = interaction_model.summary.loc[interaction_columns, ['coef', 'p']]
        buffer.write('\nFallback time-interaction test (covariate x log(stop)):\n')
        buffer.write(interaction_summary.to_string())
        buffer.write('\nInterpretation: p < 0.05 suggests a time-varying effect and possible PH violation.\n')
        interaction_summary.to_csv(output_path.replace('.txt', '.csv'))
        status = 'fallback_time_interaction'
    with open(output_path, 'w', encoding='utf-8') as report_file:
        report_file.write(f'Status: {status}\n\n{buffer.getvalue()}')
    print(f'PH check ({status}): {output_path}')


def fit_model(data, covariates, label, output_suffix=''):
    model_data = data[['start', 'stop', 'event', 'Code'] + covariates].copy()
    model = CoxPHFitter()
    model.fit(model_data, duration_col='stop', event_col='event', entry_col='start', cluster_col='Code')
    model.print_summary()
    check_ph(model, model_data, f'report/ph_assumptions_{label}{output_suffix}.txt')
    model.summary.to_csv(f'report/cox_summary_{label}{output_suffix}.csv')

    fig, ax = plt.subplots(figsize=(10, 6))
    model.plot(ax=ax)
    ax.set_title(f'Cox PH - {label} [Robust SE]', fontsize=14)
    plt.tight_layout()
    plt.savefig(f'report/cox_forest_{label}{output_suffix}.png', dpi=150)
    plt.close()
    return model


def run_branch(covariates, output_suffix='', branch_name='main'):
    os.makedirs('report', exist_ok=True)
    df = pd.read_csv('survival_data.csv')
    missing = [column for column in covariates if column not in df.columns]
    if missing:
        raise ValueError(f'Missing required covariates for {branch_name}: {", ".join(missing)}')

    print('=' * 60)
    print(f'COX PH MODEL - {branch_name.upper()} ({", ".join(covariates)})')
    print('=' * 60)
    df['is_UM'] = (df['spell_group'] == 'UM').astype(int)
    combined = fit_model(df, covariates + ['is_UM'], 'combined', output_suffix)
    lm = fit_model(df[df['spell_group'] == 'LM'], covariates, 'lm', output_suffix)
    um = fit_model(df[df['spell_group'] == 'UM'], covariates, 'um', output_suffix)

    df_spell = df.groupby(['spell_id', 'spell_group']).agg(duration=('stop', 'max'), event=('event', 'max')).reset_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    kmf = KaplanMeierFitter()
    for group_name, group_data in df_spell.groupby('spell_group'):
        kmf.fit(group_data['duration'], group_data['event'], label=f'{group_name} Group')
        kmf.plot_survival_function(ax=ax)
    ax.set_title(f'Kaplan-Meier Survival Curves [{branch_name}]')
    ax.set_xlabel('Years in Income Group')
    ax.set_ylabel('Survival Probability')
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'report/kaplan_meier{output_suffix}.png', dpi=150)
    plt.close()
    return combined, lm, um


if __name__ == '__main__':
    run_branch(FULL_COVARIATES, branch_name='main')
