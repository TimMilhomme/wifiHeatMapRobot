import time as time
import smbus
import datetime

class sweep_fct():
    
    def __init__(self,RowSeparator,ColumnSeparator,FileName,Dated):
        import RPi.GPIO as GPIO

        self.servo = 12
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo, GPIO.OUT)

        self.i2c_ch = 1

        self.i2c_address = 0x52
        self.reg_add = 0x00
        self.bus = smbus.SMBus(self.i2c_ch)
        
        x = datetime.datetime.now()
        if(Dated):
            name = FileName+'_'+'Date_'+str(x)[0:10]+'_'+str(x)[11:13]+'-'+str(x)[14:16]+".csv"
        else:
            name = FileName
        print(name)
        self.file1 = open(name, 'w')
        self.Rseparator = RowSeparator
        self.Cseparator = ColumnSeparator

        self.p = GPIO.PWM(self.servo, 50)  # 50hz frequency
        self.p.start(3.5) # starting duty cycle (it set the servo to 0 degree)
        #self.control = [5, 5.05, 5.1, 5.15, 5.20, 5.25, 5.3, 5.35, 5.4, 5.45, 5.5]
        self.control2 = [3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7,7.5,8,8.5,9]
        self.control2degree = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.control3 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        
    def radarMode(self):
        for x in range(16):
            self.p.ChangeDutyCycle(self.control[x])
            time.sleep(0.03)
        for y in range(16):
            self.p.ChangeDutyCycle(self.control[15-y])
            time.sleep(0.03)
            
    def sweepMode(self,X,Y,Ang):
        self.step= 12
        self.count = 0
        
        values = []
        values2 = [X,Y,Ang]
        
        for x in range(self.step):
            self.p.ChangeDutyCycle(self.control2[x])
            time.sleep(0.1)
            
            self.data = self.bus.read_i2c_block_data(self.i2c_address,0,2)
    
            self.length_val=self.data[0]
            self.length_val=self.length_val<<8
            self.length_val|=self.data[1]
            if self.length_val>=2000:
                self.length_val=-1
            print(self.length_val)
            values.append(self.length_val)
            self.count +=1
            
        for y in range(self.step):
            self.p.ChangeDutyCycle(self.control2[self.step-1-y])
            time.sleep(0.1)
            self.data = self.bus.read_i2c_block_data(self.i2c_address,0,2)
    
            self.length_val=self.data[0]
            self.length_val=self.length_val<<8
            self.length_val|=self.data[1]
            if self.length_val>=2000:
                self.length_val=-1
            print(self.length_val)
            values.append(self.length_val)
            self.count +=1
        for i in range(self.step):
            
            values2.append((values[i]+values[self.step-i])/2)
            
        return values2
            
            
    def read_dist(self):
   
        self.data = self.bus.read_i2c_block_data(self.i2c_address,0,2)
    
        self.length_val=self.data[0]
        self.length_val=self.length_val<<8
        self.length_val|=self.data[1]
        if self.length_val>=2000:
            self.length_val=-1
        return self.length_val 