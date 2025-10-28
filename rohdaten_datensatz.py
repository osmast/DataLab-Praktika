import pandas as pd
from pathlib import Path
from datetime import datetime
import re

RAW_DIR = Path("data/export/tremor-peso-fade@duck.com")
OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)

ZHAW_KUERZEL = {
    'oskar': 'steinosk',
    'micheelle': 'linamic',
    'michelle': 'linamic',
    'eros': 'halero01'
}

for f in RAW_DIR.glob("*_int_*.txt"):
    match = re.match(r"([A-Za-z]+)_int_(\d)", f.stem)
    person, intensity = match.groups()
    person_key = person.lower().replace('michelle', 'micheelle')
    
    start_time = datetime(2025, 10, 16, 9, 20, 31)
    rr = pd.read_csv(f, header=None)[0].values
    time_axis = start_time + pd.to_timedelta(rr.cumsum(), unit="ms")
    bpm = 60000 / rr
    
    df = pd.DataFrame({
        "time": time_axis,
        "rr_interval": rr,
        "bpm": bpm
    })
    
    zhaw_id = ZHAW_KUERZEL[person_key]
    out_file = OUT_DIR / f"{zhaw_id}_activity_intensity_{intensity}_lsdlpr25.csv"
    df.to_csv(out_file, index=False)
    print(f"✅ {out_file.name}")
