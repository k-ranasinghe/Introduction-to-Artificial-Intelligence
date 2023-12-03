import numpy as np

class Truck:
    def __init__(self, capacity, id):
        self.capacity = capacity
        self.id = id

class HillClimbing:
    def __init__(self, city_map, trucks):
        self.city_map = city_map
        self.trucks = np.array(trucks)

    def hill_climbing(self):
        best_solution = []
        best_distance = float('inf')  # Set initial best distance to infinity
        
        def generate_random_solution():
            nodes = list(range(1, len(self.city_map) + 1))
            np.random.shuffle(nodes)
            solution = []
            for truck in self.trucks:
                truck_solution = nodes[:truck.capacity]
                nodes = nodes[truck.capacity:]
                solution.append(truck_solution)
            return solution

        def calculate_distance(solution):
            total_distance = 0
            for truck_route in solution:
                for i in range(len(truck_route) - 1):
                    from_node = truck_route[i] - 1
                    to_node = truck_route[i + 1] - 1
                    total_distance += self.city_map[from_node][to_node]
            return total_distance

        current_solution = generate_random_solution()
        current_distance = calculate_distance(current_solution)

        while True:
            # Your hill climb logic here
            # Implement neighbor generation and comparison to find the better solution
            # Update current_solution and current_distance accordingly
            # If no better solution is found, break the loop

            # Sample neighbor generation logic:
            # neighbor = generate_neighbor(current_solution)
            # neighbor_distance = calculate_distance(neighbor)
            # if neighbor_distance < current_distance:
            #     current_solution = neighbor
            #     current_distance = neighbor_distance
            # else:
            #     break

            # Break the loop for now (you need to implement the hill climb logic above)
            break

        return current_solution, current_distance

def read_input(input_file):
    city_map = []
    trucks = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip():
                if line.strip().startswith('truck'):
                    truck_info = line.strip().split('#')
                    truck_id = int(truck_info[0].split('_')[1])
                    truck_capacity = int(truck_info[1])
                    trucks.append(Truck(truck_capacity, truck_id))
                else:
                    row = [float(x.strip()) if x.strip() != 'N' else np.inf for x in line.split(",")]
                    city_map.append(row)
    return city_map, trucks


# ... (previous code remains unchanged)

if __name__ == "__main__":
    input_file = "input.txt"

    city_map, trucks = read_input(input_file)
    hill_climbing = HillClimbing(city_map, trucks)
    best_solution, best_distance = hill_climbing.hill_climbing()

    print("Optimized Routes:")
    for i, solution in enumerate(best_solution):
        truck_id = trucks[i].id
        route_str = ",".join([chr(ord('A') + node) for node in solution])  # Convert nodes to letters (A, B, C, ...)
        print(f"truck_{truck_id}#{route_str}")

    total_distance = sum([city_map[solution[i]][solution[i + 1]] for solution in best_solution for i in range(len(solution) - 1)])
    print(f"Total Distance: {total_distance}")

