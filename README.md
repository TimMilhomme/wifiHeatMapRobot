# wifiHeatMapRobot

This is a project where we couple a raspberry pi 4 with a Thymio II to create an autonomous vehicle able to map a room physically and by it's wifi intensity.

## What do you need?

* Raspberry Pi 4
* Thymio II
* Servo Motor
* Laser
* Battery
* We 3D printed piece but you might get way with it with tape and blue tack
* Jumpers cables
* USB-C to USB cable
* Micro-USB to USB cable

## How do you use the code?

To use our code any Python IDE should be fine. Download the repository keep all the in the same folder as the main. You can change the parameter at the beginning of tha main.

* The code Mapper and mapperNew are to code to lunch once you obtain the data of the main code. They will create a map of the surrounding. 
* The odometry function contain everithing to control the wheels of the thymio using an odometric system.
* The sweep function combine the data of the laser with the servo motor rotation to harvest the position of the surrouding.
* The save function save the data of the sweep function in a .cvs file.

## More details

* The pdf containing the full report of the project is present in the repository
* A video of the project is avaible on Youtube:
