import pyarrow.parquet as pq

cols = ['unique_key', 'taxi_id', 'trip_start_timestamp', 'trip_end_timestamp', 
'trip_seconds', 'trip_miles', 'fare', 'trip_total', 'pickup_latitude', 'pickup_longitude']

def load_parquet(path, columns=cols):
    table = pq.read_table(path, columns=columns)
    return table.to_pandas()
