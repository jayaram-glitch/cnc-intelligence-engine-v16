def check_deep_pocket(depth, width):

    if width == 0:
        return "Invalid"

    return "Deep pocket" if depth > width else "OK"