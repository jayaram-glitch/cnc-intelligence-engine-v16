def apply_rules(topology):

    features = []

    for face in topology:

        if face["type"] == "CYLINDER":
            features.append("hole")

        elif face["type"] == "PLANE":
            features.append("pocket")

    return features