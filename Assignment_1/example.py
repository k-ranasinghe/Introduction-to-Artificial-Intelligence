import random

def objective_function(x):
    # Example objective function: maximizing the negative of a quadratic function
    return -(x ** 2)

def generate_neighbors(x):
    # Generate neighbors by adding a random small value to x
    delta = random.uniform(-0.1, 0.1)
    return x + delta

def generate_random_initial_solution():
    # Generate a random initial solution between -10 and 10
    return random.uniform(-10, 10)

def random_restart_hill_climbing(f, generate_initial_solution, max_restarts):
    best_solution = None
    best_value = float("-inf")
    
    for _ in range(max_restarts):
        current_solution = generate_initial_solution()
        while True:
            neighbor = generate_neighbors(current_solution)
            if f(neighbor) > f(current_solution):
                current_solution = neighbor
                if f(current_solution) > best_value:
                    best_solution = current_solution
                    best_value = f(current_solution)
            else:
                break
    
    return best_solution

# Example usage
max_restarts = 10
best_solution = random_restart_hill_climbing(objective_function, generate_random_initial_solution, max_restarts)
print("Best Solution:", best_solution)
print("Best Value:", objective_function(best_solution))
