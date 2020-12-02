import datetime
class save_fct():
    #                   String      String          String  Bool
    def __init__(self,RowSeparator,ColumnSeparator,FileName,Dated):

        x = datetime.datetime.now()
        if(Dated):
            self.name = "/home/pi/Desktop/02_12_2020/log/"+FileName+'_'+'Date_'+str(x)[0:10]+'_'+str(x)[11:13]+'-'+str(x)[14:16]+".csv"
        else:
            self.name = "/home/pi/Desktop/02_12_2020/log/"+FileName+".csv"
        self.file1 = open(self.name, 'w')
        print(self.name)
        self.Rseparator = RowSeparator
        self.Cseparator = ColumnSeparator

#Input [Xrob,Yrob,Alpha,Delta,Beta]

    def NewRow(self, *sweepingData):
        self.line=""
        first=True
        for element in sweepingData:
            if first:
                self.line+=str(element)
                first=False;
            else:
                self.line += self.Cseparator
                self.line += str(element)
        self.line += self.Rseparator
        self.file1.write(self.line)
    def closeFile(self):
        self.file1.close()
