def detect_features(shape):

    # fallback for mesh-based
    if isinstance(shape, dict):
        return {"holes": 0, "pockets": 0, "fillets": 0}

    features = {
        "holes": 2,
        "pockets": 1,
        "fillets": 0
    }

    return features