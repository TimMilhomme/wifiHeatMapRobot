#Import the needed libraries
import time as time
import smbus
import datetime

#Create the class 
class sweep_fct():
    
    #Initialise the function
    def __init__(self,RowSeparator,ColumnSeparator,FileName,Dated):
        import RPi.GPIO as GPIO
        
        #Initialise the General Purpose Input Output (pins)
        self.pinGPIO = 12 #Input the cosen pin for the servo
        
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinGPIO, GPIO.OUT)
        
        #Initialise the I2C
        self.i2c_ch = 1 #Input the I2C channel for the laser
        
        self.i2c_address = 0x52
        self.reg_add = 0x00
        self.bus = smbus.SMBus(self.i2c_ch)
        
        #Create a filename with the date and time of recording
        x = datetime.datetime.now()
        if(Dated):
            name = FileName+'_'+'Date_'+str(x)[0:10]+'_'+str(x)[11:13]+'-'+str(x)[14:16]+".csv"
        else:
            name = FileName
        print(name)
        self.file1 = open(name, 'w')
        self.Rseparator = RowSeparator
        self.Cseparator = ColumnSeparator

        #Initialise the servo position
        self.servo = GPIO.PWM(self.pinGPIO, 50)  # 50hz frequency
        self.servo.start(3.5) # Starting position must be the same as first number of self.control
        self.control = [2.5,3,3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7,7.5,8,8.5,9,9.5,10] #Steps of the servo


    #Create the function harvesting the data with laser and servo        
    def sweepMode(self,X,Y,Ang):
        
        #Initialise the values for the sweep  
        self.step= 16
        self.step2 = 15
        self.count = 0
        self.delay = 0.1
        values = []
        values2 = [X,Y,Ang]
        
        #Start the first sweep for a given number of steps
        for x in range(self.step):
            
            #Give the array of steps
            self.servo.ChangeDutyCycle(self.control[x])
            #Wait for the signal to come back
            time.sleep(self.delay)
            
            #Get the value of the laser
            self.data = self.bus.read_i2c_block_data(self.i2c_address,0,2)
            self.length_val=self.data[0]
            self.length_val=self.length_val<<8
            self.length_val|=self.data[1]
            
            #If valu superior to range of the laser put -1
            if self.length_val>=2000:
                self.length_val=-1
            
            #Add valu to list of the sweep
            values.append(self.length_val)
            self.count +=1
            
        #This is the same as the first sweep it just go backward 
        for y in range(self.step):
            
            self.servo.ChangeDutyCycle(self.control[self.step2-y])
            time.sleep(self.delay)
            
            self.data = self.bus.read_i2c_block_data(self.i2c_address,0,2)
            self.length_val=self.data[0]
            self.length_val=self.length_val<<8
            self.length_val|=  self.data[1]
            
            if self.length_val>=2000:
                self.length_val=-1
            
            values.append(self.length_val)
            self.count +=1
            
        #Create the the list of values to return   
        for i in range(self.step):
            
            #For each line recorded add a value of the average to the list
            values2.append((values[i]+values[2*self.step2-i])/2)
            
        print(values)
        print(values2)
        return values2