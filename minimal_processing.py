"""
Minimal Heart Rate Data Processing with Timestamps
Simple data cleaning with median filter and metadata management
"""

import pandas as pd
import numpy as np
from scipy.signal import medfilt
import json
import os
from datetime import datetime

# Updated to match homework requirements
METADATA = {
    'oskar': {
        'person_id': '001',  # TODO: Fill in your assigned ID
        'sex': 1,  # 0 = weiblich, 1 = männlich
        'age': 0,  # TODO: Fill in
        'exercise': 'running',  # running, stairs, lunges, mountain_climbers
        'diet': 0,  # 0 = Fleisch, 1 = Vegetarisch, 2 = Vegan
        'caffeine': 0,  # 0 = nein, 1 = ja
        'sleep_q': 1,  # 0 = schlecht, 1 = mittel, 2 = gut
        'sleep_h': 0.0,  # Schlafdauer in Stunden
        'wellbeeing': 0,  # WHO-5 Fragebogen (0-25 Punkte)
        'cold_hist': 0,  # 0 = nein, 1 = ja
        'asthma': 0,  # 0 = nein, 1 = ja
        'smoker': 0,  # 0 = nein, 1 = ja
        'fitness_level': 1,  # 0 = low, 1 = medium, 2 = high
        'study_modus': 0,  # 0 = vollzeit, 1 = teilzeit
        'bmi': 0.0,  # Body-Mass-Index
        'rpm': 0,  # Wiederholungen pro Minute (Kadenz)
    },
    'micheelle': {
        'person_id': '002',  # TODO: Fill in your assigned ID
        'sex': 0,  # 0 = weiblich, 1 = männlich
        'age': 22,  # TODO: Fill in
        'exercise': 'running',  # running, stairs, lunges, mountain_climbers
        'diet': 0,  # 0 = Fleisch, 1 = Vegetarisch, 2 = Vegan
        'caffeine': 0,  # 0 = nein, 1 = ja
        'sleep_q': 0,  # 0 = schlecht, 1 = mittel, 2 = gut
        'sleep_h': 0.5,  # Schlafdauer in Stunden
        'wellbeeing': 11,  # WHO-5 Fragebogen (0-25 Punkte)
        'cold_hist': 0,  # 0 = nein, 1 = ja
        'asthma': 0,  # 0 = nein, 1 = ja
        'smoker': 0,  # 0 = nein, 1 = ja
        'fitness_level': 1,  # 0 = low, 1 = medium, 2 = high
        'study_modus': 0,  # 0 = vollzeit, 1 = teilzeit
        'bmi': 0.0,  # Body-Mass-Index
        'rpm': 0,  # Wiederholungen pro Minute (Kadenz)
    },
    'eros': {
        'person_id': '003',  # TODO: Fill in your assigned ID
        'sex': 1,  # 0 = weiblich, 1 = männlich
        'age': 26,  # TODO: Fill in
        'exercise': 'running',  # running, stairs, lunges, mountain_climbers
        'diet': 0,  # 0 = Fleisch, 1 = Vegetarisch, 2 = Vegan
        'caffeine': 1,  # 0 = nein, 1 = ja
        'sleep_q': 2,  # 0 = schlecht, 1 = mittel, 2 = gut
        'sleep_h': 8,  # Schlafdauer in Stunden
        'wellbeeing': 20,  # WHO-5 Fragebogen (0-25 Punkte)
        'cold_hist': 0,  # 0 = nein, 1 = ja
        'asthma': 1,  # 0 = nein, 1 = ja
        'smoker': 0,  # 0 = nein, 1 = ja
        'fitness_level': 1,  # 0 = low, 1 = medium, 2 = high
        'study_modus': 0,  # 0 = vollzeit, 1 = teilzeit
        'bmi': 26,  # Body-Mass-Index
        'rpm': 0,  # Wiederholungen pro Minute (Kadenz)
    }
}

# ZHAW Kürzel mapping for homework submission
ZHAW_KUERZEL = {
    'oskar': 'steinosk',
    'micheelle': 'linamic',
    'eros': 'halero01'
}

# Timestamp mapping based on measurement order (Oskar → Eros → Michelle)
TIMESTAMP_MAPPING = {
    'oskar_int_1.txt': {'person': 'oskar', 'intensity': 1},
    'oskar_int_2.txt': {'person': 'oskar', 'intensity': 2},
    'oskar_int_3.txt': {'person': 'oskar', 'intensity': 3},
    'Oskar_int_1.txt': {'person': 'oskar', 'intensity': 1},
    'Oskar_int_2.txt': {'person': 'oskar', 'intensity': 2},
    'Oskar_int_3.txt': {'person': 'oskar', 'intensity': 3},
    'Eros_int_1.txt': {'person': 'eros', 'intensity': 1},
    'Eros_int_2.txt': {'person': 'eros', 'intensity': 2},
    'Eros_int_3.txt': {'person': 'eros', 'intensity': 3},
    'Micheelle_int_1.txt': {'person': 'micheelle', 'intensity': 1},
    'Micheelle_int_2.txt': {'person': 'micheelle', 'intensity': 2},
    'Micheelle_int_3.txt': {'person': 'micheelle', 'intensity': 3},
    'Michelle_int_3.txt': {'person': 'micheelle', 'intensity': 3}
}

def load_rr_data(filepath):
    """Minimal RR data loader"""
    with open(filepath, 'r') as f:
        rr_intervals = [int(line.strip()) for line in f if line.strip()]
    return np.array(rr_intervals)

def parse_timestamp_filename(filename):
    """Extract datetime from timestamp filename"""
    try:
        timestamp_str = filename.replace('.txt', '')
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H-%M-%S')
    except:
        return None

def calculate_bpm(rr_intervals):
    """Convert RR intervals to BPM"""
    return 60000 / rr_intervals

def clean_with_median_filter(bmp_data, window_size=5):
    """
    Enhanced data cleaning with median filter and interpolation
    Homework requirement 1: Datenbereinigung
    """
    # Apply median filter
    cleaned_bmp = medfilt(bmp_data, kernel_size=window_size)
    
    # Remove extreme outliers (40-200 BPM as per homework)
    cleaned_bmp = np.where(cleaned_bmp < 40, np.median(cleaned_bmp), cleaned_bmp)
    cleaned_bmp = np.where(cleaned_bmp > 200, np.median(cleaned_bmp), cleaned_bmp)
    
    # Interpolate any remaining missing/invalid values
    mask = np.isnan(cleaned_bmp) | (cleaned_bmp <= 0)
    if np.any(mask):
        # Linear interpolation for missing values
        indices = np.arange(len(cleaned_bmp))
        cleaned_bmp[mask] = np.interp(indices[mask], indices[~mask], cleaned_bmp[~mask])
    
    return cleaned_bmp

def convert_intensity_to_numeric(intensity_str):
    """Convert intensity string to numeric as per homework requirements"""
    intensity_map = {'Low': 0, 'Medium': 1, 'High': 2}
    return intensity_map.get(intensity_str, 0)

def create_homework_csv(all_results):
    """
    Create individual CSV files for each person according to homework requirements
    Homework requirement 2: Datenaufbereitung
    """
    # ZHAW Kürzel mapping
    kuerzel_mapping = {
        'oskar': 'steinosk',
        'micheelle': 'linamic', 
        'eros': 'halero01'
    }
    
    for person, data in all_results.items():
        person_metadata = METADATA[person]
        zhaw_kuerzel = kuerzel_mapping[person]
        
        all_rows = []
        
        for intensity_str, measurement in data.items():
            intensity_numeric = convert_intensity_to_numeric(intensity_str)
            
            # Create rows for each time point
            time_points = measurement['time']
            bpm_cleaned = measurement['bpm_cleaned']
            
            # Parse timestamp for each measurement
            measurement_time = datetime.fromisoformat(measurement['timestamp']) if measurement['timestamp'] else None
            
            for i, (time_point, bpm_value) in enumerate(zip(time_points, bpm_cleaned)):
                # Calculate absolute timestamp for this data point
                if measurement_time:
                    absolute_time = measurement_time + pd.Timedelta(seconds=time_point)
                    time_str = absolute_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]  # Include milliseconds
                else:
                    time_str = f"2025-10-16 00:00:{time_point:.3f}"
                
                row = {
                    'time': time_str,
                    'person_id': person_metadata['person_id'],
                    'sex': person_metadata['sex'],
                    'age': person_metadata['age'],
                    'exercise': person_metadata['exercise'],
                    'diet': person_metadata['diet'],
                    'caffeine': person_metadata['caffeine'],
                    'sleep_q': person_metadata['sleep_q'],
                    'sleep_h': person_metadata['sleep_h'],
                    'wellbeeing': person_metadata['wellbeeing'],
                    'cold_hist': person_metadata['cold_hist'],
                    'asthma': person_metadata['asthma'],
                    'smoker': person_metadata['smoker'],
                    'fitness_level': person_metadata['fitness_level'],
                    'study_modus': person_metadata['study_modus'],
                    'intensity': intensity_numeric,
                    'bmi': person_metadata['bmi'],
                    'rpm': person_metadata['rpm'],
                    'bpm': round(bpm_value, 2)
                }
                all_rows.append(row)
        
        # Create DataFrame for this person
        df = pd.DataFrame(all_rows)
        
        # Sort by time and intensity
        df = df.sort_values(['intensity', 'time']).reset_index(drop=True)
        
        # Save as CSV with homework naming convention
        filename = f"data/{zhaw_kuerzel}_activity_lsdlpr25.csv"
        df.to_csv(filename, index=False)
        
        print(f"✅ {person.capitalize()} CSV saved as: {filename} ({len(df)} data points)")

def process_person_data(person_name, data_dir):
    """Process all intensity levels for one person using timestamped files"""
    results = {}
    
    for timestamp_file, mapping in TIMESTAMP_MAPPING.items():
        if mapping['person'] == person_name.lower():
            filepath = os.path.join(data_dir, timestamp_file)
            if os.path.exists(filepath):
                rr_data = load_rr_data(filepath)
                bpm_raw = calculate_bpm(rr_data)
                bpm_cleaned = clean_with_median_filter(bpm_raw)
                time_seconds = np.cumsum(rr_data) / 1000.0
                measurement_time = parse_timestamp_filename(timestamp_file)
                
                intensity = mapping['intensity']
                intensity_str = {1: 'Low', 2: 'Medium', 3: 'High'}[intensity]
                
                results[intensity_str] = {
                    'time': time_seconds,
                    'bpm_raw': bpm_raw,
                    'bpm_cleaned': bpm_cleaned,
                    'duration': time_seconds[-1],
                    'mean_bpm': np.mean(bpm_cleaned),
                    'artifacts_removed': np.sum(bpm_raw != bpm_cleaned),
                    'timestamp': measurement_time.isoformat() if measurement_time else None,
                    'source_file': timestamp_file
                }
                print(f"  Intensity {intensity} ({intensity_str}): {len(bpm_cleaned)} points, {results[intensity_str]['artifacts_removed']} artifacts cleaned")
                print(f"    Timestamp: {measurement_time.strftime('%H:%M:%S') if measurement_time else 'unknown'}")
    
    return results

def save_results(all_results):
    """Removed - no longer needed"""
    pass

if __name__ == "__main__":
    data_dir = "/home/oskar/Dokumente/code/ADLS/FS25/DataLab Praktika/data/export/tremor-peso-fade@duck.com"
    
    print("=== Heart Rate Analysis - Homework Assignment ===")
    print("📋 Hausaufgabe nach Tag 1:")
    print("1. Datenbereinigung (Median filter + interpolation)")
    print("2. Datenaufbereitung (Standardized CSV export)")
    print()
    
    all_results = {}
    for person in ['oskar', 'micheelle', 'eros']:
        print(f"Processing {person.capitalize()}...")
        data = process_person_data(person, data_dir)
        
        if data:
            all_results[person] = data
            print(f"  Successfully processed {len(data)} intensity levels")
        else:
            print(f"  No timestamped data found for {person}")
        print()
    
    if all_results:
        print("=== Creating Homework CSV Files ===")
        create_homework_csv(all_results)
        
        print()
        print("✅ Homework Assignment Complete!")
        print("📁 Files created in data/ directory:")
        print("  - steinosk_activity_lsdlpr25.csv (Oskar)")
        print("  - linamic_activity_lsdlpr25.csv (Micheelle)")
        print("  - halero01_activity_lsdlpr25.csv (Eros)")
        print()
        print("📝 Remember to fill in the METADATA dictionary with real values")
        
    else:
        print("❌ No data processed")