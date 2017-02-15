import pandas as pd
import numpy as np
import datetime

files = [
'Unilever N.V. 3mth 5min',
'Unilever N.V. 3yr 1d'
]
for dataFile in files:
    df = pd.read_excel("data/"+dataFile+".xlsx")
    cgo = (df["Close"]>df["Open"])*1
    cgoLine= dataFile+'+CGO+' + ''.join([str(i) for i in cgo.tolist()][::-1])

    with open(datetime.datetime.now().strftime('%Y%m%d%H%M')+'-data.txt','a') as textFile:
        textFile.write(cgoLine+'\n')
