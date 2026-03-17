def plan_operations(features):

    ops = []

    if features["pockets"] > 0:
        ops.append("rough pocket")
        ops.append("finish pocket")

    if features["holes"] > 0:
        ops.append("drilling")

    return ops