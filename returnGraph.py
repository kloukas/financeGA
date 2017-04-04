"""
Reads the normalised data file of each asset and graph its return (%Chg column)
against time
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from os import listdir
from os.path import isfile, join, splitext
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')




def tickFormatter(x,pos):
    return "{0:.0f}%".format(x*100)
    #return "{0:.0f}%".format(x) # For GBPUSD

dataPath="data/normalised/"
graphPath="graphs/"
files = [splitext(f)[0] for f in listdir(dataPath) if (isfile(join(dataPath, f)) and f[0] != "~" and f[-6] !='m')]
#print(files)
#fileName = 'GBPUSD Spot 3y 1d'
for fileName in files:
    fig, ax = plt.subplots()
    data = pd.read_excel(dataPath+fileName+".xlsx",skiprows=1)
    df = pd.DataFrame(data, columns = ['Exchange Date','%Chg'])
    df['Exchange Date'] = pd.to_datetime(df['Exchange Date'])
    df.index = df['Exchange Date']
    del df['Exchange Date']
    df = df[:-1]
    df = df[::-1]
    ax.set_title(fileName + ' Daily Returns')
    ax.yaxis.grid(True)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.02)) # Change 0.02 to 1 for GBPUSD
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(tickFormatter))
    ax.plot(df.index.to_pydatetime(),df['%Chg'],linewidth=1,color='k')
    ax.set_xlim((df.index.values[0],df.index.values[-1]))
    fig.set_size_inches(8,5)
    fig.savefig(graphPath+fileName.replace(" ","")+".png",bbox_inches='tight')
    print(fileName+" done")
