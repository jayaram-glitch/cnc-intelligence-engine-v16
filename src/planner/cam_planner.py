def plan_operations(features):

    ops = []

    if features.get("pockets", 0) > 0:
        ops.append("rough pocket")
        ops.append("finish pocket")

    if features.get("holes", 0) > 0:
        ops.append("drilling")

    return ops