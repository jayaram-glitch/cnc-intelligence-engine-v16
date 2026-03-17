import ezdxf

def read_dxf(file):

    doc = ezdxf.readfile(file)

    msp = doc.modelspace()

    return [e.dxftype() for e in msp]