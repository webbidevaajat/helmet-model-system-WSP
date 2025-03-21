import json
import subprocess
import openmatrix as omx
import numpy as np
import os
import shutil

# Define the path to the dev-config.json file and helmet.py script
config_path = "c:\\GitHub\\helmet-model-system\\Scripts\\dev-config.json"
result_path = "C:\\emmeproj\\HELMET5_elasticity_tests\\Results\\"
base_scen = "Helmet5_2023"
lahtotiedot_path = "C:\\emmeproj\\HELMET5_elasticity_tests\\Ennusteskenaarioiden_syottotiedot\\"
base_lahtotiedot = "2023_decrease_car_dist_price_10_percent"
helmet_script_path = "c:\\GitHub\\helmet-model-system\\Scripts\\helmet.py"

# Define scenarios and the factors by which to multiply the impedance matrices
scens = {
    "Helmet5_2023_PT_plus_10_percent": {
        "matrices": {"transit_work_uncongested": 1.1, "transit_leisure_uncongested": 1.1},
        "type": "time"},
    "Helmet5_2023_car_plus_10_percent": {
        "matrices": {"car_work": 1.1, "car_leisure": 1.1},
        "type": "time"},
    "Helmet5_2023_PT_plus_50_percent": {
        "matrices": {"transit_work_uncongested": 1.5, "transit_leisure_uncongested": 1.5},
        "type": "time"},
    "Helmet5_2023_car_plus_50_percent": {
        "matrices": {"car_work": 1.5, "car_leisure": 1.5},
        "type": "time"},
    "2023_decrease_car_dist_price_10_percent": {
        "matrices": {"car_work": 0.9, "car_leisure": 0.9},
        "type": "dist"},
    "2023_decrease_car_dist_price_20_percent": {
        "matrices": {"car_work": 0.8, "car_leisure": 0.8},
        "type": "dist"},
    "2023_increase_car_dist_price_10_percent": {
        "matrices": {"car_work": 1.1, "car_leisure": 1.1},
        "type": "dist"},
    "2023_increase_car_dist_price_20_percent": {
        "matrices": {"car_work": 1.2, "car_leisure": 1.2},
        "type": "dist"},
    "2023_decrease_pt_price_10_percent":    {
        "matrices": {"transit_work": 0.9, "transit_leisure": 0.9},
        "type": "cost"},
    "2023_increase_pt_price_10_percent":{
        "matrices": {"transit_work": 1.1, "transit_leisure": 1.1},
        "type": "cost"},
    "base_2023_mock":{
        "matrices": {"transit_work": 1.0, "transit_leisure": 1.0},
        "type": "cost"},
    }

# Function to modify the configuration
def modify_config(config, scen_name, forecast_data):
    config["SCENARIO_NAME"] = scen_name
    config["OPTIONAL_FLAGS"] = ["DO_NOT_USE_EMME"]
    config["FORECAST_DATA_PATH"] = forecast_data
    return config

for s in scens:
    #Copy result folder
    target_folder = "{}{}".format(result_path, s)
    shutil.copytree("{}{}/matrices".format(result_path, base_scen), f"{target_folder}/matrices", dirs_exist_ok = True)
    
    #Modify impedance matrices
    for time in ["aht", "pt", "iht"]:
        for mat in scens[s]["matrices"].keys():
            with omx.open_file("{}/matrices/{}_{}.omx".format(target_folder,scens[s]["type"], time), 'a') as mtxfile:
                matrix = mtxfile[mat][:]
                # Modify the matrix by multiplying it
                modified_matrix = matrix * scens[s]["matrices"][mat]
                # Save the modified matrix back to the OMX file
                del mtxfile[mat]
                mtxfile[mat] = modified_matrix
    
    # Read the original configuration
    with open(config_path, 'r') as file:
        original_config = json.load(file)
        modified_config = modify_config(original_config.copy(), s, lahtotiedot_path + base_lahtotiedot)
        
    # Save the modified configuration
    with open(config_path, 'w') as file:
        json.dump(modified_config, file, indent=4)
        
    # Run the helmet.py script
    subprocess.run(["python", helmet_script_path])