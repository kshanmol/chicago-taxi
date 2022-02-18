import os
import pandas as pd

from src.helpers import load_parquet, group_by_date, get_bounding_box

def test_load_parquet():
    """
    Test loading a parquet file into a pd DataFrame
    """
    data = load_parquet("tests/test_data.parquet")
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 20

def test_group_by_date():
    """
    Test group by date function returns a dict with a key for each date
    """
    data = load_parquet("tests/test_data.parquet")
    grouped_data = group_by_date(data)
    assert isinstance(grouped_data, dict)
    assert len(grouped_data.keys()) == 366

def test_get_bounding_box():
    """
    Test the bounding box for the test data file
    """
    data = load_parquet("tests/test_data.parquet")
    bounding_box = get_bounding_box(data, delta=0.01)
    assert isinstance(bounding_box, dict)
    assert bounding_box['lat_min'] == data['pickup_latitude'].min() - 0.01
    assert bounding_box['lat_max'] == data['pickup_latitude'].max() + 0.01
    assert bounding_box['long_min'] == data['pickup_longitude'].min() - 0.01
    assert bounding_box['long_max'] == data['pickup_longitude'].max() + 0.01
    assert len(bounding_box.keys()) == 4