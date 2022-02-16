import pandas as pd
import datetime

import pyarrow.parquet as pq

cols = ['unique_key', 'taxi_id', 'trip_start_timestamp', 'trip_end_timestamp', 
'trip_seconds', 'trip_miles', 'fare', 'trip_total', 'pickup_latitude', 'pickup_longitude']

range_first_date = pd.to_datetime("2020-01-01", format="%Y-%m-%d", yearfirst=True)
range_last_date = pd.to_datetime("2020-12-31", format="%Y-%m-%d", yearfirst=True)

def load_parquet(path, columns=cols):
    table = pq.read_table(path, columns=columns)
    return table.to_pandas()

def group_by_date(table):
    groups = {}

    start_date = range_first_date
    delta = datetime.timedelta(days=1)

    while(start_date <= range_last_date):
        next_date = start_date + delta
        mask = (table['trip_start_timestamp'] >= start_date) & (table['trip_start_timestamp'] < next_date)
        groups[start_date] = table[mask]
        start_date = next_date
    
    return groups

def total_trips(start_date, end_date, groups):

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

    date = pd.to_datetime(date, format="%Y-%m-%d", yearfirst=True)
    target_date = date - datetime.timedelta(days=1)
    if target_date < range_first_date or target_date > range_last_date:
        return "Error: Date not in range"

    total_km = groups[target_date]['trip_miles'].sum() * 1.60934
    total_hr = groups[target_date]['trip_seconds'].sum() / (3600.0)
    average_speed = total_km / total_hr

    result = {"data" : [ {"average_speed" : f'{average_speed:.2f}'} ]}
    return result

