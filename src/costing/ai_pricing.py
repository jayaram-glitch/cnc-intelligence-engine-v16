def predict_price(features_count, ops_count):

    base = 20

    feature_cost = features_count * 5

    operation_cost = ops_count * 8

    return base + feature_cost + operation_cost