import pandas as pd
import numpy as np
import datetime

files = [
'Alphabet 3mth 5min',
'Alphabet 3yr 1d',
'British American Tobacco 3mth 5min',
'British American Tobacco 3yr 1d',
'Fast Retailing Co 3mth 5min',
'Fast Retailing Co 3yr 1d',
'GBPUSD 3mth 5min',
'GBPUSD 3yr 1d',
'Lockheed Martin 3mth 5min',
'Lockheed Martin 3yr 1d',
'Motor Oil 3mth 5min',
'Motor Oil 3yr 1d',
'Tesco 3mth 5min',
'Tesco 3yr 1d',
'Toyota 3mth 5min',
'Toyota 3yr 1d',
'Unilever N.V. 3mth 5min',
'Unilever N.V. 3yr 1d'
]
filename = datetime.datetime.now().strftime('%Y%m%d%H%M')+'-data.txt'
for dataFile in files:
    df = pd.read_excel("data/"+dataFile+".xlsx")
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
    print "Done with "+dataFile
