import pandas as pd
import numpy as np
import datetime

import pyarrow.parquet as pq

from collections import defaultdict

range_first_date = pd.to_datetime("2020-01-01", format="%Y-%m-%d", yearfirst=True)
range_last_date = pd.to_datetime("2020-12-31", format="%Y-%m-%d", yearfirst=True)

KMS_TO_MILES = 1.60934
HOURS_TO_SECS = 3600.0

cols = ['unique_key', 'taxi_id', 'trip_start_timestamp', 'trip_end_timestamp', 
'trip_seconds', 'trip_miles', 'fare', 'trip_total', 'pickup_latitude', 'pickup_longitude']

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

def get_bounding_box(data, delta=0.005):
    bounding_box = {}
    bounding_box['lat_min'] = data['pickup_latitude'].min() - delta
    bounding_box['lat_max'] = data['pickup_latitude'].max() + delta
    bounding_box['long_min'] = data['pickup_longitude'].min() - delta
    bounding_box['long_max'] = data['pickup_longitude'].max() + delta
    return bounding_box
