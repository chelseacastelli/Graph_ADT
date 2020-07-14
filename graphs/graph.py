from collections import deque
from random import choice


class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {}  # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.
        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """

        self.__neighbors_dict[vertex_obj.__id] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.
        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {}  # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.
        Returns:
        Vertex: The new vertex object.
        """
        vertex = Vertex(vertex_id)
        self.__vertex_dict[vertex_id] = vertex
        return vertex

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.
        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        if vertex_id1 not in self.__vertex_dict:
            self.add_vertex(vertex_id1)
        if vertex_id2 not in self.__vertex_dict:
            self.add_vertex(vertex_id2)

        # Add vertex_id2 as neighbor to vertex_id1 to make link/edge
        self.__vertex_dict[vertex_id1].add_neighbor(self.__vertex_dict[vertex_id2])

        if not self.__is_directed:
            self.__vertex_dict[vertex_id2].add_neighbor(self.__vertex_dict[vertex_id1])

    def get_vertices(self):
        """
        Return all vertices in the graph.
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return  # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.
        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.
        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id]  # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque()
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.popleft()  # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path:  # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for
        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        if not self.contains_id(start_id):
            raise KeyError("Vertex not found")

        # vertex keys we've seen before
        visited = set()
        # list of vertices that are the target_distance away from start vertex
        n_away_vertices = []

        # queue of vertices to visit next
        queue = deque()
        # add first item and its distance (0)
        queue.append((start_id, 0))
        visited.add(start_id)

        # do bfs
        while queue:
            # removes vertex_obj from queue and return it
            current_vertex_obj = queue.popleft()

            current_vertex_id = current_vertex_obj[0]
            vertex_distance = current_vertex_obj[1]

            # if distances match, add to n_away_vertices
            if vertex_distance == target_distance:
                n_away_vertices.append(current_vertex_id)

            # get neighbors of current vertex
            neighbors = self.get_vertex(current_vertex_id).get_neighbors()

            for neighbor in neighbors:
                # print(neighbor)
                if neighbor.get_id() not in visited:
                    queue.append((neighbor.get_id(), vertex_distance + 1))
                    visited.add(neighbor.get_id())

        return n_away_vertices

    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        queue = deque()
        visited = {}
        # visited = set()

        current_color = 0

        current_vertex_id = choice(list(self.__vertex_dict.keys()))

        queue.append(current_vertex_id)
        visited[current_vertex_id] = current_color
        # visited.add((current_vertex_id, current_color))

        while queue:
            # use bitwise operator to 'change color' (toggle 0 and 1)
            current_color ^= 1

            # grab next in queue
            current_vertex_id = queue.popleft()

            # get neighbors
            neighbors = self.get_vertex(current_vertex_id).get_neighbors()

            for neighbor in neighbors:
                # if not already visited,
                if neighbor.get_id() not in visited.keys():
                    # tag neighbor with alt color, add to visited
                    visited[neighbor.get_id()] = current_color

                    # add to queue
                    queue.append(neighbor.get_id())
                else:
                    # is neighbor same color as current vertex color?
                    if visited[current_vertex_id] == visited[neighbor.get_id()]:
                        return False

        return True

    def find_connected_components(self):
        """
        Return a list of all connected components, with each connected component represented as a list of vertex ids.
        """
        vertices = set(self.__vertex_dict.keys())

        components = []

        # while there are unvisited vertices
        while vertices:
            component = []
            queue = []

            start_id = vertices.pop()

            # add initial vertex to queue and component lists
            queue.append(start_id)
            component.append(start_id)

            # while queue is not empty
            while queue:
                # pop vertex in queue
                current_id = queue.pop()
                current_vertex = self.get_vertex(current_id)

                # get neighbors
                for neighbor in current_vertex.get_neighbors():
                    neighbor_id = neighbor.get_id()

                    # if neighbor unvisited, remove from vertices list
                    if neighbor_id in vertices:
                        vertices.remove(neighbor_id)

                    # if neighbor not already in component, add to queue for processing, add to component list
                    if neighbor_id not in component:
                        queue.append(neighbor_id)
                        component.append(neighbor_id)

            # add component group to components
            components.append(component)

        return components

    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """

        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # stack of vertices to visit next
        stack = deque()
        stack.append(self.get_vertex(start_id))

        # vertex keys we've seen before and their paths from the start vertex
        path_to_target = {
            start_id: [start_id]
        }

        # while stack is not empty
        while stack:
            current_vertex_obj = stack.pop()  # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in path_to_target:
                    stack.append(neighbor)
                    # print(vertex_id_to_path)

                    current_path = path_to_target[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    path_to_target[neighbor.get_id()] = next_path

        if target_id not in path_to_target:  # path not found
            return None

        return path_to_target[target_id]

    def dfs_traversal(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set()  # set of vertices we've visited so far

        def dfs_traversal_recursive(start_vertex):
            print(f'Visiting vertex {start_vertex.get_id()}')

            # recurse for each vertex in neighbors
            for neighbor in start_vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    visited.add(neighbor.get_id())
                    dfs_traversal_recursive(neighbor)
            return

        visited.add(start_id)
        start_vertex = self.get_vertex(start_id)
        dfs_traversal_recursive(start_vertex)

        return

    def contains_cycle(self):

        visited = set()
        stack = set()

        start_id = choice(list(self.__vertex_dict.keys()))

        def dfs_cycle_check(vertex):
            # print(f'Visiting vertex {start_vertex.get_id()}')

            # if it's already visited, it's been cleared for no cycle
            if vertex in visited:
                return False

            # else, add vertex to visited and to stack
            visited.add(vertex)
            stack.add(vertex)

            # recurse for each vertex in neighbors
            for neighbor in vertex.get_neighbors():
                # if neighbor is already in the stack or seen during the recurse, it's a cycle
                if neighbor in stack or dfs_cycle_check(neighbor):
                    return True
            # otherwise, no cycle, recurse done, pop from stack
            stack.remove(vertex)
            return False

        stack.add(start_id)
        start_vertex = self.get_vertex(start_id)

        if dfs_cycle_check(start_vertex):
            return True
        return False

        # An alternative: any() function returns True if any element of an iterable is True, returns False if any is False

        # return any(dfs_cycle_check(start_vertex) for start_vertex in self.__vertex_dict.values())

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph. If the graph contains a cycle, throw a ValueError.
        """

        stack = []
        visited = set()

        if self.contains_cycle():
            raise ValueError('Graph not DAG')

        def dfs_topo_sort(vertex):
            # print(f'Visiting vertex {vertex.get_id()}')
            visited.add(vertex.get_id())

            # recurse for each vertex in neighbors
            for neighbor in vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    dfs_topo_sort(neighbor)

            # On the way back up the recursion tree (that is, after visiting a vertex's neighbors), add the vertex to the stack.
            # print(f'Visited: {visited} \nAdding {vertex.get_id()} to stack {stack}')
            stack.append(vertex.get_id())

        # For each unvisited vertex, execute a DFS from that vertex.
        for vertex in list(self.__vertex_dict.values()):
            # print(vertex.get_id(), visited)
            if vertex.get_id() not in visited:
                dfs_topo_sort(vertex)

        # Reverse the contents of the stack and return it as a valid ordering.
        return stack[::-1]