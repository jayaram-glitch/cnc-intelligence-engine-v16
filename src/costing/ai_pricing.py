def predict_price(features, operations, cycle_time):

    # 🔹 MATERIAL COST (₹)
    material_rate_per_kg = 450
    estimated_weight = 1.5  # kg (placeholder)

    material_cost = material_rate_per_kg * estimated_weight

    # 🔹 MACHINING COST
    machine_hour_rate = 400  # ₹/hour
    machining_cost = (cycle_time / 60) * machine_hour_rate

    # 🔹 SETUP COST
    setup_cost = 1200

    total = material_cost + machining_cost + setup_cost

    return {
        "material_cost": round(material_cost, 2),
        "machining_cost": round(machining_cost, 2),
        "setup_cost": round(setup_cost, 2),
        "total_cost": round(total, 2)
    }