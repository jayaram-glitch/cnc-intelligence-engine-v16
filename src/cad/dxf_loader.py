import ezdxf

def load_dxf(path):

    doc = ezdxf.readfile(path)

    msp = doc.modelspace()

    entities = []

    for e in msp:
        entities.append(e.dxftype())

    return entities