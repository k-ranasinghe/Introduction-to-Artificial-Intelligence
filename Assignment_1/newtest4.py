import numpy as np

class Truck:
    def __init__(self, capacity, id):
        self.capacity = capacity
        self.id = id

class HillClimbing:
    def __init__(self, city_map, trucks):
        self.city_map = city_map
        self.trucks = np.array(trucks)

    def generate_random_solution(self):
    	reachable_nodes = [i for i in range(1, len(self.city_map)) if self.city_map[0][i] != float('inf')]
    	solution = []
    	for truck in self.trucks:
        	truck_nodes = reachable_nodes[:min(truck.capacity, len(reachable_nodes))]
        	truck_solution = [0] + truck_nodes
        	solution.append(truck_solution)
        	reachable_nodes = [node for node in reachable_nodes if node not in truck_nodes]
    	return solution


    def hill_climbing(self):
        best_solution = self.generate_random_solution()

        while True:
            # Implement your hill climb logic here
            # Generate a neighbor solution and compare it with the current solution
            # Update best_solution if the neighbor solution is better
            # If no better solution is found, break the loop
            # Sample neighbor generation logic:
            # neighbor = self.generate_neighbor(best_solution)
            # neighbor_distance = self.calculate_distance(neighbor)
            # if neighbor_distance < self.calculate_distance(best_solution):
            #     best_solution = neighbor

            # Break the loop for now (you need to implement the hill climb logic above)
            break

        return best_solution

    # Implement other necessary methods here, such as generate_neighbor and calculate_distance



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

if __name__ == "__main__":
    input_file = "input.txt"

    city_map, trucks = read_input(input_file)
    hill_climbing = HillClimbing(city_map, trucks)
    best_solution = hill_climbing.generate_random_solution()

    print("Optimized Routes:")
    print(best_solution)
    for i, solution in enumerate(best_solution):
        truck_id = trucks[i].id
        route_str = ",".join([chr(ord('a') + node) for node in solution])  # Convert nodes to letters (a, b, c, ...)
        print(f"truck_{truck_id}#{route_str}")
