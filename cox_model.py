"""
Cox PH Model - Branch: credit-and-to
Variables: AGEDEP, GE, IND, TO, CREDIT
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter, KaplanMeierFitter
import os
os.makedirs('report', exist_ok=True)

df = pd.read_csv('survival_data.csv')

print("=" * 60)
print("COX PH MODEL - CREDIT-AND-TO BRANCH")
print("=" * 60)

# MODEL 1: Combined
print("\n### MODEL 1: COMBINED (LM + UM) ###")
df['is_UM'] = (df['spell_group'] == 'UM').astype(int)
cph_combined = CoxPHFitter()
cph_combined.fit(
    df[['start', 'stop', 'event', 'is_UM', 'AGEDEP', 'GE', 'IND', 'TO', 'CREDIT']],
    duration_col='stop', event_col='event', entry_col='start'
)
cph_combined.print_summary()
fig, ax = plt.subplots(figsize=(10, 6))
cph_combined.plot(ax=ax)
ax.set_title('Cox PH - Hazard Ratios (Combined LM+UM) [CREDIT+TO branch]', fontsize=14)
plt.tight_layout()
plt.savefig('report/cox_forest_combined.png', dpi=150)
plt.close()

# MODEL 2: LM only
print("\n### MODEL 2: LM ONLY (LM -> UM) ###")
df_lm = df[df['spell_group'] == 'LM'].copy()
cph_lm = CoxPHFitter()
cph_lm.fit(
    df_lm[['start', 'stop', 'event', 'AGEDEP', 'GE', 'IND', 'TO', 'CREDIT']],
    duration_col='stop', event_col='event', entry_col='start'
)
cph_lm.print_summary()
fig, ax = plt.subplots(figsize=(10, 6))
cph_lm.plot(ax=ax)
ax.set_title('Cox PH - LM to UM [CREDIT+TO branch]', fontsize=14)
plt.tight_layout()
plt.savefig('report/cox_forest_lm.png', dpi=150)
plt.close()

# MODEL 3: UM only
print("\n### MODEL 3: UM ONLY (UM -> H) ###")
df_um = df[df['spell_group'] == 'UM'].copy()
cph_um = CoxPHFitter()
cph_um.fit(
    df_um[['start', 'stop', 'event', 'AGEDEP', 'GE', 'IND', 'TO', 'CREDIT']],
    duration_col='stop', event_col='event', entry_col='start'
)
cph_um.print_summary()
fig, ax = plt.subplots(figsize=(10, 6))
cph_um.plot(ax=ax)
ax.set_title('Cox PH - UM to H [CREDIT+TO branch]', fontsize=14)
plt.tight_layout()
plt.savefig('report/cox_forest_um.png', dpi=150)
plt.close()

# Kaplan-Meier
print("\n### KAPLAN-MEIER ###")
df_spell = df.groupby(['Code', 'spell_group']).agg(duration=('stop', 'max'), event=('event', 'max')).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
kmf = KaplanMeierFitter()
for gn, gd in df_spell.groupby('spell_group'):
    kmf.fit(gd['duration'], gd['event'], label=f'{gn} Group')
    kmf.plot_survival_function(ax=ax)
ax.set_title('Kaplan-Meier Survival Curves [CREDIT+TO branch]', fontsize=14)
ax.set_xlabel('Years in Income Group'); ax.set_ylabel('Survival Probability')
ax.legend(fontsize=12); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('report/kaplan_meier.png', dpi=150)
plt.close()

# Save CSVs
cph_combined.summary.to_csv('report/cox_summary_combined.csv')
cph_lm.summary.to_csv('report/cox_summary_lm.csv')
cph_um.summary.to_csv('report/cox_summary_um.csv')
print("\n=> DONE! All outputs saved to report/")
