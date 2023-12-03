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

def simulated_annealing(city_map, start_city):
    # Initialize variables
    current_path = list(range(len(city_map)))
    current_distance = 0
    temperature = 1000
    cooling_rate = 0.003
    best_path = current_path.copy()
    best_distance = current_distance

    # Loop until temperature is too low
    while temperature > 1:
        # Generate a new path by swapping two cities
        new_path = current_path.copy()
        i = random.randint(1, len(city_map) - 1)
        j = random.randint(1, len(city_map) - 1)
        new_path[i], new_path[j] = new_path[j], new_path[i]

        # Calculate the new distance
        new_distance = 0
        for k in range(len(new_path) - 1):
            new_distance += city_map[new_path[k]][new_path[k+1]]

        # Calculate the acceptance probability
        delta_distance = new_distance - current_distance
        acceptance_probability = math.exp(-delta_distance / temperature)

        # Decide whether to accept the new path
        if delta_distance < 0 or random.random() < acceptance_probability:
            current_path = new_path
            current_distance = new_distance

        # Update the best path if necessary
        if current_distance < best_distance:
            best_path = current_path.copy()
            best_distance = current_distance

        # Cool the temperature
        temperature *= 1 - cooling_rate

    return best_path

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
    total_distance = 0
    for truck in trucks:
        truck_name, truck_capacity = truck.split('#')
        print(f"{truck_name}: Capacity {truck_capacity}")
        best_path = simulated_annealing(city_map, 0)[:int(truck_capacity)+1]
        distance = 0
        for i in range(len(best_path) - 1):
            distance += city_map[best_path[i]][best_path[i+1]]
        total_distance += distance
        print(f"Best path for {truck_name}: {' -> '.join([node_mapping[i] for i in best_path])}")
        print(f"Distance travelled by {truck_name}: {distance}")
        print()
    print(f"Total distance travelled by all trucks: {total_distance}")