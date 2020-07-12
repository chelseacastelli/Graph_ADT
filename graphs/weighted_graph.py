from graphs.graph import Graph, Vertex

class WeightedVertex(Vertex):
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors.

        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor along a weighted edge by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (int): The edge weight from self -> neighbor.
        """
        # TODO: Implement this function.
        if vertex_obj.get_id() in self.__neighbors_dict.keys():
            return  # it's already a neighbor

        self.__neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex as a list of neighbor ids."""
        # TODO: Implement this function.
        return [neighbor for (neighbor, weight) in self.__neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex as a list of tuples of (neighbor_id, weight)."""
        # TODO: Implement this function.
        return list(self.__neighbors_dict.values())


class WeightedGraph(Graph):
    def __init__(self, is_directed=True):
        """
        Initialize a weighted graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {} # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        # TODO: Implement this function.
        if vertex_id in self.__vertex_dict.keys():
            return False  # it's already there
        vertex_obj = WeightedVertex(vertex_id)
        self.__vertex_dict[vertex_id] = vertex_obj
        return True


def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        # TODO: Implement this function.
        all_ids = self.__vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.__is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)
