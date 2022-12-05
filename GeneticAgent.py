class GeneticAgent:
    def __init__(self, empty=False, trainingData=''):
        pass # for implementation by subclass
    
    '''
    Copy constructor
    '''
    def __init__(self, other):
        pass

    '''
    cross over genes with other agent
    '''
    def crossover(self, other):
        pass
    
    '''
    calculate fitness of agent
    '''
    def calculateFitness(self):
        pass
    
    '''
    mutate genes of agent
    '''
    def mutate(self):
        pass