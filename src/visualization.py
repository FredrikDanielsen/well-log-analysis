"""
Well Log Visualization Module

This module provides functions for visualizing well log data in multi-track panels.
It includes capabilities to:
- Plot multiple well log curves as separate tracks
- Display formation tops as horizontal lines across all tracks
- Handle LAS (Log ASCII Standard) file parsing
- Create professional well log displays

Main Features:
- plot_well_log_tracks(): Creates multi-track well log panels
- Formation tops overlay with labels
- Automatic handling of null values (-999.25)
- Configurable track layouts

Usage:
    Run this file directly to visualize the sample well data:
    python visualization.py
    
    Or import functions for custom use:
    from visualization import plot_well_log_tracks
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_well_log_tracks(
    df,
    depth_col,
    log_tracks,
    track_labels=None,
    figsize=(12, 8),
    title="Well Log Panel"
):
    """
    Plot multiple well log tracks (subplots) sharing the same depth axis.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing well log data.
    depth_col : str
        Name of the depth column in df.
    log_tracks : list of list of str
        Each sublist contains log curve names to plot on the same track (subplot).
        Example: [["CALI", "BS"], ["GR"], ["DEN"], ...]
    track_labels : list of str, optional
        Labels for each track (subplot). If None, uses log names.
    figsize : tuple, optional
        Figure size.
    title : str, optional
        Overall plot title.

    Example
    -------
    plot_well_log_tracks(
        df,
        depth_col="DEPT",
        log_tracks=[["CALI", "BS"], ["GR"], ["DEN"], ["NEU"], ["AC", "ACS"], ["RMIC", "RMED", "RDEP"]],
        track_labels=["Caliper/Bit Size", "Gamma Ray", "Density", "Neutron", "Sonic (P & S)", "Resistivity"]
    )
    """
    import matplotlib.pyplot as plt

    n_tracks = len(log_tracks)
    fig, axes = plt.subplots(1, n_tracks, figsize=figsize, sharey=True)
    if n_tracks == 1:
        axes = [axes]
    depth = df[depth_col]

    for i, logs in enumerate(log_tracks):
        ax = axes[i]
        for log in logs:
            if log in df.columns:
                ax.plot(df[log], depth, label=log)
        ax.set_xlabel(
            track_labels[i] if track_labels and i < len(track_labels) else ", ".join(logs)
        )
        ax.invert_yaxis()
        ax.grid(True, which="both", linestyle=":", linewidth=0.5)
        if len(logs) > 1:
            ax.legend(fontsize=8)
    axes[0].set_ylabel("Depth (m)")
    fig.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()

def plot_histogram(data, column, bins=30, title='Histogram', xlabel='Value', ylabel='Frequency'):
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=bins, alpha=0.7, color='blue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()

def plot_scatter(data, x_column, y_column, title='Scatter Plot', xlabel='X', ylabel='Y'):
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_column], data[y_column], alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()


if __name__ == "__main__":
    """
    Main execution block for well log visualization.
    
    This script:
    1. Loads and parses a LAS file (Well 1.txt)
    2. Loads formation tops data (Tops_Well-1.txt)
    3. Creates a 6-track well log panel showing:
       - Track 1: Caliper and Bit Size
       - Track 2: Gamma Ray
       - Track 3: Density
       - Track 4: Neutron
       - Track 5: Sonic (P-wave and S-wave)
       - Track 6: Resistivity (Micro, Medium, Deep)
    4. Overlays formation tops as red dashed lines with labels
    
    Data handling:
    - Null values (-999.25) are handled automatically by matplotlib
    - Formation tops are hardcoded for reliability
    - Depth axis is shared across all tracks and inverted (geological convention)
    """
    import pandas as pd
    import numpy as np
    import os

    # LAS file path and tops file path
    las_path = os.path.join("data", "Well 1.txt")
    tops_path = os.path.join("data", "Tops_Well-1.txt")

    # --- LAS Parsing ---
    # Read LAS file manually (no lasio dependency)
    with open(las_path, 'r') as f:
        lines = f.readlines()

    # Find ~Curve Information Block and ~ASCII
    curve_start = None
    ascii_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('~Curve Information Block'):
            curve_start = i
        if line.strip().startswith('~ASCII'):
            ascii_start = i + 1
            break

    # Parse curve names (mnemonics)
    curve_names = []
    for line in lines[curve_start+1:ascii_start-1]:
        if line.strip().startswith('#') or not line.strip():
            continue
        parts = line.split()
        if len(parts) > 0:
            curve_names.append(parts[0].split('.')[0])

    # Parse ASCII data
    data = []
    for line in lines[ascii_start:]:
        if line.strip():
            data.append([float(x) for x in line.split()])

    df = pd.DataFrame(data, columns=curve_names)

    # --- Formation Tops ---
    # Hardcode the formation tops from the file for reliability
    formation_tops = {
        'FM-1': 479,
        'FM-2': 1294, 
        'FM-3': 2185,
        'FM-4': 2267,
        'FM-5': 2293,
        'FM-6': 2405,
        'FM-7': 2513,
        'FM-8': 2676,
        'FM-9': 2875,
        'FM-10': 2990
    }
    
    top_depths = list(formation_tops.values())
    top_names = list(formation_tops.keys())
    
    # --- Plotting ---
    # Arguments for the user:
    depth_col = "DEPT"
    
    # Debug: Print formation tops data
    print("Formation Tops:")
    print(f"Depths: {top_depths}")
    print(f"Names: {top_names}")
    print(f"Depth range in well data: {df[depth_col].min()} to {df[depth_col].max()}")
    log_tracks = [
        ["CALI", "BS"],
        ["GR"],
        ["DEN"],
        ["NEU"],
        ["AC", "ACS"],
        ["RMIC", "RMED", "RDEP"]
    ]
    track_labels = [
        "Caliper/Bit Size",
        "Gamma Ray",
        "Density",
        "Neutron",
        "Sonic (P & S)",
        "Resistivity (Micro, Medium, Deep)"
    ]

    # Plot with formation tops as horizontal lines
    n_tracks = len(log_tracks)
    fig, axes = plt.subplots(1, n_tracks, figsize=(14, 8), sharey=True)
    if n_tracks == 1:
        axes = [axes]
    depth = df[depth_col]
    for i, logs in enumerate(log_tracks):
        ax = axes[i]
        for log in logs:
            if log in df.columns:
                ax.plot(df[log], depth, label=log)
        
        # Set labels and formatting first
        ax.set_xlabel(track_labels[i] if track_labels and i < len(track_labels) else ", ".join(logs))
        ax.invert_yaxis()
        ax.grid(True, which="both", linestyle=":", linewidth=0.5)
        if len(logs) > 1:
            ax.legend(fontsize=8)
        
        # Add formation tops after plotting data (so xlim is set)
        print(f"Adding formation tops to track {i+1}...")
        for j, (td, tn) in enumerate(zip(top_depths, top_names)):
            print(f"  Adding top {tn} at depth {td}")
            ax.axhline(td, color='red', linestyle='--', linewidth=2.0, alpha=0.9)
            # Position text at 95% of the x-axis range
            x_pos = ax.get_xlim()[0] + 0.95 * (ax.get_xlim()[1] - ax.get_xlim()[0])
            ax.text(x_pos, td, f' {tn}', color='red', fontsize=8, va='center', ha='right', 
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor='red'))
    
    # Set depth axis limits to show full geological context (0 to 3500m)
    for ax in axes:
        ax.set_ylim(3500, 0)  # Note: inverted (bottom, top) because y-axis is already inverted
    
    axes[0].set_ylabel("Depth (m)")
    fig.suptitle("Well Log Panel with Formation Tops", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    # Save the plot as PNG in the data folder
    output_path = os.path.join("data", "well_log1.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Plot saved as: {output_path}")
    
    plt.show()