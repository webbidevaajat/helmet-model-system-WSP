import inro.emme.desktop.app as _app
import inro.modeller as _m
from time import process_time
from pathlib import Path

from line_statistics import get_transit_stats


def main():
    time_start = process_time()

    emme_proj_path = Path("C:/emmeproj/HELMET41/emme_testnetwork")
    emp_name = "Linjasto_2040.emp"
    emmepath = emme_proj_path / emp_name
    desktop = _app.start_dedicated(
        project=emmepath, visible=False, user_initials="WSP")
    modeller = _m.Modeller(desktop)
    results_path = Path(__file__).parent / "results"
    run_scens = ["VE0 2024"]
    get_transit_stats(run_scens, modeller, results_path)

    time_stop = process_time()
    print(f"----- Program execution time {time_stop - time_start} seconds")

main()