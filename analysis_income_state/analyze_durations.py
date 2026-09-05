import pandas as pd

df = pd.read_csv('income_data_transitioned.csv')
years = df.columns[1:]
rank = {'L': 1, 'LM': 2, 'UM': 3, 'H': 4}

up_then_down = []
transition_durations = []

for _, row in df.iterrows():
    code = row['Code']
    valid_data = row[years].dropna()
    
    if len(valid_data) < 2:
        continue
        
    has_up = False
    
    current_state = None
    start_year = None
    count = 0
    
    for year, state in valid_data.items():
        if state not in rank:
            continue
            
        if current_state is None:
            current_state = state
            start_year = int(year)
            count = 1
        elif state == current_state:
            count += 1
        else:
            if rank[state] > rank[current_state]:
                has_up = True
                transition_durations.append({
                    'Code': code,
                    'From': current_state,
                    'To': state,
                    'Duration': count,
                    'Transition_Year': year,
                    'Is_Left_Censored': start_year == int(years[0])
                })
            elif rank[state] < rank[current_state]:
                if has_up:
                    up_then_down.append({
                        'Code': code,
                        'From': current_state,
                        'To': state,
                        'Year': year
                    })
            
            current_state = state
            start_year = int(year)
            count = 1

print("=== 1. COUNTRIES THAT DROPPED AFTER TRANSITIONING UP ===")
if not up_then_down:
    print("No countries found.")
else:
    for event in up_then_down:
        print(f"- {event['Code']}: Dropped from {event['From']} to {event['To']} in {event['Year']}")

print("\n=== 2. TRANSITION DURATIONS (YEARS SPENT IN PREVIOUS GROUP) ===")
tdf = pd.DataFrame(transition_durations)
if not tdf.empty:
    summary = tdf.groupby(['From', 'To'])['Duration'].agg(
        Count='count',
        Mean='mean',
        Median='median',
        Min='min',
        Max='max'
    )
    print(summary.round(2).to_string())
    
    tdf.to_csv('transition_durations.csv', index=False)
    print("\n=> Detailed durations saved to 'transition_durations.csv'.")
