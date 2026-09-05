"""Prepare counting-process survival data for the valid income transitions."""
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

df = pd.read_csv('final_lifelines_data_clean.csv')
df.sort_values(by=['Code', 'Year'], inplace=True)

potential_cols = ['TFP', 'GE', 'AGEDEP', 'IND', 'TO', 'CREDIT', 'ECI']
missing_cols = [col for col in potential_cols if col not in df.columns]
if missing_cols:
    raise ValueError(f'Missing required covariates: {", ".join(missing_cols)}')
cols_to_use = potential_cols

valid_transitions = {('LM', 'UM'), ('UM', 'H')}
all_spells = []


def append_spell(rows, code, spell_group, spell_id, event):
    for duration_counter, (_, row) in enumerate(rows.iterrows()):
        spell_data = {
            'Code': code,
            'spell_id': spell_id,
            'spell_group': spell_group,
            'start': duration_counter,
            'stop': duration_counter + 1,
            'event': int(event and duration_counter == len(rows) - 1),
            'Year': row['Year']
        }
        for col in cols_to_use:
            spell_data[col] = row[col]
        all_spells.append(spell_data)

for code, grp in df.groupby('Code'):
    rows = grp.reset_index(drop=True)
    spell_start_idx = 0
    spell_group = rows.loc[0, 'IncomeGroup']
    spell_counter = 1

    for i in range(1, len(rows)):
        current_group = rows.loc[i, 'IncomeGroup']
        if current_group != spell_group:
            if spell_group in ['LM', 'UM']:
                transition = (spell_group, current_group)
                spell_rows = rows.iloc[spell_start_idx:i]
                spell_id = f"{code}_{spell_counter}"
                # A direct LM -> H jump is not an LM -> UM event or a valid censoring.
                if transition in valid_transitions:
                    append_spell(spell_rows, code, spell_group, spell_id, event=True)
                elif transition != ('LM', 'H'):
                    append_spell(spell_rows, code, spell_group, spell_id, event=False)
                spell_counter += 1
            spell_start_idx = i
            spell_group = current_group

    if spell_group in ['LM', 'UM']:
        spell_rows = rows.iloc[spell_start_idx:]
        spell_id = f"{code}_{spell_counter}"
        append_spell(spell_rows, code, spell_group, spell_id, event=False)

df_survival = pd.DataFrame(all_spells)
df_survival.to_csv('survival_data.csv', index=False)

total_spells = df_survival['spell_id'].nunique()
total_events = df_survival.groupby('spell_id')['event'].max().sum()

lm_spells = df_survival[df_survival['spell_group'] == 'LM']['spell_id'].nunique()
um_spells = df_survival[df_survival['spell_group'] == 'UM']['spell_id'].nunique()
lm_events = df_survival[df_survival['spell_group'] == 'LM'].groupby('spell_id')['event'].max().sum()
um_events = df_survival[df_survival['spell_group'] == 'UM'].groupby('spell_id')['event'].max().sum()

print("=== SURVIVAL DATA (valid LM -> UM and UM -> H transitions) ===")
print(f"Rows: {len(df_survival)} | Unique Spells: {total_spells}")
print(f"LM: {lm_spells} ({lm_events} events) | UM: {um_spells} ({um_events} events)")
print(f"Total events: {int(total_events)} | Censored: {int(total_spells - total_events)}")
