import pandas as pd
from os import listdir
from os.path import isfile, join, splitext
filePath="results/"

files = [splitext(f)[0] for f in listdir(filePath) if (isfile(join(filePath, f)))]
files = sorted(files)
#series, mean, max, min, strategy
results = [["Series", "Mean", "Max", "Min", "Strategy"]]
for result in files:
    header = pd.read_csv(filePath+result+".csv",nrows=6, names=["A", "B", "C", "D"])
    data = pd.read_csv(filePath+result+".csv",skiprows=6, names=["Generation","Mean","Max","Min"])
    lastData = data.iloc[-1].values[1:]
    add = [header["B"][0]+" "+header["B"][1],lastData[0],lastData[1],lastData[2],header["B"][4][:-2]]
    results.append(add)

print(results)
