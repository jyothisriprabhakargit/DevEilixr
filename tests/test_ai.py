from ai_module.emissions_predictor import predict_emissions
from ai_module.optimize_credits import recommend_offset

def test_prediction():
    data = {"temperature": 30, "machine_hours": 6}
    prediction = predict_emissions(data)
    assert prediction > 0, "Prediction must be positive"

def test_optimization():
    recommendation = recommend_offset(emission_level=80, current_credits=20)
    assert recommendation > 0, "Must recommend credit top-up"
