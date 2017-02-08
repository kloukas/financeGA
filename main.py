"""GA Analysis"""
import random
import numpy as np
import math

class GAAnalysis(object):
    def __init__(self, dataFile, memory=5, noStrategies=3000):
        self.memory = memory
        self.noStrategies = noStrategies
        self.strategies = []
        self.dataFile = dataFile
        self.maxGen = -1
        self.memPower = pow(2, self.memory)
        self.generateStrategies()

    def generateStrategies(self):
        maxStrat = pow(2, self.memPower)-1
        strategies = random.sample(xrange(maxStrat), self.noStrategies)
        for strat in strategies:
            self.strategies.append(["{0:b}".format(strat).zfill(self.memPower), 0])

    def initStrategies(self):
        for sId in range(0, len(self.strategies)):
            self.strategies[sId][1] = 0

    def scoreStrategies(self, inputStr):
        """Simple scoring function, +1 if correctly predicted, +0 otherwise. Sort asc"""
        history = inputStr[:-1]
        nextState = inputStr[-1:]
        for i in range(0, self.noStrategies):
            if self.strategies[i][0][int(history, 2)] == nextState:
                self.strategies[i][1] += 1
        self.strategies.sort(key=lambda score: score[1])

    def debugSelect(self):
        while True:
            try:
                ran = random.random()
                stratRank=int(math.ceil((math.sqrt(1+4*ran*self.noStrategies*(self.noStrategies+1)-1))/2))
                stratRank=min(self.noStrategies,stratRank) #Floating point math is weird, sometimes goes above 3000. Proper fix in the future
                print self.strategies[stratRank-1]
            except:
                print ran
                print (math.sqrt(1+4*ran*self.noStrategies*(self.noStrategies+1)-1))/2
                print stratRank
                break

    def select(self):
                ran = random.random()
                stratRank=int(math.ceil((math.sqrt(1+4*ran*self.noStrategies*(self.noStrategies+1)-1))/2))
                stratRank=min(self.noStrategies,stratRank) #Floating point math is weird, sometimes goes above 3000. Proper fix in the future
                return self.strategies[stratRank-1]


    def generateMask(self, maskP):
        rand = np.random.rand(self.memPower,) < maskP
        mask = 0
        for i in range(0, self.memPower):
            mask += rand[i]*pow(2, i)
        return mask

    def evolve(self, retain=0.2):
        """Elitist Selection"""
        retain = int(retain*self.noStrategies)
        newgen = self.strategies[-retain:]  # Elitist Selection, retain portion of fittest strategies
        # Rank Based Proportional Selection, Uniform Crossover, Uniform Mutation
        while len(newgen) < len(self.strategies):
            parent1 = int(self.select()[0], 2)
            parent2 = int(self.select()[0], 2)
            xMask = self.generateMask(0.5)
            mMask1 = self.generateMask(0.01)
            mMask2 = self.generateMask(0.01)
            child1 = "{0:b}".format(((parent1 & ~(xMask)) | (parent2 & xMask)) ^
                                    mMask1).zfill(self.memPower)
            child2 = "{0:b}".format(((parent1 & xMask) | (parent2 & ~(xMask))) ^
                                    mMask2).zfill(self.memPower)
            newgen.append([child1, 0])
            newgen.append([child2, 0])
        self.strategies = newgen

    def run(self):
        with open(self.dataFile) as dataFile:
            lines = [line.strip() for line in dataFile]
        self.initStrategies()
        tries = len(lines[0]) - self.memory
        for i in range(0, tries):
            inputStr = lines[0][i:i + self.memory+1]
            self.scoreStrategies(inputStr)


if __name__ == '__main__':
    GAA = GAAnalysis("data.txt")
    GAA.run()
    print GAA.strategies[:10]
    GAA.evolve()
    print GAA.strategies[:10]
