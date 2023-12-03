import numpy as np

class Truck:
    def __init__(self, capacity, id):
        self.capacity = capacity
        self.id = id

class HillClimbing:
    def __init__(self, city_map, trucks):
        self.city_map = city_map
        self.trucks = np.array(trucks)
        self.best_solution = None
        self.best_distance = None

    def generate_random_solution(self):
        nodes = list(range(1, len(self.city_map) + 1))
        np.random.shuffle(nodes)
        solution = []
        for truck in self.trucks:
            truck_solution = nodes[:truck.capacity]
            nodes = nodes[truck.capacity:]
            solution.append(truck_solution)
        return solution

    def calculate_distance(self, solution):
        total_distance = 0
        for truck_route in solution:
            for i in range(len(truck_route) - 1):
                from_node = truck_route[i] - 1
                to_node = truck_route[i + 1] - 1
                if from_node < len(self.city_map) and to_node < len(self.city_map[from_node]):
                    if self.city_map[from_node][to_node] != 'N':
                        total_distance += self.city_map[from_node][to_node]
                    else:
                        return float('inf')  # Return infinity for invalid routes
                else:
                    return float('inf')  # Return infinity if indices are out of range
        return total_distance

    def is_valid_solution(self, solution):
        visited_nodes = set()
        for truck_route in solution:
            for node in truck_route:
                if node in visited_nodes:
                    return False
                visited_nodes.add(node)
        return True

    def climb_hill(self):
        current_solution = self.generate_random_solution()
        current_distance = self.calculate_distance(current_solution)

        self.best_solution = current_solution
        self.best_distance = current_distance

        while True:
            neighbor = self.generate_neighbor(current_solution)
            neighbor_distance = self.calculate_distance(neighbor)

            if neighbor_distance < self.best_distance and self.is_valid_solution(neighbor):
                self.best_solution = neighbor
                self.best_distance = neighbor_distance
                current_solution = neighbor
            else:
                break

        return self.best_solution

    def generate_neighbor(self, solution):
        neighbor = [route.copy() for route in solution]
        truck_index = np.random.randint(len(self.trucks))
        node_index = np.random.randint(len(neighbor[truck_index]))
        available_nodes = [node for node in range(1, len(self.city_map) + 1) if node not in neighbor[truck_index]]
        new_node = np.random.choice(available_nodes)
        neighbor[truck_index][node_index] = new_node
        return neighbor

def read_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
        city_map = [[float(x.strip()) if x.strip().isdigit() else 'N' for x in line.split(",")] for line in lines[:len(lines) - 1]]
        trucks = [line.strip() for line in lines[len(lines) - 1:] if line.strip() and line.strip().startswith('truck')]
        trucks = [Truck(int(x.split("#")[1]), int(x.split("#")[0][6:])) for x in trucks]
    return city_map, trucks

def write_output(output_file, best_solution, best_distance):
    with open(output_file, "w") as f:
        for i, solution in enumerate(best_solution):
            route_str = ",".join([chr(ord('a') + node - 1) for node in solution])
            f.write(f"truck_{i + 1}#{route_str}\n")
        f.write(str(best_distance))

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"

    city_map, trucks = read_input(input_file)
    hill_climbing = HillClimbing(city_map, trucks)
    best_solution = hill_climbing.climb_hill()
    best_distance = hill_climbing.calculate_distance(best_solution)

    write_output(output_file, best_solution, best_distance)
