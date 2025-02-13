""" This module exports line statistics summary in csv and excel"""
import pandas
import config_scens
from pathlib import Path
from typing import Union
import inro.modeller as _m
import inro.emme.database.emmebank as _emmebank
from helmet_zone_params import kela_codes, municipalities, areas, day_to_year_factor

def export_transit_stats(scenario: dict, emmebank: _emmebank, savefile: Path):
    """This function exports mode and area specific statistics as a csv. 
    Results are saved to a user given path defined in main.
    Loops for each transit line and it's segments in network in order to fetch
    volume, boarding and transfer boarding values.
    """
    scenario_id = scenario["scenario_id"]
    network = emmebank.scenario(scenario_id).get_network()
    lines = list(network.transit_lines())
    total_transit_boa = {"b": 0, "g": 0, "m": 0, "t": 0, "p": 0, "r": 0}
    area_names = ["helsinki_other", "espoo_vant_kau", "surround_train", 
                 "surround_other", "peripheral"]
    area_totals = {name: {"total_boa": 0, "transfer_boa": 0, "first_boa": 0}
                   for name in area_names}

    for transit_line in lines:
        mode = str(transit_line.mode)
        if mode not in total_transit_boa.keys():
            continue
        for segment in transit_line.segments():
            # Total boardings
            total_transit_boa[mode] += get_boarding_volumes(segment)
            # Area specific boardings and transfers
            area_name, total_boa, transfer_boa = get_transfer_boardings(segment)
            if area_name is None:
                raise ValueError(f"Invalid area for transit line {transit_line.id} for segment {segment.id}")
            area_totals[area_name]["total_boa"] += total_boa
            area_totals[area_name]["transfer_boa"] += transfer_boa

    for area_name in area_totals:
        area_totals[area_name]["first_boa"] = (area_totals[area_name]["total_boa"] 
                                               - area_totals[area_name]["transfer_boa"])
    transit_volumes = (pandas.Series(total_transit_boa, name="boa_totals").round(-1)
                       .astype("int32") * day_to_year_factor)
    transit_volumes.index.name = "mode"
    area_boardings = pandas.DataFrame(area_totals).T
    area_boardings = area_boardings.round(-1).astype("int32") * day_to_year_factor
    area_boardings.index.name = "area"

    vol_path = savefile.parent / f"{savefile.stem}_volumes.csv"
    transit_volumes.to_csv(vol_path, sep=";")
    transfer_path = savefile.parent / f"{savefile.stem}_area_boardings.csv"
    area_boardings.to_csv(transfer_path, sep=";")


def get_boarding_volumes(segment) -> float:
    """ Aggregates general work and leisure boardings (vrk) on segment. """
    return segment["@transit_wor_boa_vrk"] + segment["@transit_lei_boa_vrk"]

def get_transfer_volumes(segment) -> float:
    """ Aggregates transfer work and leisure boardings (vrk) on segment. """
    return segment["@transit_wor_trb_vrk"] + segment["@transit_lei_trb_vrk"]

def get_transfer_boardings(segment) -> tuple:
    """Uses ui3 columns to fetch segment inode specific municipality id.
    This is further mapped to classify it under aggregated area ids.
    When correct aggregated area name is found, returns it's name and aggregated
    boardings and transfers (vrk).
    """
    kela_name = kela_codes[int(segment.i_node.data3)]
    kela_centroids = municipalities[kela_name]
    area_name = None
    total_boa = 0
    transfer_boa = 0
    for area, area_range in areas.items():
        # If area ids are simply tuple
        if isinstance(area_range[0], int):
            area_name = filter_area_ranges(area_range, kela_centroids, area, area_name)
        # Area ids are nested tuple, subloop
        else:
            for subarea in area_range:
                area_name = filter_area_ranges(subarea, kela_centroids, area, area_name)
        if area_name is not None:
                total_boa += get_boarding_volumes(segment)
                transfer_boa += get_transfer_volumes(segment)
                break
    return area_name, total_boa, transfer_boa

def filter_area_ranges(area_range: tuple, kela_centroids: tuple, 
                       area: str, area_name: None) -> Union[None, str]:
    """ Checks whether segment inode ui3 municipality id (kela centroids) 
    is within given id range of an area. This is measured as ids ranging from 
    value x to ranging until value y.
    If this range is within, area is given a name.
    """
    if (area_range[0] <= kela_centroids[0] <= area_range[1] and 
    area_range[0] <= kela_centroids[1] <= area_range[1]):
        area_name = area
    return area_name

def save_transit_stats(run_scens: list, modeller: _m, results_path: Path):
    """Saves public transit mode specific transit volumes and boardings, 
    and area specific transfer boardings.
    """
    emmebank = modeller.emmebank
    conf_scens = config_scens.scenarios
    for scenario_name in run_scens:
        scenario = conf_scens[scenario_name]
        filename = f"transit_stats_{scenario['year']}_{scenario['name']}.csv"
        savefile = results_path / filename
        export_transit_stats(scenario, emmebank, savefile)
        print("Successfully exported transit stats for {}".format(scenario_name))