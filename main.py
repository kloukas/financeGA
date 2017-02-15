"""GA Analysis"""
import numpy as np
import csv
import time
import cProfile
import multiprocessing


start_time = time.clock()

class GAAnalysis(object):
    def __init__(self, memory=5, noStrategies=3000):
        self.memory = memory
        self.noStrategies = noStrategies
        self.maxGen = 200
        self.memPower = pow(2, self.memory)
        self.generateStrategies()
        self.targetAcc = 0.90

    def generateStrategies(self):
        maxStrat = pow(2, self.memPower)-1
        #strategies = random.sample(xrange(maxStrat), self.noStrategies)
        strategies = np.random.randint(0,high=maxStrat,size=self.noStrategies,dtype=np.uint64)#non Unique
        self.strategies = np.zeros((self.noStrategies,2),dtype=np.uint64)
        self.strategies[:,0] += strategies

    def scoreStrategies(self, history, nextState):
        """Simple scoring function, +1 if correctly predicted, +0 otherwise. Sort asc"""
        score = np.apply_along_axis(self.testStrat, 0, np.transpose(self.strategies), history, nextState)
        self.strategies[:,1] = np.uint64(0)
        self.strategies[:,1] += score
        self.strategies = self.strategies[self.strategies[:,1].argsort()]

    def selectParents(self,count):
        ran = np.random.rand(count)
        ranks = np.ceil((np.sqrt(1+4*ran*self.noStrategies*(self.noStrategies+1))-1)/2).astype(np.uint64)
        return self.strategies[ranks-1,][:,0].reshape(count/2,2)

    def generateMasks(self,maskP,count):
        twos = np.power(np.full(self.memPower, 2, dtype=np.uint64),range(self.memPower))
        binary = np.random.rand(self.memPower, count) < maskP
        return np.einsum("i,ij->j",twos,binary).astype(np.uint64)

    def evolveMatrix(self, retain=0):
        retain = int(retain*self.noStrategies)
        generate = self.noStrategies-retain
        newgen = self.strategies[-retain:][:,0]
        parents = self.selectParents(generate)
        xMask = self.generateMasks(0.5,generate/2)
        mMask = self.generateMasks(0.01,generate).reshape(generate/2,2)
        children = np.empty((generate/2,2),dtype=np.uint64)
        children[:,0] = ((parents[:,0] & ~(xMask)) | (parents[:,1] & xMask))
        children[:,1] = ((parents[:,1] & ~(xMask)) | (parents[:,0] & xMask))
        if retain>0:
            newgen = np.append(newgen, (children ^ mMask).reshape(generate,),axis=0)
        else:
            newgen = (children^mMask).reshape(generate,)
        self.strategies = np.zeros((self.noStrategies,2),dtype=np.uint64)
        self.strategies[:,0] += newgen


    def testStrat(self, strategies, history, nextState):
        return np.sum((((strategies[0]&(1<<history))>0)==nextState),dtype=np.uint64)

    def runOnce(self, datafile):
        with open(datafile) as dataFile:
            lines = [line.strip() for line in dataFile]
        tries = len(lines[0]) - self.memory
        history=[]
        nextState = []
        for i in range(0, tries):
            history.append(int(lines[0][i:i + self.memory],2))
            nextState.append(int(lines[0][i+self.memory]))
        history = np.array(history)
        nextState = np.array(nextState)
        print self.strategies
        self.scoreStrategies(history,nextState)
        print self.strategies


    def accuracy(self, noTries):
        stratAcc = self.strategies[:,1]/float(noTries)
        return stratAcc

    def run(self, name, line):
        tries=len(line) - self.memory
        history=[]
        nextState = []
        for i in range(0, tries):
            history.append(np.uint64(int(line[i:i + self.memory],2)))
            nextState.append(np.uint64(int(line[i+self.memory])))
        history = np.array(history)
        nextState = np.array(nextState)

        genAccuracy = []
        gen=0
        ending=""
        while True:
            self.scoreStrategies(history,nextState)
            acc = self.accuracy(tries)
            meanAcc = np.mean(acc)
            maxAcc = max(acc)
            minAcc = min(acc)
            genAccuracy.append((gen,meanAcc,maxAcc,minAcc))
            #print genAccuracy
            #print gen
            if gen>=self.maxGen and self.maxGen>0:
                ending="max generations reached"
                break
            elif maxAcc >= self.targetAcc:
                ending="target accuracy reached"
                break
            else:
                gen += 1
                self.evolveMatrix()

        print "Total number of generations: "+str(gen)
        print "Ended because "+ending
        with open(name+'.csv','wb') as resultsFile:
            wr = csv.writer(resultsFile, quoting=csv.QUOTE_ALL)
            wr.writerows(genAccuracy)
        #print genAccuracy
        ret = [name,ending]
        print time.clock() - start_time

if __name__ == '__main__':
    GAA = GAAnalysis()
    with open('data.txt') as dataFile:
        lines = [line.strip() for line in dataFile]

    GAA.run('file2',lines[0])
