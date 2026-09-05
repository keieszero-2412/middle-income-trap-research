"""
Survival Data Preparation for Cox PH Model
Focus: Middle Income Trap (LM -> UM, UM -> H transitions only)
Branch: credit-and-to (Variables: AGEDEP, GE, IND, TO, CREDIT)
"""
import pandas as pd

df = pd.read_csv('final_lifelines_data_clean.csv')
df.sort_values(by=['Code', 'Year'], inplace=True)

income_order = {'L': 0, 'LM': 1, 'UM': 2, 'H': 3}
all_spells = []

for code, grp in df.groupby('Code'):
    rows = grp.reset_index(drop=True)
    spell_start_idx = 0
    spell_group = rows.loc[0, 'IncomeGroup']

    for i in range(1, len(rows)):
        current_group = rows.loc[i, 'IncomeGroup']
        if current_group != spell_group:
            if spell_group in ['LM', 'UM']:
                is_upward = income_order.get(current_group, -1) > income_order.get(spell_group, -1)
                spell_rows = rows.iloc[spell_start_idx:i]
                duration_counter = 0
                for _, row in spell_rows.iterrows():
                    all_spells.append({
                        'Code': code, 'spell_group': spell_group,
                        'start': duration_counter, 'stop': duration_counter + 1,
                        'event': 0,
                        'AGEDEP': row['AGEDEP'], 'GE': row['GE'],
                        'IND': row['IND'], 'TO': row['TO'], 'CREDIT': row['CREDIT'],
                        'Year': row['Year']
                    })
                    duration_counter += 1
                if is_upward and len(all_spells) > 0:
                    all_spells[-1]['event'] = 1
            spell_start_idx = i
            spell_group = current_group

    if spell_group in ['LM', 'UM']:
        spell_rows = rows.iloc[spell_start_idx:]
        duration_counter = 0
        for _, row in spell_rows.iterrows():
            all_spells.append({
                'Code': code, 'spell_group': spell_group,
                'start': duration_counter, 'stop': duration_counter + 1,
                'event': 0,
                'AGEDEP': row['AGEDEP'], 'GE': row['GE'],
                'IND': row['IND'], 'TO': row['TO'], 'CREDIT': row['CREDIT'],
                'Year': row['Year']
            })
            duration_counter += 1

df_survival = pd.DataFrame(all_spells)
df_survival.to_csv('survival_data.csv', index=False)

total_spells = df_survival.groupby(['Code', 'spell_group']).ngroups
total_events = df_survival.groupby(['Code', 'spell_group'])['event'].max().sum()
lm_spells = df_survival[df_survival['spell_group'] == 'LM'].groupby('Code').ngroups
um_spells = df_survival[df_survival['spell_group'] == 'UM'].groupby('Code').ngroups
lm_events = df_survival[df_survival['spell_group'] == 'LM'].groupby('Code')['event'].max().sum()
um_events = df_survival[df_survival['spell_group'] == 'UM'].groupby('Code')['event'].max().sum()

print("=== SURVIVAL DATA (credit-and-to) ===")
print(f"Rows: {len(df_survival)} | Spells: {total_spells}")
print(f"LM: {lm_spells} ({lm_events} events) | UM: {um_spells} ({um_events} events)")
print(f"Total events: {int(total_events)} | Censored: {int(total_spells - total_events)}")
