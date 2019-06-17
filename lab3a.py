from random import randint, choice, random


def GA(equation):
    size = len(equation) - 1

    # fitness function
    def calc_fitness(sample):
        return abs(sum(equation[i] * sample[i] for i in range(len(sample))) + equation[-1])

    # coef of mutation
    mutation = 0.1

    # generate start population
    initial_samples = [[randint(1, int(abs(equation[-1]/equation[i]))) for i in range(len(equation) - 1)] for j in range(11)]

    numOfIterations = 0
    while True:

        numOfIterations += 1
        
        # calc fitness func
        fitnesses = [calc_fitness(sample) for sample in initial_samples]

        # check if the solution founded
        if 0 in fitnesses:
            return initial_samples[fitnesses.index(0)], numOfIterations

        # calculate probabilities of each gen to become a parent
        delta_weight = sum(1.0/fitness for fitness in fitnesses)
        mate_chances = [(1.0/delta)/delta_weight for delta in fitnesses]

        for _ in range(2):
            # get pair of parents
            for i in range(2):
                rand_val = random()
                parent_1 = 0
                for chance in mate_chances:
                    if (rand_val - chance) < 0:
                        break
                    rand_val -= chance
                    parent_1 += 1
                rand_val = random()
                parent_2 = 0
                for chance in mate_chances:
                    if (rand_val - chance) < 0:
                        break
                    rand_val -= chance
                    parent_2 += 1
                par_1 = initial_samples[parent_1]
                par_2 = initial_samples[parent_2]
                div = randint(0, len(initial_samples[0])-1)
                initial_samples[parent_1] = par_1[:div] + par_2[div:]
                initial_samples[parent_2] = par_2[:div] + par_1[div:]

        for _ in range(4):
            ind1 = randint(0, len(initial_samples[0])-1)
            ind2 = randint(0, len(initial_samples[0])-1)
            par = [initial_samples[ind1], initial_samples[ind2]]
            new_one = [] 
            for i in range(size):
                new_one.append(par[randint(0,1)][i])
            another_one = []
            for i in range(size):
                another_one.append(par[randint(0,1)][i])
            initial_samples[ind1] = new_one
            initial_samples[ind2] = another_one

        for _ in range(5):
            ind = randint(0, size-1)
            par = randint(0, len(initial_samples)-1)
            initial_samples[par][ind] = initial_samples[par][ind] + 1
    
       
        if numOfIterations >= 2**15:
            print("No solution can be found")
            return [None] * size, numOfIterations

def getInput():
    # ax1+bx2+cx3+dx4=y
    global numOfWeights
    numOfWeights = None
    while numOfWeights == None:
        try:
            numOfWeights = int(input("Enter num of weights: "))
        except:
            print("Input only integers!")
        if numOfWeights > 10 or numOfWeights < 4:
            print("Please, input number of weights in range(4, 10)")
            numOfWeights = None
    weights = []
    while len(weights) != numOfWeights:
        try:
            weights.append(
                float(input("Input w" + str(len(weights) + 1) + ": ")))
        except ValueError:
            print("Input only numbers! E.g 5.2")
    while True:
        try:
            weights.append(-float(input("Input y: ")))
            return weights
        except ValueError:
            print("Input only numbers! E.g 5.2")


def printEquation(weights):
    string = str(-weights[-1]) + " = "
    for i in range(numOfWeights):
        string += str(weights[i]) + "*x" + str(i+1) + " + "
    return string[:-3]


def printSolution(weights, solution):
    string = str(-weights[-1]) + " = "
    for i in range(numOfWeights):
        string += str(weights[i]) + "*" + str(solution[i]) + " + "
    return string[:-3]


if __name__ == "__main__":
    print("""=== Laboratory work 3a ===\nGenetic algorithm of calculating y = sum(wi * xi)\nPlease, input nessesary data""")
    # weights = getInput()
    equation = [ 1.0, 1.0, 1.0, 1.0, -4.0]
    numOfWeights = 4

    # equation = getInput()
    print("Your equation is: " + printEquation(equation))
    solution, iterations = GA(equation)
    if iterations < 2**15:
        print("Solution is: " + printSolution(equation, solution))
    print(str(iterations) + " iterations were done.")
