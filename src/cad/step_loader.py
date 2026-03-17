import cadquery as cq

def load_step(path):
    return cq.importers.importStep(path)