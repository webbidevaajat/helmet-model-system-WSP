""" This module exports metro boarding statistics summary in csv and excel"""
import pandas
import config_scens
from pathlib import Path
from typing import Union
import inro.modeller as _m
import inro.emme.database.emmebank as _emmebank

def export_metro_stats(scenario: dict, emmebank: _emmebank, savefile: Path):
    """This function exports mode, area specific passenger volume statistics as a csv. 
    Results are saved to a user given path defined in main.
    Loops for each mode in link attributes. Aggregates volumes for each mode and area.
    """
    scenario_id = scenario["scenario_id"]
    network = emmebank.scenario(scenario_id).get_network()
    nodes = list(network.nodes())
    total_boardings = {i: 0 for i in range(1, 31)} # per station
    total_boardings["Yhteensa"] = 0

    for node in nodes:
        station = node["@station"]
        if station not in total_boardings.keys():
            continue
        total_boardings[station] += node["@transit_won_boa_vrk"] + node["@transit_len_boa_vrk"]

    total_boardings["Yhteensa"] = sum(total_boardings.values())
    total_boardings_df = pandas.DataFrame(list(total_boardings.items()), columns=["station", "nousijat"])
    total_boardings_df.set_index("station", inplace=True)

    total_boardings_df.to_csv(savefile, sep=";", index=True)
    
def save_metro_stats(run_scens: list, modeller: _m, results_path: Path):
    """Saves station boardings.
    """
    emmebank = modeller.emmebank
    conf_scens = config_scens.scenarios
    for scenario_name in run_scens:
        scenario = conf_scens[scenario_name]
        filename = f"metro_boarding_stats_{scenario['year']}_{scenario['name']}.csv"
        savefile = results_path / filename
        export_metro_stats(scenario, emmebank, savefile)
        print("Successfully exported volume stats for {}".format(scenario_name))