import cadquery as cq

def load_iges(path):

    try:
        shape = cq.importers.importStep(path)
        return shape
    except:
        return None