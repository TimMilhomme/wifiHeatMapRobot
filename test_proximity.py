import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser


#class detection_thymio3:
proxSensorsVal=[0,0,0,0,0]
groundSensorVal=[0,0]


def Braitenberg():

    #get the values of the sensors
    network.GetVariable("thymio-II", "prox.horizontal",reply_handler=get_variables_reply,error_handler=get_variables_error)
    
    #print the proximity sensors value in the terminal
    print ("proxSensor")
    dist = proxSensorsVal[2]
    print (dist)
    return True

def get_variables_reply(r):
    global proxSensorsVal
    proxSensorsVal=r
    
def get_variables_error(e):
    print ('error:')
    print (str(e))
    loop.quit()

def connect_to_thymio():
    
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


#def run     
network = connect_to_thymio()

#GObject loop
print ('starting loop')
loop = gobject.MainLoop()
#call the callback of Braitenberg algorithm
handle = gobject.timeout_add(10, Braitenberg)  # every 0.01 sec
loop.run()



