import numpy as np

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
    return [(p, d) for p, d in paths if len(p) == capacity + 1]

def traverse_map_helper(city_map, capacity, current_city, visited, path, paths, distance):
    if len(path) == capacity + 1:
        paths.append((path.copy(), distance))
        return
    for i in range(len(city_map)):
        if city_map[current_city][i] != np.inf and not visited[i]:
            visited[i] = True
            path.append(i)
            traverse_map_helper(city_map, capacity, i, visited, path, paths, distance + city_map[current_city][i])
            visited[i] = False
            path.pop()

def calculate_distance(path, city_map):
    distance = 0
    for i in range(len(path) - 1):
        distance += city_map[path[i]][path[i+1]]
    return distance

def main():
    input_file = "input.txt"

    city_map, trucks = read_input(input_file)

    # Node Mapping with City Map Values
    node_mapping = {i: chr(ord('A') + i) for i in range(len(city_map))}
    print("Node Mapping:")
    for node, letter in node_mapping.items():
        print(f"{letter} : {', '.join(str(x) if x != np.inf else 'N' for x in city_map[node])}")

    # Find Paths for Each Truck
    truck_paths = []
    list = []
    for truck in trucks:
        truck_name, truck_capacity = truck.split('#')
        print(f"\nPaths for {truck_name}:")
        paths = traverse_map(city_map, int(truck_capacity), 0)
        truck_path = []
        for path, distance in paths:
            truck_path.append(path)
            print(" -> ".join([node_mapping[i] for i in path]), f"({distance})")
            list.append((truck_name, path, distance))
        truck_paths.append(truck_path)

    # Find Combinations of Paths that Visit All Cities Exactly Once
    all_paths = []
    for i in range(len(truck_paths)):
        for j in range(i + 1, len(truck_paths)):
            for path1 in truck_paths[i]:
                for path2 in truck_paths[j]:
                    combined_path = path1 + path2
                    if len(set(combined_path)) == len(city_map):
                        all_paths.append(combined_path)

    # print(list)
    # Output Combinations of Paths that Visit All Cities Exactly Once
    print("\nCombinations of Paths that Visit All Cities Exactly Once:")
    for path in all_paths:
        path1, path2 = path[:len(city_map)//2+1], path[len(city_map)//2:]
        distance1 = calculate_distance(path1, city_map)
        distance2 = calculate_distance(path2, city_map)
        distance = distance1 + distance2
        path_str = " -> ".join([node_mapping[i] for i in path])
        print(f"{path_str} ({distance})")

if __name__ == "__main__":
    main()

