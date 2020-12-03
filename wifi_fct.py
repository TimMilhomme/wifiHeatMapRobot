from subprocess import check_output
import numpy as np

class wifi_fct:
 # This function gathers a list of wifi intensities associated to the name of its network
    def getWifi(self,wantedWifi):

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
    def getWifiNoZero(self,wantedWifi):
        
        # Waiting for a no-zero/parasite value of the wifi intensity
        val = 0
        while val == 0:
            val = self.getWifi(wantedWifi)
        
        return val
