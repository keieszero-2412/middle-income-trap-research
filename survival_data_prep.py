"""
Survival Data Preparation for Cox PH Model
Focus: Middle Income Trap (LM -> UM, UM -> H transitions only)
Branch: main (Variables: AGEDEP, GE, IND, TO)

Output: survival_data.csv with columns:
  Code, spell_group, start, stop, event, AGEDEP, GE, IND, TO
"""
import pandas as pd

df = pd.read_csv('final_lifelines_data_clean.csv')
df.sort_values(by=['Code', 'Year'], inplace=True)

# Only keep Middle Income groups (LM and UM) - the "trap" we're studying
# We also need to know when they transition to the NEXT group
income_order = {'L': 0, 'LM': 1, 'UM': 2, 'H': 3}

all_spells = []

for code, grp in df.groupby('Code'):
    rows = grp.reset_index(drop=True)
    
    # Track spells: consecutive years in the same income group
    spell_start_idx = 0
    spell_group = rows.loc[0, 'IncomeGroup']
    
    for i in range(1, len(rows)):
        current_group = rows.loc[i, 'IncomeGroup']
        
        if current_group != spell_group:
            # A transition happened! Record the spell if it was LM or UM
            if spell_group in ['LM', 'UM']:
                # Check if this is an UPWARD transition
                is_upward = income_order.get(current_group, -1) > income_order.get(spell_group, -1)
                
                # Build time-varying rows for this spell
                spell_rows = rows.iloc[spell_start_idx:i]
                duration_counter = 0
                for _, row in spell_rows.iterrows():
                    all_spells.append({
                        'Code': code,
                        'spell_group': spell_group,
                        'start': duration_counter,
                        'stop': duration_counter + 1,
                        'event': 0,  # Not the last row yet
                        'AGEDEP': row['AGEDEP'],
                        'GE': row['GE'],
                        'IND': row['IND'],
                        'TO': row['TO'],
                        'Year': row['Year']
                    })
                    duration_counter += 1
                
                # Mark the LAST row of the spell
                if is_upward and len(all_spells) > 0:
                    all_spells[-1]['event'] = 1  # Transition event!
                # If downward transition, we still mark event=0 (censored, not a "graduation")
            
            # Start new spell
            spell_start_idx = i
            spell_group = current_group
    
    # Handle the LAST spell (still ongoing at end of data = censored)
    if spell_group in ['LM', 'UM']:
        spell_rows = rows.iloc[spell_start_idx:]
        duration_counter = 0
        for _, row in spell_rows.iterrows():
            all_spells.append({
                'Code': code,
                'spell_group': spell_group,
                'start': duration_counter,
                'stop': duration_counter + 1,
                'event': 0,  # Censored - no transition observed
                'AGEDEP': row['AGEDEP'],
                'GE': row['GE'],
                'IND': row['IND'],
                'TO': row['TO'],
                'Year': row['Year']
            })
            duration_counter += 1

df_survival = pd.DataFrame(all_spells)

# Summary statistics
total_spells = df_survival.groupby(['Code', 'spell_group']).ngroups
total_events = df_survival.groupby(['Code', 'spell_group'])['event'].max().sum()
total_censored = total_spells - total_events

lm_events = df_survival[df_survival['spell_group'] == 'LM'].groupby('Code')['event'].max().sum()
um_events = df_survival[df_survival['spell_group'] == 'UM'].groupby('Code')['event'].max().sum()

lm_spells = df_survival[df_survival['spell_group'] == 'LM'].groupby('Code').ngroups
um_spells = df_survival[df_survival['spell_group'] == 'UM'].groupby('Code').ngroups

print("=== SURVIVAL DATA SUMMARY ===")
print(f"Total observation rows: {len(df_survival)}")
print(f"Total spells (country-group periods): {total_spells}")
print(f"  - LM spells: {lm_spells} ({lm_events} graduated to UM)")
print(f"  - UM spells: {um_spells} ({um_events} graduated to H)")
print(f"Total events (upward transitions): {int(total_events)}")
print(f"Total censored (still in same group): {int(total_censored)}")

df_survival.to_csv('survival_data.csv', index=False)
print("\n=> Saved to 'survival_data.csv'")
print(f"Columns: {df_survival.columns.tolist()}")
