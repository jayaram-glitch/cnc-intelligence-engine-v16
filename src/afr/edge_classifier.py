def classify_edge(edge):

    # Simplified logic

    try:
        if edge.is_convex():
            return "convex"
        elif edge.is_concave():
            return "concave"
    except:
        pass

    return "unknown"