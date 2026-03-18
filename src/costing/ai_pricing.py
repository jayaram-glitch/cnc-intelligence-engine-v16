def predict_price(feature_count, operation_count):

    base = 20

    feature_cost = feature_count * 5

    operation_cost = operation_count * 8

    return base + feature_cost + operation_cost