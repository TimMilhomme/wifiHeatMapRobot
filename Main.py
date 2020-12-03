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
from save_fct import *

proxSensorsVal = [0, 0, 0, 0, 0]
forwardButton = [0]

i = 0
j = 0
data = []
direction = 0
maxTime = 300
running = False
flag = True
travelled_dist = 300
obstacle_dist =350

sweeping = []

sweeper = sweep_fct('\n', ';', 'mapping', False)
odo = odometry_thymio()
saver = save_fct('\n',';','mapping',True)
saver2 = save_fct('\n',';','wifi',True)

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


def getWifi(wantedWifi):

    # using the check_output() for having the network term retrival
    networks = check_output(["iwlist", "wlan0", "scan"])

    # decoding it to strings
    networks = networks.decode('ascii')

    # Splitting the different networks
    networkList = networks.split('Cell')
    networkList.remove(networkList[0])
    
    quality = 0
    
    for i in range(0, len(networkList)-1):

        # print(i)
        network = networkList[i].split('\n')
        # print(network)
        networkName = network[5].split('\"')[1]
        # print(networkName)
        if networkName == wantedWifi:
            
            networkIntensity = network[3].split('/')[0]
            networkIntensity = int("".join(filter(str.isdigit, networkIntensity)))
            quality = int(networkIntensity*100/70) 

    return quality

def getWifiNoZero(wantedWifi):
    val = 0
    while val == 0:
        val = getWifi(wantedWifi)
    
    return val

def sensorFront():

    global i
    global j
    global data
    global direction
    global maxTime
    global wifi
    global startTime
    global running
    global travelled_dist
    global obstacle_dist
    global flag
    global sweeping
    
    network.GetVariable("thymio-II", "button.forward",reply_handler=get_button_forward_reply,error_handler=get_variables_error)
    
    if flag:
        if forwardButton[0] == 1:
            print('check')
            startTime = time.time()
            running = True
            flag = False
            x = i*travelled_dist
            y = j*travelled_dist
            sweeping = sweeper.sweepMode(x, y, direction)
            saver.NewRow(*sweeping)
            wifi = getWifiNoZero('VM514D00')
            data.append([i, j, wifi])
            datawifi = [i, j, wifi]
            saver2.NewRow(*datawifi)
        
    if running:
        
        if (sweeping[6] >= 0 and sweeping[6] < obstacle_dist) or (sweeping[7] >= 0 and sweeping[7] < obstacle_dist) or (sweeping[8] >= 0 and sweeping[8] < obstacle_dist) or (sweeping[9] >= 0 and sweeping[9] < obstacle_dist):
            print('turning')
            if direction == 0:
                ib = i+1
                jb = j
            if direction == math.pi/2:
                ib = i
                jb = j+1
            if direction == math.pi or direction == -math.pi:
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
            x = i*travelled_dist
            y = j*travelled_dist
            sweeping = sweeper.sweepMode(x, y, direction)
            saver.NewRow(*sweeping)
            wifi = getWifiNoZero('VM514D00')
            data.append([i, j, wifi])
            datawifi = [i, j, wifi]
            saver2.NewRow(*datawifi)
            
        else:
            print('forward')
            odo.forward_dist(travelled_dist)
            if direction == 0:
                i = i+1
            if direction == math.pi/2:
                j = j+1
            if direction == math.pi or direction == -math.pi:
                i = i-1
            if direction == -math.pi/2:
                j = j-1
            x = i*travelled_dist
            y = j*travelled_dist
            sweeping = sweeper.sweepMode(x, y, direction)
            saver.NewRow(*sweeping)
            wifi = getWifiNoZero('VM514D00')
            data.append([i, j, wifi])
            datawifi = [i, j, wifi]
            saver2.NewRow(*datawifi)
            
        
        runTime = time.time()-startTime
        if runTime > maxTime:
            print(data)
            saver.closeFile()
            saver2.closeFile()
            loop.quit()

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
print('Press forward button')
loop.run()
# print heatmap


