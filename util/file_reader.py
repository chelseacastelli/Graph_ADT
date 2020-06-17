import sys
sys.path.append('../')

from graphs.graph import Graph


def read_graph_from_file(filename):
    """
    Read in data from the specified filename, and create and return a graph
    object corresponding to that data.

    Arguments:
    filename (string): The relative path of the file to be processed

    Returns:
    Graph: A directed or undirected Graph object containing the specified
    vertices and edges
    """

    # TODO: Use 'open' to open the file
    with open(filename, 'r', encoding='utf-8-sig') as f:
        # TODO: Use the first line (G or D) to determine whether graph is directed
        first = next(f).strip('\n')

        if first == 'D':
            graph = Graph(is_directed=True)
        elif first == 'G':
            graph = Graph(is_directed=False)
        else:
            raise ValueError('Invalid file format')

        # TODO: Use the second line to add the vertices to the graph
        for each in next(f).strip('\n').split(','):
            graph.add_vertex(each)

        # TODO: Use the 3rd+ line to add the edges to the graph
        for line in f:
            graph.add_edge(line[1], line[3])

        return graph



if __name__ == '__main__':

    graph = read_graph_from_file('test.txt')

    print(graph)