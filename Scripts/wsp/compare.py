import pandas as pd
import bokeh as bk
from bokeh.plotting import figure, output_file, save
from bokeh.io import show
from bokeh.transform import dodge
from bokeh.models import ColumnDataSource

def get_helmet_boarding_results(scenarios: list, results_path: Path)
    """This function reads the csv files for boardings and compares results.
    """
    helmet_results = pd.DataFrame()
    
    for scenario in scenarios:
        scenario_results_path = results_path / f"transit_stats_{scenario['year']}_{scenario['name']}.csv"
        results = pd.read_csv(scenario_results_path)
        #results = results[['', '']]
        results['scenario'] = scenario['name']
        helmet_results = pd.concat([helmet_results, data], ignore_index=True)

    return helmet_results

def compare_by_mode(scenarios: list, results_path: Path, compare_data: Path):
    """This function compares the boarding totals of Helmet with 
    real boarding statistics by mode.
    """

    helmet_boardings = get_helmet_boarding_results(scenarios, results_path)
    hsl_boardings = pd.read_csv(compare_data)

    # join dataframes
    helmet_boardings[['mode_name', 'mode', 'nousijat_2023']]
    helmet_boardings = helmet_boardings.rename(columns={'nousijat_2023': 'boardings'})
    hsl_boardings['scenario'] = 'HSL'

    # Perform inner join on different column names
    merged_data = pd.merge(helmet_boardings, hsl_boardings, left_on='mode', right_on='mode', how='inner')
    
    # Group by mode and source, then sum the boardings
    grouped_data = merged_data.groupby(['mode_name', 'mode', 'scenario']).sum().reset_index()

    # Pivot the data to have sources as columns
    pivot_data = grouped_data.pivot(index='mode_name', columns='scenario', values='boardings')

    # Prepare data for Bokeh
    pivot_data = pivot_data.reset_index()
    source = ColumnDataSource(pivot_data)

    # Define output file
    output_file("boarding_totals_by_mode.html")

    # Create a figure
    p = figure(x_range=pivot_data['mode_name'], plot_height=400, plot_width=800, title="Miljoonaa nousijaa",
               toolbar_location=None, tools="")

    # Add bars for each scenario
    scenarios = pivot_data.columns[1:]
    colors = ["#c9d9d3", "#718dbf", "#e84d60"]
    for i, scenario in enumerate(scenarios):
        p.vbar(x=dodge('mode_name', -0.25 + i*0.25, range=p.x_range), top=scenario, width=0.2, source=source,
               color=colors[i], legend_label=scenario)

    # Customize plot
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Kulkumuoto"
    p.yaxis.axis_label = "Miljoonaa nousijaa"
    p.xaxis.major_label_orientation = 1.2
    p.legend.title = "Data"
    p.legend.location = "top_left"

    # Save and show the plot
    save(p)
    show(p)
   
def compare_by_area(scenarios: list, results_path: Path, compare_data: Path):
    """This function compares the boarding totals of Helmet with 
    real boarding statistics by area.
    """

    helmet_boardings = get_helmet_boarding_results(scenarios, results_path)
    hsl_boardings = pd.read_csv(compare_data)

    # join dataframes
    helmet_boardings[['area_name', 'area', 'nousijat_2023']]
    helmet_boardings = helmet_boardings.rename(columns={'nousijat_2023': 'boardings'})
    hsl_boardings['scenario'] = 'HSL'

    # Perform inner join on different column names
    merged_data = pd.merge(helmet_boardings, hsl_boardings, left_on='area', right_on='area', how='inner')
    
    # Group by area and source, then sum the boardings
    grouped_data = merged_data.groupby(['area_name', 'area', 'scenario']).sum().reset_index()

    # Pivot the data to have sources as columns
    pivot_data = grouped_data.pivot(index='area_name', columns='scenario', values='boardings')

    # Prepare data for Bokeh
    pivot_data = pivot_data.reset_index()
    source = ColumnDataSource(pivot_data)

    # Define output file
    output_file("boarding_totals_by_area.html")

    # Create a figure
    p = figure(x_range=pivot_data['area_name'], plot_height=400, plot_width=800, title="Miljoonaa nousijaa",
               toolbar_location=None, tools="")

    # Add bars for each scenario
    scenarios = pivot_data.columns[1:]
    colors = ["#c9d9d3", "#718dbf", "#e84d60"]
    for i, scenario in enumerate(scenarios):
        p.vbar(x=dodge('area_name', -0.25 + i*0.25, range=p.x_range), top=scenario, width=0.2, source=source,
               color=colors[i], legend_label=scenario)

    # Customize plot
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Alue"
    p.yaxis.axis_label = "Miljoonaa nousijaa"
    p.xaxis.major_label_orientation = 1.2
    p.legend.title = "Data"
    p.legend.location = "top_left"

    # Save and show the plot
    save(p)
    show(p)
   