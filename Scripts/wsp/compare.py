import pandas as pd
import config_scens
from pathlib import Path

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

def compare_by_mode(scenarios: list, results_path: Path, compare_data: Path):
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

   
def compare_by_area(scenarios: list, results_path: Path):
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
   