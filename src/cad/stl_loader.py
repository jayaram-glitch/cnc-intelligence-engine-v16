import trimesh

def load_stl(path):

    mesh = trimesh.load(path)

    return mesh