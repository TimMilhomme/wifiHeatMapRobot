# wifiHeatMapRobot

This is a project where we use a raspberry pi 4 with a Thymio II to create an autonomous vehicle able to map a room physically and by it's wifi intensity.

## What do you need?

* Raspberry Pi 4
* Thymio II
* Servo Motor
* Laser (Time of Flight sensor)
* Battery
* We 3D printed piece but you might get way with tape and blue tack
* Jumper cables
* USB-C to USB cable
* Micro-USB to USB cable

## How do you use the code?

To use our code any Python IDE should be fine. Download the repository keep all the functions in the same folder as the main. You can change the parameters at the beginning of the Main.
The Main will call 3 functions: odometry,sweep and save.

* The Mapper and mapperNew are two code to lunch once you obtain the data of the main code. They will create a map of the surrounding. 
* The odometry function contain everything to control the wheels of the thymio using an odometric system.
* The sweep function combine the data of the laser with the servo motor rotation to harvest the position of the surrouding.
* The save function save the data of the sweep function in a .cvs file.

## More details

* The pdf containing the full report of the project is present in the repository
* A video of the project is avaible on Youtube: https://youtu.be/JUGqk_iCWYM

## Contact

If you have any question of ways of improving the project you can contct me at: a020598k@student.staffs.ac.uk
