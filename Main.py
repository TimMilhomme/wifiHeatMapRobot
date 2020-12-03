import math
import random
import time
from subprocess import check_output
import numpy as np

import dbus
import dbus.mainloop.glib
from gi.repository import GObject as gobject
from optparse import OptionParser

from save_fct import *
from sweep_fct import *
from odometry_thymio import *

odo = odometry_thymio()
sweeper = sweep_fct()
saver = save_fct('\n',';','/home/pi/Desktop/03_12_2020_V2/log/','mapping',True)
saver2 = save_fct('\n',';','/home/pi/Desktop/03_12_2020_V2/log/','wifi',True)

running = False
flag = True
obstacle = False

forwardButton = [0]

i = 0
j = 0
direction = 0

datawifi = []
sweeping = []

maxTime = 300
travelled_dist = 200
obstacle_dist =300

wifi = 0 
startTime = time.time()


def modpi(angle):

    while angle < -math.pi or angle > math.pi:
        if angle < -math.pi:
            angle += 2*math.pi
        else:
            angle -= 2*math.pi

    return angle

# This function gathers a list of wifi intensities associated to the name of its network
def getWifi(wantedWifi):

    # using the check_output() for having the network term retrival
    networks = check_output(["iwlist", "wlan0", "scan"])

    # decoding it to strings
    networks = networks.decode('ascii')

    # Splitting the different networks
    networkList = networks.split('Cell')
    networkList.remove(networkList[0])
    
    quality = 0
    
    # Creating a list of wifi intensity by network name
    for i in range(0, len(networkList)-1):

        network = networkList[i].split('\n')
        networkName = network[5].split('\"')[1]
        if networkName == wantedWifi:
            
            networkIntensity = network[3].split('/')[0]
            networkIntensity = int("".join(filter(str.isdigit, networkIntensity)))
            quality = int(networkIntensity*100/70) 

    return quality

# This function allows us to get rid of parasitic values of wifi intensity but adds a lot of waiting
def getWifiNoZero(wantedWifi):
    
    # Waiting for a no-zero/parasite value of the wifi intensity
    val = 0
    while val == 0:
        val = getWifi(wantedWifi)
    
    return val


def get_button_forward_reply(r):
    global forwardButton
    forwardButton=r
def get_variables_error(e):
    print('error:')
    print(str(e))
    loop.quit()


# This function is executed over and over until the loop is quitted
# Its purpose is to allow the user to launch the robot whe desired
def startLoop():
    
    global startTime
    global running
    global flag
    
    # Fetching the state value of Thymio's forward button
    network.GetVariable("thymio-II", "button.forward",reply_handler=get_button_forward_reply,error_handler=get_variables_error)
    
    # Checking if the forward button is pressed to launch the main logic
    if flag:
        if forwardButton[0] == 1:
            running = True
            flag = False
            loop.quit()

    return True


# This part creates a loop that will run the startLoop function, and runs it every 0.01 sec
network = odo.connect_to_thymio()
loop = gobject.MainLoop()
handle = gobject.timeout_add(10, startLoop)
print('Press forward button')
loop.run()

startTime = time.time()

# This block is used to save and gather data
# First it converts the position of the robot from coordinates to distances
x = i*travelled_dist
y = j*travelled_dist
# Then it performs the sweep function that gathers distances in front of it, and saves it
sweeping = sweeper.sweepMode(x, y, direction)
saver.NewRow(*sweeping)
# Finally it gathers the wifi intensity and saves it
wifi = getWifiNoZero('VM514D00')
datawifi = [i, j, wifi]
saver2.NewRow(*datawifi)

# This part is main navigation logic loop and is running only when the forward button as been pressed
while running:
    
    # Using middle values of the previous sweep, the robot checks for an obstacle in front of it
    for n in range(5, 10):
        if (sweeping[n] >= 0 and sweeping[n] < obstacle_dist):
            obstacle = True
        
    if obstacle:
        # If an obstacle is detected the robot first flags the tile in front of it as containing one
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
        datawifi = [ib, jb, -1]
        saver2.NewRow(*datawifi)

        # Then it randomly choose to turn 90° left or right and updates its direction (in radians modulo pi)
        turn = random.randint(0, 1)
        if turn == 0:
            odo.turn_left(90)
            direction += math.pi/2
            direction = modpi(direction)
        else:
            odo.turn_right(90)
            direction -= math.pi/2
            direction = modpi(direction)
        
        # Finally it performs a sweep and saves the values
        x = i*travelled_dist
        y = j*travelled_dist
        sweeping = sweeper.sweepMode(x, y, direction)
        saver.NewRow(*sweeping)
        wifi = getWifiNoZero('VM514D00')
        datawifi = [i, j, wifi]
        saver2.NewRow(*datawifi)
        
    else:
        # If no obstacles were detected, it moves forward to the next tile
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
        
        # Then it performs a sweep and saves the values
        sweeping = sweeper.sweepMode(x, y, direction)
        saver.NewRow(*sweeping)
        wifi = getWifiNoZero('VM514D00')
        datawifi = [i, j, wifi]
        saver2.NewRow(*datawifi)
        
    obstacle = False
    
    # At each cycle the robot checks if its stopping condition is satisfied
    runTime = time.time()-startTime
    if runTime > maxTime:
        running = False
        
saver.closeFile()
saver2.closeFile()
        
