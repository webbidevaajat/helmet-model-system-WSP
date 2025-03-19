import pandas as pd
import config_scens
from pathlib import Path
import matplotlib.pyplot as plt

conf_scens = config_scens.scenarios

def get_helmet_metro_boardings(scenarios: list, results_path: Path):
    """This function reads the csv files for metro boardings.
    """
    helmet_results = pd.DataFrame()
    
    for scenario in scenarios:
        scenario = conf_scens[scenario]
        scenario_results_path = results_path / f"metro_boarding_stats_{scenario['year']}_{scenario['name']}.csv"
        results = pd.read_csv(scenario_results_path, sep=';')
        results['scenario'] = scenario['name']
        helmet_results = pd.concat([helmet_results, results], ignore_index=True)
    return helmet_results

def export_metro_boa_comparison(scenarios: list, results_path: Path, compare_data: Path):
    """This function compares Helmet metro boardings with
    HSL statistics.
    """
    helmet_volumes = pd.DataFrame()

    helmet_volumes = get_helmet_metro_boardings(scenarios, results_path)
    hsl_volumes = pd.read_csv(compare_data)

    # pivot table
    hsl_volumes['scenario'] = 'HSL_2023'
    helmet_volumes = pd.merge(helmet_volumes, hsl_volumes[['station', 'station_name']], on='station', how='left') # attach station names

    # join dataframes
    joined_data = pd.concat([hsl_volumes, helmet_volumes], ignore_index=True)

    # Pivot the data to have sources as columns
    pivot_data = joined_data.pivot(index=['station', 'station_name'], columns='scenario', values='nousijat')

    # Round values to the nearest zero decimal figure
    pivot_data = pivot_data.round(0)

    # Export results comparison by mode
    filename = f"metro_boa_comparison.csv"
    savefile = results_path / filename
    
    # Export results comparison by mode
    pivot_data.to_csv(savefile, sep=";", index=True)