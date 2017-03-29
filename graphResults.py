import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from os import listdir
from os.path import isfile, join, splitext
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')

filePath="results/"
graphPath="graphs/"
files = [splitext(f)[0] for f in listdir(filePath) if (isfile(join(filePath, f)))]
files = sorted(files)
assetNo = len(files)//5
styles =[
["0","solid"],
["0.5","solid"],
["0","--"],
["0.5","--"],
["0","-."]
]
for i in range(0,assetNo):
    fig, ax = plt.subplots()
    for k in range(0,5):
        header = pd.read_csv(filePath+files[i*5+k]+".csv",nrows=6, names=["A", "B", "C", "D"])
        data = pd.read_csv(filePath+files[i*5+k]+".csv",skiprows=6, names=["Generation","Mean","Max","Min"])
        ax.plot(data["Generation"],data["Max"],linewidth=2,linestyle=styles[k][1],label=header["B"][1])
        print("Plotting"+header["B"][0]+header["B"][1])

    ax.set_title(header["B"][0])
    ax.yaxis.grid(True)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
    ax.set_xlim((0,1000))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    fig.set_size_inches(8,5)
    fig.savefig(graphPath+header["B"][0].replace(" ","")+"resultsGraph.png",bbox_inches='tight')

# ax.yaxis.set_major_locator(ticker.MultipleLocator(0.02)) # Change 0.02 to 1 for GBPUSD
# ax.yaxis.set_major_formatter(ticker.FuncFormatter(tickFormatter))
# fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
