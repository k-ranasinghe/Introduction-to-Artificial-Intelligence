import numpy as np

def read_input(input_file):
    city_map = []
    trucks = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip():
                if line.strip().startswith('truck'):
                    trucks.append(line.strip())
                else:
                    row = [float(x.strip()) if x.strip() != 'N' else np.inf for x in line.split(",")]
                    city_map.append(row)
    return city_map, trucks

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
        print(f"{truck.split('#')[0]}: Capacity {truck.split('#')[1]}")




