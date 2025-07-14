def optimize_credit_offset(emission, available_credits, credit_price_per_kg=1.0):
    """
    Determines optimal offset action.
    - emission: Current emission in kg
    - available_credits: Credits already owned
    - credit_price_per_kg: Price per kg credit

    Returns dict with action plan.
    """
    if available_credits >= emission:
        return {
            "action": "offset_now",
            "needed_credits": 0,
            "estimated_cost": 0
        }
    else:
        deficit = emission - available_credits
        cost = deficit * credit_price_per_kg
        return {
            "action": "purchase",
            "needed_credits": deficit,
            "estimated_cost": cost
        }

if __name__ == "__main__":
    current_emission = 15.0  # in kg
    my_credits = 10.0        # in kg
    credit_price = 2.0       # ₹2 per kg

    result = optimize_credit_offset(current_emission, my_credits, credit_price)
    print("🧠 Optimization Result:", result)
