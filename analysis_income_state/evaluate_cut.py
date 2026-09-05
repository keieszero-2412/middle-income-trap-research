import pandas as pd

df_events = pd.read_csv('transition_events.csv')
df_events['Year'] = pd.to_numeric(df_events['Year'], errors='coerce')

total_events = len(df_events)
events_before_2000 = df_events[df_events['Year'] < 2000]
events_after_2000 = df_events[df_events['Year'] >= 2000]
events_after_2000_to_2024 = df_events[(df_events['Year'] >= 2000) & (df_events['Year'] <= 2024)]

print(f"Total upgrade events: {total_events}")
print(f"Events BEFORE 2000 (1991-1999): {len(events_before_2000)} ({len(events_before_2000)/total_events*100:.2f}%)")
print(f"Events FROM 2000 onwards: {len(events_after_2000)} ({len(events_after_2000)/total_events*100:.2f}%)")
print(f"Events FROM 2000 to 2024: {len(events_after_2000_to_2024)} ({len(events_after_2000_to_2024)/total_events*100:.2f}%)")
