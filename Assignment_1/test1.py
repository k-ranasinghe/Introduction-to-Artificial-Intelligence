import numpy as np

class Truck:
  def __init__(self, capacity, id):
    self.capacity = capacity
    self.id = id
    self.route = []

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

    def is_valid_solution(self, solution):
        visited_nodes = set()
        for truck_route in solution:
            for node in truck_route:
                if node in visited_nodes:
                    return False
                visited_nodes.add(node)
        return True

    def generate_neighbor(self, solution):
        neighbor = [route.copy() for route in solution]
        truck_index = np.random.randint(len(self.trucks))
        node_index = np.random.randint(len(neighbor[truck_index]))
        new_node = np.random.choice([node for node in range(1, len(self.city_map) + 1) if node not in neighbor[truck_index]])
        neighbor[truck_index][node_index] = new_node
        return neighbor

    def format_output(self, solution):
        formatted_routes = []
        for truck_index, route in enumerate(solution):
            route_nodes = [chr(ord('a') + node - 1) for node in route]  # Convert node indices to letters (assuming nodes start from 1)
            formatted_routes.append(f"truck_{truck_index + 1}#{','.join(route_nodes)}")
        total_distance = self.calculate_distance(solution)
        formatted_routes.append(str(total_distance))
        return formatted_routes

    def calculate_distance(self, solution):
        total_distance = 0
        for truck_route in solution:
            for i in range(len(truck_route) - 1):
                from_node = truck_route[i] - 1
                to_node = truck_route[i + 1] - 1
                total_distance += self.city_map[from_node][to_node]
        return total_distance

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


if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"

    with open(input_file, "r") as f:
        lines = f.readlines()
        city_map = [[float(x.strip()) if x.strip().isdigit() else float('inf') for x in line.split(",")] for line in lines[:len(lines) - 1]]
        trucks = [line.strip() for line in lines[len(lines) - 1:] if line.strip() and line.strip().startswith('truck')]
        trucks = [Truck(int(x.split("#")[1]), int(x.split("#")[0][6:])) for x in trucks]
    
    hill_climbing = HillClimbing(city_map, trucks)
    best_solution = hill_climbing.climb_hill()

    with open(output_file, "w") as f:
        for i, solution in enumerate(best_solution):
            f.write(f"truck_{i + 1}#{'->'.join([str(x) for x in solution])}\n")


