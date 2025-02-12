""" This module exports line statistics summary in csv and excel"""
import pandas
import config_scens
from pathlib import Path
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
    modes = {"b": 0, "g": 0, "m": 0, "t": 0, "p": 0, "r":0}
    total_vol = {
        "transit_boa": modes
    }
    area_totals = {
        "helsinki_other": {"total_boa": 0, "transfer_boa": 0, "first_boa": 0},
        "espoo_vant_kau": {"total_boa": 0, "transfer_boa": 0, "first_boa": 0},
        "surround_train": {"total_boa": 0, "transfer_boa": 0, "first_boa": 0},
        "surround_other": {"total_boa": 0, "transfer_boa": 0, "first_boa": 0},
        "peripheral": {"total_boa": 0, "transfer_boa": 0, "first_boa": 0}
    }

    for transit_line in lines:
        mode = str(transit_line.mode)
        if mode not in modes.keys():
            continue
        # Transit boardings by area
        for segment in transit_line.segments():
            boa = get_transit_volumes(segment)
            total_vol["transit_boa"][mode] += boa

        # Total trips by area
        area_name, total_boa, transfer_boa = get_transfer_boardings(segment)
        if area_name is None:
            raise ValueError(f"Invalid area for transit line {transit_line.id} for segment {segment.id}")
        area_totals[area_name]["total_boa"] += total_boa
        area_totals[area_name]["transfer_boa"] += transfer_boa

    for area_name in area_totals:
        area_totals[area_name]["first_boa"] = area_totals[area_name]["total_boa"] - area_totals[area_name]["transfer_boa"]
    
    transit_volumes = pandas.DataFrame(total_vol).round(-1).astype("int32") * day_to_year_factor
    transit_volumes.index.name = "mode"
    area_boardings = pandas.DataFrame(area_totals).T
    area_boardings = area_boardings.round(-1).astype("int32") * day_to_year_factor
    transit_volumes.index.name = "area"

    vol_path = savefile.parent / f"{savefile.stem}_volumes.csv"
    transit_volumes.to_csv(vol_path, sep=";")
    transfer_path = savefile.parent / f"{savefile.stem}_area_boardings.csv"
    area_boardings.to_csv(transfer_path, sep=";", index=True)


def get_transit_volumes(segment):
    """ Aggregates work and leisure boardings (vrk).
    Returns as separate variables (tuple).
    """
    boa_vrk = segment["@transit_wor_boa_vrk"] + segment["@transit_lei_boa_vrk"]
    return boa_vrk

def get_transfer_boardings(segment):
    """Uses ui3 columns to fetch segment inode specific municipality id.
    This is further mapped to classify it under aggregated area ids.
    When correct aggregated area name is found, returns it's name and aggregated
    work and leisure transfers (vrk).
    """
    kela_name = kela_codes[int(segment.i_node.data3)]
    kela_centroids = municipalities[kela_name]
    
    total_boa = 0
    transfer_boa = 0
    area_name = None
    for area, area_range in areas.items():
        # If area ids are not nested tuple
        if isinstance(area_range[0], int):
            if (area_range[0] <= kela_centroids[0] <= area_range[1] and 
            area_range[0] <= kela_centroids[1] <= area_range[1]):
                area_name = area
                total_boa += (segment.i_node["@transit_won_boa_vrk"]
                                + segment.i_node["@transit_len_boa_vrk"])
                transfer_boa += (segment.i_node["@transit_won_trb_vrk"] 
                                + segment.i_node["@transit_len_trb_vrk"])
                
                break
        # Area ids are nested tuple, subloop
        else:
            for subarea in area_range:
                if (subarea[0] <= kela_centroids[0] <= subarea[1] and 
                subarea[0] <= kela_centroids[1] <= subarea[1]):
                    area_name = area
                    total_boa += (segment.i_node["@transit_won_boa_vrk"]
                                    + segment.i_node["@transit_len_boa_vrk"])
                    transfer_boa += (segment.i_node["@transit_won_trb_vrk"] 
                                    + segment.i_node["@transit_len_trb_vrk"])
                    break
    return area_name, total_boa, transfer_boa


def get_transit_stats(run_scens: list, modeller: _m, results_path: Path):
    """Returns public transit mode specific transit volumes and boardings, 
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