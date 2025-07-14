import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import os

# Example features: [temperature (°C), energy_consumed (kWh), machine_hours]
def train_model(X, y, model_path="ai_module/emission_model.pkl"):
    model = LinearRegression()
    model.fit(X, y)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print("✅ Model trained and saved to", model_path)


def predict_emission(features, model_path="ai_module/emission_model.pkl"):
    """Predicts CO2 emissions based on sensor features."""
    if not os.path.exists(model_path):
        raise FileNotFoundError("⚠️ ML model not found. Please train it first.")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    prediction = model.predict([features])[0]
    print(f"📈 Predicted Emissions for {features}: {prediction:.2f} kg")
    return prediction


# 🧪 Run training and prediction with dummy data
if __name__ == "__main__":
    # Dummy training dataset
    # Format: [temperature, energy_consumed (kWh), machine_hours]
    X_train = [
        [25, 50, 8],
        [30, 60, 9],
        [20, 40, 7],
        [28, 55, 8.5],
        [22, 45, 7.2],
        [26, 52, 8.1],
    ]
    y_train = [10.5, 12.3, 9.1, 11.8, 9.7, 10.9]  # Emissions in kg

    # Step 1: Train the model
    train_model(X_train, y_train)

    # Step 2: Predict emissions for new data
    test_features = [27, 58, 9]  # e.g., today's sensor reading
    predict_emission(test_features)
