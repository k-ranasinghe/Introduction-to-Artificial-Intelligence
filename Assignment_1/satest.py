import numpy as np
import random
import math

def read_input(input_file):
    city_map = []
    trucks = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip():
                if line.strip().startswith('truck'):
                    trucks.append(line.strip())
                else:
                    row = [float(x.strip()) if x.strip() != 'N' else np.inf for x in line.split(",")]
                    city_map.append(row)
    return city_map, trucks

def traverse_map(city_map, capacity, start_city):
    paths = []
    visited = [False] * len(city_map)
    path = [start_city]
    visited[start_city] = True
    traverse_map_helper(city_map, capacity, start_city, visited, path, paths, 0)
    shortest_path = simulated_annealing(paths)
    return [(shortest_path, calculate_distance(city_map, shortest_path))]

def traverse_map_helper(city_map, capacity, current_city, visited, path, paths, distance):
    if len(path) == capacity + 1:
        paths.append(path.copy())
        return
    for i in range(len(city_map)):
        if city_map[current_city][i] != np.inf and not visited[i]:
            visited[i] = True
            path.append(i)
            traverse_map_helper(city_map, capacity, i, visited, path, paths, distance + city_map[current_city][i])
            visited[i] = False
            path.pop()

def calculate_distance(city_map, path):
    distance = 0
    for i in range(len(path) - 1):
        distance += city_map[path[i]][path[i+1]]
    return distance

def simulated_annealing(paths):
    current_path = random.choice(paths)
    current_distance = calculate_distance(city_map, current_path)
    temperature = 10
    cooling_rate = 0.1
    while temperature > 1:
        new_path = current_path.copy()
        i = random.randint(1, len(new_path) - 2)
        j = random.randint(1, len(new_path) - 2)
        new_path[i], new_path[j] = new_path[j], new_path[i]
        new_distance = calculate_distance(city_map, new_path)
        if new_distance < current_distance:
            current_path = new_path
            current_distance = new_distance
        else:
            delta = new_distance - current_distance
            probability = math.exp(-delta / temperature)
            if random.random() < probability:
                current_path = new_path
                current_distance = new_distance
        temperature *= 1 - cooling_rate
    return current_path

if __name__ == "__main__":
    input_file = "input.txt"

    city_map, trucks = read_input(input_file)

    # Node Mapping with City Map Values
    node_mapping = {i: chr(ord('A') + i) for i in range(len(city_map))}
    print("Node Mapping:")
    for node, letter in node_mapping.items():
        print(f"{letter} : {', '.join(str(x) if x != np.inf else 'N' for x in city_map[node])}")

    # Truck Names and Capacities
    print("\nTrucks:")
    for truck in trucks:
        truck_name, truck_capacity = truck.split('#')
        print(f"{truck_name}: Capacity {truck_capacity}")
        paths = traverse_map(city_map, int(truck_capacity), 0)
        shortest_path, shortest_distance = paths[0]
        print(f"Shortest Path for {truck_name}: {' -> '.join([node_mapping[i] for i in shortest_path])} ({shortest_distance})")
        print()