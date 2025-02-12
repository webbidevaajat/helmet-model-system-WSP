import sys
from os import path
from time import process_time
import inro.emme.desktop.app as _app
import inro.modeller as _m
from pathlib import Path
import matplotlib.pyplot as plt

from line_statistics import get_transit_stats

def main():
    time_start = process_time()
    

    emme_proj_path = Path("C:/EMME projects/Helmet testaus/Helmet_testaus/")
    emp_name = "Helmet_testaus.emp"
    emmepath = emme_proj_path / emp_name
    desktop = _app.start_dedicated(
        project=emmepath, visible=False, user_initials="WSP")
    modeller = _m.Modeller(desktop)
    results_path = emme_proj_path / "Output"
    run_scens = ["Helmet 4", "Helmet 5"]
    get_transit_stats(run_scens, modeller, results_path)
    

    time_stop = process_time()
    print(f"----- Program execution time {time_stop - time_start} seconds")

main()