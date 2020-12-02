#Import all needed libraries
import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser
import time

#Create the odometry class
class odometry_thymio():
    
    #Initialise the values of the proximity sensors 
    proxSensorsVal=[0,0,0,0,0]
    
    #Function connecting the Raspebbry Pi 4 to the Thymio II
    def connect_to_thymio(self):
        parser = OptionParser()
        parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
        (options, args) = parser.parse_args()
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        if options.system:
            bus = dbus.SystemBus()
        else:
            bus = dbus.SessionBus()
        #Create Aseba network
        network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
        
        return network


    #Function making the robot moving forward with a dist input, wich is the ditance we want the robot to move in cm
    def forward_dist(self,dist):
        
        #Initialize the values
        totalRight = 0
        totalLeft = 0

        #Create a delay with respect to the distance
        #This coeficient was find experimentally adjust it with the type of ground and the speed of the robot
        delay = dist*0.15 #seconds
        
        #Call the function connect to thymio
        network = self.connect_to_thymio()

        #Move robot at the speed between 0 and 500
        totalRight=totalRight*4+200
        totalLeft=totalLeft*4+193
        
        #send motor value to the robot
        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])
        
        #Wait for the robot to move
        time.sleep(delay) #seconds
        
        #Stop the robot
        totalRight = 0
        totalLeft = 0
        
        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])
        return True
    
    #Function to make the robot turn left with a given angle
    def turn_left(self,angle):
        
        #Initialize the values
        totalRight = 0
        totalLeft = 0
        
        #angle is the angle we want the robot to turn in radian 
        #This coeficient was find experimentally adjust it with the type of ground and the speed of the robot
        delay = angle*0.01151  #seconds
        
        #Connect to the robot
        network = self.connect_to_thymio()

        #Add oposit value to each wheels to make it turn on itself
        totalRight=totalRight*4+200
        totalLeft=totalLeft*4-200
        
        #send motor value to the robot
        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])

        time.sleep(delay) #seconds
        
        totalRight = 0
        totalLeft = 0
        
        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])
        return True
    
    #Same as left
    def turn_right(self,angle):

        totalRight = 0
        totalLeft = 0

        delay = angle*0.01151

        network = self.connect_to_thymio()

        totalRight=totalRight*4-200
        totalLeft=totalLeft*4+200

        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])

        time.sleep(delay)

        totalRight = 0
        totalLeft = 0

        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])
        return True
    
    #Function starting the code and waiting to activate the central button
    def start_button(self):
        
        centralButton=[0]
        forwardButton=[0]

        stop = False
        flag = False

        def waiting():
            global stop
            global flag
            
            #get the value of the center button
            network.GetVariable("thymio-II", "button.center",reply_handler=get_button_reply,error_handler=get_variables_error)
            #get the value of the foward button
            network.GetVariable("thymio-II", "button.forward",reply_handler=get_button_forward_reply,error_handler=get_variables_error)

                
            if centralButton[0] == 1:
                if flag:
                    stop = not stop
                    flag=False
            else:
                flag=True;
                
            if forwardButton[0] == 1:
                print("Quit")
                loop.quit()
                   
            if stop == True:
                print("Stop")  
         
            return True

        #Function to get the central button value 0 nothing 1 click
        def get_button_reply(r):
            global centralButton
            centralButton=r

        #Function to get the forward button value 0 nothing 1 click
        def get_button_forward_reply(r):
            global forwardButton
            forwardButton=r

        #Function to detect error and quit loop
        def get_variables_error(e):
            print ('error:')
            print (str(e))
            loop.quit()
            
        if __name__ == '__main__':
            
            network = self.connect_to_thymio()
         
            #print in the terminal the name of each Aseba NOde
            print (network.GetNodesList())
         
            #GObject loop
            print ('starting loop')
            loop = gobject.MainLoop()
            #call the callback of waiting algorithm
            handle = gobject.timeout_add (10, waiting) #every 0.01 sec
            loop.run()
        return True