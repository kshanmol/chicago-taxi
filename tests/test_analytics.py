import numpy as np
import json
from src.analytics import coordinate_to_cell, average_fare_heatmap, total_trips, average_speed_24hrs
from src.helpers import load_parquet, group_by_date, get_bounding_box

def test_coordinate_to_cell():
    data = load_parquet("tests/test_data.parquet")
    grouped_data = group_by_date(data)
    bounding_box = get_bounding_box(data)

    lat1, long1 = data['pickup_latitude'].min(), data['pickup_longitude'].min()
    lat2, long2 = data['pickup_latitude'].max(), data['pickup_longitude'].max()

    cell1 = coordinate_to_cell(lat1, long1, bounding_box)
    assert cell1 == 0
    cell2 = coordinate_to_cell(lat2, long2, bounding_box)
    assert cell2 == 3
    error = coordinate_to_cell(0, 0, bounding_box)
    assert(error == "Error: Latitude out of range")
    error = coordinate_to_cell(np.nan, np.nan, bounding_box)
    assert(error == "Error: NaN values found")

def test_average_fare_heatmap():
    data = load_parquet("tests/test_data.parquet")
    grouped_data = group_by_date(data)
    bounding_box = get_bounding_box(data)

    result = average_fare_heatmap("2020-02-05", grouped_data, bounding_box)
    assert json.dumps(result) == '{"data": [{"cell_id": 1, "fare": "13.50", "count": 1}, {"cell_id": 3, "fare": "9.25", "count": 1}]}'

def test_total_trips():
    data = load_parquet("tests/test_data.parquet")
    grouped_data = group_by_date(data)

    result = total_trips("2020-02-04", "2020-02-05", grouped_data)
    assert json.dumps(result) == '{"data": [{"date": "2020-02-04", "total_trips": 0}, {"date": "2020-02-05", "total_trips": 2}]}'

def test_average_speed_24hrs():
    data = load_parquet("tests/test_data.parquet")
    grouped_data = group_by_date(data)
    
    result = average_speed_24hrs("2020-02-06", grouped_data)
    assert json.dumps(result) == '{"data": [{"average_speed": "20.82"}]}'