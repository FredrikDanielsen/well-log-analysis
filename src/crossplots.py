"""
Well Log Cross-Plot Analysis Module

This module provides functions for creating cross-plots from well log data.
Cross-plots are essential for:
- Lithology identification
- Porosity estimation
- Fluid identification
- Rock typing
- Quality control

Main Features:
- neutron_density_crossplot(): Creates neutron-density cross-plots with lithology lines
- Formation tops color coding
- Standard petrophysical interpretation overlays
- Interactive plotting capabilities

Usage:
    Run this file directly to create cross-plots from the sample well data:
    python crossplots.py
    
    Or import functions for custom use:
    from crossplots import neutron_density_crossplot
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


def neutron_density_crossplot(
    df,
    neutron_col="NEU",
    density_col="DEN",
    depth_col="DEPT",
    formation_tops=None,
    figsize=(10, 8),
    title="Neutron-Density Cross-Plot"
):
    """
    Create a neutron-density cross-plot with lithology interpretation lines.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing well log data.
    neutron_col : str
        Name of the neutron porosity column.
    density_col : str  
        Name of the bulk density column.
    depth_col : str
        Name of the depth column for color coding.
    formation_tops : dict, optional
        Dictionary of formation names and depths for color coding.
    figsize : tuple, optional
        Figure size.
    title : str, optional
        Plot title.
    
    Returns
    -------
    fig, ax : matplotlib figure and axis objects
    """
    
    # Filter out null values
    valid_data = df[(df[neutron_col] != -999.25) & (df[density_col] != -999.25)]
    
    if len(valid_data) == 0:
        print("No valid data points found for cross-plot")
        return None, None
    
    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Color code by depth if formation tops are provided
    if formation_tops is not None:
        # Assign formation colors based on depth
        formation_colors = plt.cm.tab10(np.linspace(0, 1, len(formation_tops)))
        formation_list = list(formation_tops.keys())
        depth_list = list(formation_tops.values())
        
        # Sort by depth
        sorted_indices = np.argsort(depth_list)
        formation_list = [formation_list[i] for i in sorted_indices]
        depth_list = [depth_list[i] for i in sorted_indices]
        
        # Assign each data point to a formation
        colors = []
        labels = []
        for _, row in valid_data.iterrows():
            depth = row[depth_col]
            # Find which formation this depth belongs to
            formation_idx = 0
            for i, top_depth in enumerate(depth_list):
                if depth >= top_depth:
                    formation_idx = i
            colors.append(formation_colors[formation_idx])
            labels.append(formation_list[formation_idx])
        
        # Create scatter plot with formation colors
        scatter = ax.scatter(valid_data[neutron_col], valid_data[density_col], 
                           c=colors, alpha=0.7, s=20, edgecolors='black', linewidth=0.5)
        
        # Create legend for formations
        legend_elements = []
        for i, (fm, color) in enumerate(zip(formation_list, formation_colors)):
            legend_elements.append(plt.scatter([], [], c=[color], s=50, label=fm))
        ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')
        
    else:
        # Simple scatter plot colored by depth
        scatter = ax.scatter(valid_data[neutron_col], valid_data[density_col], 
                           c=valid_data[depth_col], cmap='viridis', alpha=0.7, s=20)
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label(f'{depth_col} (m)')
    
    # Add lithology interpretation lines
    add_lithology_lines(ax)
    
    # Set labels and title
    ax.set_xlabel(f'{neutron_col} (Neutron Porosity, v/v)')
    ax.set_ylabel(f'{density_col} (Bulk Density, g/cm³)')
    ax.set_title(title)
    
    # Set reasonable axis limits
    ax.set_xlim(-0.05, 0.6)  # Neutron porosity 0-60%
    ax.set_ylim(1.5, 3.0)    # Density 1.5-3.0 g/cm³
    ax.invert_yaxis()        # Higher density at bottom (geological convention)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig, ax


def add_lithology_lines(ax):
    """
    Add standard lithology interpretation lines to neutron-density cross-plot.
    
    Parameters
    ----------
    ax : matplotlib axis
        The axis to add lithology lines to.
    """
    
    # Define lithology end-member points (neutron, density)
    # These are approximate values for common rock types
    sandstone_line = np.array([[0, 2.65], [0.4, 2.35]])  # Clean sandstone to 40% porosity
    limestone_line = np.array([[0, 2.71], [0.4, 2.31]])  # Clean limestone to 40% porosity
    dolomite_line = np.array([[0, 2.87], [0.4, 2.47]])   # Clean dolomite to 40% porosity
    
    # Plot lithology lines
    ax.plot(sandstone_line[:, 0], sandstone_line[:, 1], 'r-', linewidth=2, label='Sandstone')
    ax.plot(limestone_line[:, 0], limestone_line[:, 1], 'b-', linewidth=2, label='Limestone')
    ax.plot(dolomite_line[:, 0], dolomite_line[:, 1], 'g-', linewidth=2, label='Dolomite')
    
    # Add porosity lines (iso-porosity lines)
    porosities = [0.1, 0.2, 0.3]  # 10%, 20%, 30% porosity
    for phi in porosities:
        # Sandstone porosity line
        ss_rho = 2.65 - phi * (2.65 - 1.0)  # Assuming fluid density = 1.0
        ax.axhline(y=ss_rho, color='red', linestyle='--', alpha=0.5)
        ax.text(0.55, ss_rho, f'{phi*100:.0f}%', color='red', fontsize=8, va='center')
    
    # Add text labels for lithologies
    ax.text(0.05, 2.65, 'Sandstone', color='red', fontsize=10, weight='bold')
    ax.text(0.05, 2.71, 'Limestone', color='blue', fontsize=10, weight='bold')
    ax.text(0.05, 2.87, 'Dolomite', color='green', fontsize=10, weight='bold')
    
    # Add clay line (approximation)
    clay_neutron = np.linspace(0.3, 0.6, 10)
    clay_density = 2.2 + 0.3 * clay_neutron  # Approximate clay trend
    ax.plot(clay_neutron, clay_density, 'brown', linestyle=':', linewidth=2, label='Clay trend')
    ax.text(0.45, 2.4, 'Clay', color='brown', fontsize=10, weight='bold')


def porosity_estimation_plot(
    df,
    neutron_col="NEU", 
    density_col="DEN",
    depth_col="DEPT",
    matrix_density=2.65,
    fluid_density=1.0,
    figsize=(12, 8)
):
    """
    Create a plot comparing neutron and density porosity estimates.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing well log data.
    neutron_col : str
        Name of the neutron porosity column.
    density_col : str
        Name of the bulk density column.
    depth_col : str
        Name of the depth column.
    matrix_density : float
        Matrix density for porosity calculation (default: 2.65 for sandstone).
    fluid_density : float
        Fluid density for porosity calculation (default: 1.0 for water).
    figsize : tuple, optional
        Figure size.
    
    Returns
    -------
    fig, axes : matplotlib figure and axes objects
    """
    
    # Calculate density porosity
    df_calc = df.copy()
    df_calc['PHID'] = (matrix_density - df_calc[density_col]) / (matrix_density - fluid_density)
    df_calc['PHID'] = df_calc['PHID'].clip(0, 1)  # Clip to reasonable porosity range
    
    # Filter out null values
    valid_data = df_calc[
        (df_calc[neutron_col] != -999.25) & 
        (df_calc[density_col] != -999.25) &
        (df_calc['PHID'] >= 0) & 
        (df_calc['PHID'] <= 1)
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # Plot 1: Neutron vs Depth
    axes[0].plot(valid_data[neutron_col], valid_data[depth_col], 'b-', linewidth=1)
    axes[0].set_xlabel('Neutron Porosity (v/v)')
    axes[0].set_ylabel('Depth (m)')
    axes[0].set_title('Neutron Porosity Log')
    axes[0].invert_yaxis()
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xlim(0, 0.6)
    
    # Plot 2: Density Porosity vs Depth  
    axes[1].plot(valid_data['PHID'], valid_data[depth_col], 'r-', linewidth=1)
    axes[1].set_xlabel('Density Porosity (v/v)')
    axes[1].set_title('Density Porosity Log')
    axes[1].invert_yaxis()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_xlim(0, 0.6)
    
    # Plot 3: Neutron vs Density Porosity Cross-plot
    axes[2].scatter(valid_data[neutron_col], valid_data['PHID'], 
                   c=valid_data[depth_col], cmap='viridis', alpha=0.7, s=20)
    axes[2].plot([0, 0.6], [0, 0.6], 'k--', alpha=0.5, label='1:1 line')
    axes[2].set_xlabel('Neutron Porosity (v/v)')
    axes[2].set_ylabel('Density Porosity (v/v)')
    axes[2].set_title('Neutron vs Density Porosity')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    axes[2].set_xlim(0, 0.6)
    axes[2].set_ylim(0, 0.6)
    
    plt.tight_layout()
    return fig, axes


if __name__ == "__main__":
    """
    Main execution block for cross-plot analysis.
    
    This script:
    1. Loads well log data from the LAS file
    2. Creates neutron-density cross-plots with formation color coding
    3. Adds lithology interpretation lines
    4. Creates porosity comparison plots
    5. Saves plots as PNG files
    """
    
    # Load the well log data (reuse parsing from visualization.py)
    las_path = os.path.join("data", "Well 1.txt")
    
    # Parse LAS file
    with open(las_path, 'r') as f:
        lines = f.readlines()

    # Find sections
    curve_start = None
    ascii_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith('~Curve Information Block'):
            curve_start = i
        if line.strip().startswith('~ASCII'):
            ascii_start = i + 1
            break

    # Parse curve names
    curve_names = []
    for line in lines[curve_start+1:ascii_start-1]:
        if line.strip().startswith('#') or not line.strip():
            continue
        parts = line.split()
        if len(parts) > 0:
            curve_names.append(parts[0].split('.')[0])

    # Parse data
    data = []
    for line in lines[ascii_start:]:
        if line.strip():
            data.append([float(x) for x in line.split()])

    df = pd.DataFrame(data, columns=curve_names)
    
    # Formation tops
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
    
    print(f"Loaded {len(df)} data points")
    print(f"Neutron range: {df['NEU'].min():.3f} to {df['NEU'].max():.3f}")
    print(f"Density range: {df['DEN'].min():.3f} to {df['DEN'].max():.3f}")
    
    # Create neutron-density cross-plot
    print("\nCreating neutron-density cross-plot...")
    fig1, ax1 = neutron_density_crossplot(
        df, 
        neutron_col="NEU",
        density_col="DEN", 
        depth_col="DEPT",
        formation_tops=formation_tops,
        title="Neutron-Density Cross-Plot with Formation Color Coding"
    )
    
    if fig1 is not None:
        # Save the plot
        output_path1 = os.path.join("data", "neutron_density_crossplot.png")
        fig1.savefig(output_path1, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"Cross-plot saved as: {output_path1}")
        plt.show()
    
    # Create porosity comparison plot
    print("\nCreating porosity comparison plots...")
    fig2, axes2 = porosity_estimation_plot(
        df,
        neutron_col="NEU",
        density_col="DEN",
        depth_col="DEPT"
    )
    
    # Save the porosity comparison plot
    output_path2 = os.path.join("data", "porosity_comparison.png")
    fig2.savefig(output_path2, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Porosity comparison saved as: {output_path2}")
    plt.show()
    
    print("\nCross-plot analysis complete!")
