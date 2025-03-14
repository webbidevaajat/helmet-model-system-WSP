import pandas as pd
import config_scens
from pathlib import Path
import matplotlib.pyplot as plt

conf_scens = config_scens.scenarios

def get_helmet_volume(scenarios: list, results_path: Path):
    """This function reads the csv files for all mode volumes of defined areas.
    """
    helmet_results = pd.DataFrame()
    
    for scenario in scenarios:
        scenario = conf_scens[scenario]
        scenario_results_path = results_path / f"volume_stats_{scenario['year']}_{scenario['name']}_volumes.csv"
        results = pd.read_csv(scenario_results_path, sep=';')
        results['scenario'] = scenario['name']
        helmet_results = pd.concat([helmet_results, results], ignore_index=True)
    return helmet_results

def export_traffic_comparison(scenarios: list, results_path: Path, compare_data: Path):
    """This function compares Helmet volumes by mode and area with  
    HSL statistics.
    """
    helmet_volumes = pd.DataFrame()

    helmet_volumes = get_helmet_volume(scenarios, results_path)
    hsl_volumes = pd.read_csv(compare_data)

    # pivot table
    hsl_volumes = hsl_volumes.melt(id_vars=["mode"], var_name="area", value_name="vrk")
    hsl_volumes['scenario'] = 'HSL_2022'

    # join dataframes
    joined_data = pd.concat([hsl_volumes, helmet_volumes], ignore_index=True)

    # Export results comparison by mode
    filename = f"volume_comparison.csv"
    savefile = results_path / filename
    
    # Export results comparison by mode
    joined_data.to_csv(savefile, sep=";", index=False)

def plot_traffic_comparison(results_path: Path):
    """Plots volumes. Saves results to result_path."""
    filename = f"volume_comparison.csv"
    volumes_stats = pd.read_csv(results_path / filename, sep=";")

    order = ["Juna", "Raitiovaunu", "Linja-auto", "Metro", "Joukkoliikenne", "Henkiloautot", "Yhteensa"]
    
    for area in volumes_stats['area'].unique():
        fig, ax = ax_settings()
        area_data = volumes_stats[volumes_stats['area'] == area]
        area_data_pivot = area_data.pivot(index='mode', columns='scenario', values='vrk')
        area_data_pivot = area_data_pivot.reindex(order)
        area_data_pivot.plot(kind='bar', ax=ax, width=0.8)
        ax.set_xticklabels(area_data_pivot.index, rotation=45, fontsize=5)
        ax.set_title(f"Liikennemäärät (vrk) - {area}")
        ax.legend()
        ax.set_xlabel('')  # Remove x-axis title

        plt.tight_layout(pad=2.0)
        plt.savefig(results_path / f"traffic_comparison_{area}.jpg", dpi=300)
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