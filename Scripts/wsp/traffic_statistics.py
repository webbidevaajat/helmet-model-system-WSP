""" This module exports line statistics summary in csv and excel"""
import pandas
import config_scens
from pathlib import Path
from typing import Union
import inro.modeller as _m
import inro.emme.database.emmebank as _emmebank
from helmet_zone_params import kela_codes, municipalities, areas, day_to_year_factor

def export_volume_stats(scenario: dict, emmebank: _emmebank, savefile: Path):
    """This function exports mode, area specific passenger volume statistics as a csv. 
    Results are saved to a user given path defined in main.
    Loops for each mode in link attributes. Aggregates volumes for each mode and area.
    """
    scenario_id = scenario["scenario_id"]
    network = emmebank.scenario(scenario_id).get_network()
    links = list(network.links())
    total_volume = {"Juna": 0, "Raitiovaunu": 0, "Linja-auto": 0, "Metro": 0, "Henkiloautot": 0}
    area_codes = {1: "Niemen raja", 2: "Kantakaupungin raja", 3: "Lantinen poikittalinja"}
    area_totals = {mode: {area_codes[code]: 0 for code in area_codes} for mode in total_volume}

    for link in links:
        area = link["@raja"]
        if area not in area_codes.keys():
            continue
        modes = link.modes
        mode_ids = []
        for mode in modes:
            mode_ids += str(mode.id)
        if "c" in mode_ids:
            # auto
            area_totals["Henkiloautot"][area_codes[area]] += link["@car_work_vrk"] + link["@car_leisure_vrk"] + link["@trailer_truck_vrk"] + link["@truck_vrk"] + link["@van_vrk"]
            # linja-auto
            area_totals["Linja-auto"][area_codes[area]] += link["@transit_work_vrk"] + link["@transit_leisure_vrk"]
        # juna
        elif any(mode in mode_ids for mode in ["j", "r"]):
            area_totals["Juna"][area_codes[area]] += link["@transit_work_vrk"] + link["@transit_leisure_vrk"]
        # raitiovaunu
        elif any(mode in mode_ids for mode in ["p", "t"]):
            area_totals["Raitiovaunu"][area_codes[area]] += link["@transit_work_vrk"] + link["@transit_leisure_vrk"]
        # metro
        elif "m" in mode_ids:
            area_totals["Metro"][area_codes[area]] += link["@transit_work_vrk"] + link["@transit_leisure_vrk"]

    total_volumes = pandas.DataFrame(area_totals).T
    total_volumes.index.name = "mode"

    # Pivot data
    total_volumes = total_volumes.reset_index().melt(id_vars=["mode"], var_name="area", value_name="vrk")

    # Sum results
    joukkoliikenne = total_volumes[total_volumes["mode"].isin(["Juna", "Raitiovaunu", "Metro", "Linja-auto"])].groupby("area")["vrk"].sum().reset_index()
    joukkoliikenne["mode"] = "Joukkoliikenne"

    yhteensa = total_volumes.groupby("area")["vrk"].sum().reset_index()
    yhteensa["mode"] = "Yhteensa"

    # Append sum rows to original dataframe
    total_volumes = pandas.concat([total_volumes, joukkoliikenne, yhteensa], ignore_index=True)

    vol_path = savefile.parent / f"{savefile.stem}_volumes.csv"
    total_volumes.to_csv(vol_path, sep=";", index=False)

def save_volume_stats(run_scens: list, modeller: _m, results_path: Path):
    """Saves all mode volumes on defined links, by area and mode to a csv file.
    """
    emmebank = modeller.emmebank
    conf_scens = config_scens.scenarios
    for scenario_name in run_scens:
        scenario = conf_scens[scenario_name]
        filename = f"volume_stats_{scenario['year']}_{scenario['name']}.csv"
        savefile = results_path / filename
        export_volume_stats(scenario, emmebank, savefile)
        print("Successfully exported volume stats for {}".format(scenario_name))