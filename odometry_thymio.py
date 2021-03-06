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
        delay = dist*0.015 #seconds
        
        #Call the function connect to thymio
        network = self.connect_to_thymio()

        #Move robot at the speed between 0 and 500
        totalRight=200
        totalLeft=193
        
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
        totalRight=200
        totalLeft=-200
        
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

        totalRight=-200
        totalLeft=200

        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])

        time.sleep(delay)

        totalRight = 0
        totalLeft = 0

        network.SetVariable("thymio-II", "motor.left.target", [totalLeft])
        network.SetVariable("thymio-II", "motor.right.target", [totalRight])
        return True
    
    #Function to get the forward button value 0 nothing 1 click
    def get_button_forward_reply(self, r):
        global forwardButton
        forwardButton=r

    #Function to detect error and quit loop
    def get_variables_error(self, e):
        print ('error:')
        print (str(e))
        loop.quit()
