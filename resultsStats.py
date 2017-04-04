"""
Reads the results file of each asset and produces a LaTeX table containing all
the assets' mean,max and min accuracy of the last generation as well as the best
performing strategy
"""
import pandas as pd
from os import listdir
from os.path import isfile, join, splitext


filePath="results/"

tickers = {
"Unilever NV":"UNc.AS",
"Alphabet":"GOOGL.O",
"Citigroup":"C",
"British American Tobacco":"BATS.L",
"Fast Retailing Co":"9983.T",
"Lockheed Martin":"LMT",
"Motor Oil":"MORr.AT",
"Tesco":"TSCO.L",
"Toyota":"7203.T",
"GBPUSD Spot":"GBPUSD"
}
files = [splitext(f)[0] for f in listdir(filePath) if (isfile(join(filePath, f)))]
files = sorted(files)

latexFormat ="""{1} & {2:.5f} & {3:.5f} & {4:.5f} & \\seqsplit{{{0}}} \\\\ \\cmidrule{{1-5}}
"""
#print(latexFormat)
for fileName in files:
    header = pd.read_csv(filePath+fileName+".csv",nrows=6, names=["A", "B", "C", "D"])
    data = pd.read_csv(filePath+fileName+".csv",skiprows=6, names=["Generation","Mean","Max","Min"])
    lastData = data.iloc[-1].values[1:]
    strategy = header["B"][4][:-1] # Remove \t from the end
    ticker = tickers[header["B"][0][:-6]] # Remove 6 characters, these are the period/interval
    period = header["B"][0][-5:] # Last 5 chars, period/interval
    rule = header["B"][1]
    mean = lastData[0]
    minV = lastData[1]
    maxV = lastData[2]
    corp = "{0} {1} {2}".format(ticker,period,rule)
    lines = latexFormat.format(strategy,corp,mean,minV,maxV)
    with open("resultsLatex.txt","a") as resultsLatex:
        resultsLatex.write(lines)
    print("Done with {}".format(corp))





# #series, mean, max, min, strategy
# results = [["Series", "Mean", "Max", "Min", "Strategy"]]
# for result in files:
#     header = pd.read_csv(filePath+result+".csv",nrows=6, names=["A", "B", "C", "D"])
#     data = pd.read_csv(filePath+result+".csv",skiprows=6, names=["Generation","Mean","Max","Min"])
#     lastData = data.iloc[-1].values[1:]
#     add = [header["B"][0]+" "+header["B"][1],lastData[0],lastData[1],lastData[2],header["B"][4]]
#     results.append(add)

#print(results)
# filename = "resultStats.csv"
# with open(filename,'w', newline='') as resultsStats:
#     wr = csv.writer(resultsStats, quoting=csv.QUOTE_ALL)
#     wr.writerows(results)
