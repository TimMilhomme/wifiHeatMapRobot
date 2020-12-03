##################################################
#csv frame:--------- X - Y - Alpha - Delta
#-------------------[0 - 1 -   2   - 3 to end]
# * Beta: 0 in the middle -> trigonometric wise
# * Angle in RADIAN
# * Length in mm
##################################################
import math
import csv
import matplotlib.pyplot as plt
import statistics as stat

#a = math.pi / 6

name='mapping.csv'

Xvalues=[]
Yvalues=[]
Xsalve=[]
Ysalve=[]
Offset=10
frame= 45

Xpos=[]
Ypos=[]
nRow=0

label=[]
def thetaC(idx):
    span = 90# Total angle range
    Nstep = 16 #Number of taken values in sweep
    b=(span/2) - (((idx-3)*span)/(Nstep-1)) #-1 to start at zero
    #print(b)
    return math.radians(b)

with open('mapping_Test4.csv', newline='') as csvfile:
    Rowreader = csv.reader(csvfile, delimiter=';',lineterminator='\n')
    for Row in Rowreader:
        Xpos.append(float(Row[0]))
        Ypos.append(float(Row[1]))
        Alpha = float(Row[2])
        for i in range(3, 19):
            if(float(Row[i])>0):
                Xsalve.append(Xpos[nRow] + frame * math.cos(Alpha) + (float(Row[i]) + Offset) * math.cos(Alpha+thetaC(i)))
                Ysalve.append(Ypos[nRow] + frame * math.sin(Alpha) + (float(Row[i]) + Offset) * math.sin(Alpha+thetaC(i)))
            elif(float(Row[i])==-3):
                Xsalve.append(Xpos[nRow] + frame * math.cos(Alpha) + (10000 + Offset) * math.cos(thetaC(Alpha, i)))
                Ysalve.append(Ypos[nRow] + frame * math.sin(Alpha) + (10000 + Offset) * math.sin(thetaC(Alpha, i)))
        Xvalues.append(Xsalve)
        Yvalues.append(Ysalve)
        Xsalve = []
        Ysalve = []
        nRow+=1


R=0.0
B=1.0
G=1

if 1==2:
    plt.scatter(Xvalues[0],Yvalues[0],color=(1,0,0),label='0',marker='.')

NewXvals=[]
NewYvals=[]

TransX=[]
TransY=[]
DistThreshold=100
DoubleFlag=False
chargement=0
stepcharge=100/len(Xvalues)

compX=0
compY=0

if(True==True):
    for Xset,Yset in zip(Xvalues,Yvalues):
        print('\r')
        chargement+=stepcharge
        print(str(int(chargement))+' %')
        for Xval,Yval in zip(Xset,Yset):
            compX = Xval
            compY = Yval
            TransX.append(Xval)
            TransY.append(Yval)
            for TransXset, TransYset in zip(Xvalues, Yvalues):
                for TransXval, TransYval in zip(Xset, Yset):
                    if((math.sqrt((compX-TransXval)**2+(compY-TransYval)**2))<DistThreshold):# and (Xset != TransXset):
                        TransX.append(TransXval)
                        TransY.append(TransYval)
                        compX = TransXval
                        compY = TransYval


#Try not to double ckeck value !!

            for XdoubleTest, YdoubleTest in zip(NewXvals, NewYvals):
                if stat.mean(TransX)==XdoubleTest and stat.mean(TransY)==YdoubleTest:
                    DoubleFlag=True
                    break

            #if DoubleFlag==False:
            if DoubleFlag == False and len(TransX) > 2:
                NewXvals.append(stat.mean(TransX))
                NewYvals.append(stat.mean(TransY))
            #if len(TransX)>2:
                #plt.plot(TransX,TransY,'b')
            TransX =[]
            TransY =[]
            Doubleflag = False


indice=0
R=1.0
G=0.0
B=0.0
step=1/len(Xvalues)
for Xset,Yset in zip(Xvalues,Yvalues):
    #plt.plot(Xset,Yset,label=indice,color=(R,G,B),marker='.')
    B+=step
    R-=step
    indice+=1
plt.plot(Xpos,Ypos)
measure=0


plt.scatter(NewXvals,NewYvals,color=(1,0,0),marker='1')

for x,y in zip(Xpos,Ypos):

    label = str(measure)
    measure+=1
    plt.annotate(label, # this is the text
                 (x,y), # this is the point to label
                 textcoords="offset points", # how to position the text
                 xytext=(0,5), # distance from text to points (x,y)
                 ha='center')

plt.legend()
plt.show()