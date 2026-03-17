def check_tool_access(depth, tool_dia):
    return "Risk" if depth/tool_dia > 4 else "OK"