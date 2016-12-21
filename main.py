"""GA Analysis"""
import logging
import random

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class GAAnalysis(object):
    def __init__(self, dataFile, memory=5, noStrategies=3000, maxGen=0):
        self.memory = memory  # Number of days
        self.noStrategies = noStrategies  # Number of Strategies
        self.score = []
        for _ in range(0, self.noStrategies-1):
            self.score.append(0)
        self.strategies = []
        self.generateStrategies()
        self.dataFile = dataFile
        self.maxGen = maxGen


    def generateStrategies(self):
        maxStrat = pow(2, pow(2, self.memory))-1
        strategies = random.sample(xrange(maxStrat), self.noStrategies)
        for strat in strategies:
            self.strategies.append("{0:b}".format(strat).zfill(pow(2, self.memory)))


    def scoreStrategies(self, inputStr):
        """Simple scoring function, +1 if correctly predicted, 0 otherwise"""
        history = inputStr[:self.memory]
        for i in range(0, self.noStrategies-1):
            if self.strategies[i] == history:
                self.score[i] += 1

    def run(self):
        with open(self.dataFile) as dataFile:
            lines = [line.strip() for line in dataFile]
        for i in range(0, len(lines[0]) - self.memory):
            inputStr = lines[0][i:i + self.memory+1]
            self.scoreStrategies(inputStr)


if __name__ == '__main__':
    # with open('data.txt') as f:
    #            lines = f.readlines()
    #            for line in lines:
    GAA = GAAnalysis("data.txt")
    #GAA.run()
