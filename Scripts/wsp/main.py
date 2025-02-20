import inro.emme.desktop.app as _app
import inro.modeller as _m
from pathlib import Path
from time import process_time

import config_scens
from line_statistics import get_transit_stats
from calc_dist_distribution import get_dd_data
from compare import compare_by_mode, compare_by_area


def main():
    time_start = process_time()
    
    emme_proj_path = Path("C:/EMME projects/Helmet testaus/Helmet_testaus/")
    emp_name = "Helmet_testaus.emp"
    emmepath = emme_proj_path / emp_name
    desktop = _app.start_dedicated(
        project=emmepath, visible=False, user_initials="WSP")
    modeller = _m.Modeller(desktop)
    results_path = emme_proj_path / "Output"
    hsl_statistics = Path("")

    run_scens = [scen_name for scen_name in config_scens.scenarios]
    dist_bins = [0, 1, 3, 5, 7, 10, 15, 25, 50]
    
    get_transit_stats(run_scens, modeller, results_path)
    get_dd_data(run_scens, modeller, dist_bins, results_path)
    compare_by_mode(run_scens, results_path, hsl_statistics / "HSL_stats_mode.csv")
    compare_by_area(run_scens, results_path)

    time_stop = process_time()
    print(f"----- Program execution time {time_stop - time_start} seconds")

main()
