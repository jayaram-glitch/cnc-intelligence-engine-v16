def check_deep_pocket(depth, width):

    if width == 0:
        return "Invalid geometry"

    ratio = depth / width

    if ratio > 1:
        return "Deep pocket - high machining time"

    return "OK"