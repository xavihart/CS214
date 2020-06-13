"""Capacited Vehicles Routing Problem (CVRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors

original_locations = \
    [(104.049, 30.641),  # start point
     (104.058, 30.650),
     (104.084, 30.650),
     (104.058, 30.678),
     (104.032, 30.650),
     (104.032, 30.678),
     (104.084, 30.678),
     (104.110, 30.650),
     (104.058, 30.621),
     (104.084, 30.621),
     (104.058, 30.707),
     (104.006, 30.678),
     (104.032, 30.707),
     (104.006, 30.650),
     (104.110, 30.678),
     (104.006, 30.621),
     (103.980, 30.650),
     (104.110, 30.707),
     (104.084, 30.593),
     (104.136, 30.678),
     (104.110, 30.593),
     (104.162, 30.678),
     (103.980, 30.678),
     (103.954, 30.650),
     (104.058, 30.763),
     (103.980, 30.707),
     (104.110, 30.735),
     (103.980, 30.735),
     (103.980, 30.593),
     (103.954, 30.707),
     (104.058, 30.565)
     ]
"""original_locations=\
    [(104.0494, 30.6412),
     (104.0584964,	30.65033414),
     (104.0844732,	30.65033414),
     (104.0584964,	30.67869848),
     (104.0325196,	30.65033414),
     (104.0325196,	30.67869848),
     (104.0844732,	30.67869848),
     (104.11045,	30.65033414),
     (104.0584964,	30.6219698),
     (104.0844732,	30.6219698),
     (104.0584964,	30.70706282),
     (104.0065428,	30.67869848),
     (104.0325196,	30.70706282),
     (104.0065428,	30.65033414),
     (104.11045,	30.67869848),
     (104.0065428,	30.6219698),
     (103.980566,	30.65033414),
     (104.11045,	30.70706282),
     (104.0844732,	30.59360546),
     (104.1364268,	30.67869848),
     (104.11045,	30.59360546),
     (104.1624036,	30.67869848),
     (103.980566,	30.67869848),
     (103.9545892,	30.65033414),
     (104.0584964,	30.7637915),
     (103.980566,	30.70706282),
     (104.11045,	30.73542716),
     (103.980566,	30.73542716),
     (103.980566,	30.59360546),
     (103.9545892,	30.70706282),
     (104.0584964,	30.56524112)
    ]"""
#original_demands = [0, 20,19,18,18,16,16,11,7,6,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3] #L=20
#original_demands=[0,25,24,22,21,18,18,12,7,6,4,4,4,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3] #L=25
#original_demands = [0, 30, 28, 26, 24, 21, 21, 13, 7, 7, 5, 5, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,3]  # L=30
#original_demands = [0, 100, 140, 78, 90, 156, 68, 154, 112, 152, 44, 20, 134, 184, 68, 130, 196, 24, 60, 156, 90, 180, 140, 134, 20,
                    #174, 180, 80, 100, 120, 28]
original_demands=[0,100,91,84,80,68,68,43,24,21,14,14,13,10,10,8,7,7,6,6,6,6,6,5,5,5,5,7,5,5,9]
_locations = []
_demands = []
_routes = {}


def haversin(theta):
    return np.sin(theta / 2) * np.sin(theta / 2)


def sphere_dis(long1, lat1, long2, lat2):
    long1_rad = long1 / 180 * np.pi
    lat1_rad = lat1 / 180 * np.pi
    long2_rad = long2 / 180 * np.pi
    lat2_rad = lat2 / 180 * np.pi

    tmp = haversin(lat1_rad - lat2_rad) + \
          np.cos(lat1_rad) * np.cos(lat2_rad) * haversin(long1_rad - long2_rad)

    return 100*2 * 6371 * np.arcsin(np.sqrt(tmp))


def init():
    _locations.append(original_locations[0])
    _demands.append(original_demands[0])
    for i in range(1, original_demands.__len__()):
        for j in range(original_demands[i]):
            _locations.append(original_locations[i])
            _demands.append(1)
    _routes['belongs_to_route'] = []
    _routes['from_set'] = []
    _routes['to_set'] = []
    _routes['drop_off'] = []
    _routes['route_distance'] = []
    _routes['route_passenger'] = []


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['num_visit'] = sum(_demands) + 1

    data['distance_matrix'] = {}
    for from_node in range(data['num_visit']):
        data['distance_matrix'][from_node] = {}
        for to_node in range(data['num_visit']):
            data['distance_matrix'][from_node][to_node] = sphere_dis(_locations[from_node][0], _locations[from_node][1],
                                                                     _locations[to_node][0], _locations[to_node][1])
            """abs(
                _locations[from_node][0] - _locations[to_node][0]) * 95.6 + abs(
                _locations[from_node][1] - _locations[to_node][1]) * 111"""
    data['demands'] = _demands
    # 0 is the start point
    # data['vehicle_capacities'] = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    # data['vehicle_capacities'] = [25, 25, 25, 25, 25, 25, 25, 25, 25]
    data['vehicle_capacities'] = []
    for i in range(0, 25):
        data['vehicle_capacities'].append(30)
    data['num_vehicles'] = 25  # 9 and 10
    data['depot'] = 0
    return data


from_set = []
to_set = []


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        # plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            next_node_index = manager.IndexToNode(solution.Value(routing.NextVar(index)))
            _routes['from_set'].append(node_index)
            _routes['to_set'].append(next_node_index)
            route_load += data['demands'][node_index]
            # plan_output += ' {0} Total_Drop_off({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        """plan_output += ' {0} Total_Drop_off({1})\n'.format(manager.IndexToNode(index),
                                                     route_load)

        plan_output += 'Distance of the route: {}km\n'.format(route_distance)
        plan_output += 'Passengers of the route: {}\n'.format(route_load)
        print(plan_output)"""
        _routes['route_distance'].append(round(route_distance/100,2))
        _routes['route_passenger'].append(route_load)
        _routes['belongs_to_route'].append(vehicle_id)
        total_distance += round(route_distance/100 ,2)
        total_load += route_load
    # print('Total distance of all routes: {}km'.format(total_distance))
    # print('Total passengers of all routes: {}'.format(total_load))
    global total_length
    total_length = round(total_distance,2)

    global total_pass
    total_pass = total_load


def execute_routes():
    partial_sum = []
    partial_sum.append(0)
    for i in range(1, original_demands.__len__()):
        partial_sum.append(partial_sum[i - 1] + original_demands[i])

    for i in range(_routes['from_set'].__len__()):
        if _routes['from_set'][i] == 0:
            _routes['from_set'][i] = 0
        else:
            for j in range(1, partial_sum.__len__()):
                if _routes['from_set'][i] > partial_sum[j - 1] and _routes['from_set'][i] <= partial_sum[j]:
                    _routes['from_set'][i] = j
                    break
                else:
                    continue

    for i in range(_routes['to_set'].__len__()):
        if _routes['to_set'][i] == 0:
            _routes['to_set'][i] = 0
        else:
            for j in range(1, partial_sum.__len__()):
                if _routes['to_set'][i] > partial_sum[j - 1] and _routes['to_set'][i] <= partial_sum[j]:
                    _routes['to_set'][i] = j
                    break
                else:
                    continue

    # prepare to print
    drop_off = 0
    j = 0
    for i in range(_routes['to_set'].__len__()):
        if _routes['from_set'][i] == 0:
            drop_off = 0
            output = 'Route for vehicle {}:\n'.format(_routes['belongs_to_route'][j])
            output += ' 0 Drop off(0) -> {}'.format(_routes['to_set'][i])
        if _routes['from_set'][i] != _routes['to_set'][i] and _routes['from_set'][i] != 0 and _routes['to_set'][
            i] != 0:  # new node
            output += ' Drop off({0}) -> {1}'.format(drop_off, _routes['to_set'][i])
            drop_off = 0
        if _routes['to_set'][i] == 0:
            if _routes['from_set'][i] != 0:
                output += ' Drop off({}) -> 0 Drop off(0)\n'.format(drop_off)
            else:
                output += ' Drop off(0)\n'
            output += 'Distance of the route: {}km\n'.format(_routes['route_distance'][j])
            output += 'Passengers of the route: {}\n'.format(_routes['route_passenger'][j])
            j += 1
            drop_off = 0
            print(output)
        drop_off += 1
    """_length=0
    for i in range (_routes['to_set'].__len__()-1):
        if _routes['from_set'][i]!=_routes['to_set'][i]:
            _length+=sphere_dis(original_locations[_routes['from_set'][i]][0], original_locations[_routes['from_set'][i]][1],
                             original_locations[_routes['to_set'][i]][0], original_locations[_routes['to_set'][i]][1])"""
    #print(_length)
    print('Total distance of all routes: {}km'.format(total_length))
    print('Total passengers of all routes: {}'.format(total_pass))


def main():
    """Solve the CVRP problem."""
    init()
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # set time limits for search
    search_parameters.time_limit.seconds = 600

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)

    execute_routes()

    print("\nSolver status: ", routing.status())

    from_set = _routes['from_set']
    to_set = _routes['to_set']
    # calculate fares and profits
    total_fares = 0
    for i in range(1, 31):
        total_fares = total_fares + np.ceil(
            sphere_dis(original_locations[i][0], original_locations[i][1], original_locations[0][0],
                       original_locations[0][1])/100 ) * 2 * \
                      original_demands[i]
    km_oil_price = 1.8
    cr_price = 220
    num_bus = _routes['belongs_to_route'].__len__()  # 9 and 10
    total_cost = km_oil_price * total_length + num_bus * cr_price
    net_profit = total_fares - total_cost
    print('\nTotal fares: {0}; Total cost: {1}; Net profit: {2}.'.format(int(total_fares), int(total_cost),
                                                                         int(net_profit)))

    # set colormap, the XKCD could be replaced with BASE, TABLEAU, etc
    colors = list(mcolors.XKCD_COLORS.keys())
    min_longitude = original_locations[0][0]
    for longitude in range(0, original_locations.__len__()):
        if original_locations[longitude][0] <= min_longitude:
            min_longitude = original_locations[longitude][0]
    min_latitude = original_locations[0][1]
    for latitude in range(0, original_locations.__len__()):
        if original_locations[latitude][1] <= min_latitude:
            min_latitude = original_locations[latitude][1]
    # create the graph
    G = nx.DiGraph()
    pos = {0: (104.049 - min_longitude, 30.641 - min_latitude),  # start point
           1: (104.058 - min_longitude, 30.650 - min_latitude),
           2: (104.084 - min_longitude, 30.650 - min_latitude),
           3: (104.058 - min_longitude, 30.678 - min_latitude),
           4: (104.032 - min_longitude, 30.650 - min_latitude),
           5: (104.032 - min_longitude, 30.678 - min_latitude),
           6: (104.084 - min_longitude, 30.678 - min_latitude),
           7: (104.110 - min_longitude, 30.650 - min_latitude),
           8: (104.058 - min_longitude, 30.621 - min_latitude),
           9: (104.084 - min_longitude, 30.621 - min_latitude),
           10: (104.058 - min_longitude, 30.707 - min_latitude),
           11: (104.006 - min_longitude, 30.678 - min_latitude),
           12: (104.032 - min_longitude, 30.707 - min_latitude),
           13: (104.006 - min_longitude, 30.650 - min_latitude),
           14: (104.110 - min_longitude, 30.678 - min_latitude),
           15: (104.006 - min_longitude, 30.621 - min_latitude),
           16: (103.980 - min_longitude, 30.650 - min_latitude),
           17: (104.110 - min_longitude, 30.707 - min_latitude),
           18: (104.084 - min_longitude, 30.593 - min_latitude),
           19: (104.136 - min_longitude, 30.678 - min_latitude),
           20: (104.110 - min_longitude, 30.593 - min_latitude),
           21: (104.162 - min_longitude, 30.678 - min_latitude),
           22: (103.980 - min_longitude, 30.678 - min_latitude),
           23: (103.954 - min_longitude, 30.650 - min_latitude),
           24: (104.058 - min_longitude, 30.763 - min_latitude),
           25: (103.980 - min_longitude, 30.707 - min_latitude),
           26: (104.110 - min_longitude, 30.735 - min_latitude),
           27: (103.980 - min_longitude, 30.735 - min_latitude),
           28: (103.980 - min_longitude, 30.593 - min_latitude),
           29: (103.954 - min_longitude, 30.707 - min_latitude),
           30: (104.058 - min_longitude, 30.565 - min_latitude)}
    # the number of edges
    num_edge = from_set.__len__()
    # add edges
    for i in range(num_edge):
        if from_set[i] != to_set[i]:
            G.add_edge(from_set[i], to_set[i])
    # add titles
    plt.title('Routes in Chengdu', fontsize=18, color='r', loc='center')
    plt.title("Total length: %skm\n Total passengers: %s" % (total_length, total_pass), fontsize=8, loc='right')
    # draw G
    nx.draw_networkx_nodes(G, pos=pos, node_size=120, node_color='#A0CBE2', with_labels=True)
    nx.draw_networkx_labels(G, pos=pos, font_size=8)
    j = 0
    for i in range(num_edge):
        if from_set[i] != to_set[i]:
            nx.draw_networkx_edges(G, pos=pos, edgelist=[(from_set[i], to_set[i])],
                                   connectionstyle='arc3,rad=0.2',
                                   arrowsize=5,
                                   edge_color=mcolors.XKCD_COLORS[colors[j]])
            if to_set[i] == 0:
                j = j + 1
    # add notations
    for p in range(0, 31):
        x = original_locations[p][0] - min_longitude
        y = original_locations[p][1] - min_latitude
        # plt.text(x-0.006, y + 0.004, '(%s,%s)' % (original_locations[p][0], original_locations[p][1]),fontsize=4.5)
        plt.text(x + 0.004, y - 0.005, '%s' % original_demands[p], fontsize=7)
    # save
    plt.savefig(fname="CVRP_chengdu_100_30.pdf", bbox_inches='tight', dpi=150)

    plt.show()

    """test_len = 0
    test = [[-1,3,12,21,28,26,24,10,4,3,-1],[-1,6,5,16,25,23,9,11,-1],[-1,6,18,20,13,5,-1], [-1,2,5,-1],[-1,4,2,-1] ,[-1,3,-1], [-1,1,-1] ,[-1,7, 8, 19, 17, 29,-1] ,[-1,0,-1],[-1,14,27,22,15,12,3,-1]];
    for i in range(10):
        for j in range(test[i].__len__() - 1):
            tmp = sphere_dis(original_locations[test[i][j] + 1][0], original_locations[test[i][j] + 1][1],
                             original_locations[test[i][j + 1] + 1][0], original_locations[test[i][j + 1] + 1][1])
            test_len += tmp
        print(round(test_len , 0))
    test_len = round(test_len , 0)
    print(test_len)"""


if __name__ == '__main__':
    main()
