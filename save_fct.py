import datetime
class save_fct():
    #                   String      String          String    String  Bool
    def __init__(self,RowSeparator,ColumnSeparator,Directory,FileName,Dated):
        
        #Create date for the file and open it
        x = datetime.datetime.now()
        
        if(Dated):
            self.name = Directory + FileName+'_' + 'Date_' + str(x)[0:10] + '_' + str(x)[11:13] + '-' + str(x)[14:16] + ".csv"
        else:
            self.name = Directory + FileName + ".csv"
        self.file1 = open(self.name, 'w')
        
        print(self.name)
        
        self.Rseparator = RowSeparator
        self.Cseparator = ColumnSeparator


    #Save each lines in the same csv file
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
        
    #Close the csv fi
    def closeFile(self):
        self.file1.close()
