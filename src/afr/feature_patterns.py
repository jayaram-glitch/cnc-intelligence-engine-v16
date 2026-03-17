def detect_features(shape):

    faces = shape.faces().vals()

    features = {
        "holes": 0,
        "pockets": 0,
        "fillets": 0
    }

    for face in faces:

        surf = face.SurfaceType()

        if surf == "CYLINDER":
            features["holes"] += 1

        elif surf == "PLANE":
            features["pockets"] += 1

        else:
            features["fillets"] += 1

    return features