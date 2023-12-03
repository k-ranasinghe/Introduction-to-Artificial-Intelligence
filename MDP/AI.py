import copy

def direction(direction):
    if direction == 0:
        d = 'North'
    elif direction == 1:
        d = 'East'
    elif direction == 2:
        d = 'South'
    elif direction == 3:
        d = 'West'
    elif direction == 4:
        d = 'Nothing'
    else:
        d = '-'
    return d

def prevUtil(direction, current, states):
    if direction == 0:
        if current + 3 < len(states):
            u = states[current + 3][7]
        else:
            u = states[current][7]

    elif direction == 1:
        if (current + 1)%3 != 0 and current + 1 < len(states):
            u = states[current + 1][7]
        else:
            u = states[current][7]

    elif direction == 2:
        if current - 3 > -1:
            u = states[current - 3][7]
        else:
            u = states[current][7]

    elif direction == 3:
        if current%3 != 0 and current - 1 > -1:
            u = states[current -1][7]
        else:
            u = states[current][7]

    elif direction == 4:
        u = states[current][7]

    return u

def util(direction, current, states):
    if direction == 4:
        stateUtility = 1*prevUtil(direction, current, states) 
    else:
        stateUtility = 0.9*prevUtil(direction, current, states) +0.05*prevUtil((direction+1)%4, current, states) +0.05*prevUtil((direction-1+4)%4, current, states) 
    return round(stateUtility, 5)

def print_gridworld(states, iteration):
    print("Iteration ", iteration)
    for state in states:
        print(state)
    print()

def get_state_utilities(epsilon, rewards, states, gamma):
    terminal_state = 3-1 
    delta = 9999
    iteration = 1

    for i in range(len(states)):
        states[i].append(rewards[i])
        states[i][5] = direction(-1) 

    print_gridworld(states, iteration)

    while delta > epsilon*((1 - gamma)/gamma):
        iteration += 1        

        prevStates = copy.deepcopy(states) 
        
        for i in range(len(states)):
            bestActionUtility = float('-inf')
            
            if i == terminal_state:
                continue
            for j in range(5):
                states[i][j] = util(j, i, prevStates)
                if bestActionUtility < states[i][j]: 
                    d = j
                    bestActionUtility = states[i][j]
            for k in range(5):
                if k == d: continue
                if bestActionUtility == states[i][k]:
                    d = -1
                    break
            states[i][5] = direction(d)
            states[i][6] = bestActionUtility 
            states[i][7] = round(rewards[i] + gamma * bestActionUtility, 5) 
        
        delta = max([states[i][7]-prevStates[i][7] for i in range(len(states))])
        print_gridworld(states, iteration) 

def main():    
    states = [[0 for _ in range(7)] for _ in range(6)] 
    rewards = [-0.1, -0.1, 1, -0.1, -0.1, -0.05] 
    epsilon = 0.01
    gamma = 0.999
    get_state_utilities(epsilon, rewards, states, gamma)

if __name__ == "__main__":
    main()
    
