import collections


class Actor:
    def __init__(self):
        """
        Constructor for Actor class
            name: name of the actor
            movies: list of movies the actor has been in
            dist: distance from the source actor
            prev: previous actor in the path
        """
        self.name = ""
        self.movies = []
        self.dist = 0
        self.prev = None

    def __str__(self):
        return self.name


class Movie:
    def __init__(self):
        """
        Constructor for Movie class
            name: name of the movie
            actors: list of actors in the movie
        """
        self.name = ""
        self.actors = []

    def __str__(self):
        return self.name


def read_file(filename):
    """
    Reads the file and creates a dictionary of actors and movies
    :param filename: name of the file
    :return: dictionary of actors and movies
    """
    actors = {}
    movies = {}

    with open(filename, 'rb') as f:
        for line in f:
            line = line.strip()
            line = line.decode('latin-1')
            line = line.split('/')
            movie = line[0]
            actors_in_movie = line[1:]
            if movie not in movies:
                movies[movie] = Movie()
                movies[movie].name = movie
            for actor in actors_in_movie:
                if actor not in actors:
                    actors[actor] = Actor()
                    actors[actor].name = actor
                actors[actor].movies.append(movie)
                movies[movie].actors.append(actor)

    return actors, movies


# STEP 1: reading the files
ActionActors, ActionMovies = read_file("BaconData\ActionCast.txt")
BaconActors06, BaconMovies06 = read_file("BaconData\Bacon_06.txt")
BaconActors00_06, BaconMovies00_06 = read_file("BaconData\BaconCast_00_06.txt")

BaconFullActors, BaconFullMovies = read_file("BaconData\BaconCastFull.txt")

PopularActors, PopularMovies = read_file("BaconData\PopularCast.txt")

# cache the results
import pickle


with open('BaconFullActors.pickle', 'wb') as f:
    pickle.dump(BaconFullActors, f)
with open('BaconFullMovies.pickle', 'wb') as f:
    pickle.dump(BaconFullMovies, f)

# load the results
with open('BaconFullActors.pickle', 'rb') as f:
    BaconFullActors = pickle.load(f)
with open('BaconFullMovies.pickle', 'rb') as f:
    BaconFullMovies = pickle.load(f)


# STEP 2: class definitions
class Vertex:
    def __init__(self, value):
        self.id = value
        self.connectedTo = {}  # {nbr: weight}
        self.degree = 0

    def addNeighbor(self, nbr_id, weight=0):
        self.connectedTo[nbr_id] = weight
        self.degree += 1

    def getId(self):
        return self.id

    def calculateDegree(self):
        self.degree = len(self.connectedTo.keys())
        return self.degree

    def __str__(self):
        return str(self.id) + ' is connected to: ' + str([x.id for x in self.connectedTo.keys()])


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        # self.numEdges = 0

    def addVertex(self, key) -> Vertex:
        self.numVertices += 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, key):
        if key in self.vertList:
            return self.vertList[key]
        else:
            return None

    def addEdge(self, f: Vertex, t: Vertex, weight=0):
        if f not in self.vertList:
            self.addVertex(f)
        if t not in self.vertList:
            self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t].id, weight)
        self.vertList[t].addNeighbor(self.vertList[f].id, weight)
        # self.numEdges += 1


# STEP 3: Create a graph object to store the relationships between actors
def create_graph(actors, movies):
    """
    Creates a graph object to store the relationships between actors

    :param actors: dictionary of actors
    :param movies: dictionary of movies
    :return: graph object
    """
    graph = Graph()
    for actor in actors:
        if actor not in graph.vertList:
            graph.addVertex(actor)
            for movie in actors[actor].movies:
                for co_actor in movies[movie].actors:
                    if co_actor != actor:
                        # record the relationship between the actor and the co-actor with the movie name as the weight
                        graph.addEdge(actor, co_actor, movies[movie].name)
    return graph


BaconGraph = create_graph(BaconFullActors, BaconFullMovies)
# cache the graph
with open('BaconGraph.pickle', 'wb') as f:
    pickle.dump(BaconGraph, f)
# load the graph from the cache
with open('BaconGraph.pickle', 'rb') as f:
    BaconGraph = pickle.load(f)


# STEP 4: Breadth-first search algorithm to find the shortest paths from a given vertex to all other vertices in the graph
def BFS(graph, start_vertex):
    """
    Breadth-first search algorithm to find the shortest paths from a given vertex to all other vertices in the graph

    :param graph: the graph to search
    :param start_vertex: the vertex to start the search from, in this case, the source actor (Kevin Bacon)
    :param distances: the dictionary to store the distances from the source actor to all other actors (Bacon Numbers)
    :param shortest_paths: the dictionary to store the shortest paths from the source actor to all other actors
    :param num_shortest_paths: the list of numbers of shortest paths from the source actor to all other actors
    """
    discovered = {}
    distances = {}
    shortest_paths = {}
    num_shortest_paths = {}

    for vert in graph.vertList:
        # prepare the dictionaries
        discovered[vert] = False
        distances[vert] = -1
        shortest_paths[vert] = []
        num_shortest_paths[vert] = 0

    distances[start_vertex] = 0
    num_shortest_paths[start_vertex] = 1

    q = collections.deque()
    discovered[start_vertex] = True
    q.append(start_vertex)

    while q:
        current_vertex = q.popleft()
        for neighbor in graph.vertList[current_vertex].connectedTo:
            if not discovered[neighbor]:
                discovered[neighbor] = True
                q.append(neighbor)

                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current_vertex] + 1

                if distances[neighbor] == distances[current_vertex] + 1:
                    shortest_paths[neighbor] = [current_vertex] + shortest_paths[current_vertex]
                    num_shortest_paths[neighbor] += num_shortest_paths[current_vertex]

    return distances, shortest_paths, num_shortest_paths


# BFS(BaconGraph, 'Kevin Bacon')
distances, shortest_paths, num_shortest_paths = BFS(BaconGraph, 'Bacon, Kevin')


# STEP 5: function to fing the Bacon Number of a given actor and print the shortest paths
def find_bacon(actor):
    """
    Finds the Bacon Number of a given actor and prints the shortest paths

    :param actor: the actor to find the Bacon Number of
    """
    if actor not in BaconGraph.vertList:
        print("Actor not in the graph.")
    else:
        print("Bacon Number:", distances[actor])
        print("Number of shortest paths:", num_shortest_paths[actor])
        print("One of the shortest paths:")
        for n, path in zip(range(len(shortest_paths[actor])), shortest_paths[actor]):
            if path == 'Bacon, Kevin':
                print('Bacon Kevin', end=' ')
                continue
            print(path, end=' ')
            print('--', end=' ')
            print(BaconGraph.vertList[path].connectedTo[shortest_paths[actor][n+1]], end=' ')
            print('->', end=' ')


find_bacon('Nordquist, Scott')


# STEP 6: function to calculate the average Bacon Number of all actors in the graph
def average_bacon():
    """
    Calculates the average Bacon Number of all actors in the graph
    """
    sum = 0
    for actor in BaconGraph.vertList:
        sum += distances[actor]
    print("Average Bacon Number:", sum / len(BaconGraph.vertList))

average_bacon()
