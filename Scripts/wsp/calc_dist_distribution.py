import config_scens
import pandas

def export_distance_distributions(scenario, emmebank, dist_bins, results_path):
    """Extracts demand and distances using user given mf ids.
    Splits distances into user defined distance bins and aggregates demand
    over split bins. Saves results as csv into user given output path.
    """
    demand_mtx = emmebank.matrix(scenario["demand_mtx_id"])
    demand_mtx = demand_mtx._get_numpy_data().flatten()
    dist_mtx = emmebank.matrix(scenario["dist_mtx_id"])
    dist_mtx = dist_mtx._get_numpy_data().flatten()
    mockup = pandas.DataFrame({"demand": demand_mtx, "dist": dist_mtx})
    bin_labels = create_bin_labels(dist_bins)
    # Bin must be one longer than bin labels
    dist_bins.append(dist_bins[-1] + 1)
    bin_df = pandas.cut(mockup["dist"], dist_bins, right=False, labels=bin_labels)
    bins_name = "dist_bins"
    bin_df = bin_df.fillna(bin_labels[-1]).rename(bins_name)
    mockup = mockup.merge(bin_df, left_index=True, right_index=True, how="left")
    mockup = mockup.groupby(by=bins_name)["demand"].sum().reset_index()
    mockup.to_csv(results_path, sep="\t")

def create_bin_labels(dist_bins: list):
    """Creates bin labels through user given distance bins."""
    bin_labels = []
    for i in range(len(dist_bins)):
        try:
            bin_labels.append(f"{dist_bins[i]}-{dist_bins[i+1]}")
        except IndexError:
            bin_labels.append(f"{dist_bins[i]}+")
    return bin_labels

def save_dd_data(run_scens, modeller, dist_bins, results_path):
    """Aggregated demand based on distance bins."""
    emmebank = modeller.emmebank
    conf_scens = config_scens.scenarios
    for scenario_name in run_scens:
        scenario = conf_scens[scenario_name]
        filename = f"distance_distribution_{scenario['result_name']}.csv"
        savefile = results_path / filename
        export_distance_distributions(scenario, emmebank, dist_bins, savefile)