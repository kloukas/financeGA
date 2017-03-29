import pandas as pd
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join, splitext

mypath="data/"
files = [splitext(f)[0] for f in listdir(mypath) if (isfile(join(mypath, f)) and f[0] != "~")]
filename = datetime.datetime.now().strftime('%Y%m%d%H%M')+'-data.txt'
for dataFile in files:
    df = pd.read_excel("data/"+dataFile+".xlsx",skiprows=1)
    highP = df["High"].values[1:]
    lowP = df["Low"].values[1:]
    closeP = df["Close"].values[:-1]
    openP = df["Open"].values[:-1]

    cgo = (df["Close"]>df["Open"])*1
    cgoLine= dataFile+'+CGO+' + ''.join([str(i) for i in cgo.tolist()][::-1])

    ogma = (openP>highP)*1
    ogmaLine= dataFile+'+OGMA+' + ''.join([str(i) for i in ogma.tolist()][::-1])

    cgma = (closeP>highP)*1
    cgmaLine = dataFile+'+CGMA+' + ''.join([str(i) for i in cgma.tolist()][::-1])

    olmi = (openP<lowP)*1
    olmiLine = dataFile+'+OLMI+' + ''.join([str(i) for i in olmi.tolist()][::-1])

    clmi = (closeP<lowP)*1
    clmiLine = dataFile+'+CLMI+' + ''.join([str(i) for i in clmi.tolist()][::-1])
    with open(filename,'a') as textFile:
        textFile.write(cgoLine+'\n')
        textFile.write(ogmaLine+'\n')
        textFile.write(cgmaLine+'\n')
        textFile.write(olmiLine+'\n')
        textFile.write(clmiLine+'\n')
    print("Done with "+dataFile)
