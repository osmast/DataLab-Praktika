# Heart Rate Analysis - DataLab Praktika FS25

## Directory Structure

```
.
├── data/                          # All data files and outputs
│   ├── export/                    # Raw data export from device
│   │   └── tremor-peso-fade@duck.com/
│   │       ├── !About This Export.txt
│   │       └── [participant_files].txt
│   ├── export.zip                 # Backup of raw data export
│   ├── halero01_activity_lsdlpr25.csv    # Eros homework submission
│   ├── linamic_activity_lsdlpr25.csv     # Micheelle homework submission
│   ├── steinosk_activity_lsdlpr25.csv    # Oskar homework submission
│   ├── processed_heart_rate_data.csv     # Combined processed data
│   └── heart_rate_summary_stats.csv      # Summary statistics
├── .venv/                         # Python virtual environment
├── minimal_processing.py          # Main processing script (homework)
├── minimal_processing_backup.py   # Backup of previous version
├── Jogging_Pipeline.ipynb         # Jupyter notebook pipeline
├── Projektbeschrieb.pdf           # Project description
├── moodle.md                      # Moodle documentation
└── who-5_german.pdf               # WHO-5 questionnaire (German)
```

## Usage

1. Activate virtual environment: `source .venv/bin/activate`
2. Run processing: `python minimal_processing.py`
3. Output files will be saved to `data/` directory

## Homework Submission

The three CSV files in `data/` with ZHAW kürzel naming are ready for submission:
- `steinosk_activity_lsdlpr25.csv`
- `linamic_activity_lsdlpr25.csv`
- `halero01_activity_lsdlpr25.csv`

**Important:** Fill in the METADATA dictionary in `minimal_processing.py` with real participant values before final submission.