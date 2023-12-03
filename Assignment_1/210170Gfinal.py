import random
import heapq

def get_inputs(inputFile):
    try:
        file = open(inputFile, "r")
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
        roadMap.append(inputArray[i])
    for i in range(numberOfLocations, len(inputArray)):
        trucks.append(inputArray[i][0].split('#'))

    for truck in trucks:
        truck.append([])
        truck.append([])

    return roadMap, trucks

def write_output(outputFile, text):
    try:
        file = open(outputFile, "w")
        file.write(text)
    except Exception as e:
        print(e)
    finally:
        file.close()

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

def output_format(trucks, minimumCost):
    text = ""
    for truck in trucks:
        deliverySequenceList = [chr(97 + city) for city in truck[3]]
        deliverySequenceString = ",".join(deliverySequenceList)
        text += truck[0] + '#' + deliverySequenceString + '\n'

    text += str(minimumCost)
    return text
        
def first_choice_hill_climbing(numberOfTrials):
    minimumCost = float('inf')
    roadMap, trucks = get_inputs('input.txt')
    for i in range(numberOfTrials):
        genarate_random_state(roadMap, trucks)
        cost = calculate_path_cost(roadMap, trucks)
        if minimumCost>cost:
            minimumCost=cost
            for truck in trucks:
                truck[3] = truck[2]
    text = output_format(trucks, minimumCost)
    write_output('210170G.txt', text)

#################################################################

if __name__ == "__main__":
    first_choice_hill_climbing(1000)

