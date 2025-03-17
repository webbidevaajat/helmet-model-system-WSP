import inro.emme.desktop.app as _app
import inro.modeller as _m
from pathlib import Path
from time import process_time

import config_scens
from line_statistics import save_transit_stats

#from calc_dist_distribution import get_dd_data
from line_statistics import save_transit_stats
from compare_boarding import export_boa_comparison_by_mode, export_boa_comparison_by_area, export_boa_per_trip_comparison, plot_boa_comparison_by_mode, plot_boa_per_trip_comparison
from traffic_statistics import save_traffic_stats
from compare_traffic import export_traffic_comparison, plot_traffic_comparison


def main():
    time_start = process_time()
    
    emme_proj_path = Path("C:/emmeproj/Helmet testaus/Helmet_testaus/")
    emp_name = "Helmet_testaus.emp"
    emmepath = emme_proj_path / emp_name
    desktop = _app.start_dedicated(
        project=emmepath, visible=False, user_initials="WSP")
    modeller = _m.Modeller(desktop)
    results_path = emme_proj_path / "Output"
    hsl_statistics = Path("")
    hsl_traffic_statistics = Path("")

    run_scens = [scen_name for scen_name in config_scens.scenarios]
    dist_bins = [0, 1, 3, 5, 7, 10, 15, 25, 50]
    
    save_transit_stats(run_scens, modeller, results_path)
    export_boa_comparison_by_mode(run_scens, results_path, hsl_statistics / "HSL_stats_mode.csv")
    export_boa_comparison_by_area(run_scens, results_path)
    export_boa_per_trip_comparison(run_scens, results_path)
    plot_boa_comparison_by_mode(results_path)
    plot_boa_per_trip_comparison(results_path)
    save_traffic_stats(run_scens, modeller, results_path)
    export_traffic_comparison(run_scens, results_path, hsl_traffic_statistics /  "combined.csv")
    plot_traffic_comparison(results_path)

    time_stop = process_time()
    print(f"----- Program execution time {time_stop - time_start} seconds")

main()
