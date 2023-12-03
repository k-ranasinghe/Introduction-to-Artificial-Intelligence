import random
import heapq
import numpy as np

def get_inputs():
    
    try:
        file = open("input.txt", "r")
        inputs = file.read()
    except Exception as e:
        print(e)
    finally:
        file.close()
    
    rows = inputs.split('\n')
    inputArray = []
    for row in rows:
        inputArray.append(row.split(','))

    numberOfLocations = len(inputArray[0])
    roadMap = []
    trucks = []
    for i in range(numberOfLocations):
        # roadMap.append(inputArray[i])
        line = inputArray[i]
        city_map = [float(x.strip()) if x.strip() != 'N' else np.inf for x in line.split(",")]
        roadMap.append(city_map)
        print(city_map)
    for i in range(numberOfLocations, len(inputArray)):
        trucks.append(inputArray[i][0].split('#'))

    for truck in trucks:
        truck.append([])

    return roadMap, trucks

def genarate_random_state(roadMap, trucks):
    noneDeliveredLocation = [c for c in range(1, len(roadMap))]

    for truck in trucks:
        if len(noneDeliveredLocation) == 0: return
        path = []
        for i in range(int(truck[1])):
            randomNumber = random.randint(0, len(noneDeliveredLocation)-1)
            location = noneDeliveredLocation[randomNumber]
            path.append(location)
            noneDeliveredLocation.remove(location)

        truck[2] = path

def calculate_node_distances(roadMap, initialLocation, targetLocation):
    numberOfNodes = len(roadMap)
    distances = [float('inf')] * numberOfNodes
    distances[initialLocation] = 0

    priorityQueue = [(0, initialLocation)]

    while priorityQueue:
        currentDistance, currentNode = heapq.heappop(priorityQueue)

        if currentDistance > distances[currentNode]:
            continue

        if currentNode == targetLocation:
            return distances[targetLocation]

        for neighbor, distance in enumerate(roadMap[currentNode]):
            if distance != 'N':
                newDistance = currentDistance + int(distance)

                if newDistance < distances[neighbor]:
                    distances[neighbor] = newDistance
                    heapq.heappush(priorityQueue, (newDistance, neighbor))

    return
            
def calculate_path_cost(roadMap, trucks):
    totalCost = 0
    for truck in trucks:
        initialLocation = 0
        cost = 0
        for location in truck[2]:
            cost += calculate_node_distances(roadMap, initialLocation, location)
            initialLocation = location
        totalCost += cost
    return totalCost
        
def hill_climbing(numberOfTrials):
    minimumCost = float('inf')
    roadMap, trucks = get_inputs()

    for i in range(numberOfTrials):
        genarate_random_state(roadMap, trucks)
        cost = calculate_path_cost(roadMap, trucks)
        if minimumCost>cost:
            minimumCost=cost
    print(trucks)
    print(minimumCost)       

#################################################################

hill_climbing(1000)



