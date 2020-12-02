from subprocess import check_output
import numpy as np
import time


def getWifi(wantedWifi):

    # using the check_output() for having the network term retrival
    networks = check_output(["iwlist", "wlan0", "scan"])

    # decoding it to strings
    networks = networks.decode('ascii')

    # Splitting the different networks
    networkList = networks.split('Cell')
    networkList.remove(networkList[0])

    # Creating a list of wifi intensity by network name
    networkIntensityList = []
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

"""
def getWifiAvg(wantedWifi, itr):
    val = 0
    count = 0
    quality = 0
    qualityAvg = 0
    for i in range(itr):
        val = getWifi(wantedWifi)
        if val != 0:
            quality += val
            count += 1
    if count != 0:
        qualityAvg = quality/count
    
    return qualityAvg"""


def getWifiNoZero(wantedWifi):
    val = 0
    while val == 0:
        val = getWifi(wantedWifi)
    
    return val


intensity = getWifiNoZero('VM514D00')
print (intensity)