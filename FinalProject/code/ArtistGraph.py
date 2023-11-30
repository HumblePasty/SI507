import networkx as nx

class ArtistGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_artist(self, artist):
        """ Add an artist to the graph. """
        self.graph.add_node(artist, attr_dict=artist.__dict__)

    def add_connection(self, artist1, artist2):
        """ Add a connection between two artists. """
        self.graph.add_edge(artist1, artist2)

    def remove_artist(self, artist):
        """ Remove an artist from the graph. """
        self.graph.remove_node(artist)

    def remove_connection(self, artist1, artist2):
        """ Remove a connection between two artists. """
        self.graph.remove_edge(artist1, artist2)

    def compute_centrality(self):
        """ Compute and return centrality measures of the graph. """
        return nx.degree_centrality(self.graph)

    def detect_communities(self):
        """ Detect and return communities in the graph. """
        return nx.community.greedy_modularity_communities(self.graph)

    # TBD: Add more methods as needed.
