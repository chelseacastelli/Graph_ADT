from graphs.graph import Graph, Vertex


class WeightedVertex(Vertex):

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {}  # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor by storing it in the neighbors dictionary.
        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (number): The weight of this edge.
        """
        if vertex_obj.get_id() in self.__neighbors_dict.keys():
            return  # it's already a neighbor

        self.__neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return [neighbor for (neighbor, weight) in self.__neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.__id} adjacent to {neighbor_ids}'


class WeightedGraph(Graph):
    INFINITY = float('inf')

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.
        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {}
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.

        Parameters:
        vertex_id (string): The unique identifier for the new vertex.
        Returns:
        Vertex: The new vertex object.
        """
        if vertex_id in self.__vertex_dict.keys():
            return False  # it's already there
        vertex_obj = WeightedVertex(vertex_id)
        self.__vertex_dict[vertex_id] = vertex_obj
        return True

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict.keys():
            return None
        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.
        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        weight (number): The edge weight.
        """
        all_ids = self.__vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.__is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)

    def get_vertices(self):
        """Return all the vertices in the graph"""
        return list(self.__vertex_dict.values())

    def get_edges(self):
        """Return all the edges in the graph"""
        return list()

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax:
        for vertex in graph"""
        return iter(self.__vertex_dict.values())

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root

    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if parent_map[vertex_id] == vertex_id:
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])

    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # Create a list of all edges in the graph, sort them by weight
        # from smallest to largest
        edges = []
        for vertex in self.get_vertices():
            # print(vertex.get_neighbors_with_weights())
            for neighbor, weight in vertex.get_neighbors_with_weights():
                edges.append((vertex.get_id(), neighbor.get_id(), weight))
        edges = sorted(edges, key=lambda x: x[2])

        # Create a dictionary `parent_map` to map vertex -> its "parent".
        # Initialize it so that each vertex is its own parent.
        parent_map = {x[0]: x[0] for x in edges}

        # Create an empty list to hold the solution (i.e. all edges in the final spanning tree)
        spanning_tree = []

        # While the spanning tree holds < V-1 edges,
        while len(spanning_tree) <= len(edges) - 1:
            # get the smallest edge.
            current = edges.pop(0)
            (vertex1, vertex2, weight) = current
            # If the two vertices connected by the edge are in different sets
            # (i.e. calling `find()` gets two different roots), then it will not create a cycle,
            if self.find(parent_map, vertex1) != self.find(parent_map, vertex2):
                # add it to the solution set and call `union()` on the two vertices.
                spanning_tree.append(current)
                self.union(parent_map, vertex1, vertex2)
            else:
                continue

        # Return the solution list.
        return spanning_tree

    def minimum_spanning_tree_prim(self):
        """
        Use Prim's Algorithm to return the total weight of all edges in the
        graph's spanning tree.
        Assume that the graph is connected.
        """
        total_mst_weight = 0
        # Create a dictionary `vertex_to_weight` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_weight = {x: float('inf') for x in self.get_vertices()}

        # Choose one vertex and set its weight to 0
        start_vertex = self.get_vertices()[0]
        vertex_to_weight[start_vertex] = 0

        # While `vertex_to_weight` is not empty:
        while vertex_to_weight:
            # Get the minimum-weighted remaining vertex,
            min_weighted_vertex = min(vertex_to_weight.items(), key=lambda x: x[1])
            # remove it from the dictionary, & add its weight to the total MST weight
            current_vertex = min_weighted_vertex[0]
            vertex_to_weight.pop(current_vertex, None)
            total_mst_weight += min_weighted_vertex[1]
            # 2. Update that vertex's neighbors, if edge weights are smaller than previous weights
            # print(min_weighted_vertex)
            try:
                for vertex in current_vertex.get_neighbors_with_weights():
                    neighbor, weight = vertex
                    if neighbor in vertex_to_weight and weight < vertex_to_weight[neighbor]:
                        vertex_to_weight[neighbor] = weight
                        # print(vertex_to_weight)
            except KeyError:
                continue

        # Return total weight of MST
        return total_mst_weight

    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight of the shortest path
        from a start vertex to a destination.
        """
        # Create a dictionary `vertex_to_distance` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`
        vertex_to_distance = {x: float('inf') for x in self.get_vertices()}
        start_vertex = self.get_vertex(start_id)
        vertex_to_distance[start_vertex] = 0

        # While `vertex_to_distance` is not empty:
        while vertex_to_distance:
            # Get the minimum-distance remaining vertex
            min_weighted_vertex = min(vertex_to_distance.items(), key=lambda x: x[1])
            # Remove it from the dictionary.
            vertex_to_distance.pop(min_weighted_vertex[0])

            # If it is the target vertex, return its distance.
            if min_weighted_vertex[0].get_id() == target_id:
                return min_weighted_vertex[1]

            # Update that vertex's neighbors by adding the edge weight to the
            #    vertex's distance, if it is lower than previous.
            try:
                for neighbor in min_weighted_vertex[0].get_neighbors_with_weights():
                    vertex, weight = neighbor
                    # if in dict and min weight + neighbor weight less than INF or etc
                    if vertex in vertex_to_distance and weight + min_weighted_vertex[1] < vertex_to_distance[vertex]:
                        # print(vertex, (weight + min_weighted_vertex[1]))
                        vertex_to_distance[vertex] = weight + min_weighted_vertex[1]
            except KeyError:
                continue

        # Return None if target vertex not found.
        return None

    def floyd_warshall(self):
        """
        Return the All-Pairs-Shortest-Paths dictionary, containing the shortest
        paths from each vertex to each other vertex.
        """
        # create a top-level dictionary to hold each vertex & map it to another
        # dictionary
        dist = dict()
        all_vertex_ids = self.__vertex_dict.keys()
        # set default values - either 0 (for v -> v) or infinity
        for vertex1 in all_vertex_ids:
            dist[vertex1] = dict()
            for vertex2 in all_vertex_ids:
                dist[vertex1][vertex2] = WeightedGraph.INFINITY
            dist[vertex1][vertex1] = 0
        # add all edge weights to the dictionary
        all_vertex_objs = self.get_vertices()
        for vertex in all_vertex_objs:
            neighbors_with_weights = vertex.get_neighbors_with_weights()
            for neighbor, weight in neighbors_with_weights:
                dist[vertex.get_id()][neighbor.get_id()] = weight
        # execute the algorithm - "relax" the distances using an intermediate vertex
        for k in all_vertex_ids:
            for i in all_vertex_ids:
                for j in all_vertex_ids:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist


if __name__ == "__main__":
    graph = WeightedGraph(is_directed=False)

    vertex_a = graph.add_vertex('A')
    vertex_b = graph.add_vertex('B')
    vertex_c = graph.add_vertex('C')
    vertex_c = graph.add_vertex('D')
    vertex_c = graph.add_vertex('E')
    vertex_c = graph.add_vertex('F')
    vertex_c = graph.add_vertex('G')
    vertex_c = graph.add_vertex('H')
    vertex_c = graph.add_vertex('J')

    graph.add_edge('A', 'B', 4)
    graph.add_edge('A', 'C', 8)
    graph.add_edge('B', 'C', 11)
    graph.add_edge('B', 'D', 8)
    graph.add_edge('C', 'F', 1)
    graph.add_edge('C', 'E', 4)
    graph.add_edge('D', 'E', 2)
    graph.add_edge('D', 'G', 7)
    graph.add_edge('D', 'H', 4)
    graph.add_edge('E', 'F', 6)
    graph.add_edge('F', 'H', 2)
    graph.add_edge('G', 'H', 14)
    graph.add_edge('G', 'J', 9)
    graph.add_edge('H', 'J', 10)

    print(graph.find_shortest_path('A', 'J'))