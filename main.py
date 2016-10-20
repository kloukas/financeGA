import os
import logging
import random
import math


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GAAnalysis():
    def __init__(self, dataFile, memory = 10, noStrategies = 3000):
        self.memory = memory #Number of days
        self.noStrategies = noStrategies #Number of Strategies
        self.score = []
        for i in range(0,self.noStrategies-1):
            self.score.append(0)
        self.strategies = []
        self.generateStrategies()
        self.dataFile = dataFile

    def generateStrategies(self):
        maxStrat = math.pow(2,self.memory)-1
        rng = random.SystemRandom()
        for i in range(0,self.noStrategies):
            strategy = "{0:b}".format(random.randint(0,maxStrat))
            for i in range(0,self.memory-len(strategy)):
                strategy = '0'+strategy
            self.strategies.append(strategy)



    def scoreStrategies(self, inputStr):
        history = inputStr[:self.memory]
        nextDigit = inputStr[self.memory:]
        for i in range(0,self.noStrategies-1):
            if self.strategies[i] == history:
                self.score[i] += 1


    def run(self):
        with open('data.txt') as file:
            lines = [line.strip() for line in file]
        for i in range(0,len(lines[0]) - self.memory):
            inputStr = lines[0][i:i + self.memory+1]
            self.scoreStrategies(inputStr)



if __name__ == '__main__':
    #with open('data.txt') as f:
    #            lines = f.readlines()
    #            for line in lines:
    gaa = GAAnalysis("data.txt")
    gaa.run()
