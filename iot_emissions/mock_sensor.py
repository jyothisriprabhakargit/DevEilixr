import random
from datetime import datetime

def read_emission_data():
    """Simulates real-time CO2 emission data from a sensor (in kg)."""
    simulated_value = round(random.uniform(10.0, 100.0), 2)
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] Emission Reading: {simulated_value} kg")
    return simulated_value
