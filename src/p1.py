from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush
DEBUG = True;

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.


    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    print(adj(graph, initial_position))
    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    dummy_dic = {}
    return dummy_dic;
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.
    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.
    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    return_list = [];
    spaces = level["spaces"]
    walls = level["walls"]
    waypoints = level["waypoints"]
    sqrt2 = sqrt(2);
    for i in range(-1,2):
        for j in range(-1, 2):
            try:
                neighbor_cell = list();
                neighbor_cell.append(cell[0] + i);
                neighbor_cell.append(cell[1] + j);
                if (tuple(neighbor_cell)) in spaces.keys():
                    neighbor_weight = spaces[tuple(neighbor_cell)]
                elif tuple(neighbor_cell) in walls:
                    neighbor_weight = inf;
                elif tuple(neighbor_cell) in waypoints.keys():
                    neighbor_weight = 1;
                if abs(i+j)% 2 == 1:
                    neighbor_weight *= sqrt2;
                tple = (neighbor_cell), neighbor_weight
                return_list.append( tple)
            except IndexError:
                print("whoops out of bounds!")
    print(return_list)
    #print(list(level["walls"])[0:5]);               # (x,y) [(11, 11), (14, 4)]
    #print(list(level["spaces"].items())[0:5]);      # ((x,y), weight) [((1, 1), 3.0), ((2, 1), 2.0)]
    #print(list(level["waypoints"].items())[0:5]);   # (waypoint, (x,y)) [('b', (18, 2)), ('e', (8, 6))]



    pass


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = '../input/example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
