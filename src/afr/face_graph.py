import networkx as nx

def build_face_graph(shape):

    graph = nx.Graph()

    faces = shape.faces().vals()

    for i, face in enumerate(faces):
        graph.add_node(i, face=face)

    # simple adjacency assumption (can be improved)
    for i in range(len(faces)-1):
        graph.add_edge(i, i+1)

    return graph