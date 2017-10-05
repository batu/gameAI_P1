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
    # create heap to store pending cells
    pending_heap = []
    # create list to store visited cells
    prev_visited = []
    
    
    # establish start of path such that:
    # cell = tuple(distance from start, coordinate, state (v for visited, uv for unvisited), parent coordinate)
    source_cell = [0, initial_position, "uv", None]
    if (DEBUG == True):
        print("Source Cell: ")
        print(source_cell)
        #heappush(pending_heap, (2.0, (2, 9), "uv", "not_discovered"))
    
    heappush(pending_heap, source_cell)
    
    while pending_heap:
        curr_cell = heappop(pending_heap)
        if curr_cell[1] == destination:
            # need to calculate path and return it here
            if (DEBUG == True):
                print("Success! Path found! Distance: ")
                print(curr_cell[0])
                #print("Prev visited: ")
                #print(prev_visited)
                return
        else:
            neighboor_list = adj(graph, curr_cell[1]) # pass coordinates of current cell to navigation edges, to find all neighboors
            for adj_cell in neighboor_list:
                
                # check if prev visited or wall
                if any(i[1] == adj_cell[1] for i in prev_visited) or (adj_cell[0] == inf): continue 
                    
                adj_cell[0] = adj_cell[0] + curr_cell[0] # add current distance to neighboor distances for comparison
                
                #check if cell already in heap
                prev_queued = next((x for x in pending_heap if x[1] == adj_cell[1]), None)
                if prev_queued: 
                    # if true, compare distances. If new path yields shorter distance, update
                    if prev_queued[0] > adj_cell[0]:
                        prev_queued[0] = adj_cell[0]
                        prev_queued[3] = curr_cell[1]
                        
                else: # not already in heap, so we need to add it
                    adj_cell[3] = curr_cell[1] # set current cell as parent
                    heappush(pending_heap, adj_cell)
                    
        # finally, mark current cell as visited and add to prev_visited
        curr_cell[2] = "v"
        prev_visited.append(curr_cell)
        
        
    #print(adj(graph, initial_position))
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
                if i == 0 and j == 0: continue
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
                tple = list((neighbor_weight, tuple(neighbor_cell), "uv", "not_discovered"))
                return_list.append( tple)
            except IndexError:
                print("whoops out of bounds!")
                
    if (DEBUG == True):
        print("Returning return_list from nav_edges: ")
    
    return(return_list)
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
    filename, src_waypoint, dst_waypoint = '../input/example.txt', 'a','z'
    
    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
