"""
Cox Proportional Hazards Model for Middle Income Trap
Focus: LM -> UM and UM -> H transitions
Uses time-varying covariates (counting process format)
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter, KaplanMeierFitter

df = pd.read_csv('survival_data.csv')

print("=" * 60)
print("COX PROPORTIONAL HAZARDS MODEL - MIDDLE INCOME TRAP")
print("=" * 60)

# ============================================================
# MODEL 1: Combined (LM + UM together)
# ============================================================
print("\n### MODEL 1: COMBINED (LM + UM) ###")

# Add dummy variable for spell_group (1 = UM, 0 = LM)
df['is_UM'] = (df['spell_group'] == 'UM').astype(int)

cph_combined = CoxPHFitter()
cph_combined.fit(
    df[['start', 'stop', 'event', 'is_UM', 'AGEDEP', 'GE', 'IND', 'TO']],
    duration_col='stop',
    event_col='event',
    entry_col='start'
)
cph_combined.print_summary()

# Save forest plot
fig, ax = plt.subplots(figsize=(10, 6))
cph_combined.plot(ax=ax)
ax.set_title('Cox PH Model - Hazard Ratios (Combined LM + UM)', fontsize=14)
plt.tight_layout()
plt.savefig('report/cox_forest_combined.png', dpi=150)
plt.close()
print("=> Saved: report/cox_forest_combined.png")

# ============================================================
# MODEL 2: LM only (Lower-Middle -> Upper-Middle)
# ============================================================
print("\n### MODEL 2: LM ONLY (LM -> UM) ###")

df_lm = df[df['spell_group'] == 'LM'].copy()

cph_lm = CoxPHFitter()
cph_lm.fit(
    df_lm[['start', 'stop', 'event', 'AGEDEP', 'GE', 'IND', 'TO']],
    duration_col='stop',
    event_col='event',
    entry_col='start'
)
cph_lm.print_summary()

fig, ax = plt.subplots(figsize=(10, 6))
cph_lm.plot(ax=ax)
ax.set_title('Cox PH Model - LM to UM Transition', fontsize=14)
plt.tight_layout()
plt.savefig('report/cox_forest_lm.png', dpi=150)
plt.close()
print("=> Saved: report/cox_forest_lm.png")

# ============================================================
# MODEL 3: UM only (Upper-Middle -> High)
# ============================================================
print("\n### MODEL 3: UM ONLY (UM -> H) ###")

df_um = df[df['spell_group'] == 'UM'].copy()

cph_um = CoxPHFitter()
cph_um.fit(
    df_um[['start', 'stop', 'event', 'AGEDEP', 'GE', 'IND', 'TO']],
    duration_col='stop',
    event_col='event',
    entry_col='start'
)
cph_um.print_summary()

fig, ax = plt.subplots(figsize=(10, 6))
cph_um.plot(ax=ax)
ax.set_title('Cox PH Model - UM to H Transition', fontsize=14)
plt.tight_layout()
plt.savefig('report/cox_forest_um.png', dpi=150)
plt.close()
print("=> Saved: report/cox_forest_um.png")

# ============================================================
# KAPLAN-MEIER CURVES
# ============================================================
print("\n### KAPLAN-MEIER SURVIVAL CURVES ###")

# Get duration and event per spell (last row of each spell)
df_spell = df.groupby(['Code', 'spell_group']).agg(
    duration=('stop', 'max'),
    event=('event', 'max')
).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
kmf = KaplanMeierFitter()

for group_name, group_data in df_spell.groupby('spell_group'):
    kmf.fit(group_data['duration'], group_data['event'], label=f'{group_name} Group')
    kmf.plot_survival_function(ax=ax)

ax.set_title('Kaplan-Meier Survival Curves by Income Group', fontsize=14)
ax.set_xlabel('Years in Income Group', fontsize=12)
ax.set_ylabel('Survival Probability (Probability of NOT transitioning)', fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('report/kaplan_meier.png', dpi=150)
plt.close()
print("=> Saved: report/kaplan_meier.png")

# ============================================================
# PH ASSUMPTION TEST (Schoenfeld Residuals)
# ============================================================
print("\n### PROPORTIONAL HAZARDS TEST (Combined Model) ###")
try:
    results = cph_combined.check_assumptions(df[['start', 'stop', 'event', 'is_UM', 'AGEDEP', 'GE', 'IND', 'TO']], 
                                              p_value_threshold=0.05,
                                              show_plots=False)
    print("PH assumption test completed.")
except Exception as e:
    print(f"PH test note: {e}")

# ============================================================
# SAVE SUMMARY TABLES TO CSV
# ============================================================
cph_combined.summary.to_csv('report/cox_summary_combined.csv')
cph_lm.summary.to_csv('report/cox_summary_lm.csv')
cph_um.summary.to_csv('report/cox_summary_um.csv')
print("\n=> All summary tables saved to report/ folder.")
print("=> DONE!")
