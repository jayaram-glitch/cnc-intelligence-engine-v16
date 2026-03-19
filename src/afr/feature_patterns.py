def detect_features(shape):

    # fallback if mesh failed
    if isinstance(shape, dict):
        return {"holes": 1, "pockets": 1, "fillets": 0}

    features = {
        "holes": 0,
        "pockets": 0,
        "fillets": 0
    }

    try:
        # Try using mesh properties
        if hasattr(shape, "faces"):
            face_count = len(shape.faces)

            # Heuristic logic
            if face_count > 50:
                features["pockets"] += 1

            if face_count > 100:
                features["holes"] += 2

            if face_count > 150:
                features["fillets"] += 1

    except:
        # fallback values
        features = {"holes": 2, "pockets": 1, "fillets": 0}

    return features