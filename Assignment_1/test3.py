import numpy as np
from collections import deque

class Truck:
    def __init__(self, capacity, id):
        self.capacity = capacity
        self.id = id

class HillClimbingWithTabuSearch:
    def __init__(self, city_map, trucks):
        self.city_map = city_map
        self.trucks = np.array(trucks)
        self.best_solution = None
        self.best_distance = float('inf')
        self.tabu_list = deque(maxlen=10)  # Tabu list to store recent solutions

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
                total_distance += self.city_map[from_node][to_node]
        return total_distance

    def generate_neighbor(self, solution):
        neighbor = [route.copy() for route in solution]
        truck_index = np.random.randint(len(self.trucks))
        node_index = np.random.randint(self.trucks[truck_index].capacity)
        new_node = np.random.randint(1, len(self.city_map) + 1)
        while new_node in neighbor[truck_index]:
            new_node = np.random.randint(1, len(self.city_map) + 1)
        neighbor[truck_index][node_index] = new_node
        return neighbor

    def climb_hill_with_tabu_search(self):
        current_solution = self.generate_random_solution()
        current_distance = self.calculate_distance(current_solution)

        self.best_solution = current_solution
        self.best_distance = current_distance

        iterations_without_improvement = 0

        while iterations_without_improvement < 50:
            neighbor = self.generate_neighbor(current_solution)
            neighbor_distance = self.calculate_distance(neighbor)

            if neighbor_distance < self.best_distance and neighbor not in self.tabu_list:
                self.best_solution = neighbor
                self.best_distance = neighbor_distance
                current_solution = neighbor
                iterations_without_improvement = 0
            else:
                iterations_without_improvement += 1

            # Add the current solution to the tabu list
            self.tabu_list.append(current_solution)

        return self.best_solution

def read_input(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
        city_map = [[float(x.strip()) if x.strip().isdigit() else np.inf for x in line.split(",")] for line in lines[:len(lines) - 1]]
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
    hill_climbing = HillClimbingWithTabuSearch(city_map, trucks)
    best_solution = hill_climbing.climb_hill_with_tabu_search()
    best_distance = hill_climbing.calculate_distance(best_solution)

    write_output(output_file, best_solution, best_distance)
