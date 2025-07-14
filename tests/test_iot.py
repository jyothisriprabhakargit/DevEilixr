from iot_emissions.mock_sensor import read_emission_data

def test_mock_sensor():
    value = read_emission_data()
    assert isinstance(value, int), "Sensor data should be integer"
    assert value >= 0, "Sensor reading can't be negative"
