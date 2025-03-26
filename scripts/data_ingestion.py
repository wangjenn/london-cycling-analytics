# Data Ingestion 

import os 
import pandas as pd 
import requests 
import time 
import logging 
from concurrent.futures import ThreadPoolExecutor 
from datetime import datetime 
import numpy as np 
import matplotlib
import glob
import pprint
import re


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("download_log.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Base URL for TfL cycling data
BASE_URL = "https://cycling.data.tfl.gov.uk/usage-stats/"

# Create directory structure
DATA_DIR = "bicycle_data"
RAW_DIR = os.path.join(DATA_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# List of target filenames - selected to provide good coverage across seasons and years

filenames = [
    # 2020 data - Quarterly representation (Jan, Apr, Jul, Oct)
    "195JourneyDataExtract01Jan2020-07Jan2020.csv",
    "206JourneyDataExtract18Mar2020-24Mar2020.csv",
    "212JourneyDataExtract29Apr2020-05May2020.csv",
    "221JourneyDataExtract01Jul2020-07Jul2020.csv",
    "232JourneyDataExtract16Sep2020-22Sep2020.csv",
    "238JourneyDataExtract28Oct2020-03Nov2020.csv",
    
    # 2021 data - Quarterly representation
    "251JourneyDataExtract03Feb2021-09Feb2021.csv",
    "258JourneyDataExtract24Mar2021-30Mar2021.csv",
    "267JourneyDataExtract26May2021-01Jun2021.csv",
    "273JourneyDataExtract07Jul2021-13Jul2021.csv",
    "282JourneyDataExtract08Sep2021-14Sep2021.csv",
    "292JourneyDataExtract17Nov2021-23Nov2021.csv",
    
    # 2022 data - Quarterly representation
    "302JourneyDataExtract02Feb2022-08Feb2022.csv",
    "313JourneyDataExtract20Apr2022-26Apr2022.csv",
    "322JourneyDataExtract15Jun2022-21Jun2022.csv",
    "331JourneyDataExtract17Aug2022-23Aug2022.csv",
    "340JourneyDataExtract19Oct2022-25Oct2022.csv",
    "348JourneyDataExtract14Dec2022-20Dec2022.csv",
    
    # 2023 data - Quarterly representation
    "356JourneyDataExtract08Feb2023-14Feb2023.csv",
    "366JourneyDataExtract19Apr2023-25Apr2023.csv",
    "375JourneyDataExtract19Jun2023-30Jun2023.csv",
    "379JourneyDataExtract15Sep2023-30Sep2023.csv",
    "383JourneyDataExtract15Oct2023-31Oct2023.csv",
    "386JourneyDataExtract15Dec2023-31Dec2023.csv",
    
    # 2024 data - Most recent data
    "388JourneyDataExtract15Jan2024-31Jan2024.csv",
    "392JourneyDataExtract15Mar2024-31Mar2024.csv",
    "396JourneyDataExtract15May2024-31May2024.csv",
    "400JourneyDataExtract15Jul2024-31Jul2024.csv",
    "406JourneyDataExtract15Nov2024-30Nov2024.csv",
    "412JourneyDataExtract15Jan2025-31Jan2025.csv",
]

def download_file(filename):
    save_path = os.path.join(RAW_DIR, filename)
    
    # Skip if file already exists
    if os.path.exists(save_path):
        logger.info(f"File already exists: {filename}")
        return True
    
    try:
        logger.info(f"Downloading {filename}...")
        response = requests.get(url, timeout=120)  # Increased timeout for larger files
        
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            # Log success with file size
            size_mb = os.path.getsize(save_path) / (1024*1024)
            logger.info(f"Successfully downloaded {filename} ({size_mb:.2f} MB)")
            return True
        else:
            logger.error(f"Failed to download {filename} (Status code: {response.status_code})")
            # Try alternative URL formats for Journey data if main one fails
            if "JourneyDataExtract" in filename and not filename.startswith("0"):
                alt_filename = filename.replace("JourneyDataExtract", "-Journey-Data-Extract-")
                logger.info(f"Trying alternative filename: {alt_filename}")
                return download_file(alt_filename)
            return False
    except Exception as e:
        logger.error(f"Error downloading {filename}: {str(e)}")
        return False

def create_download_summary():
    """Creates a summary of all downloaded files."""
    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
    
    if not files:
        logger.warning("No files were downloaded successfully.")
        return
    
    summary_data = []
    for file in files:
        file_path = os.path.join(RAW_DIR, file)
        size_mb = os.path.getsize(file_path) / (1024*1024)
        
        # Extract date from filename (approximate)
        file_info = {
            'filename': file,
            'size_mb': round(size_mb, 2),
            'download_date': datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')
        }
        summary_data.append(file_info)
    
    # Create a DataFrame and save as CSV
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(os.path.join(DATA_DIR, 'download_summary.csv'), index=False)
        logger.info(f"Download summary created with {len(summary_df)} files")
        
        # Print summary statistics
        total_size_gb = summary_df['size_mb'].sum() / 1024
        logger.info(f"Total downloaded data: {total_size_gb:.2f} GB")

def main():
    """Main function to orchestrate the download process."""
    start_time = time.time()
    logger.info(f"Starting bicycle data download process with {len(filenames)} files")
    
    # Download files in parallel with a limit on concurrent downloads
    successful_downloads = 0
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(download_file, filenames))
        successful_downloads = sum(1 for r in results if r)
    
    # Try to create summary if any files were downloaded
    if successful_downloads > 0:
        try:
            create_download_summary()
        except Exception as e:
            logger.error(f"Error creating download summary: {str(e)}")
    
    # Log final statistics
    logger.info(f"Download process completed in {(time.time() - start_time) / 60:.2f} minutes")
    logger.info(f"Successfully downloaded {successful_downloads} of {len(filenames)} files")

if __name__ == "__main__":
    # Make sure we import datetime for the summary
    from datetime import datetime
    main()
    
# Data Cleaning 
def inspect_csv_structure(file_path):
    """Inspect the CSV structure to understand its columns"""
    try:
        # Read the first few rows to examine structure
        sample = pd.read_csv(file_path, nrows=5)
        
        # Get basic file info
        file_info = {
            'filename': os.path.basename(file_path),
            'columns': list(sample.columns),
            'num_columns': len(sample.columns),
            'has_duration': any('duration' in col.lower() for col in sample.columns),
            'has_rental_id': any(col.lower() in ['rental id', 'rental_id'] for col in sample.columns),
            'row_count': len(pd.read_csv(file_path, usecols=[0])),  # Faster row count
            'sample_row': sample.iloc[0].to_dict() if not sample.empty else {}
        }
        
        # Count potential delimiter issues (when column values contain commas)
        suspicious_columns = []
        for col in sample.columns:
            if sample[col].dtype == 'object':  # String columns
                values = sample[col].astype(str)
                if any(',' in val for val in values):
                    suspicious_columns.append(col)
        
        file_info['suspicious_columns'] = suspicious_columns
        
        return file_info
    except Exception as e:
        print(f"Error inspecting {os.path.basename(file_path)}: {e}")
        return {
            'filename': os.path.basename(file_path),
            'error': str(e),
            'columns': [], 
            'num_columns': 0,
            'has_duration': False, 
            'has_rental_id': False, 
            'sample_row': {}
        }

# Inspect each file and collect results
file_structures = {}
for file_path in csv_files:
    print(f"Inspecting {os.path.basename(file_path)}...")
    file_structures[os.path.basename(file_path)] = inspect_csv_structure(file_path)

# Check for inconsistencies in column structure
all_column_sets = set(tuple(info['columns']) for info in file_structures.values())
if len(all_column_sets) > 1:
    print("\n⚠️ WARNING: Not all files have the same column structure!")
    print(f"Found {len(all_column_sets)} different column structures")
    
    # Group files by their column structure
    structure_groups = {}
    for filename, info in file_structures.items():
        col_tuple = tuple(info['columns'])
        if col_tuple not in structure_groups:
            structure_groups[col_tuple] = []
        structure_groups[col_tuple].append(filename)
    
    # Print each structure group
    for i, (columns, files) in enumerate(structure_groups.items()):
        print(f"\nStructure Group {i+1} ({len(files)} files):")
        print(f"Columns ({len(columns)}): {', '.join(columns)}")
        print(f"Example files: {', '.join(files[:3])}" + ("..." if len(files) > 3 else ""))
else:
    print("\n✅ All files have consistent column structures")

# Print detailed information for each file
print("\nDetailed file information:")
for filename, info in file_structures.items():
    print(f"\n{filename}:")
    print(f"  Columns ({info['num_columns']}): {', '.join(info['columns'])}")
    print(f"  Row count: {info['row_count']:,}")
    
    if info.get('suspicious_columns'):
        print(f"  ⚠️ Suspicious columns (may contain commas): {', '.join(info['suspicious_columns'])}")
    
    print("  Sample row:")
    for col, val in info['sample_row'].items():
        print(f"    {col}: {val}")


# Function to parse duration strings to seconds
def parse_duration(value):
    if pd.isna(value):
        return np.nan
    
    # If already numeric, return as is
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value
    
    # Handle string format
    if isinstance(value, str):
        # Format "14m 30s"
        if 'm' in value and 's' in value:
            m_match = re.search(r'(\d+)m', value)
            s_match = re.search(r'(\d+)s', value)
            minutes = int(m_match.group(1)) if m_match else 0
            seconds = int(s_match.group(1)) if s_match else 0
            return minutes * 60 + seconds
        
        # Format "5m"
        elif 'm' in value:
            m_match = re.search(r'(\d+)m', value)
            minutes = int(m_match.group(1)) if m_match else 0
            return minutes * 60
            
        # Try direct conversion
        try:
            return float(value)
        except:
            return np.nan
    
    return np.nan

# Process each file individually and standardize format
processed_dfs = []

for file_path in csv_files:
    file_name = os.path.basename(file_path)
    print(f"Processing {file_name}...")
    
    # Read file with proper quoting to handle commas in station names
    try:
        df = pd.read_csv(file_path, quotechar='"', escapechar='\\', 
                        error_bad_lines=False, warn_bad_lines=True, 
                        low_memory=False)
    except:
        # Fallback for older pandas versions
        df = pd.read_csv(file_path, quotechar='"', escapechar='\\', 
                        on_bad_lines='warn', low_memory=False)
    
    # Create standardized dataframe with consistent column names
    standardized_df = pd.DataFrame()
    
    # Add source file info
    standardized_df['source_file'] = file_name
    
    # Check which format we're dealing with
    if 'Number' in df.columns:
        # Newer format (Group 1)
        # Handle dates
        standardized_df['start_date'] = df['Start date']
        standardized_df['end_date'] = df['End date']
        
        # Handle station info
        standardized_df['start_station_id'] = df['Start station number'].astype(str)
        standardized_df['start_station_name'] = df['Start station']
        standardized_df['end_station_id'] = df['End station number'].astype(str)
        standardized_df['end_station_name'] = df['End station']
        
        # Handle bike info
        standardized_df['bike_id'] = df['Bike number'].astype(str)
        
        # Handle duration
        if 'Total duration' in df.columns:
            standardized_df['duration_seconds'] = df['Total duration'].apply(parse_duration)
        else:
            standardized_df['duration_seconds'] = np.nan
    
    elif 'Rental Id' in df.columns:
        # Older format (Group 2)
        # Handle dates - need to convert format
        standardized_df['start_date'] = pd.to_datetime(df['Start Date'], 
                                                      format='%d/%m/%Y %H:%M', 
                                                      errors='coerce').dt.strftime('%Y-%m-%d %H:%M')
        standardized_df['end_date'] = pd.to_datetime(df['End Date'], 
                                                    format='%d/%m/%Y %H:%M', 
                                                    errors='coerce').dt.strftime('%Y-%m-%d %H:%M')
        
        # Handle station info
        standardized_df['start_station_id'] = df['StartStation Id'].astype(str)
        standardized_df['start_station_name'] = df['StartStation Name']
        standardized_df['end_station_id'] = df['EndStation Id'].astype(str)
        standardized_df['end_station_name'] = df['EndStation Name']
        
        # Handle bike info
        standardized_df['bike_id'] = df['Bike Id'].astype(str)
        
        # Handle duration - already in seconds in this format
        standardized_df['duration_seconds'] = df['Duration'].astype(float)
    
    else:
        print(f"  ⚠️ Unknown file format for {file_name}. Skipping.")
        continue
    
    # Add to list of processed dataframes
    processed_dfs.append(standardized_df)
    print(f"  ✓ Processed {len(standardized_df)} rows")

# Combine all processed dataframes
print("\nCombining all processed dataframes...")
if processed_dfs:
    combined_df = pd.concat(processed_dfs, ignore_index=True)
    print(f"Combined dataframe has {len(combined_df)} rows and {len(combined_df.columns)} columns")
    
    # Add derived columns
    print("Adding time-based columns...")
    combined_df['start_datetime'] = pd.to_datetime(combined_df['start_date'], errors='coerce')
    valid_dates = combined_df['start_datetime'].notna()
    print(f"Found {valid_dates.sum():,} valid dates")
    
    if valid_dates.any():
        combined_df['day_of_week'] = combined_df['start_datetime'].dt.day_name()
        combined_df['hour_of_day'] = combined_df['start_datetime'].dt.hour
        combined_df['month'] = combined_df['start_datetime'].dt.month
        combined_df['year'] = combined_df['start_datetime'].dt.year
        
        # Create month_name for better readability
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April', 
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        combined_df['month_name'] = combined_df['month'].map(month_names)
    
    # Drop temporary column and invalid data
    combined_df = combined_df.drop('start_datetime', axis=1)
    
    # Filter out invalid data
    print("Filtering invalid data...")
    before_filter = len(combined_df)
    valid_rows = combined_df['duration_seconds'] > 0
    combined_df = combined_df[valid_rows].reset_index(drop=True)
    print(f"Kept {len(combined_df):,} valid rows out of {before_filter:,} total rows")
    
    # Save the combined file
    output_path = os.path.join(PROCESSED_DIR, 'clean_trips.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"Saved cleaned dataset to {output_path}")
    
    # Generate summary statistics
    print("\nData Summary:")
    
    # Data Pre-Processing 
    if 'start_date' in combined_df.columns and not combined_df['start_date'].isna().all():
        try:
            start_dates = pd.to_datetime(combined_df['start_date'], errors='coerce')
            end_dates = pd.to_datetime(combined_df['end_date'], errors='coerce')
            valid_dates = start_dates.notna() & end_dates.notna()
            if valid_dates.any():
                print(f"Date range: {start_dates.min()} to {end_dates.max()}")
        except Exception as e:
            print(f"Could not parse date range: {e}")
    
    if 'duration_seconds' in combined_df.columns and combined_df['duration_seconds'].notna().any():
        avg_duration = combined_df['duration_seconds'].mean()
        print(f"Average trip duration: {avg_duration/60:.2f} minutes")
    
    # Display station and bike summaries
    for col in ['bike_id', 'start_station_id', 'end_station_id']:
        if col in combined_df.columns and not combined_df[col].isna().all():
            unique_count = combined_df[col].nunique()
            print(f"Unique {col}: {unique_count:,}")
            
            # Show top 15 most common values for this column
            top_values = combined_df[col].value_counts().head(15)
            print(f"Top 5 {col}:")
            for val, count in top_values.items():
                print(f"  {val}: {count:,} trips")
else:
    print("No data to combine!")
    
## Check Station Consistency

# Analyze start and end stations
start_stations = combined_df['start_station_id'].nunique()
end_stations = combined_df['end_station_id'].nunique()
print(f"\nUnique start stations: {start_stations:,}")
print(f"Unique end stations: {end_stations:,}")

# Check if all stations appear as both start and end stations
start_set = set(combined_df['start_station_id'].unique())
end_set = set(combined_df['end_station_id'].unique())
only_start = start_set - end_set
only_end = end_set - start_set
print(f"Stations that only appear as start stations: {len(only_start)}")
print(f"Stations that only appear as end stations: {len(only_end)}")

# Check for most popular stations
top_start = combined_df['start_station_id'].value_counts().head(5)
top_end = combined_df['end_station_id'].value_counts().head(5)
print("\nTop 5 start stations:")
for station, count in top_start.items():
    station_name = combined_df[combined_df['start_station_id']==station]['start_station_name'].iloc[0]
    print(f"  {station} ({station_name}): {count:,} trips")

print("\nTop 5 end stations:")
for station, count in top_end.items():
    station_name = combined_df[combined_df['end_station_id']==station]['end_station_name'].iloc[0]
    print(f"  {station} ({station_name}): {count:,} trips")