import pandas as pd
import numpy as np
import datetime

import pyarrow.parquet as pq

from collections import defaultdict
from helpers import range_first_date, range_last_date, KMS_TO_MILES, HOURS_TO_SECS

def coordinate_to_cell(latitude, longitude, bounding_box, grid_side_length=2):
    """
    Maps a (latitude, longitude) coordinate pair to a cell number 
    in the N * N grid defined inside the bounding box where N is 
    the grid_side_length (number of cells in one side of the grid)
    """

    if np.isnan(latitude) or np.isnan(longitude):
        return "Error: NaN values found"

    lat_range = bounding_box['lat_max'] - bounding_box['lat_min']
    lat_span = (latitude - bounding_box['lat_min']) / lat_range
    long_range = bounding_box['long_max'] - bounding_box['long_min']
    long_span = (longitude - bounding_box['long_min']) / long_range
    grid_unit = 1.0 / grid_side_length

    if not (lat_span <= 1.0 and lat_span >= 0.0):
        return "Error: Latitude out of range"
    if not (long_span <= 1.0 and long_span >= 0.0):
        return "Error: Longitude out of range"

    horiz_cell = long_span // grid_unit
    vert_cell = lat_span // grid_unit
    cell_number = horiz_cell + grid_side_length * vert_cell
    return int(cell_number)

def average_fare_heatmap(date, groups, bounding_box, grid_side=2):
    """
    Calculates the average fare heatmap for a given date
    based on the pickup latitude and longitude. The heatmap 
    is built as a (grid_side * grid_side) grid within the 
    given bounding box.
    """

    date = pd.to_datetime(date, format="%Y-%m-%d", yearfirst=True)
    fares_map = defaultdict(list)
    average_fare_heat_map = {}
    for row in groups[date].index:
        cell = coordinate_to_cell(groups[date]['pickup_latitude'][row], groups[date]['pickup_longitude'][row], bounding_box, grid_side)
        fare = groups[date]['fare'][row]
        if isinstance(cell, int) and not np.isnan(fare): # we did not encounter nan values
            fares_map[cell].append(fare)

    result = {"data" : []}
    for cell in fares_map.keys():
        average_fare = sum(fares_map[cell]) / (1.0 * len(fares_map[cell]))
        result["data"].append({"cell_id": cell, "fare": f'{average_fare:.2f}', "count" : len(fares_map[cell])})
        
    return result

def total_trips(start_date, end_date, groups):
    """
    Returns the number of total trips on each date in the given range
    (inclusive of both start_date and end_date)
    """
    start_date = pd.to_datetime(start_date, format="%Y-%m-%d", yearfirst=True)
    end_date = pd.to_datetime(end_date, format="%Y-%m-%d", yearfirst=True)

    if end_date < start_date:
        return "Error: End date cannot be before start date"
    if start_date < range_first_date:
        return "Error: Start not in range"
    if end_date > range_last_date:
        return "Error: End date not in range"

    delta = datetime.timedelta(days=1)
    result = {"data" : []}
    while(start_date <= end_date):
        trips = {"date" : start_date.strftime('%Y-%m-%d'), "total_trips": len(groups[start_date].index)}
        result['data'].append(trips)
        start_date += delta
    
    return result

def average_speed_24hrs(date, groups):
    """
    Returns the average km/hr speed in the past 24 hours of the 
    given date i.e. we consider all trips made on the previous date.
    """
    date = pd.to_datetime(date, format="%Y-%m-%d", yearfirst=True)
    target_date = date - datetime.timedelta(days=1)
    if target_date < range_first_date or target_date > range_last_date:
        return "Error: Date not in range"

    total_km = groups[target_date]['trip_miles'].sum() * KMS_TO_MILES
    total_hr = groups[target_date]['trip_seconds'].sum() / HOURS_TO_SECS
    average_speed = total_km / total_hr

    result = {"data" : [ {"average_speed" : f'{average_speed:.2f}'} ]}
    return result
