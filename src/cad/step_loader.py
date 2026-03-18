import trimesh

def load_step(path):

    try:
        mesh = trimesh.load(path)
        return mesh

    except Exception as e:
        return {"error": str(e)}