def extract_topology(shape):

    faces = shape.faces().vals()

    topology = []

    for face in faces:

        topology.append({
            "type": face.SurfaceType()
        })

    return topology