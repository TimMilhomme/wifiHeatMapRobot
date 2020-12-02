import math
import random
import time
from subprocess import check_output
import numpy as np
from sweep_fct import *
from odometry_thymio import *
import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser

proxSensorsVal = [0, 0, 0, 0, 0]
forwardButton = [0]

i = 0
j = 0
data = []
direction = 0
maxTime = 30
running = False
dist = 0

# sweeper = sweep_fct('\n', ';', 'mapping', False)
odo = odometry_thymio()

wifi = 0  # getWifi()
data.append([i, j, wifi])
startTime = time.time()


def modpi(angle):

    while angle < -math.pi or angle > math.pi:
        if angle < -math.pi:
            angle += 2*math.pi
        else:
            angle -= 2*math.pi

    return angle


def getWifi():

    # using the check_output() for having the network term retrival
    networks = check_output(["iwlist", "wlan0", "scan"])

    # decoding it to strings
    networks = networks.decode('ascii')

    # Splitting the different networks
    networkList = networks.split('Cell')
    networkList.remove(networkList[0])

    # Creating a list of wifi intensity by network name
    networkIntensityList = []
    for i in range(0, len(networkList)-1):

        # print(i)
        network = networkList[i].split('\n')
        # print(network)
        networkName = network[5].split('\"')[1]
        # print(networkName)
        networkIntensity = network[3].split('/')[0]
        networkIntensity = int("".join(filter(str.isdigit, networkIntensity)))
        quality = int(networkIntensity*100/70)
        # print(quality)
        networkIntensityList.append([networkName, quality])

    # print(networkIntensityList)

    return networkIntensityList


def sensorFront():

    global i
    global j
    global data
    global direction
    global maxTime
    global wifi
    global startTime
    global running
    global dist

    network.GetVariable("thymio-II", "button.forward",reply_handler=get_button_forward_reply,error_handler=get_variables_error)
    
    # print the proximity sensors value in the terminal
    # print("proxSensor")
    #dist = proxSensorsVal[2]
    #print(dist)
    
    if forwardButton[0] == 1:
        startTime = time.time()
        running = True
        
    print(dist)
    
    if running:
    
        if dist > 1000:
            if direction == 0:
                ib = i+1
                jb = j
            if direction == math.pi/2:
                ib = i
                jb = j+1
            if direction == math.pi or -math.pi:
                ib = i-1
                jb = j
            if direction == -math.pi/2:
                ib = i
                jb = j-1
            data.append([ib, jb, -1])

            turn = random.randint(0, 1)
            if turn == 0:
                odo.turn_left(90)
                direction += math.pi/2
                direction = modpi(direction)
            else:
                odo.turn_right(90)
                direction -= math.pi/2
                direction = modpi(direction)
        else:
            odo.forward_dist(10)
            if direction == 0:
                i = i+1
            if direction == math.pi/2:
                j = j+1
            if direction == math.pi or -math.pi:
                i = i-1
            if direction == -math.pi/2:
                j = j-1
            wifi = 0  # getWifi()
            data.append([i, j, wifi])
            x = i*50
            y = j*50

            # sweeper.sweepMode(i, j, direction)
        
        runTime = time.time()-startTime
        if runTime > maxTime:
            loop.quit()
            
    # get the values of the sensors
    network.GetVariable("thymio-II", "prox.horizontal", reply_handler=get_variables_reply, error_handler=get_variables_error)
    
    dist = proxSensorsVal[2]

    return True

def get_variables_reply(r):
    global proxSensorsVal
    proxSensorsVal = r
def get_button_forward_reply(r):
    global forwardButton
    forwardButton=r
def get_variables_error(e):
    print('error:')
    print(str(e))
    loop.quit()

def connect_to_thymio():

    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False, help="use the system bus instead of the session bus")
    (options, args) = parser.parse_args()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    if options.system:
        bus = dbus.SystemBus()
    else:
        bus = dbus.SessionBus()
    # Create Aseba network
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')

    return network

network = connect_to_thymio()
loop = gobject.MainLoop()
handle = gobject.timeout_add(10, sensorFront)  # every 0.01 sec
loop.run()
# print heatmap
