def plan_operations(features):

    ops = []

    if features.get("holes", 0) > 0:
        ops.append("Center Drilling")
        ops.append("Drilling")

    if features.get("pockets", 0) > 0:
        ops.append("Facing")
        ops.append("Pocket Milling")

    if features.get("slots", 0) > 0:
        ops.append("Slot Milling")

    # finishing
    if sum(features.values()) > 0:
        ops.append("Finishing")

    return ops