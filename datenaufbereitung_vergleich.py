import pandas as pd
import numpy as np
from scipy.signal import medfilt
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

METADATA = {
    'oskar': {'person_id': '001', 'sex': 1, 'age': 0, 'exercise': 'running', 'diet': 0, 'caffeine': 0, 'sleep_q': 1, 'sleep_h': 0.0, 'wellbeeing': 0, 'cold_hist': 0, 'asthma': 0, 'smoker': 0, 'fitness_level': 1, 'study_modus': 0, 'bmi': 0.0, 'rpm': 0},
    'micheelle': {'person_id': '002', 'sex': 0, 'age': 22, 'exercise': 'running', 'diet': 0, 'caffeine': 0, 'sleep_q': 0, 'sleep_h': 0.5, 'wellbeeing': 11, 'cold_hist': 0, 'asthma': 0, 'smoker': 0, 'fitness_level': 1, 'study_modus': 0, 'bmi': 0.0, 'rpm': 0},
    'eros': {'person_id': '003', 'sex': 1, 'age': 26, 'exercise': 'running', 'diet': 0, 'caffeine': 1, 'sleep_q': 2, 'sleep_h': 8, 'wellbeeing': 20, 'cold_hist': 0, 'asthma': 1, 'smoker': 0, 'fitness_level': 1, 'study_modus': 0, 'bmi': 26, 'rpm': 0}
}

ZHAW_KUERZEL = {'oskar': 'steinosk', 'micheelle': 'linamic', 'eros': 'halero01'}

def clean_bpm(bpm, window=5):
    cleaned = medfilt(bpm, kernel_size=window)
    cleaned = np.where((cleaned < 40) | (cleaned > 200), np.median(cleaned), cleaned)
    return cleaned

def process_person(person, zhaw_id):
    raw_files = sorted(Path("data").glob(f"{zhaw_id}_activity_intensity_*_lsdlpr25.csv"))
    comparisons = []
    
    for raw_file in raw_files:
        intensity = int(raw_file.stem.split('_')[3])
        df = pd.read_csv(raw_file)
        
        bpm_clean = clean_bpm(df['bpm'].values)
        artifacts = np.sum(df['bpm'].values != bpm_clean)
        
        row = {'time': df['time'], 'rr_interval': df['rr_interval'], 'bpm_raw': df['bpm'], 'bpm_clean': bpm_clean, 'intensity': intensity, 'artifacts': artifacts}
        for k, v in METADATA[person].items():
            row[k] = v
        
        df_clean = pd.DataFrame(row)
        df_clean.to_csv(f"data/{zhaw_id}_activity_intensity_{intensity}_cleaned_lsdlpr25.csv", index=False)
        
        comparisons.append({'intensity': intensity, 'raw': df['bpm'].values, 'clean': bpm_clean, 'mean_raw': df['bpm'].mean(), 'mean_clean': bpm_clean.mean(), 'std_raw': df['bpm'].std(), 'std_clean': bpm_clean.std()})
        print(f"✅ {zhaw_id}_activity_intensity_{intensity}_cleaned_lsdlpr25.csv (artifacts: {artifacts})")
    
    return comparisons

def plot_comparison(person, zhaw_id, data):
    fig = make_subplots(rows=2, cols=3, subplot_titles=[f"Intensity {d['intensity']}" for d in data] + [f"Stats {d['intensity']}" for d in data], specs=[[{'type': 'scatter'}, {'type': 'scatter'}, {'type': 'scatter'}], [{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]])
    
    for i, d in enumerate(data, 1):
        fig.add_trace(go.Scatter(y=d['raw'], name=f"Raw {d['intensity']}", opacity=0.6, line=dict(color='red')), row=1, col=i)
        fig.add_trace(go.Scatter(y=d['clean'], name=f"Clean {d['intensity']}", line=dict(color='green')), row=1, col=i)
        fig.add_trace(go.Bar(x=['Mean', 'Std'], y=[d['mean_raw'], d['std_raw']], name=f"Raw {d['intensity']}", marker=dict(color='red'), opacity=0.6), row=2, col=i)
        fig.add_trace(go.Bar(x=['Mean', 'Std'], y=[d['mean_clean'], d['std_clean']], name=f"Clean {d['intensity']}", marker=dict(color='green')), row=2, col=i)
    
    fig.update_layout(height=800, title_text=f"{person.capitalize()} - Raw vs Cleaned BPM", showlegend=False)
    fig.show()

print("=== Datenaufbereitung & Vergleich ===\n")
for person, zhaw_id in ZHAW_KUERZEL.items():
    print(f"Processing {person.capitalize()}...")
    data = process_person(person, zhaw_id)
    plot_comparison(person, zhaw_id, data)
    print()

print("✅ Datenaufbereitung abgeschlossen!")
