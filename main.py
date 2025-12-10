import numpy as np
from sea_core import (
    load_event_table, extract_date_components,
    build_cdf_paths, merge_cdf_files,
    build_event_windows, extract_event_segments,
    epoch_average
)
from sea_plot import SEAPlotter


if __name__ == "__main__":
    
    # Load table
    events = load_event_table("TabelaEventos.csv")
    
    # Example filtering
    selected = events.query("Dropout == 'Y' and NuvemTipo == 'N-S'")
    
    # Dates
    year, month, day, hour, minute = extract_date_components(selected)
    
    # CDF locations
    base_cdf_path = "./ACE_CDF"
    paths = build_cdf_paths(year, month, day, base_cdf_path)

    # Merge CDFs
    df = merge_cdf_files(paths)

    # Windows
    windows = build_event_windows(year, month, day, hour, minute)

    # Segments
    segments = extract_event_segments(df, windows)

    # Time axis
    time_axis = np.linspace(-2, 2, len(segments[0]))

    # SEA profiles
    speed = epoch_average(segments, 'flow_speed')
    density = epoch_average(segments, 'proton_density')
    symh = epoch_average(segments, 'SYM_H')
    bz = epoch_average(segments, 'BZ_GSE')

    # Plot
    plotter = SEAPlotter()
    plotter.plot_sea(time_axis, speed, density, symh, bz)

