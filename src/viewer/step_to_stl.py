import cadquery as cq

def convert_step_to_stl(step_path, stl_path):

    shape = cq.importers.importStep(step_path)

    cq.exporters.export(shape, stl_path)