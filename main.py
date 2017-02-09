"""GA Analysis"""
import random
import numpy as np
import math

class GAAnalysis(object):
    def __init__(self, dataFile, memory=5, noStrategies=3000):
        self.memory = memory
        self.noStrategies = noStrategies
        self.dataFile = dataFile
        self.maxGen = -1
        self.strategies = []
        self.memPower = pow(2, self.memory)
        self.generateStrategies()
        self.targetAcc = 0.65

    def generateStrategies(self):
        maxStrat = pow(2, self.memPower)-1
        #strategies = random.sample(xrange(maxStrat), self.noStrategies)
        strategies = np.random.randint(0,maxStrat,size=self.noStrategies,dtype=np.int64)#non Unique
        zero = np.zeros(self.noStrategies,dtype=np.int)
        self.strategies = np.column_stack((strategies,zero))

    def initStrategies(self):
        for sId in range(0, len(self.strategies)):
            self.strategies[sId][1] = 0

    def scoreStrategies(self, inputStr):
        """Simple scoring function, +1 if correctly predicted, +0 otherwise. Sort asc"""
        history = inputStr[:-1]
        nextState = inputStr[-1:]
        history = inputStr[:-1]
        nextState = inputStr[-1:]
        self.strategies[:,1] +=((self.strategies[:,0]&(1<<int(history,2))>0)*1 == int(nextState))*1

    def select(self):
        ran = random.random()
        stratRank=int(math.ceil((math.sqrt(1+4*ran*self.noStrategies*(self.noStrategies+1)-1))/2))
        stratRank=min(self.noStrategies,stratRank) #Floating point math is weird, sometimes goes above index. Proper fix in the future
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
            parent1 = self.select()[0]
            parent2 = self.select()[0]
            xMask = self.generateMask(0.5)
            mMask1 = self.generateMask(0.01)
            mMask2 = self.generateMask(0.01)
            child1 = ((parent1 & ~(xMask)) | (parent2 & xMask)) ^ mMask1
            child2 = ((parent1 & xMask) | (parent2 & ~(xMask))) ^ mMask2
            newgen = np.append(newgen, [[child1, 0],[child2,0]],axis=0)
        self.strategies = newgen

    def runOnce(self):
        with open(self.dataFile) as dataFile:
            lines = [line.strip() for line in dataFile]
        self.initStrategies()
        tries = len(lines[0]) - self.memory
        for i in range(0, tries):
            inputStr = lines[0][i:i + self.memory+1]
            self.scoreStrategies(inputStr)
        self.strategies = self.strategies[self.strategies[:,1].argsort()]


    def accuracy(self, noTries):
        stratAcc = []
        for strat in self.strategies:
             stratAcc.append(strat[1]/float(noTries))
        return stratAcc

    def run(self):
        with open(self.dataFile) as dataFile:
            lines = [line.strip() for line in dataFile]
        self.initStrategies()
        tries = len(lines[0]) - self.memory
        genAccuracy = []
        gen=0
        while True:
            for i in range(0, tries):
                inputStr = lines[0][i:i + self.memory+1]
                self.scoreStrategies(inputStr)
            acc = self.accuracy(tries)
            meanAcc = np.mean(acc)
            maxAcc = max(acc)
            minAcc = min(acc)
            genAccuracy=(gen,(meanAcc,maxAcc,minAcc))
            if gen>=self.maxGen:
                break
            else:
                gen +=1

            if maxAcc >= self.targetAcc:
                break
            else:
                gen += 1



if __name__ == '__main__':
    GAA = GAAnalysis("data.txt")
    GAA.runOnce()
    print GAA.strategies
