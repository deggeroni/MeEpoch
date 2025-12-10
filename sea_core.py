import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from spacepy import pycdf

# =============================================
# 1. LOADING EVENT TABLE
# =============================================

def load_event_table(csv_path):
    """Load event metadata used to define the epoch centers."""
    return pd.read_csv(csv_path)


def extract_date_components(event_table):
    """
    Convert date strings in the format YYYY/MM/DD/HH/MM
    into separated numeric components.
    """
    dates_split = [d.split('/') for d in event_table['Dstdata']]
    dates_split = np.array(dates_split)

    year = dates_split[:, 0].astype(int)
    month = dates_split[:, 1].astype(int)
    day = dates_split[:, 2].astype(int)
    hour = dates_split[:, 3].astype(int)
    minute = dates_split[:, 4].astype(int)

    return year, month, day, hour, minute


# =============================================
# 2. CDF PATH CONSTRUCTION
# =============================================

def build_cdf_paths(year, month, day, base_path):
    """
    Build paths for ACE CDF files based on event dates.
    """
    paths = []

    for y, m, d in zip(year, month, day):
        month_str = f"{m:02d}"
        date_str = f"{y}{month_str}01"
        full_path = f"{base_path}/omni_hro_1min_{date_str}_v01.cdf"
        paths.append(full_path)

    return list(set(paths))


# =============================================
# 3. READ CDF FILES
# =============================================

def read_ace_cdf(cdf_path):
    """Read ACE parameters from a CDF file and return a cleaned DataFrame."""
    cdf = pycdf.CDF(cdf_path)

    parameters = {
        'Beta': cdf['Beta'][...],
        'SYM_H': cdf['SYM_H'][...],
        'BX_GSE': cdf['BX_GSE'][...],
        'BY_GSE': cdf['BY_GSE'][...],
        'BZ_GSE': cdf['BZ_GSE'][...],
        'T': cdf['T'][...],
        'flow_speed': cdf['flow_speed'][...],
        'proton_density': cdf['proton_density'][...],
    }
    epoch = cdf['Epoch'][...]

    df = pd.DataFrame(parameters, index=epoch)
    df.replace([9.999e+02, 9.999e+03, 9.99e+04, 9.99e+06, 999.99], np.nan, inplace=True)

    return df


def merge_cdf_files(paths):
    """Merge all CDF files into one continuous DataFrame."""
    frames = []

    for p in paths:
        try:
            frames.append(read_ace_cdf(p))
        except:
            pass  # silently ignore missing files

    df = pd.concat(frames)
    df = df[~df.index.duplicated(keep='first')]
    return df


# =============================================
# 4. EVENT WINDOW EXTRACTION
# =============================================

def build_event_windows(year, month, day, hour, minute, days=2):
    """Create ±N-day windows around each event."""
    windows = []
    for y, m, d, h, mn in zip(year, month, day, hour, minute):
        center = datetime(y, m, d, h, mn)
        start = center - timedelta(days=days)
        end = center + timedelta(days=days)
        windows.append((start, end))
    return windows


def extract_event_segments(df, windows):
    """Slice dataframe for each event window."""
    segments = []
    for start, end in windows:
        segment = df[(df.index >= start) & (df.index <= end)]
        segments.append(segment)
    return segments


# =============================================
# 5. SUPERPOSED EPOCH CALCULATION
# =============================================

def epoch_average(segments, column, func=np.nanmean):
    """Compute epoch-mean profile across event segments."""
    length = len(segments[0])
    values = []

    for i in range(length):
        samples = [seg[column].iloc[i] for seg in segments]
        values.append(func(samples))

    return np.array(values)

