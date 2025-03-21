import os
import pandas as pd

model_result_path = "C:\\emmeproj\\HELMET5_elasticity_tests\\Results\\"
output_path = "C:\\emmeproj\\HELMET5_elasticity_tests\\output\\"
base_scen = "base_2023_mock"

scens = {
    "Helmet5_2023_PT_plus_10_percent": 0.1,
    "Helmet5_2023_PT_plus_50_percent": 0.5,
    "2023_decrease_pt_price_10_percent": -0.1,
    "2023_increase_pt_price_10_percent": 0.1,
    "Helmet5_2023_car_plus_10_percent": 0.1,
    "Helmet5_2023_car_plus_50_percent": 0.5,
    "2023_decrease_car_dist_price_20_percent": -0.2,
    "2023_decrease_car_dist_price_10_percent": -0.1,
    "2023_increase_car_dist_price_10_percent": 0.1,
    "2023_increase_car_dist_price_20_percent": 0.2,
    }

def calculate_sums(file_path):
    # Read the origins_demand.txt file into a DataFrame
    df = pd.read_csv(file_path, sep='\t', index_col=0)
    
    # Calculate the sum of each column
    column_sums = df.sum()
    return column_sums

def main(model_result_path, base_scen):
    base_scen_path = os.path.join(model_result_path, base_scen, "trips_areas.txt")

    # Calculate the column sums for the base scenario
    base_sums = calculate_sums(base_scen_path)

    # Create a DataFrame to store the results
    results_df = pd.DataFrame(columns=["Scenario"] + list(base_sums.index))
    row = pd.DataFrame(
                {"Scenario": [base_scen], **base_sums}
            )
    results_df = pd.concat([results_df, row], ignore_index=True)
    difference_df = results_df
    relative_df = results_df
    elasticities_df  = results_df

    # Loop through each folder in the result_path
    for s in scens:
        folder_path = os.path.join(model_result_path, s)
        file_path = os.path.join(folder_path, "trips_areas.txt")
        mode_sums = calculate_sums(file_path)
        differences = mode_sums - base_sums
        differences_relative = differences / base_sums
        elasticities= differences_relative / scens[s]
        
        row = pd.DataFrame({"Scenario": [s], **mode_sums})
        results_df = pd.concat([results_df, row], ignore_index=True)
        
        row = pd.DataFrame({"Scenario": [s], **differences})
        difference_df = pd.concat([difference_df, row], ignore_index=True)
        
        row = pd.DataFrame({"Scenario": [s], **differences_relative})
        relative_df = pd.concat([relative_df, row], ignore_index=True)

        row = pd.DataFrame({"Scenario": [s], **elasticities})
        elasticities_df = pd.concat([elasticities_df, row], ignore_index=True)
    
    # Print the results
    print(elasticities_df.round(2))
    results_df.to_csv(output_path + "demands.csv", index=False)
    difference_df.to_csv(output_path + "demand_changes.csv", index=False)
    relative_df.round(2).to_csv(output_path + "demand_change_relative.csv", index=False)
    elasticities_df.round(2).to_csv(output_path + "elasticity.csv", index=False)

if __name__ == "__main__":
    main(model_result_path, base_scen)