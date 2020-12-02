from subprocess import check_output
import numpy as np
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

intensity = getWifi('VM514D00')
print (intensity)