"""GA Analysis"""
import numpy as np
import csv
import multiprocessing as mp
import logging
import traceback



class GAAnalysis(object):
    def __init__(self, memory=5, noStrategies=3000):
        self.memory = memory
        self.noStrategies = noStrategies
        self.maxGen = 1000
        self.memPower = pow(2, self.memory)
        self.targetAcc = 0.99

    def generateStrategies(self):
        maxStrat = pow(2, self.memPower)
        #strategies = random.sample(xrange(maxStrat), self.noStrategies)
        strategies = np.random.randint(0,high=maxStrat,size=self.noStrategies,dtype=np.uint64)#not Unique but probability of duplicate is effectively 0
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
        return self.strategies[ranks-1,][:,0].reshape(count//2,2)

    def generateMasks(self,maskP,count):
        twos = np.power(np.full(self.memPower, 2, dtype=np.uint64),range(self.memPower)) # Vector of powers of 2
        binary = np.random.rand(self.memPower, count) < maskP # Matrix of mask, each bit has maskP probability to be 1, each column corresponds to one mask
        # Each column of 'binary' corresponds to one mask. Multiplying each bit with the corresponding power of 2 and summing
        # gives the decimal representation of the mask
        return np.einsum("i,ij->j",twos,binary).astype(np.uint64)

    def evolveMatrix(self, gen, retain=0.1):
        retain = int(retain*self.noStrategies)
        generate = self.noStrategies-retain
        newgen = self.strategies[-retain:][:,0]
        parents = self.selectParents(generate)
        xMask = self.generateMasks(0.5,generate//2)
        mMask = self.generateMasks(self.mutRate(0.4,0.05,gen),generate).reshape(generate//2,2)
        children = np.empty((generate//2,2),dtype=np.uint64)
        children[:,0] = ((parents[:,0] & ~(xMask)) | (parents[:,1] & xMask))
        children[:,1] = ((parents[:,1] & ~(xMask)) | (parents[:,0] & xMask))
        if retain>0:
            newgen = np.append(newgen, (children ^ mMask).reshape(generate,),axis=0)
        else:
            newgen = (children^mMask).reshape(generate,)
        self.strategies = np.zeros((self.noStrategies,2),dtype=np.uint64)
        self.strategies[:,0] += newgen

    def mutRate(self,zero,inf,x):
        return (1/(np.sqrt(x)+(1/(zero-inf))))+inf

    def testStrat(self, strategies, history, nextState):
        predictionMatrix=strategies[0]&(1<<history)>0
        accuratePredictions = predictionMatrix==nextState
        return np.sum(accuratePredictions,dtype=np.uint64)

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
        print(self.strategies)
        self.scoreStrategies(history,nextState)
        print(self.strategies)


    def accuracy(self, noTries):
        stratAcc = self.strategies[:,1]/float(noTries)
        return stratAcc

    def run(self, line):
        self.generateStrategies()
        explode = line.split('+')
        name=explode[0]
        signal=explode[1]
        binStr = explode[2]
        tries=len(binStr) - self.memory
        history=[]
        nextState = []
        for i in range(0, tries):
            history.append(np.uint64(int(binStr[i:i + self.memory],2)))
            nextState.append(np.uint64(binStr[i+self.memory]))
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
            if gen%10 == 0:
                print("{}-{} on generation {}".format(name,signal,gen))

            if gen>=self.maxGen and self.maxGen>0:
                ending="max generations were reached"
                break
            elif maxAcc >= self.targetAcc:
                ending="target accuracy was reached"
                break
            else:
                gen += 1
                self.evolveMatrix(gen)
        bestStrat=self.strategies[-1]
        print("{:0b}".format(bestStrat[0]).zfill(self.memPower))
        uniqueStrat = len(np.unique(self.strategies[:,0]))
        filename = "results/{}-{}.csv".format(name,signal)
        with open(filename,'w', newline='') as resultsFile:
            wr = csv.writer(resultsFile, quoting=csv.QUOTE_ALL)
            wr.writerow(['Series',name])
            wr.writerow(['Signal',signal])
            wr.writerow(['Generations',gen])
            wr.writerow(['Ending',ending])
            wr.writerow(['Best Strategy',"{:0b}".format(bestStrat[0]).zfill(self.memPower)+"\t","Accuracy",bestStrat[1]/float(tries)])
            wr.writerow(['Unique Strats',uniqueStrat])
            wr.writerows(genAccuracy)
        print("{} finished after {} generations because {}".format(name,gen,ending))


if __name__ == '__main__':
    GAA = GAAnalysis(memory=6,noStrategies=10000)
    with open('201703151303-data.txt') as dataFile:
    #with open('testdata.txt') as dataFile:
        lines = [line.strip() for line in dataFile]
    # for i in range(len(lines)):
    #     GAA.run(lines[i])
    logger = mp.log_to_stderr(logging.DEBUG)
    workers = mp.cpu_count()
    pool = mp.Pool(workers)
    r = pool.map_async(GAA.run,lines)
    pool.close()
    pool.join()
