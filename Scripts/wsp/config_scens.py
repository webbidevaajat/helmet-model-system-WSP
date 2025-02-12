"""Define Emme scenario related parameters."""
# Scenario related settings
scenarios = {
    "Helmet 4": {
        "result_name": "Helmet 4",
        "input_name": "Helmet 4",
        "year": "2023",
        "name": "Helmet 4",
        "scenario_id": 1,
        "emme_matrix_id": 100,
    },
    "Helmet 5": {
        "result_name": "Helmet 5",
        "input_name": "Helmet 5",
        "year": "2023",
        "name": "Helmet 5",
        "scenario_id": 2,
        "emme_matrix_id": 200,
    }
}
# these id:s will be added to scenario-specific emme_matrix_id e.g. 100 + 21 = mf121
mat_ids = {
    "pop": 21,
    "wrk": 22,
    "origins_matrix": {"car": 23, "transit": 24, "bike": 25, "walk": 26},
    "shares_matrix": {"car": 27, "transit": 28, "bike": 29, "walk": 30},
    "car_density": 31,
    "wrk_access": 32,
    "wrk_transit_access": 33,
    "benefit_matrix": {"time_transit_work": 34, "time_transit_leisure": 35},
    "wrk_access_index": 36,
    "weighted_time": 80,
    "real_time": 81,
    "demand_matrix": {
        "aht": {
            "car_work": 1, "car_leisure": 2,  "transit_work": 3,
            "transit_leisure": 4, "bike": 5, "trailer_truck": 7,
            "truck": 8, "van": 9, "dem_raskas": 10,
        },
        "iht": {
            "car_work": 11, "car_leisure": 12,  "transit_work": 13,
            "transit_leisure": 14, "bike": 15, "trailer_truck": 17,
            "truck": 18, "van": 19, "dem_raskas": 20,
        },
    },
    "time_matrix": {
        "aht": {
            "car_work": 31, "car_leisure": 32,  "transit_work": 33,
            "transit_leisure": 34, "bike": 35, "trailer_truck": 37,
            "truck": 38, "van": 39, "dem_raskas": 40,
        },
        "iht": {
            "car_work": 41, "car_leisure": 42,  "transit_work": 43,
            "transit_leisure": 44, "bike": 45, "trailer_truck": 47,
            "truck": 48, "van": 49, "dem_raskas": 50,
        },
    },
}
