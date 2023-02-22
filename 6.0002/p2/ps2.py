# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer:
# The nodes are the buildings
# The edges are the possibilites of travel between two buildings
# the distances are represented as numbers stored in the WeightedEdge objects
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    if map_filename[-4:] != ".txt":
        map_filename += ".txt"
    map = Digraph()
    with open(map_filename, "r") as f:
        for line in f:
            l = line.rstrip("\n").split(" ")
            src = Node(l[0])
            dst = Node(l[1])
            if not map.has_node(src):
                map.add_node(src)
            if not map.has_node(dst):
                map.add_node(dst)
            map.add_edge(WeightedEdge(src, dst, int(l[2]), int(l[3])))
    print("Loading map from file...")
    return map

# Problem 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
# load_map("test_load_map")
#
# Problem 3: Finding the Shorest Path using Optimized Search Method
#
# Problem 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# Answer:
# The objective function is the sum of the total distances along a path connecting start to finish
# the constraint is the sum of the outdoor distances cannot exceed a certain value

# Problem 3b: Implement get_best_path

def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist, best_outdoor, best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        path: list composed of [[list of strings], int, int]
            Represents the current path of nodes being traversed. Contains
            a list of node names, total distance traveled, and total
            distance outdoors.
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path
        best_dist: int or float
            The smallest distance between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of strings
            The shortest path found so far between the original start
            and end node.

    Returns:
        A tuple with the shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k and the distance of that path.

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then return None.
    """
    if path[0] == []: path[0] = [start]
    if start == end: return path
    for edge in digraph.edges[Node(start)]:
        dest_node = edge.get_destination()
        distance = edge.get_total_distance() + path[1]
        outdoor = edge.get_outdoor_distance() + path[2]
        if distance > best_dist or outdoor > max_dist_outdoors:
            continue
        else:
            if dest_node.get_name() in path[0]:
                continue # avoids infinite loops
            update_path = [path[0] + [dest_node.get_name()], distance, outdoor]
            new_path = get_best_path(digraph, dest_node.get_name(), end,
                                    update_path, max_dist_outdoors,
                                    best_dist, best_outdoor, best_path)
            if new_path != None:
                best_path, best_dist, best_outdoor = new_path
    return (best_path, best_dist, best_outdoor)


# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    if Node(start) not in digraph.nodes or Node(end) not in digraph.nodes:
        raise ValueError("Nodes not in the graph")
    else:
        path, distance, outdoor = get_best_path(digraph, start, end, [[], 0, 0],
                                                max_dist_outdoors, float("inf"), float("inf"), None)
        if path == None:
            print(f"There is no path: path returned = {path}")
            raise ValueError("No path found.")

        if distance > max_total_dist:
            print(f"The distance required ({distance}m) > the allowed distance ({max_total_dist}m)")
            raise ValueError("Max total distance exceeded")

        if outdoor > max_dist_outdoors:
            print(f"The outdoors required ({outdoor}m) > The allowed outdoors ({max_dist_outdoors}m)")
            raise ValueError("Max outdoor distance exceeded")
    return path
# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

    def test_impossible_path2(self):
        self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
    unittest.main()

    # digraph = load_map("mit_map.txt")
    # # for edge in digraph.edges[Node("32")]:
    # #     print(edge)
    # melon = get_best_path(digraph, "32", "56", [[],0,0], 99999, float("inf"), float("inf"), None)
    # print(melon, "melon")

    # these tests below work
    # can mess with the max outside value
    # digraph = load_map("test_load_map.txt") 
    # melon = get_best_path(digraph, "1", "3", [[], 0, 0], 9, float("inf"), float("inf"), None)
    # print(melon, "melon")