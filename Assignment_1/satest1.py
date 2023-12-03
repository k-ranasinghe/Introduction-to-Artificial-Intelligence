import numpy as np
import random
import math

# read_inp() method is used to read from the input file
def read_inp(inp_file):
    map = []
    trucks = []
    with open(inp_file, 'r') as f:
        for line in f:
            if line.strip():
                if line.strip().startswith('truck'):
                    trucks.append(line.strip())
                else:
                    city_map = [float(x.strip()) if x.strip() != 'N' else np.inf for x in line.split(",")]
                    map.append(city_map)
    return map, trucks

# best_path() finds the path with the least distance
def best_path(map, capacity, start):
    paths = []
    visited = [False] * len(map)
    path = [start]
    visited[start] = True
    map_path_recursive(map, capacity, start, visited, path, paths, 0)
    best_path = simulated_annealing(paths)
    return best_path, calc_distance(map, best_path)

# this is a helper function for best_path() to find the optimum path recursively
def map_path_recursive(map, capacity, current_city, visited, path, paths, distance):
    if len(path) == capacity + 1:
        paths.append(path.copy())
        return
    for i in range(len(map)):
        if map[current_city][i] != np.inf and not visited[i]:
            visited[i] = True
            path.append(i)
            map_path_recursive(map, capacity, i, visited, path, paths, distance + map[current_city][i])
            visited[i] = False
            path.pop()

# method given below is used to calculate the distance of the chosen path
def calc_distance(map, path):
    distanc = 0
    for i in range(len(path) - 1):
        distanc += map[path[i]][path[i+1]]
    return distanc

# this implements the simutaed annealing algorithm into the code
def simulated_annealing(paths):
    curr_path = paths[0]
    curr_distance = calc_distance(map, curr_path)
    temparature = 1000
    cool_rate = 0.003
    while temparature > 1:
        i = random.randint(1, len(paths) - 1)
        new_path = paths[i]
        new_distance = calc_distance(map, new_path)
        if new_distance < curr_distance:
            curr_path = new_path
            curr_distance = new_distance
        else:
            delta = new_distance - curr_distance
            probability = math.exp(-delta / temparature)
            if random.random() < probability:
                curr_path = new_path
                curr_distance = new_distance
        temparature *= 1 - cool_rate
    return curr_path

if __name__ == "__main__":
    inp_file = "input.txt"
    outp_file = "210518H.txt"

    map, trucks = read_inp(inp_file)

    # Node Mapping with Map Values
    node_mapping = {i: chr(ord('a') + i) for i in range(len(map))}
    print("Node Maping:")
    for node, letter in node_mapping.items():
        print(f"{letter} : {', '.join(str(x) if x != np.inf else 'N' for x in map[node])}")

    # Truck Names and Capacities
    print("\nTrucks:")
    truck_paths = []
    for truck in trucks:
        truck_name, truck_capacity = truck.split('#')
        print(f"{truck_name}: Capacity {truck_capacity}")
        shortest_path, shortest_distance = best_path(map, int(truck_capacity), 0)
        truck_paths.append((truck_name, shortest_path, shortest_distance))
        print(f"Shortest Path for {truck_name}: {' -> '.join([node_mapping[i] for i in shortest_path])} ({shortest_distance})")
        print()

    # Write Output to File
    with open(outp_file, 'w') as f:
        for truck_name, shortest_path, shortest_distance in truck_paths:
            delivery_sequence = ','.join([node_mapping[i] for i in shortest_path[1:]])
            f.write(f"{truck_name}#{delivery_sequence}\n")
        total_distance = int(sum([shortest_distance for _, _, shortest_distance in truck_paths]))
        f.write(f"{total_distance}\n")