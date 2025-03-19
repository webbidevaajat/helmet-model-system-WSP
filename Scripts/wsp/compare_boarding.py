import pandas as pd
import config_scens
from pathlib import Path
import matplotlib.pyplot as plt

conf_scens = config_scens.scenarios

def get_helmet_boarding_by_mode(scenarios: list, results_path: Path):
    """This function reads the csv files for boardings and compares results.
    """
    helmet_results = pd.DataFrame()
    
    for scenario in scenarios:
        scenario = conf_scens[scenario]
        scenario_results_path = results_path / f"transit_stats_{scenario['year']}_{scenario['name']}_volumes.csv"
        results = pd.read_csv(scenario_results_path, sep=';')
        results['scenario'] = scenario['name']
        helmet_results = pd.concat([helmet_results, results], ignore_index=True)
    return helmet_results

def get_helmet_boarding_by_area(scenarios: list, results_path: Path):
    """This function reads the csv files for boardings and compares results.
    """
    helmet_results = pd.DataFrame()
    
    for scen in scenarios:
        scenario = conf_scens[scen]
        scenario_results_path = results_path / f"transit_stats_{scenario['year']}_{scenario['name']}_area_boardings.csv"
        results = pd.read_csv(scenario_results_path, sep=';')
        results['scenario'] = scenario['name']
        helmet_results = pd.concat([helmet_results, results], ignore_index=True)

    return helmet_results

def export_boa_comparison_by_mode(scenarios: list, results_path: Path, compare_data: Path):
    """This function compares Helmet boarding totals by mode with  
    HSL statistics.
    """
    helmet_boardings = pd.DataFrame()

    helmet_boardings = get_helmet_boarding_by_mode(scenarios, results_path)
    helmet_boardings['boa_totals'] = helmet_boardings['boa_totals'] / 1000000

    hsl_boardings = pd.read_csv(compare_data)

    # join dataframes
    hsl_boardings = hsl_boardings[['mode', 'nousijaa_2023']]
    hsl_boardings = hsl_boardings.rename(columns={'nousijaa_2023': 'boa_totals'})
    hsl_boardings['scenario'] = 'HSL_2023'

    # join dataframes
    joined_data = pd.concat([hsl_boardings, helmet_boardings], ignore_index=True)

    # Pivot the data to have sources as columns
    pivot_data = joined_data.pivot(index='mode', columns='scenario', values='boa_totals')

    # Add column name 
    mode_names = pd.read_csv(compare_data)
    mode_names = mode_names[['mode', 'mode_name']].drop_duplicates()
    
    pivot_data = pivot_data.reset_index().merge(mode_names, on='mode', how='left').set_index('mode')
    cols = ['mode_name'] + [col for col in pivot_data if col != 'mode_name']
    pivot_data = pivot_data[cols]

    # Export results comparison by mode
    filename = f"transit_boardings_comparison.csv"
    savefile = results_path / filename
    
    # Export results comparison by mode
    pivot_data.to_csv(savefile, sep=";", index=True)
    
    print(f"Successfully exported {filename}")

   
def export_boa_comparison_by_area(scenarios: list, results_path: Path):
    """This function compares the boarding totals of Helmet with 
    real boarding statistics by area.
    """

    helmet_boardings = pd.DataFrame()

    helmet_boardings = get_helmet_boarding_by_area(scenarios, results_path)

    # join dataframes
    helmet_boardings[['scenario', 'area', 'first_boa']]
    
    # Group by mode and source, then sum the boardings
    grouped_data = helmet_boardings.groupby(['scenario', 'area']).sum().reset_index()
    
    # Convert boardings to millions
    grouped_data['miljoonaa_matkat'] = grouped_data['first_boa'] / 1000000

    # Pivot the data to have sources as columns
    pivot_data = grouped_data.pivot(index='area', columns='scenario', values='miljoonaa_matkat')

    # Export results comparison by mode
    filename = f"transit_trips_comparison.csv"
    savefile = results_path / filename
    pivot_data.to_csv(savefile, sep=";", index=True)
    print(f"Successfully exported {filename}")

def export_boa_per_trip_comparison(scenarios: list, results_path: Path):
    """This function compares the boarding totals of Helmet with 
    real boarding statistics by area.
    """

    helmet_boardings = pd.DataFrame()

    helmet_boardings = get_helmet_boarding_by_area(scenarios, results_path)

    # join dataframes
    helmet_boardings[['scenario', 'area', 'total_boa', 'first_boa']]
    helmet_boardings['boa_per_trip'] = helmet_boardings['total_boa'] / helmet_boardings['first_boa']
    
    # select columns
    helmet_boardings[['scenario', 'area', 'boa_per_trip']]

    # Group by mode and source, then sum the boardings
    grouped_data = helmet_boardings.groupby(['scenario', 'area']).sum().reset_index()

    # Pivot the data to have sources as columns
    pivot_data = grouped_data.pivot(index='area', columns='scenario', values='boa_per_trip')

    # Export results comparison by mode
    filename = f"transit_boa_per_trip_comparison.csv"
    savefile = results_path / filename
    pivot_data.to_csv(savefile, sep=";", index=True)
    print(f"Successfully exported {filename}")

def plot_boa_comparison_by_mode(results_path: Path):
    """Plots volumes. Saves results to result_path."""
    filename = f"transit_boardings_comparison.csv"
    boa_stats = pd.read_csv(results_path / filename, sep=";")

    mode_labels = {"b": "Bussi (b)", "d": "Bussi (d)", "e": "Bussi (e)",
                   "g": "Runkobussi", "m": "Metro", "p": "Pikaraitiotie", 
                   "r": "Lähijunat", "t": "Raitiotie", "w": "Lautat" , "j": "Kaukojuna"}
    
    fig, ax = ax_settings()
    # replace mode label
    for key, title in mode_labels.items():
        boa_stats.loc[boa_stats['mode'] == key, 'mode'] = title

    melted_boa_stats = boa_stats.melt(id_vars=["mode", "mode_name"], var_name="scenario", value_name="vrk")
    melted_boa_stats['vrk'] = melted_boa_stats['vrk'].round()
    boa_stats_pivot = melted_boa_stats.pivot(index='mode', columns='scenario', values='vrk')
    boa_stats_pivot.plot(kind='bar', ax=ax, width=0.8)
    ax.set_xticklabels(boa_stats_pivot.index, rotation=45, fontsize=5)
    ax.set_title(f"Nousua vuodessa (milj. matkaa), laajennuskerroin 300")
    ax.legend()
    ax.set_xlabel('')  # Remove x-axis title
    # Add labels to the chart
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fmt='%.0f')
    plt.tight_layout(pad=2.0)
    plt.savefig(results_path / f"boarding_comparison.jpg", dpi=300)
    plt.close(fig)

def plot_boa_per_trip_comparison(results_path: Path):
    """Plots volumes. Saves results to result_path."""
    filename = f"transit_boa_per_trip_comparison.csv"
    volumes_stats = pd.read_csv(results_path / filename, sep=";")
    
    fig, ax = ax_settings()

    melted_volumes_stats = volumes_stats.melt(id_vars=["area"], var_name="scenario", value_name="ratio")
    melted_volumes_stats['ratio'] = melted_volumes_stats['ratio'].round(2)
    volumes_stats_pivot = melted_volumes_stats.pivot(index='area', columns='scenario', values='ratio')
    volumes_stats_pivot.plot(kind='bar', ax=ax, width=0.8)
    ax.set_xticklabels(volumes_stats_pivot.index, rotation=45, fontsize=5)
    ax.set_title(f"Nousua per JL-matka")
    ax.legend()
    ax.set_xlabel('')  # Remove x-axis title
    ax.set_ylim(top=3)  # Set y-axis maximum value to 3
    # Add labels to the chart
    for container in ax.containers:
        ax.bar_label(container, label_type='edge', fmt='%.2f')
    plt.tight_layout(pad=2.0)
    plt.savefig(results_path / f"boardings_per_trip_comparison.jpg", dpi=300)
    plt.close(fig)

def ax_settings() -> tuple[plt.Figure, plt.Axes]:
    """Returns common axis settings."""
    fig, ax = plt.subplots()
    ax.yaxis.grid(color="#cccccc", linestyle="-")
    ax.set_axisbelow(True)
    plt.ticklabel_format(axis="y", style="plain")
    plt.xticks(rotation=45, fontsize=5)
    plt.yticks(fontsize=5)
    return fig, ax