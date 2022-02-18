import json

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = "Hello, world"
    assert json.dumps(expected) == res.get_data(as_text=True)

def test_get_trips(app, client):
    res = client.get('/total_trips?start=2020-02-04&end=2020-02-05')
    assert res.status_code == 200

def test_average_fare_heatmap(app, client):
    res = client.get('/average_fare_heatmap?date=2020-02-05')
    assert res.status_code == 200

def test_average_speed_24hrs(app, client):
    res = client.get('/average_speed_24hrs?date=2020-02-06')
    assert res.status_code == 200
