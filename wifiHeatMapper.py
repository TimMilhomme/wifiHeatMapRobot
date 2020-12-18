import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv

csvName = "wifi_Date_2020-12-03_19-10.csv"

Xpos = []
Ypos = []
WifiIntensity = []

with open(csvName, newline='') as csvfile:
    Rowreader = csv.reader(csvfile, delimiter=';', lineterminator='\n')
    for Row in Rowreader:

        flag = False

        if int(Row[0]) in Xpos:
            indexList = [i for i, e in enumerate(Xpos) if e == int(Row[0])]
            for index in indexList:
                if Ypos[index] == int(Row[1]):
                    flag = True

        if not flag:
            Xpos.append(int(Row[0]))
            Ypos.append(int(Row[1]))
            WifiIntensity.append(int(Row[2]))

data = {'x': Xpos, 'y': Ypos, 'i': WifiIntensity}

df = pd.DataFrame(data, columns=['y', 'x', 'i'])
df = df.pivot('y', 'x', 'i')

sns.heatmap(df, linecolor='LightGrey', linewidths=.5, annot=True, cmap='RdBu',
            cbar=False, square=True)
plt.gca().invert_yaxis()
plt.show()
