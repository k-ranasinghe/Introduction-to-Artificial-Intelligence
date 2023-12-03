import random

def read_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        city_map = [[float('inf') if val == 'N' else int(val) for val in line.strip().split(',')] for line in lines[:len(lines)-1]]
        trucks_info = [line.strip() for line in lines[len(city_map):] if line.strip().startswith('truck')]
        return city_map, trucks_info


def calculate_distance(route, city_map):
    distance = 0
    for i in range(len(route) - 1):
        start_node = route[i]
        end_node = route[i + 1]
        if city_map[start_node][end_node] == 'N':
            return float('inf')
        distance += city_map[start_node][end_node]
    return distance

def hill_climbing(city_map, truck_capacity):
    nodes = list(range(len(city_map)))
    delivery_sequences = []
    for _ in range(truck_capacity):
        random.shuffle(nodes)
        current_route = nodes.copy()
        current_distance = calculate_distance(current_route, city_map)
        while True:
            neighbor_route = current_route.copy()
            i, j = sorted(random.sample(range(1, len(nodes) - 1), 2))
            neighbor_route[i:j+1] = reversed(neighbor_route[i:j+1])
            neighbor_distance = calculate_distance(neighbor_route, city_map)
            if neighbor_distance >= current_distance:
                break
            current_route, current_distance = neighbor_route, neighbor_distance
        delivery_sequences.append(current_route[1:])  # Exclude starting node 'a'
    return delivery_sequences

def main(input_file, output_file):
    city_map, trucks_info = read_input(input_file)
    output_lines = []
    total_distance = 0
    for truck_info in trucks_info:
        truck_number, capacity = truck_info.split('#')
        capacity = int(capacity)
        delivery_sequences = hill_climbing(city_map, capacity)
        for sequence in delivery_sequences:
            total_distance += calculate_distance(['a'] + sequence + ['a'], city_map)
            output_lines.append(f"{truck_number}#{','.join([chr(97 + node) for node in sequence])}")
    output_lines.append(str(total_distance))
    with open(output_file, 'w') as file:
        file.write('\n'.join(output_lines))

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "210518H.txt"  # Replace with your actual index number
    main(input_file, output_file)
