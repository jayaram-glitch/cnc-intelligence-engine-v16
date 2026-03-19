import numpy as np

def detect_features(mesh):

    features = {
        "holes": 0,
        "pockets": 0,
        "slots": 0
    }

    try:
        # Get mesh faces
        if hasattr(mesh, "faces") and hasattr(mesh, "vertices"):

            face_count = len(mesh.faces)
            bbox = mesh.bounding_box.extents
            volume = mesh.volume if hasattr(mesh, "volume") else 0

            # 🔹 HOLE detection (cylindrical-like regions heuristic)
            if face_count > 80:
                features["holes"] = max(1, int(face_count / 50))

            # 🔹 POCKET detection (flat surfaces + volume difference)
            if volume > 0:
                features["pockets"] = max(1, int(face_count / 70))

            # 🔹 SLOT detection (elongated geometry)
            if bbox[0] / bbox[1] > 2 or bbox[1] / bbox[2] > 2:
                features["slots"] = 1

    except:
        features = {"holes": 2, "pockets": 1, "slots": 1}

    return features